#!/usr/bin/env python3
"""medengine-STUDY v2.3 tests (no network): 🔨 Hammer SBAs.
The data holds 3 hammers (🔨, 🔨🔨, 🔨🔨🔨) for every unique ILO condition, drug group, test or procedure and off-map topic,
plus the 91 mock questions; every question has 5 options, a valid answer, a why and a flip; the hub opens from the sidebar
and home; filters by source, hammer, pattern, status and system change the count; a quiz answers with A to E and 1 to 5,
shows why and the flip, moves on with Enter and leaves with Esc; results are saved and survive a reload; the end screen
offers to redo missed ones; each condition page has its own 🔨 button (aliases 61 and 88 included) that starts its 3;
the mock blueprint renders; search offers matching hammers; no page overflow at 3 widths or in dark mode."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def data_checks(D, errs):
    H, M = D.get('hq', {}), D.get('mock', {})
    qs = H.get('q', [])
    if len(qs) < 900: errs.append(f'only {len(qs)} hammer questions')
    by = {}
    for q in qs:
        by.setdefault((q['t'], q['k']), []).append(q['h'])
        if len(q['o']) != 5 or not 0 <= q['a'] < 5: errs.append('bad options ' + q['id'])
        if not q.get('w') or not q.get('f'): errs.append('missing why or flip ' + q['id'])
        if re.search(r'[—–()]', q['s'] + q['w'] + q['f'] + ' '.join(q['o'])): errs.append('dash or bracket in ' + q['id'])
    for k, hs in by.items():
        if sorted(hs) != [1, 2, 3]: errs.append(f'{k}: hammers {hs}')
    units = {int(k) for t, k in by if t == 'u'}
    al = {int(k) for k in H.get('al', {})}
    miss = [i for i in range(len(D['units'])) if i not in units and i not in al]
    if miss: errs.append('units without hammers: ' + str(miss))
    for t in 'dxb':
        if sum(1 for tt, _ in by if tt == t) < (10 if t == 'b' else 20): errs.append('too few targets of type ' + t)
    mq = M.get('q', [])
    if len(mq) != 91: errs.append(f'mock has {len(mq)} questions, want 91')
    if any(m['n'] == 84 for m in mq): errs.append('Q84 duplicate kept')
    for m in mq:
        if not (len(m['o']) == 5 and 0 <= m['a'] < 5 and m['h'] in (1, 2, 3) and m['p'] in 'LNTDR' and m['f'] and 0 <= m['u'] < len(D['units'])): errs.append('bad mock item ' + m['id'])


def run(width, dark):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900}, color_scheme='dark' if dark else 'light')
        ctx.add_init_script(MOCK); ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500); ev = pg.evaluate

        def ov(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')

        def go(h, t=400):
            ev(f"location.hash = '{h}'"); pg.wait_for_timeout(t)

        if not re.search(r'v2\.3', pg.text_content('#homeBtn')): errs.append('version not v2.3')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        if width == 1280 and not dark: data_checks(D, errs)
        if not pg.locator('#main [data-go="hammer"]').count(): errs.append('no Hammer button on home')
        if not pg.locator('#side [data-go="hammer"]').count(): errs.append('no Hammer in the sidebar')
        go('hammer')
        if not pg.locator('.hq-bp').count(): errs.append('no mock blueprint')
        pg.click('.hq-bp summary'); pg.wait_for_timeout(80)
        if pg.locator('.hq-bp .hq-bar').count() < 10: errs.append('blueprint bars missing')
        n_all = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        pg.click('[data-hqset="src:m"]'); pg.wait_for_timeout(120)
        n_m = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if n_m != 91: errs.append(f'mock filter shows {n_m}')
        if pg.locator('.hq-idx .sr').count() != 91: errs.append('mock index should list 91 questions')
        pg.click('[data-hqset="src:all"]'); pg.click('[data-hqset="h:3"]'); pg.wait_for_timeout(120)
        n_h3 = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if not 0 < n_h3 < n_all: errs.append('hammer filter did not narrow')
        pg.click('[data-hqset="p:R"]'); pg.wait_for_timeout(120)
        n_r = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if not 0 < n_r < n_h3: errs.append('pattern filter did not narrow')
        pg.click('[data-hqset="h:0"]'); pg.click('[data-hqset="p:"]'); pg.wait_for_timeout(80)
        pg.select_option('[data-hqsys]', 'eye'); pg.wait_for_timeout(150)
        n_eye = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if not 0 < n_eye < n_all: errs.append('system filter did not narrow')
        pg.select_option('[data-hqsys]', ''); pg.wait_for_timeout(120)
        ov('hub')
        # a quiz of 20
        pg.click('[data-hqstart="20"]'); pg.wait_for_timeout(150)
        if pg.locator('.hq-o').count() != 5: errs.append('quiz did not show 5 options')
        pg.keyboard.press('b'); pg.wait_for_timeout(100)
        if not pg.locator('.hq-why').count(): errs.append('B did not answer')
        if not pg.locator('.hq-flip').count(): errs.append('no flip after answering')
        if pg.locator('.hq-o.ok').count() != 1: errs.append('correct option not shown')
        ov('quiz answered')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(100)
        if pg.locator('.hq-why').count(): errs.append('Enter did not move on')
        if '2 / 20' not in pg.text_content('#main'): errs.append('counter did not advance')
        pg.keyboard.press('3'); pg.wait_for_timeout(80)
        if not pg.locator('.hq-why').count(): errs.append('3 did not answer')
        for _ in range(18):
            pg.keyboard.press('Enter'); pg.wait_for_timeout(30); pg.locator('.hq-o').first.click(); pg.wait_for_timeout(30)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
        if not re.search(r'🔨 \d+ / 20', pg.text_content('#main')): errs.append('no end screen')
        saved = ev("Object.keys((JSON.parse(localStorage.getItem('qq-drill-ilo-v1'))||{}).hq||{}).length")
        if saved < 20: errs.append(f'only {saved} results saved')
        if pg.locator('[data-hqretry]').count():
            pg.click('[data-hqretry]'); pg.wait_for_timeout(120)
            if pg.locator('.hq-o').count() != 5: errs.append('redo missed did not start')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        if pg.locator('.hq-o').count(): errs.append('Esc did not leave the quiz')
        pg.reload(); pg.wait_for_timeout(1300); go('hammer')
        pg.click('[data-hqset="st:new"]'); pg.wait_for_timeout(120)
        n_new = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if n_new > n_all - 20: errs.append('results not kept after reload')
        pg.click('[data-hqset="st:"]')
        # condition pages: own button, aliases included
        al = {int(k): v for k, v in D['hq']['al'].items()}
        for ui in (0, 61, 88, 140):
            k = al.get(ui, ui); want = 3 + sum(1 for m in D['mock']['q'] if m['u'] == k)
            go(f'u{ui}-read', 350)
            btn = pg.locator('#main [data-hqtgt]')
            if not btn.count(): errs.append(f'unit {ui} has no hammer button'); continue
            btn.first.click(); pg.wait_for_timeout(150)
            t = pg.text_content('#main')
            if f'1 / {want}' not in t: errs.append(f'unit {ui}: expected {want} questions, got {t[:60]!r}')
            if '🔨' not in pg.text_content('.hq-tag .hq-h'): errs.append('first question has no hammer tag')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        # search
        pg.click('#q'); pg.keyboard.type('glaucoma'); pg.wait_for_timeout(400)
        if not pg.locator('#sp [data-hqq]').count(): errs.append('search offers no hammers')
        else:
            pg.click('#sp [data-hqq]'); pg.wait_for_timeout(200)
            if not pg.locator('.hq-o').count(): errs.append('search hammers did not start')
        ov('search quiz')
        b.close()
    return errs


all_errs = []
for w, dk in ((1280, False), (820, False), (390, False), (390, True)):
    e = run(w, dk); print(w, 'dark' if dk else 'light', 'OK' if not e else e)
    all_errs += e
sys.exit(1 if all_errs else 0)
