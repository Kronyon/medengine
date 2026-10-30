#!/usr/bin/env python3
"""medengine-STUDY v2.7.3 tests: ⚡ thought maps, 🎯 cue check, 🖍️ phone pill and 🔥 My misses sync.
Every Hammer, mock and official question must carry a valid map (coverage is reported, and must be 100% unless
--partial). After answering, the map must sit above the prose, true cues must be underlined in the stem or lab table,
and the score line must compare them with the reader's highlights. On a phone the map stacks and a pen pill appears.
Two devices with their own misses lists must both end up holding the union."""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
HERE = pathlib.Path(__file__).resolve().parent
args = [a for a in sys.argv[1:] if not a.startswith('--')]
PARTIAL = '--partial' in sys.argv
PAGE = pathlib.Path(args[0] if args else HERE / 'index.html').resolve()
STORE = {}
MOCK = """
window.claude = {use: async c => c === 'user' ? {id: async () => 'u1'} : c === 'db' ? {doc: p => ({
  get: async () => { const v = await window.__dbget(p); return {exists: v != null, data: () => v ? JSON.parse(v) : undefined}; },
  set: async o => { const s = JSON.stringify(o); if (new Blob([s]).size > 262144) { const e = new Error('too big'); throw e; } await window.__dbset(p, s); }
})} : null};
"""
errs = []
def ctx(b, mobile=False, dark=False, misses=None):
    c = b.new_context(viewport={'width': 390, 'height': 900} if mobile else {'width': 1280, 'height': 900}, has_touch=mobile, is_mobile=mobile, color_scheme='dark' if dark else 'light')
    c.expose_function('__dbget', lambda p: STORE.get(p)); c.expose_function('__dbset', lambda p, s: STORE.__setitem__(p, s))
    c.add_init_script(MOCK)
    if misses is not None: c.add_init_script("try{ if(!sessionStorage.__set){ localStorage.setItem('medengine-misses-v1', %s); sessionStorage.__set=1; } }catch(e){}" % json.dumps(json.dumps(misses)))
    pg = c.new_page(); pe = []; pg.on('pageerror', lambda e: pe.append(str(e))); pg._pe = pe
    pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1800); return c, pg
