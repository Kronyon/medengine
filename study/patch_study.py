#!/usr/bin/env python3
"""Builds medengine-STUDY v0.8 from the v0.5 page (base_v050.html) without touching the notes.

Adds: the shared visual layer (mev.css/mev.js: Clinical Atlas Lookup + Visual Showdowns), guideline updates
(content/updates_2026.json, shared with medengine-OSCE), 1st-line action/investigation per ILO (from the
OSCE packs, for the sniper), systems & presentations dropdowns, the screenshot vault and the blind clincher
sniper (ext_study.js/.css). v0.7 (v07_content.json, ext_v07.js/.css): dual-code clinchers, the Jargon Decoder,
the 3-way triangulation sniper and the WPW vs LBBB showdown. v0.8 (v08_content.json, ext_v08.js/.css): Remix
(missed question -> 3 one-change variations, AI or offline) and speed tags. Saved progress keys are unchanged (qq-drill-ilo-v1).

Usage: python3 patch_study.py [--osce /home/claude/osce] [--out index.html]
"""
import json, re, sys, pathlib, argparse

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--osce', default='/home/claude/osce')
ap.add_argument('--base', default=str(HERE / 'base_v050.html'))
ap.add_argument('--out', default=str(HERE / 'index.html'))
a = ap.parse_args()
OSCE = pathlib.Path(a.osce)
MEDAPP = pathlib.Path('/home/claude/medengine/app')  # shared pictures and schematics live with medengine-OSCE

html = open(a.base, encoding='utf-8').read()
UPD = json.load(open(OSCE / 'content' / 'updates_2026.json', encoding='utf-8'))
PK = json.load(open(OSCE / 'build' / 'osce_data_v3.json', encoding='utf-8'))['packs']


def rep(old, new, n=1):
    global html
    c = html.count(old)
    if c != n:
        raise SystemExit(f'expected {n} of {old[:80]!r}, found {c}')
    html = html.replace(old, new)


# ---------- data ----------
m = re.search(r'<script id="qqdata" type="application/json">(.*?)</script>', html, re.S)
D = json.loads(m.group(1))
U, K = D['units'], D['key']
for op in UPD['ops']:
    if op['field'] != 'ck':
        continue
    u = U[op['u']]
    if 'add' in op:
        K.append(list(op['add'])); u['ck'].append(len(K) - 1)
        continue
    hits = [i for i in u['ck'] if op['old'] in K[i][1]]
    if len(hits) != 1:
        raise SystemExit(f"clincher update for unit {op['u']} matched {len(hits)}")
    K[hits[0]][1] = K[hits[0]][1].replace(op['old'], op['new'])
for name, edits in UPD['study'].items():
    if name == 'lines':
        continue
    for idx, (old, new) in edits.items():
        item = D[name][int(idx)]
        if name == 'hunt':
            hit = [j for j, x in enumerate(item) if isinstance(x, str) and old in x]
            if len(hit) != 1: raise SystemExit(f'hunt {idx} update matched {len(hit)}')
            item[hit[0]] = item[hit[0]].replace(old, new)
        elif name == 'why':
            hit = [j for j, x in enumerate(item['a']) if old in x]
            if len(hit) != 1: raise SystemExit(f'why {idx} update matched {len(hit)}')
            item['a'][hit[0]] = item['a'][hit[0]].replace(old, new)
D['upd'] = UPD['study']['lines']
# ---------- v0.7 content: dual-code clinchers + Jargon Decoder ----------
V7 = json.load(open(HERE / 'v07_content.json', encoding='utf-8'))
UBY = {}
for i, u in enumerate(U): UBY.setdefault(u['name'], i)
for idx, text in V7['ck_dual'].items():
    k = int(idx)
    assert any(k in u['ck'] for u in U), f'clincher {k} not used'
    K[k][1] = text
for name, typ, text in V7['ck_add']:
    assert name in UBY, name
    K.append([typ, text]); U[UBY[name]]['ck'].append(len(K) - 1)
