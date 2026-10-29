#!/usr/bin/env python3
"""One-off: turn the v1.0 OSCE engine into the v1.3 FFP layout. Applied to src/app_script.html and src/app_head.html.
Every replacement must match exactly once, so a second run fails loudly instead of double-patching."""
import pathlib, sys
SRC = pathlib.Path(__file__).resolve().parent.parent / 'src'


def rep(s, old, new, n=1):
    c = s.count(old)
    if c != n: sys.exit('expected %d match(es), got %d for:\n%s' % (n, c, old[:200]))
    return s.replace(old, new)


p = SRC / 'app_script.html'; s = p.read_text(encoding='utf-8')

# ---------- constants ----------
s = rep(s, "const PPS = ST.filter(s => s.pp);", """const PPS = ST.filter(s => s.pp && !s.twin);
const TYPES = [
  ['hx', '🗣️', 'History', 'History', 'Take a focused history, then present to the examiner. No examination, no counselling.'],
  ['ex', '🩺', 'Examination', 'Exam', 'Examine, then present your findings and how you would complete it.'],
  ['img', '🖼️', 'Imaging and ECG', 'Imaging', 'Present a chest X-ray, abdominal X-ray, CT or ECG systematically.'],
  ['drug', '💊', 'Drug counselling', 'Drugs', 'Why → How → Watch → Check, with the patient.'],
  ['comm', '💬', 'Communication', 'Comms', 'Bad news, explaining a diagnosis, antibiotics, and the harder conversations.'],
  ['proc', '🧪', 'Procedures', 'Procedures', 'Every FFP DOPS step by step, with what to say and the pictures.'],
  ['psych', '🧠', 'Psychiatry', 'Psych', 'Mental health history, MSE, risk and suicide risk.']];
const TY = {}; TYPES.forEach(t => TY[t[0]] = {id: t[0], i: t[1], t: t[2], nav: t[3], d: t[4]});
const TALK = new Set(['hx', 'drug', 'comm', 'psych', 'img']);
const typeOf = s => s.type || 'hx';
const FFP = D.ffp || [];
const HOW = {
  hx: ['Read the door: who, where, what they came with.', 'Open question, then listen for the golden minute.', 'Focused questions to split your top 3 differentials, plus red flags.', 'ICE, then PMH, drugs, allergies, family and social history.', 'At 8 minutes stop and turn to the examiner: summary → diagnosis and why → what to exclude → first tests.'],
  ex: ['WIPER: wash, introduce, permission, expose, reposition.', 'Look from the end of the bed, then the system in order.', 'Say what you see as you go.', 'Finish by 7 minutes; thank and cover.', 'Present: positives, key negatives, diagnosis, and how you would complete it.'],
  img: ['Details: name, date, type of film or scan.', 'Quality checks.', 'A fixed system: the same order every time.', 'The key finding, then the diagnosis.', 'The next step.'],
  drug: ['What they know and what worries them.', 'Why: the condition and how the drug helps.', 'How: dose, timing, how long.', 'Watch: side effects, red flags, monitoring.', 'Check: teach-back, leaflet, follow-up.'],
  comm: ['Set up and find out what they know.', 'Signpost, then chunk and check.', 'Respond to emotion.', 'A clear plan.', 'Summary, teach-back and safety-net.'],
  proc: ['ID, explain, consent, allergies.', 'Equipment and hand hygiene.', 'The steps in order, saying what you are doing.', 'Sharps and waste.', 'Document and act on the result.'],
  psych: ['Rapport and confidentiality.', 'Story, mood, anxiety, psychosis, mania, substances.', 'Risk: to self, to others, from others.', 'Background and life story.', 'Present: summary, diagnosis, risk level, plan.']};""")
s = rep(s, "const APP_NAME = 'medengine-OSCE', APP_VERSION = '0.6.0-beta',", "const APP_NAME = 'medengine-OSCE', APP_VERSION = '1.3.0',")

# ---------- checklist, hooks and script: new single-task stations carry their own sections ----------
s = rep(s, "const ORDER = ['hx', 'mhx', 'ex', 'proc', 'di', 'presc', 'counsel', 'bbn', 'expl', 'acute', 'prof', 'sbar', 'ebm', 'reason', 'plan'];",
        "const ORDER = ['hx', 'mhx', 'ex', 'proc', 'di', 'presc', 'counsel', 'bbn', 'expl', 'acute', 'prof', 'sbar', 'ebm', 'reason', 'plan', 'pres'];")
