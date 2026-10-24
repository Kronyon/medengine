#!/usr/bin/env python3
"""medengine-STUDY v0.9.1 Remix tests (no network). Passmed-layout pastes written in our own words (no Passmed text
in the repo): key concept, condition tag → ILO, per-option explanations, unanswered-paste warning, × marks;
the simple card (one amber change line, no animation, no extra boxes), 🚩 flag, "Compare all five" tucked away;
instant replays with next time's variations made in the background (avoid list); spacing (due today, 1 → 3 days,
wrong → tomorrow, leaving half-way); image paste (pending, attach, sent to AI, outside the Screenshot vault, zoom);
careful mode; Weak spots panel; misses by system; overflow at 3 widths."""
import json, os, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
REAL = pathlib.Path(os.environ.get('MEDENGINE_REAL_PASTE', '/nonexistent'))

STONE = """PassMedicine
Reference ranges
End and review
Question 42 of 4,945
A 52-year-old woman attends with sudden severe right loin pain spreading to the groin. She is afebrile and her abdomen is soft. A non-contrast CT KUB shows a 6 mm stone in the distal ureter. Her bloods are below:
Creatinine\t98 µmol/L\t(60–110 µmol/L)
White Cell Count\t9 x10^9/L\t(4–11 x10^9/L)
What is the most appropriate next step?
Watchful waiting with analgesia only14%
Emergency nephrostomy3%
Analgesia and an alpha blocker to help passage61%
Percutaneous nephrolithotomy7%
Open ureterolithotomy15%
Stones under 10 mm usually pass with analgesia and an alpha blocker
Important for meLess important
Deep dive
Analgesia and an alpha blocker to help passage is the correct answer because small distal stones usually pass and the alpha blocker relaxes the ureter. Review if it has not passed.
Watchful waiting with analgesia only could be reasonable for a stone under 5 mm. This one is larger.
Emergency nephrostomy is for an obstructed, infected kidney. She is afebrile.
Percutaneous nephrolithotomy is for large renal stones over 20 mm.
Open ureterolithotomy is rarely used now. Less invasive options come first.
Textbooks
High-yield textbook
Extended textbook
UKMLA Content Map 2026
Presentation
Loin pain
Condition
Urinary tract calculi
AOCP / AOPK
Renal and ureteric stones
Urology
Suggest better categorisation
Links
Example guideline\t12 4
Score: 42.9%
1
2
8-10\t1 / 3
Back to top
All contents of this site are © 2026 Passmedicine Limited
"""
UNANSWERED = """PassMedicine
Question 1 of 4,903
A 38-year-old man has had sudden weakness of his left arm and face for 40 minutes. It is now resolving. He is in atrial fibrillation and takes no medication.
Which investigation should be arranged first?
CT head ×
Carotid doppler ×
Echocardiogram ×
24 hour ECG ×
Lumbar puncture ×
Submit answer
"""
AI = {"film": "52F, sudden right loin pain to groin, afebrile, 6 mm distal ureteric stone",
      "clue": "6 mm stone in the distal ureter", "code": "Pass, push, drain or remove: size vs infection",
      "rows": [{"if": "a stone under 5 mm", "hook": "a grain of sand slips through", "how": "**tiny stone** → ureter wide enough → **passes alone**"},
               {"if": "fever and rigors with the stone", "hook": "pus behind a dam: drain it", "how": "blocked ureter → infected urine trapped → sepsis → drain above"},
               {"if": "6 mm distal stone, no infection", "hook": "small and low: help it out"},
               {"if": "a 25 mm stone in the kidney", "hook": "a boulder needs a tunnel"},
               {"if": "", "hook": "open surgery is a last resort"}]}
FRESH = {"rows": [{"if": "a 3 mm stone", "hook": "it falls out by itself"},
                  {"if": "temperature 39°C and a raised CRP", "hook": "hot, blocked kidney"},
                  {"if": "6 mm distal stone, no infection", "hook": "small and low: help it out"},
                  {"if": "a staghorn stone filling the kidney", "hook": "antlers in the kidney"},
                  {"if": "", "hook": "open surgery is a last resort"}]}
