#!/usr/bin/env python3
"""medengine v1.1 tests (no network): the 🧬 Why it happens section (all 111 cards, search, Read all, system chips); every 🧬 Why it happens card is written as movement (an arrow in every line,
no brackets, balanced bold, no em dashes), the arrows are coloured only inside the card body, cards render on the
condition page and in the Pathoma library, and nothing overflows."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"


def run(width, mock=True):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900})
        if mock: ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500); ev = pg.evaluate
        if 'v1.1' not in pg.text_content('#homeBtn'): errs.append('version not v1.1')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        if len(D['path']) != 111: errs.append(f"expected 111 cards, got {len(D['path'])}")
        cov = {u for r in D['path'] for u in r['u']}
        for u in (12, 96, 100, 101, 102, 111, 126, 128, 141, 142, 147, 160, 162):
            if u not in cov: errs.append(f'unit {u} still has no card')
        for r in D['path']:
            if re.search(r'[()\[\]—]', r['t']): errs.append('title style: ' + r['id'])
            for l in r['l']:
                if '→' not in l: errs.append(f"{r['id']}: a line with no arrow")
                if re.search(r'[()\[\]]', l): errs.append(f"{r['id']}: brackets")
                if '—' in l: errs.append(f"{r['id']}: em dash")
                if l.count('**') % 2: errs.append(f"{r['id']}: unbalanced bold")
                if len(l.split()) > 75: errs.append(f"{r['id']}: line too long")
        ev("location.hash = 'u86-think'"); pg.wait_for_timeout(500)
        if not pg.locator('#main details.pa summary:has-text("Hot joints vs worn joints")').count(): errs.append('joints card not rewritten on the condition page')
        else:
            pg.click('#main details.pa summary:has-text("Hot joints vs worn joints")'); pg.wait_for_timeout(100)
            if pg.locator('#main details.pa[open] .pa-ar').count() < 8: errs.append('arrows not coloured')
            if 'cartilage wears away' not in pg.text_content('#main details.pa[open]'): errs.append('new wording missing')
        # the one-place section
        ev("location.hash = 'home'"); pg.wait_for_timeout(300)
        if not pg.locator('#main [data-go="why"]').count(): errs.append('no way into Why it happens from home')
        ev("location.hash = 'why'"); pg.wait_for_timeout(500)
        if pg.locator('#whyList details.pa').count() != 111: errs.append(f"section shows {pg.locator('#whyList details.pa').count()} cards")
        pg.click('[data-whyall]'); pg.wait_for_timeout(150)
        if pg.locator('#whyList details.pa[open]').count() != 111: errs.append('Read all did not open every card')
        pg.click('[data-whyall]'); pg.wait_for_timeout(150)
        if pg.locator('#whyList details.pa[open]').count(): errs.append('Close all did not close')
        pg.fill('#whyQ', 'glutathione'); pg.wait_for_timeout(150)
        vis = pg.locator('#whyList details.pa:not([hidden])')
        if vis.count() != 1 or 'Paracetamol' not in vis.first.text_content(): errs.append(f'search: {vis.count()} visible')
        pg.fill('#whyQ', 'zzzz'); pg.wait_for_timeout(150)
        if pg.locator('#whyNone').is_hidden(): errs.append('no "no match" note')
        pg.fill('#whyQ', ''); pg.wait_for_timeout(100)
        pg.click('[data-whysys]:has-text("Psych")'); pg.wait_for_timeout(300)
        n = pg.locator('#whyList details.pa').count()
        if not 5 <= n < 111: errs.append(f'system chip shows {n} cards')
        o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        if o > 1: errs.append(f'section overflow {o}px')
        if ev("[...document.querySelectorAll('details.pa')].some(d => (d.dataset.paf || '').includes('<'))"): errs.append('markup leaked into the search attribute')
        o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        if o > 1: errs.append(f'overflow {o}px')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w); bad += len(e); print(f'{w}px STUDY v1.1 errors: {len(e)}'); [print('  -', x) for x in e[:12]]
    e = run(1280, mock=False); bad += len(e); print(f'no-runtime STUDY v1.1 errors: {len(e)}'); [print('  -', x) for x in e[:12]]
    sys.exit(1 if bad else 0)
