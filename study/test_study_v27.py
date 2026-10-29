#!/usr/bin/env python3
"""medengine-STUDY v2.7 tests: MSCAA layout and spoiler fixes.
Hammer and mock items follow the paper layout (ages without hyphens, lead-in split off, results with reference ranges,
runs of results as an Investigations table, alphabetical options with the answer kept); no question word or blocker
word renders as a boxed card; the 🧬 examiner pattern chips never show answers and the pattern rule stays folded until
the set is done; a 🗺️ snapshot with the poster and clinchers appears under the answer; no overflow at 390 px."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
errs = []
D = json.loads(re.search(r'<script id="qqdata" type="application/json">(.*?)</script>', PAGE.read_text(encoding='utf-8'), re.S).group(1))
items = D['hq']['q'] + D['mock']['q']
if any(re.search(r'\d+-year-old', q['s']) for q in items): errs.append('hyphenated ages left')
if sum(1 for q in items if q.get('ql')) < 1400: errs.append('lead-ins not split off')
if sum(1 for q in items if re.search(r'\(\d[\d.]*–[\d.]+\)|\(<[\d.]+\)', q['s'] + q.get('post', ''))) < 60: errs.append('too few inline reference ranges')
if sum(1 for q in items if q.get('lab')) < 10: errs.append('too few investigation tables')
for q in items:
    if any(len(r) != 3 or (not r[2] and re.match(r'^-?\d', r[1]) and not re.match(r'(?i)csf|urin|pleural|fluid|aortic|visual', r[0])) for r in q.get('lab') or []): errs.append('lab row without range ' + q['id'])
    if any(r[1].endswith(';') for r in q.get('lab') or []): errs.append('stray semicolon ' + q['id'])
    if 'pm' in q and sorted(q['pm']) != list(range(len(q['o']))): errs.append('bad option map ' + q['id'])
if any('Medical Schools Council' in q['w'] for q in D['off']['q']): errs.append('page footers left in justifications')
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 390, 'height': 900})
    pe = []; pg.on('pageerror', lambda e: pe.append(str(e)))
    pg.add_init_script(MOCK); pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500)
    def run(src, tgt):
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150); pg.evaluate("location.hash='hammer'"); pg.wait_for_timeout(400)
        if pg.locator('[data-hqclear]').count(): pg.click('[data-hqclear]'); pg.wait_for_timeout(100)
        pg.click(f'.hq-f [data-hqset="src:{src}"]'); pg.wait_for_timeout(150)
        pg.click(f'.hq-idx [data-hqtgt="{tgt}"]'); pg.wait_for_timeout(300)
    run('o', 'oq:o-mla1-053')
    for sel in ('.hq-stem .hq-fw',):
        for i in range(pg.locator(sel).count()):
            d = pg.locator(sel).nth(i).evaluate("e => getComputedStyle(e).display")
            if d != 'inline': errs.append('highlight word renders as ' + d)
    run('m', 'mq:m098')
    if pg.locator('.hq-lab tr').count() < 5: errs.append('mock Q98 has no investigation table')
    pg.keyboard.press('c'); pg.wait_for_timeout(500)
    if not pg.locator('.hq-po .po-cond, .hq-po svg, .hq-po .hq-ck').count(): errs.append('no poster snapshot under the answer')
    chips = ' '.join(pg.locator('.hq-gx [data-hqgrp]').all_text_contents())
    if not chips or '→' in chips: errs.append('pattern chips missing or show answers')
    if not pg.locator('.hq-gx details.hq-grr').count(): errs.append('pattern rule not folded before the set is done')
    if pg.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"): errs.append('overflow at 390')
    if pe: errs.append('page errors: ' + '; '.join(pe))
    b.close()
print('\n'.join(errs) if errs else 'STUDY v2.7 OK'); sys.exit(1 if errs else 0)