s = rep(s, "function varOf(st, vk){ if (!st.pp) return null;", "function varOf(st, vk){ if (!(st.vars || []).length) return null;")
s = rep(s, """  add('open', 'Opening', frameItems('open'));
  if (st.pp) {""", """  if (st.secs) {
    const w = st.wrap || ['open', 'close'];
    add(w[0], FR[w[0]].t, frameItems(w[0]));
    st.secs.forEach((sc, i) => add('s' + i, sc.h, sc.items, i === 0));
    const v = varOf(st, vk); if (v && v.x) add('vx', 'This case: what the examiner wants', splitX(v.x).map(t => ({t})));
    add(w[1], FR[w[1]].t, frameItems(w[1]));
    return secs;
  }
  add('open', 'Opening', frameItems('open'));
  if (st.pp) {""")
s = rep(s, "function hooksFor(st, vk){\n", "function hooksFor(st, vk){\n  if (st.secs) return {trig: [], hook: st.hooks || [], clinch: [], money: moneyFor(st, vk), trap: st.traps || [], all: []};\n")
s = rep(s, """  fl('open', 'Open', true);
  if (st.pp) {""", """  if (st.secs) {
    const w = st.wrap || ['open', 'close'];
    fl(w[0], 'Open', true);
    st.secs.forEach(sc => sc.items.forEach(it => L.push({s: sc.h, say: it.say || '', act: it.t, why: it.why || '', nn: it.w === 2})));
    fl(w[1], 'Close', true);
    return L;
  }
  fl('open', 'Open', true);
  if (st.pp) {""")
s = rep(s, "    const body = l.say ? '<div class=\"say\">🗣 “' + rich(l.say) + '”</div>' : '<div class=\"say do\">' + rich(l.act || '') + '</div>';",
        "    const body = (l.say && l.act ? '<div class=\"say do\">' + rich(l.act) + '</div>' : '') + (l.say ? '<div class=\"say\">🗣 “' + rich(l.say) + '”</div>' : '<div class=\"say do\">' + rich(l.act || '') + '</div>');")
s = rep(s, "  return '<div class=\"row\"><h2 class=\"grow\">📜 Script: what to say and why</h2>", "  return '<div class=\"row\"><h2 class=\"grow\">📜 What to do, what to say, and why</h2>")

# ---------- routing ----------
s = rep(s, "const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual'];", "const VIEWS = ['home', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp'];")
s = rep(s, "  if ((m = h.match(/^e-(\\w+)$/)) && exById[m[1]]) return {v: 'exam', id: m[1]};\n  if ((m = h.match(/^p-(\\w+)$/)) && prById[m[1]]) return {v: 'proc', id: m[1]};",
        "  if ((m = h.match(/^t-(\\w+)$/)) && TY[m[1]]) return {v: 'type', id: m[1]};\n  if ((m = h.match(/^e-(\\w+)$/)) && (D.exmap || {})[m[1]] && getStation(D.exmap[m[1]])) return {v: 'station', id: D.exmap[m[1]]};\n  if ((m = h.match(/^p-(\\w+)$/)) && (D.prmap || {})[m[1]] && getStation(D.prmap[m[1]])) return {v: 'station', id: D.prmap[m[1]]};\n  if ((m = h.match(/^e-(\\w+)$/)) && exById[m[1]]) return {v: 'exam', id: m[1]};\n  if ((m = h.match(/^p-(\\w+)$/)) && prById[m[1]]) return {v: 'proc', id: m[1]};")
s = rep(s, "function toHash(r){ return r.v === 'station' ? 's-' + r.id :", "function toHash(r){ return r.v === 'type' ? 't-' + r.id : r.v === 'station' ? 's-' + r.id :")
s = rep(s, "function leaveStation(){ stopTimer(); abortChat();", "function leaveStation(){ if (window.DG) DG.stopAll(); stopTimer(); abortChat();")
s = rep(s, """  const navKey = {station: 'stations', exam: 'exams', proc: 'dops', ilo: 'ilos', frame: 'skills', fwone: 'fw', visual: 'fw'}[route.v] || route.v;
  $$('#nav button').forEach(b => b.classList.toggle('on', b.dataset.v === navKey));
  ({home: vHome,""", """  const st0 = route.v === 'station' ? getStation(route.id) : null;
  const navKey = route.v === 'type' ? 'ty:' + route.id : st0 ? 'ty:' + typeOf(st0) : route.v === 'exam' ? 'ty:ex' : route.v === 'proc' ? 'ty:proc' : route.v === 'home' || route.v === 'ffp' ? 'home' : '';
  $$('#nav button').forEach(b => b.classList.toggle('on', (b.dataset.ty ? 'ty:' + b.dataset.ty : b.dataset.v) === navKey));
  ({type: vType, ffp: vFfp, home: vHome,""")

