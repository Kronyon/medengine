/* ===================== v2.7.1 · 🖍️ highlighter + ☁️ sync across devices + 📲 save transfer ===================== */

/* ---------- 🖍️ highlighter: select or tap words in a question and they turn yellow, like Passmedicine ---------- */
function hlPen(){ return S.set.hlPen !== false; }
function hlPenToggle(){ S.set.hlPen = !hlPen(); save(); toast(hlPen() ? '🖍️ Highlighter on: select or tap words' : '🖍️ Highlighter off'); if (hqSess && !hqSess.done) hqDraw(); }
function hlGet(qid){ return (S.hl || {})[qid]; }
function hlCount(qid){ const r = hlGet(qid); return r ? Object.values(r.b || {}).reduce((n, a) => n + a.length, 0) : 0; }
function hlPut(qid, blocks){
  S.hl = S.hl || {}; S.hl[qid] = {ts: Date.now(), b: blocks};
  const ks = Object.keys(S.hl); if (ks.length > 2500) ks.sort((a, b) => (S.hl[a].ts || 0) - (S.hl[b].ts || 0)).slice(0, ks.length - 2500).forEach(k => delete S.hl[k]);
  save();
}
function hlMerge(rs, txt){
  const a = rs.filter(r => r[1] > r[0]).map(r => r.slice()).sort((x, y) => x[0] - y[0]), out = [];
  a.forEach(r => { const l = out[out.length - 1]; if (l && r[0] <= l[1] + 1 && /^[\s,;:]*$/.test(txt.slice(l[1], r[0]))) l[1] = Math.max(l[1], r[1]); else out.push(r); });
  return out;
}
function hlTextNodes(el){ const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), a = []; let n; while ((n = w.nextNode())) a.push(n); return a; }
function hlOffset(block, node, off){ const r = document.createRange(); r.setStart(block, 0); r.setEnd(node, off); return r.toString().length; }
function hlWrap(block, rs){
  let pos = 0;
  hlTextNodes(block).forEach(node => {
    const len = node.data.length, st = pos, segs = [];
    rs.forEach((r, i) => { const a = Math.max(r[0], st), b = Math.min(r[1], st + len); if (b > a) segs.push([a - st, b - st, i]); });
    pos += len;
    segs.sort((x, y) => y[0] - x[0]).forEach(([a, b, i]) => {
      if (b < node.data.length) node.splitText(b);
      const mid = a > 0 ? node.splitText(a) : node, mk = document.createElement('mark');
      mk.className = 'hq-mk'; mk.dataset.hlr = i; mid.parentNode.insertBefore(mk, mid); mk.appendChild(mid);
    });
  });
}
/* called after every question render */
function hlApply(m, qid){
  const st = m.querySelector('.hq-stem'); if (!st) return;
  st.dataset.hlq = qid; st.classList.toggle('hl-on', hlPen());
  const rec = hlGet(qid); if (!rec) return;
  st.querySelectorAll('[data-hlb]').forEach(b => { const rs = (rec.b || {})[b.dataset.hlb]; if (rs && rs.length) hlWrap(b, rs); });
}
function hlRedraw(){ if (hqSess && !hqSess.done) { const y = window.scrollY; hqDraw(); window.scrollTo({top: y}); } }
function hlAddRange(rng){
  const st = (rng.commonAncestorContainer.nodeType === 1 ? rng.commonAncestorContainer : rng.commonAncestorContainer.parentNode).closest('.hq-stem')
    || (rng.startContainer.parentNode && rng.startContainer.parentNode.closest && rng.startContainer.parentNode.closest('.hq-stem'));
  if (!st || !st.dataset.hlq) return false;
  const qid = st.dataset.hlq, rec = hlGet(qid), blocks = JSON.parse(JSON.stringify((rec && rec.b) || {})); let hit = false;
  st.querySelectorAll('[data-hlb]').forEach(b => {
    if (!rng.intersectsNode(b)) return;
    const txt = b.textContent, br = document.createRange(); br.selectNodeContents(b);
    const s = rng.compareBoundaryPoints(Range.START_TO_START, br) <= 0 ? 0 : hlOffset(b, rng.startContainer, rng.startOffset);
    const e = rng.compareBoundaryPoints(Range.END_TO_END, br) >= 0 ? txt.length : hlOffset(b, rng.endContainer, rng.endOffset);
    let a = s, z = e; while (a < z && /\s/.test(txt[a])) a++; while (z > a && /\s/.test(txt[z - 1])) z--;
    if (z <= a) return;
    blocks[b.dataset.hlb] = hlMerge((blocks[b.dataset.hlb] || []).concat([[a, z]]), txt); hit = true;
  });
  if (hit) { hlPut(qid, blocks); hlRedraw(); }
  return hit;
}
function hlWordAt(x, y){
  let node, off;
  if (document.caretPositionFromPoint) { const p = document.caretPositionFromPoint(x, y); if (p) { node = p.offsetNode; off = p.offset; } }
  else if (document.caretRangeFromPoint) { const r = document.caretRangeFromPoint(x, y); if (r) { node = r.startContainer; off = r.startOffset; } }
  if (!node || node.nodeType !== 3) return null;
  const t = node.data; let a = Math.min(off, t.length), b = a;
  if (a < t.length && /\s/.test(t[a]) && a > 0 && !/\s/.test(t[a - 1])) a = b = a - 1;
  while (a > 0 && !/\s/.test(t[a - 1])) a--; while (b < t.length && !/\s/.test(t[b])) b++;
  while (b > a && /[,.;:?!)]/.test(t[b - 1])) b--; while (a < b && /[(]/.test(t[a])) a++;
  if (b <= a) return null;
  const r = document.createRange(); r.setStart(node, a); r.setEnd(node, b); return r;
}
function hlRemove(mk){
  const b = mk.closest('[data-hlb]'), st = mk.closest('.hq-stem'); if (!b || !st) return;
  const qid = st.dataset.hlq, rec = hlGet(qid); if (!rec) return;
  const blocks = JSON.parse(JSON.stringify(rec.b || {})), rs = blocks[b.dataset.hlb] || []; rs.splice(+mk.dataset.hlr, 1);
  if (rs.length) blocks[b.dataset.hlb] = rs; else delete blocks[b.dataset.hlb];
  hlPut(qid, blocks); hlRedraw();
}
const HLP = {down: null, tap: null};
document.addEventListener('pointerdown', e => {
  HLP.down = null; if (!hlPen() || e.button > 0) return;
  const st = e.target.closest && e.target.closest('.hq-stem'); if (!st || e.target.closest('img,a,button')) return;
  HLP.down = {x: e.clientX, y: e.clientY, t: Date.now(), mk: e.target.closest('mark.hq-mk')};
}, true);
document.addEventListener('pointerup', e => {
  const d = HLP.down; HLP.down = null; if (!d || !hlPen()) return;
  setTimeout(() => {
    const sel = window.getSelection();
    if (sel && sel.rangeCount && !sel.isCollapsed) {
      clearTimeout(HLP.tap); const r = sel.getRangeAt(0).cloneRange();
      if (hlAddRange(r)) { sel.removeAllRanges(); return; }
    }
    const moved = Math.abs(e.clientX - d.x) + Math.abs(e.clientY - d.y);
    if (moved > 10 || Date.now() - d.t > 600) return;
    if (d.mk) { clearTimeout(HLP.tap); return hlRemove(d.mk); }
    const x = e.clientX, y = e.clientY; clearTimeout(HLP.tap);
    HLP.tap = setTimeout(() => { const s2 = window.getSelection(); if (s2 && !s2.isCollapsed) return; const r = hlWordAt(x, y); if (r) hlAddRange(r); }, 230);
  }, 15);
}, true);
function hlClear(){
  if (!hqSess) return; const qid = hqSess.ids[hqSess.i]; if (!hlCount(qid)) return;
  hlPut(qid, {}); hlRedraw(); toast('🧽 Highlights cleared');
}
function hlBtns(qid){
  const n = hlCount(qid);
  return '<button class="btn ghost sm hq-penb' + (hlPen() ? ' on' : '') + '" data-hlpen title="Highlighter (H): select or tap words in the question to turn them yellow. Tap a highlight to remove it." aria-pressed="' + (hlPen() ? 'true' : 'false') + '">🖍️</button>'
    + (n ? '<button class="btn ghost sm" data-hlclr title="Clear this question\'s highlights" aria-label="Clear highlights">🧽 ' + n + '</button>' : '');
}

