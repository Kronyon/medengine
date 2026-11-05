/* ---------- v1.2: ⚡ First move vs cure, and 🔥 My misses ---------- */
const ACTS = D.act || [];
const arrowsOn = h => { const k = h.indexOf('<div class="wa">'); return k < 0 ? h : h.slice(0, k) + h.slice(k).replace(/→/g, '<span class="pa-ar">→</span>'); };
function actHtml(i, lib){
  const r = ACTS[i]; if (!r) return '';
  return arrowsOn('<details class="whyc pa act" data-paf="' + esc((r.t + ' ' + r.l.join(' ')).replace(/\*\*/g, '').toLowerCase()) + '"><summary>⚡ ' + esc(r.t) + '</summary><div class="wa">' + r.l.map(l => '<div class="wl">' + fmtRich(l) + '</div>').join('') + (lib ? ulinks(r.u) : '') + '</div></details>');
}
function actPanelHtml(u){
  const xs = u.acts || []; if (!xs.length) return '';
  return '<div class="panel pap act-p"><div class="toolbar"><b class="grow">⚡ First move vs cure</b><button class="btn ghost sm" data-go="act">All ' + ACTS.length + ' cards</button></div>' + xs.map(i => actHtml(i)).join('') + '</div>';
}
function viewAct(m){ viewLib(m, 'act'); }

/* the matching action card also goes into the Remix prompt, so next-step answers follow UK guidance */
function rmxActPick(q, unit){
  const us = [unit].concat(q.opts.map(o => rmxUnitFor(o))).filter(u => u != null && u >= 0);
  const keys = q.opts.map(o => rmxNorm(o).split(' ').filter(w => w.length >= 5 && !RMX_GEN.test(w)));
  let best = -1, bs = -1;
  ACTS.forEach((r, i) => {
    const hitU = us.findIndex(u => (r.u || []).includes(u));
    const txt = ' ' + rmxNorm(r.t + ' ' + r.l.join(' ')) + ' ', hits = keys.filter(k => k.length && k.some(w => txt.includes(' ' + w))).length;
    if (hitU < 0 && hits < 2) return; // not this condition: only a card that names at least two of the options
    const sc = hits * 10 + (hitU === 0 ? 6 : hitU > 0 ? 3 : 0); if (sc > bs) { bs = sc; best = i; }
  });
  return best;
}
{ const rn = rmxRootNote; rmxRootNote = function(q){ const i = rmxActPick(q, rmxCondUnit(q.cond)); const a = i < 0 ? '' : ('\n\nCHECKED NEXT-STEP NOTES, UK guidance (use for first move vs definitive, stable vs unstable):\n' + ACTS[i].t + '\n- ' + ACTS[i].l.join('\n- ')).replace(/\*\*/g, '').slice(0, 1000); return rn(q) + a; }; }

