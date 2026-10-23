/* ---------- v0.8: 🔄 Remix (missed question → 3 one-change variations), speed tags ---------- */
const SPD = D.spdl || {};
const spdBadge = u => u.spd && SPD[u.spd] ? '<span class="spd" title="' + esc(SPD[u.spd][1] + ': ' + SPD[u.spd][2]) + '">' + SPD[u.spd][0] + ' ' + esc(SPD[u.spd][1]) + '</span>' : '';
function spdChipsHtml(){
  return '<div class="chips spdrow"><span class="hint">⏱ Speed</span>' + Object.keys(SPD).map(k => { const n = UNITS.filter(u => u.spd === k).length; return '<button class="chip' + (S.set.spd === k ? ' on' : '') + '" data-spdset="' + k + '" title="' + esc(SPD[k][2]) + '">' + SPD[k][0] + ' ' + esc(SPD[k][1]) + ' · ' + n + '</button>'; }).join('') + '</div>';
}

/* ----- AI: the claude.ai runtime in the artifact; the user's own key in the downloaded/website build ----- */
let RMX_AI = null;
(async () => { try { if (window.claude && claude.use) RMX_AI = await claude.use('sample'); } catch (e) { RMX_AI = null; } if (route.view === 'remix') { if (rmx.step === 'check') drawRemix(); else { const st = $('#rmxStat'); if (st) st.innerHTML = rmxStatusHtml(); } } })();

/* ----- storage (this browser only) ----- */
const RMX_LS = 'medengine-remix-v1', RMX_MAX = 100;
let rmxCards = null;
function rmxAll(){ if (rmxCards) return rmxCards; try { rmxCards = JSON.parse(localStorage.getItem(RMX_LS) || '[]'); } catch (e) { rmxCards = []; } if (!Array.isArray(rmxCards)) rmxCards = []; return rmxCards; }
function rmxSave(){ try { localStorage.setItem(RMX_LS, JSON.stringify(rmxAll().slice(0, RMX_MAX))); return true; } catch (e) { toast('Could not save: browser storage is full or blocked'); return false; } }

