import asyncio, json, sys, os
from playwright.async_api import async_playwright
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'file://' + R + '/out/index.html'
MOCK = r"""
window.__said = []; window.__phrases = [];
class FakeRec { constructor(){ this.on = false; } start(){ if (this.on) throw new Error('already started'); this.on = true; setTimeout(() => this.onstart && this.onstart(), 5); const p = window.__phrases.shift(); if (p) setTimeout(() => { if (!this.on) return; const r = [{transcript: p}]; r.isFinal = true; this.onresult({resultIndex: 0, results: [r]}); }, 60); } stop(){ if (!this.on) return; this.on = false; setTimeout(() => this.onend && this.onend(), 5); } abort(){ this.stop(); } }
window.webkitSpeechRecognition = FakeRec; window.SpeechRecognition = FakeRec;
Object.defineProperty(window, 'speechSynthesis', {configurable: true, value: {speak(u){ window.__said.push(u.text); setTimeout(() => u.onend && u.onend(), 20); }, cancel(){}, getVoices(){ return [{name: 'Google UK English Female', lang: 'en-GB'}, {name: 'Google UK English Male', lang: 'en-GB'}]; }, addEventListener(){} }});
window.SpeechSynthesisUtterance = function(t){ this.text = t; };
window.claude = { use: async (cap) => {
  if (cap === 'sample') { const f = async (turns, o) => { const last = turns[turns.length-1].content; const t = /examiner/i.test(last) ? '[Examiner] HR 110, BP 120/80. ECG: sinus tachycardia.' : '(fidgets) It started suddenly at my desk, doctor. It really scared me.'; if (o && o.onText) { o.onText({text: t.slice(0, 40)}); o.onText({text: t}); } return {text: t}; };
    f.json = async (p) => { const ids = [...p.matchAll(/"id":"([^"]+)"/g)].map(m => m[1]).slice(0, 6); return {global: 3, verdict: 'Borderline pass: good history, thin plan.', domains: [{score: 3, why: 'Intro and ID done'}, {score: 2, why: 'No ICE'}, {score: 3, why: 'x'}], ticked: ids, evidence: {}, missed_critical: [ids[0]], non_negotiables: [{i: 0, done: true, note: 'gelled'}, {i: 6, done: false, note: 'no ICE'}], timeline: [{t: '0:10', event: 'Introduced', good: true}], strengths: [{point: 'Warm intro', quote: 'hello my name is nana'}], fixes: [{issue: 'No ICE', t: '4:00', said: '', better: 'Is anything worrying you about this?', why: 'Communication'}], reasoning_sentence: {said: false, model: 'The important finding is...'}, ice: {ideas: true, concerns: false, expectations: false, hidden_worry: 'Fear of a heart attack: not found'}, jargon: ['tachycardia → fast heart'], safety: '', model_answer: 'So to summarise...', viva: [{q: 'What next?', a: 'ECG'}], drill: 'Ask ICE by 6:00', summary: 'Solid history; ask ICE.'}; };
    return f; }
  if (cap === 'user') return {id: async () => 'u1'};
  if (cap === 'db') return {doc: () => ({get: async () => ({exists: false}), set: async () => {}})};
  return null; } };
"""
async def check(page, label, errs):
    ov = await page.evaluate("() => document.documentElement.scrollWidth - document.documentElement.clientWidth")
    if ov > 1: errs.append(f'{label}: horizontal overflow {ov}px')