JGD = []
for j in V7['jg']:
    us = [UBY[n] for n in j['u']]
    assert len(us) == len(j['u']), j['t']
    e = {k2: j[k2] for k2 in ('t', 'al', 'f', 'h', 'x', 'm') }
    e['u'] = us
    for k2 in ('ecg', 'sd'):
        if j.get(k2): e[k2] = j[k2]
    JGD.append(e)
D['jg'] = JGD
V8 = json.load(open(HERE / 'v08_content.json', encoding='utf-8'))
D['spdl'] = V8['spd_labels']
# v1.0: new mechanism cards (own words) appended to the Pathoma library and linked to their ILO units
V10 = json.load(open(HERE / 'v10_content.json', encoding='utf-8'))
_ids = {r['id'] for r in D['path']}
for r in V10['path_add']:
    if r['id'] in _ids: raise SystemExit('duplicate Pathoma id ' + r['id'])
    if '—' in json.dumps(r, ensure_ascii=False): raise SystemExit('em dash in ' + r['id'])
    D['path'].append({'id': r['id'], 't': r['t'], 'l': r['l'], 'u': r['u']})
    for ui in r['u']:
        D['units'][ui].setdefault('pa', []).append(len(D['path']) - 1)
rep("""if (pas.length) h += '<div class="panel pap"><b>🧬 Why it happens · Pathoma</b>'""", """if (pas.length) h += '<div class="panel pap"><div class="toolbar"><b class="grow">🧬 Why it happens · Pathoma</b><button class="btn ghost sm" data-go="why">All ' + ROOTS.length + ' cards</button></div>'""")
rep("""  if (!fws.length && !whys.length && !ars.length && !hunts.length) return h ?""", """  h += actPanelHtml(u);
  if (!fws.length && !whys.length && !ars.length && !hunts.length) return h ?""")
# v1.1: every Why it happens card rewritten as movement (one chain per line, arrows, no brackets)
V11 = json.load(open(HERE / 'v11_content.json', encoding='utf-8'))['path_rewrite']
_byid = {r['id']: r for r in D['path']}
if set(V11) != set(_byid): raise SystemExit('v1.1 rewrite does not cover every card: ' + str(set(_byid) ^ set(V11)))
for _id, c in V11.items():
    _byid[_id]['t'] = c['t']; _byid[_id]['l'] = c['l']
# v1.1: new cards for ILO conditions that had none
for r in json.load(open(HERE / 'v11_content.json', encoding='utf-8'))['path_add']:
    if r['id'] in _byid: raise SystemExit('duplicate Pathoma id ' + r['id'])
    D['path'].append({'id': r['id'], 't': r['t'], 'l': r['l'], 'u': r['u']}); _byid[r['id']] = D['path'][-1]
    for ui in r['u']:
        D['units'][ui].setdefault('pa', []).append(len(D['path']) - 1)
# v1.2: ⚡ First move vs cure cards, plus the nerve-injury Why card
V12 = json.load(open(HERE / 'v12_content.json', encoding='utf-8'))
for r in V12['path_add']:
    if r['id'] in _byid: raise SystemExit('duplicate Pathoma id ' + r['id'])
    D['path'].append({'id': r['id'], 't': r['t'], 'l': r['l'], 'u': r['u']}); _byid[r['id']] = D['path'][-1]
    for ui in r['u']: D['units'][ui].setdefault('pa', []).append(len(D['path']) - 1)
D['act'] = []
for r in V12['act']:
    if '\u2014' in json.dumps(r, ensure_ascii=False): raise SystemExit('em dash in ' + r['id'])
    D['act'].append({'id': r['id'], 't': r['t'], 'l': r['l'], 'u': r['u']})
    for ui in r['u']: D['units'][ui].setdefault('acts', []).append(len(D['act']) - 1)
for k, names in V8['spd'].items():
    for n in names:
        assert n in UBY, n
        for u in U:
            if u['name'] == n: u['spd'] = k
