/* ===================== v3.3.0 ===================== */

/* ---------- 🧬 Mnemonics: every frame, exam and procedure, each with why and when not to ---------- */
const MNK = {acr: ['🔤', 'Letters'], loci: ['🧍', 'Route'], rule: ['🎵', 'Rule'], num: ['🔢', 'Numbers'], chunk: ['🧩', 'Groups'], story: ['🎬', 'Picture'], none: ['⛔', 'No mnemonic']};
const mnById = {}; MN.list.forEach(m => { mnById[m.id] = m; });
let mnState = {quiz: false, rev: new Set(), form: '', q: '', k: ''};
function mnMine(stId){ S.myMn = S.myMn || {}; return (S.myMn[stId] || []).filter(m => m && m.id); }
function mnIdsFor(st){
  if (!st) return [];
  const ids = [], add = arr => (arr || []).forEach(id => { if (mnById[id] && !ids.includes(id)) ids.push(id); });
  mnMine(st.id).forEach(m => { mnById[m.id] = Object.assign({}, m, {st: st.id, custom: 1}); ids.push(m.id); });
  (st.mn || []).forEach(m => { if (m && m.id) { mnById[m.id] = m; if (!ids.includes(m.id)) ids.push(m.id); } });
  const sid = String(st.id || '');
  if (/^E-/.test(sid)) add(MN.map.exam[sid.slice(2)]);
  if (/^P-/.test(sid)) add(MN.map.proc[sid.slice(2)]);
  (st.ex || []).forEach(e => add(MN.map.exam[e]));
  (st.pr || []).forEach(p => add(MN.map.proc[p]));
  add(MN.map.type[typeOf(st)]);
  (st.fr || []).forEach(f => add(MN.map.frame[f]));
  (st.wrap || []).forEach(f => add(MN.map.frame[f]));
  add(MN.map.frame.open);
  return ids;
}
function mnItemHtml(m, ctx){
  if (!m) return '';
  const kk = MNK[m.k] || MNK.acr, key = ctx + ':' + m.id, q = mnState.quiz;
  let h = '<div class="mn-item' + (m.k === 'none' ? ' mn-none' : '') + '"><div class="mn-hd"><span class="mn-k" title="' + kk[1] + '">' + kk[0] + ' ' + kk[1] + '</span><b class="mn-code">' + esc(m.code) + '</b>'
    + (m.mine ? '<span class="mn-tag">yours</span>' : '') + (m.custom ? '<span class="mn-tag">custom</span>' : '') + '<span class="mn-t">' + esc(m.t) + '</span></div>';
  if (m.L && m.L.length) h += '<div class="mn-letters">' + m.L.map((x, i) => { const hid = q && !mnState.rev.has(key + ':' + i); return '<button type="button" class="mn-l' + (hid ? ' hid' : '') + '" data-mnrev="' + esc(key + ':' + i) + '"><b>' + esc(x[0]) + '</b><span>' + (hid ? 'tap to reveal' : esc(x[1])) + '</span></button>'; }).join('') + '</div>';
  if (m.line) h += q && !mnState.rev.has(key + ':line') ? '<button type="button" class="mn-l hid mn-lineq" data-mnrev="' + esc(key + ':line') + '"><span>🎵 tap to reveal the line</span></button>' : '<div class="mn-line">' + esc(m.line) + '</div>';
  h += '<details class="mn-why"><summary>💡 Why this works, and when not to</summary><div><b>Why:</b> ' + esc(m.why || '') + '</div>' + (m.no ? '<div><b>Watch out:</b> ' + esc(m.no) + '</div>' : '') + '</details>';
  if (m.custom) h += '<button type="button" class="btn sm ghost" data-mndel="' + esc(m.id) + '" data-mnst="' + esc(m.st || '') + '">🗑 Delete</button>';
  return h + '</div>';
}
function mnFormHtml(stId){
  return '<div class="mn-form"><input id="mnCode" maxlength="24" placeholder="Your code, e.g. TAGBS-P"><input id="mnFor" maxlength="60" placeholder="What it is for, e.g. venepuncture tray">'
    + '<textarea id="mnLetters" rows="3" placeholder="One per line: T = Tourniquet&#10;A = Alcohol wipe"></textarea><input id="mnLine" maxlength="160" placeholder="Optional one-line hook">'
    + '<div class="row" style="gap:6px"><button type="button" class="btn sm primary" data-mnsave="' + esc(stId) + '">💾 Save to this station</button><button type="button" class="btn sm" data-mnadd="">Cancel</button></div></div>';
}
function mnCardHtml(st){
  const ids = mnIdsFor(st); if (!ids.length) return '';
  return '<details class="hk mn-card" id="mnCard"' + (S.set.mnOpen ? ' open' : '') + '><summary>🧬 Mnemonics (' + ids.length + ')</summary><div class="body">'
    + '<div class="row mn-tools"><button type="button" class="btn sm' + (mnState.quiz ? ' primary' : '') + '" data-mnquiz>🙈 Quiz letters</button><button type="button" class="btn sm" data-mnreset>↺ Reset</button><button type="button" class="btn sm" data-mnadd="' + esc(st.id) + '">＋ My mnemonic</button><span class="grow"></span><a class="btn sm ghost" href="#mn">All mnemonics →</a></div>'
    + (mnState.form === st.id ? mnFormHtml(st.id) : '')
    + ids.map(id => mnItemHtml(mnById[id], st.id)).join('') + '</div></details>';
}
function mnRedraw(){
  if (route.v === 'mn') return vMn($('#main'));
  const w = $('#mnWrap'); if (w && cur && cur.st) { const open = !!($('#mnCard') && $('#mnCard').open); w.innerHTML = mnCardHtml(cur.st); const c = $('#mnCard'); if (c && open) c.open = true; }
}
function mnWhere(){
  if (mnWhere.c) return mnWhere.c;
  const where = {};
  [['frame'], ['exam'], ['proc'], ['type']].forEach(([g]) => Object.values(MN.map[g] || {}).forEach(arr => arr.forEach(id => { if (!where[id]) where[id] = g === 'type' ? 'frame' : g; })));
  return mnWhere.c = where;
}
function mnListHtml(){
  const where = mnWhere(), q = (mnState.q || '').toLowerCase().trim(), kf = mnState.k;
  const mine = [].concat(...Object.entries(S.myMn || {}).map(([sid, arr]) => (arr || []).map(x => Object.assign({}, x, {st: sid, custom: 1}))));
  const pass = x => (!kf || x.k === kf) && (!q || (x.code + ' ' + x.t + ' ' + (x.line || '') + ' ' + (x.L || []).map(l => l.join(' ')).join(' ')).toLowerCase().includes(q));
  let h = '';
  const Lm = mine.filter(pass); if (Lm.length) h += '<section class="card"><h2>✍️ Yours · ' + Lm.length + '</h2>' + Lm.map(x => mnItemHtml(x, 'hub')).join('') + '</section>';
  [['frame', '🧠 Every station: frameworks'], ['exam', '🩺 Examinations'], ['proc', '🧪 Procedures']].forEach(([g, title]) => {
    const L = MN.list.filter(x => (where[x.id] || 'frame') === g && pass(x));
    if (L.length) h += '<section class="card"><h2>' + title + ' · ' + L.length + '</h2>' + L.map(x => mnItemHtml(x, 'hub')).join('') + '</section>';
  });
  return h || '<section class="card"><div class="empty">No mnemonics match.</div></section>';
}
function vMn(m){
  const head = '<section class="card"><span class="eyebrow">medengine-OSCE · ' + MN.list.length + ' mnemonics</span><h1>🧬 Mnemonics</h1><p class="hint" style="margin:0">Every framework, examination and procedure, with <b>why</b> each memory aid fits it, and <b>when a mnemonic would hurt</b>. Open any station to see its own set.</p>'
    + '<details class="dd" id="mnPrimer"' + (S.set.mnPrimer === false ? '' : ' open') + '><summary>💡 ' + esc(MN.primer.t) + '</summary><div class="body">' + MN.primer.pts.map(p => '<div class="mn-pr"><b>' + esc(p[0]) + ':</b> ' + esc(p[1]) + '</div>').join('') + '</div></details>'
    + '<div class="row mn-tools"><input class="sel" id="mnQ" type="search" placeholder="Search: tray, cranial, risk…" value="' + esc(mnState.q) + '" style="flex:1;min-width:160px"><select class="sel" id="mnK"><option value="">All kinds</option>' + Object.entries(MNK).map(([k, v]) => '<option value="' + k + '"' + (mnState.k === k ? ' selected' : '') + '>' + v[0] + ' ' + v[1] + '</option>').join('') + '</select>'
    + '<button type="button" class="btn sm' + (mnState.quiz ? ' primary' : '') + '" data-mnquiz>🙈 Quiz letters</button><button type="button" class="btn sm" data-mnreset>↺ Reset</button></div></section>';
  m.innerHTML = head + '<div id="mnList">' + mnListHtml() + '</div>';
}

