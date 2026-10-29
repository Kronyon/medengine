#!/usr/bin/env python3
"""medengine-STUDY v2.5 tests (no network): 🔨 Hammer SBAs.
The data holds 3 hammers (🔨, 🔨🔨, 🔨🔨🔨) for every unique ILO condition, drug group, test or procedure and off-map topic,
plus the 91 mock questions; every question has 5 options, a valid answer, a why and a flip; the hub opens from the sidebar
and home; filters by source, hammer, pattern, status and system change the count; a quiz answers with A to E and 1 to 5,
shows why and the flip, moves on with Enter and leaves with Esc; results are saved and survive a reload; the end screen
offers to redo missed ones; each condition page has its own 🔨 button (aliases 61 and 88 included) that starts its 3;
the mock blueprint renders; search offers matching hammers; no page overflow at 3 widths or in dark mode.
v2.4: a numbered palette jumps between questions; Prev, Next and the arrow keys move back and forth with answers kept;
options can be crossed out with ✕ or Shift+letter; triggers show under the answer; a run left midway resumes after a reload;
no answer is much longer than every distractor, the answer is the longest option in at most a third of questions,
and no distractor carries an absolute word the answer lacks.
v2.5: the 399 official practice paper questions with images, lab tables and justifications; paper and ILO filters;
🦅 scan mode lifts the question line, lights out-of-range values and dims normal ones; 🧬 examiner pattern groups link
twins across papers, the mock and set C (one patient, three steps)."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def data_checks(D, errs):
    H, M = D.get('hq', {}), D.get('mock', {})
    qs = H.get('q', [])
    if len(qs) < 1400: errs.append(f'only {len(qs)} hammer questions')
    longest = 0
    ABS = re.compile(r'\b(only|alone|never|always|ever|nothing|indefinitely|for life|permanently|straight away|at once)\b', re.I)
    by = {}
    for q in qs:
        by.setdefault((q['t'], q['k']), []).append(q['h'])
        if len(q['o']) != 5 or not 0 <= q['a'] < 5: errs.append('bad options ' + q['id'])
        if not q.get('w') or not q.get('f'): errs.append('missing why or flip ' + q['id'])
        if re.search(r'[—–()]', re.sub(r'\s?\([<>]?\d[\d.]*(?:–[\d.]+)?\)', '', q['s'] + q.get('post', '')) + q['w'] + q['f'] + ' '.join(q['o'])): errs.append('dash or bracket in ' + q['id'])
        L = [len(o) for o in q['o']]; rest = max(L[:q['a']] + L[q['a'] + 1:])
        longest += L[q['a']] > rest
        if L[q['a']] - rest >= 12 and L[q['a']] > rest * 1.4: errs.append('answer much longer than every distractor ' + q['id'])
        if any(ABS.search(o) for i, o in enumerate(q['o']) if i != q['a']) and not ABS.search(q['o'][q['a']]) and 'Progestogen-only' not in ' '.join(q['o']): errs.append('absolute word in a distractor ' + q['id'])
    if qs and longest / len(qs) > 0.33: errs.append(f'answer is the longest option in {longest}/{len(qs)}')
    for k, hs in by.items():
        if not (hs.count(1) == hs.count(2) == hs.count(3) >= 1 and len(hs) == 3 * hs.count(1)): errs.append(f'{k}: hammers {hs}')
    if sum(1 for (t, k), hs in by.items() if t == 'u' and len(hs) >= 6) < 160: errs.append('most units should have 6 or more hammers')
    units = {int(k) for t, k in by if t == 'u'}
    al = {int(k) for k in H.get('al', {})}
    miss = [i for i in range(len(D['units'])) if i not in units and i not in al]
    if miss: errs.append('units without hammers: ' + str(miss))
    for t in 'dxb':
        if sum(1 for tt, _ in by if tt == t) < (10 if t == 'b' else 20): errs.append('too few targets of type ' + t)
    # v2.5: the official papers
    O = D.get('off', {})
    oq = O.get('q', [])
    if len(oq) != 399: errs.append(f'official papers have {len(oq)} questions, want 399')
    ids = {q['id'] for q in qs} | {m['id'] for m in M.get('q', [])} | {o['id'] for o in oq}
    for o in oq:
        if not (len(o['o']) == 5 and 0 <= o['a'] < 5 and o['h'] in (1, 2, 3) and o['p'] in 'LNTDR' and o['f'] and o['ql'].endswith('?') and -1 <= o['u'] < len(D['units'])): errs.append('bad official item ' + o['id'])
        for n in o.get('img', []):
            if not O.get('img', {}).get(n, '').startswith('data:image/'): errs.append('missing image ' + n)
    if sum(1 for o in oq if o.get('img')) != 21: errs.append('official images should be on 21 questions')
    if sum(1 for o in oq if o['u'] >= 0) < 280: errs.append('too few official questions mapped to ILO units')
    if any(o.get('il') not in ('I', 'E', 'O') or not o.get('iw') or (o['il'] == 'O') != (o['u'] < 0) for o in oq): errs.append('ILO audit verdict missing or inconsistent')
    for g in O.get('g', []):
        if g['k'] not in ('clone', 'chain', 'block', 'decoy', 'matrix', 'twin') or len(g['ids']) < 2 or any(x not in ids for x in g['ids']): errs.append('bad group ' + g['t'])
    if sum(1 for g in O.get('g', []) if g['k'] == 'clone') < 4: errs.append('clone groups missing')
    labq = [q for q in qs if q.get('lab')]
    if len(labq) < 30: errs.append(f'only {len(labq)} hammers with an Investigations table')
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

        if not re.search(r'v2\.[5-9]', pg.text_content('#homeBtn')): errs.append('version not v2.5+')
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
        if not pg.locator('.hq-trg').count(): errs.append('no triggers under the answer')
        if pg.locator('.hq-pal .hq-pn').count() != 20: errs.append('palette should have 20 buttons')
        if pg.locator('.hq-pal .hq-pn.ok, .hq-pal .hq-pn.bad').count() != 1: errs.append('palette did not mark the answer')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(100)
        if pg.locator('.hq-why').count(): errs.append('Enter did not move on')
        if '2 / 20' not in pg.text_content('#main'): errs.append('counter did not advance')
        # cross-outs: ✕ button and Shift+letter, kept when moving away and back
        pg.locator('.hq-xb').nth(0).click(); pg.wait_for_timeout(60)
        pg.keyboard.press('Shift+D'); pg.wait_for_timeout(60)
        if pg.locator('.hq-o.x').count() != 2: errs.append('cross-outs did not apply')
        if pg.locator('.hq-why').count(): errs.append('crossing out answered the question')
        pg.keyboard.press('ArrowLeft'); pg.wait_for_timeout(80)
        if '1 / 20' not in pg.text_content('#main') or not pg.locator('.hq-why').count(): errs.append('ArrowLeft did not go back to the answered question')
        pg.click('[data-hqnav="1"]'); pg.wait_for_timeout(80)
        if '2 / 20' not in pg.text_content('#main') or pg.locator('.hq-o.x').count() != 2: errs.append('Next lost the cross-outs')
        pg.locator('.hq-xb').nth(0).click(); pg.wait_for_timeout(60)
        if pg.locator('.hq-o.x').count() != 1: errs.append('second ✕ did not undo the cross-out')
        pg.keyboard.press('3'); pg.wait_for_timeout(80)
        if not pg.locator('.hq-why').count(): errs.append('3 did not answer')
        pg.click('[data-hqgo="9"]'); pg.wait_for_timeout(80)
        if '10 / 20' not in pg.text_content('#main'): errs.append('palette jump failed')
        pg.click('[data-hqgo="1"]'); pg.wait_for_timeout(80)
        # resume after reload
        pg.click('[data-hqexit]'); pg.wait_for_timeout(120)
        pg.reload(); pg.wait_for_timeout(1300); go('hammer')
        if not pg.locator('[data-hqresume]').count(): errs.append('no resume after reload')
        else:
            pg.click('[data-hqresume]'); pg.wait_for_timeout(150)
            t = pg.text_content('#main')
            if '2 / 20' not in t or '2 answered' not in t: errs.append('resume did not restore the place: ' + t[:50])
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
        # v2.5: official papers, scan mode and examiner patterns
        go('hammer')
        pg.click('.hq-f [data-hqset="src:o"]'); pg.wait_for_timeout(120)
        n_o = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if n_o != 399: errs.append(f'official filter shows {n_o}')
        pg.click('[data-hqset="pp:p2020"]'); pg.wait_for_timeout(120)
        if int(re.search(r'(\d+) match', pg.text_content('#main')).group(1)) != 50: errs.append('paper filter wrong')
        pg.click('[data-hqset="ilo:O"]'); pg.wait_for_timeout(120)
        n_out = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if not 0 < n_out < 50: errs.append('ILO filter did not narrow')
        pg.click('[data-hqset="ilo:"]'); pg.wait_for_timeout(80)
        pg.click('.hq-idx [data-hqtgt="oq:o-p2020-001"]'); pg.wait_for_timeout(200)
        if not pg.locator('.hq-lab tr').count(): errs.append('official lab table missing')
        if pg.locator('.hq-q.scan').count(): pg.keyboard.press('s'); pg.wait_for_timeout(80)
        pg.keyboard.press('s'); pg.wait_for_timeout(120)
        if not pg.locator('.hq-q.scan').count(): errs.append('S did not turn on scan mode')
        if pg.locator('.hq-lab tr.ab').count() < 3 or not pg.locator('.hq-lab tr.nm').count(): errs.append('scan mode did not sort lab rows')
        if not pg.locator('.hq-qtop').is_visible(): errs.append('scan mode did not lift the question line')
        if not pg.locator('.vx.ab').count(): errs.append('scan mode missed the abnormal temperature')
        ov('scan mode')
        pg.keyboard.press('b'); pg.wait_for_timeout(120)
        if '📋' not in pg.text_content('.hq-why'): errs.append('official justification label missing')
        if pg.locator('.hq-gx .hq-gb').count() < 2: errs.append('examiner pattern boxes missing')
        pg.locator('.hq-gx [data-hqgrp]').first.click(); pg.wait_for_timeout(200)
        if '🧬' not in pg.text_content('.crumbs'): errs.append('group run did not start')
        pg.keyboard.press('s'); pg.wait_for_timeout(60)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        if pg.locator('[data-hqclear]').count(): pg.click('[data-hqclear]'); pg.wait_for_timeout(80)
        pg.click('.hq-f [data-hqset="src:o"]'); pg.click('[data-hqset="pp:mla1"]'); pg.wait_for_timeout(120)
        pg.click('.hq-idx [data-hqtgt="oq:o-mla1-057"]'); pg.wait_for_timeout(200)
        if not pg.locator('.hq-fig img').count(): errs.append('official image missing')
        ov('official image')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(150)
        pg.click('.hq-f [data-hqset="src:all"]'); pg.click('.hq-f [data-hqset="tr:clone"]'); pg.wait_for_timeout(120)
        n_cl = int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        if not 6 <= n_cl < 30: errs.append(f'clone filter shows {n_cl}')
        pg.click('.hq-f [data-hqset="tr:"]'); pg.wait_for_timeout(80)
        # v2.7: multi-select rows add together; rows narrow each other
        cnt = lambda: int(re.search(r'(\d+) match', pg.text_content('#main')).group(1))
        pg.click('[data-hqclear]') if pg.locator('[data-hqclear]').count() else None; pg.wait_for_timeout(80)
        pg.click('.hq-f [data-hqset="src:m"]'); pg.click('.hq-f [data-hqset="src:o"]'); pg.wait_for_timeout(120)
        if cnt() != 91 + 399: errs.append(f'mock plus official should be 490, got {cnt()}')
        pg.click('.hq-f [data-hqset="ilo:I"]'); pg.click('.hq-f [data-hqset="ilo:E"]'); pg.wait_for_timeout(120)
        n_ie = sum(1 for o in D['off']['q'] if o['il'] in 'IE')
        if cnt() != 91 + n_ie: errs.append(f'mock plus in-ILO and edge official should be {91 + n_ie}, got {cnt()}')
        h12 = sum(1 for q in D['mock']['q'] if q['h'] in (1, 2)) + sum(1 for o in D['off']['q'] if o['il'] in 'IE' and o['h'] in (1, 2))
        pg.click('.hq-f [data-hqset="h:1"]'); pg.click('.hq-f [data-hqset="h:2"]'); pg.wait_for_timeout(120)
        if cnt() != h12: errs.append(f'hammer 1 plus 2 should give {h12}, got {cnt()}')
        pg.click('.hq-f [data-hqset="src:o"]'); pg.wait_for_timeout(120)
        if pg.locator('.hq-f [data-hqset="pp:mla1"]').count(): errs.append('paper row should hide when official is unticked')
        pg.click('[data-hqclear]'); pg.wait_for_timeout(80)
        pg.click('.hq-f [data-hqset="tr:clone"]'); pg.click('.hq-f [data-hqset="tr:chain"]'); pg.wait_for_timeout(120)
        n_any = cnt()
        if not pg.locator('[data-hqtrall="1"]').count(): errs.append('no any/all switch for patterns')
        else:
            pg.click('[data-hqtrall="1"]'); pg.wait_for_timeout(120)
            if not cnt() <= n_any: errs.append('all-of-these should not widen')
        pg.click('[data-hqclear]'); pg.wait_for_timeout(80)
        if cnt() != n_all: errs.append('clear filters did not reset')
        ov('multi-select filters')
        if not pg.locator('.hq-obp').count(): errs.append('official blueprint missing')
        if pg.locator('.hq-iap .hq-arow').count() != 399: errs.append('ILO audit should list all 399')
        # condition pages: own button, aliases included
        al = {int(k): v for k, v in D['hq']['al'].items()}
        for ui in (0, 61, 88, 140):
            k = al.get(ui, ui); want = sum(1 for q in D['hq']['q'] if q['t'] == 'u' and int(q['k']) == k) + sum(1 for m in D['mock']['q'] if m['u'] == k) + sum(1 for o in D['off']['q'] if o['u'] == k)
            go(f'u{ui}-read', 350)
            btn = pg.locator('#main [data-hqtgt]')
            if not btn.count(): errs.append(f'unit {ui} has no hammer button'); continue
            btn.first.click(); pg.wait_for_timeout(150)
            t = pg.text_content('#main')
            if f'1 / {want}' not in t: errs.append(f'unit {ui}: expected {want} questions, got {t[:60]!r}')
            if '🔨' not in pg.text_content('.hq-tag .hq-h'): errs.append('first question has no hammer tag')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        # v2.6: no topic spoiler before answering; several saved runs
        for ui in (61, 140):
            k = al.get(ui, ui); nm = D['units'][k]['name'] if 'units' in D else ''
            go(f'u{ui}-read', 350); pg.locator('#main [data-hqtgt]').first.click(); pg.wait_for_timeout(150)
            tag = pg.text_content('.hq-tag')
            if not pg.locator('.hq-tag .hq-lock').count(): errs.append('no topic lock before answering')
            if nm and nm in tag: errs.append(f'topic {nm!r} shown before answering')
            if nm and nm in (pg.text_content('.crumbs') or ''): errs.append(f'topic {nm!r} in crumbs before answering')
            pg.locator('.hq-o').first.click(); pg.wait_for_timeout(100)
            if pg.locator('.hq-tag .hq-lock').count(): errs.append('lock still shown after answering')
            if nm and nm not in pg.text_content('.hq-tag'): errs.append(f'topic {nm!r} missing after answering')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        go('hammer')
        nres = pg.locator('[data-hqresume]').count()
        if nres < 2: errs.append(f'only {nres} saved runs kept')
        go('u61-read', 350); pg.locator('#main [data-hqtgt]').first.click(); pg.wait_for_timeout(150)
        if not pg.locator('.hq-why').count(): errs.append('reopening the same unit did not resume its saved run')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(120); go('hammer')
        pg.locator('[data-hqdrop]').first.click(); pg.wait_for_timeout(120)
        if pg.locator('[data-hqresume]').count() != nres - 1: errs.append('delete saved run failed')
        ov('saved runs')
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