# v1.5: 🎞️ Snapshots for every condition (snap/*.py, own words) and the related OSCE pictures per condition
sys.path.insert(0, str(HERE / 'snap'))
import importlib, glob as _glob, snapdsl
for _f in sorted(_glob.glob(str(HERE / 'snap' / 's[0-9]_*.py'))): importlib.import_module(pathlib.Path(_f).stem)
if snapdsl.ERR: raise SystemExit('snapshot errors: ' + '; '.join(snapdsl.ERR))
_miss = [i for i in range(len(U)) if i not in snapdsl.SNAP]
if _miss: raise SystemExit('units without a snapshot: ' + str(_miss))
D['snap'] = {str(k): v for k, v in sorted(snapdsl.SNAP.items())}
# v2.0: 🧭 master posters, shared with medengine-OSCE (snap/master.py)
import master as _master
D['master'] = _master.MASTER
# v2.1: 🧲 Triggers (snap/t_cond, t_bugs, t_drugs, t_ix, t_mx; engine in medengine-OSCE src/trg.js)
import triggers as _trg, hlmark as _hl
_nh = _hl.apply(D)  # v2.2: every word-hunt clue highlighted and stacked by scene
D['trg'] = _trg.build(len(U))
# v2.3: 🔨 Hammer SBAs (snap/hq_*.py) and the mock's own questions (snap/mock92.json + snap/mock_meta.py)
import hammer as _hq, mock_meta as _mm
D['hq'] = _hq.build(U)
D['hq']['al'] = {'61': 1, '88': 50}
_cov = set(_hq.units_covered(D['hq'], U))
_hmiss = [i for i in range(len(U)) if i not in _cov and str(i) not in D['hq']['al']]
if _hmiss: raise SystemExit('units without hammer SBAs: ' + str(_hmiss))
_MQ = json.load(open(HERE / 'snap' / 'mock92.json', encoding='utf-8'))
D['mock'] = {'q': []}
for _q in sorted(_MQ, key=lambda x: int(re.search(r'\d+', x['id']).group())):
    _n = int(re.search(r'\d+', _q['id']).group())
    if _n == 84: continue  # word for word the same as Q83
    _h, _p, _u, _f = _mm.META[_n]
    D['mock']['q'].append({'id': 'm%03d' % _n, 'n': _n, 'ref': _q.get('ref', ''), 's': _q['question'].strip(), 'o': _q['options'], 'a': _q['answer'], 'w': (_q.get('explanation') or '').strip(), 'h': _h, 'p': _p, 'u': _u, 'f': _f})
assert len(D['mock']['q']) == 91, len(D['mock']['q'])
_V4 = json.load(open(MEDAPP / 'build' / 'osce_data_v4.json', encoding='utf-8'))
_dgu = {}
for _st in sorted(_V4['stations'], key=lambda x: (not x.get('core'), x['id'])):
    for _u in _st.get('u', []):
        for _g in _st.get('dg', []):
            _l = _dgu.setdefault(str(_u), [])
            if _g not in _l and len(_l) < 6: _l.append(_g)
D['dgu'] = _dgu
for i, u in enumerate(U):
    p = PK.get(str(i)) or {}
    if p.get('mx'): u['act'] = p['mx'][0].replace('**', '')
    if p.get('ix'): u['ix1'] = p['ix'][0].replace('**', '')
data = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = html[:m.start(1)] + data + html[m.end(1):]

