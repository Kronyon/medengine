/* ---------- v0.8–0.9: 🔄 Remix (missed question → one-change variations), speed tags ---------- */
const SPD = D.spdl || {};
const spdBadge = u => u.spd && SPD[u.spd] ? '<span class="spd" title="' + esc(SPD[u.spd][1] + ': ' + SPD[u.spd][2]) + '">' + SPD[u.spd][0] + ' ' + esc(SPD[u.spd][1]) + '</span>' : '';
function spdChipsHtml(){
  return '<div class="chips spdrow"><span class="hint">⏱ Speed</span>' + Object.keys(SPD).map(k => { const n = UNITS.filter(u => u.spd === k).length; return '<button class="chip' + (S.set.spd === k ? ' on' : '') + '" data-spdset="' + k + '" title="' + esc(SPD[k][2]) + '">' + SPD[k][0] + ' ' + esc(SPD[k][1]) + ' · ' + n + '</button>'; }).join('') + '</div>';
}

/* ----- AI: the claude.ai runtime in the artifact; the user's own key in the downloaded/website build ----- */
let RMX_AI = null, RMX_IMG = false;
(async () => {
  try { if (window.claude && claude.use) RMX_AI = await claude.use('sample'); } catch (e) { RMX_AI = null; }
  try { const lim = RMX_AI && RMX_AI.limits ? await RMX_AI.limits() : null; RMX_IMG = !!(lim && lim.images); } catch (e) { RMX_IMG = false; }
  if (route.view === 'remix') { if (rmx.step === 'check') drawRemix(); else { const st = $('#rmxStat'); if (st) st.innerHTML = rmxStatusHtml(); } }
})();
const rmxTier = () => S.set.rmxTier === 'default' ? 'default' : 'quick';

/* ----- days and the review schedule (tomorrow → 3 days → a week → 3 weeks → 2 months) ----- */
const rmxDay = t => { const d = t ? new Date(t) : new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); };
const rmxAddDays = (day, n) => { const [y, m, d] = day.split('-').map(Number); return rmxDay(new Date(y, m - 1, d + n).getTime()); };
const RMX_GAP = [1, 3, 7, 21, 60];
const rmxIsDue = c => (c.due || '0000-00-00') <= rmxDay();
function rmxDueLabel(day){ const [y, m, d] = day.split('-').map(Number), t = new Date(), n = Math.round((new Date(y, m - 1, d) - new Date(t.getFullYear(), t.getMonth(), t.getDate())) / 864e5); return n <= 0 ? 'today' : n === 1 ? 'tomorrow' : 'in ' + n + ' days'; }

/* ----- storage (this browser only; images go to the same on-device store as the Screenshot vault) ----- */
const RMX_LS = 'medengine-remix-v1', RMX_MAX = 100;
let rmxCards = null;
function rmxAll(){
  if (rmxCards) return rmxCards;
  try { rmxCards = JSON.parse(localStorage.getItem(RMX_LS) || '[]'); } catch (e) { rmxCards = []; }
  if (!Array.isArray(rmxCards)) rmxCards = [];
  rmxCards.forEach(c => { if (!c.due) { c.due = rmxAddDays(rmxDay(c.ts), 1); c.box = 0; } if (!c.seen) c.seen = []; if (!c.res) c.res = []; }); // cards saved by v0.8
  return rmxCards;
}
function rmxSave(){ try { localStorage.setItem(RMX_LS, JSON.stringify(rmxAll().slice(0, RMX_MAX))); return true; } catch (e) { toast('Could not save: browser storage is full or blocked'); return false; } }
const rmxImgMem = {};
async function rmxImgPut(id, img){
  rmxImgMem[id] = img;
  const db = await shotIdb(); if (!db) return;
  try { await new Promise((res, rej) => { const tx = db.transaction('shots', 'readwrite'); tx.objectStore('shots').put({id: 'ri-' + id, rmx: 1, img: img.d, w: img.w, h: img.h, ts: Date.now()}); tx.oncomplete = res; tx.onerror = () => rej(tx.error); }); } catch (e) {}
}
async function rmxImgGet(id){
  if (rmxImgMem[id]) return rmxImgMem[id];
  const db = await shotIdb(); if (!db) return null;
  try { const r = await new Promise((res, rej) => { const q = db.transaction('shots').objectStore('shots').get('ri-' + id); q.onsuccess = () => res(q.result); q.onerror = () => rej(q.error); }); if (r) return (rmxImgMem[id] = {d: r.img, w: r.w, h: r.h}); } catch (e) {}
  return null;
}
async function rmxImgDel(id){ delete rmxImgMem[id]; const db = await shotIdb(); if (!db) return; try { db.transaction('shots', 'readwrite').objectStore('shots').delete('ri-' + id); } catch (e) {} }
function rmxBlob(d){ const m = /^data:([^;,]+)(;base64)?,(.*)$/.exec(d || ''); if (!m) return null; const bin = m[2] ? atob(m[3]) : decodeURIComponent(m[3]), u = new Uint8Array(bin.length); for (let i = 0; i < bin.length; i++) u[i] = bin.charCodeAt(i); return new Blob([u], {type: m[1]}); }