PASTE = """(t) => { const dt = new DataTransfer(); dt.setData('text/plain', t); document.body.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true})); }"""
PASTE_IMG = """async () => { const c = document.createElement('canvas'); c.width = 400; c.height = 160; const x = c.getContext('2d'); x.fillStyle = '#fff'; x.fillRect(0, 0, 400, 160); x.strokeStyle = '#000'; x.beginPath(); for (let i = 0; i < 400; i += 4) x.lineTo(i, 80 + (i % 40 === 0 ? -50 : 0)); x.stroke();
  const blob = await new Promise(r => c.toBlob(r, 'image/png')); const dt = new DataTransfer(); dt.items.add(new File([blob], 'ecg.png', {type: 'image/png'}));
  document.body.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true})); }"""
SET_AI = """([full, fresh, img, delay]) => { window.__calls = []; __me8.setAi(Object.assign(async () => ({text: ''}), {
  json: async (p, o) => { window.__calls.push({fresh: p.includes('REVIEW ROUND'), avoid: p.includes('ALREADY USED'), p, tier: o.modelTier, max: o.maxTokens, img: !!o.images, imgType: o.images ? o.images.type : ''});
    if (delay) await new Promise(r => setTimeout(r, delay)); return JSON.parse(JSON.stringify(p.includes('REVIEW ROUND') ? fresh : full)); },
  limits: async () => (img ? {maxPromptBytes: 262144, images: {maxCount: 5}} : {maxPromptBytes: 262144})}), img); }"""


