/* ---------- v1.5: 🎞️ Snapshot, the whole condition as a 7-frame picture film, plus related pictures ---------- */
const SNAPS = D.snap || {}, DGU = D.dgu || {};
if (window.DG && DG.snapDef) Object.keys(SNAPS).forEach(k => DG.snapDef('snap' + k, SNAPS[k]));
const snapOn = () => !!(window.DG && DG.has && DG.has('snap0'));
function snapPanelHtml(u){
  if (!window.DG || !DG.has('snap' + u.i)) return '';
  const more = (DGU[u.i] || []).filter(id => DG.has(id));
  return '<details class="panel snap" id="snapCard"' + (S.set.snapClosed ? '' : ' open') + '><summary><b>🎞️ Snapshot</b> <span class="hint">the whole condition in 7 frames · ▶ play, swipe, or test yourself</span></summary>'
    + '<label class="hint snap-t"><input type="checkbox" data-snaptest' + (S.set.dgtest ? ' checked' : '') + '> 🙈 Test me: hide the words, say them, tap the picture to check</label>'
    + '<div id="snapOne">' + DG.html('snap' + u.i) + '</div>'
    + (more.length ? '<div class="snap-more"><span class="hint">More pictures:</span>' + more.map(id => '<button class="chip" data-snapdg="' + id + '">🖼️ ' + esc(DG.title(id).split(':')[0]) + '</button>').join('') + '</div><div id="snapPic"></div>' : '')
    + '</details>';
}
{ const eh = extHeader; extHeader = function(u){ document.body.classList.toggle('dg-testing', !!S.set.dgtest); return snapPanelHtml(u) + eh(u); }; }
function viewSnap(m){
  const q = (S.set.snapq || '').toLowerCase().trim();
  let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🎞️ Snapshots</span><span class="grow"></span><span class="mono">' + UNITS.length + ' conditions</span></div><h1>Snapshots</h1><p class="hint" style="margin:0">Every condition as the same 7-frame film: <b>what goes wrong → who → spot it → prove it → treat → watch for → the hook</b>. Same order every time, so only the content changes. Open one, press ▶, then switch on 🙈 Test me and say each frame before you tap.</p><input class="snap-q" id="snapQ" type="search" placeholder="Filter, e.g. thyroid, stone, eye" value="' + esc(S.set.snapq || '') + '" aria-label="Filter snapshots"></div><div id="snapList">' + snapListHtml(q) + '</div></div>';
  m.innerHTML = h;
}
function snapListHtml(q){
  const seen = new Set();
  let h = '';
  WEEKS.forEach(w => {
    const us = unitsOf(w.id).filter(u => SNAPS[u.i] && !seen.has(SNAPS[u.i].n) && (!q || (u.name + ' ' + SNAPS[u.i].n + ' ' + SNAPS[u.i].m).toLowerCase().includes(q)));
    us.forEach(u => seen.add(SNAPS[u.i].n));
    if (us.length) h += '<h4>' + esc(w.name) + ' · ' + us.length + '</h4><div class="snap-grid">' + us.map(u => '<button class="snap-tile" data-u="' + u.i + '"><b>🎞️ ' + esc(SNAPS[u.i].n) + '</b><span>' + esc(SNAPS[u.i].m.split(/\s*→\s*/)[0]) + '</span></button>').join('') + '</div>';
  });
  return h || '<p class="hint">Nothing matches.</p>';
}
document.addEventListener('click', e => {
  const b = e.target.closest && e.target.closest('[data-snapdg]'); if (!b) return;
  const box = document.getElementById('snapPic'); if (!box) return;
  const on = b.classList.contains('on');
  document.querySelectorAll('[data-snapdg]').forEach(x => x.classList.remove('on'));
  if (window.DG) DG.stopAll();
  box.innerHTML = on ? '' : DG.html(b.dataset.snapdg); if (!on) b.classList.add('on');
});
document.addEventListener('change', e => { if (e.target.dataset && e.target.dataset.snaptest != null) { S.set.dgtest = e.target.checked; save(); document.body.classList.toggle('dg-testing', !!S.set.dgtest); } });
document.addEventListener('toggle', e => { if (e.target.id === 'snapCard') { S.set.snapClosed = !e.target.open; save(); if (!e.target.open && window.DG) DG.stopAll(); } }, true);
document.addEventListener('input', e => { if (e.target.id === 'snapQ') { S.set.snapq = e.target.value; clearTimeout(viewSnap.t); viewSnap.t = setTimeout(() => { save(); const l = document.getElementById('snapList'); if (l) l.innerHTML = snapListHtml(e.target.value.toLowerCase().trim()); }, 180); } });