/* ----- paste → question: strip the SBA Bank page around it ----- */
const RMX_JUNK = /^(passmedicine|medical student finals.*|home|questions|question bank|previous sessions|mock exams|review questions|performance|comment threads|textbooks?|high-yield textbook|extended textbook|knowledge tutor|review facts|custom revision|revision sets|concepts|all concepts|top 100 concepts|ukmla content map.*|reference ranges|end and review|deep dive|next question|previous question|next|previous|submit( answer)?|skip|flag( question)?|rate this question.*|report( an)? (error|issue)|report broken (link|media)|suggest (better categorisation|link)|key concept image|important for me.*|less important|very important|feedback|show (explanation|answer)|hide|menu|log ?out|sign ?out|my account|settings|help|contact us|privacy.*|terms.*|cookie.*|©.*|copyright.*|all contents of this site.*|back to top|score:?\s*\d+(\.\d+)?%?|\d+\s*\/\s*\d+|\d+(-\d+)?( \d+ ?\/ ?\d+)?|time( remaining)?:?.*|\d{1,3}(\.\d)?%|average score.*|\d+ (people|users) .*)$/i;
const RMX_END = /^(comments?|discussion|add a comment|post( a)? comment|\d+ comments?|show comments|view comments)$/i;
const RMX_QMARK = /^question [\d,]+ of [\d,]+$/i;
const RMX_LABEL = /^(presentation|condition|aocp ?\/ ?aopk|links|media|textbooks?|suggest better categorisation)$/i;
const LINKY = /youtube|video|zero to finals|brandl|osmosis|geeky medics|medicosis|ninja nerd|\bwatch\b|\d+ \d+$/i;
function rmxParse(raw){
  let L = String(raw || '').replace(/\r/g, '').split('\n').map(s => s.replace(/\s+/g, ' ').trim()).filter(Boolean);
  // Passmed's key-concept box sits right above "Important for me / Less important"
  for (let i = 1; i < L.length; i++) if (/^important for me/i.test(L[i]) && L[i - 1].length > 15 && !RMX_JUNK.test(L[i - 1])) L[i - 1] = '§K§' + L[i - 1];
  L = L.map(l => RMX_QMARK.test(l) ? '§Q§' : l).filter(l => l === '§Q§' || l.startsWith('§K§') || !RMX_JUNK.test(l));
  const end = L.findIndex((l, i) => i > 3 && RMX_END.test(l)); if (end > 0) L = L.slice(0, end);
  // its UKMLA Content Map tag names the condition: the most reliable link to an ILO condition
  const cond = [], ci = L.findIndex(l => /^condition$/i.test(l));
  if (ci >= 0) for (let j = ci + 1; j < L.length && j <= ci + 3 && !RMX_LABEL.test(L[j]); j++) L[j].replace(/([a-z)])([A-Z][a-z])/g, '$1|$2').split('|').forEach(x => { x = x.trim(); if (x.length >= 3 && x.length <= 70) cond.push(x); });
  const optLine = l => l.replace(/^\(?([A-Ea-e1-5])[).:]\s+/, '').replace(/\s+\d{1,3}(\.\d)?%$/, '').replace(/\s*[✓✔✗✘×]\s*$/, '').trim();
  const isOpt = l => { if (l.charAt(0) === '§') return false; const o = optLine(l); return o.length >= 1 && o.length <= 110 && !/[?]$/.test(o) && !/\.\s+[A-Z]/.test(o.slice(0, -1)); };
  // the case runs back from the question line: to "Question N of M" if Passmed's marker is there,
  // otherwise over sentences, lab rows (digits) and lines ending in . or : (up to 10 lines)
  const caseStart = i => { let a = i; while (a > 0 && L[a - 1] !== '§Q§' && !L[a - 1].startsWith('§K§') && i - a < 10 && (L[a - 1].length > 40 || /[.:]$/.test(L[a - 1]) || /\d/.test(L[a - 1]))) a--; return a; };
  // every "question line + 4-5 short lines" block is a candidate; the real one sits under the case,
  // later ones (related videos, "How does X work?" links) have no case above them
  const cands = [];
  for (let i = 0; i < L.length; i++) {
    if (!/\?$/.test(L[i]) && !/^(which|what|how|the most|select)\b.*[:?]?$/i.test(L[i])) continue;
    let n = 0; while (i + 1 + n < L.length && n < 5 && isOpt(L[i + 1 + n])) n++;
    if (n < 4) continue;
    const a = caseStart(i), caseLen = L.slice(a, i + 1).join(' ').length, links = L.slice(i + 1, i + 1 + n).filter(l => LINKY.test(l)).length;
    cands.push({qi: i, a, on: n, score: (caseLen >= 100 ? 1000 : 0) + Math.min(caseLen, 999) + (a > 0 && L[a - 1] === '§Q§' ? 500 : 0) - links * 600 - (n === 5 ? 0 : 50)});
  }
  if (!cands.length) { // no question line: the first run of 5 short lines after a long line
    for (let i = 1; i < L.length - 4; i++) if (L[i - 1].length > 120 && [0, 1, 2, 3, 4].every(k => isOpt(L[i + k]))) { cands.push({qi: i - 1, a: caseStart(i - 1), on: 5, score: 0}); break; }
  }
  if (!cands.length) return {stem: L.filter(l => l.charAt(0) !== '§').join(' ').slice(0, 1500), opts: [], correct: -1, picked: -1, expl: '', concept: '', cond, optx: [], early: false, ok: false};
  const best = cands.reduce((x, y) => y.score > x.score ? y : x), qi = best.qi, oi = qi + 1, on = best.on;
  const stem = L.slice(best.a, qi + 1).filter(l => l !== '§Q§').join(' ');
  const rawOpts = L.slice(oi, oi + on);
  let opts = rawOpts.map(optLine);
  // after you answer, Passmed glues the percentages onto each option ("…GIP50%"): strip them when every option has one
  const pct = opts.every(o => /\d{1,3}(\.\d)?%$/.test(o));
  if (pct) opts = opts.map(o => o.replace(/\s*\d{1,3}(\.\d)?%$/, '').trim());
  const afterRaw = L.slice(oi + on).filter(l => l !== '§Q§');
  const concept = ((afterRaw.find(l => l.startsWith('§K§')) || '').slice(3)).trim();
  const after = afterRaw.map(l => l.replace(/^§K§/, ''));
  const norm = s => s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const which = v => { const n = norm(v); let k = opts.findIndex(o => norm(o) === n); if (k < 0) k = opts.findIndex(o => norm(o).length >= 4 && n.startsWith(norm(o))); return k; };
  let correct = -1, picked = -1;
  // tick and cross marks only count when exactly one option carries them (the cross-out buttons can copy as ×)
  const ticks = rawOpts.map(l => /[✓✔]\s*$/.test(l)), xs = rawOpts.map(l => /[✗✘×]\s*$/.test(l));
  if (ticks.filter(Boolean).length === 1) correct = ticks.indexOf(true);
  if (xs.filter(Boolean).length === 1) picked = xs.indexOf(true);
  const txt = after.join('\n');
  if (correct < 0) { // Passmed: "<option> is correct." / "<option> is the correct answer because…"
    for (const l of after) { const m = l.match(/^(.{3,140}?) is (?:the )?correct\b/i); if (m) { const k = which(m[1]); if (k >= 0) { correct = k; break; } } }
  }
  const mC = txt.match(/(?:the )?correct answer(?: is|:)\s*([A-E1-5](?=[).:\s]|$)|[^\n.]{3,90})/i);
  if (correct < 0 && mC) { const v = mC[1].trim(); correct = /^[A-E1-5]$/i.test(v) ? 'ABCDE12345'.indexOf(v.toUpperCase()) % 5 : which(v); }
  const mP = txt.match(/you (?:answered|chose|selected|picked)(?: option)?:?\s*([A-E1-5](?=[).:\s]|$)|[^\n.]{3,90})/i);
  if (picked < 0 && mP) { const v = mP[1].trim(); picked = /^[A-E1-5]$/i.test(v) ? 'ABCDE12345'.indexOf(v.toUpperCase()) % 5 : which(v); }
  if (correct < 0 && after.length) correct = which(after[0]);
  // Passmed explains every option in its own paragraph, starting with the option's name
  const optx = opts.map(() => '');
  after.forEach(l => {
    const ll = l.toLowerCase(); let bk = -1, bl = 0;
    opts.forEach((o, k) => { const ol = o.toLowerCase(); if (ol.length >= 3 && ll.startsWith(ol) && /^[\s,.:;]/.test(l.slice(o.length) || ' ') && ol.length > bl) { bk = k; bl = ol.length; } });
    if (bk >= 0 && !optx[bk] && l.length > opts[bk].length + 8) optx[bk] = l.slice(opts[bk].length).trim().slice(0, 400);
  });
  const expl = after.filter(l => !/correct answer|you (answered|chose|selected|picked)/i.test(l) && !LINKY.test(l) && !RMX_LABEL.test(l)).join(' ').slice(0, 1800);
  const early = correct < 0 && !pct && expl.length < 120;
  return {stem: stem.slice(0, 1500), opts, correct, picked: picked === correct ? -1 : picked, expl, concept, cond, optx, early, ok: opts.length >= 4};
}

/* ----- link to the 168 ILO units ----- */
const rmxNorm = s => String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’']/g, "'").replace(/[^a-z0-9' ]+/g, ' ').replace(/\s+/g, ' ').trim();
let RMX_KEYS = null;
const RMX_GEN = /^(acute|chronic|other|disease|diseases|disorder|disorders|children|adults|upper|lower|lower gi|syndrome|infection|infections|failure|primary|secondary|related|including|overview|differentials|problems|tumours|cancer)$/;
function rmxKeys(){
  if (RMX_KEYS) return RMX_KEYS;
  const K = [], words = {};
  UNITS.forEach(u => {
    u.name.replace(/\([^)]*\)/g, m => ' / ' + m.slice(1, -1)).split(/\s*(?:\/|,|&|;|\band\b|\bincl\b)\s*/i).map(rmxNorm).filter(p => p.length >= 4 && !RMX_GEN.test(p)).forEach(p => K.push([p, u.i]));
    rmxNorm(u.name).split(' ').filter(w => w.length >= 7 && !RMX_GEN.test(w)).forEach(w => { (words[w] = words[w] || new Set()).add(u.name); if (!words[w].ui) words[w].ui = u.i; });
  });
  JG.forEach(j => [j.t].concat(j.al).forEach(a => { const p = rmxNorm(a.split(' vs ')[0]); if (p.length >= 4) j.u.forEach(ui => K.push([p, ui])); }));
  Object.keys(words).forEach(w => { if (words[w].size === 1) K.push([w, words[w].ui]); }); // single distinctive words (cholangitis, pancreatitis)
  K.sort((a, b) => b[0].length - a[0].length);
  return (RMX_KEYS = K);
}
function rmxHit(t, p){ if (t.includes(' ' + p + ' ') || t.includes(' ' + p + 's ')) return true; if (p.length < 7 || p.indexOf(' ') >= 0) return false; return new RegExp(' ' + p.slice(0, p.length - 2).replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '[a-z]* ').test(t); }
function rmxUnitFor(text){
  const t = ' ' + rmxNorm(text) + ' ';
  for (const [p, ui] of rmxKeys()) if (rmxHit(t, p)) return ui;
  return -1;
}
// Passmed condition tags that are worded differently from the ILO conditions
const RMX_COND_ALIAS = {'myocardial infarction': 'Acute coronary syndrome / MI / unstable angina', 'heart failure': 'Cardiac failure', 'deep vein thrombosis': 'VTE & pulmonary embolism', 'venous thromboembolism': 'VTE & pulmonary embolism', 'hyperthyroidism': 'Thyrotoxicosis', 'lower respiratory tract infection': 'Pneumonia (CAP & HAP)', 'gastro oesophageal reflux disease': 'GORD', 'diabetic neuropathy': 'Diabetic complications (macro/micro, neuropathy, nephropathy)', 'diabetic nephropathy': 'Diabetic complications (macro/micro, neuropathy, nephropathy)', 'migraine': 'Headache', 'cluster headache': 'Headache', 'tension type headache': 'Headache', 'peripheral nerve injuries palsies': 'Neuropathies & palsies', 'renal and ureteric stones': 'Urinary tract calculi'};
function rmxCondUnit(names){
  for (const n of names || []) {
    const a = RMX_COND_ALIAS[rmxNorm(n)]; if (a) { const u = UNITS.find(x => x.name === a); if (u) return u.i; }
    const ui = rmxUnitFor(n); if (ui >= 0) return ui;
  }
  return -1;
}