/* ----- paste → question: strip the Passmedicine page around it ----- */
const RMX_JUNK = /^(passmedicine|medical student finals.*|home|questions|question bank|previous sessions|mock exams|review questions|performance|comment threads|textbooks?|high-yield textbook|extended textbook|knowledge tutor|review facts|custom revision|revision sets|concepts|all concepts|top 100 concepts|ukmla content map.*|reference ranges|end and review|next question|previous question|next|previous|submit( answer)?|skip|flag( question)?|rate this question.*|report( an)? (error|issue)|report broken (link|media)|suggest (better categorisation|link)|key concept image|important for me.*|less important|very important|feedback|show (explanation|answer)|hide|menu|log ?out|sign ?out|my account|settings|help|contact us|privacy.*|terms.*|cookie.*|©.*|copyright.*|all contents of this site.*|back to top|score:?\s*\d+%?|\d+\s*\/\s*\d+|\d+|time( remaining)?:?.*|\d{1,3}(\.\d)?%|average score.*|\d+ (people|users) .*)$/i;
const RMX_END = /^(comments?|discussion|add a comment|post( a)? comment|\d+ comments?|show comments|view comments)$/i;
const RMX_QMARK = /^question [\d,]+ of [\d,]+$/i;
const LINKY = /youtube|video|zero to finals|brandl|osmosis|geeky medics|medicosis|ninja nerd|\bwatch\b|\d+ \d+$/i;
function rmxParse(raw){
  let L = String(raw || '').replace(/\r/g, '').split('\n').map(s => s.replace(/\s+/g, ' ').trim()).filter(Boolean);
  L = L.map(l => RMX_QMARK.test(l) ? '§Q§' : l).filter(l => l === '§Q§' || !RMX_JUNK.test(l));
  const end = L.findIndex((l, i) => i > 3 && RMX_END.test(l)); if (end > 0) L = L.slice(0, end);
  const optLine = l => l.replace(/^\(?([A-Ea-e1-5])[).:]\s+/, '').replace(/\s+\d{1,3}(\.\d)?%$/, '').replace(/\s*[✓✔✗✘×]\s*$/, '').trim();
  const isOpt = l => { if (l === '§Q§') return false; const o = optLine(l); return o.length >= 1 && o.length <= 110 && !/[?]$/.test(o) && !/\.\s+[A-Z]/.test(o.slice(0, -1)); };
  // the case runs back from the question line: to "Question N of M" if Passmed's marker is there,
  // otherwise over sentences, lab rows (digits) and lines ending in . or : (up to 10 lines)
  const caseStart = i => { let a = i; while (a > 0 && L[a - 1] !== '§Q§' && i - a < 10 && (L[a - 1].length > 40 || /[.:]$/.test(L[a - 1]) || /\d/.test(L[a - 1]))) a--; return a; };
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
  if (!cands.length) return {stem: L.filter(l => l !== '§Q§').join(' ').slice(0, 1500), opts: [], correct: -1, picked: -1, expl: '', ok: false};
  const best = cands.reduce((x, y) => y.score > x.score ? y : x), qi = best.qi, oi = qi + 1, on = best.on;
  const stem = L.slice(best.a, qi + 1).filter(l => l !== '§Q§').join(' ');
  const rawOpts = L.slice(oi, oi + on);
  let opts = rawOpts.map(optLine);
  // Passmed glues the answer percentages onto each option ("…GIP50%"): strip them when every option has one
  if (opts.every(o => /\d{1,3}(\.\d)?%$/.test(o))) opts = opts.map(o => o.replace(/\s*\d{1,3}(\.\d)?%$/, '').trim());
  const after = L.slice(oi + on).filter(l => l !== '§Q§');
  const norm = s => s.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();
  const which = v => { const n = norm(v); let k = opts.findIndex(o => norm(o) === n); if (k < 0) k = opts.findIndex(o => norm(o).length >= 4 && n.startsWith(norm(o))); return k; };
  let correct = -1, picked = -1;
  rawOpts.forEach((l, k) => { if (/[✓✔]\s*$|\bcorrect\b/i.test(l) && !/\bincorrect\b/i.test(l)) correct = k; if (/[✗✘×]\s*$|\byour answer\b|\bincorrect\b/i.test(l)) picked = k; });
  const txt = after.join('\n');
  if (correct < 0) { // Passmed: "<option> is correct."
    for (const l of after) { const m = l.match(/^(.{3,140}?) is (?:the )?correct\b/i); if (m) { const k = which(m[1]); if (k >= 0) { correct = k; break; } } }
  }
  const mC = txt.match(/(?:the )?correct answer(?: is|:)\s*([A-E1-5](?=[).:\s]|$)|[^\n.]{3,90})/i);
  if (correct < 0 && mC) { const v = mC[1].trim(); correct = /^[A-E1-5]$/i.test(v) ? 'ABCDE12345'.indexOf(v.toUpperCase()) % 5 : which(v); }
  const mP = txt.match(/you (?:answered|chose|selected|picked)(?: option)?:?\s*([A-E1-5](?=[).:\s]|$)|[^\n.]{3,90})/i);
  if (picked < 0 && mP) { const v = mP[1].trim(); picked = /^[A-E1-5]$/i.test(v) ? 'ABCDE12345'.indexOf(v.toUpperCase()) % 5 : which(v); }
  if (correct < 0 && after.length) correct = which(after[0]);
  const expl = after.filter(l => !/correct answer|you (answered|chose|selected|picked)/i.test(l) && !LINKY.test(l)).join(' ').slice(0, 1800);
  return {stem: stem.slice(0, 1500), opts, correct, picked: picked === correct ? -1 : picked, expl, ok: opts.length >= 4};
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

