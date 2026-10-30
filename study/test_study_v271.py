#!/usr/bin/env python3
"""medengine-STUDY v2.7.1 tests: 🖍️ highlighter and moving progress between devices.
Two browser contexts act as a laptop and a phone sharing one mock Claude database that enforces the real 256 KiB
per-document limit. The laptop answers a question, highlights by tap and by drag, and carries a progress record far
bigger than one document; the phone, starting empty, must pick up the run, the answer and the highlights. A third
context with no Claude runtime loads the laptop's copied save code. Tap on a highlight removes it. No overflow at 390 px."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
STORE = {}
MOCK = """
window.claude = {use: async c => c === 'user' ? {id: async () => 'u1'} : c === 'db' ? {doc: p => ({
  get: async () => { const v = await window.__dbget(p); return {exists: v != null, data: () => v ? JSON.parse(v) : undefined}; },
  set: async o => { const s = JSON.stringify(o); if (new Blob([s]).size > 262144) { const e = new Error('too big'); e.code = 'invalid_argument'; throw e; } await window.__dbset(p, s); }
})} : null};
"""
errs = []
def ctx(b, claude=True, mobile=False):
    c = b.new_context(viewport={'width': 390, 'height': 900} if mobile else {'width': 1280, 'height': 900}, has_touch=mobile, permissions=['clipboard-read', 'clipboard-write'])
    if claude:
        c.expose_function('__dbget', lambda p: STORE.get(p))
        c.expose_function('__dbset', lambda p, s: STORE.__setitem__(p, s))
        c.add_init_script(MOCK)
    pg = c.new_page(); pe = []; pg.on('pageerror', lambda e: pe.append(str(e))); pg._pe = pe
    pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1800); return c, pg
def hub(pg):
    pg.keyboard.press('Escape'); pg.wait_for_timeout(100); pg.evaluate("location.hash='hammer'"); pg.wait_for_timeout(400)
with sync_playwright() as p:
    b = p.chromium.launch()
    # ---------- laptop ----------
    c1, a = ctx(b)
    a.evaluate("""() => { __mev.S.u.__filler = 'x'.repeat(420000); __mev.save(); }""")  # far over one 256 KiB document
    hub(a)
    if a.locator('[data-hqclear]').count(): a.click('[data-hqclear]'); a.wait_for_timeout(100)
    a.locator('[data-hqstart]').first.click(); a.wait_for_timeout(400)
    qid = a.evaluate("__mev.hqSess.ids[__mev.hqSess.i]")
    if not a.locator('[data-hlpen].on').count(): errs.append('highlighter not on by default')
    # tap a word
    box = a.locator('.hq-stem [data-hlb="p0"]').bounding_box()
    a.mouse.click(box['x'] + 30, box['y'] + 8); a.wait_for_timeout(500)
    if a.locator('.hq-stem mark.hq-mk').count() < 1: errs.append('tap did not highlight a word')
    # drag across the lead-in
    q = a.locator('.hq-stem [data-hlb="q"]').bounding_box()
    a.mouse.move(q['x'] + 2, q['y'] + q['height'] / 2); a.mouse.down(); a.mouse.move(q['x'] + q['width'] * 0.6, q['y'] + q['height'] / 2, steps=8); a.mouse.up(); a.wait_for_timeout(500)
    if not a.locator('.hq-stem [data-hlb="q"] mark.hq-mk').count(): errs.append('drag selection did not highlight')
    marks = a.evaluate("__mev.hlCount(__mev.hqSess.ids[__mev.hqSess.i])")
    if marks < 2: errs.append('expected 2 highlights, got %s' % marks)
    if not a.locator('[data-hlclr]').count(): errs.append('no clear-highlights button')
    a.keyboard.press('a'); a.wait_for_timeout(300)
    if not a.locator('.hq-stem mark.hq-mk').count(): errs.append('highlights lost after answering')
    pick = a.evaluate(f"__mev.hqSess.pk['{qid}']")
    a.evaluate("document.dispatchEvent(new Event('visibilitychange'))")
    a.evaluate("__mev.syPush()"); a.wait_for_timeout(1500)
    if not any(k.endswith('s271-u-1') for k in STORE): errs.append('big progress was not split into chunks')
    if any(len(v.encode()) > 262144 for v in STORE.values()): errs.append('a sync document is over 256 KiB')
    if a.evaluate("__mev.SY.err"): errs.append('laptop sync error: ' + a.evaluate("__mev.SY.err"))
    # ---------- phone, empty ----------
    c2, ph = ctx(b, mobile=True); ph.wait_for_timeout(1500)
    if ph.evaluate("(__mev.S.hqRuns || []).length") < 1: errs.append('phone did not receive the saved run')
    if ph.evaluate("(__mev.S.u.__filler || '').length") != 420000: errs.append('chunked part did not reassemble')
    hub(ph)
    if not ph.locator('[data-hqresume]').count(): errs.append('phone shows no resume button')
    else:
        ph.locator('[data-hqresume]').first.click(); ph.wait_for_timeout(500)
        if ph.evaluate(f"__mev.hqSess.pk['{qid}']") != pick: errs.append('answer did not follow to the phone')
        if ph.locator('.hq-stem mark.hq-mk').count() < 2: errs.append('highlights did not follow to the phone')
        mk = ph.locator('.hq-stem mark.hq-mk').first.bounding_box()
        # v2.7.3: the pen starts OFF on a phone, so a tap there changes nothing until the pill is on
        ph.touchscreen.tap(mk['x'] + mk['width'] / 2, mk['y'] + mk['height'] / 2); ph.wait_for_timeout(300)
        if ph.evaluate(f"__mev.hlCount('{qid}')") != marks: errs.append('a tap with the pen OFF changed the highlights')
        if ph.locator('#hlPill').count() and 'OFF' in ph.locator('#hlPill').inner_text():
            ph.locator('#hlPill').tap(); ph.wait_for_timeout(200)
        mk = ph.locator('.hq-stem mark.hq-mk').first.bounding_box()
        ph.touchscreen.tap(mk['x'] + mk['width'] / 2, mk['y'] + mk['height'] / 2); ph.wait_for_timeout(500)
        if ph.evaluate(f"__mev.hlCount('{qid}')") != marks - 1: errs.append('tap on a highlight did not remove it')
        # phone answers the next question; laptop picks it up on focus
        ph.keyboard.press('ArrowRight'); ph.wait_for_timeout(200); ph.keyboard.press('b'); ph.wait_for_timeout(200)
        ph.evaluate("__mev.syPush()"); ph.wait_for_timeout(1200)
        a.evaluate("__mev.SY.lastPull = 0; __mev.syPull(true)"); a.wait_for_timeout(1500)
        if a.evaluate("Object.keys(__mev.hqSess.pk).length") < 2: errs.append('laptop did not pick up the answer made on the phone')
        if a.evaluate(f"__mev.hlCount('{qid}')") != marks - 1: errs.append('removed highlight came back on the laptop')
    if ph.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"): errs.append('overflow at 390')
    ph.click('#devBtn'); ph.wait_for_timeout(400)
    if not ph.locator('#devs:not([hidden]) [data-devsync]').count(): errs.append('devices panel missing sync controls')
    if ph.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"): errs.append('devices panel overflows at 390')
    # ---------- save code to a copy with no Claude runtime ----------
    a.evaluate("localStorage.setItem('medengine-anthropic-key', 'sk-test-123')")
    a.click('#devBtn'); a.wait_for_timeout(300); a.click('[data-devcopy]'); a.wait_for_timeout(800)
    code = a.locator('#devCodeOut').input_value()
    if not code.startswith('MEDSAVE1'): errs.append('no save code produced')
    if 'sk-test-123' in a.evaluate("JSON.stringify(__mev.devBundle())"): errs.append('save includes the API key')
    c3, off = ctx(b, claude=False, mobile=True)
    if off.evaluate("(__mev.S.hqRuns || []).length"): errs.append('offline copy not empty at start')
    off.click('#devBtn'); off.wait_for_timeout(300)
    if not off.locator('#devs').inner_text().count('outside Claude'): errs.append('offline panel does not explain the file route')
    off.fill('#devCodeIn', code); off.click('[data-devload]'); off.wait_for_timeout(2500)
    if off.evaluate("(__mev.S.hqRuns || []).length") < 1: errs.append('save code did not load the run')
    if off.evaluate(f"__mev.hlCount('{qid}')") < 1: errs.append('save code did not carry highlights')
    for pg, nm in ((a, 'laptop'), (ph, 'phone'), (off, 'offline')):
        if pg._pe: errs.append(nm + ' page errors: ' + '; '.join(pg._pe[:3]))
    b.close()
print('\n'.join(errs) if errs else 'STUDY v2.7.1 OK'); sys.exit(1 if errs else 0)