def run(width, mock=True):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        if mock: ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500)
        ev = pg.evaluate

        def ov(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: horizontal overflow {o}px')

        def hashgo(h, wait=400):
            ev(f"location.hash = '{h}'"); pg.wait_for_timeout(wait)

        def answer_all(right=True):
            n = ev('__me8.rmx.card.c.beats.length')
            for i in range(n):
                if ev('__me8.rmx.i') >= ev('__me8.rmx.card.c.beats.length'): break
                a = ev('__me8.rmx.card.c.beats[__me8.rmx.i].ans')
                pg.keyboard.press(str(a + 1 if right else (a + 1) % 4 + 1)); pg.wait_for_timeout(60)
                pg.keyboard.press('Enter'); pg.wait_for_timeout(60)

        if not re.search(r'v1\.\d+\.\d', pg.text_content('#homeBtn')): errs.append('version not 1.x')

        # ---- parser: Passmed layout ----
        q = ev('t => __me8.rmxParse(t)', STONE)
        if q['opts'] != ['Watchful waiting with analgesia only', 'Emergency nephrostomy', 'Analgesia and an alpha blocker to help passage', 'Percutaneous nephrolithotomy', 'Open ureterolithotomy']: errs.append(f"stone options: {q['opts']}")
        if q['correct'] != 2: errs.append(f"stone correct: {q['correct']}")
        if 'Creatinine 98' not in q['stem'] or not q['stem'].endswith('next step?') or 'Reference ranges' in q['stem']: errs.append('stone stem: ' + q['stem'][:90])
        if q['concept'] != 'Stones under 10 mm usually pass with analgesia and an alpha blocker': errs.append('concept: ' + q['concept'])
        if q['cond'] != ['Urinary tract calculi']: errs.append(f"condition tag: {q['cond']}")
        if not q['optx'][1].startswith('is for an obstructed') or not q['optx'][0].startswith('could be reasonable'): errs.append(f"per-option lines: {q['optx'][:2]}")
        if q['early']: errs.append('answered paste flagged as unanswered')
        if 'Score' in q['expl'] or '8-10' in q['expl'] or 'Deep dive' in q['expl']: errs.append('page furniture left in the explanation')
        ui = ev('n => __me8.rmxCondUnit(n)', q['cond'])
        if ev('i => i >= 0 ? document.title && __UN(i) : ""'.replace('__UN(i)', "i"), ui) is None or ui < 0: errs.append('condition tag did not map to an ILO')
        if ev('t => __me8.rmxOptLine(__me8.rmxParse(t), 2)', STONE) != 'small distal stones usually pass and the alpha blocker relaxes the ureter': errs.append('offline line for the right answer')
        L = ev('t => __me8.rmxLocal(__me8.rmxParse(t))', STONE)
        want = [('if', 'a stone under 5 mm'), ('if', 'an obstructed, infected kidney'), ('if', 'small distal stones usually pass and the alpha blocker relaxes the ureter'), ('if', 'large renal stones over 20 mm'), ('why', 'rarely used now')]
        got = [(k, r.get(k, '')) for (k, _), r in zip(want, L['rows'])]
        if got != want: errs.append(f'offline rows: {got}')
        if [x['k'] for x in L['beats']] != ['if'] * 3 or sorted(x['ans'] for x in L['beats']) != [0, 1, 3]: errs.append(f"offline rounds should be Passmed's lines: {[(x['k'], x['ans']) for x in L['beats']]}")
        if any(x['opts'] != q['opts'] for x in L['beats']): errs.append('rounds must keep the same five options in the same order')
        un = ev('t => __me8.rmxParse(t)', UNANSWERED)
        if not un['early'] or un['correct'] != -1 or un['picked'] != -1 or len(un['opts']) != 5 or un['opts'][0] != 'CT head': errs.append(f"unanswered paste: early={un['early']} correct={un['correct']} picked={un['picked']} opts={un['opts']}")
        if REAL.exists():
            rq = ev('t => __me8.rmxParse(t)', REAL.read_text(encoding='utf-8'))
            if not rq['concept'] or 'Important' in rq['concept'] or not rq['cond'] or ev('n => __me8.rmxCondUnit(n)', rq['cond']) < 0 or len([x for x in rq['optx'] if x]) < 4 or len(ev('t => __me8.rmxLocal(__me8.rmxParse(t)).beats.filter(b => b.k === "if")', REAL.read_text(encoding='utf-8'))) < 2: errs.append(f"real paste v0.9 fields: concept={rq['concept'][:40]} cond={rq['cond']} optx={len([x for x in rq['optx'] if x])}")
        # helpers
        if ev("__me8.rmxMark('A 6 mm stone here', ['6 mm stone'])") != 'A <mark class="rmx-mk">6 mm stone</mark> here': errs.append('rmxMark')
        if ev("__me8.rmxAddDays('2026-12-31', 1)") != '2027-01-01': errs.append('day maths')

        # ---- AI card: rule, deciding words, spot the change, flip, flag, grid, schedule ----
        ev(SET_AI, [AI, FRESH, True, 0])
        hashgo('remix')
        ev(PASTE, UNANSWERED); pg.wait_for_timeout(150)
        if 'hasn\'t been answered yet' not in pg.text_content('#rmx'): errs.append('no warning for an unanswered paste')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(80)
        ev(PASTE, STONE); pg.wait_for_timeout(150)
        pg.click('[data-rmxp="0"]'); pg.wait_for_timeout(50)
        ev(PASTE_IMG); pg.wait_for_timeout(500)
        if not pg.locator('#rmx .rmx-thumb img').count(): errs.append('image paste on the check screen did not attach')
        ov('check screen')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(400)
        c = ev('__me8.rmx.card')
        if not c or c['src'] != 'ai': errs.append('AI card not built'); b.close(); return errs
        call = ev('window.__calls[0]')
        if not call['img'] or call['imgType'] not in ('image/webp', 'image/jpeg', 'image/png'): errs.append('image not sent to the AI')
        if 'KEY CONCEPT FROM THE QUESTION BANK: Stones under 10 mm' not in call['p']: errs.append('key concept not in the prompt')
        if call['tier'] != 'quick' or call['max'] < 2000: errs.append(f"fast mode request: {call['tier']} {call['max']}")
        # ① stays short: film with the deciding words marked, ✅, ❌, ILO chip; no rule box, chips or original question
        if pg.locator('#rmx .rmx-case .rmx-rule, #rmx .rmx-trig, #rmx .rmx-orig, #rmx details').count(): errs.append('① has extra boxes again')
        if pg.locator('#rmx .rmx-case mark.rmx-mk').count() < 1: errs.append('deciding words not highlighted in the film')
        if pg.locator('#rmx .rmx-case .rmx-gr').count() != 2: errs.append('① should have one ✅ and one ❌ line')
        elif 'a stone under 5 mm' not in pg.text_content('#rmx .rmx-case .rmx-gr.me') or '6 mm distal stone' not in pg.text_content('#rmx .rmx-case .rmx-gr.ok'): errs.append('① lines should be the same-axis rows')
        if 'If you choose' in call['p'] or 'pregnant' in call['p'].split('Rules:')[0][-400:]: errs.append('prompt drifted')
        if '"rows"' not in call['p'] or 'same patient' not in call['p'].lower(): errs.append('prompt does not ask for one row per option')
        if not c['unit'] >= 0 or ev('i => __me8.rmxCondUnit(["Urinary tract calculi"]) === i', c['unit']) is not True: errs.append('card not linked to Urinary tract calculi')
        pg.wait_for_timeout(300)
        if not pg.locator('#rmx .rmx-thumb.sm img').count(): errs.append('card image thumbnail not shown')
        # ② one amber line, nothing moving
        chg = pg.text_content('#rmx .rmx-chg')
        if not chg.startswith('If instead:') or 'a stone under 5 mm' not in chg: errs.append('round 1 should be the option you picked: ' + chg)
        if ev('__me8.rmx.card.c.beats.map(b => b.opts.join("|"))') != ['|'.join(q['opts'])] * 3: errs.append('rounds must keep the same five options in the same order')
        if pg.locator('#rmx del, #rmx ins, #rmx .rmx-old, #rmx .rmx-new, #rmx .rmx-flipans, #rmx .rmx-film').count(): errs.append('diff or flip markup still on the card')
        if ev("[...document.querySelectorAll('#rmx *')].some(e => getComputedStyle(e).animationName !== 'none')"): errs.append('something on the card is animated')
        if pg.text_content('#rmx [data-rmxflag]').strip() != '🚩': errs.append('flag should be a lone icon')
        pg.keyboard.press('1'); pg.wait_for_timeout(80)
        if pg.locator('#rmx .opts + .kl').count() != 1: errs.append('one why line after answering')
        elif 'a grain of sand' not in pg.text_content('#rmx .opts + .kl'): errs.append('hook not shown after answering')
        elif '🧬 tiny stone → ureter wide enough → passes alone' not in pg.text_content('#rmx .opts + .kl .rmx-how') or not pg.locator('#rmx .opts + .kl .rmx-how b').count(): errs.append('mechanism chain not shown after answering')
        if pg.locator('#rmx .rmx-case .rmx-how').count(): errs.append('① should stay lean: no mechanism lines')
        if 'how' not in call['p'] or '"code"' not in call['p']: errs.append('prompt does not ask for the mechanism')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(80)
        # ③ flag it
        pg.click('#rmx [data-rmxflag]'); pg.wait_for_timeout(100)
        if ev('__me8.rmx.i') != 2 or ev('__me8.rmx.card.res[1]') is not None or not ev('__me8.rmx.card.c.beats[1].flag') or ev('__me8.rmx.card.c.rows[__me8.rmx.card.c.beats[1].ans].if'): errs.append('flag did not drop the variation')
        # ④ timeline, then the end
        a = ev('__me8.rmx.card.c.beats[2].ans'); pg.keyboard.press(str(a + 1)); pg.wait_for_timeout(80); pg.keyboard.press('Enter'); pg.wait_for_timeout(120)
        t = pg.text_content('#rmx')
        if pg.locator('#rmx details:not(.whyc)').count(): errs.append('the lineup should be open, not in a dropdown')
        if pg.locator('#rmx .rmx-lineup .rmx-gr').count() != 5 or pg.locator('#rmx .rmx-lineup .rmx-gr.ok').count() != 1 or pg.locator('#rmx .rmx-lineup .rmx-gr.me').count() != 1: errs.append('lineup should be 5 rows')
        if 'size vs infection' not in pg.text_content('#rmx .rmx-lineup .rmx-code'): errs.append('the A vs B title should head the lineup')
        if not pg.locator('#rmx .rmx-lineup details.whyc').count() or 'Kidney stones' not in pg.text_content('#rmx .rmx-lineup details.whyc summary'): errs.append('matching Pathoma card missing from the lineup')
        elif ev("document.querySelector('#rmx .rmx-lineup details.whyc').open"): errs.append('Pathoma card should start closed')
        if pg.locator('#rmx .rmx-lineup .rmx-how').count() != ev('__me8.rmx.card.c.rows.filter(r => r.how).length') or not pg.locator('#rmx .rmx-lineup .rmx-how').count(): errs.append('lineup should show each row\'s mechanism chain')
        lw = [len(x.split()) for x in ev("[...document.querySelectorAll('#rmx .rmx-lineup .rmx-gr')].map(e => { const c = e.cloneNode(true); c.querySelectorAll('.rmx-how').forEach(x => x.remove()); return c.textContent; })")]
        if max(lw) > 22: errs.append(f'lineup rows too wordy: {lw}')
        if 'back tomorrow' not in t: errs.append('end screen should say back tomorrow')
        if ev('__me8.rmx.card.due') != ev("__me8.rmxAddDays(__me8.rmxDay(), 1)") or ev('__me8.rmx.card.n') != 1: errs.append('first play should be due tomorrow')
        pg.wait_for_timeout(200)
        bg = ev('window.__calls[window.__calls.length - 1]')
        if ev('window.__calls.length') != 2 or not bg['fresh']: errs.append('next round was not made in the background after finishing')
        elif 'a stone under 5 mm' not in bg['p'] or 'ALREADY USED' not in bg['p']: errs.append('background round has no avoid list')
        if not ev('((__me8.rmx.card.next || {}).beats || []).length >= 2'): errs.append('background variations not saved on the card')
        ov('AI card end')
        # image stored outside the Screenshot vault
        cid = ev('__me8.rmx.card.id')
        if not ev('id => __me8.imgGet(id).then(x => !!x)', cid): errs.append('card image not stored')
        if pg.text_content('.qbtn[data-go="vault"] .n').strip() not in ('0', ''): errs.append('remix image leaked into the Screenshot vault count')
        pg.click('#rmx [data-rmxzoom="c"]'); pg.wait_for_timeout(250)
        if pg.locator('#rmxZoom').is_hidden(): errs.append('zoom did not open')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(80)
        if not pg.locator('#rmxZoom').is_hidden(): errs.append('Esc did not close the zoom')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)

        # ---- replay: fresh variations, flagged one gone, avoid list, schedule moves to 3 days ----
        ev("(() => { const c = __me8.rmxAll()[0]; c.due = '2000-01-01'; __me8.save(); })()")
        hashgo('home', 200); hashgo('remix', 300)
        if 'Due today · 1' not in pg.text_content('#rmxVault'): errs.append('Due today count missing')
        n0 = ev('window.__calls.length')
        ev(SET_AI, [AI, FRESH, True, 3000])  # a slow AI must not slow the replay
        pg.click('[data-rmxdue]'); pg.wait_for_timeout(120)
        if ev('__me8.rmx.step') != 'card' or not pg.locator('#rmx .rmx-chg').count(): errs.append('replay did not start instantly')
        if ev('window.__calls.length'): errs.append('replay waited on an AI call')
        if 'a 3 mm stone' not in pg.text_content('#rmx'): errs.append('replay did not use the variations made in the background')
        if ev('!!__me8.rmx.card.next'): errs.append('used variations should be cleared')
        ev(SET_AI, [AI, FRESH, True, 0])
        if ev('__me8.rmx.card.c.beats.some(b => b.flag)'): errs.append('flagged variation came back')
        answer_all(True)
        if ev('__me8.rmx.card.box') != 1 or ev('__me8.rmx.card.due') != ev("__me8.rmxAddDays(__me8.rmxDay(), 3)"): errs.append(f"all right on review should push to 3 days: box={ev('__me8.rmx.card.box')}")
        if 'back in 3 days' not in pg.text_content('#rmx'): errs.append('end screen should say back in 3 days')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        # wrong on review → tomorrow
        ev("(() => { const c = __me8.rmxAll()[0]; c.due = '2000-01-01'; __me8.save(); })()"); hashgo('home', 150); hashgo('remix', 250)
        pg.click('[data-rmxdue]'); pg.wait_for_timeout(150)
        if ev('__me8.rmx.card.c.beats.length') < 2: errs.append('replay with no background round should reuse the old variations')
        answer_all(False)
        if ev('__me8.rmx.card.box') != 0 or ev('__me8.rmx.card.due') != ev("__me8.rmxAddDays(__me8.rmxDay(), 1)"): errs.append('a miss on review should bring it back tomorrow')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        # leaving half-way after a miss: back tomorrow, nothing moves forward
        ev("(() => { const c = __me8.rmxAll()[0]; c.due = '2000-01-01'; c.box = 2; __me8.save(); })()"); hashgo('home', 150); hashgo('remix', 250)
        nplay = ev('__me8.rmxAll()[0].n')
        pg.click('[data-rmxdue]'); pg.wait_for_timeout(400)
        a = ev('__me8.rmx.card.c.beats[0].ans'); pg.keyboard.press(str((a + 1) % 4 + 1)); pg.wait_for_timeout(60)
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        cc = ev('__me8.rmxAll()[0]')
        if cc['n'] != nplay or cc['box'] != 0 or cc['due'] != ev("__me8.rmxAddDays(__me8.rmxDay(), 1)"): errs.append(f"leaving half-way: n {nplay}->{cc['n']} box {cc['box']} due {cc['due']}")

        # ---- careful mode + AI without image support + offline card with a second system ----
        ev(SET_AI, [AI, FRESH, False, 0])
        ev(PASTE_IMG); pg.wait_for_timeout(500)
        if not pg.locator('#rmx .rmx-imgrow img').count(): errs.append('image pasted first should wait for the text')
        ev(PASTE, STONE); pg.wait_for_timeout(200)
        if not pg.locator('#rmx .rmx-thumb img').count(): errs.append('waiting image not attached to the pasted question')
        pg.click('[data-rmxtier]'); pg.wait_for_timeout(80)
        if ev('__me8.rmx.q') is None: errs.append('lost the question after toggling careful mode')
        pg.keyboard.press('Enter'); pg.wait_for_timeout(400)
        lc = ev('window.__calls[window.__calls.length - 1]')
        if lc['tier'] != 'default' or lc['max'] < 8000: errs.append(f"careful mode request: {lc['tier']} {lc['max']}")
        if lc['img']: errs.append('image sent to an AI that cannot take images')
        pg.click('#rmx [data-rmxreset]'); pg.wait_for_timeout(100)
        pg.click('[data-rmxtier]') if pg.locator('[data-rmxtier]').count() else None
        ev("(() => { __me8.setAi(null); })()")
        ev(PASTE, """A 30-year-old woman has a painful red eye with haloes around lights and a fixed mid-dilated pupil. Vision is blurred.
What is the most likely diagnosis?
Acute angle-closure glaucoma
Anterior uveitis
Conjunctivitis
Scleritis
Keratitis
Acute angle-closure glaucoma is correct. Haloes and a fixed mid-dilated pupil are classic."""); pg.wait_for_timeout(150)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(200)
        if ev('__me8.rmx.card.src') != 'local': errs.append('offline card not built')
        pg.keyboard.press('Escape'); pg.wait_for_timeout(100)
        if 'Misses by system' not in pg.text_content('#rmxVault'): errs.append('misses-by-system chips missing')
        else:
            pg.click('#rmxVault [data-rmxsys]'); pg.wait_for_timeout(100)
            if pg.locator('#rmxVault .rmx-item').count() >= ev('__me8.rmxAll().length'): errs.append('system chip did not filter the vault')
            pg.click('#rmxVault [data-rmxsys].on'); pg.wait_for_timeout(100)
        ov('vault')

        # ---- Weak spots panel ----
        ev("(() => { __me8.rmxAll().forEach(c => { c.due = '2000-01-01'; }); __me8.save(); })()")
        hashgo('weak', 400)
        if not pg.locator('#main .rmx-weak').count() or 'From Remix' not in pg.text_content('#main .rmx-weak'): errs.append('Weak spots has no Remix panel')
        elif not pg.locator('#main .rmx-weak [data-u]').count(): errs.append('Weak spots Remix panel has no ILO chips')
        else:
            pg.click('#main [data-rmxduego]'); pg.wait_for_timeout(400)
            if 'remix' not in pg.url or ev('__me8.rmx.step') != 'card' or not ev('!!__me8.rmx.queue'): errs.append('due button in Weak spots did not start the replay')
        ov('weak spots')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px STUDY v0.10 errors: {len(e)}'); [print('  -', x) for x in e]
    e = run(1280, mock=False); bad += len(e)
    print(f'no-runtime STUDY v0.10 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