# ---------- shared visual layer + v0.6 styles ----------
mev_css = open(MEDAPP / 'src' / 'mev.css', encoding='utf-8').read()
mev_js = open(MEDAPP / 'src' / 'mev.js', encoding='utf-8').read()
dg_js = '\n'.join(open(MEDAPP / 'src' / f, encoding='utf-8').read() for f in ('dg_core.js', 'dg_cards.js', 'dg_ex.js', 'dg_img.js', 'dg_more.js', 'dg_new.js', 'dg_snap.js', 'dg_poster.js', 'dg_figs.js', 'trg.js'))
ext_css = open(HERE / 'ext_study.css', encoding='utf-8').read()
ext_js = open(HERE / 'ext_study.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v07.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v08.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v11.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v12.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v15.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v20.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v21.js', encoding='utf-8').read() + '\n' + open(HERE / 'ext_v22.js', encoding='utf-8').read()
ext_css += open(HERE / 'ext_v07.css', encoding='utf-8').read() + open(HERE / 'ext_v08.css', encoding='utf-8').read() + open(HERE / 'ext_v11.css', encoding='utf-8').read() + open(HERE / 'ext_v12.css', encoding='utf-8').read() + open(HERE / 'ext_v15.css', encoding='utf-8').read() + open(HERE / 'ext_v20.css', encoding='utf-8').read() + open(HERE / 'ext_v21.css', encoding='utf-8').read() + open(HERE / 'ext_v22.css', encoding='utf-8').read()
assert '</script' not in mev_js and '</script' not in ext_js and '</script' not in dg_js
rep('<header class="top">', '<style>\n' + mev_css + ext_css + '</style>\n<header class="top">')
rep('<script id="qqdata" type="application/json">', '<script>\n' + mev_js + '</script>\n<script>\n' + dg_js + '</script>\n<script id="qqdata" type="application/json">')

# ---------- version ----------
rep('<small>v0.5.0 beta</small>', '<small>v2.3.0</small>')
rep('const fmtRich = t => fmtPlain(t)', 'const fmtRich = t => dualHtml(t) || fmtRich0(t);\nconst fmtRich0 = t => fmtPlain(t)')

