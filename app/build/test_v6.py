#!/usr/bin/env python3
"""medengine-OSCE v0.6 feature tests: atlas lookup, visual showdowns, system/presentation dropdowns,
amber zone + 8:00 gong, chime toggle, guideline updates, phonetic marking rule. No network."""
import pathlib, re, sys
from playwright.sync_api import sync_playwright

PAGE = pathlib.Path(__file__).resolve().parent.parent / 'out' / 'index.html'
MOCK = """
window.claude = { use: async (cap) => {
  if (cap === 'sample') { const f = async (turns, o) => { const t = '(fidgets) It started suddenly at my desk.'; if (o && o.onText) o.onText({text: t}); return {text: t}; };
    f.json = async (p) => { window.__prompt = p; return {global: 3, verdict: 'ok', domains: [], ticked: [], summary: 'ok'}; }; return f; }
  return null; } };
"""


def run(width):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(500)

        def overflow(label):
            ov = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if ov > 1: errs.append(f'{label}: horizontal overflow {ov}px')

        if 'v1.0.0' not in pg.text_content('#homeBtn'): errs.append('version badge not 1.0.0')
        # station: atlas row + showdown chip
        pg.evaluate("location.hash = 's-PP01'"); pg.wait_for_timeout(400)
        if not pg.locator('.mev-atlasrow').count(): errs.append('no atlas row on station')
        hrefs = pg.eval_on_selector_all('.mev-atlasrow a', 'as => as.map(a => a.href + "|" + a.target)')
        if not hrefs or not all(h.endswith('|_blank') for h in hrefs): errs.append('atlas links not new-tab: ' + str(hrefs[:2]))
        pg.click('.mev-atlasrow [data-mev-atlas]'); pg.wait_for_timeout(200)
        if not pg.locator('dialog.mev-dlg[open]').count(): errs.append('atlas dialog did not open')
        hosts = set(re.sub(r'^https?://(www\.)?([^/]+).*', r'\2', h) for h in pg.eval_on_selector_all('dialog.mev-dlg a', 'as => as.map(a => a.href)'))
        for need in ('dermnetnz.org', 'radiopaedia.org', 'google.com'):
            if need not in hosts: errs.append('atlas missing ' + need)
        pg.fill('#mevQ', 'Wellens'); pg.wait_for_timeout(100)
        if 'Wellens' not in (pg.get_attribute('dialog.mev-dlg .mev-at a', 'href') or ''): errs.append('atlas query edit did not update links')
        pg.click('[data-mev-close]'); pg.wait_for_timeout(100)
        chip = pg.locator('.mev-atlasrow [data-mev-sd]')
        if not chip.count(): errs.append('no showdown chip on PP01 (palpitations)')
        else:
            chip.first.click(); pg.wait_for_timeout(200)
            if not pg.locator('dialog.mev-dlg[open] .mev-sd svg').count(): errs.append('showdown dialog has no schematic')
            pg.click('[data-mev-close]')
        overflow('station')
        # timer: amber zone + 8:00 gong + chime toggle
        pg.evaluate("window.__g = []; const og = gong; gong = function(){ window.__g.push(cur.left + ' ' + (new Error().stack || '').split('\\n').slice(2, 4).join(' / ')); return og(); }; 0")
        pg.click('[data-timer]'); pg.evaluate('cur.left = 121'); pg.wait_for_timeout(1300)
        if not pg.evaluate("document.querySelector('.timer .track').classList.contains('live')"): errs.append('track not live (amber) at 8:00')
        if len(pg.evaluate('window.__g')) != 1: errs.append('gong did not fire exactly once at 8:00: ' + str(pg.evaluate('window.__g')))
        if pg.evaluate("document.querySelector('.timer .track i').style.width") in ('', '0%'): errs.append('timer bar not moving')
        pg.click('[data-timer]')
        pg.click('[data-gong]'); pg.wait_for_timeout(100)
        if pg.inner_text('[data-gong]').strip() != '🔕' or not pg.evaluate('S.set.beepOff'): errs.append('chime toggle off failed')
        pg.click('[data-gong]'); pg.wait_for_timeout(100)
        if pg.evaluate('S.set.beepOff'): errs.append('chime toggle on failed')
        # phonetic marking rule present
        if 'am load a pin' not in pg.evaluate("[...document.scripts].map(s => s.textContent).join('')"): errs.append('phonetic marking line missing')
        # stations: system dropdown
        pg.click('#nav button[data-v="stations"]'); pg.wait_for_timeout(200)
        pg.select_option('#fGrp', ''); pg.select_option('#fWk', ''); pg.select_option('#fKind', '')
        pg.select_option('#fSys', 'derm'); pg.wait_for_timeout(200)
        n = pg.locator('#stList .li').count()
        ok = pg.evaluate("[...document.querySelectorAll('#stList .li')].every(b => { const s = getStation(b.dataset.st); return s.u.some(i => MEV.unitSys(i, UNITS[i].w) === 'derm'); })")
        if n < 5 or not ok: errs.append(f'derm system filter wrong: {n} rows, ok={ok}')
        overflow('stations')
        pg.select_option('#fSys', '')
        # frameworks: presentation jump
        pg.click('#nav button[data-v="fw"]'); pg.wait_for_timeout(200)
        opt = pg.eval_on_selector('#fwJump', "s => [...s.options].find(o => /chest pain/i.test(o.text))?.value || s.options[1].value")
        pg.select_option('#fwJump', opt); pg.wait_for_timeout(300)
        if not pg.url.split('#')[1].startswith('fw-'): errs.append('fwJump did not open a framework: ' + pg.url)
        if not pg.locator('.mev-atlasrow').count(): errs.append('no atlas row on framework page')
        overflow('framework')
        # ILOs: system filter + guideline updates
        pg.click('#nav button[data-v="ilos"]'); pg.wait_for_timeout(200)
        pg.select_option('#iSys', 'eye'); pg.wait_for_timeout(200)
        if pg.locator('#main details.dd').count() != 1: errs.append('ILO eye filter should leave one week')
        pg.select_option('#iSys', ''); pg.wait_for_timeout(100)
        pg.evaluate("location.hash = 'u67'"); pg.wait_for_timeout(300)
        t = pg.inner_text('#main')
        if 'NG28 (Feb 2026)' not in t or '🆕' not in t: errs.append('T2DM 2026 update missing in pack')
        pg.evaluate("location.hash = 'u112'"); pg.wait_for_timeout(300)
        if 'never in ED' not in pg.inner_text('#main'): errs.append('s5(2) ED nuance missing')
        pg.evaluate("location.hash = 'u93'"); pg.wait_for_timeout(300)
        if '>50' not in pg.inner_text('#main'): errs.append('Listeria >50 nuance missing')
        # visual view
        pg.evaluate("location.hash = 'visual'"); pg.wait_for_timeout(400)
        cards = pg.locator('#mevLib .mev-sd').count()
        if cards < 14: errs.append(f'expected 14 showdowns, got {cards}')
        pg.click('[data-mev-flt="derm"]'); pg.wait_for_timeout(100)
        vis = pg.evaluate("[...document.querySelectorAll('#mevLib .mev-sd')].filter(c => !c.hidden).length")
        if vis != 4: errs.append(f'derm filter shows {vis}')
        pg.click('[data-mev-flt=""]')
        pg.locator('#SD-blocks [data-mev-quiz]').click(); pg.wait_for_timeout(100)
        pg.locator('#SD-blocks .mev-pick').first.click(); pg.wait_for_timeout(100)
        if not pg.locator('#SD-blocks .mev-pick.right').count(): errs.append('quiz did not mark the right answer')
        pg.locator('#SD-blocks [data-mev-back]').click()
        if not pg.locator('#SD-blocks svg').count(): errs.append('back to card lost the schematic')
        pg.locator('#SD-stemi [data-mev-terr="inf"]').click()
        dim = pg.evaluate("[...document.querySelectorAll('#SD-stemi .mev-lead')].filter(g => g.classList.contains('dim')).length")
        if dim != 9: errs.append(f'inferior territory should dim 9 leads, dimmed {dim}')
        pg.fill('#atlasQ', 'tension pneumothorax'); pg.click('[data-atlasgo]'); pg.wait_for_timeout(200)
        if pg.input_value('#mevQ') != 'tension pneumothorax': errs.append('visual page atlas search failed')
        pg.click('[data-mev-close]')
        overflow('visual')
        # home tile
        pg.click('#homeBtn'); pg.wait_for_timeout(200)
        if not pg.locator('.tile[data-go="visual"]').count(): errs.append('no visual tile on home')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w)
        print(f'{w}px v0.6 errors: {len(e)}')
        for x in e: print('  -', x)
        bad += len(e)
    sys.exit(1 if bad else 0)