/* ----- the AI remix ----- */
function rmxPrompt(q, target){
  const L = q.opts.map((o, i) => (i + 1) + '. ' + o).join('\n');
  return 'You turn a UK medical-school single-best-answer question that a student got wrong into a fast "change one thing" drill. UK practice only (NICE, BNF, Resus Council UK). Be medically accurate; if a change would be doubtful, pick a simpler, textbook one.\n\n'
    + 'QUESTION:\n' + q.stem + '\n\nOPTIONS:\n' + L + '\n\nCORRECT: ' + (q.correct + 1) + '. ' + q.opts[q.correct]
    + '\nSTUDENT PICKED: ' + (q.picked >= 0 ? (q.picked + 1) + '. ' + q.opts[q.picked] : 'not given')
    + (q.expl ? '\n\nEXPLANATION FROM THE QUESTION BANK (treat as correct):\n' + q.expl.slice(0, 1500) : '')
    + '\n\nReply with ONLY this JSON, every value one short line in plain words, no paragraphs:\n'
    + '{"film":"the case in at most 18 words: age/sex + main problem + the clue that decides it",'
    + '"right":"at most 14 words: why ' + (q.correct + 1) + ' is right",'
    + '"wrong":"at most 14 words: why ' + (q.picked >= 0 ? (q.picked + 1) : 'the strongest wrong option') + ' is wrong",'
    + '"flip":{"change":"at most 14 words: ONE changed clinical feature that makes option ' + (target + 1) + ' the answer; the rest of the case stays the same","answer":' + (target + 1) + ',"why":"at most 16 words"},'
    + '"twist":{"change":"at most 12 words: same diagnosis, one change to the patient (pregnant, eGFR under 30, allergy, unstable, first-line failed, on a DOAC...)","options":["4 management or investigation options, at most 8 words each"],"answer":1,"why":"at most 16 words"},'
    + '"time":{"speed":"sudden|comes and goes|fluctuates|gradual","change":"at most 14 words: same body area, a different time course","options":["4 diagnoses, at most 6 words each"],"answer":1,"why":"at most 16 words"}}\n'
    + 'Rules: "answer" values are 1-based. In "flip", if option ' + (target + 1) + ' cannot be made right by one change, use another wrong option and give its number. Twist and time must each have exactly one right option.';
}
function rmxShuffle4(b){ const idx = shuffle([0, 1, 2, 3], Math.random); return {opts: idx.map(i => b.options[i]), ans: idx.indexOf(b.answer)}; }
function rmxFromAi(q, j){
  const s1 = v => String(v == null ? '' : v).replace(/\s+/g, ' ').trim().slice(0, 220);
  const beats = [];
  if (j.flip && j.flip.change) { const a = (+j.flip.answer || 0) - 1; if (a >= 0 && a < q.opts.length) beats.push({k: 'flip', change: s1(j.flip.change), opts: q.opts.slice(), ans: a, why: s1(j.flip.why)}); }
  ['twist', 'time'].forEach(k => { const b = j[k]; if (!b || !b.change || !Array.isArray(b.options) || b.options.length !== 4) return; const a = (+b.answer || 0) - 1; if (a < 0 || a > 3) return; const sh = rmxShuffle4({options: b.options.map(s1), answer: a}); beats.push({k, change: s1(b.change), spd: k === 'time' ? s1(b.speed) : '', opts: sh.opts, ans: sh.ans, why: s1(b.why)}); });
  if (beats.length < 2) throw {code: 'invalid_json', message: 'incomplete remix'};
  return {film: s1(j.film), right: s1(j.right), wrong: s1(j.wrong), beats};
}

