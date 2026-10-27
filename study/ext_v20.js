/* ---------- v2.0: 🗺️ Posters. Every condition is one picture drawn with the same code (PLACE + LOCK), with its
   film and pictures one tap away; 14 master posters; and 🖼️ My infographics: your own pictures, with boxes you draw
   over the details and tap to reveal, kept only in this browser on this device. ---------- */
const MASTER = D.master || [], MBY = {}; MASTER.forEach(x => MBY[x.id] = x);
const MOFU = {}; MASTER.forEach(x => (x.u || []).forEach(u => (MOFU[u] = MOFU[u] || []).push(x.id)));
const QUIZ = new Set(['fill', 'mcq', 'recall']);
let poTabCur = {u: -1, tab: 'poster'}; /* the tab sticks while you stay on a condition; a new condition opens on its poster */
const poTab = ui => poTabCur.u === ui ? poTabCur.tab : 'poster';
function poMasterChips(ui){
  const L = [...new Set(MOFU[ui] || [])].filter(id => MBY[id]);
  return L.length ? '<div class="po-mp"><span>🧭 Master posters</span>' + L.map(id => '<button type="button" class="chip" data-mp="' + id + '">' + esc(MBY[id].ic || '🧭') + ' ' + esc(MBY[id].t) + '</button>').join('') + '</div>' : '';
}
function poClosedKey(){ return route.view === 'unit' && QUIZ.has(route.mode) ? 'poClosedQ' : 'poClosedR'; }
function posterPanelHtml(u){
  const s = SNAPS[u.i];
  if (!s || !window.PO) return snapPanelHtml(u);
  const tab = poTab(u.i), quiz = route.view === 'unit' && QUIZ.has(route.mode);
  return '<details class="panel popanel" id="poCard"' + (S.set[poClosedKey()] ? '' : ' open') + '><summary><b>🗺️ Poster</b> <span class="hint">' + (quiz ? 'locked while you quiz: tap a pill to peek' : 'the whole condition as one picture · 🔒 Lock or L to test yourself') + '</span></summary>'
    + '<div class="seg potabs" role="tablist">' + [['poster', '🗺️ Poster'], ['film', '🎞️ Film'], ['pics', '🖼️ Pictures']].map(([k, l]) => '<button type="button" data-potab="' + k + '" class="' + (tab === k ? 'on' : '') + '" role="tab" aria-selected="' + (tab === k) + '">' + l + '</button>').join('') + '</div>'
    + '<div id="poBody">' + poBodyHtml(u, tab) + '</div></details>';
}
function poBodyHtml(u, tab){
  if (tab === 'film') return '<label class="hint snap-t"><input type="checkbox" data-snaptest' + (S.set.dgtest ? ' checked' : '') + '> 🔒 Lock: hide the words, say them, tap the picture to check</label><div id="snapOne">' + (DG.has('snap' + u.i) ? DG.html('snap' + u.i) : '') + '</div>';
  if (tab === 'pics') {
    const more = (DGU[u.i] || []).filter(id => DG.has(id));
    return (more.length ? '<div class="snap-more"><span class="hint">OSCE pictures:</span>' + more.map(id => '<button class="chip" data-snapdg="' + id + '">🖼️ ' + esc(DG.title(id).split(':')[0]) + '</button>').join('') + '</div><div id="snapPic"></div>' : '') + igBoxHtml(u.i);
  }
  const quiz = route.view === 'unit' && QUIZ.has(route.mode);
  return PO.cond(SNAPS[u.i], {id: 'u' + u.i, lock: PO.lockOn || quiz, foot: poMasterChips(u.i)});
}
function poRedraw(){
  const b = document.getElementById('poBody'); if (!b || route.view !== 'unit') return;
  const tab = poTab(route.u);
  if (window.DG) DG.stopAll(); if (window.PO) PO.stopWalk();
  b.innerHTML = poBodyHtml(UNITS[route.u], tab);
  document.querySelectorAll('[data-potab]').forEach(x => { x.classList.toggle('on', x.dataset.potab === tab); x.setAttribute('aria-selected', x.dataset.potab === tab); });
  if (tab === 'pics') igRefreshBox(route.u);
}
document.addEventListener('toggle', e => { if (e.target.id === 'poCard') { S.set[poClosedKey()] = !e.target.open; save(); if (!e.target.open) { if (window.DG) DG.stopAll(); if (window.PO) PO.stopWalk(); } } }, true);

