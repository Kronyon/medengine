# Browser test for the public build: loads web/dist over HTTP with Appwrite unreachable (signed-out state).
import asyncio, subprocess, sys, os, time
from playwright.async_api import async_playwright
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dist')
async def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765', '-d', D], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
    errs = []
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            for w in (390, 1280):
                page = await (await b.new_context(viewport={'width': w, 'height': 900})).new_page()
                page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
                await page.route('**/v1/**', lambda r: r.fulfill(status=401, content_type='application/json', body='{"message":"User (role: guests) missing scope (account)","code":401,"type":"general_unauthorized_scope"}'))
                await page.goto('http://localhost:8765/'); await page.wait_for_timeout(800)
                html = await page.content()
                if 'Nana' in html: errs.append('personal name in public build')
                if await page.evaluate("() => !!document.querySelector('header .site-foot') || document.querySelector('.site-foot').parentElement !== document.body"): errs.append('footer misplaced')
                if await page.is_visible('#drillLink'): errs.append('private drill link visible')
                if 'Your feedback priorities' in await page.inner_text('#main'): errs.append('personal feedback card shown')
                if not await page.is_visible('#acctBtn'): errs.append('account button missing')
                if 'medengine' not in (await page.title()): errs.append('title')
                await page.evaluate("() => { location.hash = 's-PP01'; }"); await page.wait_for_timeout(300)
                if await page.locator('[data-mode="voice"]').is_disabled(): errs.append('voice disabled on site')
                await page.click('[data-mode="ai"]'); await page.fill('#say', 'hello'); await page.click('[data-send]'); await page.wait_for_timeout(800)
                if not await page.is_visible('dialog.acct'): errs.append('sign-in modal did not open on AI use')
                await page.fill('#aEmail', 'a@b.co'); await page.fill('#aPass', 'password1'); await page.click('[data-acct="signin"]'); await page.wait_for_timeout(500)
                if 'missing scope' not in await page.inner_text('dialog.acct') and 'User' not in await page.inner_text('dialog.acct'): errs.append('sign-in error not shown')
                await page.click('[data-acct="close"]')
                ov = await page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
                if ov > 1: errs.append(f'{w}: overflow {ov}')
                await page.screenshot(path=f'/tmp/claude-0/-home-claude/4ed579fd-372d-5fbd-bef3-b5ed49c38207/scratchpad/site_{w}.png')
                for pg in ('terms.html', 'privacy.html', 'reset.html'):
                    r = await page.goto('http://localhost:8765/' + pg)
                    if r.status != 200: errs.append(pg)
            await b.close()
    finally:
        srv.terminate()
    print('site errors:', len(errs)); [print('  ', e) for e in errs]
    sys.exit(1 if errs else 0)
asyncio.run(main())