async def run(width, mock):
    errs = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={'width': width, 'height': 900})
        if mock: await ctx.add_init_script(MOCK)
        page = await ctx.new_page()
        page.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        page.on('console', lambda m: errs.append('console: ' + m.text) if m.type == 'error' else None)
        await page.goto(URL); await page.wait_for_timeout(400)
        await check(page, 'home', errs)
        for v in ['stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills']:
            await page.click(f'#nav button[data-v="{v}"]'); await page.wait_for_timeout(150); await check(page, v, errs)
        # stations filter to PP
        await page.click('#nav button[data-v="stations"]'); await page.select_option('#fGrp', 'PP'); await page.wait_for_timeout(100)
        n = await page.locator('#stList .li').count()
        if n < 105: errs.append(f'PP list only {n}')
        # open each PP station in script mode quickly
        ids = await page.evaluate("() => D.stations.filter(s=>s.pp).map(s=>s.id)")
        for sid in ids:
            await page.evaluate(f"() => {{ location.hash = 's-{sid}'; }}"); await page.wait_for_timeout(40)
            t = await page.locator('h1').first.inner_text()
            if not t: errs.append('empty station ' + sid)
            lines = await page.locator('#scriptCard .sl').count()
            if lines < 8: errs.append(f'{sid}: only {lines} script lines')
            if await page.locator('#fwCard').count() < 1: errs.append(f'{sid}: no framework card')
        await check(page, 'pp station', errs)
        # detailed: PP01
        await page.evaluate("() => { location.hash = 's-PP01'; }"); await page.wait_for_timeout(150)
        await page.click('[data-mode="script"]'); await page.check('#recallT'); await page.wait_for_timeout(80)
        if await page.locator('[data-reveal]').count() < 5: errs.append('recall mode not hiding')
        await page.locator('[data-reveal]').first.click()
        await page.uncheck('#recallT')
        await page.select_option('#varSel', 'B'); await page.wait_for_timeout(80)
        dx = await page.inner_text('#varDx')
        if 'SVT' not in dx and 'Supraventricular' not in dx: errs.append('variant dx not shown: ' + dx)
        res = await page.text_content('#resWrap')
        if '180' not in res: errs.append('results card not variant B')
        await page.click('[data-mode="tick"]'); await page.wait_for_timeout(80)
        cbs = page.locator('details.sec[open] [data-tick]'); c = await cbs.count()
        for i in range(min(c, 8)): await cbs.nth(i).check()
        pct = await page.inner_text('#pct')
        if pct == '0%': errs.append('tick score not updating')
        await page.click('[data-saveatt]')
        await page.click('[data-mode="friends"]'); await page.wait_for_timeout(60)
        for r in ['cand', 'actor', 'exam']:
            await page.click(f'[data-role="{r}"]'); await page.wait_for_timeout(60); await check(page, 'friends ' + r, errs)
            if r == 'cand':
                if await page.is_visible('#hookCard'): errs.append('hooks visible to candidate')
                if await page.is_visible('#varSel'): errs.append('variant visible to candidate')
        sels = page.locator('[data-lik]'); k = await sels.count()
        for i in range(k): await sels.nth(i).select_option('3')
        fp = await page.inner_text('#fpct')
        if fp != '75%': errs.append('friends pct ' + fp)
        await page.click('[data-savefr]')
        await page.select_option('#varSel', '?'); await page.wait_for_timeout(60)
        # AI
        aib = page.locator('[data-mode="ai"]')
        if mock:
            await aib.click(); await page.fill('#say', 'Hello, what brought you in?'); await page.click('[data-send]'); await page.wait_for_timeout(200)
            await page.fill('#say', 'examiner: findings please'); await page.click('[data-send]'); await page.wait_for_timeout(200)
            await page.click('[data-grade]'); await page.wait_for_timeout(400)
            out = await page.inner_text('#aiOut')
            if 'Domain scores' not in out: errs.append('AI grading output missing domains')
        else:
            if not await aib.is_disabled(): errs.append('AI button should be disabled without claude')
        # bank station
        await page.evaluate("() => { location.hash = 's-CV06'; }"); await page.wait_for_timeout(150)
        for md in ['script', 'tick', 'friends']:
            await page.click(f'[data-mode="{md}"]'); await page.wait_for_timeout(60); await check(page, 'bank ' + md, errs)
        await page.click('[data-role="actor"]'); await page.click('[data-role="exam"]')


        # ---- v4: voice station ----
        if mock:
            await page.evaluate("() => { location.hash = 's-PP01'; }"); await page.wait_for_timeout(150)
            await page.click('[data-mode="voice"]'); await page.wait_for_timeout(80)
            await page.evaluate("() => { S.set.vRead = false; S.set.vPause = 300; window.__phrases = ['hello my name is nana a third year medical student can i check your name and date of birth', 'what has brought you in today', 'examiner could i have the observations please']; }")
            await page.click('[data-vstart]'); await page.wait_for_timeout(5000)
            n = await page.locator('#vChat .msg').count()
            if n < 6: errs.append(f'voice chat only {n} messages')
            said = await page.evaluate("() => window.__said.join(' | ')")
            if 'fidgets' in said: errs.append('stage directions were spoken')
            if 'scared' not in said: errs.append('patient reply not spoken: ' + said[:120])
            if await page.locator('#vChat .msg.me').filter(has_text='📋').count() < 1: errs.append('examiner address not detected')
            await check(page, 'voice live', errs)
            await page.click('[data-vend]'); await page.wait_for_timeout(600)
            out = await page.inner_text('#vOut')
            for k in ['Domain scores', 'Fix these next time', 'Non-negotiables', 'Reasoning sentence']:
                if k not in out: errs.append('voice feedback missing ' + k)
            await check(page, 'voice feedback', errs)
            st = await page.evaluate("() => JSON.parse(localStorage.getItem('qq-osce-v1')).att.PP01.slice(-1)[0]")
            if st.get('mode') != 'voice' or not st.get('fb'): errs.append('voice attempt not saved with feedback')
            # push to talk
            await page.evaluate("() => { window.__phrases = ['is anything worrying you']; }")
            await page.click('[data-vagain]'); await page.wait_for_timeout(400)
            await page.click('#voiceCard details summary'); await page.select_option('#vPttSel', 'ptt'); await page.wait_for_timeout(100)
            if await page.locator('[data-vptt]').count() != 1: errs.append('push-to-talk button missing')
            else:
                pb = page.locator('[data-vptt]'); await pb.dispatch_event('pointerdown'); await page.wait_for_timeout(200); await page.dispatch_event('body', 'pointerup'); await page.wait_for_timeout(800)
                if await page.locator('#vChat .msg.me').count() < 1: errs.append('push-to-talk did not send')
            await page.click('[data-vreset]'); await page.wait_for_timeout(100)
            await page.evaluate("() => { S.set.vPtt = false; save(); }")
        else:
            await page.evaluate("() => { location.hash = 's-PP01'; }"); await page.wait_for_timeout(150)
            if not await page.locator('[data-mode="voice"]').is_disabled(): errs.append('voice should be disabled without claude')
        # ---- v4: all hooks ----
        await page.click('#nav button[data-v="hooks"]'); await page.wait_for_timeout(150)
        nh = await page.locator('#hAll .hkall').count()
        if nh < 250: errs.append(f'all hooks only {nh}')
        await page.fill('#hQ', 'warfarin'); await page.wait_for_timeout(400)
        nw = await page.locator('#hAll .hkall').count()
        if not (0 < nw < nh): errs.append(f'hook filter {nw}')
        await check(page, 'all hooks', errs)
        await page.fill('#hQ', ''); await page.wait_for_timeout(300)
        await page.click('[data-hview="drill"]'); await page.wait_for_timeout(100)
        # ---- v3: frameworks ----
        await page.click('#nav button[data-v="fw"]'); await page.wait_for_timeout(100)
        tiles = await page.locator('#main .tile').count()
        if tiles != 9: errs.append(f'fw tiles {tiles}')
        await page.locator('#main .tile').first.click(); await page.wait_for_timeout(100)
        await page.select_option('#fwMem', 'chest'); await page.wait_for_timeout(100)
        if await page.locator('.chg').count() < 3: errs.append('fw changes not shown')
        await page.check('#fwOnly'); await page.wait_for_timeout(80)
        if await page.locator('.fst.dim').count() < 1: errs.append('fw only-changes toggle')
        await page.uncheck('#fwOnly')
        await check(page, 'fwone', errs)
        mems = await page.evaluate("() => D.fw.list.flatMap(f => f.m.map(m => f.id + '--' + m.id)).concat(D.fw.list.map(f => f.id))")
        for h in mems:
            await page.evaluate(f"() => {{ location.hash = 'fw-{h}'; }}"); await page.wait_for_timeout(30)
            if await page.locator('.fst').count() < 5: errs.append('fw page empty ' + h)
        await check(page, 'fw members', errs)
        # per-case door
        await page.evaluate("() => { location.hash = 's-PP03'; }"); await page.wait_for_timeout(120)
        await page.select_option('#varSel', 'C'); await page.wait_for_timeout(80)
        if 'mechanical' not in (await page.inner_text('#briefP')): errs.append('per-case door not shown')
        await page.click('#fwCard summary'); await page.wait_for_timeout(60); await check(page, 'fwCard open', errs)
        # fw deck
        await page.click('#nav button[data-v="hooks"]'); await page.wait_for_timeout(80)
        await page.click('[data-hview="drill"]'); await page.wait_for_timeout(80)
        await page.select_option('#hDeck', 'fw'); await page.wait_for_timeout(80)
        await page.click('[data-hshow]'); await page.wait_for_timeout(60)
        if await page.locator('.flash .back .nnr').count() < 1: errs.append('fw deck back empty')
        await check(page, 'fw deck', errs)
        await page.select_option('#hDeck', 'all'); await page.wait_for_timeout(60)
        # hooks drill
        await page.click('#nav button[data-v="hooks"]'); await page.wait_for_timeout(100)
        for i in range(3):
            await page.click('[data-hshow]'); await page.wait_for_timeout(40); await check(page, 'hook back', errs)
            await page.click('[data-hk="ok"]' if i % 2 else '[data-hk="a"]'); await page.wait_for_timeout(40)
        await page.select_option('#hDeck', 'ilo'); await page.wait_for_timeout(60)
        await page.click('[data-hshow]')
        # exam, proc, ilo, frame views
        for h in ['e-cvs', 'p-abpi', 'u41', 'f-hx']:
            await page.evaluate(f"() => {{ location.hash = '{h}'; }}"); await page.wait_for_timeout(100); await check(page, h, errs)
        # search
        await page.evaluate("() => { location.hash = 'home'; }")
        if width < 620: await page.click('#qBtn')
        await page.fill('#q', 'cholangitis'); await page.wait_for_timeout(350)
        if await page.locator('#main .li').count() < 1: errs.append('search found nothing')
        await page.fill('#q', 'jaundice'); await page.wait_for_timeout(350)
        if await page.locator('#main [data-fwm]').count() < 1: errs.append('search: no framework chips')
        await check(page, 'search', errs)
        st = await page.evaluate("() => JSON.parse(localStorage.getItem('qq-osce-v1'))")
        if not st['att'].get('PP01'): errs.append('attempt not saved')
        if not st['hk']: errs.append('hook progress not saved')
        await b.close()
    return errs

async def main():
    allerr = []
    for w, mock in [(1280, False), (390, False), (390, True), (1280, True)]:
        e = await run(w, mock); print(w, 'mock' if mock else 'plain', 'errors:', len(e))
        for x in e[:15]: print('  ', x)
        allerr += e
    sys.exit(1 if allerr else 0)
asyncio.run(main())
