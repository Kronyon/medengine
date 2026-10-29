#!/usr/bin/env python3
"""medengine v2.6 OSCE: the three new frameworks (present and differentials, what to say next, management plan).
Content: tiles exist, every ILO week has a plan member, no em dashes or brackets in the new text, step titles shorten
cleanly. Page: framework pages render without overflow at 390 px; history, exam, data and psych stations show the
present and plan card in script mode."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(ROOT / 'build' / 'osce_data_v4.json'))
errs = []
FW = {f['id']: f for f in D['fw']['list']}
for k in ('present', 'flow', 'plan'):
    if k not in FW: errs.append('missing framework ' + k)
if len(D['fw']['list']) != 12: errs.append('expected 12 framework tiles, got %d' % len(D['fw']['list']))
if 'plan' in FW:
    wk = {D['units'][u]['w'] for m in FW['plan']['m'] for u in m['u']}
    miss = {w['id'] for w in D['weeks']} - wk
    if miss: errs.append('ILO weeks with no plan member: ' + str(sorted(miss)))
txt = json.dumps([FW.get(k) for k in ('present', 'flow', 'plan')], ensure_ascii=False)
if '—' in txt: errs.append('em dash in new frameworks')
if re.search(r'[()]', txt): errs.append('bracket in new frameworks')
for k in ('present', 'flow', 'plan'):
    for s in FW.get(k, {}).get('steps', []):
        short = re.split(r'[:(,]', s['t'])[0].strip()
        if len(short) < 3 or short[0].isdigit(): errs.append(f'{k}.{s["k"]} short title {short!r}')
PAGE = str((ROOT / 'dist' / 'app.html').resolve())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 900})
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    for h in ('fw-present--afterhx', 'fw-present--exnorm', 'fw-flow--blank', 'fw-plan--chest', 'fw-plan--eye'):
        pg.goto('file://' + PAGE + '#' + h)
        try: pg.wait_for_selector('.fst', timeout=8000)
        except Exception: pass
        if pg.evaluate('document.documentElement.scrollWidth') > 392: errs.append(h + ' overflows')
        if not pg.locator('.fst').count(): errs.append(h + ' has no steps')
    for sid in ('PP05', 'PP84', 'PP65'):
        pg.goto('file://' + PAGE + '#s-' + sid); pg.wait_for_selector('#modeSeg button[data-mode="script"]', timeout=10000)
        pg.click('#modeSeg button[data-mode="script"]')
        try: pg.wait_for_selector('#nextCard', state='visible', timeout=8000)
        except Exception: pass
        c = pg.locator('#nextCard')
        if not c.count() or not c.is_visible(): errs.append(sid + ' has no present and plan card'); continue
        t = c.text_content()
        if '🎤 Present' not in t or '🗺 Plan' not in t: errs.append(sid + ' card incomplete')
    b.close()
print('OSCE v2.6 frameworks errors:', len(errs))
for e in errs: print('  ', e)
sys.exit(1 if errs else 0)
