#!/usr/bin/env python3
"""medengine v1.5 tests, kept green for v2.0 (no network): 🎞️ the 7-frame film for every ILO condition, which now sits in
the 🎞️ Film tab of the poster panel; frames step, play and swipe; 🔒 Lock hides the words and a tap reveals; related
pictures open in the 🖼️ Pictures tab; the Posters hub (old #snap link) lists and filters; content is in our own words with
no brackets or em dashes; no overflow."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def run(width):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.add_init_script(MOCK); ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500); ev = pg.evaluate
        def ov(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')
        if not re.search(r'v(1\.[5-9]|2\.\d)', pg.text_content('#homeBtn')): errs.append('version not v1.5+')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        SN = D.get('snap', {})
        miss = [u['name'] for i, u in enumerate(D['units']) if str(i) not in SN]
        if miss: errs.append(f'conditions with no snapshot: {miss[:5]}')
        for k, s in SN.items():
            def _flat(x): return ' '.join(_flat(y) for y in x) if isinstance(x, list) else str(x)
            blob = ' '.join(_flat(v) for v in s.values())
            if re.search(r'[()\[\]—]', blob): errs.append(f'snapshot {k}: brackets or em dash')
            for w in (r'\bcolors?\b', r'\banemia', r'(?<!o)esophag', r'\bpediatric', r'\bhemoglobin', r'behavior', r'\bcenter\b'):
                if re.search(w, blob, re.I): errs.append(f'snapshot {k}: American spelling {w}')
            if not (s['m'] and s['w'] and s['s'] and s['x'] and s['t'] and s['d'] and s['h']): errs.append(f'snapshot {k}: empty frame')
            if '→' not in s['m']: errs.append(f'snapshot {k}: mechanism has no arrows')
            if not any(len(x) > 2 for x in s['x']): errs.append(f'snapshot {k}: no test marked as the one that proves it')
        bad = ev("Object.keys(JSON.parse(document.getElementById('qqdata').textContent).snap).filter(k => !DG.has('snap' + k))")
        if bad: errs.append('snapshots not registered: ' + str(bad[:5]))
        if width == 1280:
            broken = ev("""() => { const out = []; Object.keys(JSON.parse(document.getElementById('qqdata').textContent).snap).forEach(k => { const w = document.createElement('div'); w.innerHTML = DG.html('snap' + k); document.body.appendChild(w); const f = w.firstChild; for (let i = 0; i < 7; i++) { DG.show(f, i); const s = f.querySelector('svg'); if (!s) { out.push(k + ':' + i); continue; } const vb = s.viewBox.baseVal; s.querySelectorAll('text').forEach(t => { const bb = t.getBBox(); if (bb.x + bb.width > vb.width + 1) out.push(k + ':' + i + ' wide'); }); } w.remove(); }); return out; }""")
            if broken: errs.append('snapshot frames broken or overflowing: ' + str(broken[:6]))
        # home → section
        if not pg.locator('#main [data-go="posters"]').count(): errs.append('no way into Posters from home')
        ev("location.hash = 'snap'"); pg.wait_for_timeout(400)
        n0 = pg.locator('#snapList .snap-tile').count()
        if n0 < 160: errs.append(f'Snapshots section lists only {n0}')
        pg.fill('#snapQ', 'thyroid'); pg.wait_for_timeout(400)
        n1 = pg.locator('#snapList .snap-tile').count()
        if not 0 < n1 < 10: errs.append(f'snapshot filter did not narrow: {n1}')
        pg.fill('#snapQ', ''); pg.wait_for_timeout(300)
        ov('snapshots section')
        # the condition page
        ev("location.hash = 'u0-read'"); pg.wait_for_timeout(500)
        if pg.locator('#poCard').evaluate('e => e.open') is not True: errs.append('poster panel should be open by default')
        pg.click('[data-potab="film"]'); pg.wait_for_timeout(150)
        if not pg.locator('#poCard #snapOne .dg').count(): errs.append('no film on the ACS page')
        cap0 = pg.text_content('#snapOne .dg-cap'); pg.click('#snapOne [data-dgn="1"]'); pg.wait_for_timeout(80)
        if pg.text_content('#snapOne .dg-cap') == cap0: errs.append('next frame did not change')
        if '7' not in pg.text_content('#snapOne .dg-n'): errs.append('snapshot should have 7 frames')
        pg.click('#snapOne [data-dgp]'); pg.wait_for_timeout(3600)
        if ev("+document.querySelector('#snapOne .dg').dataset.i") < 2: errs.append('play did not advance the snapshot')
        pg.click('#snapOne [data-dgp]')
        pg.check('[data-snaptest]'); pg.wait_for_timeout(60)
        if not ev("document.body.classList.contains('dg-testing')"): errs.append('test-me did not switch on')
        pg.click('#snapOne .dg-stage'); pg.wait_for_timeout(40)
        if not ev("document.querySelector('#snapOne .dg').classList.contains('dg-rev')"): errs.append('test-me tap did not reveal')
        pg.uncheck('[data-snaptest]')
        pg.click('[data-potab="pics"]'); pg.wait_for_timeout(200)
        if pg.locator('[data-snapdg]').count():
            pg.click('[data-snapdg] >> nth=0'); pg.wait_for_timeout(80)
            if not pg.locator('#snapPic .dg').count(): errs.append('more-pictures chip did not open a picture')
        else: errs.append('ACS should have related pictures')
        pg.click('#poCard > summary'); pg.wait_for_timeout(80)
        ev("location.hash = 'u2-read'"); pg.wait_for_timeout(400)
        if pg.locator('#poCard').evaluate('e => e.open'): errs.append('closing the poster panel was not remembered')
        pg.click('#poCard > summary'); pg.wait_for_timeout(80)
        ov('condition page')
        for h in ('u91-fill', 'u160-mcq', 'u102-think'):
            ev(f"location.hash = '{h}'"); pg.wait_for_timeout(300)
            if not pg.locator('#poCard .po').count(): errs.append(f'no poster on {h}')
            ov(h)
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px STUDY v1.5 errors: {len(e)}'); [print('  -', x) for x in e[:15]]
    sys.exit(1 if bad else 0)