# ---------- script hooks ----------
rep("  if (us.length) { h += '<h6>ILO conditions</h6>';", "  const mpm = (D.master || []).filter(x => has((x.t + ' ' + (x.sub || '') + ' ' + (x.hook || '')).toLowerCase())).slice(0, 4);\n  h += hqSearchHtml(q, has) + trgSearchHtml(q, has);\n  if (mpm.length) { h += '<h6>🧭 Master posters</h6>'; mpm.forEach(x => h += '<button class=\"sr\" data-sr=\"mp\" data-mpid=\"' + x.id + '\"><span class=\"where\">' + x.ic + ' poster</span>' + hl(x.t, terms) + '</button>'); }\n  if (us.length) { h += '<h6>ILO conditions</h6>';")
rep("qb('all', '📖', 'All ILO notes (Ctrl+F)')", "qb('all', '📖', 'All ILO notes on one page')")
rep("Press <span class=\"kbd\">/</span> to search every ILO condition, or open “All ILO notes” and use Ctrl+F.", "Press <span class=\"kbd\">/</span> or <span class=\"kbd\">⌘F</span> to search every ILO condition, every line of the notes and the posters. Press <span class=\"kbd\">⌘F</span> twice for the browser\\'s own find.")
rep("Use your browser’s Ctrl+F / ⌘F here: every line linked to your ILOs is on this one scroll.", "Every line linked to your ILOs is on this one scroll. ⌘F or Ctrl+F jumps to the search bar; press it twice for your browser’s own find.")
rep("const CLK = D.key || [], KICON = {in: '✅', out: '❌', lab: '🧪'};", "const CLK = D.key || [], KICON = {in: '✅', out: '❌', lab: '🧪', nb: '🆕'};")
rep("if (['sprint','weak','gloss','all','home'].includes(h)) return {view: h};", "const mp = h.match(/^mp-([\\w-]+)$/); if (mp && (D.master || []).some(x => x.id === mp[1])) return {view: 'mp', id: mp[1]};\n  if (['sprint','weak','gloss','all','home','sniper','vault','visual','jargon','remix','why','act','misses','snap','posters','triggers','hammer'].includes(h)) return {view: h};")
rep("const h = r.view === 'unit' ? 'u' + r.u + '-' + r.mode : r.view === 'fw' ? 'fw' + (r.id ? '-' + r.id : '') : r.view;", "const h = r.view === 'unit' ? 'u' + r.u + '-' + r.mode : r.view === 'fw' ? 'fw' + (r.id ? '-' + r.id : '') : r.view === 'mp' ? 'mp-' + r.id : r.view;")
rep("if (r.view !== route.view || r.u !== route.u || r.mode !== route.mode) go(r, false);", "if (r.view !== route.view || r.u !== route.u || r.mode !== route.mode || r.id !== route.id) go(r, false);")
rep("  else if (route.view === 'fw') viewFw(m);\n}", "  else if (route.view === 'fw') viewFw(m);\n  else if (route.view === 'sniper') viewSniper(m);\n  else if (route.view === 'vault') viewVault(m);\n  else if (route.view === 'visual') viewVisual(m);\n  else if (route.view === 'jargon') viewJargon(m);\n  else if (route.view === 'remix') viewRemix(m);\n  else if (route.view === 'why') viewWhy(m);\n  else if (route.view === 'act') viewAct(m);\n  else if (route.view === 'misses') viewMisses(m);\n  else if (route.view === 'snap' || route.view === 'posters') viewPosters(m);\n  else if (route.view === 'mp') viewMaster(m);\n  else if (route.view === 'triggers') viewTriggers(m);\n  else if (route.view === 'hammer') viewHammer(m);\n}")
rep("qb('weak', '🎯', 'Weak spots', weakN)", "qb('hammer', '🔨', 'Hammer SBAs', hqCount()) + qb('triggers', '🧲', 'Triggers', trgCount()) + qb('posters', '🗺️', 'Posters', (D.master || []).length + new Set(Object.values(D.snap || {}).map(x => x.n)).size) + qb('remix', '🔄', 'Remix a missed question') + qb('why', '🧬', 'Why it happens', ROOTS.length) + qb('act', '⚡', 'First move vs cure', ACTS.length) + qb('misses', '🔥', 'My misses', msLoad().items.filter(x => !x.fixed).length || null) + qb('sniper', '🎯', 'Blind clincher sniper') + qb('weak', '♻️', 'Weak spots', weakN)")
rep("+ qb('gloss', '🔤', 'Abbreviations', GLOSS.length);", "+ qb('gloss', '🔤', 'Abbreviations', GLOSS.length) + qb('visual', '👁️', 'Visual showdowns', MEV.SD.length) + qb('jargon', '🔺', 'Jargon decoder', JG.length) + qb('vault', '📋', 'Screenshot vault', shotsCache ? shotsCache.length : 0);")
rep("""  h += '</div><h4>ILO weeks · ' + UNITS.length + ' conditions</h4>';
  WEEKS.forEach((w, wi) => {
    const us = unitsOf(w.id), open = openWk.has(w.id);""", """  h += '</div>' + jumpHtml() + '<h4>' + (S.set.sys || S.set.spd ? [S.set.sys ? esc(MEV.sysLabel(S.set.sys)) : '', S.set.spd && SPD[S.set.spd] ? SPD[S.set.spd][0] + ' ' + esc(SPD[S.set.spd][1]) : ''].filter(Boolean).join(' · ') + ' · ' + UNITS.filter(u => (!S.set.sys || usys(u) === S.set.sys) && (!S.set.spd || u.spd === S.set.spd)).length : 'ILO weeks · ' + UNITS.length) + ' conditions</h4>';
  WEEKS.forEach((w, wi) => {
    const us = unitsOf(w.id).filter(u => (!S.set.sys || usys(u) === S.set.sys) && (!S.set.spd || u.spd === S.set.spd)), open = openWk.has(w.id) || !!S.set.sys || !!S.set.spd;
    if (!us.length) return;""")
rep("""data-rand="1">🎲 Random condition</button></div></section>';""", """data-rand="1">🎲 Random condition</button><button class="btn" data-go="hammer">🔨 Hammer SBAs</button><button class="btn" data-go="triggers">🧲 Triggers</button><button class="btn" data-go="posters">🗺️ Posters</button><button class="btn" data-go="sniper">🎯 Blind sniper</button><button class="btn" data-go="visual">👁️ Visual showdowns</button><button class="btn" data-go="jargon">🔺 Jargon decoder</button><button class="btn" data-go="remix">🔄 Remix</button><button class="btn" data-go="why">🧬 Why it happens</button><button class="btn" data-go="act">⚡ First move vs cure</button><button class="btn" data-go="misses">🔥 My misses</button></div></section>';""")
rep("""  h += '<div class="crumbs" style="justify-content:space-between"><h2>Your ILO weeks</h2>""", """  h += homeSysHtml();
  h += '<div class="crumbs" style="justify-content:space-between"><h2>Your ILO weeks</h2>""")