# ---------- views: new home, type lists, FFP checklist ----------
s = rep(s, "function vHome(m){", r"""const doneOf = id => best(id) != null;
const stTitle = s => s.t;
function stRow(s, showCode){
  const n = (s.vars || []).length, cs = (s.cases || []).length;
  const sub = s.sub || (s.secs ? (s.ffp ? '✅ FFP: ' + s.ffp : '') : s.u.length && UNITS[s.u[0]] ? UNITS[s.u[0]].name : '');
  return '<button class="li" data-st="' + s.id + '">' + (showCode && s.pp ? '<span class="code">' + esc(s.id.replace(/-x$/, '')) + '</span>' : '<span class="code ty">' + TY[typeOf(s)].i + '</span>') + '<span class="tt"><b>' + esc(stTitle(s)) + '</b><span>' + esc(sub) + (n > 1 ? ' · ' + n + ' cases' : '') + (cs ? ' · ' + cs + ' cases to present' : '') + ((s.dg || []).length ? ' · 🖼️ ' + s.dg.length : '') + '</span></span>' + scoreHtml(s.id) + '</button>';
}
function ffpDone(){ let n = 0, t = 0; FFP.forEach(sec => sec.items.forEach(it => { t++; if (it.s.some(doneOf)) n++; })); return [n, t]; }
function ffpHtml(open){
  const [n, t] = ffpDone();
  return '<details class="dd ffp"' + (open ? ' open' : '') + '><summary>✅ FFP checklist <span class="hint">· ' + n + ' of ' + t + ' practised</span></summary><div class="body">' + FFP.map(sec => '<div class="ffps"><span class="hkh">' + esc(sec.h) + '</span><div class="chips">' + sec.items.map(it => { const b = Math.max(...it.s.map(id => best(id) == null ? -1 : best(id))); return '<button class="chip' + (b >= 0 ? ' did' : '') + '" data-st="' + it.s[0] + '">' + (b >= 0 ? '✓ ' : '') + esc(it.n) + (b >= 0 ? ' · ' + b + '%' : '') + '</button>' + (it.s.length > 1 ? it.s.slice(1).map(id => '<button class="chip sm" data-st="' + id + '">+ ' + esc(stById[id] ? stById[id].t.replace(/^.*?:\s*/, '') : id) + '</button>').join('') : ''); }).join('') + '</div></div>').join('') + '</div></details>';
}
function vFfp(m){ m.innerHTML = '<section class="card"><h1>✅ FFP checklist</h1><p class="hint" style="margin:0">Your paper checklist, every item linked to its station. A tick means you have saved an attempt.</p></section>' + ffpHtml(true); }
function vHome(m){
  const all = Object.entries(S.att).flatMap(([id, a]) => a.map(x => Object.assign({id}, x))).sort((a, b) => b.ts - a.ts);
  const [fn, ft] = ffpDone();
  let h = '<section class="card hero"><span class="eyebrow">' + APP_NAME + ' v1.3 · FFP CPSA · one station, one task</span><h1>What kind of station?</h1><p class="hint" style="margin:0">Every station is a single 10-minute task, the way FFP runs them. Open one, read the door, then pick 📜 <b>Script</b> to learn it, ✅ <b>Tick</b> to mark yourself, 👥 <b>Friends</b> to run it together, or 🤖 <b>AI</b> on the talking stations.</p><div class="row"><button class="btn primary" data-rand>🎲 Random FFP station</button>' + (all.length ? '<button class="btn" data-st="' + all[0].id + '">↩︎ Back to the last one</button>' : '') + '<span class="hint">' + fn + ' of ' + ft + ' FFP items practised</span></div></section>';
  h += '<section class="tiles">' + TYPES.map(([k]) => { const L = ST.filter(s => typeOf(s) === k), core = L.filter(s => s.core || s.pp).length, done = L.filter(s => doneOf(s.id)).length; return '<button class="tile ty-' + k + '" data-ty="' + k + '"><span class="tic">' + TY[k].i + '</span><b>' + esc(TY[k].t) + '</b><span class="hint">' + esc(TY[k].d) + '</span><span class="tmeta">' + L.length + ' stations' + (done ? ' · ' + done + ' practised' : '') + '</span><span class="tbar"><i style="width:' + (L.length ? Math.round(done * 100 / L.length) : 0) + '%"></i></span></button>'; }).join('') + '</section>';
  h += ffpHtml(false);
  if (all.length) { const ML = {ai: '🤖 AI-marked', voice: '🎙 Voice-marked', friends: '👥 Friend-marked', tick: '✅ Self-marked'}; h += '<section class="card"><h2>Recent attempts</h2><div class="list">' + all.slice(0, 5).map(a => { const s = getStation(a.id); return s ? '<button class="li" data-st="' + a.id + '"><span class="code ty">' + TY[typeOf(s)].i + '</span><span class="tt"><b>' + esc(s.t) + '</b><span>' + (ML[a.mode] || ML.tick) + ' · ' + new Date(a.ts).toLocaleDateString('en-GB') + '</span></span><span class="score ' + scoreCls(a.pct) + '">' + a.pct + '%</span></button>' : ''; }).join('') + '</div></section>'; }
  if (!PUBLIC) h += '<details class="dd"><summary>🎯 Your feedback priorities</summary><div class="body">' + PRIOS.map(([t, d, ids], i) => '<div class="prio"><span class="n">' + (i + 1) + '</span><div><b>' + esc(t) + '</b><div class="hint">' + esc(d) + '</div><div class="chips" style="margin-top:4px">' + ids.filter(x => stById[x]).map(x => '<button class="chip" data-st="' + x + '">' + esc(stById[x].t) + (best(x) != null ? ' ' + best(x) + '%' : '') + '</button>').join('') + '</div></div></div>').join('') + '</div></details>';
  h += '<div class="row more"><span class="hint">More:</span><button class="btn sm" data-go="hooks">🪝 Hook drill</button><button class="btn sm" data-go="ilos">🧩 ILO packs</button><button class="btn sm" data-go="fw">🧭 Frameworks</button><button class="btn sm" data-go="skills">🗣 How you\'re marked</button><button class="btn sm" data-go="visual">👁️ Showdowns</button></div>';
  m.innerHTML = h;
}
function sysOf(s){ const u = (s.u || []).find(i => UNITS[i]); return u == null ? 'other' : MEV.unitSys(u, UNITS[u].w); }
function groupHtml(title, L, open, code){ return L.length ? '<details class="dd grp"' + (open ? ' open' : '') + '><summary>' + title + ' <span class="hint">· ' + L.length + '</span></summary><div class="body"><div class="list">' + L.map(s => stRow(s, code)).join('') + '</div></div></details>' : ''; }
function bySystem(L, open, code){ const g = {}; L.forEach(s => (g[sysOf(s)] = g[sysOf(s)] || []).push(s)); return MEV.SYS.map(([k, lab]) => g[k] ? groupHtml(esc(lab), g[k], open, code) : '').join('') + (g.other ? groupHtml('Other', g.other, open, code) : ''); }
function vType(m){
  const k = route.id, T = TY[k], q = (S.set['tq_' + k] || '').toLowerCase().trim();
  const hit = s => !q || q.split(/\s+/).every(w => (s.t + ' ' + (s.sub || '') + ' ' + (s.ffp || '') + ' ' + s.id + ' ' + (s.u || []).map(i => UNITS[i] ? UNITS[i].name : '').join(' ')).toLowerCase().includes(w));
  const L = ST.filter(s => typeOf(s) === k && hit(s));
  let h = '<section class="card"><span class="eyebrow">' + T.i + ' ' + esc(T.t) + ' stations · 10 minutes · one task</span><h1>' + esc(T.t) + '</h1><p class="hint" style="margin:0">' + esc(T.d) + '</p><div class="howto">' + HOW[k].map((x, i) => '<span><b>' + (i + 1) + '</b>' + esc(x) + '</span>').join('') + '</div><div class="row"><input class="sel" id="tQ" type="search" placeholder="Filter: a condition, a drug, a sign…" value="' + esc(S.set['tq_' + k] || '') + '" aria-label="Filter stations"><button class="btn sm" data-randty="' + k + '">🎲 Random</button></div></section><div id="tList">' + typeListHtml(k, L, !!q) + '</div>';
  m.innerHTML = h;
}
function typeListHtml(k, L, open){
  const core = L.filter(s => s.core), pp = L.filter(s => s.pp && !s.core), bank = L.filter(s => !s.core && !s.pp);
  let h = '';
  if (k === 'ex') return ['Medicine', 'Surgery', 'Speciality'].map(g => groupHtml(g, core.filter(s => s.grp === g), true)).join('') || '<div class="empty">No stations match.</div>';
  if (k === 'proc' || k === 'img') return groupHtml(k === 'proc' ? 'FFP DOPS and procedures' : 'FFP imaging', core, true) || '<div class="empty">No stations match.</div>';
  if (core.length) h += groupHtml('✅ The FFP list', core, true);
  if (k === 'hx') h += '<h2 class="lh">⭐ Past-paper histories <span class="hint">with an actor story for every case</span></h2>' + bySystem(pp, open, true) + (bank.length ? '<h2 class="lh">More presentations <span class="hint">from your ILO bank</span></h2>' + bySystem(bank, open) : '');
  else h += groupHtml('⭐ Past-paper stations', pp, open || !core.length, true) + groupHtml('More practice', bank, open);
  return h || '<div class="empty">No stations match.</div>';
}
function vHome0(m){""")
s = rep(s, "function kindOf(s){ const k = s.k.toLowerCase();", "function kindOf(s){ if (s.type) return TY[s.type].t; const k = (s.k || '').toLowerCase();")

