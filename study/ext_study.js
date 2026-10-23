/* ---------- v0.6: atlas, guideline notes, systems, screenshot vault, blind clincher sniper ---------- */
const usys = u => MEV.unitSys(u.i, u.w);
const UPD_LINES = D.upd || {};
function applyUpd(){
  for (const id in UPD_LINES) { const el = document.getElementById('L' + id); if (el && !el.querySelector('.mev-upd')) el.insertAdjacentHTML('beforeend', '<span class="mev-upd">' + esc(UPD_LINES[id]) + '</span>'); }
}
new MutationObserver(() => { clearTimeout(applyUpd.t); applyUpd.t = setTimeout(applyUpd, 30); }).observe($('#main'), {childList: true, subtree: true});
MEV.onLibrary = id => { go({view: 'visual'}); if (id) requestAnimationFrame(() => { const c = document.getElementById('SD-' + id); if (c) { c.scrollIntoView({block: 'start'}); c.classList.add('flash'); setTimeout(() => c.classList.remove('flash'), 1600); } }); };
MEV.onQuiz = ok => { if (ok) addXp(3); };

function extHeader(u){
  setTimeout(() => refreshShotBox(u.i, false), 0);
  return (u.spd ? '<div class="spdline">' + spdBadge(u) + '</div>' : '') + MEV.atlasRowHtml(u.name, usys(u), u.name + ' ' + (weekName[u.w] || '')) + jgChipsHtml(u) + shotBoxHtml(u.i);
}

/* systems & presentations */
let jumpOpen = false;
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('jump')) jumpOpen = e.target.open; }, true);
function jumpHtml(){
  const sys = S.set.sys || '';
  return '<details class="jump"' + (sys || jumpOpen ? ' open' : '') + '><summary>🗂 Systems &amp; presentations' + (sys ? ' · ' + esc(MEV.sysLabel(sys)) : '') + '</summary><div class="jumpb">'
    + '<label>System<select class="jsel" data-jsys aria-label="Filter conditions by system"><option value="">All systems</option>' + MEV.sysOptions(sys) + '</select></label>'
    + '<label>Presentation or framework<select class="jsel" data-jpres aria-label="Jump to a presentation"><option value="">Jump to…</option><optgroup label="ILO weeks">' + WEEKS.map(w => '<option value="w:' + w.id + '">' + esc(w.name) + '</option>').join('') + '</optgroup><optgroup label="Frameworks (chest pain, SOB, abdo pain, jaundice…)">' + FW.map(f => '<option value="f:' + f.id + '">' + esc(f.title) + '</option>').join('') + '</optgroup></select></label></div></details>';
}
function homeSysHtml(){
  return '<details class="sysrow"' + (S.set.sys || S.set.spd ? ' open' : '') + '><summary>🗂 Browse by system or speed</summary><div class="chips">' + MEV.SYS.map(s => { const n = UNITS.filter(u => usys(u) === s[0]).length; return '<button class="chip' + (S.set.sys === s[0] ? ' on' : '') + '" data-sysset="' + s[0] + '">' + esc(s[1]) + ' · ' + n + '</button>'; }).join('') + '</div>' + spdChipsHtml() + '</details>';
}

