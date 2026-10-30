/* ===================== v2.7.3 · ⚡ thought maps, 🎯 cue check against your highlights, 🔥 misses sync ===================== */

/* ---------- ⚡ thought map: 🎯 cues ➔ ⚙️ mechanism ➔ ⚖️ gate ➔ ✅ answer, with 🔀 one-feature flips ---------- */
function tmHtml(it){
  const tm = it.tm; if (!tm) return '';
  const L = 'ABCDE', node = (c, k, v) => '<div class="tm-n ' + c + '"><span class="tm-k">' + k + '</span><span class="tm-v">' + v + '</span></div>', ar = '<span class="tm-a" aria-hidden="true"></span>';
  return '<div class="tm" role="group" aria-label="Thought map"><div class="tm-h">⚡ Thought map</div><div class="tm-row">'
    + node('tm-c', '🎯 Cues', tm.c.map(c => '<span class="tm-cue">' + esc(c) + '</span>').join(''))
    + ar + node('tm-m', '⚙️ Mechanism', esc(tm.m))
    + ar + node('tm-g', '⚖️ Decisive gate', esc(tm.g))
    + ar + node('tm-w', '✅ Answer', '<b>' + L[it.a] + '.</b> ' + esc(it.o[it.a]))
    + '</div><div class="tm-fl"><span class="tm-fk">From the gate: change one thing and…</span>'
    + tm.f.map(([c, i]) => '<div class="tm-f"><span class="tm-fa" aria-hidden="true">↳ 🔀</span><span>If ' + esc(c) + ' <span class="tm-fx">➔</span> <b>' + L[i] + '. ' + esc(it.o[i]) + '</b></span></div>').join('')
    + '</div><div class="tm-score" data-tmscore></div></div>';
}
function tmRe(c){ return new RegExp(c.trim().replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/\s+/g, '\\s+'), 'i'); }
function tmWrap(block, rs, cls){
  let pos = 0;
  hlTextNodes(block).forEach(node => {
    const len = node.data.length, st = pos, segs = [];
    rs.forEach(r => { const a = Math.max(r[0], st), b = Math.min(r[1], st + len); if (b > a) segs.push([a - st, b - st]); });
    pos += len;
    segs.sort((x, y) => y[0] - x[0]).forEach(([a, b]) => {
      if (b < node.data.length) node.splitText(b);
      const mid = a > 0 ? node.splitText(a) : node, sp = document.createElement('span');
      sp.className = cls; mid.parentNode.insertBefore(sp, mid); sp.appendChild(mid);
    });
  });
}
/* after an answer: underline the deciding cues in green and score your highlights against them */
function tmCues(m, it){
  const tm = it.tm, st = m.querySelector('.hq-stem'); if (!tm || !st) return;
  const rec = hlGet(it.id), hb = (rec && rec.b) || {}, blocks = Array.from(st.querySelectorAll('[data-hlb]')), per = {}, cues = [];
  tm.c.forEach(c => {
    const re = tmRe(c), n = c.replace(/\s+/g, ' ').trim().toLowerCase();
    for (const b of blocks) {
      if (b.dataset.hlb === 'lab') {
        for (const tr of b.querySelectorAll('tr')) {
          const td = tr.querySelectorAll('td'); if (td.length < 2) continue;
          if ((td[0].textContent + ' ' + td[1].textContent).replace(/\s+/g, ' ').toLowerCase().includes(n)) {
            tr.classList.add('hq-cuerow'); const s = hlOffset(b, tr, 0); cues.push({b: 'lab', s, e: s + tr.textContent.length}); return;
          }
        }
        continue;
      }
      const mt = re.exec(b.textContent); if (!mt) continue;
      const r = [mt.index, mt.index + mt[0].length]; (per[b.dataset.hlb] = per[b.dataset.hlb] || []).push(r); cues.push({b: b.dataset.hlb, s: r[0], e: r[1]}); return;
    }
  });
  blocks.forEach(b => { if (per[b.dataset.hlb]) tmWrap(b, per[b.dataset.hlb], 'hq-cue'); });
  const box = m.querySelector('[data-tmscore]'); if (!box) return;
  const hls = []; Object.entries(hb).forEach(([k, rs]) => rs.forEach(r => hls.push({b: k, s: r[0], e: r[1]})));
  const ov = (x, y) => x.b === y.b && x.s < y.e && y.s < x.e;
  const hit = cues.filter(c => hls.some(h => ov(c, h))).length, off = hls.filter(h => !cues.some(c => ov(c, h))).length;
  if (!hls.length) { box.innerHTML = '<span class="tm-sc">🖍️ Next time, highlight the clue before you pick. The <span class="tm-u">green underlines</span> are the cues that decide this one.</span>'; return; }
  const all = hit === cues.length && cues.length;
  box.innerHTML = '<span class="tm-sc ' + (all ? 'ok' : hit ? 'part' : 'miss') + '">' + (all ? '🎯 ' : hit ? '👀 ' : '⚠️ ') + 'Your highlights caught <b>' + hit + ' of ' + cues.length + '</b> deciding cue' + (cues.length === 1 ? '' : 's') + (off ? ' · ' + off + ' on something else' : '') + '.</span>' + (!all ? ' <span class="hint">The <span class="tm-u">green underlines</span> show what you missed.</span>' : '');
}

