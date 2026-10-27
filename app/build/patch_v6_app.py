#!/usr/bin/env python3
"""medengine-OSCE v2.0, one-off patch of src/app_script.html and src/app_head.html (already applied: do not re-run).

🗺️ Poster becomes the first mode on every station: history, psychiatry, drug, communication and imaging stations become a
10-minute clock with 4 timed corners (⚡ Last 2 min collapses it to the plan), examinations become a route walked around a
body or a head, procedures become a 3-frame storyboard. ILO pages open on the condition poster; a Posters hub holds the 14
master posters. ⌘F / Ctrl+F jumps to the search bar. 🙈 Test me becomes 🔒 Lock everywhere. Version 2.0.0.
Later v2.0 polish was made straight in src/app_script.html: whole steps lock, brackets become commas on station
posters, short storyboards split evenly, and bank and past-paper stations use the history clock labels."""
import pathlib
SRC = pathlib.Path(__file__).resolve().parent.parent / 'src'
js_p, head_p = SRC / 'app_script.html', SRC / 'app_head.html'
js, head = js_p.read_text(encoding='utf-8'), head_p.read_text(encoding='utf-8')
assert 'v2.0: 🗺️ posters' not in js, 'already applied'


def rep(s, old, new, n=1):
    c = s.count(old)
    if c != n:
        raise SystemExit(f'expected {n} of {old[:90]!r}, found {c}')
    return s.replace(old, new)


# ---------- state: Poster is the first mode, and everyone starts on it once ----------
js = rep(js, "const SET0 = {mode: 'script',", "const SET0 = {mode: 'poster',")
js = rep(js, "if (!['script', 'tick', 'friends', 'ai', 'voice'].includes(S.set.mode)) S.set.mode = 'script';",
         "if (!S.set.v2) { S.set.mode = 'poster'; S.set.v2 = 1; }\nif (!['poster', 'script', 'tick', 'friends', 'ai', 'voice'].includes(S.set.mode)) S.set.mode = 'poster';")
js = rep(js, "const APP_NAME = 'medengine-OSCE', APP_VERSION = '1.4.0'", "const APP_NAME = 'medengine-OSCE', APP_VERSION = '2.0.0'")

# ---------- routing ----------
js = rep(js, "const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp', 'rf'];",
         "const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp', 'rf', 'posters'];")
js = rep(js, "  if ((m = h.match(/^f-(\\w+)$/)) && FR[m[1]]) return {v: 'frame', id: m[1]};",
         "  if ((m = h.match(/^f-(\\w+)$/)) && FR[m[1]]) return {v: 'frame', id: m[1]};\n  if ((m = h.match(/^mp-([\\w-]+)$/)) && MBY[m[1]]) return {v: 'master', id: m[1]};")
js = rep(js, "r.v === 'frame' ? 'f-' + r.id :", "r.v === 'frame' ? 'f-' + r.id : r.v === 'master' ? 'mp-' + r.id :")
js = rep(js, ": route.v === 'rf' ? 'ty:hx' : '';", ": route.v === 'rf' ? 'ty:hx' : route.v === 'posters' || route.v === 'master' ? 'posters' : '';")
js = rep(js, "frame: vFrame, fw: vFw, fwone: vFwOne, visual: vVisual}[route.v] || vHome)(m);",
         "frame: vFrame, fw: vFw, fwone: vFwOne, visual: vVisual, posters: vPosters, master: vMaster}[route.v] || vHome)(m);")

# ---------- home ----------
js = rep(js, "APP_NAME + ' v1.4 · FFP CPSA · one station, one task</span>", "APP_NAME + ' v2.0 · FFP CPSA · one station, one task</span>")
js = rep(js, "Open one, read the door, then pick 📜 <b>Script</b> to learn it,", "Open one, read the door, then pick 🗺️ <b>Poster</b> to see the whole station as one picture, 📜 <b>Script</b> to learn it,")
js = rep(js, """<div class="row more"><span class="hint">More:</span><button class="btn sm" data-go="rf">""",
         """<div class="row more"><span class="hint">More:</span><button class="btn sm" data-go="posters">🗺️ Posters</button><button class="btn sm" data-go="rf">""")