/* the "why" behind the code, in one panel */
function whyPostersHtml(open){
  return '<details class="panel why-po"' + (open ? ' open' : '') + '><summary><b>💡 Why posters work for you</b></summary><p class="hint" style="margin:6px 0 0">You take in a page as one picture and remember where things sat, so every poster follows one code. Only the content changes.</p><div class="place">'
    + [['P', 'Picture with the words on it', 'the words sit inside the picture, never in a separate list'], ['L', 'Location never changes', 'cause top-left, who top-right, tests on the right, treatment bottom-right, danger bottom-left, the lookalike on the left, signs in the middle'], ['A', 'Arrows carry the movement', 'every mechanism is a chain you can play like a film'], ['C', 'Contrast on one axis', 'each condition sits beside the one it gets confused with, compared on a single question'], ['E', 'Exaggerate one thing', 'one hook per poster, not ten'], ['🔒', 'Then LOCK it', 'a glance feels like knowing, so Lock hides the drugs, numbers and signs: say them, then tap. Pulling them back out is what makes them stick']].map(r => '<div><b>' + r[0] + '</b><span><b>' + esc(r[1]) + ':</b> ' + esc(r[2]) + '</span></div>').join('') + '</div></details>';
}

/* ---------- the Posters hub and the master posters ---------- */
function posterWallHtml(q){
  const seen = new Set(); let h = '';
  WEEKS.forEach(w => {
    const us = unitsOf(w.id).filter(u => SNAPS[u.i] && !seen.has(SNAPS[u.i].n) && (!q || (u.name + ' ' + SNAPS[u.i].n + ' ' + SNAPS[u.i].m + ' ' + ((SNAPS[u.i].v || [])[0] || '')).toLowerCase().includes(q)));
    us.forEach(u => seen.add(SNAPS[u.i].n));
    if (us.length) h += '<h4>' + esc(w.name) + ' · ' + us.length + '</h4><div class="snap-grid">' + us.map(u => { const s = SNAPS[u.i]; return '<button class="snap-tile" data-u="' + u.i + '" data-mode="read"><b>🗺️ ' + esc(s.n) + '</b><span>' + esc(s.m.split(/\s*→\s*/)[0]) + '</span>' + (s.v ? '<span class="po-vsline">⚖️ vs ' + esc(s.v[0]) + '</span>' : '') + '</button>'; }).join('') + '</div>';
  });
  return h || '<p class="hint">Nothing matches.</p>';
}
function viewPosters(m){
  const q = (S.set.snapq || '').toLowerCase().trim(), nCond = new Set(Object.values(SNAPS).map(s => s.n)).size;
  let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🗺️ Posters</span><span class="grow"></span><span class="mono">' + nCond + ' conditions · ' + MASTER.length + ' master posters</span></div><h1>Posters</h1><p class="hint" style="margin:0">Every condition drawn with the same code, so only the content changes. Press 🔒 <b>Lock</b> or <span class="kbd">L</span> to hide the details, say them, then tap each pill or press <span class="kbd">N</span>. ▶ <b>Walk it</b> lights the zones in reading order.</p></div>';
  h += whyPostersHtml(false);
  h += '<h4>🧭 Master posters · one picture for a whole topic</h4><div class="mp-grid">' + MASTER.map(x => '<button class="snap-tile mp-tile" data-mp="' + x.id + '"><b>' + esc(x.ic) + ' ' + esc(x.t) + '</b><span>' + esc(x.sub || '') + '</span>' + ((x.fix || []).length ? '<span class="po-vsline">🔎 your AI version, ' + x.fix.length + ' fixes</span>' : '') + '</button>').join('') + '</div>';
  h += '<details class="panel igpanel" id="igHub"' + (S.set.igHubOpen ? ' open' : '') + '><summary><b>🖼️ My infographics</b> <span class="hint" id="igHubN"></span></summary><div id="igHubBody"><p class="hint">Loading…</p></div></details>';
  h += '<h4>🗺️ Condition posters</h4><input class="snap-q" id="snapQ" type="search" placeholder="Filter: e.g. thyroid, stone, eye" value="' + esc(S.set.snapq || '') + '" aria-label="Filter condition posters"><div id="snapList">' + posterWallHtml(q) + '</div></div>';
  m.innerHTML = h;
  igRefreshHub();
}
function viewMaster(m){
  const x = MBY[route.id]; if (!x || !window.PO) return viewPosters(m);
  const i = MASTER.indexOf(x), pv = MASTER[(i - 1 + MASTER.length) % MASTER.length], nx = MASTER[(i + 1) % MASTER.length], seen = new Set();
  const us = (x.u || []).filter(u => UNITS[u] && !seen.has(UNITS[u].name) && seen.add(UNITS[u].name));
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><button class="btn ghost" data-go="posters">← All posters</button><span class="grow"></span><button class="btn ghost" data-mp="' + pv.id + '" title="Previous master poster">← ' + esc(pv.t) + '</button><button class="btn ghost" data-mp="' + nx.id + '" title="Next master poster">' + esc(nx.t) + ' →</button></div></div>'
    + PO.split(x, {lock: PO.lockOn}) + (us.length ? '<div class="panel"><b>Conditions on this poster</b><div class="snap-more" style="margin-top:6px">' + us.map(u => '<button class="chip" data-u="' + u + '" data-mode="read">🗺️ ' + esc(UNITS[u].name) + '</button>').join('') + '</div></div>' : '') + '</div>';
}
document.addEventListener('click', e => {
  const b = e.target.closest && e.target.closest('[data-mp],[data-potab],[data-sr="mp"]'); if (!b) return;
  if (b.dataset.potab) { poTabCur = {u: route.u, tab: b.dataset.potab}; poRedraw(); e.stopImmediatePropagation(); return; }
  const id = b.dataset.mp || b.dataset.mpid;
  if (id && MBY[id]) { e.stopImmediatePropagation(); const sp = document.getElementById('sp'); if (sp) sp.hidden = true; go({view: 'mp', id}); }
});

