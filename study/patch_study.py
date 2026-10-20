#!/usr/bin/env python3
"""Builds medengine-STUDY v0.6 from the v0.5 page (base_v050.html) without touching the notes.

Adds: the shared visual layer (mev.css/mev.js: Clinical Atlas Lookup + Visual Showdowns), guideline updates
(content/updates_2026.json, shared with medengine-OSCE), 1st-line action/investigation per ILO (from the
OSCE packs, for the sniper), systems & presentations dropdowns, the screenshot vault and the blind clincher
sniper (ext_study.js/.css). Saved progress keys are unchanged (qq-drill-ilo-v1).

Usage: python3 patch_study.py [--osce /home/claude/osce] [--out index.html]
"""
import json, re, sys, pathlib, argparse

HERE = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--osce', default=str(HERE.parent / 'app') if (HERE.parent / 'app' / 'src' / 'mev.js').exists() else '/home/claude/osce')
ap.add_argument('--base', default=str(HERE / 'base_v050.html'))
ap.add_argument('--out', default=str(HERE / ('medengine-study.html' if (HERE.parent / 'app').exists() else 'index.html')))
a = ap.parse_args()
OSCE = pathlib.Path(a.osce)

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
for i, u in enumerate(U):
    p = PK.get(str(i)) or {}
    if p.get('mx'): u['act'] = p['mx'][0].replace('**', '')
    if p.get('ix'): u['ix1'] = p['ix'][0].replace('**', '')
data = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
html = html[:m.start(1)] + data + html[m.end(1):]

# ---------- shared visual layer + v0.6 styles ----------
mev_css = open(OSCE / 'src' / 'mev.css', encoding='utf-8').read()
mev_js = open(OSCE / 'src' / 'mev.js', encoding='utf-8').read()
ext_css = open(HERE / 'ext_study.css', encoding='utf-8').read()
ext_js = open(HERE / 'ext_study.js', encoding='utf-8').read()
assert '</script' not in mev_js and '</script' not in ext_js
rep('<header class="top">', '<style>\n' + mev_css + ext_css + '</style>\n<header class="top">')
rep('<script id="qqdata" type="application/json">', '<script>\n' + mev_js + '</script>\n<script id="qqdata" type="application/json">')

# ---------- version ----------
rep('<small>v0.5.0 beta</small>', '<small>v0.6.0 beta</small>')

# ---------- script hooks ----------
rep("const CLK = D.key || [], KICON = {in: '✅', out: '❌', lab: '🧪'};", "const CLK = D.key || [], KICON = {in: '✅', out: '❌', lab: '🧪', nb: '🆕'};")
rep("if (['sprint','weak','gloss','all','home'].includes(h)) return {view: h};", "if (['sprint','weak','gloss','all','home','sniper','vault','visual'].includes(h)) return {view: h};")
rep("  else if (route.view === 'fw') viewFw(m);\n}", "  else if (route.view === 'fw') viewFw(m);\n  else if (route.view === 'sniper') viewSniper(m);\n  else if (route.view === 'vault') viewVault(m);\n  else if (route.view === 'visual') viewVisual(m);\n}")
rep("qb('weak', '🎯', 'Weak spots', weakN)", "qb('sniper', '🎯', 'Blind clincher sniper') + qb('weak', '♻️', 'Weak spots', weakN)")
rep("+ qb('gloss', '🔤', 'Abbreviations', GLOSS.length);", "+ qb('gloss', '🔤', 'Abbreviations', GLOSS.length) + qb('visual', '👁️', 'Visual showdowns', MEV.SD.length) + qb('vault', '📋', 'Screenshot vault', shotsCache ? shotsCache.length : 0);")
rep("""  h += '</div><h4>ILO weeks · ' + UNITS.length + ' conditions</h4>';
  WEEKS.forEach((w, wi) => {
    const us = unitsOf(w.id), open = openWk.has(w.id);""", """  h += '</div>' + jumpHtml() + '<h4>' + (S.set.sys ? esc(MEV.sysLabel(S.set.sys)) + ' · ' + UNITS.filter(u => usys(u) === S.set.sys).length : 'ILO weeks · ' + UNITS.length) + ' conditions</h4>';
  WEEKS.forEach((w, wi) => {
    const us = unitsOf(w.id).filter(u => !S.set.sys || usys(u) === S.set.sys), open = openWk.has(w.id) || !!S.set.sys;
    if (!us.length) return;""")