# ---------- ILO page opens on its condition poster ----------
js = rep(js, """'</section>' + packHtml(p, true) + '<section class="card"><h2>Stations for this ILO · '""",
         """'</section>' + condPosterHtml(u.i) + packHtml(p, true) + '<section class="card"><h2>Stations for this ILO · '""")

# ---------- station page: a poster card and the Poster mode ----------
js = rep(js, "const MODES = [['script', '📜 Script'],", "const MODES = [['poster', '🗺️ Poster'], ['script', '📜 Script'],")
js = rep(js, "  if (!modesFor(st).some(([k]) => k === cur.mode)) cur.mode = 'script';", "  if (!modesFor(st).some(([k]) => k === cur.mode)) cur.mode = 'poster';")
js = rep(js, """  h += '<div id="fwWrap"></div><div id="dgWrap"></div><div id="hookWrap"></div>';""",
         """  h += '<div id="posterCard"></div><div id="fwWrap"></div><div id="dgWrap"></div><div id="hookWrap"></div>';""")
js = rep(js, """  const bp = $('#briefP'); if (bp) bp.textContent = (v && v.d) || st.info;""",
         """  const bp = $('#briefP'); if (bp) bp.textContent = (v && v.d) || st.info;
  const pc = $('#posterCard'); if (pc) pc.innerHTML = posterFor(st);""")
js = rep(js, "const dx = $('#varDx'); if (dx) dx.textContent = v && !cur.hidden && (cur.mode === 'script' || cur.mode === 'tick' ||",
         "const dx = $('#varDx'); if (dx) dx.textContent = v && !cur.hidden && (cur.mode === 'poster' || cur.mode === 'script' || cur.mode === 'tick' ||")
js = rep(js, "  $('#scriptCard').hidden = md !== 'script';", "  $('#posterCard').hidden = md !== 'poster';\n  $('#scriptCard').hidden = md !== 'script';")
js = rep(js, "  $('#modelCard').hidden = cand || (md === 'ai' || md === 'voice') && !cur.fb;\n  $('#hookWrap').hidden = cand;",
         "  $('#modelCard').hidden = cand || md === 'poster' || (md === 'ai' || md === 'voice') && !cur.fb;\n  $('#hookWrap').hidden = cand || md === 'poster';")
js = rep(js, "  const ss = $('#stSub'); if (ss) ss.hidden = md !== 'script';", "  const ss = $('#stSub'); if (ss) ss.hidden = md !== 'script' && md !== 'poster';")
js = rep(js, "  if (l === 120) { toast('8:00 🔔 Stop gathering: summarise → reasoning sentence → plan → safety-net'); gong();",
         "  if (l === 120) { toast('8:00 🔔 Stop gathering: summarise → reasoning sentence → plan → safety-net'); gong(); if (cur.mode === 'poster') { const po = $('#posterCard .po-corners'); if (po && window.PO) { PO.setSprint(po, true); cur.sprint = true; } }")

# ---------- 🔒 Lock wording ----------
js = rep(js, "> 🙈 Test me: hide the words, say them, tap to check</label>", "> 🔒 Lock: hide the words, say them, tap to check</label>")
js = rep(js, "> 🙈 Recall mode</label>", "> 🔒 Lock the lines</label>")
js = rep(js, "(rc ? 'Say each line out loud before you tap to check it.' : 'Read it once, then switch on Recall mode and say each line before revealing it.')",
         "(rc ? 'Say each line out loud before you tap to check it.' : 'Read it once, then lock the lines and say each one before revealing it.')")

