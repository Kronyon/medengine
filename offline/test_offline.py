#!/usr/bin/env python3
"""Tests the offline bundle over file:// with the Anthropic API faked (no network, no claude.ai)."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

DIST = pathlib.Path(__file__).resolve().parent / 'dist' / 'medengine'
MARK = {"global": 3, "verdict": "Borderline pass: good history, thin plan.",
        "domains": [{"score": 3, "why": "Intro and ID done"}, {"score": 2, "why": "No ICE"}, {"score": 3, "why": "x"}],
        "ticked": [], "evidence": {}, "missed_critical": [], "non_negotiables": [{"i": 0, "done": True, "note": "gelled"}],
        "timeline": [{"t": "0:10", "event": "Introduced", "good": True}], "strengths": [{"point": "Warm intro", "quote": "hello"}],
        "fixes": [{"issue": "No ICE", "t": "4:00", "said": "", "better": "Is anything worrying you?", "why": "Communication"}],
        "reasoning_sentence": {"said": False, "model": "The important finding is..."},
        "ice": {"ideas": True, "concerns": False, "expectations": False, "hidden_worry": "Fear of MI"},
        "jargon": [], "safety": "", "model_answer": "So to summarise...", "viva": [{"q": "What next?", "a": "ECG"}],
        "drill": "Ask ICE by 6:00", "summary": "Solid history; ask ICE."}
calls = []


def fake_api(route):
    req = route.request
    body = json.loads(req.post_data or '{}')
    calls.append({'key': req.headers.get('x-api-key'), 'browser': req.headers.get('anthropic-dangerous-direct-browser-access'),
                  'model': body.get('model'), 'stream': body.get('stream')})
    if req.headers.get('x-api-key') == 'sk-ant-bad':
        return route.fulfill(status=401, headers={'access-control-allow-origin': '*', 'content-type': 'application/json'},
                             body=json.dumps({'type': 'error', 'error': {'type': 'authentication_error', 'message': 'invalid x-api-key'}}))
    if body.get('stream'):
        last = body['messages'][-1]['content']
        text = '[Examiner] HR 110, BP 120/80.' if 'examiner: findings please' in last.lower() else '(fidgets) It started suddenly at my desk, doctor.'
        parts = [text[:15], text[15:]]
        sse = 'event: message_start\ndata: {"type":"message_start","message":{}}\n\n'
        for p in parts:
            sse += 'event: content_block_delta\ndata: ' + json.dumps({'type': 'content_block_delta', 'index': 0, 'delta': {'type': 'text_delta', 'text': p}}) + '\n\n'
        sse += 'event: message_delta\ndata: {"type":"message_delta","delta":{"stop_reason":"end_turn"}}\n\nevent: message_stop\ndata: {"type":"message_stop"}\n\n'
        return route.fulfill(status=200, headers={'access-control-allow-origin': '*', 'content-type': 'text/event-stream'}, body=sse)
    prompt = body['messages'][-1]['content']
    if 'single word: ready' in prompt:
        out = 'ready'
    else:
        m = dict(MARK); m['ticked'] = re.findall(r'"id":"([^"]+)"', prompt)[:6]
        out = '```json\n' + json.dumps(m) + '\n```'
    return route.fulfill(status=200, headers={'access-control-allow-origin': '*', 'content-type': 'application/json'},
                         body=json.dumps({'content': [{'type': 'text', 'text': out}], 'stop_reason': 'end_turn'}))


def main():
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': 1280, 'height': 900})
        ctx.route('https://api.anthropic.com/**', fake_api)
        ctx.route(re.compile(r'^https?://(?!api\.anthropic\.com).*'), lambda r: r.abort())  # prove it runs with no other network
        page = ctx.new_page()
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        page.on('dialog', lambda d: d.dismiss())

        # launcher → OSCE with key 1
        page.goto((DIST / 'medengine.html').as_uri()); page.wait_for_timeout(300)
        if 'claude.ai' in page.content(): errs.append('launcher mentions claude.ai links')
        page.keyboard.press('1'); page.wait_for_load_state(); page.wait_for_timeout(800)
        if not page.url.endswith('osce.html'): errs.append('key 1 did not open osce.html: ' + page.url)
        if page.locator('#aiKeyBtn').count() != 1: errs.append('no AI key button')

        # AI with no key → key panel opens
        page.evaluate("() => { location.hash = 's-PP01'; }"); page.wait_for_timeout(300)
        aib = page.locator('[data-mode="ai"]')
        if aib.is_disabled(): errs.append('AI mode disabled in offline build')
        aib.click(); page.fill('#say', 'Hello'); page.click('[data-send]'); page.wait_for_timeout(400)
        if not page.locator('dialog.acct[open]').count(): errs.append('key panel did not open without a key')

        # bad key → rejected message
        page.fill('#okKey', 'sk-ant-bad'); page.click('#okSave'); page.wait_for_timeout(100)
        page.click('#okTest'); page.wait_for_timeout(500)
        if 'rejected' not in page.inner_text('dialog.acct'): errs.append('bad key not reported: ' + page.inner_text('dialog.acct')[:200])
        # good key → test passes
        page.fill('#okKey', 'sk-ant-good-123456'); page.click('#okSave'); page.wait_for_timeout(100)
        page.click('#okTest'); page.wait_for_timeout(500)
        if 'Key works' not in page.inner_text('dialog.acct'): errs.append('good key test failed: ' + page.inner_text('dialog.acct')[:200])
        page.click('#okClose')
        if '🟢' not in page.inner_text('#aiKeyBtn'): errs.append('key button not green')

        # AI patient (streamed) + examiner marking (json)
        page.reload(); page.wait_for_timeout(800)
        page.evaluate("() => { location.hash = 's-PP01'; }"); page.wait_for_timeout(300)
        page.click('[data-mode="ai"]'); page.wait_for_timeout(100)
        page.fill('#say', 'Hello, what brought you in?'); page.click('[data-send]'); page.wait_for_timeout(500)
        page.fill('#say', 'examiner: findings please'); page.click('[data-send]'); page.wait_for_timeout(500)
        chat = page.inner_text('#main')
        if 'started suddenly at my desk' not in chat: errs.append('streamed patient reply missing')
        if 'HR 110' not in chat: errs.append('examiner reply missing')
        page.click('[data-grade]'); page.wait_for_timeout(800)
        out = page.inner_text('#aiOut') if page.locator('#aiOut').count() else ''
        if 'Domain scores' not in out: errs.append('marking output missing: ' + out[:200])
        if not calls or any(c['browser'] != 'true' or c['key'] not in ('sk-ant-bad', 'sk-ant-good-123456') for c in calls): errs.append('bad request headers')
        if not any(c['model'] == 'claude-haiku-5-5' and c['stream'] for c in calls): errs.append('quick tier did not stream on the fast model')
        if not any(c['model'] == 'claude-sonnet-5-5' and not c['stream'] for c in calls): errs.append('marking did not use the smart model')

        # links between apps stay local
        if page.get_attribute('#drillLink', 'href') != 'study.html': errs.append('drill link not local')
        with ctx.expect_page() as np: page.click('#drillLink')
        page = np.value; page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e))); page.wait_for_load_state(); page.wait_for_timeout(1500)
        if not page.url.endswith('study.html'): errs.append('STUDY did not open: ' + page.url)
        if 'medengine-STUDY' not in page.title(): errs.append('STUDY title wrong')
        hrefs = page.evaluate("() => [...document.querySelectorAll('a[href]')].map(a => a.getAttribute('href'))")
        if any('claude.ai' in h for h in hrefs): errs.append('STUDY has claude.ai links')
        # a page image loads from the folder
        ok = page.evaluate("""() => new Promise(r => { const i = new Image(); i.onload = () => r(i.naturalWidth > 0); i.onerror = () => r(false); i.src = 'img/p009.webp'; })""")
        if not ok: errs.append('STUDY image did not load')
        b.close()
    print('offline errors:', len(errs))
    for e in errs: print(' -', e)
    print('api calls:', len(calls))
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
