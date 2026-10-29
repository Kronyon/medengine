/* ---------- v2.3: 🔨 Hammer SBAs: 3 graded single-best-answer questions for every ILO condition, drug group, test and procedure,
   the off-map topics your mock tested, and your mock's own questions (D.hq from snap/hq_*.py, D.mock from snap/mock92.json + mock_meta.py) ---------- */
const HQ = D.hq || {q: [], tt: {}, pat: {}, al: {}};
const MOCK = D.mock || {q: []};
/* v2.5: 🏛️ the official papers (MS AKT 2023 P1 and P2; MSCAA 2017, 2018, 2019, 2020) and 🧬 how they repeat */
const OFF = D.off || {q: [], pp: {}, img: {}, g: []};
const HQ_IL = {I: ['🎯', 'In my ILOs'], E: ['🟡', 'ILO edge'], O: ['🌍', 'Outside my ILOs']};
const HQ_GK = {clone: ['🔥', 'Double-tested'], chain: ['⛓️', 'Same patient, next step'], block: ['🚫', 'Comorbidity blocks first line'], decoy: ['⚠️', 'Lab decoy'], matrix: ['🧮', 'One grid, every angle'], twin: ['🔗', 'Same trap, new patient']};
function hqGroupsOf(id){ if (!hqGroupsOf.c) { const m = {}; OFF.g.forEach((g, gi) => g.ids.forEach(x => (m[x] = m[x] || []).push(gi))); hqGroupsOf.c = m; } return hqGroupsOf.c[id] || []; }
function hqInKind(id, k){ return hqGroupsOf(id).some(gi => OFF.g[gi].k === k); }
const HQ_SRC = [['all', '🔨', 'Everything'], ['u', '🩺', 'Conditions'], ['d', '💊', 'Drugs'], ['x', '🛠️', 'Tests and procedures'], ['b', '🧭', 'Off the map'], ['m', '🎓', 'My mock'], ['o', '🏛️', 'Official papers']];
const HQ_PI = {L: '👯', N: '🔢', T: '📍', D: '💊', R: '🪜'};
const HAM = n => '🔨'.repeat(n);
let hqCfg = {src: 'all', h: 0, p: '', sys: '', st: '', tgt: '', pp: '', ilo: '', tr: ''};
let hqSess = null;
/* every item, hammers and mock, in one shape: {id, t, k, h, p, s, o, a, w, f, ref?} */
function hqAll(){
  if (hqAll.c) return hqAll.c;
  return hqAll.c = HQ.q.concat(MOCK.q.map(m => Object.assign({t: 'm', k: String(m.u)}, m)), OFF.q.map(o => Object.assign({t: 'o', k: String(o.u)}, o)));
}
function hqUnitOf(it){ return it.t === 'u' || it.t === 'm' ? +it.k : it.t === 'o' && +it.k >= 0 ? +it.k : null; }
function hqPaper(it){ return (OFF.pp[it.pp] || [it.pp])[0]; }
function hqTitle(it){
  if (it.t === 'u') return (UNITS[+it.k] || {}).name || '';
  if (it.t === 'm') return '🎓 Mock Q' + it.n + ' · ' + ((UNITS[+it.k] || {}).name || '');
  if (it.t === 'o') return '🏛️ ' + hqPaper(it) + ' Q' + it.n + ' · ' + (+it.k >= 0 ? (UNITS[+it.k] || {}).name || '' : 'beyond the ILOs');
  return HQ.tt[it.t + ':' + it.k] || it.k;
}
/* the label shown before you answer: where the question comes from, never what it is about */
function hqSrcLabel(it){ return it.t === 'm' ? '🎓 Mock Q' + it.n : it.t === 'o' ? '🏛️ ' + hqPaper(it) + ' Q' + it.n : '🔨 Hammer SBA'; }
/* a run label that names a topic waits until the question is answered */
function hqLblSafe(l){ return !l || /^(🔥|“)/.test(l); }
function hqStat(id){ S.hq = S.hq || {}; return S.hq[id]; }
function hqMark(id, ok){ S.hq = S.hq || {}; const r = S.hq[id] || [0, 0, 0]; r[0] += ok ? 1 : 0; r[1] += 1; r[2] = ok ? 1 : 0; S.hq[id] = r; save(); }
function hqFilter(){
  const c = hqCfg;
  return hqAll().filter(it => {
    if (c.tgt) return c.tgt.slice(0, 2) === 'g:' ? OFF.g[+c.tgt.slice(2)].ids.includes(it.id) : c.tgt === 'mq:' + it.id || c.tgt === 'oq:' + it.id || c.tgt === it.t + ':' + it.k || (c.tgt[0] === 'u' && (it.t === 'm' || it.t === 'o') && 'u:' + it.k === c.tgt);
    if (c.src !== 'all' && it.t !== c.src) return false;
    if (c.pp && it.pp !== c.pp) return false;
    if (c.ilo && it.il !== c.ilo) return false;
    if (c.tr && !hqInKind(it.id, c.tr)) return false;
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
  const n = HQ.q.filter(q => q.t === 'u' && q.k === k).length, mk = MOCK.q.filter(m => String(m.u) === k).length, ok = OFF.q.filter(o => String(o.u) === k).length;
  if (!n && !mk && !ok) return '';
  const done = HQ.q.filter(q => q.t === 'u' && q.k === k && hqStat(q.id)).length;
  return '<div class="srcs hq-row"><button class="src hq-go" data-hqtgt="u:' + k + '">🔨 ' + n + ' hammer SBAs' + (done ? ' · ' + done + ' done' : '') + '</button>' + (mk || ok ? '<span class="hint">plus ' + [mk ? mk + ' from your mock 🎓' : '', ok ? ok + ' from the official papers 🏛️' : ''].filter(Boolean).join(' and ') + '</span>' : '') + '</div>';
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
  let h = '<div class="wrap hq-wrap"><div class="ph"><div class="crumbs"><span class="code">🔨 Hammer</span></div><h1>Hammer SBAs</h1><p class="hint" style="margin:0">Three questions for every ILO condition, drug group, test and procedure, plus the off-map topics, your own mock and 399 questions from the official practice papers 🏛️. <b>🔨</b> the classic picture · <b>🔨🔨</b> two steps, a lookalike or a number that overrides the story · <b>🔨🔨🔨</b> the curveball. After each answer, <b>🔄 the flip</b> shows the one change that would make another option right. Keys: <span class="kbd">A</span>–<span class="kbd">E</span> or <span class="kbd">1</span>–<span class="kbd">5</span>, <span class="kbd">Enter</span> next, <span class="kbd">S</span> 🦅 scan mode, <span class="kbd">Esc</span> leave.</p></div>';
  h += '<div class="tiles">' + [[all.length, 'Questions'], [done, 'Answered'], [miss, 'Missed last time'], [MOCK.q.length, 'From your mock'], [OFF.q.length, 'Official papers']].map(([v, l]) => '<div class="tile"><div class="v">' + v + '</div><div class="l">' + l + '</div></div>').join('') + '</div>';
  h += hqBlueprint() + hqOffBlueprint() + hqIloAudit();
  h += hqResumeBox();
  if (c.tgt) {
    h += '<div class="panel"><div class="toolbar"><b class="grow">' + esc(hqTitle(list[0] || {t: c.tgt[0], k: c.tgt.slice(2)})) + ' · ' + list.length + ' questions</b><button class="btn ghost sm" data-hqset="tgt:">✕ Show everything</button></div></div>';
  } else {
    h += '<div class="panel hq-f"><div class="chips">' + HQ_SRC.map(([k, ic, l]) => chip('src', k, ic + ' ' + l + ' · ' + (k === 'all' ? all.length : all.filter(it => it.t === k).length))).join('') + '</div>'
      + '<div class="chips">' + chip('h', 0, 'Any hammer') + [1, 2, 3].map(n => chip('h', n, HAM(n))).join('') + '<span class="hq-sep"></span>' + chip('p', '', 'Any pattern') + Object.keys(HQ.pat).map(p => chip('p', p, HQ_PI[p] + ' ' + esc(HQ.pat[p]))).join('') + '</div>'
      + (c.src === 'o' ? '<div class="chips">' + chip('pp', '', 'Every paper') + Object.entries(OFF.pp).map(([k, v]) => chip('pp', k, esc(v[0]) + ' · ' + OFF.q.filter(o => o.pp === k).length)).join('') + '<span class="hq-sep"></span>' + chip('ilo', '', 'Any topic') + Object.entries(HQ_IL).map(([k, v]) => chip('ilo', k, v[0] + ' ' + v[1] + ' · ' + OFF.q.filter(o => o.il === k).length)).join('') + '</div>' : '')
      + '<div class="chips">' + chip('tr', '', '🧬 Any examiner pattern') + Object.entries(HQ_GK).map(([k, v]) => chip('tr', k, v[0] + ' ' + v[1])).join('') + '</div>'
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
  list.forEach(it => { const k = it.t === 'm' ? 'mq:' + it.id : it.t === 'o' ? 'oq:' + it.id : it.t + ':' + it.k; if (!seen.has(k)) seen.set(k, [it, 0]); seen.get(k)[1]++; });
  return '<div class="hq-idx">' + Array.from(seen.entries()).map(([k, [it, n]]) => '<button class="sr" data-hqtgt="' + esc(k) + '"><span class="where">' + (it.t === 'm' ? '🎓' : it.t === 'o' ? '🏛️' : HAM(1)) + ' ' + n + '</span>' + esc(it.t === 'm' ? 'Q' + it.n + ' · ' + ((UNITS[+it.k] || {}).name || '') : it.t === 'o' ? hqPaper(it) + ' Q' + it.n + ' · ' + (+it.k >= 0 ? (UNITS[+it.k] || {}).name || '' : 'beyond the ILOs') : hqTitle(it)) + '</button>').join('') + '</div>';
}
/* ----- a run: Passmedicine-style. Move back and forth, cross options out, leave and come back; it is saved with your progress ----- */
const HQ_BY = {}; function hqItem(id){ if (!HQ_BY._ok) { hqAll().forEach(it => HQ_BY[it.id] = it); HQ_BY._ok = 1; } return HQ_BY[id]; }
/* every unfinished run is kept (newest first, up to HQ_KEEP) so starting a new one never wipes the last */
const HQ_KEEP = 12;
function hqRuns(){
  if (S.hqRun && S.hqRun.ids && S.hqRun.ids.length) { S.hqRuns = S.hqRuns || []; S.hqRuns.unshift(Object.assign({rid: 'r' + (S.hqRun.ts || Date.now())}, S.hqRun)); }
  if (S.hqRun !== undefined) { delete S.hqRun; save(); }
  return S.hqRuns || (S.hqRuns = []);
}
function hqNewRun(list, lbl){
  const ids = list.map(it => it.id), key = ids.join(','), same = hqRuns().find(r => r.ids.join(',') === key);
  if (same && ids.length > 1) return hqResume(same.rid);
  hqSess = {kind: 'hammer', rid: 'r' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), ids, i: 0, pk: {}, x: {}, lbl: lbl || ''};
  hqSave(); session = hqSess; hqDraw($('#main')); window.scrollTo({top: 0});
}
function hqSave(){
  if (!hqSess || hqSess.done || hqSess.rev) return; const R = hqRuns(), rec = {rid: hqSess.rid, ids: hqSess.ids, i: hqSess.i, pk: hqSess.pk, x: hqSess.x, lbl: hqSess.lbl, ts: Date.now()};
  const k = R.findIndex(r => r.rid === hqSess.rid); if (k >= 0) R.splice(k, 1);
  R.unshift(rec); R.length = Math.min(R.length, HQ_KEEP); save();
}
function hqDrop(rid){ S.hqRuns = hqRuns().filter(r => r.rid !== rid); save(); }
function hqResume(rid){
  const R = hqRuns(), r = rid ? R.find(x => x.rid === rid) : R[0]; if (!r || !r.ids || !r.ids.length) return false;
  const ids = r.ids.filter(id => hqItem(id)); if (!ids.length) { hqDrop(r.rid); return false; }
  hqSess = {kind: 'hammer', rid: r.rid, ids, i: Math.min(r.i || 0, ids.length - 1), pk: r.pk || {}, x: r.x || {}, lbl: r.lbl || ''};
  session = hqSess; hqDraw($('#main')); window.scrollTo({top: 0}); return true;
}
function hqAgo(ts){ const m = Math.round((Date.now() - (ts || 0)) / 60000); return m < 1 ? 'just now' : m < 60 ? m + ' min ago' : m < 1440 ? Math.round(m / 60) + ' h ago' : Math.round(m / 1440) + ' d ago'; }
function hqResumeBox(){
  const R = hqRuns().filter(r => r.ids && r.ids.length); if (!R.length) return '';
  return '<div class="panel hq-resume"><h6>⏸ Saved runs · ' + R.length + '</h6>' + R.map(r => {
    const nd = Object.keys(r.pk || {}).length, ok = Object.entries(r.pk || {}).filter(([id, p]) => { const q = hqItem(id); return q && q.a === p; }).length;
    return '<div class="toolbar hq-rrow"><span class="grow"><b>' + esc(r.lbl || '🔀 Mixed run') + '</b> <span class="hint">' + nd + ' of ' + r.ids.length + ' answered' + (nd ? ' · ' + ok + ' right' : '') + ' · ' + hqAgo(r.ts) + '</span></span><button class="btn primary sm" data-hqresume="' + esc(r.rid) + '">▶ Resume at Q' + ((r.i || 0) + 1) + '</button><button class="btn ghost sm" data-hqdrop="' + esc(r.rid) + '" title="Delete this saved run" aria-label="Delete saved run">🗑</button></div>';
  }).join('') + '<p class="hint" style="margin:0">Each run keeps its place, answers and cross-outs. Starting a new run never wipes these; 🏁 End closes one.</p></div>';
}
function hqStart(n){
  let list = hqFilter();
  if (!hqCfg.tgt) list = shuffle(list, rng(Date.now() & 0xffffffff));
  else if (hqCfg.tgt.slice(0, 2) === 'g:') { const ids = OFF.g[+hqCfg.tgt.slice(2)].ids; list = list.slice().sort((a, b) => ids.indexOf(a.id) - ids.indexOf(b.id)); }
  else list = list.slice().sort((a, b) => a.h - b.h || (a.t === 'm') - (b.t === 'm'));
  if (n) list = list.slice(0, n);
  if (!list.length) return;
  hqNewRun(list, hqCfg.tgt ? (hqCfg.tgt.slice(0, 2) === 'g:' ? '🧬 ' + OFF.g[+hqCfg.tgt.slice(2)].t : hqTitle(list[0])) : '');
}
/* 🧲 the trigger lines that belong with a question, shown under the answer */
function hqTrIndex(){
  if (hqTrIndex.c) return hqTrIndex.c;
  const T = D.trg || {}, out = [];
  Object.entries(T.c || {}).forEach(([u, s]) => out.push({c: s[0], a: s[1], u: +u, star: 1}));
  if (window.TG) trgU().units.forEach(u => (u.h || []).forEach(h => out.push({c: h[1], a: h[2], u: u.i})));
  (T.sc || []).forEach(sc => sc[2].forEach(l => out.push({c: l[1], a: l[2] + ' · ' + (((T.bug || {})[l[0]] || [])[0] || ''), g: (((T.bug || {})[l[0]] || [])[0] || '')})));
  ['dr', 'ix', 'mx'].forEach(k => (T[k] || []).forEach(gr => gr[2].forEach(d => { const nm = d[0].split(' · ')[0]; out.push({c: d[2], a: nm, g: nm}); (d[3] || []).forEach(c => out.push({c: c[0], a: nm + ': ' + c[1], g: nm})); })));
  out.forEach(x => x.k = (x.c + ' ' + x.a).replace(/\*\*/g, '').toLowerCase());
  return hqTrIndex.c = out;
}
const HQ_STOP = new Set('with that this from have been their which what most likely appropriate management after before into than then them they there these those when where would could should about other also only such your over under more less each both very none acute chronic first next given patient woman years year week weeks days hours left right normal raised severe'.split(' '));
function hqToks(t){ return (t || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(' ').filter(w => w.length > 3 && !HQ_STOP.has(w)); }
function hqTriggers(it){
  const ui = hqUnitOf(it), ans = it.o[it.a], idx = hqTrIndex();
  const strong = new Set(hqToks(ans)), weak = new Set(hqToks(hqTitle(it) + ' ' + (it.f || '').split('→')[0]));
  const sc = idx.map(x => {
    let s = 0; const ws = new Set(hqToks(x.k));
    strong.forEach(w => { if (ws.has(w)) s += 3; }); weak.forEach(w => { if (ws.has(w)) s += 1; });
    if (x.g && ans.toLowerCase().includes(x.g.toLowerCase())) s += 4;
    if (x.g && it.t !== 'u' && it.t !== 'm' && hqTitle(it).toLowerCase().includes(x.g.toLowerCase())) s += 3;
    if (ui != null && x.u === ui) s += 2.5;
    return [s, x];
  }).filter(p => p[0] >= 3).sort((a, b) => b[0] - a[0]);
  const pick = [], seen = new Set();
  const star = ui != null ? idx.find(x => x.star && x.u === ui) : null;
  if (star) { pick.push(star); seen.add(star.k); }
  for (const [, x] of sc) { if (pick.length >= 4) break; if (!seen.has(x.k)) { pick.push(x); seen.add(x.k); } }
  if (!pick.length) return '';
  return '<div class="hq-trg"><span class="hq-fl">🧲 Triggers</span>' + pick.map(x => '<div class="hq-tl">' + (x.star ? '⭐ ' : '') + fmtRich0(x.c) + ' <span class="tr-arr">→</span> <b class="hq-ta">' + fmtRich0(x.a) + '</b></div>').join('')
    + '<div class="hq-tgo">' + (ui != null && UNITS[ui] ? '<button class="btn ghost sm" data-trjump="' + ui + '">🧲 All triggers for ' + esc(UNITS[ui].name) + '</button>' : '<button class="btn ghost sm" data-trgo="' + esc(hqToks(ans)[0] || ans) + '">🧲 More triggers</button>') + '</div></div>';
}
function hqDraw(m){
  const s = hqSess; m = m || $('#main');
  if (s.done) return hqEnd(m);
  const n = s.ids.length, it = hqItem(s.ids[s.i]), L = 'ABCDE', pick = s.pk[it.id], ans = pick != null, xs = s.x[it.id] || [];
  const done = Object.keys(s.pk).length;
  let h = '<div class="wrap hq-wrap"><div class="ph"><div class="crumbs"><span class="code">🔨 ' + (s.i + 1) + ' / ' + n + '</span><span class="hint">' + done + ' answered' + (s.lbl && (ans || hqLblSafe(s.lbl)) ? ' · ' + esc(s.lbl) : /^🧬/.test(s.lbl || '') ? ' · 🧬 Examiner pattern set' : '') + ' · <span class="hq-saved" title="Every answer and cross-out is saved on this device">💾 saved</span></span><span class="grow"></span><button class="btn ghost sm hq-scanb' + (S.set.hqScan ? ' on' : '') + '" data-hqscan title="Scan mode: question line first, out-of-range numbers lit, normal ones dimmed (S)" aria-pressed="' + (S.set.hqScan ? 'true' : 'false') + '">🦅 Scan</button><button class="btn ghost sm" data-hqfin>🏁 End</button><button class="btn ghost sm" data-hqexit title="Your place is saved">✕ Leave</button></div>';
  h += '<div class="hq-pal" role="navigation" aria-label="Questions">' + s.ids.map((id, j) => { const p = s.pk[id], q = hqItem(id); const c = p == null ? '' : p === q.a ? ' ok' : ' bad'; return '<button class="hq-pn' + c + (j === s.i ? ' on' : '') + '" data-hqgo="' + j + '" aria-label="Question ' + (j + 1) + '">' + (j + 1) + '</button>'; }).join('') + '</div>';
  h += ans ? '<div class="hq-tag"><span>' + esc(hqTitle(it)) + '</span><span class="hq-h">' + HAM(it.h) + '</span><span class="hq-p">' + HQ_PI[it.p] + ' ' + esc(HQ.pat[it.p] || '') + '</span>' + (it.ref ? '<span class="hq-ref">' + esc(it.ref) + '</span>' : '') + hqBadges(it) + '</div></div>'
    : '<div class="hq-tag"><span>' + esc(hqSrcLabel(it)) + '</span><span class="hq-h">' + HAM(it.h) + '</span>' + (it.ref ? '<span class="hq-ref">' + esc(it.ref) + '</span>' : '') + '<span class="hq-p hq-lock" title="The topic and the pattern appear once you answer, so they cannot give the answer away">🔒 Topic after you answer</span></div></div>';
  h += '<div class="panel hq-q' + (S.set.hqScan ? ' scan' : '') + '">' + hqStem(it) + '<div class="hq-os">';
  it.o.forEach((o, i) => {
    let cl = 'hq-o' + (xs.includes(i) ? ' x' : '');
    if (ans) cl += i === it.a ? ' ok' : i === pick ? ' bad' : ' dim';
    h += '<div class="hq-orow"><button class="' + cl + '" data-hqpick="' + i + '"' + (ans ? ' disabled' : '') + '><span class="hq-l">' + L[i] + '</span><span class="hq-ot">' + esc(o) + '</span></button><button class="hq-xb' + (xs.includes(i) ? ' on' : '') + '" data-hqx="' + i + '" title="Cross out (Shift+' + L[i] + ')" aria-label="Cross out option ' + L[i] + '">✕</button></div>';
  });
  h += '</div>';
  if (!ans) h += '<p class="hint hq-hint">Tap ✕ or right-click an option to cross it out (Shift + letter). Answer with <span class="kbd">A</span>–<span class="kbd">E</span>. <span class="kbd">←</span> <span class="kbd">→</span> move between questions.</p>';
  if (ans) {
    const ok = pick === it.a;
    h += '<div class="hq-why ' + (ok ? 'ok' : 'bad') + '"><b>' + (ok ? '✅ Right.' : '❌ ' + L[it.a] + ' is the answer.') + '</b> ' + (it.t === 'o' ? '<span class="hq-off">📋 Examiners\' justification:</span> ' + esc(it.w || 'none given in the paper; the flip and triggers below explain it.') : esc(it.w || '')) + '</div>';
    if (it.f) h += '<div class="hq-flip"><span class="hq-fl">🔄 Flip it</span>' + esc(it.f).replace('→', '<b class="hq-arr">→</b>') + '</div>';
    if (it.t === 'o' && it.iw) h += '<div class="hq-ilo hq-il' + it.il + '"><span class="hq-fl">' + (HQ_IL[it.il] || ['🎯'])[0] + ' ILO check</span>' + esc(it.iw) + (it.ic ? ' <span class="hint">Belongs to: ' + esc(it.ic) + '.</span>' : '') + '</div>';
    h += hqTriggers(it) + hqGroupBox(it);
    const ui = hqUnitOf(it);
    if (ui != null && UNITS[ui]) h += '<div class="toolbar"><button class="btn ghost sm" data-u="' + ui + '" data-mode="read">📖 Notes for ' + esc(UNITS[ui].name) + '</button></div>';
  }
  h += '<div class="toolbar hq-nav"><button class="btn" data-hqnav="-1"' + (s.i ? '' : ' disabled') + '>← Prev</button><span class="grow"></span>' + (s.i + 1 < n ? '<button class="btn' + (ans ? ' primary' : '') + '" data-hqnav="1">Next →</button>' : '<button class="btn primary" data-hqfin>🏁 Finish</button>') + '</div>';
  h += '</div></div>';
  m.innerHTML = h;
  const on = m.querySelector('.hq-pn.on'); if (on && on.scrollIntoView) { const pal = m.querySelector('.hq-pal'); pal.scrollLeft = on.offsetLeft - pal.clientWidth / 2; }
}
function hqPick(i){
  const s = hqSess; if (!s) return; const it = hqItem(s.ids[s.i]);
  if (s.pk[it.id] != null || i >= it.o.length) return;
  s.pk[it.id] = i; const ok = i === it.a;
  hqMark(it.id, ok); if (ok) addXp(it.h * 2);
  hqSave(); hqDraw();
}
function hqStrike(i){
  const s = hqSess; if (!s) return; const it = hqItem(s.ids[s.i]); if (s.pk[it.id] != null) return;
  const xs = s.x[it.id] || (s.x[it.id] = []); const k = xs.indexOf(i); if (k >= 0) xs.splice(k, 1); else xs.push(i);
  hqSave(); hqDraw();
}
function hqGo(j){ const s = hqSess; if (!s) return; s.i = Math.max(0, Math.min(s.ids.length - 1, j)); hqSave(); hqDraw(); window.scrollTo({top: 0}); }
function hqFinish(){ const s = hqSess; if (!s) return; hqDrop(s.rid); s.done = true; hqEnd($('#main')); window.scrollTo({top: 0}); }
function hqEnd(m){
  const s = hqSess, r = s.ids.filter(id => s.pk[id] != null).map(id => [hqItem(id), s.pk[id] === hqItem(id).a]), ok = r.filter(x => x[1]).length;
  const byP = {}; r.forEach(([it, g]) => { const b = byP[it.p] || (byP[it.p] = [0, 0]); b[1]++; if (g) b[0]++; });
  const wrong = r.filter(x => !x[1]).map(x => x[0]), skipped = s.ids.length - r.length;
  let h = '<div class="wrap hq-wrap"><div class="ph"><h1>🔨 ' + ok + ' / ' + r.length + '</h1><p class="hint" style="margin:0">' + (skipped ? skipped + ' left unanswered. ' : '') + 'Where the points went, by pattern. The weakest row is what to drill next.</p></div><div class="panel">';
  Object.entries(byP).sort((a, b) => a[1][0] / a[1][1] - b[1][0] / b[1][1]).forEach(([p, [g, n]]) => h += '<div class="hq-bar"><span class="hq-bl">' + HQ_PI[p] + ' ' + esc(HQ.pat[p] || p) + '</span><span class="hq-bt"><i style="width:' + Math.round(g / n * 100) + '%"></i></span><b>' + g + '/' + n + '</b></div>');
  h += '</div>';
  if (wrong.length) h += '<div class="panel"><h6>🔄 Flips you missed</h6>' + wrong.map(it => '<div class="hq-flip"><span class="hq-fl">' + esc(hqTitle(it)) + '</span>' + esc(it.f || '') + '</div>').join('') + '</div>';
  h += '<div class="toolbar">' + (wrong.length ? '<button class="btn primary" data-hqretry>🔥 Redo the ' + wrong.length + ' missed</button>' : '') + '<button class="btn" data-hqreview>👀 Review this run</button><button class="btn" data-hqexit>Back to the list</button></div></div>';
  m.innerHTML = h;
  s.wrong = wrong;
}
function hqKey(e){
  const s = hqSess; if (!s) return false;
  if (e.key === 'Escape') { hqSess = null; hqCfg.tgt = ''; render(); return true; }
  if (s.done) return false;
  if (e.key === 'ArrowLeft') { e.preventDefault(); hqGo(s.i - 1); return true; }
  if (e.key === 'ArrowRight') { e.preventDefault(); if (s.i + 1 < s.ids.length) hqGo(s.i + 1); return true; }
  if (e.key === 's' || e.key === 'S') { if (e.metaKey || e.ctrlKey || e.altKey) return false; e.preventDefault(); hqScanToggle(); return true; }
  const it = hqItem(s.ids[s.i]), k = e.key.toUpperCase(), li = 'ABCDE'.indexOf(k), idx = li >= 0 && k.length === 1 ? li : /^[1-5]$/.test(e.key) ? +e.key - 1 : -1;
  if (idx >= 0 && idx < it.o.length) { e.preventDefault(); if (e.shiftKey && li >= 0) hqStrike(idx); else hqPick(idx); return true; }
  if (e.key === 'Enter' || k === 'N') { e.preventDefault(); if (s.i + 1 < s.ids.length) hqGo(s.i + 1); else hqFinish(); return true; }
  return false;
}
/* search: hammer stems that mention the term */
function hqSearchHtml(q, has){
  const n = hqAll().filter(it => has((it.s + ' ' + it.o.join(' ')).toLowerCase())).length;
  return n ? '<h6>🔨 Hammer SBAs</h6><button class="sr" data-hqq="' + esc(q) + '"><span class="where">🔨 ' + n + '</span>Practise every question that mentions “' + esc(q) + '”</button>' : '';
}
document.addEventListener('click', e => {
  const t = e.target.closest && e.target.closest('[data-hqset],[data-hqstart],[data-hqpick],[data-hqx],[data-hqnav],[data-hqgo],[data-hqfin],[data-hqexit],[data-hqretry],[data-hqreview],[data-hqresume],[data-hqdrop],[data-hqtgt],[data-hqq],[data-hqscan],[data-hqgrp]'); if (!t) return;
  const d = t.dataset; e.preventDefault(); e.stopImmediatePropagation();
  const sp = document.getElementById('sp'); if (sp) sp.hidden = true;
  const toHub = () => { if (route.view !== 'hammer') { route = {view: 'hammer'}; try { history.replaceState(null, '', '#hammer'); } catch(x) {} renderSide(); } };
  if (d.hqset != null) { const i = d.hqset.indexOf(':'), k = d.hqset.slice(0, i), v = d.hqset.slice(i + 1); hqCfg[k] = k === 'h' ? +v : v; if (k === 'tgt' && !v) hqCfg.tgt = ''; if (k === 'src' && v !== 'o') { hqCfg.pp = ''; hqCfg.ilo = ''; } return viewHammer($('#main')); }
  if (d.hqstart != null) return hqStart(+d.hqstart);
  if (d.hqscan != null) return hqScanToggle();
  if (d.hqgrp != null) { const [gi, j] = d.hqgrp.split(':').map(Number); hqCfg.tgt = 'g:' + gi; hqSess = null; toHub(); hqStart(0); return hqGo(j); }
  if (d.hqpick != null) return hqPick(+d.hqpick);
  if (d.hqx != null) return hqStrike(+d.hqx);
  if (d.hqnav != null) return hqGo(hqSess.i + (+d.hqnav));
  if (d.hqgo != null) return hqGo(+d.hqgo);
  if (d.hqfin != null) return hqFinish();
  if (d.hqresume != null) { toHub(); return hqResume(d.hqresume); }
  if (d.hqdrop != null) { hqDrop(d.hqdrop); return viewHammer($('#main')); }
  if (d.hqexit != null) { hqSess = null; hqCfg.tgt = ''; return route.view === 'hammer' ? render() : go({view: 'hammer'}); }
  if (d.hqretry != null) return hqNewRun(hqSess.wrong, '🔥 Missed');
  if (d.hqreview != null) { hqSess.done = false; hqSess.rev = 1; hqSess.i = 0; session = hqSess; return hqDraw(); }
  if (d.hqtgt != null) { hqCfg.tgt = d.hqtgt; hqSess = null; toHub(); return hqStart(0); }
  if (d.hqq != null) {
    const q = d.hqq.toLowerCase(); const list = hqAll().filter(it => (it.s + ' ' + it.o.join(' ')).toLowerCase().includes(q));
    toHub(); const qi = document.getElementById('q'); if (qi) qi.blur(); return hqNewRun(list, '“' + d.hqq + '”');
  }
}, true);
document.addEventListener('contextmenu', e => { const b = e.target.closest && e.target.closest('[data-hqpick]'); if (!b || !hqSess || b.disabled) return; e.preventDefault(); hqStrike(+b.dataset.hqpick); });
document.addEventListener('change', e => { const t = e.target; if (t.dataset && t.dataset.hqsys != null) { hqCfg.sys = t.value; viewHammer($('#main')); } });
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('hq-bp') && !e.target.classList.contains('hq-obp') && !e.target.classList.contains('hq-iap')) { S.set.hqBp = e.target.open; save(); } }, true);
/* ---------- v2.5: 🏛️ official papers, 🦅 scan mode and 🧬 examiner patterns ---------- */
function hqScanToggle(){ S.set.hqScan = !S.set.hqScan; save(); if (hqSess && !hqSess.done) hqDraw(); }
function hqNum(v){ const m = String(v).replace(/,/g, '').match(/-?\d+(?:\.\d+)?/); return m ? +m[0] : null; }
/* is a value outside its reference range? true high or low, false normal, null unknown. Returns [abnormal, direction] */
function hqAbn(val, rg){
  const v = hqNum(val); rg = String(rg || '').replace(/\s+/g, '');
  if (v == null || !rg) return [null, ''];
  let m = rg.match(/^(-?[\d.]+)[–-]([\d.]+)$/); if (m) return v < +m[1] ? [true, '↓'] : v > +m[2] ? [true, '↑'] : [false, ''];
  m = rg.match(/^[<≤]([\d.]+)$/); if (m) return v >= +m[1] ? [true, '↑'] : [false, ''];
  m = rg.match(/^[>≥]([\d.]+)$/); if (m) return v <= +m[1] ? [true, '↓'] : [false, ''];
  m = rg.match(/^([\d.]+)$/); if (m) return v > +m[1] * 1.2 ? [true, '↑'] : [false, ''];
  return [null, ''];
}
/* the words that flip an answer: blockers in the stem, and the rung words in the question line */
const HQ_FW = /\b(Parkinson['’]s disease|chronic kidney disease(?: stage \d)?|CKD stage \d|eGFR (?:of )?\d+|\d+ weeks['’]? (?:pregnant|gestation)|pregnant|breastfeeding|asthma|COPD|heart failure|ventricular systolic dysfunction|takes warfarin|on warfarin|apixaban|rivaroxaban|metallic \w+ valve|mechanical \w+ valve|allergic to \w+|firefighter|lorry driver|deep vein thrombosis|peptic ulcer|is dying|last days of life|end of life|unable to swallow|methotrexate|immunosuppress\w*|takes lithium|on lithium|clozapine|sickle cell disease|HIV positive|contact lens(?:es)?|after (?:a |an )?(?:long-haul flight|spinal anaesthetic|femoral artery angioplasty)|recently returned from \w+|\d+ (?:minutes|hours|days|weeks) (?:ago|after|previously))\b/gi;
const HQ_QW = /\b(first|initial|immediate|next|definitive|long-term|additional|most sensitive|most specific|confirm|safest|most important|underlying|mechanism|before|in addition)\b/gi;
function hqHi(text, mode){
  text = String(text || ''); const spans = [];
  const add = (re, fn) => { re.lastIndex = 0; let m; while ((m = re.exec(text))) { const c = fn(m); if (c) spans.push([m.index, m.index + m[0].length, c]); if (!m[0].length) re.lastIndex++; } };
  if (mode === 'q') add(HQ_QW, () => 'fw');
  else {
    add(/(\d{2}(?:\.\d)?) ?°C/g, m => 'vx ' + (+m[1] >= 38 || +m[1] < 36 ? 'ab' : 'nm'));
    add(/(\d{2,3}) ?bpm/g, m => 'vx ' + (+m[1] > 100 || +m[1] < 50 ? 'ab' : 'nm'));
    add(/(\d{2,3}) ?\/ ?(\d{2,3}) ?mmHg/g, m => 'vx ' + (+m[1] < 90 || +m[1] >= 180 || +m[2] >= 110 ? 'ab' : 'nm'));
    add(/respiratory rate (?:is |of )?(\d{1,2})(?: breaths per minute)?/gi, m => 'vx ' + (+m[1] > 20 || +m[1] < 10 ? 'ab' : 'nm'));
    add(/oxygen saturation (?:is |of )?(\d{2,3}) ?%/gi, m => 'vx ' + (+m[1] < 94 ? 'ab' : 'nm'));
    add(/(\d+(?:\.\d+)?)([^()\d]{0,24}?)\(\s*([<>≤≥]?\s*\d+(?:\.\d+)?(?:\s*[–-]\s*\d+(?:\.\d+)?)?)\s*\)/g, m => { const r = hqAbn(m[1], m[3])[0]; return r == null ? '' : 'vx ' + (r ? 'ab' : 'nm'); });
    add(HQ_FW, () => 'fw');
  }
  spans.sort((a, b) => a[0] - b[0] || b[1] - a[1]);
  let out = '', at = 0;
  spans.forEach(([s, e, c]) => { if (s < at) return; out += esc(text.slice(at, s)) + '<span class="' + c + '">' + esc(text.slice(s, e)) + '</span>'; at = e; });
  return out + esc(text.slice(at));
}
function hqLab(rows){
  return '<div class="hq-labw"><table class="hq-lab"><caption>Investigations</caption><tbody>' + rows.map(r => {
    const [ab, dir] = hqAbn(r[1], r[2]); const c = ab == null ? (r[2] ? 'nm' : 'tx') : ab ? 'ab' : 'nm';
    return '<tr class="' + c + '"><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + (dir ? ' <span class="dir">' + dir + '</span>' : '') + '</td><td class="rg">' + (r[2] ? '(' + esc(r[2]) + ')' : '') + '</td></tr>';
  }).join('') + '</tbody></table></div>';
}
function hqStem(it){
  let s = it.s || '', ql = it.ql || '';
  if (!ql) { const m = s.match(/^([\s\S]*?)((?:Which|What|How|Where|When|Who|Why|In which|In what|At what|To what|From which|Damage to which|A surge in which)[^?]*\?)\s*$/); if (m && m[1].trim()) { s = m[1].trim(); ql = m[2]; } }
  let h = '<div class="hq-stem">' + (ql ? '<p class="hq-ql hq-qtop"><span class="hq-qi">❓ Read this first</span> ' + hqHi(ql, 'q') + '</p>' : '');
  s.split('\n').filter(x => x.trim()).forEach(p => h += '<p class="hq-s">' + hqHi(p) + '</p>');
  if (it.lab && it.lab.length) h += hqLab(it.lab);
  (it.post || '').split('\n').filter(x => x.trim()).forEach(p => h += '<p class="hq-s">' + hqHi(p) + '</p>');
  (it.img || []).forEach(n => { if (OFF.img[n]) h += '<figure class="hq-fig"><img src="' + OFF.img[n] + '" alt="Image for this question" loading="lazy" data-hqzoom></figure>'; });
  return h + (ql ? '<p class="hq-ql hq-qbot">' + hqHi(ql, 'q') + '</p>' : '') + '</div>';
}
function hqBadges(it){
  return (it.t === 'o' && HQ_IL[it.il] ? '<span class="hq-p hq-il' + it.il + '">' + HQ_IL[it.il].join(' ') + '</span>' : '') + (hqInKind(it.id, 'clone') ? '<span class="hq-p hq-hot">🔥 Double-tested</span>' : '');
}
function hqGLabel(it){
  const a = it.o[it.a]; return (it.t === 'm' ? '🎓 Mock Q' + it.n : it.t === 'o' ? '🏛️ ' + hqPaper(it) + ' Q' + it.n : HAM(it.h) + ' Step ' + it.h) + ' → ' + (a.length > 46 ? a.slice(0, 44) + '…' : a);
}
function hqGroupBox(it){
  const gs = hqGroupsOf(it.id); if (!gs.length) return '';
  return '<div class="hq-gx"><span class="hq-fl">🧬 Examiner pattern</span>' + gs.map(gi => {
    const g = OFF.g[gi], K = HQ_GK[g.k] || ['🧬', g.k];
    return '<div class="hq-gb"><div class="hq-gt"><span class="hq-gk">' + K[0] + ' ' + esc(K[1]) + '</span> <b>' + esc(g.t) + '</b></div><p class="hq-gr">' + esc(g.r) + '</p><div class="hq-gp">'
      + g.ids.map((id, j) => { const x = hqItem(id); if (!x) return ''; return '<button class="chip' + (id === it.id ? ' on' : '') + '" data-hqgrp="' + gi + ':' + j + '"' + (id === it.id ? ' aria-current="true"' : '') + '>' + esc(hqGLabel(x)) + '</button>'; }).join('')
      + '</div><div class="hint">Tap one to run the whole set in order and watch which single detail moves the answer.</div></div>';
  }).join('') + '</div>';
}
/* ----- the official papers, decoded: computed from the papers themselves ----- */
function hqOffBlueprint(){
  const Q = OFF.q; if (!Q.length) return '';
  const words = t => (String(t || '').match(/[A-Za-z0-9'’]+/g) || []).length, med = a => { const b = a.slice().sort((x, y) => x - y); return b.length ? b[b.length >> 1] : 0; };
  const qt = t => { t = t.toLowerCase(); return /most likely (diagnosis|cause|explanation|underlying)|likely to explain|which (virus|organism|artery|nerve|structure|deficiency|pathogen|personality)|what is the (diagnosis|most likely)/.test(t) ? 'dx' : /management|treatment|next step|action|therapy|prescribe|medication|drug|advice|plan|manage|should be|change/.test(t) ? 'mx' : /investigation|imaging|test|radiological|measure|parameter/.test(t) ? 'ix' : 'oth'; };
  const ty = {dx: 0, mx: 0, ix: 0, oth: 0}; Q.forEach(q => ty[qt(q.ql)]++);
  const mty = {dx: 0, mx: 0, ix: 0, oth: 0}; MOCK.q.forEach(m => { const x = (m.s.match(/[^.?]*\?\s*$/) || [m.s])[0]; mty[qt(x)]++; });
  const ow = med(Q.map(q => words(q.s + ' ' + q.post))), mw = med(MOCK.q.map(m => words(m.s.replace(/(Which|What|How)[^?]*\?\s*$/, ''))));
  const lab = Q.filter(q => q.lab && q.lab.length).length, rows = []; Q.forEach(q => (q.lab || []).forEach(r => { const a = hqAbn(r[1], r[2])[0]; if (a != null) rows.push(a); }));
  const normal = rows.filter(a => !a).length, inn = Q.filter(q => q.u >= 0).length, mscaa = MOCK.q.filter(m => /^MSCAA/i.test(m.ref || '')).length;
  const pc = (a, b) => Math.round(a / b * 100) + '%';
  const bar = (lab_, n, max) => '<div class="hq-bar"><span class="hq-bl">' + lab_ + '</span><span class="hq-bt"><i style="width:' + Math.round(n / max * 100) + '%"></i></span><b>' + n + '</b></div>';
  const byK = {}; OFF.g.forEach(g => byK[g.k] = (byK[g.k] || 0) + 1);
  return '<details class="panel hq-bp hq-obp"' + (S.set.hqObp ? ' open' : '') + '><summary>🏛️ The official papers, decoded · ' + Q.length + ' questions from 6 papers</summary><div class="hq-bpg"><div><h6>What the stem asks: official vs your mock</h6>'
    + bar('🔎 Diagnosis', ty.dx, Q.length) + bar('💊 Management', ty.mx, Q.length) + bar('🧪 Investigation', ty.ix, Q.length) + bar('🧠 Mechanism, law, stats', ty.oth, Q.length)
    + '<p class="hint">Your mock: ' + pc(mty.dx, MOCK.q.length) + ' diagnosis, ' + pc(mty.mx, MOCK.q.length) + ' management. The official papers: ' + pc(ty.dx, Q.length) + ' diagnosis, ' + pc(ty.mx, Q.length) + ' management.</p>'
    + '<h6>Papers</h6>' + Object.entries(OFF.pp).map(([k, v]) => bar(esc(v[0]), Q.filter(q => q.pp === k).length, 100)).join('')
    + '</div><div><h6>Why the stems look longer (medians)</h6>' + bar('Story words, official', ow, 80) + bar('Story words, mock', mw, 80) + bar('Has a lab table', lab, Q.length) + bar('Normal lab rows', normal, rows.length)
    + '<h6>🧬 How they repeat</h6>' + Object.entries(HQ_GK).map(([k, v]) => '<button class="chip" data-hqset="tr:' + k + '">' + v[0] + ' ' + esc(v[1]) + ' · ' + (byK[k] || 0) + '</button>').join(' ')
    + '</div></div><ul class="hq-take">'
    + '<li><b>Same bank as your mock.</b> ' + mscaa + ' of your ' + MOCK.q.length + ' mock questions carry MSCAA codes. Three are here almost word for word, and one chest X-ray is reused for two different answers. 🔥 marks them.</li>'
    + '<li><b>The stories are not longer.</b> Median ' + ow + ' words against ' + mw + ' in your mock. The length is the vertical lab table (' + pc(lab, Q.length) + ' of questions) and the full vitals block. ' + pc(normal, rows.length) + ' of lab rows are normal: noise.</li>'
    + '<li><b>🦅 Scan mode (S):</b> the question line moves to the top, out-of-range numbers and vitals light up, normal rows fade, and blocker words (CKD, Parkinson\'s, pregnant, a job, a valve) get the highlighter.</li>'
    + '<li><b>Your mock leans to diagnosis; the national papers lean to management.</b> Expect “what do you do next” as often as “what is it”.</li>'
    + '<li><b>Only ' + pc(Q.filter(q => q.il === 'I').length, Q.length) + ' test one of your ILO conditions directly.</b> ' + pc(Q.filter(q => q.il === 'E').length, Q.length) + ' sit on the edge of an ILO week, and ' + pc(Q.filter(q => q.il === 'O').length, Q.length) + ' are outside your ILOs altogether. The 🎯 ILO audit below goes through every one.</li></ul></details>';
}
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('hq-obp')) { S.set.hqObp = e.target.open; save(); } }, true);
document.addEventListener('click', e => { const im = e.target.closest && e.target.closest('[data-hqzoom]'); if (im) im.classList.toggle('big'); });