/* ----- highlighting: deciding words in yellow, the changed words struck out → the new words ----- */
function rmxMark(text, phrases){
  const t = String(text || ''), low = t.toLowerCase(), R = [];
  (phrases || []).forEach(p => { const pl = String(p || '').toLowerCase().trim(); if (pl.length < 2) return; let i = low.indexOf(pl); while (i >= 0) { R.push([i, i + pl.length]); i = low.indexOf(pl, i + pl.length); } });
  R.sort((a, b) => a[0] - b[0]); const M = [];
  R.forEach(r => { if (M.length && r[0] <= M[M.length - 1][1]) M[M.length - 1][1] = Math.max(M[M.length - 1][1], r[1]); else M.push(r.slice()); });
  let h = '', p = 0; M.forEach(([a, b]) => { h += esc(t.slice(p, a)) + '<mark class="rmx-mk">' + esc(t.slice(a, b)) + '</mark>'; p = b; });
  return h + esc(t.slice(p));
}
// offline: numbers with units, and stem words the key concept or the right answer's explanation also uses
function rmxLocalTrig(q){
  const out = [], st = q.stem || '';
  (st.match(/\b\d+(?:\.\d+)?\s?(?:mm|cm|kg|g\/l|mmol\/l|µmol\/l|umol\/l|mg|%|hours?|days?|weeks?|months?)(?![a-z])/gi) || []).forEach(x => { if (!out.includes(x)) out.push(x); });
  const ref = rmxNorm((q.concept || '') + ' ' + (q.optx && q.correct >= 0 ? q.optx[q.correct] || '' : ''));
  const refW = ref.split(' ').filter(w => w.length >= 6).map(w => w.slice(0, 6));
  st.split(/[\s,.;:()]+/).forEach(w => { const n = rmxNorm(w); if (n.length >= 6 && refW.includes(n.slice(0, 6)) && !out.some(o => o.toLowerCase() === w.toLowerCase())) out.push(w); });
  return out.slice(0, 4);
}
/* ----- one patient, five endings: for each option, the one clue in THIS patient that makes it the answer ----- */
const rmxWords = (s, n) => { const w = String(s || '').trim().split(/\s+/); return w.length > n ? w.slice(0, n).join(' ') + '…' : w.join(' '); };
const rmxSent = s => String(s || '').match(/[^.!?]+[.!?]?/g) || [];
const RMX_WHEN = [
  /^(?:is|are)\s+(?:(?:usually|typically|mainly|mostly|often|only|best|classically)\s+)?(?:(?:used|indicated|reserved|given|preferred|first[- ]line|appropriate|useful|suitable|seen|found|the (?:treatment|management|investigation|test|drug) of choice)\s+)(?:for|in|when|if|with|after)\s+(.+)/i,
  /^(?:is|are)\s+(?:(?:usually|typically|mainly|mostly|only|best)\s+)?(?:for|if|when)\s+(.+)/i,
  /^(?:could|would|might|may)\s+(?:be\s+)?(?:reasonable|appropriate|correct|right|considered|the answer|used|indicated|suitable|useful|preferred)\s+(?:for|in|if|when|with)\s+(.+)/i,
  /^describes\s+(.+)/i
];
// offline: Passmed's own line for each option, cut down to the clue that would make it right
function rmxOptRow(q, k){
  const raw = ((q.optx && q.optx[k]) || '').replace(/\s+/g, ' ').trim(); if (!raw) return {if: '', why: ''};
  let S = rmxSent(raw).map(x => x.trim()).filter(Boolean);
  if (k === q.correct) {
    S[0] = (S[0] || '').replace(/^(is|are)\s+(the\s+)?correct(\s+answer)?\s*(because|as|since)?[.,:]?\s*/i, '');
    if (S[0].split(/\s+/).length < 3) S.shift();
    return {if: rmxWords((S[0] || '').replace(/[.!?]$/, ''), 12), why: ''};
  }
  for (const R of RMX_WHEN) { const m = (S[0] || '').match(R); if (m) return {if: rmxWords(m[1].replace(/[.!?]$/, ''), 12), why: ''}; }
  S[0] = (S[0] || '').replace(/^(is|are)\s+(incorrect|wrong|not correct|a (common )?(misconception|distractor|trap))\b[.,:]?\s*/i, '').replace(/^(is|are)\s+/i, '');
  if (S[0].split(/\s+/).length < 3) S.shift();
  return {if: '', why: rmxWords((S[0] || '').replace(/[.!?]$/, ''), 12)};
}
function rmxOptLine(q, k){ const r = rmxOptRow(q, k); return r.if || r.why; }
function rmxRoundOrder(q, rows){ // the option you picked first, then the others; three rounds at most
  const w = q.opts.map((_, k) => k).filter(k => k !== q.correct && rows[k] && rows[k].if);
  const rest = shuffle(w.filter(k => k !== q.picked), Math.random);
  return (w.includes(q.picked) ? [q.picked] : []).concat(rest).slice(0, 3);
}
function rmxRounds(q, rows){
  return rmxRoundOrder(q, rows).map(k => {
    let txt = rows[k].if; q.opts.forEach(o => { if (o.length >= 4) txt = txt.split(new RegExp(o.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')).join('▒▒▒'); }); // hide only a whole option name
    return {k: 'if', change: txt, opts: q.opts.slice(), ans: k, why: rows[k].hook || '', how: rows[k].how || ''};
  });
}

/* ----- the AI remix ----- */
function rmxQBlock(q, hasImg){
  return 'You turn a UK medical-school single-best-answer question that a student got wrong into a "same patient, five endings" drill: for every option, the ONE clue in this same patient that would make that option the answer. UK practice only (NICE, BNF, Resus Council UK). Be medically accurate: if a clue would be doubtful, choose a simpler textbook one.\n\n'
    + (hasImg ? 'The attached image is part of the question: read it.\n\n' : '')
    + 'QUESTION:\n' + q.stem + '\n\nOPTIONS:\n' + q.opts.map((o, i) => (i + 1) + '. ' + o).join('\n') + '\n\nCORRECT: ' + (q.correct + 1) + '. ' + q.opts[q.correct]
    + '\nSTUDENT PICKED: ' + (q.picked >= 0 ? (q.picked + 1) + '. ' + q.opts[q.picked] : 'not given')
    + (q.concept ? '\n\nKEY CONCEPT FROM THE QUESTION BANK: ' + q.concept : '')
    + (q.expl ? '\n\nEXPLANATION FROM THE QUESTION BANK (treat as correct):\n' + q.expl.slice(0, 1500) : '')
    + rmxRootNote(q);
}
const rmxRowSpec = q => '"rows":[exactly ' + q.opts.length + ' objects, one per option in the order given: {"if":"at most 9 words: the ONE clue in this same patient that would make this option the answer (for option ' + (q.correct + 1) + ', the clue already in the question that makes it right)","hook":"at most 6 words: a picture or feeling that makes it stick","how":"at most 16 words, Pathophysiology style: cause → what physically happens: the finding or reason this option fits; wrap the 2 or 3 key words in **double asterisks**"}]';
const RMX_RULES = '\nRules: same patient, same question, same options. Each "if" changes ONE clue only, and keep the five on the same theme where you can (size, site, timing, one sign, one result) so they read like a lineup. No pregnancy, allergy or kidney-function twists unless the question is about them. If nothing in this patient could make an option right, set its "if" to "" and make its "hook" the reason it never wins. Plain words, no brackets.';
function rmxPrompt(q){
  return rmxQBlock(q, q.hasImg)
    + '\n\nReply with ONLY this JSON:\n{"film":"the case in at most 18 words: age/sex + main problem + the clue that decides it, using the clue\'s exact words",'
    + '"clue":"at most 5 words copied word for word from QUESTION: the clue that decides it",'
    + '"code":"at most 10 words: a title naming the ONE axis that separates the options, in the form \'A vs B: X vs Y\' (for example \'Extradural vs subdural: artery vs bridging vein\')",'
    + rmxRowSpec(q) + '}' + RMX_RULES;
}
function rmxFreshPrompt(C, avoid){
  return rmxQBlock(C.q, C.hasImg)
    + '\n\nREVIEW ROUND: new clues for the wrong options (keep option ' + (C.q.correct + 1) + '\'s row as it is).' + (avoid.length ? ' ALREADY USED, pick different clues:\n- ' + avoid.join('\n- ') : '')
    + '\n\nReply with ONLY this JSON:\n{' + rmxRowSpec(C.q) + '}' + RMX_RULES;
}
const rmxS1 = v => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, 160);
function rmxRowsFromAi(q, j){
  const R = j && Array.isArray(j.rows) ? j.rows : null;
  if (!R || R.length !== q.opts.length) throw {code: 'invalid_json', message: 'need one row per option'};
  const rows = R.map(r => ({if: rmxS1(r && r.if), hook: rmxS1(r && r.hook), how: rmxS1(r && r.how)}));
  const beats = rmxRounds(q, rows);
  if (beats.length < 2) throw {code: 'invalid_json', message: 'incomplete remix'};
  return {rows, beats};
}
function rmxFromAi(q, j){
  if (!j || typeof j !== 'object' || Array.isArray(j)) throw {code: 'invalid_json', message: 'not an object'};
  const st = (q.stem || '').toLowerCase(), cl = rmxS1(Array.isArray(j.clue) ? j.clue[0] : j.clue);
  const R = rmxRowsFromAi(q, j);
  return {film: rmxS1(j.film), code: rmxS1(j.code), trig: cl.length >= 2 && st.includes(cl.toLowerCase()) ? [cl] : [], rows: R.rows, beats: R.beats};
}

/* ----- offline remix: Passmed's own per-option lines become the rounds; else your ILO clinchers ----- */
function rmxLocal(q){
  const units = q.opts.map(o => rmxUnitFor(o));
  const rows = q.opts.map((_, k) => rmxOptRow(q, k));
  let beats = rmxRounds(q, rows);
  if (beats.length < 2) {
    beats = [];
    const optKeys = q.opts.map(o => rmxNorm(o).split(' ').filter(w => w.length >= 5 && !RMX_GEN.test(w)));
    const mentions = text => { const t = ' ' + rmxNorm(text) + ' '; return q.opts.map((o, k) => { const n = rmxNorm(o); return (n.length >= 4 && rmxHit(t, n)) || (optKeys[k].length && optKeys[k].every(w => rmxHit(t, w))); }); };
    const cands = [];
    [...new Set(units.filter(ui => ui >= 0))].forEach(ui => {
      const mine = units.map((x, k) => x === ui ? k : -1).filter(k => k >= 0);
      (UNITS[ui].ck || []).forEach(ci => {
        if (!CLK[ci] || CLK[ci][0] === 'out') return;
        const m = mentions(CLK[ci][1]), hit = m.map((v, k) => v ? k : -1).filter(k => k >= 0);
        const ans = hit.length === 1 ? hit[0] : hit.length === 0 && mine.length === 1 ? mine[0] : -1;
        if (ans >= 0) cands.push({ui, ci, ans});
      });
    });
    const usedA = new Set();
    shuffle(cands, Math.random).forEach(c => {
      if (beats.length >= 3 || usedA.has(c.ans)) return;
      usedA.add(c.ans);
      let txt = snpMask(dxStrip(CLK[c.ci][1]), UNITS[c.ui]);
      q.opts.forEach(o => { txt = snpMask(txt, {name: o}); });
      beats.push({k: 'ck', change: txt, opts: q.opts.slice(), ans: c.ans, why: CLK[c.ci][1]});
    });
  }
  const words = q.stem.replace(/\s+/g, ' ').split(' ');
  return {film: words.slice(0, 28).join(' ') + (words.length > 28 ? '…' : ''), trig: rmxLocalTrig(q), rows, beats, units};
}

/* ----- 🧬 Why it happens: colour the arrows so the movement stands out (only inside the card body, never in attributes) ----- */
{ const base = rootHtml; rootHtml = function(i, lib){ const h = base(i, lib), k = h.indexOf('<div class="wa">'); return k < 0 ? h : h.slice(0, k) + h.slice(k).replace(/→/g, '<span class="pa-ar">→</span>'); }; }

/* ----- view ----- */
let rmx = {step: 'home', q: null, card: null, i: 0, pick: null, busy: false, ctl: null, err: '', missOnly: false, sys: '', queue: null, scheduled: false, pendingImg: null};
const RMX_BEAT = {if: ['🔄', 'Same patient, one clue changed', 'If instead'], flip: ['🔄', 'Change one clue', 'If instead'], twist: ['🧍', 'Change the patient', 'Now'], time: ['⏱', 'Change the timeline', 'Now'], ck: ['🔑', 'Whose clincher is this?', 'Clincher']};
function viewRemix(m){
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🔄 Remix</span><span class="grow"></span><span class="mono" id="rmxN"></span></div><h1>Remix a question you got wrong</h1><p class="hint" style="margin:0">Answer it on SBA Bank first, then copy the page (⌘A then ⌘C), come here and press ⌘V. You get the case in one line, then the <b>same patient with one clue changed</b>: watch which option wins. Answer with <span class="kbd">1</span>–<span class="kbd">5</span>, <span class="kbd">Enter</span> for next, <span class="kbd">Esc</span> to paste another.</p></div><div id="rmx" class="panel"></div><div id="rmxVault"></div></div>';
  drawRemix(); drawRmxVault();
}
function rmxStatusHtml(){
  let hasKey = true; if (window.medengineAccount) { try { hasKey = !!localStorage.getItem('medengine-anthropic-key'); } catch (e) { hasKey = false; } }
  if (RMX_AI) return '<span class="hint">' + (hasKey ? '🤖 AI remix on' + (window.medengineAccount ? ' · uses your AI key' : '') : '🔑 Add your AI key for the AI remix (offline remix works without it)') + '</span>' + (window.medengineAccount ? '<button class="btn ghost" data-rmxkey>🔑 AI key</button>' : '');
  return '<span class="hint">📴 Offline remix (no AI here): your options are matched to your ILO clinchers</span>';
}
function drawRemix(){
  const box = $('#rmx'); if (!box) return;
  const n = $('#rmxN'); if (n) n.textContent = rmxAll().length + ' saved';
  let h = '';
  if (rmx.step === 'home') {
    const due = rmxAll().filter(rmxIsDue).length;
    h += '<textarea id="rmxIn" class="rmx-in" rows="4" placeholder="Paste the question here (or press ⌘V / Ctrl+V anywhere on this page)." aria-label="Paste a question"></textarea>'
      + (rmx.pendingImg ? '<div class="rmx-imgrow"><button class="rmx-thumb sm" data-rmxzoom="p"><img src="' + rmx.pendingImg.d + '" alt="Image ready"></button><span class="hint">📷 ready: now paste the question</span></div>' : '')
      + '<div class="toolbar"><button class="btn primary" data-rmxpaste>📋 Paste</button><button class="btn" data-rmxgo>Use this text →</button>' + (due ? '<button class="btn" data-rmxdue>▶ ' + due + ' due today</button>' : '') + '<span class="grow"></span><span id="rmxStat" class="rmx-stat">' + rmxStatusHtml() + '</span></div>';
  } else if (rmx.step === 'check') {
    const q = rmx.q;
    h += '<div class="snp-lab">Check it</div><div class="rmx-stem">' + esc(q.stem) + '</div>';
    if (q.early) h += '<div class="kl kl-out"><span class="ki">⏳</span><span>Looks like this one hasn\'t been answered yet. Submit it on SBA Bank first, then copy the page: the explanation is what makes the remix accurate.</span></div>';
    if (q.opts.length < 4) h += '<div class="kl kl-out"><span class="ki">⚠️</span><span>I couldn\'t find the 5 options. Copy the whole question page, or paste the stem with one option per line.</span></div>';
    else h += '<p class="hint" style="margin:0">Tap <b>✅</b> on the right answer and <b>✋</b> on the one you picked.</p><div class="rmx-opts">' + q.opts.map((o, k) => '<div class="rmx-opt' + (k === q.correct ? ' ok' : '') + (k === q.picked ? ' me' : '') + '"><span class="k">' + (k + 1) + '</span><span class="t">' + esc(o) + '</span><button class="iconbtn" data-rmxc="' + k + '" aria-label="Right answer" aria-pressed="' + (k === q.correct) + '">✅</button><button class="iconbtn" data-rmxp="' + k + '" aria-label="My pick" aria-pressed="' + (k === q.picked) + '">✋</button></div>').join('') + '</div>';
    if (rmx.err) h += '<div class="kl kl-out"><span class="ki">⚠️</span><span>' + esc(rmx.err) + '</span></div>';
    const ready = q.opts.length >= 4 && q.correct >= 0, careful = rmxTier() === 'default';
    h += '<div class="toolbar">' + (rmx.busy ? '<span class="rmx-busy">' + (careful ? 'Thinking carefully… (up to a minute)' : 'Thinking…') + '</span><button class="btn" data-rmxstop>Stop</button>' : (RMX_AI ? '<button class="btn primary" data-rmxai' + (ready ? '' : ' disabled') + '>🔄 Remix <span class="kbd">Enter</span></button><button class="btn" data-rmxlocal' + (ready ? '' : ' disabled') + '>Offline remix</button><button class="chip' + (careful ? ' on' : '') + '" data-rmxtier title="Slower but more accurate: use it for tricky topics">🧠 Careful</button>' : '<button class="btn primary" data-rmxlocal' + (ready ? '' : ' disabled') + '>🔄 Remix offline <span class="kbd">Enter</span></button>') + '<button class="btn ghost" data-rmxreset>Start again</button>') + (q.img ? '<button class="rmx-thumb sm" data-rmxzoom="q" title="Tap to zoom"><img src="' + q.img.d + '" alt="Question image"></button><button class="iconbtn" data-rmximgdel aria-label="Remove image" title="Remove image">✕</button>' : '<label class="btn ghost" title="ECG, X-ray or rash? Screenshot it and press ⌘V here, or choose the file" aria-label="Add image"><input type="file" accept="image/*" data-rmximgfile hidden>📷</label>') + '<span class="grow"></span>' + rmxStatusHtml() + '</div>';
  } else if (rmx.step === 'card') h += rmxCardHtml();
  box.innerHTML = h;
  if (rmx.step === 'card' && rmx.card && rmx.card.img) rmxFillThumbs(rmx.card);
}
async function rmxFillThumbs(C){ const im = await rmxImgGet(C.id); if (!im) return; document.querySelectorAll('[data-rmximg="' + C.id + '"]').forEach(b => { b.innerHTML = '<img src="' + im.d + '" alt="Question image">'; b.hidden = false; }); }
const rmxRowsOf = C => (C.c.rows && C.c.rows.length === C.q.opts.length) ? C.c.rows : C.q.opts.map((_, k) => rmxOptRow(C.q, k));
function rmxRowHtml(q, r, k, mark, how){
  return '<div class="rmx-gr' + (k === q.correct ? ' ok' : '') + (k === q.picked && k !== q.correct ? ' me' : '') + '"><span class="k">' + mark + '</span><span><b>' + esc(q.opts[k]) + '</b>'
    + (r.if ? ' <span class="rmx-arw">←</span> ' + esc(r.if) : r.why ? ' <span class="rmx-why">· ' + esc(r.why) + '</span>' : '')
    + (r.hook ? ' <span class="rmx-hook">🔗 ' + esc(r.hook) + '</span>' : '') + (how && r.how ? '<span class="rmx-how">' + fmtRich(r.how) + '</span>' : '') + '</span></div>';
}
function rmxCaseHtml(C){
  const c = C.c, q = C.q, rows = rmxRowsOf(C);
  const film = c.film || q.stem.slice(0, 160), fl = film.toLowerCase();
  let marks = (c.trig || []).filter(t => fl.includes(String(t).toLowerCase()));
  if (!marks.length) marks = [].concat(...(c.trig || []).map(t => String(t).match(/\d+(?:\.\d+)?\s?[a-zµ%\/]*|[a-z][a-z'-]{3,}/gi) || [])).filter(w => new RegExp('(^|[^a-z0-9])' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '($|[^a-z0-9])', 'i').test(film));
  let h = '<div class="rmx-case"><div class="snp-lab">① What happened</div><div class="stem snp-clue">🎬 ' + rmxMark(film, marks) + '</div>';
  const ended = rmx.card === C && rmx.i >= (c.beats || []).length && (c.beats || []).length > 0;
  if (ended && rows.filter(r => r.if || r.why || r.hook).length >= 2) { /* the lineup below already has these */ }
  else if (c.rows || rows[q.correct].if) {
    h += rmxRowHtml(q, rows[q.correct], q.correct, '✅');
    if (q.picked >= 0 && q.picked !== q.correct) h += rmxRowHtml(q, rows[q.picked], q.picked, '❌');
  } else { // cards saved before v0.10
    if (c.right) h += '<div class="kl kl-in"><span class="ki">✅</span><span><b>' + esc(q.opts[q.correct]) + '</b>: ' + esc(c.right) + '</span></div>';
    if (c.wrong) h += '<div class="kl kl-out"><span class="ki">❌</span><span>' + (q.picked >= 0 ? '<b>' + esc(q.opts[q.picked]) + '</b>: ' : '') + esc(c.wrong) + '</span></div>';
  }
  const us = [...new Set([C.unit].concat(c.units || []).filter(x => x != null && x >= 0))].slice(0, 3);
  if (us.length || C.img) h += '<div class="chips rmx-chips">' + (C.img ? '<button class="rmx-thumb sm" data-rmxzoom="c" data-rmximg="' + C.id + '" hidden></button>' : '') + us.map(ui => UNITS[ui] ? '<button class="chip" data-u="' + ui + '" data-mode="read">📖 ' + esc(UNITS[ui].name) + '</button>' : '').join('') + '</div>';
  return h + '</div>';
}
// the matching Pathophysiology card from your library (checked content), for the card's condition first
// the best card is the one that names the most of this question's options (ties: the card's own condition first)
function rmxRootPick(q, unit){
  const us = [unit].concat(q.opts.map(o => rmxUnitFor(o))).filter(u => u != null && u >= 0);
  if (!us.length) return -1;
  const keys = q.opts.map(o => rmxNorm(o).split(' ').filter(w => w.length >= 5 && !RMX_GEN.test(w)));
  let best = -1, bs = -1;
  ROOTS.forEach((r, i) => {
    const ru = r.u || [], hitU = us.findIndex(u => ru.includes(u)); if (hitU < 0) return;
    const txt = ' ' + rmxNorm(r.t + ' ' + r.l.join(' ')) + ' ';
    const sc = keys.filter(k => k.length && k.some(w => txt.includes(' ' + w))).length * 10 + (hitU === 0 ? 5 : 0) - hitU * 0.01;
    if (sc > bs) { bs = sc; best = i; }
  });
  return best;
}
function rmxRootFor(C){ return rmxRootPick(C.q, C.unit); }
// the checked card goes into the AI prompt so its "why" lines stay consistent with your library
function rmxRootNote(q){
  const i = rmxRootPick(q, rmxCondUnit(q.cond)); if (i < 0) return '';
  const r = ROOTS[i]; return ('\n\nCHECKED MECHANISM NOTES from the student\'s library (stay consistent with these; reuse their cause → effect logic):\n' + r.t + '\n- ' + r.l.join('\n- ')).replace(/\*\*/g, '').slice(0, 1200);
}
// the payoff: one line per option, all on the same axis (answer ← the clue that picks it)
function rmxLineupHtml(C){
  const q = C.q, rows = rmxRowsOf(C);
  if (rows.filter(r => r.if || r.why || r.hook).length < 2 && !q.concept && !C.c.code) return '';
  const code = C.c.code ? '<div class="rmx-code">🧬 ' + esc(C.c.code) + '</div>' : q.concept ? '<div class="rmx-rule">🔑 ' + esc(q.concept) + '</div>' : '';
  const ri = rmxRootFor(C);
  return '<div class="rmx-lineup"><div class="snp-lab">🧬 Why it happens</div>' + code
    + '<div class="rmx-grid">' + rows.map((r, k) => rmxRowHtml(q, r, k, k === q.correct ? '✅' : k === q.picked ? '✋' : k + 1, true)).join('') + '</div>' + (ri >= 0 ? rootHtml(ri) : '') + '</div>';
}
function rmxCardHtml(){
  const C = rmx.card, c = C.c, i = rmx.i, total = c.beats.length;
  let h = '<div class="qmeta"><span class="code">' + (rmx.queue ? '🔁 Replay ' + (rmx.queue.pos + 1) + ' / ' + rmx.queue.list.length : '🔄 Remix') + '</span>' + (C.src === 'local' ? '<span class="code">📴 offline</span>' : '<span class="code" title="Written by AI from your question: check it against the explanation">🤖 AI</span>') + '<span class="grow"></span><span class="mono">' + (C.res || []).map(r => r == null ? '·' : r ? '✅' : '❌').join(' ') + '</span><button class="btn ghost rmx-out" data-rmxreset title="Back to pasting (Esc). You can also just press ⌘V here.">' + (rmx.queue ? '⏹ Stop replay' : '📋 New question') + ' <span class="kbd">Esc</span></button></div>';
  h += rmxCaseHtml(C);
  if (!total) return h + '<p class="hint">Not enough here to build rounds offline. Turn the AI on for a full remix.</p>' + rmxLineupHtml(C) + '<div class="toolbar"><button class="btn primary" data-rmxnext>Done <span class="kbd">Enter</span></button></div>';
  if (i < total) {
    const b = c.beats[i], B = RMX_BEAT[b.k], tag = b.k === 'time' && b.spd ? ' · ' + esc(b.spd) : '';
    h += '<div class="snp-lab rmx-bl"><span>' + '②③④⑤'[i] + ' ' + B[0] + ' ' + B[1] + tag + '</span>' + (b.k !== 'ck' ? '<button class="iconbtn rmx-flag" data-rmxflag title="Looks medically wrong: drop it" aria-label="Looks wrong: drop it">🚩</button>' : '') + '</div>';
    h += '<div class="rmx-chg"><b>' + B[2] + ':</b> ' + (b.k === 'ck' ? snpHtml(b.change) : esc(b.change)) + '</div>';
    h += '<div class="opts">' + b.opts.map((o, k) => { let cl = 'opt'; if (rmx.pick != null) { if (k === b.ans) cl += ' right'; else if (k === rmx.pick) cl += ' wrong'; } return '<button class="' + cl + '" data-rmxa="' + k + '"' + (rmx.pick != null ? ' disabled' : '') + '><span class="k">' + (k + 1) + '</span><span>' + esc(o) + '</span></button>'; }).join('') + '</div>';
    if (rmx.pick != null) h += '<div class="kl ' + (rmx.pick === b.ans ? 'kl-in' : 'kl-out') + '"><span class="ki">' + (rmx.pick === b.ans ? '✅' : '❌') + '</span><span>' + (b.k === 'ck' ? fmtRich(b.why) : b.k === 'if' ? '<b>' + esc(b.opts[b.ans]) + '</b>' + (b.why ? ' <span class="rmx-hook">🔗 ' + esc(b.why) + '</span>' : '') + (b.how ? '<span class="rmx-how">🧬 ' + fmtRich(b.how) + '</span>' : '') : esc(b.why)) + '</span></div><div class="toolbar"><button class="btn primary" data-rmxnext>' + (i + 1 < total ? 'Next' : 'Finish') + ' <span class="kbd">Enter</span></button></div>';
  } else {
    const got = C.res.filter(Boolean).length, asked = C.res.filter(r => r != null).length;
    h += '<div class="snp-end"><div class="rmx-endl"><b>' + got + ' / ' + asked + '</b>' + (C.due ? '<span class="hint">back ' + rmxDueLabel(C.due) + '</span>' : '') + '</div>' + rmxLineupHtml(C) + '<div class="toolbar">' + (rmx.queue ? '<button class="btn primary" data-rmxnext>' + (rmx.queue.pos + 1 < rmx.queue.list.length ? 'Next card' : 'Finish replay') + ' <span class="kbd">Enter</span></button>' : '<button class="btn primary" data-rmxreset>📋 Paste another <span class="kbd">Enter</span></button>') + '</div></div>';
  }
  return h;
}
function rmxVaultList(){ let list = rmx.missOnly ? rmxAll().filter(c => c.res.some(r => r === false)) : rmxAll(); if (rmx.sys) list = list.filter(c => UNITS[c.unit] && usys(UNITS[c.unit]) === rmx.sys); return list; }
function drawRmxVault(){
  const box = $('#rmxVault'); if (!box) return;
  const all = rmxAll(), miss = all.filter(c => c.res.some(r => r === false)), due = all.filter(rmxIsDue);
  if (!all.length) { box.innerHTML = ''; return; }
  const list = rmxVaultList(), bySys = {};
  all.forEach(c => { const u = UNITS[c.unit], s = u ? usys(u) : ''; if (s) bySys[s] = (bySys[s] || 0) + 1; });
  const sysE = Object.entries(bySys).sort((a, b) => b[1] - a[1]);
  box.innerHTML = '<div class="panel"><div class="toolbar"><b class="grow">🗂 Remix vault · ' + all.length + '</b><button class="btn' + (due.length ? ' primary' : '') + '" data-rmxdue' + (due.length ? '' : ' disabled') + '>▶ Due today · ' + due.length + '</button><button class="btn" data-rmxreplay>🔁 Replay ' + list.length + '</button><button class="btn' + (rmx.missOnly ? ' primary' : '') + '" data-rmxmiss>♻️ Only misses · ' + miss.length + '</button><button class="btn ghost" data-rmxexport>⬇️ Export</button><button class="btn ghost" data-rmxclear>🗑 Clear</button></div>'
    + (sysE.length >= 2 ? '<div class="chips rmx-sys"><span class="hint">🗺 Misses by system</span>' + sysE.map(([s, n]) => '<button class="chip' + (rmx.sys === s ? ' on' : '') + '" data-rmxsys="' + s + '">' + esc(MEV.sysLabel(s)) + ' · ' + n + '</button>').join('') + '</div>' : '')
    + '<div class="rmx-list">' + list.slice(0, 30).map(c => '<button class="rmx-item" data-rmxopen="' + c.id + '"><span class="t">' + (c.img ? '📷 ' : '') + esc(c.c.film || c.q.stem.slice(0, 120)) + '</span><span class="hint">' + (c.res || []).map(r => r == null ? '·' : r ? '✅' : '❌').join('') + ' · ' + new Date(c.ts).toLocaleDateString('en-GB') + (c.due ? ' · ' + (rmxIsDue(c) ? 'due now' : 'back ' + rmxDueLabel(c.due)) : '') + '</span></button>').join('') + (list.length > 30 ? '<p class="hint">…and ' + (list.length - 30) + ' older</p>' : '') + '</div></div>';
}
function rmxHome(){
  if (rmx.ctl && rmx.busy) rmx.ctl.abort();
  rmx = Object.assign(rmx, {step: 'home', q: null, card: null, queue: null, err: '', busy: false, pick: null});
  drawRemix(); drawRmxVault();
  setTimeout(() => { const el = $('#rmxIn'); if (el) { el.focus({preventScroll: true}); el.scrollIntoView({block: 'nearest'}); } }, 30);
}
function rmxIngest(text){
  const q = rmxParse(text);
  if (!q.stem || q.stem.length < 30) return toast('That doesn\'t look like a question: copy the question page and paste again');
  if (rmx.pendingImg) { q.img = rmx.pendingImg; rmx.pendingImg = null; }
  rmx = Object.assign(rmx, {step: 'check', q, card: null, i: 0, pick: null, err: '', queue: null});
  drawRemix();
}
async function rmxAttachImg(file){
  let img; try { img = await compressImg(file); } catch (e) { return toast('That file is not an image'); }
  if (rmx.step === 'check' && rmx.q) { rmx.q.img = img; drawRemix(); toast('📷 Image added'); }
  else { rmx.pendingImg = img; if (rmx.step === 'home') drawRemix(); toast('📷 Image ready: now paste the question text'); }
}
function rmxMake(c, src){
  const q = rmx.q, cu = rmxCondUnit(q.cond);
  if (src === 'local' && !(c.trig || []).length) c.trig = rmxLocalTrig(q);
  const card = {id: 'rx' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5), ts: Date.now(), src, q: {stem: q.stem, opts: q.opts, correct: q.correct, picked: q.picked, expl: (q.expl || '').slice(0, 1500), concept: q.concept || '', cond: q.cond || [], optx: q.optx || []}, unit: cu >= 0 ? cu : rmxUnitFor(q.opts[q.correct]), img: !!q.img, c, res: c.beats.map(() => null), due: rmxAddDays(rmxDay(), 1), box: 0, seen: [], n: 0};
  if (q.img) rmxImgPut(card.id, q.img);
  rmxAll().unshift(card);
  rmxCards.slice(RMX_MAX).forEach(x => { if (x.img) rmxImgDel(x.id); });
  rmxCards = rmxCards.slice(0, RMX_MAX); rmxSave();
  rmx = Object.assign(rmx, {step: 'card', card, i: 0, pick: null, busy: false, err: '', queue: null, scheduled: false});
  drawRemix(); drawRmxVault();
}
function rmxAiErr(e){
  const code = e && e.code;
  if (code === 'sign_in_required' && window.medengineAccount) window.medengineAccount.open(code);
  if (['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'].includes(code)) RMX_AI = null;
  return ({invalid_json: 'The AI reply came back garbled. Try again, or use the offline remix.', rate_limited: 'Too many requests just now. Wait a minute, or use the offline remix.', sign_in_required: 'Add your AI key first (🔑), or use the offline remix.', not_granted: 'AI isn\'t allowed on this page, so use the offline remix.', refused: 'The AI declined this one. Use the offline remix.', images_unavailable: 'The AI here can\'t see images: remove the image or use the offline remix.', image_rejected: 'That image couldn\'t be sent: try a smaller screenshot.'})[code] || ((e && e.message) || 'The AI could not answer. Try again, or use the offline remix.');
}
async function rmxRunAi(){
  const q = rmx.q; if (!RMX_AI || rmx.busy || q.correct < 0) return;
  rmx.busy = true; rmx.err = ''; rmx.ctl = new AbortController(); drawRemix();
  try {
    const images = q.img && RMX_IMG ? rmxBlob(q.img.d) : null;
    const j = await RMX_AI.json(rmxPrompt(Object.assign({}, q, {hasImg: !!images})), Object.assign({modelTier: rmxTier(), maxTokens: rmxTier() === 'default' ? 8000 : 2400, signal: rmx.ctl.signal, cache: false}, images ? {images} : {}));
    rmxMake(rmxFromAi(q, j), 'ai');
  } catch (e) {
    rmx.busy = false;
    if (e && e.code === 'cancelled') { drawRemix(); return; }
    rmx.err = rmxAiErr(e); drawRemix();
  }
}
/* ----- replays: instant, on a spaced schedule; next time's variations are made quietly after you finish ----- */
async function rmxFreshBeats(C){
  if (!RMX_AI) return null;
  const avoid = (C.seen || []).concat((C.c.beats || []).map(b => b.change)).filter(Boolean).slice(-12);
  try {
    let images = null; if (C.img && RMX_IMG) { const im = await rmxImgGet(C.id); if (im) images = rmxBlob(im.d); }
    const j = await RMX_AI.json(rmxFreshPrompt(Object.assign({}, C, {hasImg: !!images}), avoid), Object.assign({modelTier: 'quick', maxTokens: 1800, cache: false}, images ? {images} : {}));
    return rmxRowsFromAi(C.q, j);
  } catch (e) { return null; }
}
const rmxMaking = new Set();
function rmxMakeNext(C){
  if (!C || C.src !== 'ai' || !RMX_AI || rmxMaking.has(C.id)) return;
  rmxMaking.add(C.id);
  rmxFreshBeats(C).then(R => { rmxMaking.delete(C.id); if (R && R.beats.length >= 2) { C.next = R; rmxSave(); } });
}
function rmxReuse(C){ return (C.c.beats || []).filter(b => !b.flag).map(b => { if (b.k === 'ck' || b.k === 'if') return b; const idx = shuffle(b.opts.map((_, i) => i), Math.random); return Object.assign({}, b, {opts: idx.map(i => b.opts[i]), ans: idx.indexOf(b.ans)}); }); }
function rmxPlay(card, queue){
  rmx = Object.assign(rmx, {step: 'card', card, i: 0, pick: null, queue: queue || null, scheduled: false, err: ''});
  if (card.src === 'local') { const L = rmxLocal(card.q); if (L.beats.length) card.c.beats = L.beats; }
  else if (card.next && card.next.beats && card.next.beats.length >= 2) { card.seen = (card.seen || []).concat(card.c.beats.map(b => b.change)).filter(Boolean).slice(-12); card.c.rows = card.next.rows; card.c.beats = card.next.beats; delete card.next; }
  else if (card.c.rows && card.c.rows.length === card.q.opts.length) { delete card.next; card.c.beats = rmxRounds(card.q, card.c.rows); }
  else { delete card.next; card.c.beats = rmxReuse(card); }
  card.c.beats = card.c.beats.filter(b => !b.flag); card.res = card.c.beats.map(() => null);
  rmxSave(); drawRemix();
  const b = $('#rmx'); if (b) b.scrollIntoView({block: 'start'});
}
function rmxSchedule(C){
  const wrong = C.res.some(r => r === false);
  C.n = (C.n || 0) + 1; C.last = Date.now();
  C.box = C.n === 1 || wrong ? 0 : Math.min((C.box || 0) + 1, RMX_GAP.length - 1);
  C.due = rmxAddDays(rmxDay(), RMX_GAP[C.box]);
  rmxSave();
}
function rmxFinish(){ const C = rmx.card; if (!rmx.scheduled && C && rmx.i >= C.c.beats.length) { rmx.scheduled = true; rmxSchedule(C); rmxMakeNext(C); drawRmxVault(); } }
// leaving half-way: anything you got wrong still comes back tomorrow, nothing moves forward
function rmxLeave(){ const C = rmx.card; if (rmx.step !== 'card' || !C || rmx.scheduled) return; if (rmx.i >= C.c.beats.length) return rmxFinish(); if ((C.res || []).some(r => r === false)) { C.box = 0; C.due = rmxAddDays(rmxDay(), 1); rmxSave(); } }
function rmxAnswer(k){
  if (rmx.step !== 'card' || rmx.pick != null) return;
  const C = rmx.card, b = C.c.beats[rmx.i]; if (!b || k >= b.opts.length) return;
  rmx.pick = k; C.res[rmx.i] = k === b.ans;
  if (C.res[rmx.i]) addXp(5);
  rmxSave(); drawRemix();
}
function rmxFlag(){
  if (rmx.step !== 'card') return;
  const C = rmx.card, b = C.c.beats[rmx.i]; if (!b) return;
  b.flag = true; C.res[rmx.i] = null; if (b.k === 'if' && C.c.rows && C.c.rows[b.ans]) C.c.rows[b.ans] = {if: '', hook: ''}; C.seen = (C.seen || []).concat('(this one was wrong) ' + b.change).slice(-12);
  toast('🚩 Dropped: it won\'t come back');
  rmx.pick = null; rmx.i++; if (rmx.i >= C.c.beats.length) rmxFinish();
  rmxSave(); drawRemix();
}
function rmxNext(){
  if (rmx.step !== 'card') return;
  const C = rmx.card, total = C.c.beats.length;
  if (rmx.i < total) { if (rmx.pick == null) return; rmx.i++; rmx.pick = null; if (rmx.i >= total) rmxFinish(); return drawRemix(); }
  rmxFinish();
  if (rmx.queue) { rmx.queue.pos++; if (rmx.queue.pos < rmx.queue.list.length) return rmxPlay(rmx.queue.list[rmx.queue.pos], rmx.queue); rmx.queue = null; toast('🔁 Replay done'); }
  rmxHome();
}
function rmxQueue(list){ list = list.filter(c => c.src === 'local' || (c.c.beats || []).length); if (!list.length) return toast('Nothing to replay'); rmxPlay(list[0], {list: list.slice(), pos: 0}); }
function rmxReplay(){ rmxQueue(rmxVaultList()); }
function rmxDue(){ rmxQueue(rmxAll().filter(rmxIsDue).sort((a, b) => (a.due < b.due ? -1 : a.due > b.due ? 1 : a.ts - b.ts))); }
async function rmxExport(){
  const data = JSON.stringify({app: 'medengine-STUDY', kind: 'remix-vault', exported: new Date().toISOString(), note: 'Images stay on this device and are not exported.', cards: rmxAll()}, null, 1), name = 'medengine-remix-vault-' + new Date().toISOString().slice(0, 10) + '.json';
  let dl = null; try { if (window.claude && claude.use) dl = await claude.use('downloads'); } catch (e) {}
  if (dl) { try { await dl.save({filename: name, data: new Blob([data], {type: 'application/json'})}); return; } catch (e) { if (e && e.code === 'declined') return; } }
  try { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], {type: 'application/json'})); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); } catch (e) { toast('Export is not available here'); }
}
async function rmxPasteBtn(){
  try { const t = await navigator.clipboard.readText(); if (t && t.trim()) return rmxIngest(t); } catch (e) {}
  const el = $('#rmxIn'); if (el) el.focus(); toast('Long-press the box and tap Paste (or press ⌘V)');
}
function rmxZoom(src){
  if (!src) return;
  let ov = $('#rmxZoom');
  if (!ov) { ov = document.createElement('div'); ov.className = 'overlay'; ov.id = 'rmxZoom'; document.body.appendChild(ov); ov.addEventListener('click', () => { ov.hidden = true; }); }
  ov.innerHTML = '<div class="modal shotmodal" role="dialog" aria-label="Question image"><div class="shotbig"><img src="' + src + '" alt="Question image"></div><p class="hint" style="margin:0">Tap anywhere to close</p></div>';
  ov.hidden = false;
}
document.addEventListener('paste', e => {
  if (route.view !== 'remix') return;
  const tg = e.target;
  if (tg && (tg.tagName === 'INPUT' || (tg.tagName === 'TEXTAREA' && tg.id !== 'rmxIn') || tg.isContentEditable)) return;
  const cd = e.clipboardData; if (!cd) return;
  const t = cd.getData('text/plain') || '';
  let file = Array.from(cd.files || []).find(f => /^image\//.test(f.type)) || null;
  if (!file && cd.items) for (const it of cd.items) if (it.kind === 'file' && /^image\//.test(it.type)) { file = it.getAsFile(); break; }
  if (t.trim().length >= 30) { e.preventDefault(); rmxLeave(); rmxIngest(t); if (file) rmxAttachImg(file); return; }
  if (file) { e.preventDefault(); rmxAttachImg(file); }
});
document.addEventListener('change', e => { const t = e.target; if (t && t.dataset && t.dataset.rmximgfile != null && t.files && t.files[0]) { const f = t.files[0]; t.value = ''; rmxAttachImg(f); } });
document.addEventListener('dragover', e => { if (route.view === 'remix' && rmx.step === 'check') e.preventDefault(); });
document.addEventListener('drop', e => { if (route.view !== 'remix' || rmx.step !== 'check') return; const f = Array.from((e.dataTransfer && e.dataTransfer.files) || []).find(x => /^image\//.test(x.type)); if (f) { e.preventDefault(); rmxAttachImg(f); } });
function rmxKey(e){
  if (route.view !== 'remix') return false;
  const k = e.key;
  const zo = $('#rmxZoom'); if (zo && !zo.hidden && k === 'Escape') { zo.hidden = true; return true; }
  if (rmx.step === 'check' && k === 'Enter' && !rmx.busy && rmx.q.correct >= 0 && rmx.q.opts.length >= 4) { e.preventDefault(); RMX_AI ? rmxRunAi() : rmxMake(rmxLocal(rmx.q), 'local'); return true; }
  if (k === 'Escape' && rmx.step !== 'home') { e.preventDefault(); rmxLeave(); rmxHome(); return true; }
  if (rmx.step !== 'card') return false;
  const C = rmx.card;
  if (/^[1-5]$/.test(k) && rmx.i < C.c.beats.length) { e.preventDefault(); rmxAnswer(+k - 1); return true; }
  if (k === 'Enter' || k === ' ' || k === 'ArrowRight') {
    if (rmx.i >= C.c.beats.length && !rmx.queue) { e.preventDefault(); rmxFinish(); rmxHome(); return true; }
    e.preventDefault(); rmxNext(); return true;
  }
  return k.toLowerCase() === 's';
}
document.addEventListener('keydown', e => { const tg = e.target; if (tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || tg.isContentEditable) || e.metaKey || e.ctrlKey || e.altKey) return; if (rmxKey(e)) e.stopImmediatePropagation(); }, true);

/* ----- Weak spots: what you got wrong in Remix, clustered by ILO condition ----- */
function rmxWeakPanel(m){
  const all = rmxAll(); if (!all.length) return;
  const due = all.filter(rmxIsDue).length, byU = {};
  all.forEach(c => { if (c.unit >= 0 && UNITS[c.unit]) byU[c.unit] = (byU[c.unit] || 0) + 1; });
  const E = Object.entries(byU).sort((a, b) => b[1] - a[1]).slice(0, 12);
  const html = '<div class="panel rmx-weak"><div class="toolbar"><b class="grow">🔄 From Remix · ' + all.length + ' question' + (all.length === 1 ? '' : 's') + ' you got wrong</b>' + (due ? '<button class="btn primary" data-rmxduego>▶ ' + due + ' due today</button>' : '') + '<button class="btn" data-go="remix">Open Remix →</button></div>'
    + (E.length ? '<div class="chips">' + E.map(([ui, n]) => '<button class="chip" data-u="' + ui + '" data-mode="read" style="--h:' + wkHue[UNITS[ui].w] + '"><span class="dot"></span>' + esc(UNITS[ui].name) + ' · ' + n + '</button>').join('') + '</div>' : '') + '</div>';
  const ph = m.querySelector('.ph'); if (ph) ph.insertAdjacentHTML('afterend', html);
}
if (typeof viewWeak === 'function') { const _viewWeak = viewWeak; viewWeak = function (m){ _viewWeak(m); try { rmxWeakPanel(m); } catch (e) {} }; }

function extClick8(t, d){
  if (d.spdset) { S.set.spd = S.set.spd === d.spdset ? '' : d.spdset; save(); renderSide(); if (route.view === 'home') render(); if (S.set.spd && matchMedia('(max-width:860px)').matches) document.body.classList.add('nav'); return true; }
  if (d.rmxduego != null) { go({view: 'remix'}); rmxDue(); return true; }
  if (route.view !== 'remix') return false;
  if (d.rmxpaste != null) { rmxPasteBtn(); return true; }
  if (d.rmxgo != null) { const el = $('#rmxIn'); if (el && el.value.trim()) rmxIngest(el.value); else toast('Paste a question first'); return true; }
  if (d.rmxc != null) { rmx.q.correct = +d.rmxc; rmx.q.early = false; if (rmx.q.picked === rmx.q.correct) rmx.q.picked = -1; drawRemix(); return true; }
  if (d.rmxp != null) { const k = +d.rmxp; rmx.q.picked = rmx.q.picked === k || k === rmx.q.correct ? -1 : k; drawRemix(); return true; }
  if (d.rmxai != null) { rmxRunAi(); return true; }
  if (d.rmxlocal != null) { rmxMake(rmxLocal(rmx.q), 'local'); return true; }
  if (d.rmxtier != null) { S.set.rmxTier = rmxTier() === 'default' ? 'quick' : 'default'; save(); drawRemix(); toast(rmxTier() === 'default' ? '🧠 Careful mode: slower, more accurate' : '⚡ Fast mode'); return true; }
  if (d.rmxstop != null) { if (rmx.ctl) rmx.ctl.abort(); return true; }
  if (d.rmxreset != null) { rmxLeave(); rmxHome(); return true; }
  if (d.rmxa != null) { rmxAnswer(+d.rmxa); return true; }
  if (d.rmxnext != null) { rmxNext(); return true; }
  if (d.rmxflag != null) { rmxFlag(); return true; }
  if (d.rmximgdel != null) { if (rmx.q) { rmx.q.img = null; drawRemix(); } return true; }
  if (d.rmxzoom) { if (d.rmxzoom === 'q' && rmx.q && rmx.q.img) rmxZoom(rmx.q.img.d); else if (d.rmxzoom === 'p' && rmx.pendingImg) rmxZoom(rmx.pendingImg.d); else if (d.rmxzoom === 'c' && rmx.card) rmxImgGet(rmx.card.id).then(im => im && rmxZoom(im.d)); return true; }
  if (d.rmxkey != null) { if (window.medengineAccount) window.medengineAccount.open(); return true; }
  if (d.rmxopen) { const c = rmxAll().find(x => x.id === d.rmxopen); if (c) rmxPlay(c, null); return true; }
  if (d.rmxdue != null) { rmxDue(); return true; }
  if (d.rmxreplay != null) { rmxReplay(); return true; }
  if (d.rmxmiss != null) { rmx.missOnly = !rmx.missOnly; drawRmxVault(); return true; }
  if (d.rmxsys) { rmx.sys = rmx.sys === d.rmxsys ? '' : d.rmxsys; drawRmxVault(); return true; }
  if (d.rmxexport != null) { rmxExport(); return true; }
  if (d.rmxclear != null) { if (!t.dataset.armed) { t.dataset.armed = '1'; t.textContent = 'Tap again to delete all'; return true; } rmxAll().forEach(c => { if (c.img) rmxImgDel(c.id); }); rmxCards = []; rmxSave(); drawRmxVault(); drawRemix(); toast('Remix vault cleared'); return true; }
  return false;
}
try { Object.defineProperty(window, '__me8', {value: Object.freeze({rmxParse, rmxUnitFor, rmxCondUnit, rmxFromAi, rmxLocal, rmxMark, rmxOptLine, rmxDay, rmxAddDays, rmxIsDue, get rmx(){ return rmx; }, rmxAll: () => rmxAll(), save: () => rmxSave(), imgGet: id => rmxImgGet(id), rootPick: (q, u) => { const i = rmxRootPick(q, u); return i >= 0 ? ROOTS[i].id : ''; }, setAi(f, img){ RMX_AI = f; RMX_IMG = !!img; }})}); } catch (e) {}
