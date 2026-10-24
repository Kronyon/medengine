/* ---------- v1.1: 🧬 Why it happens, every mechanism card in one place ---------- */
let whySys = '', whyOpen = false;
const whySysOf = r => { const u = UNITS[(r.u || [])[0]]; return u ? usys(u) : 'other'; };
function whyOrder(){ return ROOTS.map((r, i) => ({r, i, s: whySysOf(r), k: Math.min(...((r.u || []).length ? r.u : [999]))})).sort((a, b) => a.k - b.k); }
function viewWhy(m){
  const all = whyOrder(), groups = [];
  all.forEach(x => { let g = groups.find(g => g.s === x.s); if (!g) groups.push(g = {s: x.s, xs: []}); g.xs.push(x); });
  const shown = groups.filter(g => !whySys || g.s === whySys);
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🧬 Why it happens</span><span class="grow"></span><span class="mono">' + ROOTS.length + ' cards</span></div><h1>Why it happens</h1><p class="hint" style="margin:0">Every mechanism in one place: cause → what physically moves → what you see. Tap a card to open it, or read straight through.</p></div>'
    + '<div class="panel why-bar"><div class="toolbar"><input id="whyQ" class="why-q" type="search" placeholder="Search: gout, murmur, shock…" aria-label="Search the cards"><button class="btn' + (whyOpen ? ' primary' : '') + '" data-whyall>' + (whyOpen ? '📕 Close all' : '📖 Read all') + '</button></div>'
    + '<div class="chips why-sys"><button class="chip' + (whySys ? '' : ' on') + '" data-whysys="">All</button>' + groups.map(g => '<button class="chip' + (whySys === g.s ? ' on' : '') + '" data-whysys="' + esc(g.s) + '">' + esc(MEV.sysLabel(g.s) || g.s) + ' · ' + g.xs.length + '</button>').join('') + '</div></div>'
    + '<div id="whyList">' + shown.map(g => '<section class="why-g"><h3 class="why-h">' + esc(MEV.sysLabel(g.s) || g.s) + '</h3>' + g.xs.map(x => rootHtml(x.i, true)).join('') + '</section>').join('') + '<p class="hint" id="whyNone" hidden>No card matches that. Try one word.</p></div></div>';
  if (whyOpen) $$('#whyList details.pa').forEach(d => { d.open = true; });
  const q = $('#whyQ');
  if (q) q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase(); let n = 0;
    $$('#whyList details.pa').forEach(d => { const hit = !v || (d.dataset.paf || '').includes(v); d.hidden = !hit; if (hit) n++; if (v && hit) d.open = true; });
    $$('#whyList .why-g').forEach(g => { g.hidden = !$$('details.pa:not([hidden])', g).length; });
    const none = $('#whyNone'); if (none) none.hidden = n > 0;
  });
}
function extClick11(t, d){
  if (d.whysys != null) { whySys = d.whysys; render(); return true; }
  if (d.whyall != null) { whyOpen = !whyOpen; $$('#whyList details.pa').forEach(x => { x.open = whyOpen; }); t.textContent = whyOpen ? '📕 Close all' : '📖 Read all'; t.classList.toggle('primary', whyOpen); return true; }
  return false;
}
{ const b8 = extClick8; extClick8 = function(t, d){ return extClick11(t, d) || b8(t, d); }; }