/* ---------- ☁️ sync: the same Claude account on every device ---------- */
/* One database document holds at most 256 KiB, so progress is split into parts and long parts into chunks.
   Each run, answer record and highlight is merged one by one, so two devices never wipe each other's work. */
const SY_PARTS = ['core', 'hq', 'runs', 'weak', 'u', 'hl'], SY_CH = 90000;
const SY = {busy: false, dirty: false, last: {}, at: 0, err: '', on: false, lastPull: 0};
function syPath(name, i){ return 'data/users/' + UID + '/s271-' + name + (i ? '-' + i : ''); }
function sySplit(st){
  const c = JSON.parse(JSON.stringify(st)), p = {};
  p.hq = c.hq || {}; p.runs = {r: c.hqRuns || [], d: c.hqDel || {}}; p.weak = c.weak || {}; p.u = c.u || {}; p.hl = c.hl || {};
  ['hq', 'hqRuns', 'hqDel', 'hqRun', 'weak', 'u', 'hl'].forEach(k => delete c[k]); p.core = c;
  const out = {}; SY_PARTS.forEach(k => out[k] = JSON.stringify(p[k])); return out;
}
function syJoin(parts){
  if (!parts.core) return null;
  const c = JSON.parse(parts.core);
  c.hq = parts.hq ? JSON.parse(parts.hq) : {}; const r = parts.runs ? JSON.parse(parts.runs) : {r: [], d: {}};
  c.hqRuns = r.r || []; c.hqDel = r.d || {}; c.weak = parts.weak ? JSON.parse(parts.weak) : {}; c.u = parts.u ? JSON.parse(parts.u) : {}; c.hl = parts.hl ? JSON.parse(parts.hl) : {};
  return c;
}
function syMerge(a, b){
  if (!b) return a; if (!a) return b;
  const nb = (b.ts || 0) > (a.ts || 0), base = JSON.parse(JSON.stringify(nb ? b : a)), oth = nb ? a : b;
  const hq = Object.assign({}, oth.hq || {}); Object.entries(base.hq || {}).forEach(([k, r]) => { const o = hq[k]; hq[k] = !o || ((r || [])[1] || 0) >= ((o || [])[1] || 0) ? r : o; }); base.hq = hq;
  const del = Object.assign({}, oth.hqDel || {}); Object.entries(base.hqDel || {}).forEach(([k, t]) => del[k] = Math.max(t || 0, del[k] || 0));
  const cut = Date.now() - 90 * 864e5; Object.keys(del).forEach(k => { if (del[k] < cut) delete del[k]; }); base.hqDel = del;
  const runs = {}; [].concat(oth.hqRuns || [], base.hqRuns || []).forEach(r => { if (!r || !r.rid) return; if (!runs[r.rid] || (r.ts || 0) > (runs[r.rid].ts || 0)) runs[r.rid] = r; });
  base.hqRuns = Object.values(runs).filter(r => !(del[r.rid] && del[r.rid] >= (r.ts || 0))).sort((x, y) => (y.ts || 0) - (x.ts || 0)).slice(0, HQ_KEEP);
  const days = Object.assign({}, oth.days || {}, base.days || {}); Object.keys(oth.days || {}).forEach(k => days[k] = Math.max(days[k] || 0, oth.days[k] || 0)); base.days = days;
  base.xp = Math.max(a.xp || 0, b.xp || 0);
  base.u = Object.assign({}, oth.u || {}, base.u || {});
  const hl = Object.assign({}, oth.hl || {}); Object.entries(base.hl || {}).forEach(([k, v]) => { if (!hl[k] || ((v || {}).ts || 0) >= ((hl[k] || {}).ts || 0)) hl[k] = v; }); base.hl = hl;
  base.ts = Math.max(a.ts || 0, b.ts || 0);
  return base;
}
async function syReadPart(name){
  const s0 = await DB.doc(syPath(name, 0)).get(); if (!s0.exists) return null;
  const d0 = s0.data() || {}; let txt = d0.d || ''; const n = d0.n || 1;
  for (let i = 1; i < n; i++) { const si = await DB.doc(syPath(name, i)).get(); if (!si.exists) return null; txt += (si.data() || {}).d || ''; }
  return txt;
}
async function syWritePart(name, txt){
  const n = Math.max(1, Math.ceil(txt.length / SY_CH)), ts = Date.now();
  for (let i = n - 1; i >= 0; i--) await DB.doc(syPath(name, i)).set({ts, n, i, d: txt.slice(i * SY_CH, (i + 1) * SY_CH)});
}
function syStatus(){
  if (!SY.on) return window.claude ? 'Connecting to sync…' : 'Saved on this device. Use 📲 to move it to another device.';
  if (SY.err) return '⚠️ ' + SY.err;
  return '☁️ Synced ' + (SY.at ? hqAgo(SY.at) : '') + ' · open this page in Claude on any device with the same account and you carry on where you left off.';
}
function syRefresh(){
  setSync(syStatus());
  document.querySelectorAll('.hq-saved').forEach(el => { el.textContent = SY.on && !SY.err ? '☁️ synced' : '💾 saved'; el.title = SY.on && !SY.err ? 'Saved here and synced to your other devices' : 'Saved on this device. Tap 📲 to move it'; });
  const box = document.getElementById('devs'); if (box && !box.hidden) devPaint();
}
async function pushDb(){ return syPush(); }
async function syPush(){
  if (!DB || !UID) return;
  if (SY.busy) { SY.dirty = true; return; }
  SY.busy = true;
  try {
    hqRuns(); const parts = sySplit(S);
    for (const k of SY_PARTS) if (parts[k] !== SY.last[k]) { await syWritePart(k, parts[k]); SY.last[k] = parts[k]; }
    SY.at = Date.now(); SY.err = '';
  } catch (e) {
    const c = e && e.code;
    SY.err = c === 'resource_exhausted' ? 'Sync storage is full. Your progress is still saved on this device.' : c === 'rate_limited' ? 'Sync is busy; it will retry shortly.' : c === 'unavailable' || c === 'revoked' || c === 'not_granted' ? 'Sync is not available in this view. Your progress is saved on this device.' : 'Sync paused (' + (c || 'error') + '). Your progress is saved on this device.';
    if (c === 'rate_limited') setTimeout(syPush, 20000);
  }
  SY.busy = false; syRefresh();
  if (SY.dirty) { SY.dirty = false; syPush(); }
}
let syLocalRunTs = 0;
async function syPull(force){
  if (!DB || !UID) return;
  if (!force && Date.now() - SY.lastPull < 8000) return; SY.lastPull = Date.now();
  try {
    const parts = {}; for (const k of SY_PARTS) parts[k] = await syReadPart(k);
    let R = syJoin(parts);
    if (!R) { const old = await DB.doc('data/users/' + UID + '/ilo').get(); if (old.exists) R = old.data(); }
    else SY_PARTS.forEach(k => { if (parts[k] != null) SY.last[k] = parts[k]; });
    hqRuns();
    const M = R ? syMerge(S, R) : S, changed = JSON.stringify(M) !== JSON.stringify(S);
    if (changed) {
      const sess = hqSess && !hqSess.done && !hqSess.rev ? hqSess : null;
      S = M; S.set = Object.assign({}, DEF_SET, S.set || {}); S.u = S.u || {};
      try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {}
      if (sess) {
        const rec = (S.hqRuns || []).find(r => r.rid === sess.rid);
        if (rec && (rec.ts || 0) > syLocalRunTs && JSON.stringify([rec.pk, rec.x, rec.i]) !== JSON.stringify([sess.pk, sess.x, sess.i])) {
          sess.pk = rec.pk || {}; sess.x = rec.x || {}; sess.i = Math.min(rec.i || 0, sess.ids.length - 1); hqDraw(); toast('☁️ Picked up where your other device left off');
        }
      }
      refreshChrome();
      if (!sess && (route.view === 'home' || route.view === 'hammer') && !(hqSess && !hqSess.done)) render();
    }
    if (JSON.stringify(sySplit(S)) !== JSON.stringify(Object.fromEntries(SY_PARTS.map(k => [k, SY.last[k]])))) await syPush();
    SY.at = Date.now(); if (!SY.err || /busy/.test(SY.err)) SY.err = '';
  } catch (e) { SY.err = 'Could not reach sync just now. Your progress is saved on this device.'; }
  syRefresh();
}
async function syncInit(){
  try {
    if (!window.claude || !window.claude.use) { syRefresh(); return; }
    const [user, db] = await Promise.all([window.claude.use('user'), window.claude.use('db')]);
    if (!user || !db) { syRefresh(); return; }
    const id = await user.id(); if (!id) { syRefresh(); return; }
    DB = db; UID = id; SY.on = true;
    await syPull(true);
    setInterval(() => { if (document.visibilityState === 'visible') syPull(); }, 60000);
  } catch (e) { syRefresh(); }
}
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'hidden') { if (DB && UID) { clearTimeout(dbTimer); syPush(); } }
  else syPull();
});
window.addEventListener('pagehide', () => { if (DB && UID) { clearTimeout(dbTimer); syPush(); } });