# ---------- station page ----------
s = rep(s, "const MODES = [['script', '📜 Script'], ['tick', '✅ Tick'], ['friends', '👥 Friends'], ['ai', '🤖 AI text'], ['voice', '🎙 Voice']];",
        "const MODES = [['script', '📜 Script'], ['tick', '✅ Tick'], ['friends', '👥 Friends'], ['ai', '🤖 AI text'], ['voice', '🎙 Voice']];\nconst modesFor = st => TALK.has(typeOf(st)) ? MODES : MODES.filter(([k]) => k !== 'ai' && k !== 'voice');")
s = rep(s, "  if (!st.pp) return secs.filter(s => s.key !== 'open' && s.key !== 'close').map(s => ({h: s.h, items: s.items.slice(0, 6)}));",
        "  if (!st.pp) { const ds = secs.filter(s => !/^(open|close|xopen|xclose|popen|pclose|vx)$/.test(s.key)).map(s => ({h: s.h, items: s.items.slice(0, 6)})); return TALK.has(typeOf(st)) ? [DPROF, DCOMM].concat(ds).slice(0, 7) : [DPROF].concat(ds).slice(0, 7); }")
s = rep(s, """  const vk0 = st.pp ? (st.vars[0].k) : null;
  cur = {st, vk: vk0, hidden: false, secs: buildChecklist(st, vk0), ticks: new Set(), ai: new Set(), chat: [], mode: S.set.mode, left: 600, fb: null, lik: {}};
  if ((cur.mode === 'ai' || cur.mode === 'voice') && sampleChecked && !SAMPLE) cur.mode = 'script';
  const pk = packFor(st);
  let h = '<section class="card"><div class="row"><span class="code">' + esc(st.id) + '</span><span class="hint">' + (st.pp ? '📚 Past paper · ' : '') + esc(kindOf(st)) + '</span>' + (best(st.id) != null ? '<span class="score ' + scoreCls(best(st.id)) + '">best ' + best(st.id) + '%</span>' : '') + '</div><h1>' + esc(st.t) + '</h1>' + (st.src ? '<span class="src">Source: ' + esc(st.src) + '</span>' : '') + '<div class="chips">' + iloChips(st.u) + (st.ex || []).map(e => exById[e] ? '<button class="chip" data-ex="' + e + '">🩺 ' + esc(exById[e].t) + '</button>' : '').join('') + (st.pr || []).map(p => prById[p] ? '<button class="chip" data-pr="' + p + '">💉 ' + esc(prById[p].t) + '</button>' : '').join('') + '</div>';
  h += atlasFor(st.u, st.u.length && UNITS[st.u[0]] ? UNITS[st.u[0]].name : st.t, st.t);
  if (st.pp && st.vars.length) h +=""", """  const vk0 = (st.vars || []).length ? st.vars[0].k : null;
  cur = {st, vk: vk0, hidden: false, secs: buildChecklist(st, vk0), ticks: new Set(), ai: new Set(), chat: [], mode: S.set.mode, left: 600, fb: null, lik: {}};
  if ((cur.mode === 'ai' || cur.mode === 'voice') && sampleChecked && !SAMPLE) cur.mode = 'script';
  if (!modesFor(st).some(([k]) => k === cur.mode)) cur.mode = 'script';
  const pk = packFor(st), ty = TY[typeOf(st)];
  let h = '<section class="card"><div class="row"><button class="chip typill" data-ty="' + ty.id + '">' + ty.i + ' ' + esc(ty.t) + '</button>' + (st.pp ? '<span class="code">' + esc(st.id.replace(/-x$/, '')) + '</span><span class="hint">📚 past paper</span>' : '') + (st.ffp ? '<span class="hint">✅ FFP: ' + esc(st.ffp) + '</span>' : '') + (best(st.id) != null ? '<span class="score ' + scoreCls(best(st.id)) + '">best ' + best(st.id) + '%</span>' : '') + '</div><h1>' + esc(st.t) + '</h1>' + (st.sub && !st.core ? '<span class="src" id="stSub">' + esc(st.sub) + '</span>' : '') + '<div class="chips">' + iloChips((st.u || []).slice(0, 4)) + '</div>';
  if (ty.id === 'ex' || ty.id === 'img') h += atlasFor(st.u, st.u.length && UNITS[st.u[0]] ? UNITS[st.u[0]].name : st.t, st.t);
  if ((st.vars || []).length) h +=""")
