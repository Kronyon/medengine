#!/usr/bin/env python3
"""medengine v2.1 🧲 Triggers tests for both apps (no network). Usage: test_trg.py PAGE osce|study
Content: every ILO unit has a ⭐ line, every bug has a picture and a line, drugs, investigations and management are all
there, no brackets or em dashes in the new lines. Page: opens from the side, renders 3000+ lines with a picture each,
the parts and the filter work, 🔒 L and N, ⌘F lands in the filter (and a second press is left to the browser), the jump
list scrolls, a condition link opens its page, the condition page links back to its triggers, search finds triggers,
no page overflow at 3 widths and in dark mode."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

PAGE, APP = str(pathlib.Path(sys.argv[1]).resolve()), sys.argv[2]
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def run(width, dark=False):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900}, color_scheme='dark' if dark else 'light')
        ctx.add_init_script(MOCK); ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto('file://' + PAGE); pg.wait_for_timeout(1300); ev = pg.evaluate
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)") if APP == 'study' else ev("({units: D.units, trg: D.trg})")
        T = D.get('trg') or {}
        if width == 1280 and not dark:
            n_units = len(D['units'])
            if len(T.get('c', {})) != n_units: errs.append(f"⭐ lines {len(T.get('c', {}))} for {n_units} units")
            used = {l[0] for s in T.get('sc', []) for l in s[2]}
            if set(T.get('bug', {})) - used: errs.append('bugs without a line: ' + str(sorted(set(T['bug']) - used)[:5]))
            for k, lo in (('dr', 200), ('ix', 100), ('mx', 120)):
                n = sum(len(g[2]) for g in T.get(k, []))
                if n < lo: errs.append(f'{k}: only {n} entries')
            blob = str(T)
            for k in ('dr', 'ix', 'mx'):
                for g in T[k]:
                    for d in g[2]:
                        txt = d[0] + d[2] + ''.join(a + b for a, b in d[3])
                        if re.search(r'[()—]', txt): errs.append(f'{k} {d[0]}: bracket or em dash')
            for need in ('Wells', 'CT pulmonary angiogram', 'MRCP', 'Cystoscopy', 'Flexible sigmoidoscopy', 'ERCP', 'CT angiogram'):
                if need.lower() not in blob.lower(): errs.append('missing investigation ' + need)
            for need in ('cardioversion', 'Hemiarthroplasty', 'VATS', 'Chest drain', 'Needle decompression', 'Aortic valve replacement', 'TAVI'):
                if need.lower() not in blob.lower(): errs.append('missing management ' + need)
        # open from the side
        side = '#side [data-go="triggers"]' if APP == 'study' else '#nav [data-v="triggers"]'
        if width > 900 and not pg.locator(side).count(): errs.append('no Triggers in the side or nav')
        ev("location.hash = 'triggers'"); pg.wait_for_selector('#tgRoot', timeout=8000); pg.wait_for_timeout(300)
        rows = pg.locator('#tgRoot .tg').count()
        if rows < 3000: errs.append(f'only {rows} lines')
        noimg = ev("Array.from(document.querySelectorAll('#tgRoot .tg')).filter(r => !r.querySelector('svg use')).length")
        if noimg: errs.append(f'{noimg} lines without a picture')
        broken = ev("Array.from(new Set(Array.from(document.querySelectorAll('#tgRoot use')).map(u => u.getAttribute('href')))).filter(h => !document.querySelector(h))")
        if broken: errs.append('pictures with no symbol: ' + str(broken[:5]))
        o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        if o > 1: errs.append(f'overflow {o}px')
        if dark: b.close(); return errs
        # parts
        for part in ('b', 'd', 'x', 'm', 'c'):
            pg.click(f'[data-tgpart="{part}"]'); pg.wait_for_timeout(150)
            vis = ev(f"Array.from(document.querySelectorAll('#tgRoot .tg-part')).filter(p => !p.hidden).map(p => p.dataset.part).join('')")
            if vis != part: errs.append(f'part {part} shows {vis}')
        pg.click('[data-tgpart="all"]'); pg.wait_for_timeout(150)
        # filter
        pg.fill('#trq', 'parrot'); pg.wait_for_timeout(350)
        vis = pg.locator('#tgRoot .tg:visible').count()
        if not 0 < vis < 6: errs.append(f'filter "parrot" left {vis} lines')
        pg.fill('#trq', 'hemiarthroplasty'); pg.wait_for_timeout(350)
        if not pg.locator('#tgRoot .tg:visible').count(): errs.append('filter found no hemiarthroplasty')
        pg.fill('#trq', ''); pg.wait_for_timeout(350)
        # jump list
        opts = pg.locator('#tgJump option').count()
        if opts < 30: errs.append(f'jump list has {opts} options')
        pg.select_option('#tgJump', index=opts - 1); pg.wait_for_timeout(300)
        if ev('window.scrollY') < 2000: errs.append('jump did not scroll')
        ev('window.scrollTo(0, 0)'); pg.wait_for_timeout(100)
        # lock, L and N
        pg.click('#tgRoot h1'); pg.keyboard.press('l'); pg.wait_for_timeout(80)
        if not ev("document.getElementById('tgRoot').classList.contains('tg-lock')"): errs.append('L did not lock')
        pg.keyboard.press('n'); pg.keyboard.press('n'); pg.wait_for_timeout(80)
        if pg.locator('#tgRoot .tg.rv').count() != 2: errs.append('N did not reveal 2 lines')
        pg.locator('#tgRoot .tg:not(.rv)').nth(3).click(); pg.wait_for_timeout(60)
        if pg.locator('#tgRoot .tg.rv').count() != 3: errs.append('tap did not reveal')
        pg.keyboard.press('l'); pg.wait_for_timeout(60)
        # ⌘F / Ctrl+F
        pg.click('#tgRoot h1'); pg.keyboard.press('Control+f'); pg.wait_for_timeout(80)
        if ev("document.activeElement && document.activeElement.id") != 'trq': errs.append('Ctrl+F did not focus the trigger filter')
        pg.keyboard.press('Escape')
        # condition link and back
        pg.locator('#tgRoot .tg-un').first.click(); pg.wait_for_timeout(400)
        if ev("!!document.getElementById('tgRoot')"): errs.append('condition link did not open the condition')
        ev("location.hash = %r" % ('u7-think' if APP == 'study' else 'u7')); pg.wait_for_timeout(500)
        j = pg.locator('[data-trjump]').first
        if not j.count(): errs.append('condition page has no link to its triggers')
        else:
            j.click(); pg.wait_for_timeout(700)
            top = ev("(() => { const e = document.getElementById('tg-u7'); return e ? e.getBoundingClientRect().top : -999; })()")
            if not 0 <= top < 450: errs.append(f'triggers link did not land on the condition: top {top}')
        # search finds triggers
        q = pg.locator('#q')
        if APP == 'osce' and not q.is_visible(): pg.click('#qBtn')
        q.fill('psittaci'); pg.keyboard.press('Enter') if APP == 'osce' else None; pg.wait_for_timeout(600)
        if not pg.locator('[data-trgo]').count(): errs.append('search shows no Triggers result')
        else:
            pg.locator('[data-trgo]').first.click(); pg.wait_for_timeout(600)
            if not ev("!!document.getElementById('tgRoot')") or pg.locator('#tgRoot .tg:visible').count() > 10: errs.append('search did not open filtered triggers')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w, d in ((1280, False), (820, False), (390, False), (1280, True)):
        e = run(w, d); bad += len(e)
        print(f'{w}px{" dark" if d else ""} {APP} triggers errors: {len(e)}'); [print('  -', x) for x in e[:20]]
    sys.exit(1 if bad else 0)
