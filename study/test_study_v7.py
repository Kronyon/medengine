#!/usr/bin/env python3
"""medengine-STUDY v0.7 tests (no network): dual-code clinchers, Jargon Decoder, 3-way triangulation sniper,
WPW vs LBBB showdown, film/label leak audit, overflow at 3 widths, no-runtime mode."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
V7 = json.load(open(HERE / 'v07_content.json', encoding='utf-8'))
STOP = {'sign', 'signs', 'test', 'syndrome', 'disease', 'wave', 'triad', 'law', 'rule', 'criteria', 'lines', 'nodes', 'lesions', 'phenomenon',
        'breathing', 'manoeuvre', 'pupil', 'thickness', 'the', 'of', 'vs', 'and', 'nipple', 'oesophagus', 'encephalopathy', 'first-rank', 'symptoms', 'mobitz'}


def data_audit():
    errs = []
    for j in V7['jg']:
        words = set()
        for w in re.split(r"[\s()/–-]+", j['t'] + ' ' + ' '.join(j['al'])):
            w = re.sub(r"['’]s?$", '', w.lower()).strip("'’.,")
            if len(w) >= 3 and w not in STOP: words.add(w)
        for w in words:
            if re.search(r'(?<![a-z])' + re.escape(w) + r'(?![a-z])', j['f'].lower()): errs.append(f"film of {j['t']} leaks the label word '{w}'")
        for k in ('t', 'f', 'h', 'x', 'm'):
            if not j.get(k): errs.append(f"{j['t']} missing {k}")
        if any(x in (j['h'] + j['f']) for x in ('apple core', 'bamboo', 'tram-track', 'tram track')): errs.append(f"visual metaphor in {j['t']}")
    for t in list(V7['ck_dual'].values()) + [a[2] for a in V7['ck_add']]:
        if not (t.startswith('🎬') and '🟰 🏷️' in t and '→ 🎯' in t): errs.append('dual clincher format: ' + t[:60])
        lab = t.split('🟰')[1].split('→ 🎯')[0]
        if re.search(r'\(\s*=|\(\s*[a-zδ]', lab): errs.append('bracketed lowercase label in: ' + lab[:60])
    if '—' in json.dumps(V7, ensure_ascii=False): errs.append('em dash in v0.7 content')
    return errs


def run(width, mock=True):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        if mock: ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500)

        def ov(label):
            o = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: horizontal overflow {o}px')

        def hashgo(h, wait=400):
            pg.evaluate(f"location.hash = '{h}'"); pg.wait_for_timeout(wait)

        if not re.search(r'v0\.([789]|1\d)\.\d', pg.text_content('#homeBtn')): errs.append('version not 0.7+')
        if not pg.locator('#main [data-go="jargon"]').count(): errs.append('home: no Jargon decoder button')

        # ---- dual-code clinchers ----
        hashgo('u3-read', 600)
        pg.evaluate("document.querySelector('.keyc').open = true"); pg.wait_for_timeout(100)
        kc = pg.text_content('#main .keyc')
        if pg.locator('#main .keyc .dc').count() < 2: errs.append('Arrhythmias: dual-code clinchers not rendered')
        if 'Delta (Δ) wave' not in pg.text_content('#main .keyc .dc-l'): errs.append('Δ label pill missing')
        if '(= δ' in kc or '[' in kc: errs.append('brackets visible in clinchers')
        if '🔗 Δ = triangle ramp' not in kc: errs.append('hook chip missing')
        if not pg.locator('#main .jgchips [data-jgopen]').count(): errs.append('unit page: no decoder chips')
        ov('unit page')
        pg.click('#main .jgchips [data-jgopen]'); pg.wait_for_timeout(200)
        if pg.locator('#jgView').is_hidden(): errs.append('decoder chip did not open the card')
        else:
            t = pg.text_content('#jgView')
            for k in ('WHAT YOU SEE', 'MEMORY HOOK', 'EXAM TRAP', 'WHAT TO DO'):
                if k.lower() not in t.lower(): errs.append('decoder card missing ' + k)
            if not pg.locator('#jgView svg.mev-ecg polygon.dl').count(): errs.append('Δ shading missing on decoder ECG')
            pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
            if not pg.locator('#jgView').is_hidden(): errs.append('Escape did not close the decoder card')
        ov('decoder overlay')

        # ---- Jargon Decoder view ----
        hashgo('jargon')
        n = pg.locator('#jgList .jg').count()
        if n != len(V7['jg']): errs.append(f'decoder shows {n} of {len(V7["jg"])}')
        if not 35 <= n <= 45: errs.append(f'decoder size {n} not ~35-45')
        pg.fill('#jgQ', 'kussmaul'); pg.wait_for_timeout(100)
        if pg.locator('#jgList .jg').count() != 1: errs.append('search kussmaul != 1')
        pg.fill('#jgQ', 'Δ'); pg.wait_for_timeout(100)
        if pg.locator('#jgList .jg').count() < 1: errs.append('search Δ found nothing')
        pg.fill('#jgQ', 'apple core'); pg.wait_for_timeout(100)
        if pg.locator('#jgList .jg').count(): errs.append('visual metaphor found in decoder')
        pg.fill('#jgQ', ''); pg.wait_for_timeout(100)
        pg.select_option('[data-jgsys]', index=1); pg.wait_for_timeout(100)
        if pg.locator('#jgList .jg').count() >= n: errs.append('system filter did nothing')
        pg.select_option('[data-jgsys]', index=0); pg.wait_for_timeout(100)
        ov('decoder view')

        # ---- triangulation sniper: each mode ----
        hashgo('sniper', 500)
        if not pg.locator('[data-snpmode="m1"]').count(): errs.append('sniper: mode toggle missing')
        for md in ('m1', 'm2', 'm3'):
            pg.click(f'[data-snpmode="{md}"]'); pg.wait_for_timeout(200)
            if not pg.locator('.jgq').count(): errs.append(f'{md}: no triangulation card'); continue
            st = pg.evaluate('({t: __me7.session.t.j.t, f: __me7.session.t.j.f, m: __me7.session.t.j.m})')
            txt = pg.text_content('#snp')
            if md == 'm1':
                if st['t'] in txt: errs.append('m1 leaks the label before reveal')
                if st['f'][:25] not in txt: errs.append('m1 film missing')
            if md == 'm2':
                if st['f'][:25] in txt: errs.append('m2 leaks the film before reveal')
                if st['t'] not in txt: errs.append('m2 label missing')
            if md == 'm3':
                if st['m'][:25] in txt: errs.append('m3 leaks the move before reveal')
                if st['t'] not in txt or st['f'][:25] not in txt: errs.append('m3 needs film + label shown')
            pg.keyboard.press('Space'); pg.wait_for_timeout(120)
            txt = pg.text_content('#snp')
            if md == 'm1' and st['t'] not in txt: errs.append('m1 reveal missing label')
            if md == 'm2' and st['f'][:25] not in txt: errs.append('m2 reveal missing film')
            if md == 'm3' and st['m'][:25] not in txt: errs.append('m3 reveal missing move')
            pg.keyboard.press('2' if md == 'm2' else '1'); pg.wait_for_timeout(120)
            if not pg.locator('#snp [data-snpnext]').count(): errs.append(f'{md}: no end state')
            pg.keyboard.press('s'); pg.wait_for_timeout(80)
            if 'sniper' not in pg.url: errs.append('S key left the triangulation sniper')
            k0 = pg.evaluate('__me7.session.k'); pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
            if pg.evaluate('__me7.session.k') != k0 + 1: errs.append(f'{md}: Enter did not load the next target')
            ov(f'sniper {md}')
        # all three on one term
        pg.click('[data-snpmode="tri"]'); pg.wait_for_timeout(200)
        term = pg.evaluate('__me7.session.t.j.t')
        f0 = pg.evaluate('__me7.session.t.j.f')
        for i in range(3):
            if i == 1 and f0[:25] in pg.text_content('#snp'): errs.append('tri step 2 can copy the film from step 1')
            pg.keyboard.press('Space'); pg.wait_for_timeout(80)
            if pg.evaluate('__me7.session.t.j.t') != term: errs.append('tri changed term mid-way')
            pg.keyboard.press('2' if i == 2 else '1'); pg.wait_for_timeout(80)
        if pg.evaluate('__me7.session.t.res.length') != 3: errs.append('tri did not record 3 shots')
        if pg.locator('#snp .jgstep').count() != 3: errs.append('tri should show 3 steps')
        ov('sniper tri')
        # misses queue for triangulation
        miss = pg.evaluate('Object.keys(__me7.S.snp.jm || {}).length')
        if miss < 1: errs.append('missed term not queued')
        pg.click('[data-snpmiss]'); pg.wait_for_timeout(200)
        cnt = pg.text_content('.snp-cfg .hint')
        if f'{miss} terms' not in cnt: errs.append(f'only-misses pool wrong: {cnt}')
        pg.click('[data-snpmiss]'); pg.wait_for_timeout(150)
        # mode persists after reload
        pg.reload(); pg.wait_for_timeout(1200); hashgo('sniper', 400)
        if not pg.locator('[data-snpmode="tri"].on').count(): errs.append('mode not remembered after reload')
        # decoder → triangulate a chosen term
        hashgo('jargon'); pg.fill('#jgQ', 'wenckebach'); pg.wait_for_timeout(100)
        pg.click('#jgList [data-jgtri]'); pg.wait_for_timeout(300)
        if 'sniper' not in pg.url or pg.evaluate("__me7.session.t && __me7.session.t.j ? __me7.session.t.j.t : ''") != 'Wenckebach (Mobitz I)': errs.append('triangulate button did not load that term')
        if pg.evaluate('__me7.session.k') != 1: errs.append('triangulate button double-loaded a target')
        # classic sniper still works and hides the 🎯 half of dual clinchers
        pg.click('[data-snpmode="clue"]'); pg.wait_for_timeout(200)
        if not pg.locator('#snp .snp [data-snp]').count(): errs.append('classic sniper broken')
        if pg.evaluate("__me7.dxStrip('🎬 a 🟰 🏷️ **L** [h] → 🎯 Dx')") != '🎬 a 🟰 🏷️ **L** [h]': errs.append('dxStrip wrong')
        for _ in range(12):
            if pg.evaluate("__me7.session.t.clue.indexOf('🟰') >= 0"): break
            pg.evaluate('__me7.snpNext()'); pg.wait_for_timeout(30)
        if pg.evaluate("__me7.session.t.clue.indexOf('🟰') >= 0") and '🎯' in pg.text_content('#snp .snp-clue'): errs.append('classic sniper shows the 🎯 answer half')

        # ---- WPW vs LBBB showdown ----
        hashgo('visual')
        c = pg.locator('#SD-wpw-lbbb')
        if not c.count(): errs.append('WPW vs LBBB showdown missing')
        else:
            if c.locator('svg.mev-ecg').count() != 2: errs.append('showdown should draw 2 strips')
            if c.locator('polygon.dl').count() < 2: errs.append('Δ triangles not shaded')
            if c.locator('.mev-feat li').count() != 3: errs.append('showdown needs 3 features')
            t = c.text_content()
            for k in ('START', 'END', 'pseudo-infarction', 'NEVER', 'catheter ablation', 'WiLLiaM'):
                if k not in t: errs.append('showdown missing ' + k)
        ov('visual library')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    e = data_audit(); print(f'data audit errors: {len(e)}'); [print('  -', x) for x in e]; bad += len(e)
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px STUDY v0.7 errors: {len(e)}'); [print('  -', x) for x in e]
    e = run(1280, mock=False); bad += len(e)
    print(f'no-runtime STUDY v0.7 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