s = rep(s, """  h += '<div class="brief"><span class="eyebrow">Candidate information</span><p id="briefP">' + esc(st.info) + '</p>' + (st.task ? '<p class="task">' + esc(st.task) + '</p>' : '') + '</div><div id="resWrap"></div>';""",
        """  h += '<div class="brief"><span class="eyebrow">Candidate information</span><p id="briefP">' + esc(st.info) + '</p>' + (st.task ? '<p class="task">' + esc(st.task) + '</p>' : '') + '<div id="caseImg"></div></div><div id="resWrap"></div>';""")
s = rep(s, """  h += '<div class="row"><div class="seg" id="modeSeg">' + MODES.map(""", """  h += '<div class="row"><div class="seg" id="modeSeg">' + modesFor(st).map(""")
s = rep(s, """  h += '<div id="fwWrap"></div><div id="hookWrap"></div>';
  h += '<section class="card" id="scriptCard"></section>';""", """  h += '<div id="fwWrap"></div><div id="hookWrap"></div><div id="dgWrap"></div>';
  h += '<section class="card" id="casesCard" hidden></section>';
  h += '<section class="card" id="scriptCard"></section>';""")
s = rep(s, "  $('#fwWrap').innerHTML = fwCard(st);\n", """  $('#fwWrap').innerHTML = st.secs || st.type ? '' : fwCard(st);
  const ci = $('#caseImg'); if (ci) ci.innerHTML = v && v.img && window.DG ? DG.img(v.img) : '';
  $('#dgWrap').innerHTML = dgCardHtml(st);
  const cc = $('#casesCard'); if (cc) { cc.innerHTML = casesHtml(st); }
""")
s = rep(s, "  $('#clCard').innerHTML = '<div class=\"row\"><h2 class=\"grow\">Mark scheme</h2>", "  $('#clCard').innerHTML = '<div class=\"row\"><h2 class=\"grow\">✅ Mark scheme</h2>")
s = rep(s, """    if (st.def) mh += '<details class="dd" open><summary>🧭 Default instruction</summary>""", """    if (st.secs && v) mh += '<details class="dd"' + (cur.hidden ? '' : ' open') + '><summary>🧭 This case' + (cur.hidden ? '' : ': ' + esc(v.dx)) + '</summary><div class="body"><p style="margin:0">' + rich(v.x) + '</p></div></details>';
    if (st.money && st.secs) mh += '<div class="money"><b>🎯 Model answer</b>' + rich(moneyFor(st, cur.vk)) + '</div>';
    if (st.def) mh += '<details class="dd" open><summary>🧭 Default instruction</summary>""")