/* ---------- 🔒 My circuit: your private stations, encrypted on this device ---------- */
// Nothing exam-specific ships in this file. You import a pack once, choose a password, and the
// pack is sealed with AES-GCM (key from PBKDF2-SHA256, 600,000 rounds). Only the sealed copy is
// stored; the plaintext lives in memory while unlocked and is gone when you lock or reload.
const MY_KEY = 'medengine-private-v1', MY_ITER = 600000;
const MY = {pack: null, pending: null, msg: '', armDel: false, hiddenAt: 0};
function myB64(buf){ const a = new Uint8Array(buf); let s = ''; for (let i = 0; i < a.length; i += 0x8000) s += String.fromCharCode.apply(null, a.subarray(i, i + 0x8000)); return btoa(s); }
function myUnB64(s){ const b = atob(s), a = new Uint8Array(b.length); for (let i = 0; i < b.length; i++) a[i] = b.charCodeAt(i); return a; }
async function myDerive(pass, salt, iter){
  const base = await crypto.subtle.importKey('raw', new TextEncoder().encode(pass), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey({name: 'PBKDF2', hash: 'SHA-256', salt, iterations: iter}, base, {name: 'AES-GCM', length: 256}, false, ['encrypt', 'decrypt']);
}
async function mySeal(pack, pass){
  const salt = crypto.getRandomValues(new Uint8Array(16)), iv = crypto.getRandomValues(new Uint8Array(12));
  const key = await myDerive(pass, salt, MY_ITER);
  const ct = await crypto.subtle.encrypt({name: 'AES-GCM', iv}, key, new TextEncoder().encode(JSON.stringify(pack)));
  return {v: 1, kind: 'medengine-sealed', kdf: 'PBKDF2-SHA256', iter: MY_ITER, salt: myB64(salt), iv: myB64(iv), ct: myB64(ct), n: (pack.stations || []).length, ts: Date.now()};
}
async function myOpen(sealed, pass){
  const key = await myDerive(pass, myUnB64(sealed.salt), +sealed.iter || MY_ITER);
  const pt = await crypto.subtle.decrypt({name: 'AES-GCM', iv: myUnB64(sealed.iv)}, key, myUnB64(sealed.ct));
  return JSON.parse(new TextDecoder().decode(pt));
}
function mySealed(){ try { const s = JSON.parse(localStorage.getItem(MY_KEY) || 'null'); return s && s.kind === 'medengine-sealed' && s.ct ? s : null; } catch (e) { return null; } }
function myValid(p){ return p && p.kind === 'medengine-private-pack' && Array.isArray(p.stations) && p.stations.length && p.stations.every(s => s && /^MY\d{1,3}$/.test(s.id) && s.t && Array.isArray(s.secs)); }
function myLoad(pack){
  myUnload();
  MY.pack = pack;
  pack.stations.forEach(s => { s.my = 1; s.grp = s.grp || '🔒 My circuit'; s.u = s.u || []; s.fr = s.fr || []; s.ex = s.ex || []; s.pr = s.pr || []; s.wrap = s.wrap || ['open', 'close']; ST.push(s); stById[s.id] = s; });
}
function myUnload(){
  if (!MY.pack) return;
  MY.pack.stations.forEach(s => { const i = ST.indexOf(s); if (i >= 0) ST.splice(i, 1); if (stById[s.id] === s) delete stById[s.id]; });
  MY.pack = null;
}
function myLock(){ myUnload(); MY.msg = '🔒 Locked.'; if (route.v === 'station' && /^MY/.test(route.id || '')) location.hash = 'my'; else if (route.v === 'my') vMy($('#main')); }
document.addEventListener('visibilitychange', () => {
  if (document.hidden) { MY.hiddenAt = Date.now(); return; }
  if (MY.pack && MY.hiddenAt && Date.now() - MY.hiddenAt > 15 * 60000) myLock();
});
function vMy(m){
  const sealed = mySealed(), ok = !!(window.crypto && crypto.subtle);
  let h = '<section class="card"><span class="eyebrow">Private · encrypted on this device</span><h1>🔒 My circuit</h1>';
  if (MY.msg) h += '<div class="alert">' + esc(MY.msg) + '</div>';
  if (!ok) h += '<div class="alert">This browser can\'t do encryption here (it needs https). Open your website copy instead.</div>';
  if (MY.pack) {
    h += '<p class="hint" style="margin:0">Unlocked until you lock it, reload, or leave the app for 15 minutes.</p><div class="list">' + MY.pack.stations.map(s => '<button class="li" data-st="' + esc(s.id) + '"><span class="code ty">' + (TY[typeOf(s)] ? TY[typeOf(s)].i : '🔒') + '</span><span class="tt"><b>' + esc(s.t) + '</b><span class="hint">' + esc(s.sub || s.info || '').slice(0, 120) + '</span></span><span class="score ' + scoreCls(best(s.id)) + '">' + (best(s.id) != null ? best(s.id) + '%' : 'new') + '</span></button>').join('') + '</div>'
      + '<div class="row" style="gap:6px;margin-top:10px;flex-wrap:wrap"><button class="btn primary" data-mylock>🔒 Lock now</button>' + (window.MEDENGINE_ARTIFACT ? '' : '<button class="btn" data-myexport>📤 Save sealed copy (for another device)</button>') + '</div>';
  } else if (MY.pending) {
    h += '<p class="hint" style="margin:0">Pack read: <b>' + MY.pending.stations.length + ' stations</b>. Choose a password. It never leaves this device, and it can\'t be recovered if you forget it (you would import the file again).</p>'
      + '<div class="my-form"><input type="password" id="myP1" autocomplete="new-password" placeholder="Password (8+ characters)"><input type="password" id="myP2" autocomplete="new-password" placeholder="Same password again"><button class="btn primary" data-myseal>🔐 Encrypt and save</button><button class="btn" data-mycancel>Cancel</button></div>';
  } else if (sealed) {
    h += '<p class="hint" style="margin:0">Sealed pack on this device: <b>' + (+sealed.n || 0) + ' stations</b>. Enter your password to open it.</p>'
      + '<div class="my-form"><input type="password" id="myPw" autocomplete="current-password" placeholder="Password"><button class="btn primary" data-myopen>🔓 Unlock</button></div>'
      + '<details class="dd"><summary>More</summary><div class="body"><div class="row" style="gap:6px;flex-wrap:wrap">' + (window.MEDENGINE_ARTIFACT ? '' : '<button class="btn" data-myexport>📤 Save sealed copy</button>') + '<button class="btn" data-mydel>' + (MY.armDel ? '⚠️ Tap again to delete it from this device' : '🗑 Remove from this device') + '</button></div></div></details>';
  } else {
    h += '<p class="hint" style="margin:0">Import your private pack file (<b>.json</b>). It\'s encrypted with a password you choose, and only the encrypted copy is kept. Delete the file afterwards.</p>';
  }
  if (!MY.pack && !MY.pending) h += '<label class="btn" style="margin-top:10px">📥 Import a pack or a sealed copy<input type="file" id="myFile" accept=".json,application/json" hidden></label>';
  m.innerHTML = h + '</section>';
}
async function myHandleFile(file){
  try {
    const obj = JSON.parse(await file.text());
    if (obj && obj.kind === 'medengine-sealed' && obj.ct) { localStorage.setItem(MY_KEY, JSON.stringify(obj)); MY.msg = '✅ Sealed copy saved. Enter your password to unlock.'; }
    else if (myValid(obj)) { MY.pending = obj; MY.msg = ''; }
    else MY.msg = '⚠️ That file is not a medengine pack.';
  } catch (e) { MY.msg = '⚠️ Could not read that file.'; }
  vMy($('#main'));
}
async function mySealPending(){
  const p1 = ($('#myP1') || {}).value || '', p2 = ($('#myP2') || {}).value || '';
  if (p1.length < 8) { MY.msg = '⚠️ Use at least 8 characters.'; return vMy($('#main')); }
  if (p1 !== p2) { MY.msg = '⚠️ The passwords do not match.'; return vMy($('#main')); }
  MY.msg = '🔐 Encrypting…'; vMy($('#main'));
  try {
    const sealed = await mySeal(MY.pending, p1);
    localStorage.setItem(MY_KEY, JSON.stringify(sealed));
    myLoad(MY.pending); MY.pending = null;
    MY.msg = '✅ Encrypted and unlocked. You can delete the pack file now.';
  } catch (e) { MY.msg = '⚠️ Could not encrypt: ' + ((e && e.message) || 'storage may be full'); }
  vMy($('#main'));
}
async function myUnlock(){
  const sealed = mySealed(), pw = ($('#myPw') || {}).value || '';
  if (!sealed || !pw) return;
  MY.msg = '🔓 Unlocking…'; vMy($('#main'));
  try { const pack = await myOpen(sealed, pw); if (!myValid(pack)) throw new Error('bad pack'); myLoad(pack); MY.msg = ''; }
  catch (e) { MY.msg = '⚠️ Wrong password.'; }
  vMy($('#main'));
}
function myExport(){
  const s = localStorage.getItem(MY_KEY); if (!s) return;
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([s], {type: 'application/json'})); a.download = 'my-circuit.sealed.json'; a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 4000);
}

