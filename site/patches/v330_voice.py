#!/usr/bin/env python3
"""v3.3.0 voice patience for site/osce.html (applied once; kept as a record).

v3.2.0 sent your words 0.7 s after the recogniser's last final result (1.3 s mid-word), so a
normal thinking pause made the patient jump in. Now:
  - default wait 2.5 s after your last word; 1.5 / 3.5 / 5 s or "only when I tap Send"
  - +1.5 s when you trail off on "and / so / because / um / the ..." (semantic patience)
  - a countdown bar with ➤ Send now (Enter) and ✋ Hold (Esc)
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'osce.html'
t = F.read_text(encoding='utf-8')


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


# 1. settings
t = one(t, """'<label>Pause before the patient replies<select class="sel" id="vPauseSel">' + [['500', 'Short (fastest)'], ['700', 'Normal'], ['1100', 'Long (I pause a lot)']].map(([v, l]) => opt(String(S.set.vPause || 700), v, l)).join('') + '</select></label>'""",
        """'<label>Wait after I stop talking<select class="sel" id="vPauseSel">' + [['1500', '1.5 s (quick)'], ['2500', '2.5 s (default)'], ['3500', '3.5 s (relaxed)'], ['5000', '5 s (I think out loud)'], ['tap', 'Only when I tap ➤ Send or press Enter']].map(([v, l]) => opt(String(S.set.vWait || '2500'), v, l)).join('') + '</select></label>'""")
t = one(t, "if (t.id === 'vPauseSel') { S.set.vPause = +t.value; return save(); }",
        "if (t.id === 'vPauseSel') { S.set.vWait = t.value; save(); return vArm(); }")

# 2. arm the patient timer on every bit of speech
t = one(t, "if (!S.set.vPtt) { clearTimeout(VO.cT); VO.cT = setTimeout(vCommit, VO.interim ? 1300 : +(S.set.vPause || 700)); }",
        "if (!S.set.vPtt) vArm();")

# 3. reset the countdown after each send
t = one(t, "  VO.buf = ''; VO.interim = ''; VO.segStart = 0; const live = $('#vLive'); if (live) live.textContent = '';\n",
        "  VO.buf = ''; VO.interim = ''; VO.segStart = 0; const live = $('#vLive'); if (live) live.textContent = '';\n  VO.wEnd = 0; VO.hold = false; vWaitPaint();\n")

PATIENCE = r"""
/* ---------- v3.3.0 ⏳ voice patience: wait after your last word, longer if you trail off, and show it ---------- */
const V_TRAIL = /\b(and|but|so|because|cos|cause|um+|erm+|uh+|er+|ah+|like|the|a|an|to|of|with|or|if|then|which|that|is|are|was|were|i'm|i|my|your|any|have|has|about|for|in|on|at|any)\s*$/i;
function vWaitMs(){ const w = String(S.set.vWait || '2500'); return w === 'tap' ? 0 : Math.max(1200, +w || 2500); }
function vArm(){
  if (!VO) return;
  clearTimeout(VO.cT); cancelAnimationFrame(VO.wRaf || 0);
  const text = (VO.buf + ' ' + (VO.interim || '')).trim();
  const base = vWaitMs();
  if (!text || !base || VO.hold) { VO.wEnd = 0; return vWaitPaint(); }
  const ms = base + (VO.interim ? 700 : 0) + (V_TRAIL.test(text) ? 1500 : 0);
  VO.wEnd = Date.now() + ms; VO.wLen = ms;
  VO.cT = setTimeout(vCommit, ms);
  vWaitPaint();
}
function vWaitPaint(){
  const box = $('#vWait'); if (!box) return;
  const text = VO ? (VO.buf + ' ' + (VO.interim || '')).trim() : '';
  if (!VO || !VO.on || VO.busy || VO.speaking || !text || S.set.vPtt) { box.hidden = true; return; }
  box.hidden = false;
  const bar = $('#vWaitBar'), lab = $('#vWaitLab'), hb = $('[data-vhold]');
  if (hb) hb.textContent = VO.hold ? '▶ Resume' : '✋ Hold';
  if (!vWaitMs() || VO.hold || !VO.wEnd) {
    if (bar) bar.style.width = '100%';
    if (lab) lab.textContent = VO.hold ? 'Holding. Tap ➤ Send (or press Enter) when you have finished.' : 'Tap ➤ Send (or press Enter) when you have finished.';
    return;
  }
  const tick = () => {
    if (!VO || !VO.wEnd) return;
    const left = Math.max(0, VO.wEnd - Date.now());
    if (bar) bar.style.width = (left / VO.wLen * 100).toFixed(1) + '%';
    if (lab) lab.textContent = 'Sending in ' + (left / 1000).toFixed(1) + ' s · keep talking to add more · Enter sends now · Esc holds';
    if (left > 0) VO.wRaf = requestAnimationFrame(tick);
  };
  tick();
}
function vSendNow(){ if (!VO || !VO.on) return; VO.hold = false; clearTimeout(VO.cT); VO.wEnd = 0; vCommit(); }
function vHoldToggle(){ if (!VO || !VO.on) return; VO.hold = !VO.hold; vArm(); }
function vCommit(){"""
t = one(t, "\nfunction vCommit(){", PATIENCE)

# 4. the countdown strip under the live transcript
t = one(t, """<div class="grow" style="min-width:0"><b id="vStatus" aria-live="polite">Ready when you are</b><div class="vlive" id="vLive"></div></div></div>'""",
        """<div class="grow" style="min-width:0"><b id="vStatus" aria-live="polite">Ready when you are</b><div class="vlive" id="vLive"></div></div></div>'
    + '<div class="vwait" id="vWait" hidden><div class="vwait-track"><i id="vWaitBar"></i></div><div class="row vwait-row"><span class="hint grow" id="vWaitLab"></span><button class="btn sm" data-vhold>✋ Hold</button><button class="btn sm primary" data-vsendnow>➤ Send</button></div></div>'""")
t = one(t, ".vptt{user-select:none;", ".vwait{margin:6px 0 2px}\n.vwait-track{height:5px;border-radius:99px;background:var(--line);overflow:hidden}\n.vwait-track i{display:block;height:100%;width:100%;background:var(--accent);border-radius:99px}\n.vwait-row{gap:6px;align-items:center;flex-wrap:wrap;margin-top:4px}\n.vptt{user-select:none;")

# 5. buttons and keys
t = one(t, "  if (d.vsend != null) { const ta = $('#vSay')", "  if (d.vsendnow != null) return vSendNow();\n  if (d.vhold != null) return vHoldToggle();\n  if (d.vsend != null) { const ta = $('#vSay')")
t = one(t, "  if (e.target.id === 'vSay' && e.key === 'Enter' && !e.shiftKey) {",
        "  if (cur && cur.mode === 'voice' && VO && VO.on && !/^(TEXTAREA|INPUT|SELECT)$/.test(e.target.tagName) && (VO.buf || VO.interim)) {\n    if (e.key === 'Enter') { e.preventDefault(); return vSendNow(); }\n    if (e.key === 'Escape') { e.preventDefault(); return vHoldToggle(); }\n  }\n  if (e.target.id === 'vSay' && e.key === 'Enter' && !e.shiftKey) {")

F.write_text(t, encoding='utf-8')
print('voice patch applied')