/* ---------- 🖍️ on a touchscreen: a floating switch, so one thumb can turn the pen on and off ---------- */
function hlPill(m){
  const old = document.getElementById('hlPill'); if (old) old.remove();
  if (!(window.matchMedia && matchMedia('(pointer: coarse)').matches) || !hqSess || hqSess.done) return;
  const b = document.createElement('button'); b.id = 'hlPill'; b.className = 'hq-penpill' + (hlPen() ? ' on' : ''); b.dataset.hlpen = '';
  b.setAttribute('aria-pressed', hlPen() ? 'true' : 'false'); b.textContent = '🖍️ Highlight: ' + (hlPen() ? 'ON' : 'OFF');
  document.body.appendChild(b);
}
window.addEventListener('hashchange', () => { if (!hqSess || hqSess.done) { const p = document.getElementById('hlPill'); if (p) p.remove(); } });
document.addEventListener('keydown', e => { if (e.key === 'Escape') setTimeout(() => { if (!hqSess) { const p = document.getElementById('hlPill'); if (p) p.remove(); } }, 0); });

/* ---------- 🔥 My misses: synced, merged item by item ---------- */
function msMerge(a, b){
  if (!b || !Array.isArray(b.items)) return a; if (!a || !Array.isArray(a.items)) return b;
  const rank = x => [(x.seen || 0), x.fixed ? 1 : 0, (x.box || 0), (x.due || '')];
  const better = (x, y) => { const p = rank(x), q = rank(y); for (let i = 0; i < p.length; i++) { if (p[i] > q[i]) return true; if (p[i] < q[i]) return false; } return false; };
  const byId = new Map(); a.items.forEach(x => byId.set(String(x.id), x));
  b.items.forEach(y => { const k = String(y.id), x = byId.get(k); if (!x || better(y, x)) byId.set(k, y); });
  const order = a.items.map(x => String(x.id)); b.items.forEach(y => { if (!order.includes(String(y.id))) order.push(String(y.id)); });
  return Object.assign({}, b, a, {items: order.map(k => byId.get(k)), imported: Math.max(a.imported || 0, b.imported || 0)});
}
function msSave(){
  try { localStorage.setItem(MS_LS, JSON.stringify(msData)); } catch (e) { toast('Could not save: browser storage is full or blocked'); }
  if (DB && UID) { clearTimeout(dbTimer); dbTimer = setTimeout(pushDb, 3500); }
}
Object.assign(window.__mev, {tmHtml, msMerge, hqItem, hqAll, run: ids => hqNewRun(ids.map(hqItem), 'test')});
Object.defineProperty(window.__mev, 'msData', {get(){ return msLoad(); }});
