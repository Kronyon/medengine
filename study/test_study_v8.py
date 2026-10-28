#!/usr/bin/env python3
"""medengine-STUDY v0.8 tests (no network): Remix (paste parser, unit matching, offline remix, AI remix via a mock,
errors, keyboard 1-5/Enter, vault, replay, only-misses, clear), speed tags + filter, plain-word labels, overflow."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"

NAV = "PassMedicine\nMedical student finals / UKMLA resource\nHome\nUKMLA Content Map 2026\n\nQUESTIONS\nQuestion bank\nPrevious sessions\nMock exams\nReview questions\nPerformance\nComment threads\n\nTEXTBOOKS\nHigh-yield textbook\nExtended textbook\n\nKNOWLEDGE TUTOR\nKnowledge tutor\nReview facts\nPerformance\n\nCUSTOM REVISION\nRevision sets\n\nCONCEPTS\nAll concepts\nTop 100 concepts\n\n"
SAMPLE_A = NAV + """Question 14 of 50
A 45-year-old woman presents with a 3-day history of constant right upper quadrant pain, a fever of 38.6°C and vomiting. She has had shorter episodes of similar pain after fatty meals over the last year.
On examination she is tender in the right upper quadrant and catches her breath on deep palpation there. Bloods show WCC 15.2 x 10^9/L, bilirubin 14 µmol/L.
What is the most likely diagnosis?
Biliary colic 31%
Acute cholecystitis 52%
Ascending cholangitis 9%
Acute pancreatitis 5%
Hepatitis A 3%
Incorrect
You answered Biliary colic
The correct answer is Acute cholecystitis
Acute cholecystitis
Pain lasting longer than 6 hours with fever and a raised white cell count suggests acute cholecystitis rather than biliary colic. Murphy's sign is often positive.
Important for me
Less important
Comments
12 comments
Great question!
"""
SAMPLE_B = """A 68-year-old man has had 6 weeks of painless jaundice, pale stools, dark urine and weight loss. A smooth, non-tender mass is felt under the right costal margin.
Which is the most likely diagnosis?
A. Acute cholecystitis
B. Pancreatic cancer
C. Biliary colic
D. Ascending cholangitis
E. Hepatitis A
The correct answer is B
"""
SAMPLE_C = """A 63-year-old man presents to the emergency department with 1 hour of severe pain in his left groin and he is unable to identify a trigger for it. He is on the waiting list for a left inguinal hernia repair. On examination, there is a tender, erythematous lump superomedial to the pubic tubercle, separate from the testis, that does not disappear in the supine position. A cough impulse is absent. What is the next step in management?
Apply a cold compress to the area0%
Attempt at manual reduction9%
Proceed immediately to theatre for laparoscopic repair40%
Proceed immediately to theatre for open repair46%
Request CT abdomen and pelvis5%
"""
SAMPLE_D = NAV + """A 58-year-old man with type 2 diabetes has an HbA1c of 62 mmol/mol on metformin 1 g twice daily. His BMI is 27 kg/m2 and he has no cardiovascular disease. He is started on sitagliptin.
What is the mechanism of action of sitagliptin?
Increases incretin levels by inhibiting their breakdown14%
Increases insulin sensitivity via PPAR-gamma22%
Blocks glucose reabsorption in the proximal tubule9%
Closes ATP-sensitive potassium channels on beta cells11%
Reduces hepatic gluconeogenesis via AMP kinase44%
The correct answer is Increases incretin levels by inhibiting their breakdown
DPP-4 inhibitors (gliptins) stop the breakdown of GLP-1 and GIP, increasing insulin release after meals. They are weight neutral.
How does sitagliptin work? DPP-4 inhibitors and GLP-1 mimetics
Zero to Finals - YouTube 32 2
YouTube
Type 2 diabetes agents and their mechanism of action
Brandl's Basics - YouTube 7 1
YouTube
Comments
4 comments
"""
AI_JSON = {"film": "45F, 3 days constant RUQ pain, fever, raised WCC, positive Murphy's", "clue": "3 days",
           "rows": [{"if": "pain settled within 4 hours, afebrile", "hook": "a cramp that passes"},
                    {"if": "over 6 hours with fever and Murphy's", "hook": "inflamed bag stops the breath"},
                    {"if": "jaundice, fever and rigors", "hook": "yellow, hot and shaking"},
                    {"if": "epigastric pain through to the back", "hook": "pain boring into the back"},
                    {"if": "", "hook": "no colic pattern at all"}]}
# a real Passmedicine page copy (kept outside the repo): pass its path in MEDENGINE_REAL_PASTE to test against it
import os
REAL = pathlib.Path(os.environ.get('MEDENGINE_REAL_PASTE', '/nonexistent'))
PASTE = """(t) => { const dt = new DataTransfer(); dt.setData('text/plain', t); document.body.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true})); }"""


def run(width, mock=True):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900}, accept_downloads=True)
        if mock: ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500)

        def ov(label):
            o = pg.evaluate('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: horizontal overflow {o}px')

        def hashgo(h, wait=400):
            pg.evaluate(f"location.hash = '{h}'"); pg.wait_for_timeout(wait)

        if not re.search(r'v(0\.([89]|1\d)|[12]\.\d+)\.\d', pg.text_content('#homeBtn')): errs.append('version not 0.8+')
        if not pg.locator('#main [data-go="remix"]').count(): errs.append('home: no Remix button')

        # ---- parser + matching (pure functions) ----
        a = pg.evaluate('t => __me8.rmxParse(t)', SAMPLE_A)
        if a['opts'] != ['Biliary colic', 'Acute cholecystitis', 'Ascending cholangitis', 'Acute pancreatitis', 'Hepatitis A']: errs.append(f"parser A options: {a['opts']}")
        if a['correct'] != 1 or a['picked'] != 0: errs.append(f"parser A correct/picked: {a['correct']}/{a['picked']}")
        if not a['stem'].startswith('A 45-year-old') or not a['stem'].endswith('diagnosis?'): errs.append('parser A stem: ' + a['stem'][:80])
        if 'PassMedicine' in a['stem'] or 'comments' in a['expl'].lower() or 'Great question' in a['expl']: errs.append('parser A kept page junk')
        if 'Murphy' not in a['expl']: errs.append('parser A lost the explanation')
        cq = pg.evaluate('t => __me8.rmxParse(t)', SAMPLE_C)
        if cq['opts'] != ['Apply a cold compress to the area', 'Attempt at manual reduction', 'Proceed immediately to theatre for laparoscopic repair', 'Proceed immediately to theatre for open repair', 'Request CT abdomen and pelvis']: errs.append(f"parser C (glued %): {cq['opts']}")
        dq = pg.evaluate('t => __me8.rmxParse(t)', SAMPLE_D)
        if not dq['stem'].startswith('A 58-year-old') or dq['correct'] != 0 or len(dq['opts']) != 5 or dq['opts'][4] != 'Reduces hepatic gluconeogenesis via AMP kinase': errs.append(f"parser D (video links after the explanation): {dq['stem'][:50]} {dq['opts']} {dq['correct']}")
        if 'YouTube' in dq['expl']: errs.append('parser D kept video links in the explanation')
        if REAL.exists():
            rq = pg.evaluate('t => __me8.rmxParse(t)', REAL.read_text(encoding='utf-8'))
            if not re.match(r'A \d+-year-old', rq['stem']) or not re.search(r'HbA1c \d', rq['stem']) or not rq['stem'].endswith('?') or 'Reference ranges' in rq['stem']: errs.append('real paste stem: ' + rq['stem'][:120])
            if len(rq['opts']) != 5 or any(re.search(r'\d%$', o) for o in rq['opts']) or any('YouTube' in o for o in rq['opts']): errs.append(f"real paste options: {rq['opts']}")
            if rq['correct'] != 3: errs.append(f"real paste correct: {rq['correct']}")
            if len(rq['expl']) < 200 or 'YouTube' in rq['expl'] or 'Important for me' in rq['expl']: errs.append('real paste explanation: ' + rq['expl'][:100])
        bq = pg.evaluate('t => __me8.rmxParse(t)', SAMPLE_B)
        if bq['opts'][1] != 'Pancreatic cancer' or bq['correct'] != 1 or bq['picked'] != -1: errs.append(f"parser B: {bq['opts']} {bq['correct']} {bq['picked']}")
        for txt, want in (('Acute cholecystitis', 'Gallstones'), ('Ascending cholangitis', 'Acute cholangitis'), ('Acute pancreatitis', 'Acute pancreatitis'), ("Wolff-Parkinson-White syndrome", None), ('Hepatitis A', '')):
            ui = pg.evaluate('t => __me8.rmxUnitFor(t)', txt)
            name = pg.evaluate('i => i >= 0 ? UNITS_NAME(i) : ""'.replace('UNITS_NAME(i)', "document.title && i"), ui) if False else ui
            if want == '' and ui != -1: errs.append(f'{txt} should not match a unit')
            if want and ui == -1: errs.append(f'{txt} did not match a unit')
        loc = pg.evaluate('t => { const q = __me8.rmxParse(t); return __me8.rmxLocal(q); }', SAMPLE_A)
        if len(loc['beats']) < 2: errs.append(f"offline remix built {len(loc['beats'])} rounds")
        for bt in loc['beats']:
            opt = a['opts'][bt['ans']].lower()
            if re.search(r'\b' + re.escape(opt.split()[-1]) + r'\b', bt['change'].lower()): errs.append('offline clue gives away the answer: ' + bt['change'][:70])
            whyl = bt['why'].lower()
            others = [o.lower() for k, o in enumerate(a['opts']) if k != bt['ans']]
            if any(re.search(r'\b' + re.escape(o) + r'\b', whyl) for o in others) and opt not in whyl: errs.append('offline answer key points to the wrong option: ' + bt['why'][:80])
        if len(set(bt['ans'] for bt in loc['beats'])) != len(loc['beats']): errs.append('offline rounds repeat the same answer')

        # ---- offline flow (no AI in this view) ----
        pg.evaluate('__me8.setAi(null)')
        hashgo('remix')
        ov('remix home')
        pg.evaluate(PASTE, SAMPLE_A); pg.wait_for_timeout(200)
        if pg.locator('.rmx-opt').count() != 5: errs.append('check screen: options not shown')
        if 'ok' not in (pg.get_attribute('.rmx-opt:nth-child(2)', 'class') or ''): errs.append('check screen: correct not pre-ticked')
        if 'me' not in (pg.get_attribute('.rmx-opt:nth-child(1)', 'class') or ''): errs.append('check screen: pick not pre-ticked')
        pg.click('[data-rmxp="2"]'); pg.wait_for_timeout(60)
        if 'me' not in (pg.get_attribute('.rmx-opt:nth-child(3)', 'class') or ''): errs.append('✋ toggle failed')
        pg.click('[data-rmxp="0"]'); pg.wait_for_timeout(60)
        ov('remix check')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(200)
        if not pg.locator('#rmx .rmx-case').count(): errs.append('offline remix card not shown')
        n = pg.evaluate('__me8.rmx.card.c.beats.length')
        for i in range(n):
            ans = pg.evaluate('__me8.rmx.card.c.beats[__me8.rmx.i].ans')
            pg.keyboard.press(str(ans + 1 if i else (ans + 1) % 5 + 1)); pg.wait_for_timeout(80)
            if not pg.locator('#rmx .opt.right').count(): errs.append('answer not revealed after key press')
            pg.keyboard.press('Enter'); pg.wait_for_timeout(80)
        res = pg.evaluate('__me8.rmx.card.res')
        if res[:1] != [False] or not all(res[1:]): errs.append(f'results not recorded: {res}')
        if pg.evaluate('__me8.rmxAll().length') != 1: errs.append('remix not saved to the vault')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        if pg.evaluate('__me8.rmx.step') != 'home': errs.append('Enter after the end did not reset')

        # ---- AI flow (mock sample) ----
        pg.evaluate("j => __me8.setAi(Object.assign(async () => ({text: ''}), {json: async () => j}))", AI_JSON)
        pg.evaluate(PASTE, SAMPLE_A); pg.wait_for_timeout(150)
        if not pg.locator('[data-rmxai]').count(): errs.append('AI remix button missing when AI is available')
        pg.click('[data-rmxai]'); pg.wait_for_timeout(300)
        card = pg.evaluate('__me8.rmx.card')
        if not card or card['src'] != 'ai': errs.append('AI card not built')
        else:
            ks = [x['k'] for x in card['c']['beats']]
            if ks != ['if', 'if', 'if']: errs.append(f'AI beats: {ks}')
            if card['c']['beats'][0]['ans'] != 0: errs.append('first round should be the option you picked')
            if sorted(x['ans'] for x in card['c']['beats']) != [0, 2, 3]: errs.append('rounds should be the wrong options that have a clue')
            if any(x['opts'] != a['opts'] for x in card['c']['beats']): errs.append('rounds must keep the options in place')
            t = pg.text_content('#rmx')
            if '45F, 3 days constant RUQ pain' not in t: errs.append('film line missing')
            if 'If instead:' not in t or 'pain settled within 4 hours' not in t: errs.append('round change not shown')
            for k in ('1', 'Enter', '2', 'Enter', '3', 'Enter'): pg.keyboard.press(k); pg.wait_for_timeout(70)
            if pg.evaluate('__me8.rmx.card.res.length') != 3 or pg.evaluate('__me8.rmx.card.res[0]') is not True: errs.append('AI card answers not recorded')
            ov('remix AI card')
        pg.click('[data-rmxreset]'); pg.wait_for_timeout(100)
        # AI error → message + offline still offered
        pg.evaluate("__me8.setAi(Object.assign(async () => ({text: ''}), {json: async () => { throw {code: 'invalid_json', message: 'x'}; }}))")
        pg.evaluate(PASTE, SAMPLE_B); pg.wait_for_timeout(150)
        pg.click('[data-rmxai]'); pg.wait_for_timeout(200)
        if 'garbled' not in pg.text_content('#rmx') or not pg.locator('[data-rmxlocal]').count(): errs.append('AI error not handled')
        pg.click('[data-rmxreset]'); pg.wait_for_timeout(100)

        # ---- vault: replay, only misses, export, clear ----
        if pg.evaluate('__me8.rmxAll().length') != 2: errs.append('vault should hold 2 cards')
        nm = pg.evaluate('__me8.rmxAll().filter(c => c.res.some(r => r === false)).length')
        if nm < 1 or f'Only misses · {nm}' not in pg.text_content('#rmxVault'): errs.append('only-misses count wrong')
        pg.click('[data-rmxmiss]'); pg.wait_for_timeout(80); pg.click('[data-rmxreplay]'); pg.wait_for_timeout(150)
        if f'Replay 1 / {nm}' not in pg.text_content('#rmx'): errs.append('replay misses did not start')
        # getting out of a replay: Esc, the button, or just pasting a new question
        if 'Stop replay' not in pg.text_content('#rmx'): errs.append('no Stop replay button during a replay')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(120)
        if pg.evaluate('__me8.rmx.step') != 'home' or pg.evaluate('__me8.rmx.queue') is not None: errs.append('Esc did not leave the replay')
        if pg.evaluate("document.activeElement && document.activeElement.id") != 'rmxIn': errs.append('paste box not focused after leaving')
        pg.click('[data-rmxreplay]'); pg.wait_for_timeout(120); pg.click('#rmx [data-rmxreset]'); pg.wait_for_timeout(120)
        if pg.evaluate('__me8.rmx.step') != 'home': errs.append('Stop replay button did not leave the replay')
        pg.click('[data-rmxreplay]'); pg.wait_for_timeout(120); pg.evaluate(PASTE, SAMPLE_B); pg.wait_for_timeout(150)
        if pg.evaluate('__me8.rmx.step') != 'check' or pg.evaluate('__me8.rmx.queue') is not None: errs.append('pasting during a replay did not start a new question')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        pg.click('[data-rmxmiss]'); pg.wait_for_timeout(80)
        if pg.locator('[data-rmxexport]').count():
            try:
                with pg.expect_download(timeout=3000) as dl: pg.click('[data-rmxexport]')
                if not dl.value.suggested_filename.endswith('.json'): errs.append('export filename')
            except Exception as e:
                if not mock: errs.append('export did not download: ' + str(e)[:80])
        pg.reload(); pg.wait_for_timeout(1200); hashgo('remix')
        if pg.evaluate('__me8.rmxAll().length') != 2: errs.append('vault not kept after reload')
        pg.click('[data-rmxclear]'); pg.wait_for_timeout(60)
        if pg.evaluate('__me8.rmxAll().length') != 2: errs.append('clear deleted on the first tap')
        pg.click('[data-rmxclear]'); pg.wait_for_timeout(100)
        if pg.evaluate('__me8.rmxAll().length') != 0: errs.append('clear did not empty the vault')

        # ---- speed tags ----
        hashgo('u91-read', 500)
        if '⚡ Sudden' not in (pg.text_content('#main .spdline') or ''): errs.append('SAH speed badge missing')
        hashgo('home', 400)
        pg.evaluate("document.querySelector('details.sysrow').open = true"); pg.wait_for_timeout(80)
        pg.click('[data-spdset="s"]'); pg.wait_for_timeout(200)
        if width < 860: pg.evaluate("document.body.classList.remove('nav')")
        side = pg.evaluate("Array.from(document.querySelectorAll('#side [data-u]')).length")
        want = len(json.load(open(HERE / 'v08_content.json'))['spd']['s']) + 1  # aortic dissection sits in 2 ILO weeks
        if side != want: errs.append(f'speed filter shows {side} units, expected {want}')
        pg.reload(); pg.wait_for_timeout(1300)
        if pg.evaluate("Array.from(document.querySelectorAll('#side [data-u]')).length") != want: errs.append('speed filter not kept after reload')
        hashgo('home', 300); pg.evaluate("document.querySelector('details.sysrow').open = true"); pg.wait_for_timeout(60)
        if width < 860: pg.evaluate("document.body.classList.remove('nav')")
        pg.click('[data-spdset="s"]'); pg.wait_for_timeout(150)
        if pg.evaluate("Array.from(document.querySelectorAll('#side [data-u]')).length") < 160: errs.append('speed filter did not clear')
        ov('home')

        # ---- plain words ----
        hashgo('jargon')
        t = pg.text_content('#main')
        for w in ('4K', 'collision', '2-Hammer', 'Triangulat', 'opaque'):
            if w.lower() in t.lower(): errs.append('buzzword left: ' + w)
        hashgo('sniper'); pg.click('[data-snpmode="m3"]'); pg.wait_for_timeout(150)
        t = pg.text_content('#main')
        for w in ('Strike', '2-Hammer', 'Triangulat', 'lethal contraindication'):
            if w.lower() in t.lower(): errs.append('sniper buzzword left: ' + w)
        pg.click('[data-snpmode="clue"]'); pg.wait_for_timeout(100)
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px STUDY v0.8 errors: {len(e)}'); [print('  -', x) for x in e]
    e = run(1280, mock=False); bad += len(e)
    print(f'no-runtime STUDY v0.8 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
