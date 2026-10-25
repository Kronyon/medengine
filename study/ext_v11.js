/* ---------- v1.1–1.2: card libraries in one place: 🧬 Why it happens and ⚡ First move vs cure ---------- */
const CARDLIB = {
  why: {list: () => ROOTS, html: (i, lib) => rootHtml(i, lib), icon: '🧬', title: 'Why it happens', unit: 'cards',
    hint: 'Every mechanism in one place: cause → what physically moves → what you see. Tap a card to open it, or read straight through.', ph: 'Search: gout, murmur, shock…'},
  act: {list: () => ACTS, html: (i, lib) => actHtml(i, lib), icon: '⚡', title: 'First move vs cure', unit: 'cards',
    hint: 'Read every stem like a playmaker: <b>last line first</b> → first move or cure? → <b>vitals</b> → 🔴 unstable or 🟢 stable? → then the clue. Each card is the decision in arrows.', ph: 'Search: SVT, DKA, PE, fissure…'}
};
const libState = {why: {sys: '', open: false}, act: {sys: '', open: false}};
const libSysOf = r => { const u = UNITS[(r.u || [])[0]]; return u ? usys(u) : 'other'; };
function libOrder(list){ return list.map((r, i) => ({r, i, s: libSysOf(r), k: Math.min(...((r.u || []).length ? r.u : [999]))})).sort((a, b) => a.k - b.k); }
function viewLib(m, kind){
  const L = CARDLIB[kind], st = libState[kind], list = L.list(), all = libOrder(list), groups = [];
  all.forEach(x => { let g = groups.find(g => g.s === x.s); if (!g) groups.push(g = {s: x.s, xs: []}); g.xs.push(x); });
  const shown = groups.filter(g => !st.sys || g.s === st.sys);
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">' + L.icon + ' ' + L.title + '</span><span class="grow"></span><span class="mono">' + list.length + ' ' + L.unit + '</span></div><h1>' + L.title + '</h1><p class="hint" style="margin:0">' + L.hint + '</p></div>'
    + '<div class="panel why-bar"><div class="toolbar"><input id="whyQ" class="why-q" type="search" placeholder="' + L.ph + '" aria-label="Search the cards"><button class="btn' + (st.open ? ' primary' : '') + '" data-whyall>' + (st.open ? '📕 Close all' : '📖 Read all') + '</button></div>'
    + '<div class="chips why-sys"><button class="chip' + (st.sys ? '' : ' on') + '" data-whysys="">All</button>' + groups.map(g => '<button class="chip' + (st.sys === g.s ? ' on' : '') + '" data-whysys="' + esc(g.s) + '">' + esc(MEV.sysLabel(g.s) || g.s) + ' · ' + g.xs.length + '</button>').join('') + '</div></div>'
    + '<div id="whyList">' + shown.map(g => '<section class="why-g"><h3 class="why-h">' + esc(MEV.sysLabel(g.s) || g.s) + '</h3>' + g.xs.map(x => L.html(x.i, true)).join('') + '</section>').join('') + '<p class="hint" id="whyNone" hidden>No card matches that. Try one word.</p></div></div>';
  if (st.open) $$('#whyList details.pa').forEach(d => { d.open = true; });
  const q = $('#whyQ');
  if (q) q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase(); let n = 0;
    $$('#whyList details.pa').forEach(d => { const hit = !v || (d.dataset.paf || '').includes(v); d.hidden = !hit; if (hit) n++; if (v && hit) d.open = true; });
    $$('#whyList .why-g').forEach(g => { g.hidden = !$$('details.pa:not([hidden])', g).length; });
    const none = $('#whyNone'); if (none) none.hidden = n > 0;
  });
}
function viewWhy(m){ viewLib(m, 'why'); }
function extClick11(t, d){
  const kind = route.view === 'act' ? 'act' : 'why', st = libState[kind];
  if (d.whysys != null) { st.sys = d.whysys; render(); return true; }
  if (d.whyall != null) { st.open = !st.open; $$('#whyList details.pa').forEach(x => { x.open = st.open; }); t.textContent = st.open ? '📕 Close all' : '📖 Read all'; t.classList.toggle('primary', st.open); return true; }
  return false;
}
{ const b8 = extClick8; extClick8 = function(t, d){ return extClick11(t, d) || (typeof extClick12 === 'function' && extClick12(t, d)) || b8(t, d); }; }