/* ----- offline remix: match the options to your ILO units and quiz their clinchers ----- */
function rmxLocal(q){
  const units = q.opts.map(o => rmxUnitFor(o));
  const optKeys = q.opts.map(o => rmxNorm(o).split(' ').filter(w => w.length >= 5 && !RMX_GEN.test(w)));
  // which options does a clincher talk about? (whole option text, or its distinctive words)
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
  const beats = [], usedU = new Set(), usedA = new Set();
  shuffle(cands, Math.random).forEach(c => {
    if (beats.length >= 3 || usedA.has(c.ans) || usedU.has(c.ui + ':' + c.ans)) return;
    usedA.add(c.ans); usedU.add(c.ui + ':' + c.ans);
    let txt = snpMask(dxStrip(CLK[c.ci][1]), UNITS[c.ui]);
    q.opts.forEach(o => { txt = snpMask(txt, {name: o}); });
    beats.push({k: 'ck', change: txt, opts: q.opts.slice(), ans: c.ans, why: CLK[c.ci][1]});
  });
  const words = q.stem.replace(/\s+/g, ' ').split(' ');
  return {film: words.slice(0, 28).join(' ') + (words.length > 28 ? '…' : ''), right: '', wrong: '', beats, units};
}

/* ----- view ----- */
let rmx = {step: 'home', q: null, card: null, i: 0, pick: null, busy: false, ctl: null, err: '', missOnly: false, queue: null};
const RMX_BEAT = {flip: ['🔄', 'Change one clue', 'If instead'], twist: ['🧍', 'Change the patient', 'Now'], time: ['⏱', 'Change the timeline', 'Now'], ck: ['🔑', 'Whose clincher is this?', 'Clincher']};
function viewRemix(m){
  m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🔄 Remix</span><span class="grow"></span><span class="mono" id="rmxN"></span></div><h1>Remix a question you got wrong</h1><p class="hint" style="margin:0">Copy the Passmedicine page (⌘A then ⌘C), come here and press ⌘V. You get the case in one line, then the same question three ways with <b>one thing changed</b> each time. Answer with <span class="kbd">1</span>–<span class="kbd">5</span>, <span class="kbd">Enter</span> for next.</p></div><div id="rmx" class="panel"></div><div id="rmxVault"></div></div>';
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
    h += '<textarea id="rmxIn" class="rmx-in" rows="4" placeholder="Paste the question here (or press ⌘V / Ctrl+V anywhere on this page)." aria-label="Paste a question"></textarea>'
      + '<div class="toolbar"><button class="btn primary" data-rmxpaste>📋 Paste</button><button class="btn" data-rmxgo>Use this text →</button><span class="grow"></span><span id="rmxStat" class="rmx-stat">' + rmxStatusHtml() + '</span></div>';
  } else if (rmx.step === 'check') {
    const q = rmx.q;
    h += '<div class="snp-lab">Check it (2 taps)</div><div class="rmx-stem">' + esc(q.stem) + '</div>';
    if (q.opts.length < 4) h += '<div class="kl kl-out"><span class="ki">⚠️</span><span>I couldn\'t find the 5 options. Copy the whole question page, or paste the stem with one option per line.</span></div>';
    else h += '<p class="hint" style="margin:0">Tap <b>✅</b> on the right answer and <b>✋</b> on the one you picked.</p><div class="rmx-opts">' + q.opts.map((o, k) => '<div class="rmx-opt' + (k === q.correct ? ' ok' : '') + (k === q.picked ? ' me' : '') + '"><span class="k">' + (k + 1) + '</span><span class="t">' + esc(o) + '</span><button class="iconbtn" data-rmxc="' + k + '" aria-label="Right answer" aria-pressed="' + (k === q.correct) + '">✅</button><button class="iconbtn" data-rmxp="' + k + '" aria-label="My pick" aria-pressed="' + (k === q.picked) + '">✋</button></div>').join('') + '</div>';
    if (rmx.err) h += '<div class="kl kl-out"><span class="ki">⚠️</span><span>' + esc(rmx.err) + '</span></div>';
    const ready = q.opts.length >= 4 && q.correct >= 0;
    h += '<div class="toolbar">' + (rmx.busy ? '<span class="rmx-busy">Thinking…</span><button class="btn" data-rmxstop>Stop</button>' : (RMX_AI ? '<button class="btn primary" data-rmxai' + (ready ? '' : ' disabled') + '>🔄 Remix <span class="kbd">Enter</span></button><button class="btn" data-rmxlocal' + (ready ? '' : ' disabled') + '>Offline remix</button>' : '<button class="btn primary" data-rmxlocal' + (ready ? '' : ' disabled') + '>🔄 Remix offline <span class="kbd">Enter</span></button>') + '<button class="btn ghost" data-rmxreset>Start again</button>') + '<span class="grow"></span>' + rmxStatusHtml() + '</div>';
  } else if (rmx.step === 'card') h += rmxCardHtml();
  box.innerHTML = h;
}
function rmxCardHtml(){
  const C = rmx.card, c = C.c, i = rmx.i, total = c.beats.length;
  let h = '<div class="qmeta"><span class="code">' + (rmx.queue ? '🔁 Replay ' + (rmx.queue.pos + 1) + ' / ' + rmx.queue.list.length : '🔄 Remix') + '</span>' + (C.src === 'local' ? '<span class="code">📴 offline</span>' : '<span class="code" title="Written by AI from your question: check it against the explanation">🤖 AI</span>') + '<span class="grow"></span><span class="mono">' + C.res.map(r => r == null ? '·' : r ? '✅' : '❌').join(' ') + '</span><button class="btn ghost rmx-out" data-rmxreset title="Back to pasting (Esc). You can also just press ⌘V here.">' + (rmx.queue ? '⏹ Stop replay' : '📋 New question') + ' <span class="kbd">Esc</span></button></div>';
  h += '<div class="rmx-case"><div class="snp-lab">① What happened</div><div class="stem snp-clue">🎬 ' + esc(c.film || C.q.stem.slice(0, 160)) + '</div>';
  if (c.right) h += '<div class="kl kl-in"><span class="ki">✅</span><span><b>' + esc(C.q.opts[C.q.correct]) + '</b>: ' + esc(c.right) + '</span></div>';
  if (c.wrong) h += '<div class="kl kl-out"><span class="ki">❌</span><span>' + (C.q.picked >= 0 ? '<b>' + esc(C.q.opts[C.q.picked]) + '</b>: ' : '') + esc(c.wrong) + '</span></div>';
  const us = [...new Set([C.unit].concat(c.units || []).filter(x => x != null && x >= 0))].slice(0, 4);
  if (us.length) h += '<div class="chips">' + us.map(ui => UNITS[ui] ? '<button class="chip" data-u="' + ui + '" data-mode="read">📖 ' + esc(UNITS[ui].name) + '</button>' : '').join('') + '</div>';
  h += '</div>';
  if (!total) return h + '<p class="hint">Not enough of these options are in your ILO units to build an offline quiz. Turn the AI on for a full remix.</p><div class="toolbar"><button class="btn primary" data-rmxnext>Done <span class="kbd">Enter</span></button></div>';
  if (i < total) {
    const b = c.beats[i], B = RMX_BEAT[b.k], tag = b.k === 'time' && b.spd ? ' · ' + esc(b.spd) : '';
    h += '<div class="snp-lab">' + '②③④⑤'[i] + ' ' + B[0] + ' ' + B[1] + tag + '</div><div class="rmx-chg"><b>' + B[2] + ':</b> ' + (b.k === 'ck' ? snpHtml(b.change) : esc(b.change)) + '</div>';
    h += '<div class="opts">' + b.opts.map((o, k) => { let cl = 'opt'; if (rmx.pick != null) { if (k === b.ans) cl += ' right'; else if (k === rmx.pick) cl += ' wrong'; } return '<button class="' + cl + '" data-rmxa="' + k + '"' + (rmx.pick != null ? ' disabled' : '') + '><span class="k">' + (k + 1) + '</span><span>' + esc(o) + '</span></button>'; }).join('') + '</div>';
    if (rmx.pick != null) h += '<div class="kl ' + (rmx.pick === b.ans ? 'kl-in' : 'kl-out') + '"><span class="ki">' + (rmx.pick === b.ans ? '✅' : '❌') + '</span><span>' + (b.k === 'ck' ? fmtRich(b.why) : esc(b.why)) + '</span></div><div class="toolbar"><button class="btn primary" data-rmxnext>' + (i + 1 < total ? 'Next' : 'Finish') + ' <span class="kbd">Enter</span></button></div>';
  } else {
    const got = C.res.filter(Boolean).length;
    h += '<div class="snp-end"><b>' + got + ' / ' + total + (rmx.queue ? '' : ' · saved to your Remix vault') + '</b><div class="toolbar">' + (rmx.queue ? '<button class="btn primary" data-rmxnext>' + (rmx.queue.pos + 1 < rmx.queue.list.length ? 'Next card' : 'Finish replay') + ' <span class="kbd">Enter</span></button>' : '<button class="btn primary" data-rmxreset>📋 Paste another <span class="kbd">Enter</span></button>') + '</div></div>';
  }
  return h;
}
function drawRmxVault(){
  const box = $('#rmxVault'); if (!box) return;
  const all = rmxAll(), miss = all.filter(c => c.res.some(r => r === false));
  if (!all.length) { box.innerHTML = ''; return; }
  const list = rmx.missOnly ? miss : all;
  box.innerHTML = '<div class="panel"><div class="toolbar"><b class="grow">🗂 Remix vault · ' + all.length + '</b><button class="btn primary" data-rmxreplay>🔁 Replay ' + list.length + '</button><button class="btn' + (rmx.missOnly ? ' primary' : '') + '" data-rmxmiss>♻️ Only misses · ' + miss.length + '</button><button class="btn ghost" data-rmxexport>⬇️ Export</button><button class="btn ghost" data-rmxclear>🗑 Clear</button></div>'
    + '<div class="rmx-list">' + list.slice(0, 30).map(c => '<button class="rmx-item" data-rmxopen="' + c.id + '"><span class="t">' + esc(c.c.film || c.q.stem.slice(0, 120)) + '</span><span class="hint">' + c.res.map(r => r == null ? '·' : r ? '✅' : '❌').join('') + ' · ' + new Date(c.ts).toLocaleDateString('en-GB') + '</span></button>').join('') + (list.length > 30 ? '<p class="hint">…and ' + (list.length - 30) + ' older</p>' : '') + '</div></div>';
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
  rmx = Object.assign(rmx, {step: 'check', q, card: null, i: 0, pick: null, err: '', queue: null});
  drawRemix();
}
function rmxMake(c, src){
  const q = rmx.q, card = {id: 'rx' + Date.now().toString(36) + Math.random().toString(36).slice(2, 5), ts: Date.now(), src, q: {stem: q.stem, opts: q.opts, correct: q.correct, picked: q.picked}, unit: rmxUnitFor(q.opts[q.correct]), c, res: c.beats.map(() => null)};
  rmxAll().unshift(card); rmxCards = rmxCards.slice(0, RMX_MAX); rmxSave();
  rmx = Object.assign(rmx, {step: 'card', card, i: 0, pick: null, busy: false, err: ''});
  drawRemix(); drawRmxVault();
}
async function rmxRunAi(){
  const q = rmx.q; if (!RMX_AI || rmx.busy || q.correct < 0) return;
  const others = q.opts.map((_, k) => k).filter(k => k !== q.correct);
  const target = q.picked >= 0 && q.picked !== q.correct && Math.random() < 0.6 ? q.picked : others[Math.floor(Math.random() * others.length)];
  rmx.busy = true; rmx.err = ''; rmx.ctl = new AbortController(); drawRemix();
  try {
    const j = await RMX_AI.json(rmxPrompt(q, target), {modelTier: S.set.rmxTier === 'default' ? 'default' : 'quick', maxTokens: 2000, signal: rmx.ctl.signal, cache: false});
    rmxMake(rmxFromAi(q, j), 'ai');
  } catch (e) {
    rmx.busy = false;
    const code = e && e.code;
    if (code === 'cancelled') { drawRemix(); return; }
    if (code === 'sign_in_required' && window.medengineAccount) window.medengineAccount.open(code);
    if (['not_granted', 'sampling_disabled', 'not_declared', 'capability_disabled', 'capability_removed'].includes(code)) RMX_AI = null;
    rmx.err = ({invalid_json: 'The AI reply came back garbled. Try again, or use the offline remix.', rate_limited: 'Too many requests just now. Wait a minute, or use the offline remix.', sign_in_required: 'Add your AI key first (🔑), or use the offline remix.', not_granted: 'AI isn\'t allowed on this page, so here is the offline remix.', refused: 'The AI declined this one. Use the offline remix.'})[code] || ((e && e.message) || 'The AI could not answer. Try again, or use the offline remix.');
    drawRemix();
  }
}
function rmxAnswer(k){
  if (rmx.step !== 'card' || rmx.pick != null) return;
  const C = rmx.card, b = C.c.beats[rmx.i]; if (!b || k >= b.opts.length) return;
  rmx.pick = k; C.res[rmx.i] = k === b.ans;
  if (C.res[rmx.i]) addXp(5);
  rmxSave(); drawRemix();
}
function rmxNext(){
  if (rmx.step !== 'card') return;
  const C = rmx.card, total = C.c.beats.length;
  if (rmx.i < total) { if (rmx.pick == null) return; rmx.i++; rmx.pick = null; return drawRemix(); }
  if (rmx.queue) { rmx.queue.pos++; if (rmx.queue.pos < rmx.queue.list.length) return rmxPlay(rmx.queue.list[rmx.queue.pos], rmx.queue); rmx.queue = null; toast('🔁 Replay done'); }
  rmx.step = 'home'; rmx.card = null; drawRemix(); drawRmxVault();
}
function rmxPlay(card, queue){
  card.res = card.c.beats.map(() => null);
  rmx = Object.assign(rmx, {step: 'card', card, i: 0, pick: null, queue: queue || null});
  drawRemix(); const b = $('#rmx'); if (b) b.scrollIntoView({block: 'start'});
}
function rmxReplay(){
  const list = (rmx.missOnly ? rmxAll().filter(c => c.res.some(r => r === false)) : rmxAll()).filter(c => c.c.beats.length);
  if (!list.length) return toast('Nothing to replay');
  rmxPlay(list[0], {list: list.slice(), pos: 0});
}
async function rmxExport(){
  const data = JSON.stringify({app: 'medengine-STUDY', kind: 'remix-vault', exported: new Date().toISOString(), cards: rmxAll()}, null, 1), name = 'medengine-remix-vault-' + new Date().toISOString().slice(0, 10) + '.json';
  let dl = null; try { if (window.claude && claude.use) dl = await claude.use('downloads'); } catch (e) {}
  if (dl) { try { await dl.save({filename: name, data: new Blob([data], {type: 'application/json'})}); return; } catch (e) { if (e && e.code === 'declined') return; } }
  try { const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([data], {type: 'application/json'})); a.download = name; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); } catch (e) { toast('Export is not available here'); }
}
async function rmxPasteBtn(){
  try { const t = await navigator.clipboard.readText(); if (t && t.trim()) return rmxIngest(t); } catch (e) {}
  const el = $('#rmxIn'); if (el) el.focus(); toast('Long-press the box and tap Paste (or press ⌘V)');
}
document.addEventListener('paste', e => {
  if (route.view !== 'remix') return;
  const tg = e.target;
  if (tg && (tg.tagName === 'INPUT' || (tg.tagName === 'TEXTAREA' && tg.id !== 'rmxIn') || tg.isContentEditable)) return;
  const t = e.clipboardData && e.clipboardData.getData('text/plain');
  if (!t || t.trim().length < 30) { if (e.clipboardData && Array.from(e.clipboardData.items || []).some(i => i.kind === 'file')) { e.preventDefault(); toast('That\'s an image: paste images on a condition page (📋 Paste exam image)'); } return; }
  e.preventDefault(); rmxIngest(t);
});
function rmxKey(e){
  if (route.view !== 'remix') return false;
  const k = e.key;
  if (rmx.step === 'check' && k === 'Enter' && !rmx.busy && rmx.q.correct >= 0 && rmx.q.opts.length >= 4) { e.preventDefault(); RMX_AI ? rmxRunAi() : rmxMake(rmxLocal(rmx.q), 'local'); return true; }
  if (k === 'Escape' && rmx.step !== 'home') { e.preventDefault(); rmxHome(); return true; }
  if (rmx.step !== 'card') return false;
  const C = rmx.card;
  if (/^[1-5]$/.test(k) && rmx.i < C.c.beats.length) { e.preventDefault(); rmxAnswer(+k - 1); return true; }
  if (k === 'Enter' || k === ' ' || k === 'ArrowRight') {
    if (rmx.i >= C.c.beats.length && !rmx.queue) { e.preventDefault(); rmxHome(); return true; }
    e.preventDefault(); rmxNext(); return true;
  }
  return k.toLowerCase() === 's';
}
document.addEventListener('keydown', e => { const tg = e.target; if (tg && (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || tg.isContentEditable) || e.metaKey || e.ctrlKey || e.altKey) return; if (rmxKey(e)) e.stopImmediatePropagation(); }, true);
function extClick8(t, d){
  if (d.spdset) { S.set.spd = S.set.spd === d.spdset ? '' : d.spdset; save(); renderSide(); if (route.view === 'home') render(); if (S.set.spd && matchMedia('(max-width:860px)').matches) document.body.classList.add('nav'); return true; }
  if (route.view !== 'remix') return false;
  if (d.rmxpaste != null) { rmxPasteBtn(); return true; }
  if (d.rmxgo != null) { const el = $('#rmxIn'); if (el && el.value.trim()) rmxIngest(el.value); else toast('Paste a question first'); return true; }
  if (d.rmxc != null) { rmx.q.correct = +d.rmxc; if (rmx.q.picked === rmx.q.correct) rmx.q.picked = -1; drawRemix(); return true; }
  if (d.rmxp != null) { const k = +d.rmxp; rmx.q.picked = rmx.q.picked === k || k === rmx.q.correct ? -1 : k; drawRemix(); return true; }
  if (d.rmxai != null) { rmxRunAi(); return true; }
  if (d.rmxlocal != null) { rmxMake(rmxLocal(rmx.q), 'local'); return true; }
  if (d.rmxstop != null) { if (rmx.ctl) rmx.ctl.abort(); return true; }
  if (d.rmxreset != null) { rmxHome(); return true; }
  if (d.rmxa != null) { rmxAnswer(+d.rmxa); return true; }
  if (d.rmxnext != null) { rmxNext(); return true; }
  if (d.rmxkey != null) { if (window.medengineAccount) window.medengineAccount.open(); return true; }
  if (d.rmxopen) { const c = rmxAll().find(x => x.id === d.rmxopen); if (c) rmxPlay(c, null); return true; }
  if (d.rmxreplay != null) { rmxReplay(); return true; }
  if (d.rmxmiss != null) { rmx.missOnly = !rmx.missOnly; drawRmxVault(); return true; }
  if (d.rmxexport != null) { rmxExport(); return true; }
  if (d.rmxclear != null) { if (!t.dataset.armed) { t.dataset.armed = '1'; t.textContent = 'Tap again to delete all'; return true; } rmxCards = []; rmxSave(); drawRmxVault(); drawRemix(); toast('Remix vault cleared'); return true; }
  return false;
}
try { Object.defineProperty(window, '__me8', {value: Object.freeze({rmxParse, rmxUnitFor, rmxFromAi, rmxLocal, get rmx(){ return rmx; }, rmxAll: () => rmxAll(), setAi(f){ RMX_AI = f; }})}); } catch (e) {}