/* ----- 🎯 the ILO audit: every official question checked against the 168 ILO conditions ----- */
function hqIloAudit(){
  const Q = OFF.q; if (!Q.length || !Q[0].il) return '';
  const W = {}; (D.weeks || []).forEach(w => W[w.id] = w.name);
  const wk = q => q.u >= 0 && UNITS[q.u] ? W[UNITS[q.u].w] || UNITS[q.u].w : '';
  const n = k => Q.filter(q => q.il === k).length;
  const bar = (lab, v, max) => '<div class="hq-bar"><span class="hq-bl">' + lab + '</span><span class="hq-bt"><i style="width:' + Math.round(v / max * 100) + '%"></i></span><b>' + v + '</b></div>';
  const byW = {}; Q.filter(q => q.il !== 'O').forEach(q => { const w = wk(q); const b = byW[w] || (byW[w] = [0, 0]); b[q.il === 'I' ? 0 : 1]++; });
  const byC = {}; Q.filter(q => q.il === 'O').forEach(q => byC[q.ic] = (byC[q.ic] || 0) + 1);
  const row = q => '<button class="sr hq-arow" data-hqtgt="oq:' + q.id + '"><span class="where">' + HQ_IL[q.il][0] + ' ' + esc(hqPaper(q)) + ' Q' + q.n + '</span><b>' + esc(q.il === 'O' ? q.ic || '' : (UNITS[q.u] || {}).name || '') + '</b> · ' + esc(q.iw) + '</button>';
  const group = (k, keyf, order) => { const g = {}; Q.filter(q => q.il === k).forEach(q => (g[keyf(q)] = g[keyf(q)] || []).push(q)); return Object.keys(g).sort(order).map(x => '<h6>' + esc(x) + ' · ' + g[x].length + '</h6>' + g[x].map(row).join('')).join(''); };
  const wOrder = (D.weeks || []).map(w => w.name), byWeek = (a, b) => wOrder.indexOf(a) - wOrder.indexOf(b);
  return '<details class="panel hq-bp hq-iap"' + (S.set.hqIap ? ' open' : '') + '><summary>🎯 ILO audit · every official question checked against your 168 ILO conditions</summary>'
    + '<p class="hint">Contains answers: open it after you have done the papers, or use it to pick what to drill. Tap any row to practise that question.</p>'
    + '<div class="hq-bpg"><div><h6>Verdict</h6>' + Object.entries(HQ_IL).map(([k, v]) => bar(v[0] + ' ' + v[1], n(k), Q.length)).join('')
    + '<p class="hint">🎯 the condition or decision is one of your ILO conditions. 🟡 it sits in one of your 16 ILO weeks as a differential, complication or principle, but is not itself an ILO condition. 🌍 not in any of your ILO weeks.</p>'
    + '<h6>Outside your ILOs: where they belong</h6>' + Object.entries(byC).sort((a, b) => b[1] - a[1]).map(([c, v]) => bar(esc(c), v, n('O'))).join('')
    + '</div><div><h6>In and on the edge of your ILOs, by week</h6>' + Object.entries(byW).sort((a, b) => byWeek(a[0], b[0])).map(([w, [i, e]]) => '<div class="hq-bar"><span class="hq-bl">' + esc(w) + '</span><span class="hq-bt"><i style="width:' + Math.round((i + e) / 40 * 100) + '%"></i></span><b>' + i + '+' + e + '</b></div>').join('')
    + '<p class="hint">Numbers show 🎯 + 🟡.</p></div></div>'
    + '<div class="hq-alist"><h5>🎯 In my ILOs · ' + n('I') + '</h5>' + group('I', wk, byWeek) + '<h5>🟡 ILO edge · ' + n('E') + '</h5>' + group('E', wk, byWeek) + '<h5>🌍 Outside my ILOs · ' + n('O') + '</h5>' + group('O', q => q.ic || 'Other', (a, b) => a.localeCompare(b)) + '</div></details>';
}
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('hq-iap')) { S.set.hqIap = e.target.open; save(); } }, true);