/* ---------- 📲 move a save by file or code (works anywhere, including the offline and website copies) ---------- */
const DEV_SKIP = /key|token|secret/i;
function devKeys(){ const a = []; try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (/^(qq-|medengine-)/.test(k) && !DEV_SKIP.test(k)) a.push(k); } } catch (e) {} return a.sort(); }
function devBundle(){
  const ls = {}; devKeys().forEach(k => { try { ls[k] = localStorage.getItem(k); } catch (e) {} });
  hqRuns(); ls[KEY] = JSON.stringify(S);
  return {app: 'medengine-study', fmt: 1, at: Date.now(), ls};
}
function devKb(n){ return n < 1024 ? n + ' B' : n < 1048576 ? Math.round(n / 1024) + ' KB' : (n / 1048576).toFixed(1) + ' MB'; }
function devB64(bytes){ let s = ''; for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000)); return btoa(s); }
function devUnB64(s){ const b = atob(s), u = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) u[i] = b.charCodeAt(i); return u; }
async function devEncode(obj){
  const raw = new TextEncoder().encode(JSON.stringify(obj));
  if (window.CompressionStream) { const z = new Uint8Array(await new Response(new Blob([raw]).stream().pipeThrough(new CompressionStream('gzip'))).arrayBuffer()); return 'MEDSAVE1z:' + devB64(z); }
  return 'MEDSAVE1:' + devB64(raw);
}
async function devDecode(txt){
  txt = (txt || '').trim();
  if (txt[0] === '{') return JSON.parse(txt);
  const m = txt.replace(/\s+/g, '').match(/^MEDSAVE1(z?):(.+)$/); if (!m) throw new Error('That is not a medengine save code.');
  let bytes = devUnB64(m[2]);
  if (m[1]) { if (!window.DecompressionStream) throw new Error('This browser cannot unpack a compressed code. Use the save file instead.'); bytes = new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer()); }
  return JSON.parse(new TextDecoder().decode(bytes));
}
function devMergeStore(cur, inc){
  let a, b; try { a = JSON.parse(cur); b = JSON.parse(inc); } catch (e) { return inc; }
  const idOf = x => x && typeof x === 'object' ? (x.id != null ? 'i' + x.id : 'j' + JSON.stringify(x)) : 'v' + JSON.stringify(x);
  const uni = (x, y) => { const m = new Map(); x.forEach(v => m.set(idOf(v), v)); y.forEach(v => { const k = idOf(v), o = m.get(k); if (!o || ((v && (v.ts || v.at || v.t)) || 0) >= ((o && (o.ts || o.at || o.t)) || 0)) m.set(k, v); }); return Array.from(m.values()); };
  if (Array.isArray(a) && Array.isArray(b)) return JSON.stringify(uni(a, b));
  if (a && b && typeof a === 'object' && typeof b === 'object') {
    const o = Object.assign({}, a, b); Object.keys(o).forEach(k => { if (Array.isArray(a[k]) && Array.isArray(b[k])) o[k] = uni(a[k], b[k]); }); return JSON.stringify(o);
  }
  return inc;
}
async function devImport(bundle){
  if (!bundle || bundle.app !== 'medengine-study' || !bundle.ls) throw new Error('That file is not a medengine-STUDY save.');
  let n = 0;
  for (const [k, v] of Object.entries(bundle.ls)) {
    if (!/^(qq-|medengine-)/.test(k) || DEV_SKIP.test(k) || typeof v !== 'string') continue;
    if (k === KEY) {
      let r; try { r = JSON.parse(v); } catch (e) { continue; }
      hqRuns(); const M = syMerge(S, r); M.ts = Date.now(); S = M; S.set = Object.assign({}, DEF_SET, S.set || {}); S.u = S.u || {};
      localStorage.setItem(KEY, JSON.stringify(S)); n++; continue;
    }
    let cur = null; try { cur = localStorage.getItem(k); } catch (e) {}
    try { localStorage.setItem(k, cur == null ? v : devMergeStore(cur, v)); n++; } catch (e) { toast('Part of the save did not fit in this browser\'s storage'); }
  }
  if (DB && UID) await syPush();
  return n;
}
async function devSaveFile(){
  const txt = JSON.stringify(devBundle()), name = 'medengine-study-save-' + today() + '.json';
  try {
    const dl = window.claude && window.claude.use ? await window.claude.use('downloads') : null;
    if (dl) { await dl.save({filename: name, data: new Blob([txt], {type: 'application/json'})}); toast('💾 Save file ready'); return; }
  } catch (e) { if (e && e.code === 'declined') return; }
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([txt], {type: 'application/json'})); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000);
  toast('💾 Save file downloaded');
}
async function devCopyCode(){
  const code = await devEncode(devBundle()), out = document.getElementById('devCodeOut');
  if (out) { out.hidden = false; out.value = code; }
  document.getElementById('devCodeN').textContent = devKb(code.length);
  try { await navigator.clipboard.writeText(code); toast('📋 Save code copied'); }
  catch (e) { if (out) { out.focus(); out.select(); } toast('Press ⌘C to copy the selected code'); }
}
async function devLoad(txt){
  const msg = document.getElementById('devMsg');
  try {
    const b = await devDecode(txt), n = await devImport(b);
    msg.textContent = '✅ Loaded ' + n + ' part' + (n === 1 ? '' : 's') + ' from a save made ' + new Date(b.at || Date.now()).toLocaleString('en-GB') + '. Reloading…';
    setTimeout(() => location.reload(), 900);
  } catch (e) { msg.textContent = '⚠️ ' + (e && e.message || 'Could not read that save.'); }
}
function devPaint(){
  const box = document.getElementById('devs'); if (!box) return;
  const parts = devKeys().map(k => { let n = 0; try { n = (localStorage.getItem(k) || '').length; } catch (e) {} return [k, n]; });
  const runs = hqRuns().length, ans = Object.keys(S.hq || {}).length, hls = Object.values(S.hl || {}).filter(r => Object.keys(r.b || {}).length).length;
  const names = {'qq-drill-ilo-v1': 'Progress, Hammer runs, highlights and settings', 'medengine-misses-v1': '🔥 My misses', 'medengine-remix-v1': '🔄 Remix cards', 'medengine-shots-v1': '📋 Vault notes', 'medengine-ig-v1': '🖼️ Pictures'};
  box.querySelector('.dv-body').innerHTML =
    '<div class="dv-sec"><h4>☁️ Automatic sync</h4><p class="dv-st">' + esc(syStatus()) + '</p>'
    + (SY.on ? '<div class="toolbar"><button class="btn primary sm" data-devsync>🔄 Sync now</button></div><p class="hint">Works when you open <b>this same STUDY page in Claude</b> (app or browser) while signed in to the same account. Your saved runs, answers, cross-outs, highlights, weak spots and streak follow you. 🔥 My misses and pasted images stay on each device: move those with a save file.</p>'
      : '<p class="hint">This copy is running outside Claude (the offline app or your website), so it cannot sync by itself. Use a save file or a save code below.</p>')
    + '</div><div class="dv-sec"><h4>📤 Send to another device</h4><p class="hint">This device holds ' + ans + ' answered questions, ' + runs + ' saved run' + (runs === 1 ? '' : 's') + ' and highlights on ' + hls + ' question' + (hls === 1 ? '' : 's') + '.</p>'
    + '<div class="toolbar"><button class="btn sm" data-devfile>💾 Save file</button><button class="btn sm" data-devcopy>📋 Copy save code</button><span class="hint" id="devCodeN"></span></div>'
    + '<textarea id="devCodeOut" class="dv-ta" rows="3" readonly hidden aria-label="Your save code"></textarea>'
    + '<p class="hint">Mac to iPhone: 📋 Copy here, then on the phone open STUDY → 📲 → paste into the box below (Universal Clipboard does the move). Or AirDrop or email yourself the save file.</p></div>'
    + '<div class="dv-sec"><h4>📥 Load a save from another device</h4><div class="toolbar"><label class="btn sm dv-file">📂 Choose save file<input type="file" accept=".json,.txt,application/json,text/plain" data-devin hidden></label></div>'
    + '<textarea id="devCodeIn" class="dv-ta" rows="3" placeholder="…or paste a save code here" aria-label="Paste a save code"></textarea><div class="toolbar"><button class="btn primary sm" data-devload>Load code</button></div>'
    + '<p class="hint">Loading <b>merges</b>: nothing on this device is lost. For each run the newer version wins, answer counts keep the higher total, and highlights keep the latest edit.</p><p class="dv-msg" id="devMsg" aria-live="polite"></p></div>'
    + '<details class="dv-sec"><summary class="hint">What is in a save</summary><ul class="dv-list">' + parts.map(([k, n]) => '<li>' + esc(names[k] || k) + ' <span class="hint">' + devKb(n) + '</span></li>').join('') + '</ul><p class="hint">Never included: your API key. Images in the 📋 vault stay on the device that pasted them.</p></details>';
}
function devOpen(){
  let box = document.getElementById('devs');
  if (!box) {
    box = document.createElement('div'); box.className = 'overlay'; box.id = 'devs'; box.hidden = true;
    box.innerHTML = '<div class="modal dv-modal" role="dialog" aria-label="Sync and move your progress"><div style="display:flex;align-items:center;gap:10px;margin-bottom:6px"><h2 class="grow">📲 Your progress on every device</h2><button class="iconbtn" data-devclose aria-label="Close">✕</button></div><div class="dv-body"></div></div>';
    document.body.appendChild(box);
    box.addEventListener('click', e => { if (e.target === box) box.hidden = true; });
    box.addEventListener('change', e => {
      const f = e.target.matches && e.target.matches('[data-devin]') && e.target.files && e.target.files[0]; if (!f) return;
      const r = new FileReader(); r.onload = () => devLoad(String(r.result || '')); r.readAsText(f);
    });
  }
  devPaint(); box.hidden = false; if (SY.on) syPull(true);
}
document.addEventListener('click', e => {
  const t = e.target.closest && e.target.closest('#devBtn,[data-devopen],[data-devclose],[data-devsync],[data-devfile],[data-devcopy],[data-devload],[data-hlpen],[data-hlclr]'); if (!t) return;
  const d = t.dataset; e.preventDefault(); e.stopImmediatePropagation();
  if (t.id === 'devBtn' || d.devopen != null) { const h = document.getElementById('help'); if (h) h.hidden = true; return devOpen(); }
  if (d.devclose != null) { document.getElementById('devs').hidden = true; return; }
  if (d.devsync != null) { syPull(true).then(() => toast('☁️ Synced')); return; }
  if (d.devfile != null) return devSaveFile();
  if (d.devcopy != null) return devCopyCode();
  if (d.devload != null) return devLoad((document.getElementById('devCodeIn') || {}).value || '');
  if (d.hlpen != null) return hlPenToggle();
  if (d.hlclr != null) return hlClear();
}, true);
document.addEventListener('keydown', e => { if (e.key === 'Escape') { const b = document.getElementById('devs'); if (b && !b.hidden) { b.hidden = true; e.stopImmediatePropagation(); } } }, true);
/* read-only handle for the automated tests */
window.__mev = {get S(){ return S; }, get hqSess(){ return hqSess; }, get SY(){ return SY; }, hlCount, syPush, syPull, devBundle, save: () => save()};