rep("  if ((u.ck || []).length) h += keyHtml(u);", "  h += extHeader(u) + hqUnitBtn(u);\n  if ((u.ck || []).length) h += keyHtml(u);")
rep("<span class=\"code\">🎯 Weak spots</span>", "<span class=\"code\">♻️ Weak spots</span>")
rep("  if (!t.closest('.search-wrap')) $('#sp').hidden = true;\n", "  if (!t.closest('.search-wrap')) $('#sp').hidden = true;\n  if (extClick(t, d)) return;\n")
rep("  if (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || e.metaKey || e.ctrlKey || e.altKey) return;",
    "  if (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || tg.isContentEditable || e.metaKey || e.ctrlKey || e.altKey) return;")
rep("  const s = session;\n  if (s && s.kind === 'quiz') {", "  const s = session;\n  if (s && s.kind === 'hammer' && hqKey(e)) return;\n  if (s && s.kind === 'sniper' && snpKey(e)) return;\n  if (s && s.kind === 'vault' && vaultKey(e)) return;\n  if (s && s.kind === 'quiz') {")
rep("if (e.key.toLowerCase() === 's' && route.view !== 'sprint') return go({view: 'sprint'});", "if (e.key.toLowerCase() === 's' && route.view !== 'sprint' && route.view !== 'sniper') return go({view: 'sprint'});")
rep("/* ---------- events ---------- */", ext_js + "\n/* ---------- events ---------- */")
help_rows = ('<tr><td>🔨</td><td>Hammer SBAs: three single-best-answer questions for every ILO condition, drug group, test and procedure, plus off-map topics and your own mock (🎓). 🔨 classic, 🔨🔨 two steps or a lookalike, 🔨🔨🔨 curveball. Each answer shows why, then 🔄 the flip: the one change that makes another option right. <span class="kbd">A</span>–<span class="kbd">E</span> answer, <span class="kbd">Enter</span> next, <span class="kbd">Esc</span> leave. Each condition page has its own 🔨 button.</td></tr>'
             '<tr><td>🧲</td><td>Triggers: every condition, bug, drug, investigation and procedure in your ILOs as one line each: the scene, the word that flips it in highlighter, then the answer. One long scroll with a picture on every line. <span class="kbd">⌘F</span> filters it, twice for the browser\'s find; 🔒 <span class="kbd">L</span> blurs the answers, tap or <span class="kbd">N</span> to reveal. Each condition\'s word hunt opens its own triggers.</td></tr>'
             '<tr><td>🗺️</td><td>Poster: every condition as one picture with the same layout: cause top-left, who top-right, tests on the right, treatment bottom-right, danger bottom-left, the lookalike on the left, signs in the middle, the hook along the bottom. 🔒 Lock or <span class="kbd">L</span> hides the drugs, numbers and signs: say them, then tap or press <span class="kbd">N</span>. ▶ Walk it lights the zones in order. In quiz modes the poster starts locked. The 🎞️ Film and 🖼️ Pictures tabs sit beside it; paste your own infographics there and box over the details.</td></tr>'
             '<tr><td>🧭</td><td>Master posters: one picture for a whole topic, from spirometry to antidotes. The first five rebuild your AI-made infographics, with what was wrong listed under 🔎.</td></tr>'
             '<tr><td>⌘F</td><td>⌘F or Ctrl+F jumps to the search bar. Press it again there for the browser\'s own find.</td></tr>'
             '<tr><td>👁️</td><td>Clinical Atlas Lookup on every condition: DermNet, LITFL, Radiopaedia, Radiology Masterclass and Google Images open in a new tab. 🥊 chips open the visual showdowns (drawn ECGs, X-rays, fundi, eardrums).</td></tr>'
             '<tr><td>📋</td><td>Paste exam image: on any condition press Ctrl+V / ⌘V (iPad and phone: long-press the paste box → Paste, or 📷 Choose image) to file a question image that tricked you. The vault reviews them with your note hidden.</td></tr>'
             '<tr><td>🎯</td><td>Blind clincher sniper: a clincher with the disease blacked out. <span class="kbd">1</span>–<span class="kbd">4</span> name it and pick the first move, <span class="kbd">Space</span> reveals the trap, <span class="kbd">M</span> mutates (same presentation, one feature changed).</td></tr>'
             '<tr><td>🔄</td><td>Remix: answer the question on Passmedicine, copy the page (⌘A, ⌘C), open 🔄 Remix and press ⌘V. Check ✅ and ✋ (📷 adds an image), then the same patient with one clue changed each round: watch which option wins (<span class="kbd">1</span>–<span class="kbd">5</span>, <span class="kbd">Enter</span>, <span class="kbd">Esc</span> to leave). The end lines up all five: answer ← the clue that picks it. Cards come back tomorrow, then in 3 days, a week and so on, with new variations ready each time (▶ Due today). 🚩 drops one that looks wrong; 🧠 Careful is slower and more accurate.</td></tr>'
             '<tr><td>⚡〰️🌊📈</td><td>Speed tags: how fast a condition arrives (sudden, comes and goes, fluctuates, gradual). Filter by speed under 🗂 Browse on the home screen.</td></tr>'
             '<tr><td>🎬🟰🏷️</td><td>Clinchers that hinge on an exam name read as: 🎬 what you see 🟰 🏷️ the exam name (with a 🔗 memory hook) → 🎯 the diagnosis. The sniper hides the 🎯 part until you answer.</td></tr>'
             '<tr><td>🔺</td><td>Jargon decoder: exam names that don\'t describe what they are (Δ wave, Wenckebach, Kussmaul, Rinne…). Chips on each condition open them. In the sniper: ① picture → name, ② name → picture, ③ what do you do, or 🔺 all three. <span class="kbd">Space</span> reveal, <span class="kbd">1</span>/<span class="kbd">2</span> mark, <span class="kbd">Enter</span> next.</td></tr>'
             '<tr><td>🗂 / 🆕</td><td>Systems &amp; presentations (top of the chapter list) filters by system or jumps to any ILO week or framework. 🆕 marks guideline updates next to older rules.</td></tr>')