with sync_playwright() as p:
    b = p.chromium.launch()
    c1, a = ctx(b, misses={'items': [{'id': 'L1', 'seen': 2, 'box': 1}, {'id': 'B', 'seen': 1}]})
    cov = a.evaluate("""() => { const all = __mev.hqAll(), by = {}; all.forEach(it => { const k = it.t || 'u'; by[k] = by[k] || [0, 0]; by[k][1]++; if (it.tm) by[k][0]++; });
      const bad = all.filter(it => it.tm && (!it.tm.c.length || !it.tm.m || !it.tm.g || it.tm.f.some(f => f[1] === it.a || !it.o[f[1]]))).map(it => it.id);
      return {by, bad, ids: ['u', 'm', 'o'].map(t => (all.find(it => it.t === t && it.tm && it.tm.f.length) || {}).id)}; }""")
    print('coverage', {k: '%d/%d' % tuple(v) for k, v in cov['by'].items()})
    if cov['bad']: errs.append('malformed maps: ' + ', '.join(cov['bad'][:10]))
    if not PARTIAL:
        for k, (n, tot) in cov['by'].items():
            if n < tot: errs.append('%s: only %d of %d questions have a thought map' % (k, n, tot))
    for qid in cov['ids']:
        if not qid: errs.append('no mapped question of some type'); continue
        a.evaluate("ids => __mev.run(ids)", [qid]); a.wait_for_timeout(300)
        if a.locator('.tm').count(): errs.append(qid + ': map shown before answering')
        box = a.locator('.hq-stem [data-hlb="p0"]').bounding_box()
        if not a.locator('[data-hlpen].on').count(): a.keyboard.press('h'); a.wait_for_timeout(100)
        a.mouse.click(box['x'] + 30, box['y'] + 8); a.wait_for_timeout(300)
        a.keyboard.press('a'); a.wait_for_timeout(400)
        if not a.locator('.tm').count(): errs.append(qid + ': no thought map after answering'); continue
        order = a.evaluate("() => { const t = document.querySelector('.tm'), w = document.querySelector('.hq-why'); return !w || (t.compareDocumentPosition(w) & 4) ? 1 : 0; }")
        if not order: errs.append(qid + ': map is not above the explanation')
        for sel in ['.tm-c', '.tm-m', '.tm-g', '.tm-w', '.tm-f']:
            if not a.locator('.tm ' + sel).count(): errs.append(qid + ': map lacks ' + sel)
        if a.locator('.hq-stem .hq-cue, .hq-stem tr.hq-cuerow').count() < 1: errs.append(qid + ': no cue underlined in the stem')
        dec = a.evaluate("getComputedStyle(document.querySelector('.hq-stem .hq-cue, .hq-stem tr.hq-cuerow td')).textDecorationColor")
        if '16, 185, 129' not in dec: errs.append(qid + ': cue underline is not green (%s)' % dec)
        sc = a.locator('[data-tmscore]').inner_text()
        if 'highlights caught' not in sc: errs.append(qid + ': no cue score (%r)' % sc[:80])
        dirn = a.evaluate("getComputedStyle(document.querySelector('.tm-row')).flexDirection")
        if dirn != 'row': errs.append(qid + ': map not horizontal on desktop (%s)' % dirn)
        a.screenshot(path=str(HERE / ('shot_tm_%s.png' % qid)), full_page=False) if '--shots' in sys.argv else None
        a.keyboard.press('Escape'); a.wait_for_timeout(200)
    # ---------- phone ----------
    c2, ph = ctx(b, mobile=True, dark=True, misses={'items': [{'id': 'P1', 'seen': 1}, {'id': 'B', 'seen': 3, 'fixed': True}]})
    ph.evaluate("ids => __mev.run(ids)", [cov['ids'][0]]); ph.wait_for_timeout(300)
    if not ph.locator('#hlPill').count(): errs.append('no highlight pill on a phone')
    else:
        if 'OFF' not in ph.locator('#hlPill').inner_text(): errs.append('pill not OFF by default on a phone')
        ph.locator('#hlPill').tap(); ph.wait_for_timeout(200)
        if 'ON' not in ph.locator('#hlPill').inner_text(): errs.append('pill tap did not switch the pen on')
    ph.keyboard.press('a'); ph.wait_for_timeout(400)
    if ph.locator('.tm').count():
        if ph.evaluate("getComputedStyle(document.querySelector('.tm-row')).flexDirection") != 'column': errs.append('map not stacked on a phone')
    else: errs.append('no map on phone')
    if ph.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth"): errs.append('overflow at 390 with map')
    if '--shots' in sys.argv: ph.locator('.tm').screenshot(path=str(HERE / 'shot_tm_phone.png'))
    ph.keyboard.press('Escape'); ph.wait_for_timeout(200)
    if ph.locator('#hlPill').count(): errs.append('pill stayed after leaving the run')
    # ---------- misses sync ----------
    a.evaluate("__mev.syPush()"); a.wait_for_timeout(1200)
    ph.evaluate("__mev.syPush()"); ph.wait_for_timeout(1200)
    a.evaluate("__mev.SY.lastPull = 0; __mev.syPull(true)"); a.wait_for_timeout(1500)
    ph.evaluate("__mev.SY.lastPull = 0; __mev.syPull(true)"); ph.wait_for_timeout(1500)
    print('ms docs', {k: v[:160] for k, v in STORE.items() if 's271-ms' in k})
    for pg, nm in ((a, 'laptop'), (ph, 'phone')):
        its = {x['id']: x for x in pg.evaluate("__mev.msData.items")}
        if not {'L1', 'P1', 'B'} <= set(its): errs.append(nm + ' misses not merged: ' + ','.join(its))
        elif not its['B'].get('fixed'): errs.append(nm + ': further-along miss did not win')
    for pg, nm in ((a, 'laptop'), (ph, 'phone')):
        if pg._pe: errs.append(nm + ' page errors: ' + '; '.join(pg._pe[:3]))
    b.close()
print('\n'.join(errs) if errs else 'STUDY v2.7.3 OK'); sys.exit(1 if errs else 0)