/* ---------- 🖼️ My infographics ---------- */
const IG_LS = 'medengine-ig-v1';
let igCache = null, igCur = null, igMode = 'study';
function igLs(){ try { return JSON.parse(localStorage.getItem(IG_LS) || '[]'); } catch (e) { return []; } }
async function igAll(){
  if (igCache) return igCache;
  const db = await shotIdb();
  if (db) { try { igCache = await new Promise((res, rej) => { const r = db.transaction('shots').objectStore('shots').getAll(); r.onsuccess = () => res((r.result || []).filter(x => x.ig)); r.onerror = () => rej(r.error); }); return igCache; } catch (e) {} }
  igCache = igLs(); return igCache;
}
async function igPut(x){
  const db = await shotIdb(); let ok = false;
  if (db) { try { await new Promise((res, rej) => { const tx = db.transaction('shots', 'readwrite'); tx.objectStore('shots').put(x); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); ok = true; } catch (e) {} }
  if (!ok) { try { const a = igLs().filter(y => y.id !== x.id); a.push(x); localStorage.setItem(IG_LS, JSON.stringify(a)); ok = true; } catch (e) {} }
  if (ok && igCache) { const i = igCache.findIndex(y => y.id === x.id); if (i >= 0) igCache[i] = x; else igCache.push(x); }
  return ok;
}
async function igDel(id){
  const db = await shotIdb();
  if (db) { try { await new Promise((res, rej) => { const tx = db.transaction('shots', 'readwrite'); tx.objectStore('shots').delete(id); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); } catch (e) {} }
  try { localStorage.setItem(IG_LS, JSON.stringify(igLs().filter(x => x.id !== id))); } catch (e) {}
  if (igCache) igCache = igCache.filter(x => x.id !== id);
}
function igZoneHtml(ui){
  return '<div class="shotzone igzone" contenteditable="true" spellcheck="false" data-igzone="' + ui + '" role="textbox" aria-label="Paste an infographic here" data-ph="Click here, then paste a picture (⌘V / Ctrl+V), drop one in, or choose a file. Then drag boxes over the details you want to hide."></div>'
    + '<div class="toolbar"><label class="btn"><input type="file" accept="image/*" data-igfile="' + ui + '" hidden>📷 Choose picture</label><span class="hint grow">Kept only in this browser on this device. Nothing is uploaded.</span></div>';
}
function igThumbs(list){
  return list.slice().sort((a, b) => b.ts - a.ts).map(x => '<button class="shot igthumb" data-igopen="' + x.id + '" title="' + esc(x.title || 'Open') + '"><img src="' + x.img + '" alt="' + esc(x.title || 'My infographic') + '" loading="lazy"><span>' + esc(x.title || new Date(x.ts).toLocaleDateString('en-GB')) + ' · 🔒 ' + (x.boxes || []).length + '</span></button>').join('');
}
function igBoxHtml(ui){
  return '<div class="igpanel-in"><b>🖼️ My infographics</b> <span class="hint" data-ign="' + ui + '"></span><p class="hint" style="margin:4px 0 6px">Got a picture you like, from an AI or a book? Paste it here, box over the drugs, numbers and signs, then quiz yourself by tapping the boxes. Check every detail against the poster above: AI pictures get details wrong.</p><div class="shotgrid" data-iggrid="' + ui + '"></div>' + igZoneHtml(ui) + '</div>';
}
async function igRefreshBox(ui){
  const all = await igAll(), mine = all.filter(x => x.u === ui);
  const g = document.querySelector('[data-iggrid="' + ui + '"]'); if (g) g.innerHTML = igThumbs(mine);
  const n = document.querySelector('[data-ign="' + ui + '"]'); if (n) n.textContent = mine.length ? '· ' + mine.length + ' saved' : '';
}
async function igRefreshHub(){
  const all = await igAll(), body = document.getElementById('igHubBody'); if (!body) return;
  const n = document.getElementById('igHubN'); if (n) n.textContent = all.length ? '· ' + all.length + ' saved on this device' : '· pictures you box over and quiz yourself on';
  const groups = {}; all.forEach(x => (groups[x.u] = groups[x.u] || []).push(x));
  let h = '<p class="hint" style="margin:6px 0">Paste a picture on any condition\'s 🖼️ Pictures tab to file it there, or below to keep it unsorted.</p>';
  Object.keys(groups).map(Number).sort((a, b) => a - b).forEach(ui => { const u = UNITS[ui]; h += '<div class="vgroup"><div class="toolbar"><b class="grow">' + (u ? esc(u.name) : '📥 Unsorted') + ' <span class="hint">· ' + groups[ui].length + '</span></b>' + (u ? '<button class="btn ghost" data-u="' + u.i + '" data-mode="read">Open →</button>' : '') + '</div><div class="shotgrid">' + igThumbs(groups[ui]) + '</div></div>'; });
  body.innerHTML = h + igZoneHtml(-1);
}
async function igSave(file, ui){
  let c; try { c = await compressImg(file); } catch (e) { return toast('That file is not an image'); }
  const x = {id: 'ig' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), ig: 1, u: ui, title: '', img: c.d, w: c.w, h: c.h, ts: Date.now(), boxes: []};
  await igAll();
  if (!(await igPut(x))) return toast('Could not save: browser storage is full or blocked');
  document.querySelectorAll('[data-igzone]').forEach(z => z.textContent = '');
  if (route.view === 'unit') igRefreshBox(ui); else igRefreshHub();
  igOpen(x.id, 'draw');
}
document.addEventListener('paste', e => {
  const z = e.target && e.target.closest ? e.target.closest('[data-igzone]') : null; if (!z) return;
  e.preventDefault(); e.stopImmediatePropagation();
  const cd = e.clipboardData; let f = null;
  if (cd) { f = Array.from(cd.files || []).find(x => /^image\//.test(x.type)) || null; if (!f && cd.items) for (const it of cd.items) if (it.kind === 'file' && /^image\//.test(it.type)) { f = it.getAsFile(); break; } }
  if (!f) return toast('No picture on the clipboard: copy the image first');
  igSave(f, +z.dataset.igzone);
}, true);
document.addEventListener('drop', e => { const z = e.target.closest && e.target.closest('[data-igzone]'); if (!z) return; e.preventDefault(); e.stopImmediatePropagation(); const f = Array.from((e.dataTransfer && e.dataTransfer.files) || []).find(x => /^image\//.test(x.type)); if (f) igSave(f, +z.dataset.igzone); }, true);
document.addEventListener('dragover', e => { if (e.target.closest && e.target.closest('[data-igzone]')) e.preventDefault(); });
document.addEventListener('input', e => { const z = e.target.closest && e.target.closest('[data-igzone]'); if (z && !z.querySelector('img')) z.textContent = ''; });
document.addEventListener('change', e => {
  const f = e.target.dataset && e.target.dataset.igfile; if (f != null && e.target.files && e.target.files[0]) { igSave(e.target.files[0], +f); e.target.value = ''; return; }
  if (e.target.dataset && e.target.dataset.igunit != null && igCur) { igCur.u = +e.target.value; igPut(igCur).then(() => { toast('Moved'); if (route.view === 'posters') igRefreshHub(); else if (route.view === 'unit') igRefreshBox(route.u); }); }
});
document.addEventListener('toggle', e => { if (e.target.id === 'igHub') { S.set.igHubOpen = e.target.open; save(); } }, true);

/* the viewer: 🔒 study mode hides every box until tapped; ✏️ draw mode adds boxes by dragging */
function igBoxesHtml(x){ return (x.boxes || []).map((b, k) => '<div class="igbox" data-igb="' + k + '" style="left:' + (b[0] * 100).toFixed(2) + '%;top:' + (b[1] * 100).toFixed(2) + '%;width:' + (b[2] * 100).toFixed(2) + '%;height:' + (b[3] * 100).toFixed(2) + '%">' + (igMode === 'draw' ? '<span>✕</span>' : '') + '</div>').join(''); }
function igDraw(){
  const x = igCur, ov = document.getElementById('igView'); if (!x || !ov) return;
  const seen = new Set(), opts = UNITS.filter(u => !seen.has(u.name) && seen.add(u.name)).map(u => '<option value="' + u.i + '"' + (u.i === x.u ? ' selected' : '') + '>' + esc(u.name) + '</option>').join('');
  ov.innerHTML = '<div class="modal igmodal" role="dialog" aria-label="My infographic"><div class="toolbar"><input class="shotnote igtitle" data-igtitle value="' + esc(x.title || '') + '" placeholder="Name this picture" aria-label="Name"><span class="grow"></span>'
    + '<div class="seg"><button type="button" data-igmode="study" class="' + (igMode === 'study' ? 'on' : '') + '">🔒 Study</button><button type="button" data-igmode="draw" class="' + (igMode === 'draw' ? 'on' : '') + '">✏️ Draw boxes</button></div><button class="iconbtn" data-igclose aria-label="Close">✕</button></div>'
    + '<p class="hint" style="margin:0">' + (igMode === 'draw' ? 'Drag over each detail you want to hide: drugs, doses, numbers, signs. Tap ✕ to remove a box.' : 'Say what is under each box, then tap it. <span class="kbd">N</span> next · <span class="kbd">H</span> hide all · <span class="kbd">Esc</span> close.') + '</p>'
    + '<div class="igstage' + (igMode === 'draw' ? ' draw' : '') + '" data-igstage><img src="' + x.img + '" alt="' + esc(x.title || 'My infographic') + '" draggable="false">' + igBoxesHtml(x) + '</div>'
    + '<div class="toolbar"><label class="hint">Filed under <select class="jsel" data-igunit style="width:auto"><option value="-1"' + (x.u < 0 ? ' selected' : '') + '>📥 Unsorted</option>' + opts + '</select></label><span class="grow"></span><span class="hint">' + (x.boxes || []).length + ' boxes</span>' + (igMode === 'study' ? '<button class="btn ghost" data-igall="1">Show all</button><button class="btn ghost" data-igall="0">Hide all</button>' : '') + '<button class="btn ghost" data-igdel="' + x.id + '">🗑 Delete</button></div></div>';
  ov.hidden = false;
}
async function igOpen(id, mode){
  const all = await igAll(), x = all.find(y => y.id === id); if (!x) return;
  igCur = x; igMode = mode || ((x.boxes || []).length ? 'study' : 'draw');
  let ov = document.getElementById('igView');
  if (!ov) { ov = document.createElement('div'); ov.className = 'overlay'; ov.id = 'igView'; document.body.appendChild(ov); ov.addEventListener('click', e => { if (e.target === ov) igClose(); }); }
  igDraw();
}
function igClose(){ const ov = document.getElementById('igView'); if (ov) ov.hidden = true; igCur = null; if (route.view === 'unit') igRefreshBox(route.u); else if (route.view === 'posters') igRefreshHub(); }
document.addEventListener('click', e => {
  const t = e.target; if (!t || !t.closest) return;
  const op = t.closest('[data-igopen]'); if (op) { e.stopImmediatePropagation(); igOpen(op.dataset.igopen); return; }
  if (!igCur || !t.closest('#igView')) return;
  if (t.closest('[data-igclose]')) return igClose();
  const md = t.closest('[data-igmode]'); if (md) { igMode = md.dataset.igmode; igDraw(); return; }
  const al = t.closest('[data-igall]'); if (al) { document.querySelectorAll('#igView .igbox').forEach(b => b.classList.toggle('rv', al.dataset.igall === '1')); return; }
  const dl = t.closest('[data-igdel]'); if (dl) { if (confirm('Delete this picture from this device?')) igDel(igCur.id).then(igClose); return; }
  const bx = t.closest('.igbox');
  if (bx && igMode === 'study') { bx.classList.toggle('rv'); return; }
  if (bx && igMode === 'draw' && t.closest('.igbox span')) { igCur.boxes.splice(+bx.dataset.igb, 1); igPut(igCur).then(igDraw); }
});
let igDrag = null;
document.addEventListener('pointerdown', e => {
  const st = e.target.closest && e.target.closest('[data-igstage].draw'); if (!st || !igCur || e.target.closest('.igbox span')) return;
  const r = st.getBoundingClientRect(); e.preventDefault();
  const el = document.createElement('div'); el.className = 'igbox drawing'; st.appendChild(el);
  igDrag = {st, r, x0: (e.clientX - r.left) / r.width, y0: (e.clientY - r.top) / r.height, el, id: e.pointerId};
  try { st.setPointerCapture(e.pointerId); } catch (er) {}
});
document.addEventListener('pointermove', e => {
  if (!igDrag || e.pointerId !== igDrag.id) return;
  const d = igDrag, x = Math.min(1, Math.max(0, (e.clientX - d.r.left) / d.r.width)), y = Math.min(1, Math.max(0, (e.clientY - d.r.top) / d.r.height));
  d.b = [Math.min(d.x0, x), Math.min(d.y0, y), Math.abs(x - d.x0), Math.abs(y - d.y0)];
  Object.assign(d.el.style, {left: d.b[0] * 100 + '%', top: d.b[1] * 100 + '%', width: d.b[2] * 100 + '%', height: d.b[3] * 100 + '%'});
});
document.addEventListener('pointerup', e => {
  if (!igDrag || e.pointerId !== igDrag.id) return;
  const d = igDrag; igDrag = null;
  if (d.b && d.b[2] > 0.01 && d.b[3] > 0.008 && igCur) { igCur.boxes = igCur.boxes || []; igCur.boxes.push(d.b.map(v => Math.round(v * 10000) / 10000)); igPut(igCur).then(igDraw); }
  else d.el.remove();
});
document.addEventListener('change', e => { if (e.target.dataset && e.target.dataset.igtitle != null && igCur) { igCur.title = e.target.value.trim(); igPut(igCur); } });
document.addEventListener('keydown', e => {
  const ov = document.getElementById('igView'); if (!ov || ov.hidden || !igCur) return;
  const tg = e.target; if (tg && /^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName)) { if (e.key === 'Escape') tg.blur(); return; }
  const k = (e.key || '').toLowerCase();
  if (k === 'escape') { e.preventDefault(); e.stopImmediatePropagation(); igClose(); return; }
  if (igMode !== 'study') return;
  if (k === 'n') { const nx = ov.querySelector('.igbox:not(.rv)'); if (nx) nx.classList.add('rv'); e.preventDefault(); e.stopImmediatePropagation(); }
  else if (k === 'h' || k === 'l') { ov.querySelectorAll('.igbox').forEach(b => b.classList.remove('rv')); e.preventDefault(); e.stopImmediatePropagation(); }
}, true);

/* ⌘F / Ctrl+F jumps to the search bar; press it again there for the browser's own find */
document.addEventListener('keydown', e => {
  if (!(e.metaKey || e.ctrlKey) || e.altKey || e.shiftKey || (e.key || '').toLowerCase() !== 'f') return;
  const q = document.getElementById('q'); if (!q || document.activeElement === q) return;
  e.preventDefault(); e.stopImmediatePropagation(); q.focus(); q.select();
  if (q.value.trim().length >= 2) doSearch(q.value);
}, true);