/* ---------- 🛡️ Safety and order checks for 📋 Grade ---------- */
// The examiner-sheet matcher looks for words. These checks add what words alone miss:
// order (tourniquet off before the needle comes out), things you must never do (resheathing),
// and negation for those ("I won't re-palpate" is not a re-palpation). Only true safety steps are
// critical (c): missing one caps the station at 54%, a borderline fail, as an examiner would.
const NEG_RX = /\b(?:not|never|didn'?t|did not|don'?t|do not|won'?t|will not|shan'?t|forgot to|without|skipped|wasn'?t|haven'?t)\s+(?:\S+\s+){0,2}$/i, NO_RX = /\bno\s+$/i;
function chkAll(text, rx, neg){
  const g = new RegExp(rx.source, rx.flags.includes('g') ? rx.flags : rx.flags + 'g'), out = [];
  let m;
  while ((m = g.exec(text))) {
    if (m[0] === '') { g.lastIndex++; continue; }
    if (neg) { const pre = text.slice(Math.max(0, m.index - 40), m.index); if (NEG_RX.test(pre) || NO_RX.test(pre)) continue; }
    out.push(m.index);
  }
  return out;
}
const CK = (t, o) => Object.assign({t}, o);
const ID_RX = [/\bname\b/, /date of birth|\bdob\b|birthday|wristband|hospital number|nhs number/];
const CHK = {
  venep: [
    CK('Two identifiers checked', {c: 1, all: ID_RX}),
    CK('Allergies asked (latex, plasters, chlorhexidine)', {all: [/allerg|latex|plaster/]}),
    CK('Arm to avoid asked (fistula, mastectomy side, drip)', {all: [/fistula|mastectomy|lymph|which arm|either arm|arm to avoid|avoid (this|that|either|an) arm|drip/]}),
    CK('Tourniquet on', {all: [/tourniquet/]}),
    CK('Cleaned 30 s and left to dry', {c: 1, all: [/chlorhexidine|alcohol (wipe|swab)|clean(ing)? (the )?(skin|site|area|arm)|swab|wipe/, /\b30\b|thirty|dry/]}),
    CK('Did not re-touch the cleaned site', {bad: /re-?palpat|feel (for )?(it|the vein) again|touch(ing)? (it|the (vein|site|skin)) again/, fix: 'Once cleaned, don\'t touch the site again; say "I won\'t re-palpate".'}),
    CK('Warned "sharp scratch"', {all: [/sharp scratch|small scratch|sharp prick|little prick|scratch/]}),
    CK('Order of draw kept', {draw: 1}),
    CK('Tourniquet off before the needle comes out', {c: 1, order: [/(releas\w*|loosen\w*|undo\w*|take off|taking off|let go of|remov\w*) (the )?tourniquet|tourniquet (off|released|loosened)/, /(remov\w*|withdraw\w*|take out|taking out|pull\w* out) (the )?needle|needle (out|removed|withdrawn|comes out)/], fix: 'Release the tourniquet BEFORE the needle comes out, or you cause a haematoma.'}),
    CK('Sharps straight into the bin, no resheathing', {c: 1, all: [/sharps/], bad: /re-?sheath|re-?cap|put the cap back/, fix: 'Never resheath; the needle goes straight into the sharps bin.'}),
    CK('Labelled at the bedside', {c: 1, all: [/label/, /bedside|at the bed|in front of (you|the patient)|by the bed|with the patient/]}),
    CK('Pressure, plaster and safety-net', {all: [/pressure|press|gauze|cotton wool|plaster/, /bleed|bruis|swell|let (me|someone|us|a nurse|the nurse) know|tell (me|a nurse)/]}),
  ],
  cann: [
    CK('Two identifiers checked', {c: 1, all: ID_RX}),
    CK('Allergies asked', {all: [/allerg/]}),
    CK('Cleaned 30 s and left to dry', {c: 1, all: [/chlorhexidine|alcohol|clean|swab|wipe/, /\b30\b|thirty|dry/]}),
    CK('Flashback, then advance a little and slide the cannula off', {all: [/flashback|flash back|blood in the chamber/, /advance|slide|feed/]}),
    CK('Tourniquet off before the needle comes out', {c: 1, order: [/(releas\w*|loosen\w*|undo\w*|take off|remov\w*) (the )?tourniquet|tourniquet (off|released)/, /(remov\w*|withdraw\w*|take out|pull\w* out) (the )?(needle|introducer|stylet)/]}),
    CK('Sharps straight into the bin', {c: 1, all: [/sharps/], bad: /re-?sheath|re-?cap/}),
    CK('Flushed with saline, watching for swelling or pain', {all: [/flush/, /saline|sodium chloride/]}),
    CK('Dressing dated and documented', {all: [/dressing|tegaderm/, /date|document|vip|label/]}),
  ],
  abg: [
    CK('Two identifiers checked', {c: 1, all: ID_RX}),
    CK("Collateral circulation checked (Allen's test)", {all: [/allen|collateral|ulnar/]}),
    CK('Heparinised syringe, air bubbles expelled', {all: [/heparin|blood gas syringe|abg syringe/, /bubble|expel|air out/]}),
    CK('Firm pressure for 3 to 5 minutes', {all: [/pressure/, /\b(3|5|three|five)\b.{0,10}minutes?/]}),
    CK('Sharps straight into the bin', {c: 1, all: [/sharps/], bad: /re-?sheath|re-?cap/}),
    CK('Oxygen noted and sample analysed within 10 minutes', {all: [/room air|litres|oxygen|fio2/, /analy[sz]|gas machine|ten minutes|10 minutes|straight away/]}),
  ],
  catheter: [
    CK('Consent and chaperone', {c: 1, all: [/chaperone/, /consent|is that (ok|okay|alright)|happy for me/]}),
    CK('Aseptic technique, sterile gloves', {all: [/aseptic|sterile/]}),
    CK('Lidocaine gel and a wait', {all: [/lidocaine|instillagel|anaesthetic gel|numbing gel/, /wait|minutes/]}),
    CK('Urine flows before the balloon goes up', {c: 1, order: [/urine (flow|comes|draining|starts)|see (the )?urine|urine in the (tube|catheter)/, /inflat\w*|balloon/], fix: 'Only inflate the balloon once urine is flowing; a balloon in the urethra causes serious injury.'}),
    CK('Balloon filled with sterile water to the stated volume', {all: [/sterile water|water for injection|\b10 ?ml\b|ten ml/]}),
    CK('Foreskin replaced (male)', {male: 1, c: 1, all: [/foreskin/, /back|replace|forward|reduce/], fix: 'Always replace the foreskin to prevent paraphimosis.'}),
    CK('Bag attached and secured; residual volume documented', {all: [/bag/, /document|residual|volume|record/]}),
  ],
  inj: [
    CK('Two identifiers checked', {c: 1, all: ID_RX}),
    CK('Allergies asked', {all: [/allerg/]}),
    CK('Right site named', {all: [/deltoid|vastus|thigh|ventrogluteal|abdomen|tummy|upper arm/]}),
    CK('Right angle: 90° IM (stretch), 45° or 90° SC (pinch)', {all: [/\b(90|ninety|45|forty[- ]five)\b|pinch|stretch|bunch/]}),
    CK('Sharps straight into the bin', {c: 1, all: [/sharps/], bad: /re-?sheath|re-?cap/}),
    CK('Batch and expiry documented; observe for a reaction', {all: [/batch|expiry|document|record/, /reaction|observe|wait|stay|feel unwell|faint/]}),
  ],
  ecg12: [
    CK('Consent and a gown or chaperone offered', {all: [/consent|is that (ok|okay|alright)|happy for me/, /gown|chaperone|cover|dignity/]}),
    CK('Limb leads placed by colour or position', {all: [/\bred\b|right arm|right wrist/, /yellow|left arm|left wrist/, /green|left leg|left ankle/]}),
    CK('Chest lead landmarks named', {all: [/(4th|fourth) intercostal|(5th|fifth) intercostal|mid-?clavicular|axillary|sternal edge|v1|v4/]}),
    CK('Asked to lie still and relax', {all: [/still|relax|don'?t (talk|move)/]}),
    CK('Trace checked and labelled', {all: [/label|name|check (the )?(trace|ecg|calibration)|25 ?mm|10 ?mm/]}),
  ],
  transf: [
    CK('Positive ID: patient says their own name and date of birth', {c: 1, all: [/(what is|what'?s|can you tell me|could you tell me|confirm|say) (your )?(full )?name/, /date of birth|dob/], bad: /are you (mr|mrs|ms|miss)\b/, fix: 'Ask the patient to say their name and date of birth; never ask "Are you Mr…?".'}),
    CK('Wristband, prescription and blood label match', {c: 1, all: [/wristband/, /prescription|compatibility|label|unit|bag/]}),
    CK('Expiry, unit number and special requirements checked', {all: [/expir|unit number|irradiated|cmv|special requirement/]}),
    CK('Observations before and 15 minutes in', {c: 1, all: [/observation|\bobs\b|blood pressure|temperature|pulse/, /\b15\b|fifteen/]}),
    CK('Reaction safety-net', {all: [/fever|rigor|rash|itch|breath|back pain|feel unwell|tell (me|a nurse|someone)/]}),
  ],
  ngt: [
    CK('Measured nose, earlobe, xiphisternum', {all: [/nose|nostril|\bnex\b/, /ear/, /xiphi|sternum|breastbone/]}),
    CK('Swallowing sips as it passes', {all: [/swallow|sip/]}),
    CK('Aspirate pH checked (5.5 or below)', {c: 1, all: [/\bph\b|litmus|indicator paper/, /5\.5|five point five|aspirat/]}),
    CK('No "whoosh" test', {c: 1, bad: /whoosh|listen for (a )?(bubbl|whoosh)|(push|inject) air/, fix: 'The whoosh test is unsafe and must not be used; check pH, then X-ray if the pH is above 5.5.'}),
    CK('X-ray if pH is not confirming; tube secured and documented', {all: [/x-?ray|tape|secure|document/]}),
  ],
  pefr: [
    CK('Stands or sits upright', {all: [/stand|sit (up )?straight|upright/]}),
    CK('Pointer set to zero', {all: [/zero|reset|bottom of the scale/]}),
    CK('Deep breath, lips sealed', {all: [/deep breath|big breath|breathe in/, /seal|lips (tight )?around|tight/]}),
    CK('Short sharp blast', {all: [/short|sharp|fast|hard/, /blast|blow|huff/]}),
    CK('Best of three recorded and compared', {all: [/three|3 times|best of|highest/, /predicted|personal best|chart|record/]}),
  ],
  inhaler: [
    CK('Shake (MDI)', {all: [/shake/]}),
    CK('Breathe out first', {all: [/breathe out|exhale|empty your lungs/]}),
    CK('Lips sealed around the mouthpiece', {all: [/seal|lips (tight )?around/]}),
    CK('Press while starting a slow, deep breath', {all: [/press|push|actuat/, /slow|deep|breathe in/]}),
    CK('Hold the breath for 10 seconds', {all: [/hold/, /\b10\b|ten seconds/]}),
    CK('Rinse mouth (steroid) or spacer advice', {all: [/rinse|gargle|spacer/]}),
  ],
  abdo: [
    CK('Lying flat on one pillow', {all: [/(lie|lay|lying) (you )?(down )?flat|flat on (the|your) back|one pillow/]}),
    CK('Asked about pain before touching', {all: [/(any|in) pain|sore|tender/]}),
    CK('Started away from the pain', {all: [/away from|furthest from|start (on|at|with) the (other|opposite)|opposite side|other side/]}),
    CK('Watched the face while palpating', {all: [/(watch|look|looking|keep an eye) (at |on )?(your )?face/]}),
    CK('Light, then deep palpation', {all: [/light|gentl/, /deep/]}),
    CK('Liver, spleen and kidneys', {all: [/liver/, /spleen/, /kidney|ballot/]}),
    CK('Percussion (shifting dullness) and bowel sounds', {all: [/percuss|shifting dullness|tap/, /bowel sounds|listen|auscultat/]}),
    CK('Completes: hernial orifices, genitalia, rectal examination', {all: [/hernia/, /genitalia|genitals/, /rectal|\bdre\b|\bpr\b/]}),
  ],
  cvs: [
    CK('Sat at 45 degrees', {all: [/\b45\b|forty[- ]five/]}),
    CK('Collapsing pulse after asking about the shoulder', {all: [/collapsing|water hammer/, /shoulder/]}),
    CK('JVP', {all: [/jvp|jugular/]}),
    CK('Apex, heaves and thrills', {all: [/apex/, /heave|thrill/]}),
    CK('Four auscultation areas', {all: [/aortic|right second/, /pulmonary|left second/, /tricuspid|sternal edge/, /mitral|apex/]}),
    CK('Manoeuvres: left lateral and sitting forward', {all: [/left lateral|onto your left|roll (over )?(to|on|onto) your left/, /lean forward|sit forward|sitting forward/]}),
    CK('Lung bases and oedema', {all: [/base|crackle/, /oedema|swelling/]}),
  ],
  resp: [
    CK('Respiratory rate counted', {all: [/respiratory rate|breathing rate|count(ing)? (your )?breath/]}),
    CK('Trachea and expansion', {all: [/trachea/, /expansion/]}),
    CK('Percussion compared side to side', {all: [/percuss/]}),
    CK('Auscultation and vocal resonance', {all: [/listen|auscultat|breath sounds/, /vocal resonance|\b99\b|ninety[- ]nine/]}),
    CK('Front and back', {all: [/back|posterior|behind/]}),
  ],
  neuro: [
    CK('Tone', {all: [/\btone\b/]}),
    CK('Power with the joint fixed', {all: [/power/, /push|pull|resist|fix|support/]}),
    CK('Reflexes with reinforcement', {all: [/reflex/, /reinforc|jendrassik|clench|bite|grit/]}),
    CK('Coordination', {all: [/finger[- ]nose|heel[- ]shin|dysdiadocho|rapid alternating|coordination/]}),
    CK('Sensation: light touch, pin-prick, vibration, proprioception', {all: [/light touch/, /pin ?prick|sharp/, /vibration|tuning fork|128/, /proprioception|joint position|up or down/]}),
    CK('Compared sides', {all: [/compare|both sides|left (and|to|with) right|symmetr|other side/]}),
  ],
  joint: [
    CK('Look standing and walking', {all: [/walk|gait|stand/]}),
    CK('Feel: temperature, effusion, joint line', {all: [/temperature|warm/, /effusion|patellar tap|bulge|sweep|swelling|joint line/]}),
    CK('Move: active then passive', {all: [/active/, /passive/]}),
    CK('Special tests named', {all: [/lachman|drawer|mcmurray|collateral|valgus|varus|thomas|trendelenburg|faber|schober|neer|hawkins|empty can|straight leg/]}),
    CK('Neurovascular and the joint above and below', {all: [/joint above|joint below|pulses|neurovascular|sensation/]}),
  ],
  thyroid: [
    CK('Swallow water and stick the tongue out', {all: [/swallow|sip of water/, /tongue/]}),
    CK('Palpated from behind, nodes checked', {all: [/behind/, /lymph node|nodes/]}),
    CK('Eyes: lid lag and exophthalmos', {all: [/lid lag|lid retraction|exophthalmos|proptosis|bulging/]}),
    CK('Hands, pulse and tremor', {all: [/tremor|sweaty|pulse|warm/]}),
    CK('Completes: thyroid function tests', {all: [/\btft|thyroid function|\btsh/]}),
  ],
  cn: [
    CK('Acuity, fields and pupils', {all: [/acuity|snellen|read (the )?(chart|letters)/, /field/, /pupil|light reflex|swinging/]}),
    CK('Eye movements', {all: [/follow my finger|eye movements|h pattern|double vision/]}),
    CK('Face: sensation and muscles', {all: [/sensation|feel (this|me) touch|forehead|cheek|jaw/, /eyebrows|close your eyes|puff|smile|teeth/]}),
    CK('Hearing', {all: [/whisper|rinne|weber|hearing/]}),
    CK('Palate, tongue, shrug', {all: [/say ah|palate|uvula/, /tongue/, /shrug|turn your head/]}),
  ],
  mse: [
    CK('Appearance and behaviour', {all: [/appear|dressed|eye contact|behaviour|groom/]}),
    CK('Speech', {all: [/speech|rate|volume|pressured|slow/]}),
    CK('Mood (their words) and affect (what you see)', {all: [/mood/, /affect/]}),
    CK('Thoughts and perception', {all: [/thought|delusion|preoccup/, /hallucinat|voices|perception/]}),
    CK('Cognition and insight', {all: [/orient|cognition|memory|attention/, /insight/]}),
    CK('Risk', {all: [/risk|suicid|harm/]}),
  ],
  risk: [
    CK('Asked directly about suicidal thoughts', {c: 1, all: [/end(ing)? (your|my) life|kill (yourself|myself)|suicid|not (want(ing)? to be|wanting to be) (here|alive)|life (is|isn'?t|is not) worth living|harm(ing)? yourself/]}),
    CK('Plans, intent, means and preparation', {c: 1, all: [/\bplan/, /intend|intent|act on|going to/, /tablets|pills|means|note|prepar|stockpil|sav(ed|ing) up|research|look(ed|ing)? (things )?up/]}),
    CK('Past self-harm or attempts', {all: [/self-?harm|harmed yourself|before|in the past|previous(ly)?|ever (tried|done)/]}),
    CK('Protective factors', {all: [/what (stops|keeps|kept)|reason(s)? to live|keeps you going|kept you going|protective|look forward/]}),
    CK('Risk to others, children, and from others', {all: [/anyone else|others|children|kids|safeguard|safe at home/]}),
    CK('Alcohol and drugs', {all: [/alcohol|drink|drugs|cannabis|substance/]}),
    CK('Mania and psychosis screened', {all: [/high|elated|energy|little sleep|grand/, /voices|hearing things|seeing things|watching|following|messages|paranoi/]}),
    CK('Safety plan and crisis contacts', {c: 1, all: [/crisis|samaritans|\b111\b|\b999\b|a&e|a and e|safety plan|emergency/]}),
  ],
  counsel: [
    CK('Why: what it is for', {all: [/for your|to (treat|lower|control|reduce|protect)|because/]}),
    CK('How it works in plain words', {all: [/works by|how it works|relax|block|widen|open up/]}),
    CK('Dose and timing', {all: [/\d+ ?mg|once a day|twice a day|daily|morning|night|evening/]}),
    CK('Common side effects', {all: [/side effect/]}),
    CK('Serious side effects and what to do now', {c: 1, all: [/swelling|breath|rash|chest pain|faint|bleed|jaundice|yellow/, /999|a&e|a and e|urgent|straight away|stop/]}),
    CK('Interactions, alcohol, other medicines', {all: [/alcohol|grapefruit|ibuprofen|nsaid|interact|other (medicines|tablets)|over the counter/]}),
    CK('Monitoring and review', {all: [/blood test|kidney|u&e|monitor|blood pressure (check|reading)|review|follow[- ]up|come back|(\d+|two|four) weeks/]}),
    CK('Teach-back', {all: [/in your own words|tell me back|explain (it )?back|recap|summari[sz]e|what will you|how (are|will) you (going to )?take/]}),
  ],
  candour: [
    CK('Sincere apology for the error itself', {c: 1, all: [/sorry|apologi[sz]e/], bad: /sorry (that )?you feel|sorry you('re| are) upset/, fix: 'Apologise for what happened, not for how they feel.'}),
    CK('Checked how they are now (safety first)', {c: 1, all: [/how are you (feeling|now)|any (swelling|rash|breathing|itch)|feel(ing)? (ok|okay|now)|breath/]}),
    CK('Explained what happened, facts only', {all: [/what happened|was given|should(n'?t| not) have|mistake|error/]}),
    CK('Allergy documented and drug stopped', {all: [/allerg|wristband|record|alert|notes|stop/]}),
    CK('Senior informed and incident reported', {all: [/consultant|senior|registrar|supervisor/, /incident|datix|report/]}),
    CK('Complaint route: PALS', {all: [/\bpals\b|patient advice|complaint/]}),
    CK('Follow-up and contact', {all: [/follow[- ]up|meet|update|keep you informed|letter|contact/]}),
  ],
  bbn: [
    CK('Setting and support person', {all: [/private|sit down|somewhere quiet|anyone with you|bring someone|family/]}),
    CK('Perception: what they already know', {all: [/what do you (know|understand)|what have you been told|what('s| is) your understanding/]}),
    CK('Warning shot', {all: [/i'?m afraid|unfortunately|not the news|i have some (difficult|bad|serious) news|i'?m sorry to (have to )?tell/]}),
    CK('Silence and empathy', {all: [/take your time|i can see|must be|this is (a lot|difficult|hard)|shock|upsetting/]}),
    CK('Next steps and support', {all: [/next step|plan|scan|refer|team|specialist|nurse|support|leaflet|macmillan/]}),
    CK('Checked understanding and questions', {all: [/understand|questions|make sense/]}),
  ],
};
const CHK_DRAW = [[/culture/, 0], [/light blue|\bblue\b|citrate|coag|clotting/, 1], [/gold|yellow|serum|\bsst\b|u ?& ?e|\blft|crp|biochem/, 2], [/green|heparin/, 3], [/purple|lavender|edta|fbc|full blood count/, 4], [/pink|crossmatch|group and save/, 5], [/grey|gray|fluoride|glucose/, 6]];
function chkKeysFor(st){
  if (!st) return [];
  if (Array.isArray(st.chk)) return ['own'];
  const id = String(st.id || ''), t = ((st.t || '') + ' ' + (st.info || '') + ' ' + (st.task || '')).toLowerCase(), ks = [];
  const add = k => { if (CHK[k] && !ks.includes(k)) ks.push(k); };
  const pr = (/^P-/.test(id) ? [id.slice(2)] : []).concat(st.pr || []), ex = (/^E-/.test(id) ? [id.slice(2)] : []).concat(st.ex || []);
  pr.forEach(p => add({venep: 'venep', cann: 'cann', abg: 'abg', catm: 'catheter', catf: 'catheter', im: 'inj', sc: 'inj', ecg12: 'ecg12', transf: 'transf', ngt: 'ngt', pefr: 'pefr', inhaler: 'inhaler'}[p]));
  ex.forEach(e => add({abdo: 'abdo', cvs: 'cvs', resp: 'resp', ul: 'neuro', ll: 'neuro', knee: 'joint', hip: 'joint', spine: 'joint', thyroid: 'thyroid', cn: 'cn', mse: 'mse'}[e]));
  const fr = st.fr || [];
  if (fr.includes('mhx') || (typeOf(st) === 'psych' && /risk|suicid|self-?harm|overdose|low mood|depress|hopeless/.test(t))) add('risk');
  if (fr.includes('counsel')) add('counsel');
  if (fr.includes('bbn')) add('bbn');
  if ((fr.includes('prof') || typeOf(st) === 'comm') && /candour|error|mistake|wrong|complain|allerg|given .* despite/.test(t)) add('candour');
  return ks;
}
function chkSex(st){
  const v = cur && cur.st === st ? curVar() : (st.vars || [])[0];
  if (v && /^[mf]$/.test(v.sex || '')) return v.sex;
  if (st.id === 'P-catm') return 'm';
  if (st.id === 'P-catf') return 'f';
  const s = ((st.t || '') + ' ' + (st.info || '') + ' ' + ((v && v.who) || '')).toLowerCase();
  return /\b(woman|female|mrs|ms|miss|she|her|lady|girl)\b/.test(s) ? 'f' : /\b(man|male|mr|he|his|gentleman|boy)\b/.test(s) ? 'm' : '';
}
function chkRun(st, normText, prevResult){
  const ks = chkKeysFor(st); if (!ks.length) return [];
  const text = String(normText || '').toLowerCase().replace(/\s+/g, ' ');
  const sex = chkSex(st), risky = /risk|suicid|self-?harm|overdose|low mood|depress|hopeless/i.test((st.t || '') + ' ' + (st.info || '') + ' ' + (st.task || ''));
  const R = s => new RegExp(s, 'i');
  const rules = ks.includes('own')
    ? st.chk.map(r => Object.assign({}, r, {all: (r.all || []).map(R), bad: r.bad ? R(r.bad) : null, order: r.order ? r.order.map(R) : null}))
    : [].concat(...ks.map(k => CHK[k].map(r => k === 'risk' && !risky ? Object.assign({}, r, {c: 0}) : r)));
  const prevOk = new Set((prevResult && prevResult.chkOk) || []);
  const quote = i => i < 0 ? '' : text.slice(Math.max(0, i - 10), i + 70).trim();
  const out = [];
  rules.forEach(r => {
    if ((r.male && sex !== 'm') || (r.female && sex !== 'f')) return;
    if (r.draw) {
      const seen = [];
      CHK_DRAW.forEach(([rx, rank]) => { const L = chkAll(text, rx, false); if (L.length) seen.push([L[0], rank]); });
      if (seen.length < 2) return;
      seen.sort((a, b) => a[0] - b[0]);
      const ok = seen.every((x, i) => !i || x[1] >= seen[i - 1][1]);
      out.push({t: r.t, ok, c: false, why: ok ? '' : 'Tubes named out of order: cultures, citrate, serum, heparin, EDTA, fluoride. If you filled them in the right order, say each one as you fill it.'});
      return;
    }
    let ok = true, why = '', at = -1, badHit = false;
    (r.all || []).forEach(rx => { if (!ok) return; const L = chkAll(text, rx, false); if (!L.length) ok = false; else if (at < 0) at = L[0]; });
    if (ok && r.order) {
      const A = chkAll(text, r.order[0], true), B = chkAll(text, r.order[1], true);
      if (!A.length) { ok = false; why = r.fix || ''; }
      else { at = A[0]; if (B.length && B.every(b => b < A[0])) { ok = false; why = r.fix || 'Done in the wrong order.'; } }
    }
    if (r.bad && chkAll(text, r.bad, true).length) { ok = false; badHit = true; why = r.fix || 'Something you must never do was said.'; }
    if (!ok && !badHit && prevOk.has(r.t)) { ok = true; why = ''; }
    if (!ok && !why) why = r.fix || '';
    out.push({t: r.t, ok, c: !!r.c, why, quote: ok ? quote(at) : ''});
  });
  return out;
}
function chkHtml(r){
  if (!r || !r.chk || !r.chk.length) return '';
  const bad = r.chk.filter(x => !x.ok), crit = bad.filter(x => x.c);
  return '<div class="tt-sec chk"><div class="row"><b>🛡️ Safety and order checks · ' + (r.chk.length - bad.length) + '/' + r.chk.length + '</b>' + (crit.length ? '<span class="tt-cap">🚨 ' + crit.length + ' safety step' + (crit.length > 1 ? 's' : '') + ' missed: capped at 54% (borderline fail)</span>' : '') + '</div>'
    + (crit.length && r.rawPct != null && r.rawPct > r.pct ? '<p class="hint" style="margin:0">Without the cap you would have scored ' + r.rawPct + '%. An examiner fails an unsafe step however good the rest is.</p>' : '')
    + '<ul class="tt-list">' + r.chk.map(x => '<li>' + (x.ok ? '✅ ' : x.c ? '🚨 ' : '❌ ') + '<b>' + esc(x.t) + '</b>' + (x.ok && x.quote ? ' <span class="tt-quote">· "' + esc(x.quote) + '"</span>' : '') + (!x.ok && x.why ? '<div class="tt-say">' + esc(x.why) + '</div>' : '') + '</li>').join('') + '</ul></div>';
}
function ttBridgeHtml(st){
  const ui = (st.u || []).find(i => UNITS[i]);
  if (ui == null) return '';
  return '<div class="row" style="margin-top:6px"><a class="btn sm" href="' + DRILL + '#hq-u' + ui + '"' + (/^https?:/.test(DRILL) ? ' target="_blank" rel="noopener"' : '') + '>📚 Drill the SBAs for ' + esc(UNITS[ui].name) + ' in STUDY ↗</a></div>';
}
/* ✨ put the corrected words into the box, so the transcript you keep reads properly */
const TT_KEEP = /^(rapid alternating|water hammer|supinator|ninety[- ]nine|a fib|atrial fib|liver flap|spoony nails|troisier|kussmaul|murphy'?s?|interossei|leukonychia|ophthalmoplegia|dupuytren|kayser fleischer|caput medusa|any quarters|no quarters|rapid alternating)$/i;
function ttFixCount(st, text){ let n = 0; ttMapFor(st).forEach(([rx]) => { const m = String(text || '').match(rx); if (m) m.forEach(x => { if (!TT_KEEP.test(x.trim())) n++; }); }); return n; }
function ttApplyFix(st){
  const ta = $('#ttTranscriptInput'); if (!ta) return;
  let v = ta.value, n = 0;
  ttMapFor(st).forEach(([rx, rep, label]) => {
    const to = (String(label || '').split('->')[1] || rep).trim();
    v = v.replace(rx, m => { if (TT_KEEP.test(m.trim()) || m.toLowerCase() === to.toLowerCase()) return m; n++; return to; });
  });
  ta.value = v; ttGradeState.raw = v;
  toast(n ? '✨ Fixed ' + n + ' voice slip' + (n > 1 ? 's' : '') + ' in the box' : 'No voice slips found');
}

/* ---------- v3.3.0 listeners ---------- */
document.addEventListener('click', e => {
  const b = e.target.closest && e.target.closest('button'); if (!b) return;
  const d = b.dataset;
  if (d.mnquiz != null) { mnState.quiz = !mnState.quiz; mnState.rev = new Set(); return mnRedraw(); }
  if (d.mnreset != null) { mnState.rev = new Set(); return mnRedraw(); }
  if (d.mnrev) { if (mnState.rev.has(d.mnrev)) mnState.rev.delete(d.mnrev); else mnState.rev.add(d.mnrev); return mnRedraw(); }
  if (d.mnadd != null) { mnState.form = mnState.form === d.mnadd ? '' : d.mnadd; return mnRedraw(); }
  if (d.mnsave) {
    const val = id => (($(id) || {}).value || '').trim();
    const code = val('#mnCode').slice(0, 24), tt = val('#mnFor').slice(0, 60), line = val('#mnLine').slice(0, 160);
    const L = val('#mnLetters').split('\n').map(x => x.trim()).filter(Boolean).slice(0, 12).map(x => { const m = x.match(/^(.{1,8}?)\s*(?:=|:|–|-)\s*(.+)$/); return m ? [m[1].trim(), m[2].trim().slice(0, 90)] : [x.slice(0, 1).toUpperCase(), x.slice(0, 90)]; });
    if (!code || (!L.length && !line)) { toast('Add a code, and at least one letter or a line'); return; }
    S.myMn = S.myMn || {};
    (S.myMn[d.mnsave] = S.myMn[d.mnsave] || []).push({id: 'u' + Date.now().toString(36), k: L.length ? 'acr' : 'rule', code, t: tt || code, L, line, why: 'Made by you. Cues you build yourself are remembered better than borrowed ones (the generation effect).', no: ''});
    save(); mnState.form = ''; toast('🧬 Saved to this station'); return mnRedraw();
  }
  if (d.mndel) {
    const sid = d.mnst;
    if (S.myMn && S.myMn[sid]) { S.myMn[sid] = S.myMn[sid].filter(x => x.id !== d.mndel); if (!S.myMn[sid].length) delete S.myMn[sid]; save(); }
    delete mnById[d.mndel]; return mnRedraw();
  }
  if (d.ttfix != null) { if (cur && cur.st) ttApplyFix(cur.st); return; }
  if (d.mylock != null) return myLock();
  if (d.myexport != null) return myExport();
  if (d.myseal != null) return mySealPending();
  if (d.mycancel != null) { MY.pending = null; MY.msg = ''; return vMy($('#main')); }
  if (d.myopen != null) return myUnlock();
  if (d.mydel != null) {
    if (!MY.armDel) { MY.armDel = true; vMy($('#main')); setTimeout(() => { MY.armDel = false; }, 6000); return; }
    try { localStorage.removeItem(MY_KEY); } catch (x) {}
    MY.armDel = false; MY.msg = '🗑 Removed from this device.'; return vMy($('#main'));
  }
});
document.addEventListener('input', e => {
  if (e.target.id === 'mnQ') { mnState.q = e.target.value; const L = $('#mnList'); if (L) L.innerHTML = mnListHtml(); }
});
document.addEventListener('change', e => {
  if (e.target.id === 'mnK') { mnState.k = e.target.value; const L = $('#mnList'); if (L) L.innerHTML = mnListHtml(); }
  else if (e.target.id === 'myFile' && e.target.files && e.target.files[0]) myHandleFile(e.target.files[0]);
});
document.addEventListener('keydown', e => {
  if (e.key !== 'Enter') return;
  if (e.target.id === 'myPw') { e.preventDefault(); myUnlock(); }
  else if (e.target.id === 'myP2') { e.preventDefault(); mySealPending(); }
});
document.addEventListener('toggle', e => {
  const id = e.target && e.target.id;
  if (id === 'mnCard') { S.set.mnOpen = e.target.open; save(); }
  else if (id === 'mnPrimer') { S.set.mnPrimer = e.target.open; save(); }
}, true);

/* ---------- voice slips that only make sense in one kind of station ---------- */
(function scopeTalkType(){
  const dx = TALKTYPE_MAP.findIndex(e => /deflated/.test(e[0].source));
  if (dx >= 0) TALKTYPE_MAP.splice(dx, 1);   // "deflated" is a real word patients use; it is not "lethargic"
  const thy = st => typeof isThyroidStation === 'function' && isThyroidStation(st), exam = st => typeOf(st) === 'ex';
  const SCOPE = [[/thorough examination/, thy], [/no quarters/, thy], [/put custom/, thy], [/acropathy/, thy], [/mix oedema/, thy], [/breeds/, exam], [/murphys/, exam], [/rov sings/, exam], [/the nar/, exam]];
  TALKTYPE_MAP.forEach(e => { const s = SCOPE.find(([k]) => k.test(e[0].source)); if (s) e[3] = s[1]; });
  const comm = st => typeOf(st) === 'comm' || /pals|complain|candour/i.test((st.t || '') + ' ' + (st.info || ''));
  TALKTYPE_MAP.push(
    [/\b(?:palls|pauls|powells|pals service)\b/gi, 'pals', 'pauls -> PALS', comm],
    [/\b(?:day ?ticks|day ?tix|datex|data ?x)\b/gi, 'datix', 'day ticks -> Datix', comm],
    [/\b(?:turbine a fine|terbina fine|terba fine|turban a fine|turbo na fine)\b/gi, 'terbinafine', 'turbine a fine -> terbinafine'],
    [/\b(?:clot rim a zole|clot trim azole|clotrima zole)\b/gi, 'clotrimazole', 'clot rim a zole -> clotrimazole'],
    [/\b(?:am low to pin|amlo deeping|am lodge a pin|amlo dipping|amlodipene)\b/gi, 'amlodipine', 'am low to pin -> amlodipine'],
    [/\b(?:rammy pril|rami prill|ram a pril|rammi pril)\b/gi, 'ramipril', 'rammy pril -> ramipril'],
    [/\b(?:brady kinin|brady keenan|brady chinon|brady kinnin)\b/gi, 'bradykinin', 'brady keenan -> bradykinin'],
    [/\b(?:tourney kit|turn a kit|tourni kit|tony kit)\b/gi, 'tourniquet', 'tourney kit -> tourniquet'],
    [/\b(?:chlorhexadine|chlora hex a dean|chlorhex a dine|chlor hexi dean)\b/gi, 'chlorhexidine', 'chlora hex a dean -> chlorhexidine']
  );
})();
function ttMapFor(st){ return TALKTYPE_MAP.filter(e => !e[3] || (st && e[3](st))); }

function vWaitHint(){ const w = String(S.set.vWait || '2500'); return w === 'tap' ? 'only when you tap <b>➤ Send</b> or press Enter' : '<b>' + (vWaitMs() / 1000) + ' s</b> after you stop talking (longer if you trail off on "and…" or "um…"); <b>➤ Send</b> or Enter sends sooner, <b>✋ Hold</b> or Esc waits. Change the wait in voice settings'; }

/* ---------- views and routes ---------- */
VIEWS.push('mn', 'my');
