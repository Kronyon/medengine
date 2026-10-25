"""One-off engine patch for v1.4: skeleton card, red-flag card and browse view, test-me pictures, history close.
Fails loudly if run twice. Already applied for v1.4.0; later tweaks were made to app_script.html directly."""
import pathlib
P = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'app_script.html'
s = P.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# ---- data handles
rep("const FFP = D.ffp || [];", "const FFP = D.ffp || [], RF = D.rf || [], URG = D.urg || {}, SKEL = D.skel || {}, rfById = Object.fromEntries(RF.map(r => [r.id, r]));\nconst HXT = new Set(['hx', 'psych']);\nconst closeKey = st => HXT.has(typeOf(st)) && FR.hxclose ? 'hxclose' : 'close';")

# ---- histories close with thanks, not a plan and safety-net
rep("    add('close', 'Closing', frameItems('close'));\n    return secs;\n  }\n  const pk = packFor(st)",
    "    add(closeKey(st), 'Closing', frameItems(closeKey(st)));\n    return secs;\n  }\n  const pk = packFor(st)")
rep("  add('close', 'Closing', frameItems('close').filter(it => !(hasExpl && /^(Check understanding|Safety-net)/.test(it.t))));\n  return secs;",
    "  add(closeKey(st), 'Closing', frameItems(closeKey(st)).filter(it => !(hasExpl && /^(Check understanding|Safety-net)/.test(it.t))));\n  return secs;")
rep("  fl('close', 'Close', true);\n  return L;", "  fl(closeKey(st), 'Close', true);\n  return L;")

# ---- the station-specific card gets its new name
rep("<summary>🪝 Hooks, triggers and the money line</summary>", "<summary>🎯 Only remember for this one</summary>")


# ---- skeleton + red flags cards
CARDS = r'''
function skelCardHtml(st){
  const k = SKEL[st.skel]; if (!k) return '';
  return '<details class="hk sk" id="skelCard"><summary>🧱 Skeleton: the same in every ' + esc(k.t.replace(/^Every /, '').toLowerCase()) + ' station</summary><div class="body"><div class="skrow">' + k.chips.map((c, i) => '<span>' + esc(c) + '</span>' + (i < k.chips.length - 1 ? '<i>→</i>' : '')).join('') + '</div>' + k.mn.map(([a, b]) => '<div class="mn"><b>' + esc(a) + '</b><span>' + rich(b) + '</span></div>').join('') + '</div></details>';
}
const URGL = () => Object.entries(URG).map(([k, [e, l]]) => '<span>' + e + ' ' + esc(l) + '</span>').join('');
function rfRows(sh, q){ return sh.rows.filter(r => !q || r.join(' ').toLowerCase().includes(q)).map(([f, th, u, d]) => '<div class="rfr"><span class="u" title="' + esc((URG[u] || ['', ''])[1]) + '">' + (URG[u] || ['•'])[0] + '</span><span><b>' + rich(f) + '</b> → ' + esc(th) + '<span class="s">' + rich(d) + '</span></span></div>').join(''); }
function rfCardHtml(st){
  const L = (st.rf || []).map(id => rfById[id]).filter(Boolean); if (!L.length) return '';
  return '<details class="hk rf" id="rfCard"><summary>🚩 Red flags → where to send <span class="hint">· ' + esc(L.map(x => x.t).join(' · ')) + '</span></summary><div class="body"><div class="urg">' + URGL() + '</div>' + L.map(sh => (L.length > 1 ? '<span class="hkh">' + esc(sh.t) + '</span>' : '') + rfRows(sh)).join('') + '<button class="btn sm" data-go="rf">🚩 Every red flag ↗</button></div></details>';
}
function vRf(m){
  const q = (S.set.rfq || '').toLowerCase().trim();
  m.innerHTML = '<section class="card"><span class="eyebrow">History stations · UK guidance</span><h1>🚩 Red flags → where to send</h1><p class="hint" style="margin:0">One sheet per presentation, covering every ILO condition. Read across: <b>the flag</b> → what it means, then what you do and how fast. Ask these in every history, then say the referral in your plan.</p><div class="urg">' + URGL() + '</div><input class="sel" id="rfQ" type="search" placeholder="Filter, e.g. dysphagia, 2 weeks, testis" value="' + esc(S.set.rfq || '') + '" aria-label="Filter red flags"></section><div id="rfList">' + rfListHtml(q) + '</div>';
}
function rfListHtml(q){ const h = RF.map(sh => { const r = rfRows(sh, q); return r ? '<details class="dd"' + (q ? ' open' : '') + '><summary>' + esc(sh.t) + ' <span class="hint">· ' + sh.rows.length + '</span></summary><div class="body">' + r + '</div></details>' : ''; }).join(''); return h || '<p class="hint">Nothing matches.</p>'; }
'''
rep("function scriptFor(st, vk){", CARDS.strip() + "\nfunction scriptFor(st, vk){")
rep("  $('#hookWrap').innerHTML = hookHtml(", "  $('#hookWrap').innerHTML = skelCardHtml(st) + rfCardHtml(st) + hookHtml(")
rep("  const hc = $('#hookCard'); if (hc) hc.open = md === 'script';",
    "  const hc = $('#hookCard'); if (hc) hc.open = md === 'script';\n  ['#skelCard', '#rfCard'].forEach(q => { const c = $(q); if (c) c.open = md === 'script'; });")

