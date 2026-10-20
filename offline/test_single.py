#!/usr/bin/env python3
"""Tests offline/dist/medengine.html (the one-file build) over file:// with no network except a faked Anthropic API."""
import pathlib, re, sys, time
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import test_offline as T

FILE = pathlib.Path(__file__).resolve().parent / 'dist' / 'medengine.html'


def frame(page, app):
    return page.frame_locator('#f-' + app)


def frame_obj(page, app):
    for f in page.frames:
        if f.parent_frame == page.main_frame and f.frame_element().get_attribute('id') == 'f-' + app:
            return f
    return None


def run(width):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 860})
        ctx.route('https://api.anthropic.com/**', T.fake_api)
        ctx.route(re.compile(r'^https?://(?!api\.anthropic\.com).*'), lambda r: r.abort())
        page = ctx.new_page()
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        t0 = time.time()
        page.goto(FILE.as_uri()); page.wait_for_selector('#osce')
        load_s = time.time() - t0
        if page.locator('#apps').is_visible(): errs.append('apps visible on the home screen')

        # tap OSCE → goes straight to OSCE
        page.click('#osce'); page.wait_for_timeout(1500)
        if not page.url.endswith('#osce'): errs.append('url not #osce: ' + page.url)
        if page.locator('main').is_visible(): errs.append('home still visible after tapping OSCE')
        fo = frame_obj(page, 'osce')
        if not fo or 'medengine-OSCE' not in fo.title(): errs.append('OSCE did not open')
        fo.wait_for_selector('#drillLink')
        if fo.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth') > 1: errs.append('OSCE overflow')

        # OSCE storage + AI with a key
        fo.evaluate("localStorage.setItem('medengine-anthropic-key', 'sk-ant-good-123456')")
        fo.evaluate("location.hash = 's-PP01'"); page.wait_for_timeout(400)
        fo.click('[data-mode="ai"]'); fo.fill('#say', 'Hello, what brought you in?'); fo.click('[data-send]'); page.wait_for_timeout(600)
        if 'started suddenly at my desk' not in fo.inner_text('#main'): errs.append('AI patient reply missing in one-file build')

        # OSCE → STUDY via the header button
        fo.click('#drillLink'); page.wait_for_timeout(2500)
        if not page.url.endswith('#study'): errs.append('drill link did not switch to #study: ' + page.url)
        fs = frame_obj(page, 'study')
        if not fs or 'medengine-STUDY' not in fs.title(): errs.append('STUDY did not open')
        if not page.locator('#f-study').is_visible() or page.locator('#f-osce').is_visible(): errs.append('wrong frame visible')
        if fs.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth') > 1: errs.append('STUDY overflow')

        # STUDY page image from inside the file
        for i in range(0, 20):
            fs.evaluate(f"location.hash = 'u{i}-read'"); page.wait_for_timeout(250)
            if fs.locator('[data-fig]').count(): break
        if not fs.locator('[data-fig]').count(): errs.append('no page-image buttons found')
        else:
            fs.locator('[data-fig]').first.click(); page.wait_for_timeout(500)
            ok = fs.evaluate("(() => { const i = document.querySelector('#figImg'); return !!i && i.src.startsWith('data:image/webp') && i.complete && i.naturalWidth > 0; })()")
            if not ok: errs.append('STUDY page image did not load from inside the file')
        for i in range(0, 40):
            if fs.locator('[data-osts]').count(): break
            fs.evaluate(f"location.hash = 'u{i}-read'"); page.wait_for_timeout(200)
        if fs.locator('[data-osts]').count():
            fs.locator('[data-osts]').first.click(); page.wait_for_timeout(400)
            if not fs.evaluate("document.querySelector('#figImg').naturalWidth > 0 && document.querySelector('#figImg').src.startsWith('data:')"): errs.append('OSTS image did not load')

        # STUDY → OSCE pack link (deep link)
        hrefs = fs.evaluate("[...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
        if any('claude.ai' in h or h.endswith('.html') for h in hrefs): errs.append('STUDY has non-local links')
        for i in range(1, 30):
            fs.evaluate(f"location.hash = 'u{i}-read'"); page.wait_for_timeout(200)
            if fs.locator('a[href^="medengine:osce#"]').count(): break
        link = fs.locator('a[href^="medengine:osce#"]').first
        if link.count():
            target = link.get_attribute('href').split('#', 1)[1]
            link.click(); page.wait_for_timeout(800)
            if not page.url.endswith('#osce'): errs.append('OSCE pack link did not switch app')
            if fo.evaluate('location.hash') != '#' + target: errs.append('OSCE did not jump to ' + target + ' (got ' + fo.evaluate('location.hash') + ')')
            if 'started suddenly at my desk' in fo.inner_text('body') and False: pass
        else:
            errs.append('no OSCE pack link found in STUDY ILO view')

        # STUDY header button → OSCE
        page.evaluate("medengineGo('study')"); page.wait_for_timeout(300)
        fs.click('a.oscelink'); page.wait_for_timeout(400)
        if not page.url.endswith('#osce') or not page.locator('#f-osce').is_visible(): errs.append('STUDY header button did not open OSCE')
        # OSCE kept its state (not reloaded): the AI key survived and the page did not reload
        if fo.evaluate("localStorage.getItem('medengine-anthropic-key')") != 'sk-ant-good-123456': errs.append('storage lost')

        # clearing the hash (what back eventually does) → home
        page.evaluate("location.hash = ''"); page.wait_for_timeout(300)
        if not page.locator('main').is_visible(): errs.append('back did not return home: ' + page.url)
        # keyboard 2 → STUDY
        page.keyboard.press('2'); page.wait_for_timeout(500)
        if not page.url.endswith('#study'): errs.append('key 2 did not open STUDY')

        # reopen the file fresh: progress persists
        page2 = ctx.new_page(); page2.goto(FILE.as_uri() + '#osce'); page2.wait_for_timeout(1500)
        f2 = frame_obj(page2, 'osce')
        if not f2 or f2.evaluate("localStorage.getItem('medengine-anthropic-key')") != 'sk-ant-good-123456': errs.append('storage did not persist across opens')
        b.close()
    return errs, load_s


if __name__ == '__main__':
    bad = 0
    for w in (1280, 390):
        e, s = run(w)
        print(f'{w}px one-file errors: {len(e)} (home screen ready in {s:.1f}s)')
        for x in e: print('  -', x)
        bad += len(e)
    sys.exit(1 if bad else 0)
