/* ---------- v2.3: 🔨 Hammer SBAs: 3 graded single-best-answer questions for every ILO condition, drug group, test and procedure,
   the off-map topics your mock tested, and your mock's own questions (D.hq from snap/hq_*.py, D.mock from snap/mock92.json + mock_meta.py) ---------- */
const HQ = D.hq || {q: [], tt: {}, pat: {}, al: {}};
const MOCK = D.mock || {q: []};
const HQ_SRC = [['all', '🔨', 'Everything'], ['u', '🩺', 'Conditions'], ['d', '💊', 'Drugs'], ['x', '🛠️', 'Tests and procedures'], ['b', '🧭', 'Off the map'], ['m', '🎓', 'My mock']];
const HQ_PI = {L: '👯', N: '🔢', T: '📍', D: '💊', R: '🪜'};
const HAM = n => '🔨'.repeat(n);
let hqCfg = {src: 'all', h: 0, p: '', sys: '', st: '', tgt: ''};
let hqSess = null;
/* every item, hammers and mock, in one shape: {id, t, k, h, p, s, o, a, w, f, ref?} */
function hqAll(){
  if (hqAll.c) return hqAll.c;
  return hqAll.c = HQ.q.concat(MOCK.q.map(m => Object.assign({t: 'm', k: String(m.u)}, m)));
}
function hqUnitOf(it){ return it.t === 'u' || it.t === 'm' ? +it.k : null; }
function hqTitle(it){
  if (it.t === 'u') return (UNITS[+it.k] || {}).name || '';
  if (it.t === 'm') return '🎓 Mock Q' + it.n + ' · ' + ((UNITS[+it.k] || {}).name || '');
  return HQ.tt[it.t + ':' + it.k] || it.k;
}
function hqStat(id){ S.hq = S.hq || {}; return S.hq[id]; }
function hqMark(id, ok){ S.hq = S.hq || {}; const r = S.hq[id] || [0, 0, 0]; r[0] += ok ? 1 : 0; r[1] += 1; r[2] = ok ? 1 : 0; S.hq[id] = r; save(); }
function hqFilter(){
  const c = hqCfg;
  return hqAll().filter(it => {
    if (c.tgt) return c.tgt === 'mq:' + it.id || c.tgt === it.t + ':' + it.k || (c.tgt[0] === 'u' && it.t === 'm' && 'u:' + it.k === c.tgt);
    if (c.src !== 'all' && it.t !== c.src) return false;
    if (c.h && it.h !== c.h) return false;
    if (c.p && it.p !== c.p) return false;
    if (c.sys) { const ui = hqUnitOf(it); if (ui == null || !UNITS[ui] || usys(UNITS[ui]) !== c.sys) return false; }
    const st = hqStat(it.id);
    if (c.st === 'new' && st) return false;
    if (c.st === 'miss' && !(st && st[2] === 0)) return false;
    return true;
  });
}
function hqCount(){ return hqAll().length; }
/* the button on each condition page: its own 3 hammers, plus any mock question on it */
function hqUnitBtn(u){
  const k = String(HQ.al && HQ.al[u.i] != null ? HQ.al[u.i] : u.i);
  const n = HQ.q.filter(q => q.t === 'u' && q.k === k).length, mk = MOCK.q.filter(m => String(m.u) === k).length;
  if (!n && !mk) return '';
  const done = HQ.q.filter(q => q.t === 'u' && q.k === k && hqStat(q.id)).length;
  return '<div class="srcs hq-row"><button class="src hq-go" data-hqtgt="u:' + k + '">🔨 ' + n + ' hammer SBAs' + (done ? ' · ' + done + ' done' : '') + '</button>' + (mk ? '<span class="hint">includes ' + mk + ' from your mock 🎓</span>' : '') + '</div>';
}
/* ----- the blueprint: what the mock actually tested, computed from the paper ----- */
function hqBlueprint(){
  const M = MOCK.q; if (!M.length) return '';
  const bySys = {}, byH = [0, 0, 0, 0], byP = {}, src = {NOT: 0, MSCAA: 0}, ty = {dx: 0, mx: 0, ix: 0, oth: 0};
  M.forEach(m => {
    const u = UNITS[m.u]; const s = u ? usys(u) : 'haemid'; bySys[s] = (bySys[s] || 0) + 1;
    byH[m.h]++; byP[m.p] = (byP[m.p] || 0) + 1;
    if (/^MSCAA/i.test(m.ref || '')) src.MSCAA++; else src.NOT++;
    const st = m.s.toLowerCase();
    if (/most likely (diagnosis|cause)|likely to explain|term to describe|most likely to be responsible|which (virus|organism|artery|cranial nerve|group of lymph)/.test(st)) ty.dx++;
    else if (/management|treatment|next step|action|therapy|psychotherapy|antithrombotic|class of medication|manage/.test(st)) ty.mx++;
    else if (/investigation|imaging|test|diagnostic/.test(st)) ty.ix++; else ty.oth++;
  });
  const bar = (lab, n, max) => '<div class="hq-bar"><span class="hq-bl">' + lab + '</span><span class="hq-bt"><i style="width:' + Math.round(n / max * 100) + '%"></i></span><b>' + n + '</b></div>';
  const sys = Object.entries(bySys).sort((a, b) => b[1] - a[1]), mx = sys[0][1];
  let h = '<details class="panel hq-bp"' + (S.set.hqBp ? ' open' : '') + '><summary>📊 Your mock blueprint · ' + M.length + ' questions</summary><div class="hq-bpg"><div><h6>By system</h6>' + sys.map(([s, n]) => bar(esc(MEV.sysLabel(s) || s), n, mx)).join('') + '</div><div><h6>What the stem asks</h6>'
    + bar('🔎 Diagnosis or cause', ty.dx, M.length) + bar('💊 Management', ty.mx, M.length) + bar('🧪 Investigation', ty.ix, M.length) + bar('🧠 Mechanism, anatomy, law', ty.oth, M.length)
    + '<h6>Paper</h6>' + bar('Nottingham items', src.NOT, M.length) + bar('MSCAA items', src.MSCAA, M.length)
    + '<h6>Hammer rating</h6>' + [1, 2, 3].map(n => bar(HAM(n), byH[n], M.length)).join('')
    + '<h6>Pattern tested</h6>' + Object.entries(byP).sort((a, b) => b[1] - a[1]).map(([p, n]) => bar(HQ_PI[p] + ' ' + esc(HQ.pat[p] || p), n, M.length)).join('') + '</div></div>'
    + '<ul class="hq-take"><li><b>Half the paper is “most likely diagnosis”.</b> The stem tells a story and one word flips it to the sibling. That is the 👯 lookalike pattern: train it with 🔨🔨.</li>'
    + '<li><b>The small systems punch above their weight.</b> Eye, ENT and skin together match psychiatry. Each is a pool of 5 siblings sharing one option list.</li>'
    + '<li><b>🪜 Right rung:</b> when a stem asks for the <i>first</i> or <i>initial</i> step, the answer is the safe bedside one, not the definitive fix. Erect X-ray before laparotomy; needle before drain; cultures before antibiotics.</li>'
    + '<li><b>Off-map items</b> came from just outside the ILO titles: otosclerosis, CSF leak, Budd-Chiari, Capgras, grief, GPA, gut blood supply, node drainage. They sit under 🧭.</li></ul></details>';
  return h;
}
function viewHammer(m){
  if (hqSess) { session = hqSess; return hqDraw(m); }
  const c = hqCfg, list = hqFilter(), all = hqAll();
  const done = all.filter(it => hqStat(it.id)).length, miss = all.filter(it => { const s = hqStat(it.id); return s && s[2] === 0; }).length;
  const chip = (k, v, lab) => '<button class="chip' + (String(c[k]) === String(v) ? ' on' : '') + '" data-hqset="' + k + ':' + v + '">' + lab + '</button>';
  let h = '<div class="wrap hq-wrap"><div class="ph"><div class="crumbs"><span class="code">🔨 Hammer</span></div><h1>Hammer SBAs</h1><p class="hint" style="margin:0">Three questions for every ILO condition, drug group, test and procedure, plus the off-map topics and your own mock. <b>🔨</b> the classic picture · <b>🔨🔨</b> two steps, a lookalike or a number that overrides the story · <b>🔨🔨🔨</b> the curveball. After each answer, <b>🔄 the flip</b> shows the one change that would make another option right. Keys: <span class="kbd">A</span>–<span class="kbd">E</span> or <span class="kbd">1</span>–<span class="kbd">5</span>, <span class="kbd">Enter</span> next, <span class="kbd">Esc</span> leave.</p></div>';
  h += '<div class="tiles">' + [[all.length, 'Questions'], [done, 'Answered'], [miss, 'Missed last time'], [MOCK.q.length, 'From your mock']].map(([v, l]) => '<div class="tile"><div class="v">' + v + '</div><div class="l">' + l + '</div></div>').join('') + '</div>';
  h += hqBlueprint();
  if (c.tgt) {
    h += '<div class="panel"><div class="toolbar"><b class="grow">' + esc(hqTitle(list[0] || {t: c.tgt[0], k: c.tgt.slice(2)})) + ' · ' + list.length + ' questions</b><button class="btn ghost sm" data-hqset="tgt:">✕ Show everything</button></div></div>';
  } else {
    h += '<div class="panel hq-f"><div class="chips">' + HQ_SRC.map(([k, ic, l]) => chip('src', k, ic + ' ' + l + ' · ' + (k === 'all' ? all.length : all.filter(it => it.t === k).length))).join('') + '</div>'
      + '<div class="chips">' + chip('h', 0, 'Any hammer') + [1, 2, 3].map(n => chip('h', n, HAM(n))).join('') + '<span class="hq-sep"></span>' + chip('p', '', 'Any pattern') + Object.keys(HQ.pat).map(p => chip('p', p, HQ_PI[p] + ' ' + esc(HQ.pat[p]))).join('') + '</div>'
      + '<div class="chips">' + chip('st', '', 'All') + chip('st', 'new', '🆕 Not done') + chip('st', 'miss', '🔥 Missed last time') + '<label class="hq-sys">System <select data-hqsys aria-label="Filter by system"><option value="">All systems</option>' + MEV.sysOptions(c.sys) + '</select></label></div></div>';
  }
  h += '<div class="panel"><div class="toolbar"><b class="grow">' + list.length + ' match</b>' + (list.length ? '<button class="btn primary" data-hqstart="20">▶ Start ' + Math.min(20, list.length) + '</button>' + (list.length > 20 ? '<button class="btn" data-hqstart="0">Start all ' + list.length + '</button>' : '') : '') + '</div>';
  if (!c.tgt && c.src !== 'all') h += hqIndex(list);
  h += '</div></div>';
  m.innerHTML = h;
}
/* list of targets in the current source, each opening its own 3 */
function hqIndex(list){
  const seen = new Map();
  list.forEach(it => { const k = it.t === 'm' ? 'mq:' + it.id : it.t + ':' + it.k; if (!seen.has(k)) seen.set(k, [it, 0]); seen.get(k)[1]++; });
  return '<div class="hq-idx">' + Array.from(seen.entries()).map(([k, [it, n]]) => '<button class="sr" data-hqtgt="' + esc(k) + '"><span class="where">' + (it.t === 'm' ? '🎓' : HAM(1)) + ' ' + n + '</span>' + esc(it.t === 'm' ? 'Q' + it.n + ' · ' + ((UNITS[+it.k] || {}).name || '') : hqTitle(it)) + '</button>').join('') + '</div>';
}
function hqStart(n){
  let list = hqFilter();
  if (!hqCfg.tgt) list = shuffle(list, rng(Date.now() & 0xffffffff));
  else list = list.slice().sort((a, b) => a.h - b.h || (a.t === 'm') - (b.t === 'm'));
  if (n) list = list.slice(0, n);
  if (!list.length) return;
  hqSess = {kind: 'hammer', list, i: 0, pick: null, res: []};
  session = hqSess; hqDraw($('#main')); window.scrollTo({top: 0});
}
function hqDraw(m){
  const s = hqSess; m = m || $('#main');
  if (s.i >= s.list.length) return hqEnd(m);
  const it = s.list[s.i], L = 'ABCDE', ans = s.pick != null;
  let h = '<div class="wrap hq-wrap"><div class="ph"><div class="crumbs"><span class="code">🔨 ' + (s.i + 1) + ' / ' + s.list.length + '</span><span class="grow"></span><button class="btn ghost sm" data-hqexit>✕ Leave</button></div>';
  h += '<div class="hq-tag"><span>' + esc(hqTitle(it)) + '</span><span class="hq-h">' + HAM(it.h) + '</span><span class="hq-p">' + HQ_PI[it.p] + ' ' + esc(HQ.pat[it.p] || '') + '</span>' + (it.ref ? '<span class="hq-ref">' + esc(it.ref) + '</span>' : '') + '</div></div>';
  h += '<div class="panel hq-q"><p class="hq-s">' + esc(it.s) + '</p><div class="hq-os">';
  it.o.forEach((o, i) => {
    let cl = 'hq-o';
    if (ans) cl += i === it.a ? ' ok' : i === s.pick ? ' bad' : ' dim';
    h += '<button class="' + cl + '" data-hqpick="' + i + '"' + (ans ? ' disabled' : '') + '><span class="hq-l">' + L[i] + '</span><span>' + esc(o) + '</span></button>';
  });
  h += '</div>';
  if (ans) {
    const ok = s.pick === it.a;
    h += '<div class="hq-why ' + (ok ? 'ok' : 'bad') + '"><b>' + (ok ? '✅ Right.' : '❌ ' + L[it.a] + ' is the answer.') + '</b> ' + esc(it.w || '') + '</div>';
    if (it.f) h += '<div class="hq-flip"><span class="hq-fl">🔄 Flip it</span>' + esc(it.f).replace('→', '<b class="hq-arr">→</b>') + '</div>';
    const ui = hqUnitOf(it);
    h += '<div class="toolbar">' + (ui != null && UNITS[ui] ? '<button class="btn ghost sm" data-u="' + ui + '" data-mode="read">📖 Notes</button><button class="btn ghost sm" data-trjump="' + ui + '">🧲 Triggers</button>' : '') + '<span class="grow"></span><button class="btn primary" data-hqnext>' + (s.i + 1 < s.list.length ? 'Next →' : 'Finish') + ' <span class="kbd">Enter</span></button></div>';
  }
  h += '</div></div>';
  m.innerHTML = h;
}
function hqPick(i){
  const s = hqSess; if (!s || s.pick != null) return;
  const it = s.list[s.i]; s.pick = i; const ok = i === it.a;
  s.res.push([it, ok]); hqMark(it.id, ok); if (ok) addXp(it.h * 2);
  hqDraw();
}
function hqNext(){ const s = hqSess; if (!s || s.pick == null) return; s.i++; s.pick = null; hqDraw(); window.scrollTo({top: 0}); }
function hqEnd(m){
  const s = hqSess, r = s.res, ok = r.filter(x => x[1]).length;
  const byP = {}; r.forEach(([it, g]) => { const b = byP[it.p] || (byP[it.p] = [0, 0]); b[1]++; if (g) b[0]++; });
  const wrong = r.filter(x => !x[1]).map(x => x[0]);
  let h = '<div class="wrap hq-wrap"><div class="ph"><h1>🔨 ' + ok + ' / ' + r.length + '</h1><p class="hint" style="margin:0">Where the points went, by pattern. The weakest row is what to drill next.</p></div><div class="panel">';
  Object.entries(byP).sort((a, b) => a[1][0] / a[1][1] - b[1][0] / b[1][1]).forEach(([p, [g, n]]) => h += '<div class="hq-bar"><span class="hq-bl">' + HQ_PI[p] + ' ' + esc(HQ.pat[p] || p) + '</span><span class="hq-bt"><i style="width:' + Math.round(g / n * 100) + '%"></i></span><b>' + g + '/' + n + '</b></div>');
  h += '</div>';
  if (wrong.length) h += '<div class="panel"><h6>🔄 Flips you missed</h6>' + wrong.map(it => '<div class="hq-flip"><span class="hq-fl">' + esc(hqTitle(it)) + '</span>' + esc(it.f || '') + '</div>').join('') + '</div>';
  h += '<div class="toolbar">' + (wrong.length ? '<button class="btn primary" data-hqretry>🔥 Redo the ' + wrong.length + ' missed</button>' : '') + '<button class="btn" data-hqexit>Back to the list</button></div></div>';
  m.innerHTML = h;
  s.wrong = wrong;
}
function hqKey(e){
  const s = hqSess; if (!s) return false;
  if (e.key === 'Escape') { hqSess = null; render(); return true; }
  if (s.i >= s.list.length) return false;
  const k = e.key.toUpperCase(), idx = 'ABCDE'.indexOf(k) >= 0 ? 'ABCDE'.indexOf(k) : /^[1-5]$/.test(e.key) ? +e.key - 1 : -1;
  if (s.pick == null && idx >= 0 && idx < s.list[s.i].o.length) { e.preventDefault(); hqPick(idx); return true; }
  if (s.pick != null && (e.key === 'Enter' || e.key === 'ArrowRight' || k === 'N')) { e.preventDefault(); hqNext(); return true; }
  return idx >= 0;
}
/* search: hammer stems that mention the term */
function hqSearchHtml(q, has){
  const n = hqAll().filter(it => has((it.s + ' ' + it.o.join(' ')).toLowerCase())).length;
  return n ? '<h6>🔨 Hammer SBAs</h6><button class="sr" data-hqq="' + esc(q) + '"><span class="where">🔨 ' + n + '</span>Practise every question that mentions “' + esc(q) + '”</button>' : '';
}
document.addEventListener('click', e => {
  const t = e.target.closest && e.target.closest('[data-hqset],[data-hqstart],[data-hqpick],[data-hqnext],[data-hqexit],[data-hqretry],[data-hqtgt],[data-hqq]'); if (!t) return;
  const d = t.dataset; e.preventDefault(); e.stopImmediatePropagation();
  const sp = document.getElementById('sp'); if (sp) sp.hidden = true;
  if (d.hqset != null) { const i = d.hqset.indexOf(':'), k = d.hqset.slice(0, i), v = d.hqset.slice(i + 1); hqCfg[k] = k === 'h' ? +v : v; if (k === 'tgt' && !v) hqCfg.tgt = ''; return viewHammer($('#main')); }
  if (d.hqstart != null) return hqStart(+d.hqstart);
  if (d.hqpick != null) return hqPick(+d.hqpick);
  if (d.hqnext != null) return hqNext();
  if (d.hqexit != null) { hqSess = null; return route.view === 'hammer' ? render() : go({view: 'hammer'}); }
  if (d.hqretry != null) { const w = hqSess.wrong; hqSess = {kind: 'hammer', list: w, i: 0, pick: null, res: []}; session = hqSess; return hqDraw(); }
  if (d.hqtgt != null) { hqCfg.tgt = d.hqtgt; hqSess = null; if (route.view !== 'hammer') { route = {view: 'hammer'}; try { history.replaceState(null, '', '#hammer'); } catch(x) {} renderSide(); } return hqStart(0); }
  if (d.hqq != null) {
    const q = d.hqq.toLowerCase(); const list = hqAll().filter(it => (it.s + ' ' + it.o.join(' ')).toLowerCase().includes(q));
    hqSess = {kind: 'hammer', list, i: 0, pick: null, res: []};
    if (route.view !== 'hammer') { route = {view: 'hammer'}; try { history.replaceState(null, '', '#hammer'); } catch(x) {} renderSide(); }
    session = hqSess; const qi = document.getElementById('q'); if (qi) qi.blur(); return hqDraw();
  }
}, true);
document.addEventListener('change', e => { const t = e.target; if (t.dataset && t.dataset.hqsys != null) { hqCfg.sys = t.value; viewHammer($('#main')); } });
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('hq-bp')) { S.set.hqBp = e.target.open; save(); } }, true);