rep("""data-rand="1">🎲 Random condition</button></div></section>';""", """data-rand="1">🎲 Random condition</button><button class="btn" data-go="sniper">🎯 Blind sniper</button><button class="btn" data-go="visual">👁️ Visual showdowns</button></div></section>';""")
rep("""  h += '<div class="crumbs" style="justify-content:space-between"><h2>Your ILO weeks</h2>""", """  h += homeSysHtml();
  h += '<div class="crumbs" style="justify-content:space-between"><h2>Your ILO weeks</h2>""")
rep("  if ((u.ck || []).length) h += keyHtml(u);", "  h += extHeader(u);\n  if ((u.ck || []).length) h += keyHtml(u);")
rep("<span class=\"code\">🎯 Weak spots</span>", "<span class=\"code\">♻️ Weak spots</span>")
rep("  if (!t.closest('.search-wrap')) $('#sp').hidden = true;\n", "  if (!t.closest('.search-wrap')) $('#sp').hidden = true;\n  if (extClick(t, d)) return;\n")
rep("  if (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || e.metaKey || e.ctrlKey || e.altKey) return;",
    "  if (tg.tagName === 'INPUT' || tg.tagName === 'TEXTAREA' || tg.tagName === 'SELECT' || tg.isContentEditable || e.metaKey || e.ctrlKey || e.altKey) return;")
rep("  const s = session;\n  if (s && s.kind === 'quiz') {", "  const s = session;\n  if (s && s.kind === 'sniper' && snpKey(e)) return;\n  if (s && s.kind === 'vault' && vaultKey(e)) return;\n  if (s && s.kind === 'quiz') {")
rep("if (e.key.toLowerCase() === 's' && route.view !== 'sprint') return go({view: 'sprint'});", "if (e.key.toLowerCase() === 's' && route.view !== 'sprint' && route.view !== 'sniper') return go({view: 'sprint'});")
rep("/* ---------- events ---------- */", ext_js + "\n/* ---------- events ---------- */")
help_rows = ('<tr><td>👁️</td><td>Clinical Atlas Lookup on every condition: DermNet, LITFL, Radiopaedia, Radiology Masterclass and Google Images open in a new tab. 🥊 chips open the visual showdowns (drawn ECGs, X-rays, fundi, eardrums).</td></tr>'
             '<tr><td>📋</td><td>Paste exam image: on any condition press Ctrl+V / ⌘V (iPad and phone: long-press the paste box → Paste, or 📷 Choose image) to file a question image that tricked you. The vault reviews them with your note hidden.</td></tr>'
             '<tr><td>🎯</td><td>Blind clincher sniper: a clincher with the disease blacked out. <span class="kbd">1</span>–<span class="kbd">4</span> name it and pick the first move, <span class="kbd">Space</span> reveals the trap, <span class="kbd">M</span> mutates (same presentation, one feature changed).</td></tr>'
             '<tr><td>🗂 / 🆕</td><td>Systems &amp; presentations (top of the chapter list) filters by system or jumps to any ILO week or framework. 🆕 marks guideline updates next to older rules.</td></tr>')
rep('<tr><td>🩺 / 🧬</td>', help_rows + '<tr><td>🩺 / 🧬</td>')

open(a.out, 'w', encoding='utf-8').write(html)
print('wrote', a.out, len(html) // 1024, 'KB; clinchers', len(K), '; units with act', sum(1 for u in U if u.get('act')))