s = rep(s, """  $('#modelCard').hidden = cand || (md === 'ai' || md === 'voice') && !cur.fb;
  $('#hookWrap').hidden = cand;""", """  $('#modelCard').hidden = cand || (md === 'ai' || md === 'voice') && !cur.fb;
  $('#hookWrap').hidden = cand;
  $('#dgWrap').hidden = cand || ((md === 'ai' || md === 'voice') && !cur.fb);
  const dc = $('#dgCard'); if (dc) dc.open = md === 'script' || md === 'tick';
  $('#casesCard').hidden = !(md === 'script' && (cur.st.cases || []).length);""")

# pictures card and practice cases
s = rep(s, "function curVar(){ return varOf(cur.st, cur.vk); }", r"""function curVar(){ return varOf(cur.st, cur.vk); }
function dgCardHtml(st){
  const ids = (st.dg || []).filter(id => window.DG && DG.has(id)); if (!ids.length) return '';
  const i = Math.min(cur.dg || 0, ids.length - 1);
  return '<details class="hk dgc" id="dgCard" open><summary>🖼️ Pictures <span class="hint">· ' + ids.length + ' · tap ▶ to play, or swipe</span></summary><div class="body">' + (ids.length > 1 ? '<div class="chips dgchips">' + ids.map((id, k) => '<button class="chip' + (k === i ? ' on' : '') + '" data-dgpick="' + k + '">' + esc(DG.title(id).split(':')[0]) + '</button>').join('') + '</div>' : '') + '<div id="dgOne">' + DG.html(ids[i]) + '</div></div></details>';
}
function casesHtml(st){
  const C = st.cases || []; if (!C.length) return '';
  return '<h2>🎤 Present these findings <span class="hint">· ' + C.length + '</span></h2><p class="hint" style="margin:0">Read the findings, say your presentation out loud, then reveal the model.</p><div class="cases">' + C.map((c, k) => '<div class="case"><span class="n">' + (k + 1) + '</span><div><div class="f">' + rich(c.f) + '</div><button class="rev" data-reveal>Say it, then tap to reveal</button><div hidden><div class="money"><b>' + esc(c.dx) + '</b>' + rich(c.p) + '</div></div></div></div>').join('') + '</div>';
}""")