# ---- routes
rep("const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp'];", "const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp', 'rf'];")
rep("({type: vType, ffp: vFfp,", "({type: vType, ffp: vFfp, rf: vRf,")
rep("route.v === 'home' || route.v === 'ffp' ? 'home' : '';", "route.v === 'home' || route.v === 'ffp' ? 'home' : route.v === 'rf' ? 'ty:hx' : '';")
rep("<span class=\"hint\">More:</span><button class=\"btn sm\" data-go=\"hooks\">🪝 Hook drill</button>", "<span class=\"hint\">More:</span><button class=\"btn sm\" data-go=\"rf\">🚩 Red flags</button><button class=\"btn sm\" data-go=\"hooks\">🪝 Hook drill</button>")
rep("<button class=\"btn sm\" data-randty=\"' + k + '\">🎲 Random</button></div></section>", "<button class=\"btn sm\" data-randty=\"' + k + '\">🎲 Random</button>' + (HXT.has(k) ? '<button class=\"btn sm\" data-go=\"rf\">🚩 Red flags → where to send</button>' : '') + '</div>' + (SKEL[k === 'psych' ? 'psych' : k === 'drug' ? 'counsel' : k === 'ex' ? 'exam' : k] ? skelCardHtml({skel: k === 'psych' ? 'psych' : k === 'drug' ? 'counsel' : k === 'ex' ? 'exam' : k}).replace('<details class=\"hk sk\" id=\"skelCard\">', '<details class=\"hk sk\" open>') : '') + '</section>")
rep("document.addEventListener('input', e => { if (e.target.id === 'tQ') {",
    "document.addEventListener('input', e => { if (e.target.id === 'rfQ') { S.set.rfq = e.target.value; clearTimeout(vRf.t); vRf.t = setTimeout(() => { save(); $('#rfList').innerHTML = rfListHtml(e.target.value.toLowerCase().trim()); }, 180); return; } if (e.target.id === 'tQ') {")

# ---- pictures: test-me toggle (retrieval practice)
rep("<summary>🖼️ Pictures <span class=\"hint\">· ' + ids.length + ' · tap ▶ to play, or swipe</span></summary><div class=\"body\">",
    "<summary>🖼️ Pictures <span class=\"hint\">· ' + ids.length + ' · tap ▶ to play, or swipe</span></summary><div class=\"body\"><div class=\"row dgtools\"><label class=\"hint\"><input type=\"checkbox\" data-dgtest' + (S.set.dgtest ? ' checked' : '') + '> 🙈 Test me: hide the words, say them, tap to check</label></div>")
rep("  if (t.dataset && t.dataset.tick) {", "  if (t.dataset && t.dataset.dgtest != null) { S.set.dgtest = t.checked; save(); document.body.classList.toggle('dg-testing', !!S.set.dgtest); return; }\n  if (t.dataset && t.dataset.tick) {")
rep("function vStation(m){\n", "function vStation(m){\n  document.body.classList.toggle('dg-testing', !!S.set.dgtest);\n")
rep("function leaveStation(){ if (window.DG) DG.stopAll();", "function leaveStation(){ document.body.classList.remove('dg-testing'); if (window.DG) DG.stopAll();")

P.write_text(s, encoding='utf-8')
print('patched', P)
