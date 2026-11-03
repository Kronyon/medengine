#!/usr/bin/env python3
"""v3.3.1: get TalkType (or any dictation app) into 📋 Grade without copy-paste gymnastics.

  - osce.html#talk=<text> catches a transcript (an iPhone or Mac Shortcut sends it from the
    share sheet or the clipboard). It is a #fragment, so the text never reaches the web server.
  - The transcript waits for the station you last used (or the one you open next, including a
    🔒 My circuit station after you unlock), fills 📋 Grade and marks it.
  - 📋 Paste & mark button in 📋 Grade reads the clipboard in one tap (website copy).
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'osce.html'
t = F.read_text(encoding='utf-8')


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


if 'medengine-talk-pending' in t:
    raise SystemExit('already applied')

JS = r"""
/* ---------- v3.3.1 🎙️ TalkType → 📋 Grade ---------- */
const TALK_KEY = 'medengine-talk-pending', LAST_ST_KEY = 'medengine-last-station';
let talkMem = '';
function talkPending(v){
  if (v === undefined) { try { return sessionStorage.getItem(TALK_KEY) || talkMem; } catch (e) { return talkMem; } }
  talkMem = v || '';
  try { if (v) sessionStorage.setItem(TALK_KEY, v); else sessionStorage.removeItem(TALK_KEY); } catch (e) {}
}
function talkTake(){
  const m = (location.hash || '').match(/^#talk=([\s\S]*)$/);
  if (!m) return false;
  let txt = m[1];
  try { txt = decodeURIComponent(txt.replace(/\+/g, ' ')); } catch (e) {}
  txt = txt.replace(/\s+/g, ' ').trim().slice(0, 20000);
  if (txt) talkPending(txt);
  let last = ''; try { last = localStorage.getItem(LAST_ST_KEY) || ''; } catch (e) {}
  const target = last && getStation(last) ? '#s-' + last : /^MY\d/.test(last) ? '#my' : '#home';
  try { history.replaceState(null, '', location.pathname + location.search + target); } catch (e) { location.hash = target; }
  setTimeout(() => toast(txt ? (target === '#home' ? '🎙️ Transcript received: open a station to mark it' : target === '#my' ? '🎙️ Transcript received: unlock and open your station' : '🎙️ Transcript received') : 'No text came through'), 400);
  return true;
}
window.addEventListener('hashchange', () => { talkTake(); });
talkTake();
function talkApply(st){
  if (!st) return;
  try { localStorage.setItem(LAST_ST_KEY, st.id); } catch (e) {}
  const txt = talkPending(); if (!txt) return;
  talkPending('');
  setTimeout(() => {
    if (!cur || cur.st !== st) return talkPending(txt);
    setMode('grade');
    ttGradeState.stId = st.id; ttGradeState.open = true; ttGradeState.retryMode = false;
    redrawSniperStationWrap();
    const ta = $('#ttTranscriptInput'); if (ta) ta.value = txt;
    const mk = $('[data-ttmark]'); if (mk) mk.click();
    const gd = $('#gradeDrawer'); if (gd) { gd.open = true; gd.scrollIntoView({behavior: 'smooth', block: 'start'}); }
    toast('🎙️ Transcript marked in 📋 Grade');
  }, 120);
}
async function talkPaste(){
  let txt = '';
  try { txt = (await navigator.clipboard.readText() || '').trim(); } catch (e) { return toast('Paste is blocked here: long-press the box and tap Paste'); }
  if (!txt) return toast('The clipboard is empty');
  const ta = $('#ttTranscriptInput'); if (!ta) return;
  ta.value = txt; ttGradeState.raw = txt;
  const mk = $('[data-ttmark]'); if (mk) mk.click();
}
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ttpaste]'); if (b) talkPaste(); });
"""

# 1. run before the first route is read (the v3.3.0 block sits there already)
anchor = "VIEWS.push('mn', 'my');"
t = one(t, anchor, anchor + '\n' + JS)

# 2. every station render records itself and picks up a waiting transcript
t = one(t, "  const mnw = $('#mnWrap'); if (mnw) mnw.innerHTML = mnCardHtml(st);\n",
        "  const mnw = $('#mnWrap'); if (mnw) mnw.innerHTML = mnCardHtml(st);\n  talkApply(st);\n")

# 3. one-tap paste in 📋 Grade (the claude.ai viewer blocks clipboard reads, so website only)
dict_btn = "  h += '<button type=\"button\" class=\"btn sm tt-dict' + (ttDictState.on ? ' on' : '') + '\" data-ttdictate>' + (ttDictState.on ? '⏹ Stop Mic (' + mmss(ttDictState.sec) + ')' : '🎙️ Dictate') + '</button>';\n"
t = one(t, dict_btn, dict_btn + "  if (!window.MEDENGINE_ARTIFACT) h += '<button type=\"button\" class=\"btn sm\" data-ttpaste title=\"Paste what TalkType copied and mark it\">📋 Paste &amp; mark</button>';\n")

F.write_text(t, encoding='utf-8')
print('v3.3.1 TalkType bridge applied')
