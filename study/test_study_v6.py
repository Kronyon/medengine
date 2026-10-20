#!/usr/bin/env python3
"""medengine-STUDY v0.6 tests (no network): atlas, guideline notes, systems dropdowns, screenshot vault
(paste + file + review), blind clincher sniper (masking, steps, keys, mutation), visual library, regressions."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / 'medengine-study.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
PASTE = """async (sel) => {
  const c = document.createElement('canvas'); c.width = 600; c.height = 300; const x = c.getContext('2d');
  x.fillStyle = '#fff'; x.fillRect(0, 0, 600, 300); x.fillStyle = '#c00'; x.font = '40px sans-serif'; x.fillText('Q: which rash?', 40, 150);
  const blob = await new Promise(r => c.toBlob(r, 'image/png'));
  const dt = new DataTransfer(); dt.items.add(new File([blob], 'shot.png', {type: 'image/png'}));
  const tg = sel ? document.querySelector(sel) : document.body;
  tg.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true}));
}"""


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
        narrow = width < 860

        def ov(label):
            o = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: horizontal overflow {o}px')

        def side():
            if narrow and not pg.evaluate("document.body.classList.contains('nav')"): pg.click('#menuBtn'); pg.wait_for_timeout(150)

        if 'v0.6.0' not in pg.text_content('#homeBtn'): errs.append('version not 0.6.0')
        ov('home')
        # systems & presentations
        side()
        pg.click('.jump > summary'); pg.select_option('[data-jsys]', 'derm'); pg.wait_for_timeout(200)
        n = pg.locator('#side .pg').count()
        if n != 18: errs.append(f'derm filter shows {n} conditions (expected 18)')
        side()
        pg.select_option('[data-jsys]', ''); pg.wait_for_timeout(150)
        if pg.locator('#side .pg').count() != 168: errs.append('clearing the system filter did not restore 168')
        side()
        pg.select_option('[data-jpres]', 'f:chestpain'); pg.wait_for_timeout(300)
        if 'fw' not in pg.url.split('#')[-1]: errs.append('framework jump failed: ' + pg.url)
        # unit 67: atlas, 2026 clincher, line notes
        pg.evaluate("location.hash = 'u67-read'"); pg.wait_for_timeout(500)
        if not pg.locator('#main .mev-atlasrow').count(): errs.append('no atlas row in unit header')
        if not pg.locator('#main .kl-nb').count(): errs.append('no 🆕 clincher on T2DM')
        if not pg.locator('[id="L60.3.7.2"] .mev-upd').count(): errs.append('no 2026 note on the old SGLT2i line')
        pg.click('#main .mev-atlasrow [data-mev-atlas]'); pg.wait_for_timeout(150)
        if not pg.locator('dialog.mev-dlg[open]').count(): errs.append('atlas dialog did not open')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        pg.evaluate("location.hash = 'u93-read'"); pg.wait_for_timeout(300)
        if '>50' not in pg.text_content('#main .keyc'): errs.append('Listeria nuance missing')
        pg.evaluate("location.hash = 'u112-read'"); pg.wait_for_timeout(300)
        if "can't be used in ED" not in pg.text_content('#main .keyc'): errs.append('s5(2) ED clincher missing')
        ov('unit read')
        # paste exam image on a derm unit
        pg.evaluate("location.hash = 'u137-read'"); pg.wait_for_timeout(400)
        pg.evaluate(PASTE, None); pg.wait_for_timeout(900)
        if '1 saved' not in pg.text_content('[data-shotn="137"]'): errs.append('paste did not save to the unit: ' + pg.text_content('[data-shotn="137"]'))
        if pg.locator('[data-shotgrid="137"] .shot').count() != 1: errs.append('thumbnail missing after paste')
        pg.locator('[data-shotnote="137"]').fill('silvery scale = psoriasis')
        pg.set_input_files('[data-shotfile="137"]', files=[{'name': 'x.png', 'mimeType': 'image/png', 'buffer': bytes.fromhex('89504e470d0a1a0a0000000d4948445200000001000000010806000000') + bytes.fromhex('1f15c4890000000d49444154789c636060606000000005000173d5a4a00000000049454e44ae426082')}])
        pg.wait_for_timeout(900)
        if '2 saved' not in pg.text_content('[data-shotn="137"]'): errs.append('file chooser did not save')
        pg.locator('[data-shotgrid="137"] .shot').first.click(); pg.wait_for_timeout(200)
        if not pg.locator('#shotView .shotbig img').count(): errs.append('lightbox did not open')
        pg.click('[data-shotclose]')
        # vault + review
        pg.evaluate("location.hash = 'vault'"); pg.wait_for_timeout(600)
        if pg.locator('#vaultBody .shot').count() != 2: errs.append('vault does not list 2 shots')
        pg.click('[data-vrev]'); pg.wait_for_timeout(150)
        pg.keyboard.press('Space'); pg.wait_for_timeout(100)
        if not pg.locator('[data-vgot]').count(): errs.append('review reveal failed')
        pg.keyboard.press('1'); pg.wait_for_timeout(150); pg.keyboard.press('Space'); pg.wait_for_timeout(100); pg.keyboard.press('2'); pg.wait_for_timeout(200)
        if 'Review done' not in pg.inner_text('#vaultBody'): errs.append('review did not finish')
        ov('vault')
        # paste on vault = unsorted
        pg.click('[data-vexit]'); pg.wait_for_timeout(300)
        pg.evaluate(PASTE, '[data-shotzone="-1"]'); pg.wait_for_timeout(900)
        if 'Unsorted' not in pg.inner_text('#vaultBody'): errs.append('vault paste did not file as unsorted')
        # sniper
        pg.evaluate("location.hash = 'sniper'"); pg.wait_for_timeout(500)
        bad = 0; masked = 0; steps = 0
        for i in range(40):
            clue = pg.inner_text('.snp-clue')
            if pg.locator('.snp-clue .snp-mask').count(): masked += 1
            pg.keyboard.press('1'); pg.wait_for_timeout(40)
            right = pg.locator('.opts').first.locator('.opt.right').inner_text().split('\n', 1)[-1].strip()
            parts = [x.strip() for x in re.split(r'\s*(?:/|,|&|\(|\))\s*', right) if len(x.strip()) >= 5]
            if right.lower() in clue.lower() or any(pp.lower() in clue.lower() for pp in parts if not re.match(r'(?i)^(acute|chronic|cancer)', pp)): bad += 1
            # finish remaining steps by keyboard
            for _ in range(4):
                if pg.locator('[data-snpnext]').count(): break
                if pg.locator('[data-snprev]').count(): pg.keyboard.press('Space'); pg.wait_for_timeout(30); pg.keyboard.press('1')
                else: pg.keyboard.press('2')
                pg.wait_for_timeout(40); steps += 1
            if not pg.locator('[data-snpnext]').count(): errs.append('sniper target did not complete'); break
            if i == 5:
                pg.keyboard.press('s'); pg.wait_for_timeout(100)
                if 'sniper' not in pg.url: errs.append('S key left the sniper')
                pg.keyboard.press('m'); pg.wait_for_timeout(100)
                if not pg.locator('.snp-mut').count(): errs.append('mutation did not start')
                continue
            pg.keyboard.press('Enter'); pg.wait_for_timeout(60)
        if bad > 2: errs.append(f'{bad} of 40 sniper clues leaked the diagnosis')
        if masked < 3: errs.append(f'only {masked} of 40 clues had masking')
        st = pg.evaluate("JSON.parse(localStorage.getItem('qq-drill-ilo-v1')).snp")
        if not st or st.get('n', 0) < 40: errs.append('sniper stats not saved: ' + str(st))
        ov('sniper')
        # visual library
        pg.evaluate("location.hash = 'visual'"); pg.wait_for_timeout(400)
        if pg.locator('#mevLib .mev-sd').count() != 13: errs.append('visual library not 13 cards')
        ov('visual')
        # regressions: fill, mcq, think still render
        for mode, sel in (('fill', 'select.dd'), ('mcq', '#quiz .opt'), ('think', '#main .panel')):
            pg.evaluate(f"location.hash = 'u0-{mode}'"); pg.wait_for_timeout(500)
            if not pg.locator(sel).count(): errs.append(f'{mode} mode broken')
        pg.evaluate("location.hash = 'u0-mcq'"); pg.wait_for_timeout(400); pg.keyboard.press('1'); pg.wait_for_timeout(100)
        if not pg.locator('#quiz .opt.right').count(): errs.append('MCQ answer key broken')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w)
        print(f'{w}px STUDY v0.6 errors: {len(e)}')
        for x in e: print('  -', x)
        bad += len(e)
    e = run(1280, mock=False)
    print(f'no-runtime STUDY v0.6 errors: {len(e)}')
    for x in e: print('  -', x)
    sys.exit(1 if bad + len(e) else 0)