rep('data-huntall>Reveal all</button></div><p class="hint" style="margin:0">The phrase a stem hides', 'data-huntall>Reveal all</button><button class="btn ghost sm" data-trjump="\' + u.i + \'">🧲 All triggers</button></div>\' + trStar(u) + \'<p class="hint" style="margin:0">The phrase a stem hides')
rep("hwBar(hunts) + '<div class=\"hws' + (lim ? ' lim' : '') + '\">' + huntHtml(hunts) + '</div>'", "hwBar(hunts) + '<div class=\"hws' + (lim ? ' lim' : '') + '\">' + huntStacks(hunts, u.i) + '</div>'")
rep("</h6><div class=\"hws\">' + huntHtml(u.hunt) + '</div></div>'", "</h6><div class=\"hws\">' + huntStacks(u.hunt, u.i) + '</div></div>'")
rep("  $$('.hw', box).forEach(x => x.hidden = (f !== 'all' && !x.classList.contains(f)) || (!!q && !x.textContent.toLowerCase().includes(q)));\n", "  $$('.hw', box).forEach(x => x.hidden = (f !== 'all' && !x.classList.contains(f)) || (!!q && !x.textContent.toLowerCase().includes(q)));\n  hwStHide(box);\n")
rep('<tr><td>🩺 / 🧬</td>', help_rows + '<tr><td>🩺 / 🧬</td>')

open(a.out, 'w', encoding='utf-8').write(html)
print('wrote', a.out, len(html) // 1024, 'KB; clinchers', len(K), '; units with act', sum(1 for u in U if u.get('act')))