# AI: the imaging station is an examiner viva
s = rep(s, "function patientRules(st, voice){\n  const pk = packFor(st), p = pk ? pk.p : {}, v = curVar();", """function patientRules(st, voice){
  const pk = packFor(st), p = pk ? pk.p : {}, v = curVar();
  if (typeOf(st) === 'img') return 'You are a fair UK OSCE EXAMINER for the University of Nottingham Foundations for Practice CPSA (fourth-year medical students). This is an imaging and data interpretation station: ' + st.t + '. The candidate is looking at ' + (v ? 'the image for ' + v.who : 'an image') + '. What it shows (never say this unless the candidate has already said it): ' + (v ? v.r + ' Diagnosis: ' + v.dx + '. What the examiner wants: ' + v.x : '') + '\\n' + (voice ? 'SPOKEN STATION: reply in one or two short spoken sentences, no markdown.\\n' : '') + 'RULES:\\n- Start every reply with [Examiner].\\n- Let the candidate present. Answer factual questions about the clinical context briefly.\\n- When they finish or stall, ask one short follow-up question at a time, chosen from: ' + (st.ask || []).join(' | ') + '.\\n- Never coach, hint, praise, or give the diagnosis. Never mention you are an AI.\\nReply with ONLY your next line.';""")

# ---------- events ----------
s = rep(s, "  if (d.v) { if (d.v === 'hooks') deck = null; return go({v: d.v}); }", """  if (d.ty && !d.st) return go({v: 'type', id: d.ty});
  if (d.randty) { const l = ST.filter(s => typeOf(s) === d.randty && (s.core || s.pp)); const n = l.filter(s => best(s.id) == null); const p = n.length ? n : l; return go({v: 'station', id: p[Math.floor(Math.random() * p.length)].id}); }
  if (d.rand != null) { const ids = FFP.flatMap(x => x.items.flatMap(it => it.s)); const n = ids.filter(id => best(id) == null); const p = n.length ? n : ids; return go({v: 'station', id: p[Math.floor(Math.random() * p.length)]}); }
  if (d.dgpick != null) { cur.dg = +d.dgpick; if (window.DG) DG.stopAll(); $('#dgWrap').innerHTML = dgCardHtml(cur.st); return; }
  if (d.v) { if (d.v === 'hooks') deck = null; return go({v: d.v}); }""")