/* ----- 🔥 My misses: your old pick vs the right answer, cued by the learning point, spaced until fixed ----- */
const MS_LS = 'medengine-misses-v1', MS_GAP = [1, 3, 7];
let msData = null, msCur = null, msPick = null, msMore = false;
function msLoad(){ if (msData) return msData; try { msData = JSON.parse(localStorage.getItem(MS_LS) || 'null'); } catch (e) { msData = null; } if (!msData || !Array.isArray(msData.items)) msData = {items: []}; return msData; }
function msSave(){ try { localStorage.setItem(MS_LS, JSON.stringify(msData)); } catch (e) { toast('Could not save: browser storage is full or blocked'); } }
const msQn = x => parseInt(String(x.id).replace(/\D/g, ''), 10) || 0;
function msQueue(all){
  const t = rmxDay(); let xs = msLoad().items.filter(x => !x.fixed);
  if (!all) xs = xs.filter(x => !x.due || x.due <= t);
  return xs.sort((a, b) => (a.rec === b.rec ? 0 : a.rec ? 1 : -1) || (a.due || '') .localeCompare(b.due || '') || msQn(a) - msQn(b));
}
const MS_STOP = /^(with|from|that|this|then|than|into|over|under|after|before|first|line|start|give|refer|urgent|acute|chronic|oral|treatment|management|disease|syndrome|patient|use|used|test|risk)$/i;
function msMask(lp, correct){
  let s = String(lp || '');
  const phrase = String(correct || '').trim(); if (phrase.length >= 3) s = s.split(new RegExp(phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')).join('▒▒▒');
  (phrase.match(/[A-Za-z][A-Za-z'-]{3,}/g) || []).filter(w => !MS_STOP.test(w)).forEach(w => { s = s.replace(new RegExp('\\b' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi'), '▒▒▒'); });
  return s.replace(/(▒▒▒[\s,]*){2,}/g, '▒▒▒ ');
}
const msHash = s => [...String(s)].reduce((h, c) => (h * 31 + c.charCodeAt(0)) >>> 0, 7);
function msImport(text){
  let j; try { j = JSON.parse(text); } catch (e) { return toast('That file is not a medengine misses file'); }
  const raw = Array.isArray(j) ? j : j && Array.isArray(j.items) ? j.items : null;
  if (!raw) return toast('That file is not a medengine misses file');
  const old = {}; msLoad().items.forEach(x => { old[x.id] = x; });
  const items = raw.filter(x => x && x.id && x.correct && x.mine).map(x => Object.assign({box: 0, due: '', fixed: false, seen: 0}, old[x.id] || {}, {id: String(x.id), spec: String(x.spec || ''), tags: String(x.tags || ''), correct: String(x.correct), mine: String(x.mine), lp: String(x.lp || ''), rec: !!x.rec}));
  msData = {items, imported: Date.now()}; msSave(); msCur = null; msPick = null;
  toast('🔥 ' + items.length + ' misses loaded'); render();
}
function msUnit(x){ const tags = x.tags.replace(/^EMQ: /, '').split(/(?<=[a-z)])\s(?=[A-Z])/); for (const t of tags) { const u = rmxUnitFor(t); if (u >= 0) return u; } return rmxUnitFor(x.correct); }
function viewMisses(m){
  const d = msLoad(), all = d.items, fixed = all.filter(x => x.fixed).length, left = all.length - fixed, unrec = all.filter(x => !x.fixed && !x.rec).length;
  let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🔥 My misses</span><span class="grow"></span><span class="mono">' + (all.length ? left + ' left · ' + fixed + ' fixed' : '') + '</span></div><h1>My misses</h1><p class="hint" style="margin:0">Your old pick against the right answer, cued by the rule. Answer with <span class="kbd">1</span> or <span class="kbd">2</span>, <span class="kbd">Enter</span> for next. Right on two separate days and it is fixed.</p></div><div id="ms" class="panel">';
  if (!all.length) {
    h += '<p style="margin:0 0 8px">No misses loaded yet. Import the <b>medengine misses file</b> made from your SBA Bank history: it stays on this device only.</p><div class="toolbar"><label class="btn primary">📥 Import my misses file<input type="file" accept=".json,application/json" data-msfile hidden></label></div>';
  } else {
    if (!msCur || msCur.fixed || (msPick == null && !msQueue(msMore).includes(msCur))) { msCur = msQueue(msMore)[0] || null; msPick = null; }
    h += '<div class="chips ms-stat"><span class="chip on">🔥 ' + unrec + ' never re-done</span><span class="chip">🔁 ' + (left - unrec) + ' to re-check</span><span class="chip">✅ ' + fixed + ' fixed</span></div>';
    if (!msCur) h += '<div class="snp-end"><p><b>All done for today.</b> Next ones come back on schedule.</p><div class="toolbar"><button class="btn primary" data-msmore>Keep going anyway</button></div></div>';
    else {
      const x = msCur, flip = msHash(x.id) % 2, opts = flip ? [x.mine, x.correct] : [x.correct, x.mine], ans = flip ? 1 : 0, cue = msMask(x.lp, x.correct), ui = msUnit(x);
      h += '<div class="qmeta"><span class="code">' + esc(x.id) + '</span><span class="code">' + esc(x.spec) + '</span>' + (x.rec ? '' : '<span class="code">🔥 never re-done</span>') + '</div><div class="ms-tag">' + esc(x.tags) + '</div><div class="stem snp-clue ms-cue">' + esc(cue || x.tags) + '</div>';
      h += '<div class="opts">' + opts.map((o, k) => { let cl = 'opt'; if (msPick != null) { if (k === ans) cl += ' right'; else if (k === msPick) cl += ' wrong'; } return '<button class="' + cl + '" data-msa="' + k + '"' + (msPick != null ? ' disabled' : '') + '><span class="k">' + (k + 1) + '</span><span>' + esc(o) + '</span></button>'; }).join('') + '</div>';
      if (msPick != null) {
        const u = ui >= 0 ? UNITS[ui] : null, links = u ? '<div class="chips"><button class="chip" data-u="' + ui + '" data-mode="think">🧬 ⚡ ' + esc(u.name) + '</button></div>' : '';
        h += '<div class="kl ' + (msPick === ans ? 'kl-in' : 'kl-out') + '"><span class="ki">' + (msPick === ans ? '✅' : '❌') + '</span><span>' + esc(x.lp) + '</span></div>' + links + '<div class="toolbar"><button class="btn primary" data-msnext>Next <span class="kbd">Enter</span></button></div>';
      }
    }
    h += '<div class="toolbar ms-tools"><label class="btn ghost">📥 Import again<input type="file" accept=".json,application/json" data-msfile hidden></label><button class="btn ghost" data-msclear>🗑 Clear</button></div>';
  }
  m.innerHTML = h + '</div></div>';
  const f = $('[data-msfile]', m); if (f) f.addEventListener('change', () => { const file = f.files && f.files[0]; if (!file) return; file.text().then(msImport); });
}
function msAnswer(k){
  const x = msCur; if (!x || msPick != null) return;
  const flip = msHash(x.id) % 2, ans = flip ? 1 : 0, t = rmxDay(); msPick = k; x.seen = (x.seen || 0) + 1;
  if (k === ans) { if (x.last !== t) x.box = (x.box || 0) + 1; x.fixed = x.box >= 2; x.due = rmxAddDays(t, MS_GAP[Math.min(x.box, MS_GAP.length - 1)]); addXp(3); }
  else { x.box = 0; x.fixed = false; x.due = rmxAddDays(t, 1); }
  x.last = t; msSave(); render();
}
function msNext(){ msCur = null; msPick = null; render(); }
function extClick12(t, d){
  if (d.msa != null) { msAnswer(+d.msa); return true; }
  if (d.msnext != null) { msNext(); return true; }
  if (d.msmore != null) { msMore = true; msCur = null; render(); return true; }
  if (d.msclear != null) { if (confirm('Clear all imported misses and progress from this device?')) { msData = {items: []}; msSave(); msCur = null; render(); } return true; }
  return false;
}
document.addEventListener('keydown', e => {
  if (route.view !== 'misses' || e.metaKey || e.ctrlKey || e.altKey || /^(INPUT|TEXTAREA|SELECT)$/.test((e.target && e.target.tagName) || '')) return;
  if ((e.key === '1' || e.key === '2') && msCur && msPick == null) { e.preventDefault(); e.stopPropagation(); msAnswer(+e.key - 1); }
  else if (e.key === 'Enter' && msPick != null) { e.preventDefault(); e.stopPropagation(); msNext(); }
}, true);
try { Object.defineProperty(window, '__me12', {value: Object.freeze({msMask, msImport, msLoad: () => msLoad(), get cur(){ return msCur; }, rootNote: q => rmxRootNote(q)})}); } catch (e) {}