/* ----- screenshot vault (IndexedDB, falls back to localStorage) ----- */
const SHOT_LS = 'medengine-shots-v1';
let shotDb = null, shotDbTried = false, shotsCache = null, vaultSys = '';
function shotIdb(){
  return new Promise(res => {
    if (shotDb || shotDbTried) return res(shotDb);
    shotDbTried = true;
    try {
      const rq = indexedDB.open('medengine-study', 1);
      rq.onupgradeneeded = () => { const db = rq.result; if (!db.objectStoreNames.contains('shots')) db.createObjectStore('shots', {keyPath: 'id'}); };
      rq.onsuccess = () => { shotDb = rq.result; res(shotDb); };
      rq.onerror = () => res(null); rq.onblocked = () => res(null);
    } catch (e) { res(null); }
  });
}
function lsShots(){ try { return JSON.parse(localStorage.getItem(SHOT_LS) || '[]'); } catch (e) { return []; } }
async function shotsAll(){
  if (shotsCache) return shotsCache;
  const db = await shotIdb();
  if (db) { try { shotsCache = await new Promise((res, rej) => { const r = db.transaction('shots').objectStore('shots').getAll(); r.onsuccess = () => res(r.result || []); r.onerror = () => rej(r.error); }); return shotsCache; } catch (e) {} }
  shotsCache = lsShots(); return shotsCache;
}
async function shotPut(s){
  const db = await shotIdb(); let ok = false;
  if (db) { try { await new Promise((res, rej) => { const tx = db.transaction('shots', 'readwrite'); tx.objectStore('shots').put(s); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); ok = true; } catch (e) {} }
  if (!ok) { try { const a = lsShots().filter(x => x.id !== s.id); a.push(s); localStorage.setItem(SHOT_LS, JSON.stringify(a)); ok = true; } catch (e) {} }
  if (ok && shotsCache) { const i = shotsCache.findIndex(x => x.id === s.id); if (i >= 0) shotsCache[i] = s; else shotsCache.push(s); }
  return ok;
}
async function shotDel(id){
  const db = await shotIdb();
  if (db) { try { await new Promise((res, rej) => { const tx = db.transaction('shots', 'readwrite'); tx.objectStore('shots').delete(id); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); } catch (e) {} }
  try { localStorage.setItem(SHOT_LS, JSON.stringify(lsShots().filter(x => x.id !== id))); } catch (e) {}
  if (shotsCache) shotsCache = shotsCache.filter(x => x.id !== id);
}
function compressImg(file){
  return new Promise((res, rej) => {
    const url = URL.createObjectURL(file), img = new Image();
    img.onload = () => {
      const k = Math.min(1, 1600 / Math.max(img.naturalWidth, img.naturalHeight)), w = Math.max(1, Math.round(img.naturalWidth * k)), h = Math.max(1, Math.round(img.naturalHeight * k));
      const c = document.createElement('canvas'); c.width = w; c.height = h;
      const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, w, h); x.drawImage(img, 0, 0, w, h);
      let d = c.toDataURL('image/webp', 0.78); if (!/^data:image\/webp/.test(d)) d = c.toDataURL('image/jpeg', 0.8);
      URL.revokeObjectURL(url); res({d, w, h});
    };
    img.onerror = () => { URL.revokeObjectURL(url); rej(new Error('not an image')); };
    img.src = url;
  });
}
function shotBoxHtml(ui){
  return '<details class="shotbox" data-shotbox="' + ui + '"><summary>📋 Paste exam image <span class="hint" data-shotn="' + ui + '"></span></summary><div class="shotin">'
    + '<div class="shotzone" contenteditable="true" spellcheck="false" data-shotzone="' + ui + '" role="textbox" aria-label="Paste a screenshot here" data-ph="Click or tap here, then paste a question image that tricked you (Ctrl+V / ⌘V, or long-press → Paste)."></div>'
    + '<div class="toolbar"><input class="shotnote" type="text" data-shotnote="' + ui + '" placeholder="What tricked me? (optional, saved with the image)" aria-label="Note"><label class="btn"><input type="file" accept="image/*" data-shotfile="' + ui + '" hidden>📷 Choose image</label><button class="btn ghost" data-go="vault">Vault →</button></div>'
    + '<p class="hint" style="margin:0">Save only the ones you got wrong: the 15–20 images that actually tricked you. Kept in this browser on this device.</p><div class="shotgrid" data-shotgrid="' + ui + '"></div></div></details>';
}
function thumbsHtml(list){
  return list.slice().sort((a, b) => b.ts - a.ts).map(s => '<button class="shot" data-shotopen="' + s.id + '" title="' + esc(s.note || 'Open') + '"><img src="' + s.img + '" alt="Saved exam screenshot" loading="lazy"><span>' + esc(s.note || new Date(s.ts).toLocaleDateString('en-GB')) + '</span></button>').join('');
}
async function refreshShotBox(ui, open){
  const list = await shotsAll(), mine = list.filter(s => s.u === ui);
  const n = $('[data-shotn="' + ui + '"]'); if (n) n.textContent = mine.length ? '· ' + mine.length + ' saved' : '';
  const box = $('[data-shotbox="' + ui + '"]'); if (!box) return;
  if (open) box.open = true;
  if (box.open) { const g = $('[data-shotgrid="' + ui + '"]'); if (g) g.innerHTML = thumbsHtml(mine); }
  const q = $('.qbtn[data-go="vault"] .n'); if (q) q.textContent = list.length;
}
function refreshAllShotViews(){ if (route.view === 'vault') return viewVault($('#main')); if (route.view === 'unit') refreshShotBox(route.u, true); }
async function saveShot(file, ui){
  let c;
  try { c = await compressImg(file); } catch (e) { return toast('That file is not an image'); }
  const noteEl = $('[data-shotnote="' + ui + '"]');
  const s = {id: 'sh' + Date.now().toString(36) + Math.random().toString(36).slice(2, 6), u: ui, note: noteEl ? noteEl.value.trim() : '', img: c.d, w: c.w, h: c.h, ts: Date.now(), rv: 0, ok: 0};
  await shotsAll();
  if (!(await shotPut(s))) return toast('Could not save: browser storage is full or blocked');
  if (noteEl) noteEl.value = '';
  const z = $('[data-shotzone="' + ui + '"]'); if (z) z.textContent = '';
  toast('📋 Saved' + (UNITS[ui] ? ' to ' + UNITS[ui].name : ' to the vault'));
  if (route.view === 'vault') viewVault($('#main')); else refreshShotBox(ui, true);
}
document.addEventListener('paste', e => {
  const tg = e.target, zone = tg && tg.closest ? tg.closest('[data-shotzone]') : null;
  if (!zone && tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA')) return;
  const ui = zone ? +zone.dataset.shotzone : route.view === 'unit' ? route.u : route.view === 'vault' ? -1 : null;
  if (ui == null) return;
  const cd = e.clipboardData; let file = null;
  if (cd) { file = Array.from(cd.files || []).find(f => /^image\//.test(f.type)) || null; if (!file && cd.items) for (const it of cd.items) if (it.kind === 'file' && /^image\//.test(it.type)) { file = it.getAsFile(); break; } }
  if (!file) { if (zone) { e.preventDefault(); toast('No image on the clipboard: copy the screenshot first'); } return; }
  e.preventDefault(); saveShot(file, ui);
});
document.addEventListener('input', e => { const z = e.target.closest && e.target.closest('[data-shotzone]'); if (z && !z.querySelector('img')) z.textContent = ''; });
document.addEventListener('dragover', e => { if (e.target.closest && e.target.closest('[data-shotzone]')) e.preventDefault(); });
document.addEventListener('drop', e => { const z = e.target.closest && e.target.closest('[data-shotzone]'); if (!z) return; e.preventDefault(); const f = Array.from((e.dataTransfer && e.dataTransfer.files) || []).find(x => /^image\//.test(x.type)); if (f) saveShot(f, +z.dataset.shotzone); });
document.addEventListener('toggle', e => { const el = e.target; if (el.classList && el.classList.contains('shotbox') && el.open) refreshShotBox(+el.dataset.shotbox, false); }, true);
function openShot(id){
  const s = (shotsCache || []).find(x => x.id === id); if (!s) return;
  let ov = $('#shotView');
  if (!ov) { ov = document.createElement('div'); ov.className = 'overlay'; ov.id = 'shotView'; document.body.appendChild(ov); ov.addEventListener('click', e => { if (e.target === ov) ov.hidden = true; }); }
  const u = UNITS[s.u];
  ov.innerHTML = '<div class="modal shotmodal" role="dialog" aria-label="Saved screenshot"><div class="toolbar"><b class="grow">📋 ' + (u ? esc(u.name) : 'Unsorted') + '</b><button class="iconbtn" data-shotclose aria-label="Close">✕</button></div><div class="shotbig"><img src="' + s.img + '" alt="Saved exam screenshot"></div><input class="shotnote" data-shotedit="' + s.id + '" value="' + esc(s.note || '') + '" placeholder="What tricked me?" aria-label="Note"><div class="toolbar">' + (u ? '<button class="btn" data-u="' + u.i + '" data-mode="read">📖 ' + esc(u.name) + '</button>' : '') + '<span class="grow"></span><span class="hint">Reviewed ' + (s.rv || 0) + '×</span><button class="btn ghost" data-shotdel="' + s.id + '">🗑 Delete</button></div></div>';
  ov.hidden = false;
}
function viewVault(m){
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">📋 Vault</span></div><h1>Screenshot vault</h1><p class="hint" style="margin:0">The exam images that tricked you, filed under their ILO condition. Paste on any condition page (Ctrl+V / ⌘V, or long-press → Paste), or below to file it as unsorted. 🧠 Review hides your note until you have named the trap yourself.</p></div><div id="vaultBody" class="panel">Loading…</div></div>';
  shotsAll().then(list => {
    const box = $('#vaultBody'); if (!box) return;
    const keep = list.filter(s => !vaultSys || (UNITS[s.u] ? usys(UNITS[s.u]) === vaultSys : vaultSys === '-'));
    let h = '<div class="toolbar">' + (list.length ? '<button class="btn primary" data-vrev>🧠 Review ' + keep.length + '</button>' : '') + '<select class="jsel" data-vsys aria-label="Filter by system" style="width:auto"><option value="">All systems</option>' + MEV.sysOptions(vaultSys) + '</select><span class="grow"></span><span class="hint">' + list.length + ' saved</span></div>';
    h += '<div class="shotzone" contenteditable="true" spellcheck="false" data-shotzone="-1" role="textbox" aria-label="Paste a screenshot here" data-ph="Paste here to save an unsorted image (or open the condition first so it is filed under it)."></div><div class="toolbar"><input class="shotnote" type="text" data-shotnote="-1" placeholder="What tricked me? (optional)"><label class="btn"><input type="file" accept="image/*" data-shotfile="-1" hidden>📷 Choose image</label></div>';
    if (!list.length) h += '<div class="empty">Nothing saved yet. Miss an image question on Passmedicine? Screenshot it, open the matching condition here and paste.</div>';
    const groups = {}; keep.forEach(s => (groups[s.u] = groups[s.u] || []).push(s));
    Object.keys(groups).map(Number).sort((a, b) => a - b).forEach(ui => {
      const u = UNITS[ui];
      h += '<div class="vgroup"><div class="toolbar"><b class="grow">' + (u ? esc(u.name) : '📥 Unsorted') + ' <span class="hint">· ' + groups[ui].length + '</span></b>' + (u ? '<button class="btn ghost" data-u="' + u.i + '" data-mode="read">Open →</button>' : '') + '</div><div class="shotgrid">' + thumbsHtml(groups[ui]) + '</div></div>';
    });
    box.innerHTML = h;
  });
}
function vaultReview(){
  const list = (shotsCache || []).filter(s => !vaultSys || (UNITS[s.u] ? usys(UNITS[s.u]) === vaultSys : false));
  if (!list.length) return toast('Nothing to review');
  const score = s => (s.ok || 0) / Math.max(1, s.rv || 0);
  session = {kind: 'vault', list: list.slice().sort((a, b) => score(a) - score(b) || (a.last || 0) - (b.last || 0)), i: 0, rev: false, got: 0};
  drawVaultReview();
}
function drawVaultReview(){
  const s = session, box = $('#vaultBody'); if (!box || !s || s.kind !== 'vault') return;
  if (s.i >= s.list.length) { box.innerHTML = '<div class="toolbar"><b class="grow">🧠 Review done: ' + s.got + ' of ' + s.list.length + ' named before the reveal</b><button class="btn primary" data-vrev>Again</button><button class="btn" data-vexit>Back to the vault</button></div>'; return; }
  const x = s.list[s.i], u = UNITS[x.u];
  let h = '<div class="toolbar"><b class="grow">🧠 Review ' + (s.i + 1) + ' / ' + s.list.length + '</b><button class="btn ghost" data-vexit>Exit</button></div><div class="vrev"><img src="' + x.img + '" alt="Saved exam screenshot"></div>';
  if (!s.rev) h += '<p class="hint" style="margin:0">What was the trap? Say it out loud, then reveal.</p><div class="toolbar"><button class="btn primary" data-vreveal>Reveal <span class="kbd">Space</span></button></div>';
  else h += '<div class="kl kl-out"><span class="ki">🪤</span><span><b>' + (u ? esc(u.name) : 'Unsorted') + '</b>' + (x.note ? ': ' + esc(x.note) : ' (no note saved)') + '</span></div><div class="toolbar"><button class="btn primary" data-vgot="1">✅ Got it <span class="kbd">1</span></button><button class="btn" data-vgot="0">❌ Still tricky <span class="kbd">2</span></button>' + (u ? '<button class="btn ghost" data-u="' + u.i + '" data-mode="read">📖 Open ' + esc(u.name) + '</button>' : '') + '</div>';
  box.innerHTML = h;
}
async function vaultGrade(ok){
  const s = session; if (!s || s.kind !== 'vault' || !s.rev) return;
  const x = s.list[s.i]; x.rv = (x.rv || 0) + 1; if (ok) { x.ok = (x.ok || 0) + 1; s.got++; addXp(2); } x.last = Date.now();
  await shotPut(x); s.i++; s.rev = false; drawVaultReview();
}

/* ----- 🎯 blind clincher sniper ----- */
const SNP_META = /differentials|pain ladder|describing skin|overview|catheterisation|IV fluids|joint replacements/i;
const SNP_STOP = new Set(['acute','chronic','disease','diseases','disorder','disorders','syndrome','syndromes','other','problems','overview','primary','secondary','cancer','tumours','tumour','infection','infections','failure','differentials','related','including','incl','children','adults','upper','lower','lung','skin','heart','with','and','the','of','in','&','drugs','toxicity','misuse','pain','type','test','care','from']);
let SNPU = null, snpCfg = {sys: '', wk: '', miss: false, mode: (S.set && ['clue', 'm1', 'm2', 'm3', 'tri'].includes(S.set.snpm)) ? S.set.snpm : 'clue'}, snpRecent = [];
function snpUnits(){
  if (SNPU) return SNPU;
  const seen = new Set();
  SNPU = UNITS.filter(u => { if (SNP_META.test(u.name) || seen.has(u.name)) return false; seen.add(u.name); return (u.ck || []).some(i => CLK[i] && (CLK[i][0] === 'in' || CLK[i][0] === 'lab')); });
  return SNPU;
}
const snpState = () => (S.snp = Object.assign({n: 0, dx: 0, act: 0, trap: 0, best: 0, miss: {}}, S.snp || {}));
const reEsc = s => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
function snpTokens(u){
  if (u._tok) return u._tok;
  const parts = u.name.replace(/[()]/g, ' / ').split(/\s*(?:\/|,|&|;|\band\b|\bincl\b|\bvs\b)\s*/i).map(s => s.trim()).filter(s => s.length >= 2 && !SNP_STOP.has(s.toLowerCase()));
  const words = [], acro = [], stems = [];
  parts.forEach(p => {
    const ws = p.split(/\s+/);
    ws.forEach(w => {
      const c = w.replace(/[^A-Za-z0-9'’-]/g, '');
      if ((c.length >= 4 && !SNP_STOP.has(c.toLowerCase())) || /^[A-Z0-9]{2,5}$/.test(c)) {
        words.push(c);
        if (/ies$/i.test(c) && c.length >= 6) words.push(c.slice(0, -3) + 'y');
        else if (/sses$/i.test(c)) words.push(c.slice(0, -2));
        else if (/ae$/i.test(c) && c.length >= 6) words.push(c.slice(0, -1));
        else if (/[^s]s$/i.test(c) && c.length >= 6) words.push(c.slice(0, -1));
        if (/^[A-Za-z]{7,}$/.test(c)) stems.push(c.slice(0, Math.max(5, c.length - 3)));
        if (c.indexOf('-') > 0) c.split('-').forEach(h => { if (h.length >= 4 && !SNP_STOP.has(h.toLowerCase()) && !/^related$/i.test(h)) words.push(h); });
      }
    });
    const a = ws.filter(w => !/^(of|the|and|in|with)$/i.test(w)).map(w => w[0]).join('').toUpperCase();
    if (ws.length >= 2 && a.length >= 2 && a.length <= 5) acro.push(a);
  });
  return (u._tok = {t: [...new Set(parts.concat(words))].sort((a, b) => b.length - a.length), a: [...new Set(acro)], s: [...new Set(stems)]});
}
function snpMask(text, u){
  const tk = snpTokens(u); let t = text;
  tk.t.forEach(tok => { const tail = /^[A-Za-z'’-]{4,}$/.test(tok) ? "[a-z'’]{0,3}" : 's?'; t = t.replace(new RegExp('(^|[^A-Za-z])' + reEsc(tok) + tail + '(?=$|[^A-Za-z])', 'gi'), (m, a) => a + '\u2592\u2592\u2592'); });
  tk.s.forEach(st => { t = t.replace(new RegExp('(^|[^A-Za-z])' + reEsc(st) + '[a-z]*(?=$|[^A-Za-z])', 'gi'), (m, a) => a + '\u2592\u2592\u2592'); });
  tk.a.forEach(ac => { t = t.replace(new RegExp('(^|[^A-Za-z])' + reEsc(ac) + 's?(?=$|[^A-Za-z])', 'g'), (m, a) => a + '\u2592\u2592\u2592'); });
  return t;
}
const snpHtml = t => fmtRich(t).replace(/▒▒▒/g, '<span class="snp-mask" title="hidden">▒▒▒</span>');
const snpClean = (t, u) => snpMask(String(t || '').replace(/^[^:→]{2,32}:\s+/, ''), u);
function snpDistractors(u, n){
  const P = snpUnits(), out = [];
  [P.filter(x => x.w === u.w), P.filter(x => x.w !== u.w && usys(x) === usys(u)), P].forEach(arr => shuffle(arr, Math.random).forEach(x => { if (out.length < n && x.name !== u.name && !out.some(y => y.name === x.name)) out.push(x); }));
  return out;
}
function snpBuild(u, mut){
  const clues = u.ck.filter(i => CLK[i] && (CLK[i][0] === 'in' || CLK[i][0] === 'lab'));
  const ci = clues[Math.floor(Math.random() * clues.length)];
  const dis = snpDistractors(u, 3), dx = shuffle([u].concat(dis), Math.random);
  const steps = [{k: 'dx', opts: dx.map(x => ({t: x.name, u: x.i})), ans: dx.indexOf(u), pick: null}];
  const key = u.ix1 && Math.random() < 0.35 ? 'ix1' : 'act';
  if (u[key]) {
    const correct = snpClean(u[key], u), seen = new Set([normA(correct)]), opts = [{t: correct, ok: true}];
    dis.concat(snpDistractors(u, 9)).forEach(x => { if (opts.length >= 4 || !x[key]) return; const t = snpClean(x[key], x), n = normA(t); if (!n || seen.has(n)) return; seen.add(n); opts.push({t}); });
    if (opts.length >= 3) { const sh = shuffle(opts, Math.random); steps.push({k: key === 'ix1' ? 'ix' : 'act', opts: sh, ans: sh.findIndex(o => o.ok), pick: null}); }
  }
  const outs = u.ck.filter(i => CLK[i] && CLK[i][0] === 'out');
  if (outs.length) steps.push({k: 'trap', text: CLK[outs[Math.floor(Math.random() * outs.length)]][1], rev: false, got: null});
  return {u, clue: CLK[ci][1], steps, cur: 0, mut: mut || null, pickedU: null};
}
function snpPool(){
  const st = snpState();
  let P = snpUnits().filter(u => (!snpCfg.sys || usys(u) === snpCfg.sys) && (!snpCfg.wk || u.w === snpCfg.wk));
  if (snpCfg.miss) P = P.filter(u => st.miss[u.i]);
  return P;
}
function viewSniper(m){
  const st = snpState(), tri = snpCfg.mode !== 'clue', missN = tri ? Object.keys(jgSt().jm).length : Object.keys(st.miss).length, P = tri ? jgPool() : snpPool();
  let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">' + (tri ? '🔺 Name · picture · treat' : '🎯 Sniper') + '</span><span class="grow"></span><span class="mono">best streak ' + st.best + ' · ' + (tri ? jgSt().jg.got + '/' + jgSt().jg.n + ' fired' : st.dx + '/' + st.n + ' named') + '</span></div><h1>' + (tri ? 'Name it · picture it · treat it' : 'Blind clincher sniper') + '</h1><p class="hint" style="margin:0">' + (tri ? 'Exam names from the decoder, three ways: <b>① picture → name</b>, <b>② name → picture</b>, <b>③ what do you do</b>. Answer in your head, reveal, then mark yourself honestly.' : 'One decisive clue with the disease blacked out. <b>Name it</b>, pick the <b>first move</b>, then call the <b>lookalike trap</b>. 🧬 Mutate keeps the presentation and changes one feature of the film.') + '</p></div>';
  h += '<div class="panel snp-cfg">' + snpModeHtml() + '<div class="toolbar"><select class="jsel" data-snpsys aria-label="System" style="width:auto"><option value="">All systems</option>' + MEV.sysOptions(snpCfg.sys) + '</select><select class="jsel" data-snpwk aria-label="ILO week" style="width:auto"><option value="">All ILO weeks</option>' + WEEKS.map(w => '<option value="' + w.id + '"' + (snpCfg.wk === w.id ? ' selected' : '') + '>' + esc(w.name) + '</option>').join('') + '</select><button class="btn' + (snpCfg.miss ? ' primary' : '') + '" data-snpmiss>♻️ Only my misses · ' + missN + '</button><span class="grow"></span><span class="hint">' + P.length + (tri ? ' terms' : ' targets') + '</span></div></div><div id="snp"></div></div>';
  m.innerHTML = h;
  session = {kind: 'sniper', k: 0, shots: 0, hits: 0, streak: 0, earned: 0, t: null};
  snpNext();
}
function snpNext(){
  const s = session; if (!s || s.kind !== 'sniper') return;
  if (snpCfg.mode !== 'clue') return jgNext();
  const st = snpState(), P = snpPool();
  if (!P.length) { const b = $('#snp'); if (b) b.innerHTML = '<div class="panel empty">' + (snpCfg.miss ? 'No misses queued: every target you missed has been re-sniped. 🎯' : 'No targets for this filter.') + '</div>'; return; }
  const misses = P.filter(u => st.miss[u.i]);
  let pool = misses.length && Math.random() < 0.3 ? misses : P;
  const fresh = pool.filter(u => !snpRecent.includes(u.i)); if (fresh.length) pool = fresh;
  const u = pool[Math.floor(Math.random() * pool.length)];
  snpRecent = [u.i].concat(snpRecent).slice(0, Math.min(12, Math.floor(P.length / 2)));
  s.k++; s.t = snpBuild(u); drawSnp();
}
function snpMutate(){
  const s = session; if (!s || s.kind !== 'sniper' || !s.t) return;
  if (s.t.jg) return;
  const T = s.t, P = snpUnits();
  let c = T.pickedU != null && UNITS[T.pickedU] && P.includes(UNITS[T.pickedU]) ? UNITS[T.pickedU] : null;
  if (!c) { const same = P.filter(x => x.w === T.u.w && x.name !== T.u.name); const sys = P.filter(x => usys(x) === usys(T.u) && x.name !== T.u.name); const arr = same.length ? same : sys; c = arr[Math.floor(Math.random() * arr.length)]; }
  if (!c) return snpNext();
  s.k++; s.t = snpBuild(c, {u: T.u, clue: T.clue}); drawSnp();
}
function drawSnp(){
  const s = session, box = $('#snp'); if (!box || !s || s.kind !== 'sniper' || !s.t) return;
  if (s.t.jg) return drawJg();
  const T = s.t, u = T.u, done = T.cur >= T.steps.length;
  let h = '<div class="qcard snp"><div class="qmeta"><span class="code">🎯 Target ' + s.k + '</span>' + (T.mut ? '<span class="code">🧬 Mutation</span>' : '') + '<span class="grow"></span><span class="mono">🔥 ' + s.streak + ' · ' + s.hits + '/' + s.shots + (s.earned ? ' · ฿' + s.earned : '') + '</span></div>';
  if (T.mut) h += '<div class="snp-mut">🧬 Same presentation, one feature changed. Last film: <i>' + fmtRich(T.mut.clue) + '</i> = <b>' + esc(T.mut.u.name) + '</b>. What does the new feature make it?</div>';
  const named = T.steps[0].pick != null;
  h += '<div class="snp-lab">🔍 Decisive clue</div><div class="stem snp-clue">' + (named ? fmtRich(T.clue) : snpHtml(snpMask(dxStrip(T.clue), u))) + '</div>';
  T.steps.forEach((st, i) => {
    if (i > T.cur) return;
    if (st.k === 'trap') {
      h += '<div class="snp-lab">🪤 The lookalike trap</div>';
      if (!st.rev) h += '<p class="hint" style="margin:0">What catches people out with <b>' + esc(u.name) + '</b>? Say it to yourself, then reveal.</p><div class="toolbar"><button class="btn primary" data-snprev>Reveal the trap <span class="kbd">Space</span></button></div>';
      else {
        h += '<div class="kl kl-out"><span class="ki">❌</span><span>' + fmtRich(st.text) + '</span></div>';
        h += st.got == null ? '<div class="toolbar"><button class="btn primary" data-snpgot="1">✅ Got it <span class="kbd">1</span></button><button class="btn" data-snpgot="0">❌ Missed it <span class="kbd">2</span></button></div>' : '<p class="hint" style="margin:0">' + (st.got ? '✅ Trap called (+฿5)' : '❌ Noted: this one comes back') + '</p>';
      }
      return;
    }
    const lab = st.k === 'dx' ? 'Which diagnosis?' : st.k === 'act' ? '💊 First-line action for ' + u.name + '?' : '🧪 First investigation for ' + u.name + '?';
    h += i ? '<div class="snp-lab">' + esc(lab) + '</div>' : '<p class="hint" style="margin:0">' + esc(lab) + '</p>';
    h += '<div class="opts">' + st.opts.map((o, k) => { let c = 'opt'; if (st.pick != null) { if (k === st.ans) c += ' right'; else if (k === st.pick) c += ' wrong'; } return '<button class="' + c + '" data-snp="' + i + ':' + k + '"' + (st.pick != null ? ' disabled' : '') + '><span class="k">' + (k + 1) + '</span><span>' + (st.k === 'dx' ? esc(o.t) : snpHtml(o.t)) + '</span></button>'; }).join('') + '</div>';
  });
  if (done) {
    const r = T.steps.map(st => st.k === 'trap' ? (st.got ? '✅' : '❌') : (st.pick === st.ans ? '✅' : '❌')).join(' ');
    h += '<div class="snp-end"><b>' + r + ' · ' + esc(u.name) + '</b><div class="toolbar"><button class="btn primary" data-snpnext>Next target → <span class="kbd">Enter</span></button><button class="btn" data-snpmut>🧬 Mutate <span class="kbd">M</span></button><button class="btn ghost" data-u="' + u.i + '" data-mode="read">📖 Open ' + esc(u.name) + '</button></div></div>';
  }
  box.innerHTML = h + '</div>';
}
function snpAnswer(i, k){
  const s = session; if (!s || s.kind !== 'sniper') return;
  const T = s.t, st = T.steps[i]; if (!st || st.k === 'trap' || st.pick != null || i !== T.cur) return;
  st.pick = k; const ok = k === st.ans, P = snpState();
  if (st.k === 'dx') {
    s.shots++; P.n++;
    if (ok) { s.hits++; s.streak++; P.dx++; P.best = Math.max(P.best || 0, s.streak); const v = 10 + (s.streak >= 3 ? 5 : 0); s.earned += v; addXp(v); if (P.miss[T.u.i]) { P.miss[T.u.i]--; if (P.miss[T.u.i] <= 0) delete P.miss[T.u.i]; } if (s.streak && s.streak % 5 === 0) toast('🔥 ' + s.streak + ' in a row'); }
    else { s.streak = 0; P.miss[T.u.i] = (P.miss[T.u.i] || 0) + 1; T.pickedU = st.opts[k].u; }
  } else if (ok) { P.act++; s.earned += 10; addXp(10); }
  T.cur++; save(); drawSnp();
}
function snpReveal(){ const s = session; if (!s || s.kind !== 'sniper') return; const st = s.t.steps[s.t.cur]; if (st && st.k === 'trap' && !st.rev) { st.rev = true; drawSnp(); } }
function snpGrade(got){ const s = session; if (!s || s.kind !== 'sniper') return; const st = s.t.steps[s.t.cur]; if (!st || st.k !== 'trap' || !st.rev || st.got != null) return; st.got = got; if (got) { snpState().trap++; s.earned += 5; addXp(5); } else save(); s.t.cur++; drawSnp(); }
function snpKey(e){
  const s = session, T = s.t; if (!T) return false;
  if (T.jg) return jgKey(e);
  const k = e.key.toLowerCase();
  if (T.cur >= T.steps.length) { if (k === 'enter' || k === 'arrowright') { e.preventDefault(); snpNext(); return true; } if (k === 'm') { snpMutate(); return true; } return k === 's'; }
  const st = T.steps[T.cur];
  if (st.k === 'trap') { if (!st.rev && (k === ' ' || k === 'enter')) { e.preventDefault(); snpReveal(); return true; } if (st.rev && (k === '1' || k === '2')) { snpGrade(k === '1'); return true; } return k === 's'; }
  if (/^[1-4]$/.test(k) && +k <= st.opts.length) { e.preventDefault(); snpAnswer(T.cur, +k - 1); return true; }
  return k === 's';
}
function vaultKey(e){
  const s = session; if (s.i >= s.list.length) return false;
  if (!s.rev && (e.key === ' ' || e.key === 'Enter')) { e.preventDefault(); s.rev = true; drawVaultReview(); return true; }
  if (s.rev && (e.key === '1' || e.key === '2')) { vaultGrade(e.key === '1'); return true; }
  return false;
}

/* ----- visual library view ----- */
function viewVisual(m){
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">👁️ Visual</span></div><h1>Visual showdowns</h1><p class="hint" style="margin:0">The ' + MEV.SD.length + ' look-alikes you have to <b>see</b> to separate. Drawn schematics (no photos stored, so the app stays light), the 🎬 mental film for each side, ✂️ the one feature that splits them, and links to real images. 🎯 Quiz me hides the name.</p></div><div class="panel"><div class="toolbar"><input class="shotnote" id="atlasQ" type="search" placeholder="Look anything up: e.g. Wellens, BCC, cherry-red spot" aria-label="Atlas search"><button class="btn primary" data-atlasgo>👁️ Clinical Atlas Lookup</button></div></div><div class="panel">' + MEV.libraryHtml() + '</div></div>';
}

/* ----- click and change handlers for the v0.6 layer ----- */
function extClick(t, d){
  if (extClick7(t, d)) return true;
  if (extClick8(t, d)) return true;
  if (d.atlasgo != null) { MEV.openAtlas((($('#atlasQ') || {}).value || '').trim(), ''); return true; }
  if (d.shotopen) { openShot(d.shotopen); return true; }
  if (d.shotclose != null) { $('#shotView').hidden = true; return true; }
  if (d.shotdel) { if (!t.dataset.armed) { t.dataset.armed = '1'; t.textContent = 'Tap again to delete'; return true; } shotDel(d.shotdel).then(() => { $('#shotView').hidden = true; refreshAllShotViews(); toast('Deleted'); }); return true; }
  if (t.closest('#shotView') && d.u != null) { $('#shotView').hidden = true; return false; }
  if (d.sysset) { S.set.sys = S.set.sys === d.sysset ? '' : d.sysset; save(); renderSide(); if (route.view === 'home') render(); if (S.set.sys && matchMedia('(max-width:860px)').matches) document.body.classList.add('nav'); return true; }
  if (d.snp) { const [i, k] = d.snp.split(':').map(Number); snpAnswer(i, k); return true; }
  if (d.snprev != null) { snpReveal(); return true; }
  if (d.snpgot != null) { snpGrade(d.snpgot === '1'); return true; }
  if (d.snpnext != null) { snpNext(); return true; }
  if (d.snpmut != null) { snpMutate(); return true; }
  if (d.snpmiss != null) { snpCfg.miss = !snpCfg.miss; render(); return true; }
  if (d.vrev != null) { vaultReview(); return true; }
  if (d.vreveal != null) { if (session && session.kind === 'vault') { session.rev = true; drawVaultReview(); } return true; }
  if (d.vgot != null) { vaultGrade(d.vgot === '1'); return true; }
  if (d.vexit != null) { render(); return true; }
  return false;
}
document.addEventListener('change', e => {
  const t = e.target, d = t.dataset || {};
  if (d.jsys != null) { S.set.sys = t.value; save(); renderSide(); if (route.view === 'home') render(); toast(t.value ? 'Showing ' + MEV.sysLabel(t.value) : 'All systems'); return; }
  if (d.jpres != null) { const v = t.value; t.value = ''; if (!v) return; const id = v.slice(2); if (v[0] === 'w') { openWk.add(id); const u = unitsOf(id).find(x => x.refs.length) || unitsOf(id)[0]; return go({view: 'unit', u: u.i, mode: 'read'}); } return go({view: 'fw', id}); }
  if (d.snpsys != null) { snpCfg.sys = t.value; return render(); }
  if (d.snpwk != null) { snpCfg.wk = t.value; return render(); }
  if (d.vsys != null) { vaultSys = t.value; return viewVault($('#main')); }
  if (d.shotfile != null && t.files && t.files[0]) { const f = t.files[0]; t.value = ''; return saveShot(f, +d.shotfile); }
  if (d.shotedit) { const s = (shotsCache || []).find(x => x.id === d.shotedit); if (s) { s.note = t.value.trim(); shotPut(s).then(() => { if (route.view === 'vault') viewVault($('#main')); else if (route.view === 'unit') refreshShotBox(route.u, false); }); } }
});
shotsAll().then(l => { const q = $('.qbtn[data-go="vault"] .n'); if (q) q.textContent = l.length; });

