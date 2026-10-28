#!/usr/bin/env python3
"""medengine-STUDY v2.0 tests (no network): 🗺️ posters.
Every condition page opens on its poster (unlocked when reading, locked in quiz modes), with 🎞️ Film and 🖼️ Pictures tabs;
🔒 Lock, N, taps and the counter; ▶ Walk; the collapse is remembered separately for reading and quizzing; the Posters hub
lists 14 master posters and filters the condition wall; every master poster renders with its figure inside its frame;
🖼️ My infographics: save a picture, draw boxes, study by tapping, keep it after a reload, keep it out of the screenshot
vault; search finds master posters; ⌘F / Ctrl+F jumps to the search bar; no page overflow at 3 widths."""
import pathlib, re, sys, tempfile
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def picture():
    from PIL import Image, ImageDraw
    f = pathlib.Path(tempfile.gettempdir()) / 'medengine_ig_test.png'
    im = Image.new('RGB', (900, 600), 'white'); d = ImageDraw.Draw(im)
    d.rectangle([40, 40, 860, 140], outline='black', width=3); d.text((60, 70), 'Warfarin for AF with moderate or severe MS', fill='black')
    im.save(f); return f


def run(width, pic):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.add_init_script(MOCK); ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500); ev = pg.evaluate

        def ov(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')

        def go(h, t=400):
            ev(f"location.hash = '{h}'"); pg.wait_for_timeout(t)

        if not re.search(r'v2\.[0-9]', pg.text_content('#homeBtn')): errs.append('version not v2.x')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        if len(D.get('master', [])) != 14: errs.append('expected 14 master posters in the data')
        if not pg.locator('#main [data-go="posters"]').count(): errs.append('no way into Posters from home')
        if not pg.locator('#side [data-go="posters"]').count(): errs.append('no Posters in the sidebar')
        # a condition page while reading
        go('u0-read')
        if pg.locator('#poCard[open] .po-cond').count() != 1: errs.append('reading: poster panel should open on the poster')
        if pg.locator('#poCard .po.lock').count(): errs.append('reading: poster should start unlocked')
        pg.click('#poCard [data-polock]'); pg.wait_for_timeout(60)
        n0 = pg.locator('#poCard .pz.rv').count(); pg.keyboard.press('n'); pg.keyboard.press('n'); pg.wait_for_timeout(60)
        if pg.locator('#poCard .pz.rv').count() != n0 + 2: errs.append('N did not reveal 2 pills')
        pg.locator('#poCard .pz:not(.rv)').first.click(); pg.wait_for_timeout(60)
        if not re.search(r'3 of \d+ open', pg.text_content('#poCard .po-cnt') or ''): errs.append('counter not showing progress')
        pg.keyboard.press('l'); pg.wait_for_timeout(60)
        if pg.locator('#poCard .po.lock').count(): errs.append('L did not unlock')
        pg.click('#poCard [data-poplay]'); pg.wait_for_timeout(250)
        if pg.locator('#poCard .po.walking [data-ord].on').count() != 1: errs.append('Walk it did not spotlight a zone')
        pg.click('#poCard [data-poplay]')
        if not pg.locator('#poCard .po-z.z6').count(): errs.append('ACS poster has no lookalike zone')
        ov('condition poster')
        # tabs: film and pictures, and a new condition opens on its poster again
        pg.click('[data-potab="film"]'); pg.wait_for_timeout(150)
        if not pg.locator('#poCard #snapOne .dg').count(): errs.append('Film tab has no film')
        go('u2-read')
        if not pg.locator('#poCard .po-cond').count(): errs.append('a new condition should open on its poster, not the last tab')
        # quiz modes start locked; collapse is remembered per kind of mode
        go('u7-fill')
        if not pg.locator('#poCard .po.lock').count(): errs.append('fill mode: poster should start locked')
        pg.click('#poCard > summary'); pg.wait_for_timeout(80)
        go('u7-mcq')
        if pg.locator('#poCard').evaluate('e => e.open'): errs.append('quiz modes should remember the collapse')
        go('u7-read')
        if not pg.locator('#poCard').evaluate('e => e.open'): errs.append('reading should stay open after collapsing in a quiz')
        go('u7-recall'); pg.click('#poCard > summary'); pg.wait_for_timeout(80)
        # hub and master posters
        go('posters')
        if pg.locator('.mp-tile').count() != 14: errs.append('hub should list 14 master posters')
        n0 = pg.locator('#snapList .snap-tile').count(); pg.fill('#snapQ', 'stone'); pg.wait_for_timeout(400)
        n1 = pg.locator('#snapList .snap-tile').count()
        if not 0 < n1 < n0: errs.append(f'wall filter did not narrow: {n0} → {n1}')
        pg.fill('#snapQ', ''); pg.wait_for_timeout(300)
        ov('posters hub')
        for m in D['master']:
            go('mp-' + m['id'], 150)
            if not pg.locator('#main .po-split').count(): errs.append(f'master {m["id"]} did not render'); continue
            if m.get('fig') and not pg.locator('#main .po-fig svg').count(): errs.append(f'master {m["id"]}: figure missing')
            if re.search(r'undefined|NaN', pg.text_content('#main .po-split')): errs.append(f'master {m["id"]}: undefined text')
            if m.get('fix') and not pg.locator('#main .po-fix li').count(): errs.append(f'master {m["id"]}: fixes missing')
            ov('master ' + m['id'])
        # my infographics
        if width == 1280:
            go('u7-read'); pg.click('[data-potab="pics"]'); pg.wait_for_timeout(300)
            pg.set_input_files('[data-igfile="7"]', str(pic))
            try: pg.locator('#igView:not([hidden]) .igstage.draw').wait_for(timeout=6000)
            except Exception: pass
            if not pg.locator('#igView:not([hidden]) .igstage.draw').count(): errs.append('saving a picture should open the box editor')
            else:
                st = pg.locator('#igView .igstage').bounding_box()
                pg.mouse.move(st['x'] + st['width'] * .05, st['y'] + st['height'] * .08); pg.mouse.down(); pg.mouse.move(st['x'] + st['width'] * .6, st['y'] + st['height'] * .22, steps=4); pg.mouse.up(); pg.wait_for_timeout(250)
                if pg.locator('#igView .igbox').count() != 1: errs.append('drawing did not make a box')
                pg.click('[data-igmode="study"]'); pg.wait_for_timeout(120)
                pg.locator('#igView .igbox').first.click(); pg.wait_for_timeout(60)
                if not pg.locator('#igView .igbox.rv').count(): errs.append('tapping a box did not reveal it')
                pg.keyboard.press('Escape'); pg.wait_for_timeout(300)
            pg.reload(); pg.wait_for_timeout(1200); pg.click('[data-potab="pics"]'); pg.wait_for_timeout(500)
            if pg.locator('[data-iggrid="7"] .igthumb').count() != 1: errs.append('the picture did not survive a reload')
            go('vault', 500)
            if not re.search(r'(?<!\d)0 saved', pg.text_content('#vaultBody') or ''): errs.append('infographics leaked into the screenshot vault')
        # search and ⌘F / Ctrl+F
        go('u0-read')
        pg.keyboard.press('Control+f'); pg.wait_for_timeout(80)
        if not ev("document.activeElement && document.activeElement.id === 'q'"): errs.append('Ctrl+F did not focus the search bar')
        pg.keyboard.type('antidote'); pg.wait_for_timeout(450)
        if not pg.locator('#sp [data-sr="mp"]').count(): errs.append('search did not find the antidotes poster')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0; pic = picture()
    for w in (1280, 820, 390):
        e = run(w, pic); bad += len(e)
        print(f'{w}px STUDY v2.0 errors: {len(e)}'); [print('  -', x) for x in e[:20]]
    sys.exit(1 if bad else 0)