s = rep(s, "document.addEventListener('input', e => { if (e.target.id === 'hQ') {", "document.addEventListener('input', e => { if (e.target.id === 'tQ') { S.set['tq_' + route.id] = e.target.value; clearTimeout(vType.t); vType.t = setTimeout(() => { save(); const k = route.id, q = e.target.value.toLowerCase().trim(); const L = ST.filter(s => typeOf(s) === k && (!q || q.split(/\\s+/).every(w => (s.t + ' ' + (s.sub || '') + ' ' + (s.ffp || '') + ' ' + s.id + ' ' + (s.u || []).map(i => UNITS[i] ? UNITS[i].name : '').join(' ')).toLowerCase().includes(w)))); $('#tList').innerHTML = typeListHtml(k, L, !!q); }, 180); return; } if (e.target.id === 'hQ') {")
p.write_text(s, encoding='utf-8')

# ---------- head: nav, version, styles ----------
p = SRC / 'app_head.html'; h = p.read_text(encoding='utf-8')
h = rep(h, """    <button data-v="home">🏠 Today</button>
    <button data-v="stations">📋 Stations</button>
    <button data-v="fw">🧭 Frameworks</button>
    <button data-v="hooks">🪝 Hooks</button>
    <button data-v="exams">🩺 Exams</button>
    <button data-v="dops">💉 DOPS</button>
    <button data-v="ilos">🧩 ILOs</button>
    <button data-v="skills">🗣 Skills</button>""", """    <button data-v="home">🏠 Home</button>
    <button data-ty="hx">🗣️ History</button>
    <button data-ty="ex">🩺 Exam</button>
    <button data-ty="img">🖼️ Imaging</button>
    <button data-ty="drug">💊 Drugs</button>
    <button data-ty="comm">💬 Comms</button>
    <button data-ty="proc">🧪 Procedures</button>
    <button data-ty="psych">🧠 Psych</button>""")
h = rep(h, '<span class="ver">v1.0.0</span>', '<span class="ver">v1.3.0</span>')
h = rep(h, '    <input class="search" id="q" type="search" placeholder="Search stations, exams, DOPS, ILOs…"', '    <input class="search" id="q" type="search" placeholder="Search any station, drug or sign…"')
h = rep(h, "#atlasQ{flex:1 1 220px;min-height:38px}\n", """#atlasQ{flex:1 1 220px;min-height:38px}
/* v1.3: FFP layout */
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,210px),1fr));gap:10px}
.tiles .tile{gap:4px;position:relative;overflow:hidden}
.tiles .tic{font-size:1.6rem;line-height:1.1}
.tiles .tmeta{font-family:var(--f-mono);font-size:.72rem;color:var(--muted);margin-top:auto}
.tbar{display:block;height:4px;border-radius:2px;background:var(--line);overflow:hidden}.tbar i{display:block;height:100%;background:var(--accent)}
.hero h1{font-size:1.7rem}
.howto{display:flex;flex-wrap:wrap;gap:6px}.howto span{display:flex;gap:6px;align-items:baseline;background:var(--surface-2);border:1px solid var(--line);border-radius:9px;padding:5px 9px;font-size:.86rem;flex:1 1 200px}.howto b{font-family:var(--f-mono);color:var(--accent-ink)}
#tQ{flex:1 1 220px;min-height:38px}
.lh{margin:10px 2px 2px;font-size:1.05rem}
.grp>summary{font-weight:700}
.code.ty{font-size:1rem;background:none;border:0;padding:0;min-width:1.6em;text-align:center}
.chip.did{border-color:var(--good);color:var(--good)}.chip.sm{font-size:.78rem;opacity:.85}
.ffps{display:flex;flex-direction:column;gap:4px;margin-bottom:6px}
.typill{font-weight:700}
.dgchips .chip.on{border-color:var(--accent);background:var(--accent-soft);color:var(--accent-ink)}
.dgc .body{display:flex;flex-direction:column;gap:8px}
.cases{display:flex;flex-direction:column;gap:8px}.case{display:flex;gap:10px;border:1px solid var(--line);border-radius:10px;padding:10px;background:var(--surface-2)}.case .n{font-family:var(--f-mono);font-weight:700;color:var(--accent-ink)}.case .f{margin-bottom:6px}
#caseImg .dg-img{margin-top:8px}
.more{gap:6px}
""")
p.write_text(h, encoding='utf-8')
print('patched')
