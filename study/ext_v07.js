/* ---------- v0.7: dual-code clinchers, Jargon Decoder, 3-way triangulation sniper ---------- */
const JG = D.jg || [];
JG.forEach((j, i) => { j.i = i; });
const jgOfUnit = ui => JG.filter(j => j.u.includes(ui));
const DC_EQ = '🟰', DC_DX = '→ 🎯';
/* 🎬 film 🟰 🏷️ Label [hook] → 🎯 diagnosis: rendered as a high-contrast split, hooks as chips (no brackets to skip) */
function dualHtml(t){
  if (typeof t !== 'string' || t.indexOf(DC_EQ) < 0) return null;
  const i = t.indexOf(DC_EQ);
  const film = t.slice(0, i).replace(/^\s*🎬\s*/u, '').trim();
  let rest = t.slice(i + DC_EQ.length).trim().replace(/^🏷️?\s*/u, ''), dx = '';
  const j = rest.indexOf(DC_DX);
  if (j >= 0) { dx = rest.slice(j + DC_DX.length).trim(); rest = rest.slice(0, j).trim(); }
  const hooks = [];
  const lab = rest.replace(/\s*\[([^\]]+)\]/g, (m, x) => { hooks.push(x); return ''; }).trim();
  return '<span class="dc"><span class="dc-f"><span class="dc-i" aria-hidden="true">🎬</span>' + fmtRich0(film) + '</span>'
    + '<span class="dc-eq" aria-label="equals">🟰</span>'
    + '<span class="dc-l"><span class="dc-i" aria-hidden="true">🏷️</span><span class="dc-lt">' + fmtRich0(lab) + '</span>' + hooks.map(x => '<span class="dc-h">🔗 ' + fmtRich0(x) + '</span>').join('') + '</span>'
    + (dx ? '<span class="dc-d"><span class="dc-i" aria-hidden="true">→ 🎯</span>' + fmtRich0(dx) + '</span>' : '') + '</span>';
}
/* the classic sniper hides the 🎯 answer half of a dual-code clincher until you have named it */
const dxStrip = t => { const s = String(t || ''), k = s.indexOf(DC_DX); return s.indexOf(DC_EQ) >= 0 && k > 0 ? s.slice(0, k).trim() : s; };

