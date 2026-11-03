#!/usr/bin/env python3
"""medengine v2.7 OSCE: a full case for every history, psychiatry and examination station.
Data: every hx, psych and ex station has a case on every variant, with a presentation, three-tier differentials,
investigations, management and a verbatim plan; exam variants carry findings; no em dashes. Page: at 390 px the
patient sheet, examiner sheet, script and mark scheme show the case for a past-paper, a bank history, a psychiatry and
an exam station, a case's own door brief replaces the station's, and nothing overflows."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
ROOT = pathlib.Path(__file__).resolve().parents[1]
D = json.load(open(ROOT / 'build' / 'osce_data_v4.json'))
errs = []
T = [s for s in D['stations'] if s.get('type') in ('hx', 'psych', 'ex')]
for s in T:
    vs = s.get('vars') or []
    if not vs: errs.append(s['id'] + ' has no case'); continue
    for v in vs:
        c = v.get('cs')
        if not c: errs.append(f"{s['id']} {v['k']} has no case"); continue
        if not (c['pres'] and len(c['ddx']) == 3 and c['ix'] and c['mx']): errs.append(f"{s['id']} {v['k']} case incomplete")
        if s['type'] == 'ex' and not (c['find'] and v.get('r')): errs.append(f"{s['id']} {v['k']} exam case has no findings")
        if s['type'] != 'ex' and not (c['open'] and c['sum'] and c['tell'] and len(c['hpc']) >= 4): errs.append(f"{s['id']} {v['k']} history case thin")
if '—' in json.dumps([v.get('cs') for s in T for v in s.get('vars') or []], ensure_ascii=False): errs.append('em dash in a case')
if sum(len(s.get('vars') or []) for s in T if s['id'].startswith('E-')) < 70: errs.append('exam stations should have about 3 cases each')
PAGE = str((ROOT / 'dist' / 'app.html').resolve())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 900})
    pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
    def open_(sid, k=None):
        pg.goto('file://' + PAGE + '#s-' + sid); pg.wait_for_selector('#modeSeg button[data-mode="script"]', timeout=10000)
        if k: pg.select_option('#varSel', k); pg.wait_for_timeout(150)
    def mode(m):
        pg.click(f'#modeSeg button[data-mode="{m}"]'); pg.wait_for_timeout(150)
    def ov(tag):
        if pg.evaluate('document.documentElement.scrollWidth') > 392: errs.append(tag + ' overflows at 390')
    for sid, k, ex in (('PP05', None, 0), ('NE03', None, 0), ('MH02', None, 0), ('E-cvs', 'B', 1), ('E-scrotal', 'C', 1)):
        open_(sid, k)
        mode('friends'); pg.click('#roleSeg [data-role="actor"]'); pg.wait_for_timeout(150)
        t = pg.text_content('#friendsCard')
        if ('🩺 Findings' if ex else '🗣 Your opening line') not in t: errs.append(sid + ' patient sheet has no case')
        ov(sid + ' actor')
        pg.click('#roleSeg [data-role="exam"]'); pg.wait_for_timeout(150)
        if not any(s in pg.text_content('#friendsCard') for s in ('What a clear pass sounds like', 'Clear Pass')): errs.append(sid + ' examiner sheet has no model')
        ov(sid + ' examiner')
        pg.click('#roleSeg [data-role="cand"]'); pg.wait_for_timeout(100)
        mode('tick'); pg.click('[data-expand]'); pg.wait_for_timeout(100)
        if 'This case' not in pg.text_content('#clCard'): errs.append(sid + ' mark scheme has no case section')
        ov(sid + ' tick')
        mode('script')
        if not pg.text_content('#scriptCard').strip(): errs.append(sid + ' script empty')
        ov(sid + ' script')
    open_('E-cvs', 'B')
    if '71-year-old woman' not in (pg.text_content('#briefP') or ''): errs.append('case door brief not shown')
    b.close()
print('OSCE v2.7 cases errors:', len(errs))
for e in errs[:40]: print('  ', e)
sys.exit(1 if errs else 0)