# ---------- search finds master posters ----------
js = rep(js, """  m.innerHTML = '<section class="card"><h1>Search: ' + esc(q) + '</h1></section>' + (fm.length""",
         """  const mpm = MASTER.filter(x => hit(x.t + ' ' + (x.sub || '') + ' ' + (x.hook || '') + ' ' + (x.u || []).map(i => UNITS[i] ? UNITS[i].name : '').join(' ')));
  m.innerHTML = '<section class="card"><h1>Search: ' + esc(q) + '</h1></section>' + (mpm.length ? '<section class="card"><h2>🧭 Master posters</h2><div class="chips">' + mpm.map(x => '<button class="chip" data-mp="' + x.id + '">' + esc(x.ic) + ' ' + esc(x.t) + '</button>').join('') + '</div></section>' : '') + (fm.length""")

# ---------- clicks ----------
js = rep(js, "  if (t.id === 'homeBtn') return go({v: 'home'});",
         "  if (t.id === 'homeBtn') return go({v: 'home'});\n  if (d.mp) return go({v: 'master', id: d.mp});\n  if (d.stpo) { S.set.mode = 'poster'; save(); return go({v: 'station', id: d.stpo}); }")

# ---------- the poster code itself ----------
BLOCK = r"""
/* ---------- v2.0: 🗺️ posters: one picture code for every station and every condition ---------- */
const SNAPD = D.snap || {}, MASTER = D.master || [], MBY = {}, POD = D.po || {routes: {}, story: {}};
MASTER.forEach(x => MBY[x.id] = x);
const MOFU = {}; MASTER.forEach(x => (x.u || []).forEach(u => (MOFU[u] = MOFU[u] || []).push(x.id)));
const cutT = (t, n) => { t = String(t == null ? '' : t).trim(); if (t.replace(/\*\*/g, '').length <= n) return t; t = t.replace(/\*\*/g, ''); const c = t.slice(0, n); return c.slice(0, Math.max(c.lastIndexOf(' '), n - 24)).replace(/[\s,;:.]+$/, '') + '…'; };
function masterChipsHtml(ids){ const L = [...new Set(ids.flatMap(i => MOFU[i] || []))].filter(id => MBY[id]); return L.length ? '<div class="po-mp"><span>🧭 Master posters</span>' + L.map(id => '<button type="button" class="chip" data-mp="' + id + '">' + esc(MBY[id].ic || '🧭') + ' ' + esc(MBY[id].t) + '</button>').join('') + '</div>' : ''; }
function condPosterHtml(ui){ const s = SNAPD[ui]; return s && window.PO ? PO.cond(s, {id: 'u' + ui, lock: PO.lockOn, foot: masterChipsHtml([ui])}) : ''; }
function whyPostersHtml(){
  return '<details class="dd why-po"><summary>💡 Why posters work for you</summary><div class="body"><p class="hint" style="margin:0">You take in a page as one picture and remember where things sat, so every poster follows one code. Only the content changes.</p><div class="place">'
    + [['P', 'Picture with the words on it', 'the words sit inside the picture, never in a separate list'], ['L', 'Location never changes', 'cause top-left, who top-right, tests on the right, treatment bottom-right, danger bottom-left, the lookalike on the left, signs in the middle'], ['A', 'Arrows carry the movement', 'every mechanism is a chain you can play like a film'], ['C', 'Contrast on one axis', 'each condition sits beside the one it gets confused with, compared on a single question'], ['E', 'Exaggerate one thing', 'one hook per poster, not ten'], ['🔒', 'Then LOCK it', 'a glance feels like knowing, so Lock hides the drugs, numbers and signs: say them, then tap. Pulling them back out is what makes them stick']].map(r => '<div><b>' + r[0] + '</b><span><b>' + esc(r[1]) + ':</b> ' + esc(r[2]) + '</span></div>').join('') + '</div></div></details>';
}
/* a talking station as a 10-minute clock: 4 timed corners, the plan always bottom-right */
const PCF = {
  hx: [['🚪', 'The door', 'who', '0:00', 1], ['🗣️', 'Gather', 'spot', '1:00', 5], ['🧠', 'Think', 'cause', '6:00', 2], ['🎯', 'Present and plan', 'treat', '8:00', 2]],
  talk: [['🚪', 'The door', 'who', '0:00', 1], ['💬', 'Explain', 'spot', '1:00', 5], ['🧠', 'Clinch', 'cause', '6:00', 2], ['🎯', 'Plan and safety-net', 'treat', '8:00', 2]],
  psych: [['🤝', 'Open', 'who', '0:00', 1], ['🗣️', 'Story and screen', 'spot', '1:00', 4], ['🚩', 'Risk and background', 'watch', '5:00', 3], ['🎯', 'Present: risk and plan', 'treat', '8:00', 2]],
  drug: [['🤝', 'Start with them', 'who', '0:00', 1], ['💊', 'Why and how', 'spot', '1:00', 4], ['🚩', 'Watch', 'watch', '5:00', 3], ['✅', 'Check and safety-net', 'treat', '8:00', 2]],
  comm: [['🤝', 'Set up and find out', 'who', '0:00', 2], ['💬', 'Explain in chunks', 'spot', '2:00', 3], ['💛', 'Feelings and plan', 'cause', '5:00', 3], ['✅', 'Summary and safety-net', 'treat', '8:00', 2]],
  img: [['📋', 'Details and quality', 'who', '0:00', 1], ['🔍', 'The system', 'spot', '1:00', 4], ['🎯', 'The finding', 'cause', '5:00', 2], ['➡️', 'Conclude and next step', 'treat', '7:00', 3]]};
const PRE = {psych: [/^Open/, /^(Presenting|Screen|Substances|Current)/, /^(Risk|Background|Context)/, /^(Present|Formulate)/],
  drug: [/^(Start|Explore)/, /^(Why|How|Detox|Explain|Pen)/, /^(Watch|Monitor|Fire|Sick|Driving|Life|Staying|Act on|Decide)/, /^(Check|Safety)/],
  comm: [/^(S: Setting|P:|I:|Start|Explore)/, /^(K:|Explain)/, /^(E:|Plan)/, /^(S: Strategy|Close|Safety)/],
  img: [/^(Details|Quality|Orientation)/, /./, /^$/, /^Conclude/]};
const SPRINT = {hx: ['Summarise in one line: who, what, how long', '"The important finding is ___. It suggests ___ because ___."', 'What you must exclude, and how', 'First tests, then the plan and the safety-net'],
  talk: ['Summarise the 2 or 3 key points', 'Check understanding: teach-back', 'The plan and the follow-up date', 'Safety-net: exactly when to come back'],
  img: ['The diagnosis in one line', 'The 2 findings that prove it', 'What else it could be', 'The next step, today']};
function splitArrow(t){ const s = String(t || ''), i = Math.max(s.lastIndexOf(' → '), s.lastIndexOf(' = ')); return i > 0 ? {h: s.slice(0, i + 2).trim(), t: s.slice(i + 3).trim(), all: 1} : {t: s}; }
function routeSecs(secs, re){ const out = [[], [], [], []]; let last = 0; secs.forEach((sc, i) => { let k = i === secs.length - 1 ? 3 : re.findIndex(r => r.test(sc.h)); if (k < 0) k = last; out[k].push(sc); last = k; }); return out; }
const secLines = L => L.flatMap(sc => sc.items.map((it, j) => ({h: j === 0 && L.length > 1 ? sc.h + ':' : '', t: it.t})));
function forkLines(st, n){
  const V = (st.vars || []).filter(v => v.dx); if (!V.length || (cur && cur.hidden)) return [];
  const first = V.find(v => cur && v.k === cur.vk) || V[0];
  return [first].concat(V.filter(v => v !== first)).slice(0, n || 4).map(v => ({h: (V.length > 1 ? 'Case ' + v.k + ' · ' : '') + plainDx(v.dx) + ' →', t: cutT(String((st.mv && st.mv[v.k]) || v.x || '').replace(/^In summary,\s*_+\.?\s*/i, ''), 260), all: 1}));
}
const plainDx = t => String(t || '').replace(/\*\*/g, '');
function rfLines(st, n){ const out = []; (st.rf || []).map(id => rfById[id]).filter(Boolean).forEach(sh => sh.rows.forEach(r => out.push({h: r[0] + ' →', t: r[1] + ': ' + r[3], all: 1}))); return out.slice(0, n); }
function cornersOf(st){
  const ty = typeOf(st), pk = packFor(st), p = pk ? pk.p : {}, sk = SKEL[st.skel];
  let Z = PCF[ty] || PCF.hx, L = [[], [], [], []], hook = '', sp = SPRINT.hx;
  if (st.secs && PRE[ty]) {
    routeSecs(st.secs, PRE[ty]).forEach((g, i) => L[i] = secLines(g));
    if (ty === 'img') { L[2] = (st.vars || []).filter(v => v.r).slice(0, 4).map(v => ({h: plainDx(v.dx) + ':', t: cutT(v.r, 220), all: 1})); sp = SPRINT.img; }
    else L[3] = L[3].concat(forkLines(st, 3));
    if (ty === 'drug' || ty === 'comm') sp = SPRINT.talk;
    hook = (st.hooks || [])[0] || '';
  } else if (st.pp) {
    const talk = ty === 'drug' || ty === 'comm'; if (talk) { Z = PCF.talk; sp = SPRINT.talk; }
    L[0] = (st.trig || []).slice(0, 4).map(splitArrow);
    L[1] = talk ? (st.hook || []).slice(0, 3).map(t => ({t})) : (sk ? [{h: 'Skeleton:', t: sk.chips.join(' → ')}] : []).concat(rfLines(st, 3));
    L[1] = L[1].concat((st.ask || []).slice(0, 2).map(q => ({h: 'They ask:', t: '“' + q + '”'})));
    L[2] = (st.clinch || []).slice(0, 5).map(c => Object.assign({}, splitArrow(c[1]), {h: (CKI[c[0]] || '•') + ' ' + (splitArrow(c[1]).h || '')})).concat((st.trap || []).slice(0, 2).map(t => ({h: '⚠️', t})));
    L[3] = [{h: 'Say:', t: st.money || ''}].concat(forkLines(st, 4));
    hook = talk ? '' : (st.hook || [])[0] || '';
  } else {
    L[0] = (st.cmp ? [{h: 'Split:', t: st.cmp}] : []).concat((() => { const dx = []; (st.rf || []).map(id => rfById[id]).filter(Boolean).forEach(sh => sh.rows.forEach(r => { if (!dx.includes(r[1])) dx.push(r[1]); })); return dx.length ? [{h: 'Think of:', t: dx.slice(0, 5).join(', ')}] : []; })());
    L[1] = (p.hx || []).slice(0, 5).map(t => ({h: 'Ask:', t})).concat(rfLines(st, 2));
    L[2] = (p.ck || []).slice(0, 5).map(c => Object.assign({}, splitArrow(c[1]), {h: (CKI[c[0]] || '•') + ' ' + (splitArrow(c[1]).h || '')}));
    L[3] = [{h: 'Say:', t: 'In summary, ___. The most likely diagnosis is ___ because ___. I would exclude ___, and my first tests are ___.'}].concat((p.ix || []).slice(0, 3).map(t => ({h: 'Test:', t})), (p.mx || []).slice(0, 3).map(t => ({h: 'Treat:', t})), (p.sn || []).slice(0, 1).map(t => ({h: 'Safety-net:', t})));
  }
  if (sk) L.forEach((l, i) => { if (!l.length) L[i] = [{h: 'Skeleton:', t: sk.chips.join(' → ')}]; });
  return {id: st.id, t: st.t, sub: st.pp ? '📚 past paper' : '', hook,
    top: '<div class="po-sprint"><b>⚡ The last 2 minutes</b><ol>' + sp.map(x => '<li>' + esc(x) + '</li>').join('') + '</ol></div>',
    zones: Z.map((z, i) => ({i: z[0], h: z[1], c: z[2], time: z[3], span: z[4], lines: L[i].length ? L[i] : [{t: '…'}]}))};
}
function storyOf(st){
  const x = POD.story[st.id] || {fail: [], nums: []}, secs = st.secs || [], n = secs.length, H = [['🧰', 'Set up'], ['✋', 'Do it'], ['✅', 'Finish and act']], F = [[], [], []];
  if (n >= 3) secs.forEach((sc, i) => F[i === 0 ? 0 : i === n - 1 ? 2 : 1].push(sc));
  const lines = g => g.flatMap(sc => sc.items.map(it => it.t));
  let L = F.map(lines);
  if (n < 3) { const all = lines(secs), k = Math.ceil(all.length / 3); L = [all.slice(0, k), all.slice(k, 2 * k), all.slice(2 * k)]; }
  L[2] = L[2].concat(x.more || []);
  return {id: st.id, t: st.t, nums: x.nums || [], frames: H.map((h, k) => ({i: h[0], h: n >= 3 ? F[k].map(sc => sc.h).join(' · ') : h[1], lines: L[k].length ? L[k] : ['…'], fail: (x.fail || [])[k]}))};
}
function posterFor(st){
  if (!window.PO) return '';
  const ty = typeOf(st), o = {id: st.id, lock: PO.lockOn};
  if (ty === 'ex' && POD.routes[st.id]) return PO.route(Object.assign({id: st.id, t: st.t, present: st.money || ''}, POD.routes[st.id]), o) + masterChipsHtml(st.u || []);
  if (ty === 'proc' && POD.story[st.id]) return PO.story(storyOf(st), o);
  return PO.corners(cornersOf(st), Object.assign(o, {sprint: !!(cur && cur.sprint), extra: '<button type="button" class="po-b" data-posprint aria-pressed="' + (cur && cur.sprint ? 'true' : 'false') + '" title="Collapse to the last 2 minutes: present and plan">⚡ Last 2 min</button>'})) + masterChipsHtml(st.u || []);
}
if (window.PO) PO.onSprint = on => { if (cur) cur.sprint = on; };
/* the Posters hub and the master posters */
function posterWallHtml(q){
  const seen = new Set(); let h = '';
  D.weeks.forEach(w => {
    const us = UNITS.filter(u => u.w === w.id && SNAPD[u.i] && !seen.has(SNAPD[u.i].n) && (!q || (u.name + ' ' + SNAPD[u.i].n + ' ' + SNAPD[u.i].m).toLowerCase().includes(q)));
    us.forEach(u => seen.add(SNAPD[u.i].n));
    if (us.length) h += '<span class="hkh">' + esc(w.name) + ' · ' + us.length + '</span><div class="chips">' + us.map(u => '<button class="chip" data-u="' + u.i + '">🗺️ ' + esc(SNAPD[u.i].n) + '</button>').join('') + '</div>';
  });
  return h || '<p class="hint">Nothing matches.</p>';
}
function vPosters(m){
  const q = (S.set.poq || '').toLowerCase().trim(), ex = ST.filter(s => typeOf(s) === 'ex' && POD.routes[s.id]), pr = ST.filter(s => typeOf(s) === 'proc' && POD.story[s.id]);
  let h = '<section class="card"><span class="eyebrow">🗺️ One picture code everywhere</span><h1>Posters</h1><p class="hint" style="margin:0">Every condition, examination and procedure drawn the same way, so only the content changes. Press 🔒 <b>Lock</b> or the <span class="kbd">L</span> key to hide the details, say them, then tap each pill or press <span class="kbd">N</span>. ▶ <b>Walk it</b> lights the zones in reading order.</p>' + whyPostersHtml() + '</section>';
  h += '<section class="card"><h2>🧭 Master posters · ' + MASTER.length + '</h2><p class="hint" style="margin:0">One picture for a whole topic. The first five rebuild your AI-made infographics with every error fixed; 🔎 lists what was wrong.</p><div class="grid2">' + MASTER.map(x => '<button class="tile" data-mp="' + x.id + '"><b>' + esc(x.ic) + ' ' + esc(x.t) + '</b><span class="hint">' + esc(x.sub || '') + '</span>' + ((x.fix || []).length ? '<span class="hint">🔎 ' + x.fix.length + ' fixes to the AI version</span>' : '') + '</button>').join('') + '</div></section>';
  h += '<section class="card"><h2>🩺 Examination routes · ' + ex.length + '</h2><div class="chips">' + ex.map(s => '<button class="chip" data-stpo="' + s.id + '">' + esc(s.t) + '</button>').join('') + '</div><h2>🎬 Procedure storyboards · ' + pr.length + '</h2><div class="chips">' + pr.map(s => '<button class="chip" data-stpo="' + s.id + '">' + esc(s.t) + '</button>').join('') + '</div></section>';
  h += '<section class="card"><h2>🗺️ Condition posters · ' + new Set(Object.values(SNAPD).map(s => s.n)).size + '</h2><input class="sel" id="poQ" type="search" placeholder="Filter: e.g. thyroid, stone, eye" value="' + esc(S.set.poq || '') + '" aria-label="Filter condition posters"><div id="poWall">' + posterWallHtml(q) + '</div></section>';
  m.innerHTML = h;
}
function vMaster(m){
  const x = MBY[route.id]; if (!x || !window.PO) return vPosters(m);
  const i = MASTER.indexOf(x), pv = MASTER[(i - 1 + MASTER.length) % MASTER.length], nx = MASTER[(i + 1) % MASTER.length];
  m.innerHTML = '<section class="card"><div class="row"><button class="btn sm" data-v="posters">← All posters</button><span class="grow"></span><button class="btn sm" data-mp="' + pv.id + '">← ' + esc(pv.t) + '</button><button class="btn sm" data-mp="' + nx.id + '">' + esc(nx.t) + ' →</button></div></section>' + PO.split(x, {lock: PO.lockOn}) + ((x.u || []).length ? '<section class="card"><h2>Conditions on this poster</h2><div class="chips">' + iloChips(x.u) + '</div></section>' : '');
}
document.addEventListener('input', e => { if (e.target.id === 'poQ') { S.set.poq = e.target.value; clearTimeout(vPosters.t); vPosters.t = setTimeout(() => { save(); const w = $('#poWall'); if (w) w.innerHTML = posterWallHtml(e.target.value.toLowerCase().trim()); }, 180); } });
/* ⌘F / Ctrl+F jumps to the search bar; press it again there for the browser's own find */
document.addEventListener('keydown', e => {
  if (!(e.metaKey || e.ctrlKey) || e.altKey || e.shiftKey || (e.key || '').toLowerCase() !== 'f') return;
  const q = $('#q'); if (!q || document.activeElement === q) return;
  e.preventDefault(); q.classList.add('show'); q.focus(); q.select();
}, true);
"""
js = rep(js, "\n/* ---------- events ---------- */", BLOCK + "\n/* ---------- events ---------- */")

# ---------- header: version, nav ----------
head = rep(head, '<span class="ver">v1.4.0</span>', '<span class="ver">v2.0.0</span>')
head = rep(head, '    <button data-v="home">🏠 Home</button>\n', '    <button data-v="home">🏠 Home</button>\n    <button data-v="posters">🗺️ Posters</button>\n')
CSS = """.po-mp{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-top:8px}.po-mp>span{color:var(--muted);font-size:.8rem;font-weight:700}
#posterCard{display:flex;flex-direction:column;gap:8px}#posterCard[hidden]{display:none}
.why-po .place{display:flex;flex-direction:column;gap:6px;margin-top:8px}.why-po .place>div{display:grid;grid-template-columns:28px minmax(0,1fr);gap:8px;align-items:baseline;font-size:.9rem;line-height:1.4}.why-po .place>div>b{font-family:var(--f-display);font-size:1.1rem;color:var(--accent)}
"""
head = rep(head, '</style>', CSS + '</style>')
js_p.write_text(js, encoding='utf-8')
head_p.write_text(head, encoding='utf-8')
print('patched', len(js), len(head))