/* ----- 🔺 Jargon Decoder ----- */
function jgUnitBtns(j){ return j.u.map(ui => UNITS[ui] ? '<button class="chip" data-u="' + ui + '" data-mode="read">📖 ' + esc(UNITS[ui].name) + '</button>' : '').join(''); }
function jgCardHtml(j){
  const u0 = UNITS[j.u[0]];
  return '<article class="jg" id="JG-' + j.i + '"><h3>🏷️ ' + esc(j.t) + '</h3>'
    + '<div class="jgr jg-f"><span class="jgk">🎬 What you see</span><span>' + fmtRich0(j.f) + '</span></div>'
    + '<div class="jgr jg-h"><span class="jgk">🔗 Memory hook</span><span>' + fmtRich0(j.h) + '</span></div>'
    + '<div class="jgr jg-x"><span class="jgk">⚡ Exam trap</span><span>' + fmtRich0(j.x) + '</span></div>'
    + '<div class="jgr jg-m"><span class="jgk">🔨 What to do</span><span>' + fmtRich0(j.m) + '</span></div>'
    + (j.ecg && MEV.ECG[j.ecg] ? '<figure class="jg-ecg">' + MEV.ECG[j.ecg]() + '<figcaption>Drawn schematic, not a real trace</figcaption></figure>' : '')
    + '<div class="toolbar jg-tools">' + (j.sd ? '<button class="btn" data-mev-sd="' + j.sd + '">🥊 Visual showdown</button>' : '') + '<button class="btn" data-mev-atlas="' + esc(j.t.split(' vs ')[0]) + '" data-mev-sys="' + esc(u0 ? usys(u0) : '') + '">👁️ Atlas</button><button class="btn" data-jgtri="' + j.i + '">🔺 Drill it</button></div>'
    + '<div class="chips jg-units">' + jgUnitBtns(j) + '</div></article>';
}
function jgChipsHtml(u){
  const js = jgOfUnit(u.i); if (!js.length) return '';
  return '<div class="jgchips"><span class="hint">🔺 Decoder</span>' + js.map(j => '<button class="chip" data-jgopen="' + j.i + '">' + esc(j.t) + '</button>').join('') + '</div>';
}
function openJg(i){
  const j = JG[i]; if (!j) return;
  let ov = $('#jgView');
  if (!ov) { ov = document.createElement('div'); ov.className = 'overlay'; ov.id = 'jgView'; document.body.appendChild(ov); ov.addEventListener('click', e => { if (e.target === ov) ov.hidden = true; }); }
  ov.innerHTML = '<div class="modal jgmodal" role="dialog" aria-label="Jargon Decoder"><div class="toolbar"><b class="grow">🔺 Jargon Decoder</b><button class="iconbtn" data-jgclose aria-label="Close">✕</button></div>' + jgCardHtml(j) + '</div>';
  ov.hidden = false;
}
document.addEventListener('keydown', e => { const ov = $('#jgView'); if (e.key === 'Escape' && ov && !ov.hidden) { ov.hidden = true; e.stopPropagation(); } }, true);
let jgQ = '', jgSys = '';
const jgNorm = s => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’']/g, "'");
function jgFilter(){
  const q = jgNorm(jgQ.trim());
  return JG.filter(j => (!jgSys || j.u.some(ui => UNITS[ui] && usys(UNITS[ui]) === jgSys)) && (!q || jgNorm(j.t + ' ' + j.al.join(' ') + ' ' + j.u.map(ui => UNITS[ui] ? UNITS[ui].name : '').join(' ')).includes(q)));
}
function jgDrawList(){
  const box = $('#jgList'); if (!box) return;
  const L = jgFilter(), n = $('#jgN'); if (n) n.textContent = L.length + ' of ' + JG.length;
  box.innerHTML = L.length ? L.map(jgCardHtml).join('') : '<div class="panel empty">Nothing matches. Names that already paint a picture (apple core, bamboo spine) are left out on purpose.</div>';
}
function viewJargon(m){
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🔺 Decoder</span><span class="grow"></span><span class="mono" id="jgN"></span></div><h1>Jargon Decoder</h1><p class="hint" style="margin:0">' + JG.length + ' exam names that don\'t describe what they are (Rinne, Kussmaul, Δ wave…). Each card: 🎬 what you see, 🔗 a hook that ties the word to the picture, ⚡ the trap and 🔨 what to do.</p></div>'
    + '<div class="panel"><div class="toolbar"><input class="shotnote" id="jgQ" type="search" placeholder="Find a term: Kussmaul, Rinne, Δ, Charcot…" aria-label="Find a term" value="' + esc(jgQ) + '"><select class="jsel" data-jgsys aria-label="Filter by system" style="width:auto"><option value="">All systems</option>' + MEV.sysOptions(jgSys) + '</select><button class="btn primary" data-jgmode="tri">🔺 Drill it</button></div></div><div id="jgList" class="jgs"></div></div>';
  jgDrawList();
}
document.addEventListener('input', e => { if (e.target && e.target.id === 'jgQ') { jgQ = e.target.value; jgDrawList(); } });
document.addEventListener('change', e => { const t = e.target; if (t && t.dataset && t.dataset.jgsys != null) { jgSys = t.value; jgDrawList(); } });

