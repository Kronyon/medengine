/* ---------- v2.1: 🧲 Triggers: every condition, bug, drug, test and procedure as High-Yield-style lines (engine: trg.js) ---------- */
/* word-hunt stacks: lines that share a scene sit together under its label (D.hst, from snap/hl_*.py) */
const HST = D.hst || {};
function stackOrder(ids, ui){
  const st = HST[ui], left = new Set(ids), out = [];
  (st || []).forEach(([lab, hs]) => hs.forEach(i => { if (left.has(i)) { out.push([i, lab]); left.delete(i); } }));
  ids.forEach(i => { if (left.has(i)) out.push([i, '']); });
  return out;
}
function huntStacks(ids, ui){
  let h = '', last = null;
  stackOrder(ids, ui).forEach(([i, lab]) => { if (lab !== last) { if (lab) h += '<div class="hw-st">' + esc(lab) + '</div>'; last = lab; } h += huntHtml([i]); });
  return h;
}
function hwStHide(box){
  if (!box) return;
  $$('.hw-st', box).forEach(st => { let n = st.nextElementSibling, any = false; while (n && !n.classList.contains('hw-st')) { if (n.classList.contains('hw') && !n.hidden) { any = true; break; } n = n.nextElementSibling; } st.hidden = !any; });
}
function trgU(){
  if (trgU.c) return trgU.c;
  return trgU.c = {weeks: WEEKS.map(w => [w.id, w.name]), units: UNITS.map(u => ({i: u.i, name: u.name, w: u.w, o: (SNAPS[u.i] || {}).o, h: stackOrder((u.hunt || []).filter(i => huntUnit[i] === u.i && HUNT[i]), u.i).map(([i, lab]) => HUNT[i].slice(0, 3).concat(lab ? [lab] : []))}))};
}
function trgCount(){ return window.TG && D.trg ? TG.count(D.trg, trgU()) : null; }
function viewTriggers(m){
  if (!window.TG || !D.trg) { m.innerHTML = '<div class="wrap"><div class="panel empty">Triggers did not load.</div></div>'; return; }
  m.innerHTML = '<div class="wrap trg-wrap">' + TG.page(D.trg, trgU(), {unitAttr: i => 'data-u="' + i + '" data-mode="read"'}) + '</div>';
  TG.mount();
}
/* the ⭐ trigger on each condition's word-hunt panel */
function trStar(u){
  const s = ((D.trg || {}).c || {})[u.i];
  return s ? '<div class="tr-star">⭐ ' + fmtRich0(s[0]) + ' <span class="tr-arr">→</span> <b>' + fmtRich0(s[1]) + '</b></div>' : '';
}
/* search: how many trigger lines match */
function trgTexts(){
  if (trgTexts.c) return trgTexts.c;
  const T = D.trg || {}, out = [];
  Object.values(T.c || {}).forEach(x => out.push(x.join(' ')));
  (T.sc || []).forEach(s => s[2].forEach(l => out.push(l[1] + ' ' + l[2] + ' ' + ((T.bug || {})[l[0]] || []).slice(0, 2).join(' '))));
  ['dr', 'ix', 'mx'].forEach(k => (T[k] || []).forEach(g => g[2].forEach(d => { out.push(d[0] + ' ' + d[2]); d[3].forEach(c => out.push(d[0] + ' ' + c.join(' '))); })));
  HUNT.forEach(x => out.push(x[1] + ' ' + x[2]));
  return trgTexts.c = out.map(s => s.replace(/\*\*/g, '').toLowerCase());
}
function trgSearchHtml(q, has){
  const n = trgTexts().filter(has).length;
  return n ? '<h6>🧲 Triggers</h6><button class="sr" data-trgo="' + esc(q) + '"><span class="where">🧲 ' + n + ' line' + (n > 1 ? 's' : '') + '</span>Open every trigger that mentions “' + esc(q) + '”</button>' : '';
}
document.addEventListener('click', e => {
  const b = e.target.closest && e.target.closest('[data-trjump],[data-trgo]'); if (!b || !window.TG) return;
  e.preventDefault(); e.stopImmediatePropagation();
  const sp = document.getElementById('sp'); if (sp) sp.hidden = true;
  if (b.dataset.trjump != null) { TG.jump = 'tg-u' + b.dataset.trjump; TG.preset = ''; }
  else { TG.preset = b.dataset.trgo; const q = document.getElementById('q'); if (q) q.blur(); }
  if (route.view === 'triggers') { viewTriggers($('#main')); } else go({view: 'triggers'});
}, true);