/* ----- 🔺 3-way triangulation sniper ----- */
const JGM = {
  m1: {b: '① 🎬→🏷️', n: 'Picture → name', ask: '🏷️ Name it (the exam word) and the diagnosis, then reveal.'},
  m2: {b: '② 🏷️→🎬', n: 'Name → picture', ask: '🎬 What does it look like? Picture it, then reveal.'},
  m3: {b: '③ 🔨 Treat', n: 'What do you do?', ask: '🔨 First-line move, or the thing you must never do?'},
  tri: {b: '🔺 All three', n: 'All three on one term', ask: ''}
};
let jgRecent = [], jgOnly = null;
const jgSt = () => { const st = snpState(); st.jg = Object.assign({n: 0, got: 0}, st.jg || {}); st.jm = st.jm || {}; return st; };
function jgPool(){
  const st = jgSt();
  let P = JG.filter(j => j.u.some(ui => UNITS[ui] && (!snpCfg.sys || usys(UNITS[ui]) === snpCfg.sys) && (!snpCfg.wk || UNITS[ui].w === snpCfg.wk)));
  if (snpCfg.miss) P = P.filter(j => st.jm[j.i]);
  return P;
}
function jgStart(j){
  const md = snpCfg.mode;
  return {jg: true, j, steps: md === 'tri' ? ['m1', 'm2', 'm3'] : [md], cur: 0, rev: false, res: []};
}
function jgNext(){
  const s = session; if (!s || s.kind !== 'sniper') return;
  const P = jgPool(), st = jgSt();
  if (jgOnly != null) { const o = JG[jgOnly]; jgOnly = null; if (o) { s.k++; s.t = jgStart(o); return drawSnp(); } }
  if (!P.length) { const b = $('#snp'); if (b) b.innerHTML = '<div class="panel empty">' + (snpCfg.miss ? 'No missed terms queued: every one has been re-triangulated. 🔺' : 'No decoder terms for this filter.') + '</div>'; return; }
  const misses = P.filter(j => st.jm[j.i]);
  let pool = misses.length && Math.random() < 0.3 ? misses : P;
  const fresh = pool.filter(j => !jgRecent.includes(j.i)); if (fresh.length) pool = fresh;
  const j = pool[Math.floor(Math.random() * pool.length)];
  jgRecent = [j.i].concat(jgRecent).slice(0, Math.min(12, Math.floor(P.length / 2)));
  s.k++; s.t = jgStart(j); drawSnp();
}
function jgDx(j){ return j.u.map(ui => UNITS[ui] ? esc(UNITS[ui].name) : '').filter(Boolean).join(' · '); }
function drawJg(){
  const s = session, box = $('#snp'), T = s.t, j = T.j, done = T.cur >= T.steps.length;
  let h = '<div class="qcard snp jgq"><div class="qmeta"><span class="code">🔺 Target ' + s.k + '</span>' + (T.steps.length > 1 ? '<span class="code">' + Math.min(T.cur + 1, 3) + ' / 3</span>' : '') + '<span class="grow"></span><span class="mono">🔥 ' + s.streak + ' · ' + s.hits + '/' + s.shots + (s.earned ? ' · ฿' + s.earned : '') + '</span></div>';
  T.steps.forEach((md, i) => {
    if (i > T.cur) return;
    const open = T.rev, M = JGM[md];
    // finished steps collapse to their result, so the next direction can't be copied from the screen
    if (i < T.cur) { h += '<div class="jgstep past"><div class="snp-lab">' + M.b + ' · ' + esc(M.n) + (T.res[i] ? ' ✅' : ' ❌') + '</div></div>'; return; }
    h += '<div class="jgstep"><div class="snp-lab">' + M.b + ' · ' + esc(M.n) + '</div>';
    if (md === 'm1') h += '<div class="stem snp-clue jg-film">🎬 ' + fmtRich0(j.f) + '</div>';
    else if (md === 'm2') h += '<div class="jg-label">🏷️ ' + esc(j.t) + '</div>';
    else h += '<div class="stem snp-clue jg-film">🎬 ' + fmtRich0(j.f) + '</div><div class="jg-label sm">🏷️ ' + esc(j.t) + '</div>';
    if (!open) h += '<p class="hint" style="margin:0">' + M.ask + '</p><div class="toolbar"><button class="btn primary" data-jgrev>Reveal <span class="kbd">Space</span></button></div>';
    else {
      if (md === 'm1') h += '<div class="jg-ans"><div class="jg-label">🏷️ ' + esc(j.t) + '</div><div class="jgr jg-h"><span class="jgk">🔗 Memory hook</span><span>' + fmtRich0(j.h) + '</span></div><div class="jgr"><span class="jgk">🎯 Diagnosis</span><span>' + jgDx(j) + '</span></div></div>';
      else if (md === 'm2') h += '<div class="jg-ans"><div class="jgr jg-f"><span class="jgk">🎬 What you see</span><span>' + fmtRich0(j.f) + '</span></div><div class="jgr jg-h"><span class="jgk">🔗 Memory hook</span><span>' + fmtRich0(j.h) + '</span></div>' + (j.ecg && MEV.ECG[j.ecg] ? '<figure class="jg-ecg">' + MEV.ECG[j.ecg]() + '</figure>' : '') + '</div>';
      else h += '<div class="jg-ans"><div class="jgr jg-m"><span class="jgk">🔨 What to do</span><span>' + fmtRich0(j.m) + '</span></div><div class="jgr jg-x"><span class="jgk">⚡ Exam trap</span><span>' + fmtRich0(j.x) + '</span></div></div>';
      if (i === T.cur) h += '<div class="toolbar"><button class="btn primary" data-jggot="1">✅ Got it <span class="kbd">1</span></button><button class="btn" data-jggot="0">❌ Missed it <span class="kbd">2</span></button></div>';
    }
    h += '</div>';
  });
  if (done) {
    h += '<div class="snp-end"><b>' + T.res.map(r => r ? '✅' : '❌').join(' ') + ' · ' + esc(j.t) + '</b><div class="toolbar"><button class="btn primary" data-snpnext>Next target → <span class="kbd">Enter</span></button><button class="btn" data-jgopen="' + j.i + '">🔺 Decoder card</button>' + (j.u[0] != null && UNITS[j.u[0]] ? '<button class="btn ghost" data-u="' + j.u[0] + '" data-mode="read">📖 Open ' + esc(UNITS[j.u[0]].name) + '</button>' : '') + '</div></div>';
  }
  box.innerHTML = h + '</div>';
}
function jgReveal(){ const s = session; if (!s || !s.t || !s.t.jg || s.t.cur >= s.t.steps.length || s.t.rev) return; s.t.rev = true; drawSnp(); }
function jgGrade(ok){
  const s = session; if (!s || !s.t || !s.t.jg) return;
  const T = s.t; if (!T.rev || T.cur >= T.steps.length) return;
  const st = jgSt();
  T.res[T.cur] = ok; st.jg.n++; s.shots++;
  if (ok) { st.jg.got++; s.hits++; s.streak++; st.best = Math.max(st.best || 0, s.streak); s.earned += 5; addXp(5); if (st.jm[T.j.i]) { st.jm[T.j.i]--; if (st.jm[T.j.i] <= 0) delete st.jm[T.j.i]; } }
  else { s.streak = 0; st.jm[T.j.i] = (st.jm[T.j.i] || 0) + 1; }
  T.cur++; T.rev = false; save(); drawSnp();
}
function jgKey(e){
  const T = session.t, k = e.key.toLowerCase();
  if (T.cur >= T.steps.length) { if (k === 'enter' || k === 'arrowright') { e.preventDefault(); snpNext(); return true; } return k === 's' || k === 'm'; }
  if (!T.rev && (k === ' ' || k === 'enter')) { e.preventDefault(); jgReveal(); return true; }
  if (T.rev && (k === '1' || k === '2')) { e.preventDefault(); jgGrade(k === '1'); return true; }
  return k === 's' || k === 'm';
}
function snpModeHtml(){
  const md = snpCfg.mode;
  return '<div class="seg snp-modes" role="group" aria-label="Retrieval direction"><button class="' + (md === 'clue' ? 'on' : '') + '" data-snpmode="clue">🎯 Blind clincher</button>' + ['m1', 'm2', 'm3', 'tri'].map(k => '<button class="' + (md === k ? 'on' : '') + '" data-snpmode="' + k + '" title="' + esc(JGM[k].n) + '">' + JGM[k].b + '</button>').join('') + '</div>';
}
function extClick7(t, d){
  if (d.jgopen != null) { openJg(+d.jgopen); return true; }
  if (d.jgclose != null) { $('#jgView').hidden = true; return true; }
  if (t.closest('#jgView') && (d.u != null || d.jgtri != null)) $('#jgView').hidden = true;
  if (d.jgtri != null) { snpCfg.mode = 'tri'; S.set.snpm = 'tri'; jgOnly = +d.jgtri; save(); go({view: 'sniper'}); return true; }
  if (d.jgmode) { snpCfg.mode = d.jgmode; S.set.snpm = d.jgmode; save(); go({view: 'sniper'}); return true; }
  if (d.snpmode) { snpCfg.mode = d.snpmode; S.set.snpm = d.snpmode; save(); render(); return true; }
  if (d.jgrev != null) { jgReveal(); return true; }
  if (d.jggot != null) { jgGrade(d.jggot === '1'); return true; }
  return false;
}
/* read-only hook for the automated tests (no effect on the app) */
try { Object.defineProperty(window, '__me7', {value: Object.freeze({get session(){ return session; }, get S(){ return S; }, dxStrip, snpNext: () => snpNext()})}); } catch (e) {}
