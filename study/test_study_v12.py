#!/usr/bin/env python3
"""medengine v1.2 tests (no network): ⚡ First move vs cure (section, rules, condition strip, Remix grounding) and
🔥 My misses (import from a file, masked cue, old pick vs right answer, never-re-done first, spaced until fixed,
keyboard, no overflow). The fixture is written in our own words, not anyone's real question history."""
import json, pathlib, re, sys, tempfile
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
FIX = {'app': 'medengine', 'kind': 'misses', 'items': [
    {'id': 'Q900', 'spec': 'Cardiology', 'tags': 'Tachyarrhythmias', 'correct': 'Synchronised cardioversion', 'mine': 'Adenosine', 'lp': 'Tachycardia with shock: synchronised cardioversion straight away.', 'rec': True},
    {'id': 'Q12', 'spec': 'Emergency Medicine', 'tags': 'Pneumothorax', 'correct': 'Needle decompression', 'mine': 'Chest drain', 'lp': 'Tension pneumothorax: needle decompression before any imaging.', 'rec': False},
    {'id': 'Q40', 'spec': 'Endocrinology', 'tags': 'Diabetic ketoacidosis (DKA)', 'correct': '1 L saline over an hour', 'mine': 'IV insulin infusion', 'lp': 'DKA starts with fluids, then insulin.', 'rec': True},
    {'id': 'Q41', 'spec': 'ENT', 'tags': 'Hearing loss', 'correct': 'Otosclerosis', 'mine': '', 'lp': 'blank pick, should be skipped', 'rec': False}]}


def run(width, mock=True):
    errs = []
    fx = pathlib.Path(tempfile.mkdtemp()) / 'misses.json'; fx.write_text(json.dumps(FIX), encoding='utf-8')
    with sync_playwright() as p:
        b = p.chromium.launch(); ctx = b.new_context(viewport={'width': width, 'height': 900})
        if mock: ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page(); pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(1500); ev = pg.evaluate
        def ov(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')
        if not re.search(r'v(1\.([2-9]|\d\d)|2\.\d)', pg.text_content('#homeBtn')): errs.append('version not v1.2+')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        A = D.get('act', [])
        if len(A) < 45: errs.append(f'only {len(A)} action cards')
        cov = {u for r in A for u in r['u']}
        miss = [u['name'] for i, u in enumerate(D['units']) if i not in cov]
        if miss: errs.append(f'ILO conditions with no ⚡ card: {miss[:5]}')
        if len(A) > 120: errs.append(f'{len(A)} action cards is getting bloated')
        for r in A:
            for l in r['l']:
                if '→' not in l: errs.append(f"{r['id']}: a line with no arrow")
                if re.search(r'[()\[\]—]', l): errs.append(f"{r['id']}: brackets or em dash")
                if l.count('**') % 2: errs.append(f"{r['id']}: unbalanced bold")
            for u in r['u']:
                if A.index(r) not in D['units'][u].get('acts', []): errs.append(f"{r['id']} not linked to unit {u}")
        if not any(r['id'] == 'nerves' for r in D['path']): errs.append('nerve injuries Why card missing')
        # the section
        if not pg.locator('#main [data-go="act"]').count(): errs.append('no way into First move vs cure from home')
        ev("location.hash = 'act'"); pg.wait_for_timeout(400)
        if pg.locator('#whyList details.pa').count() != len(A): errs.append('section does not show every action card')
        if 'last line first' not in pg.text_content('#main .ph'): errs.append('reading cue missing')
        pg.fill('#whyQ', 'cardioversion'); pg.wait_for_timeout(150)
        if not 1 <= pg.locator('#whyList details.pa:not([hidden])').count() <= 6: errs.append('search did not narrow the cards')
        pg.fill('#whyQ', ''); pg.click('[data-whyall]'); pg.wait_for_timeout(150)
        if pg.locator('#whyList details.pa[open] .pa-ar').count() < 100: errs.append('arrows not coloured in action cards')
        ov('action section')
        # the condition strip
        ev("location.hash = 'u3-think'"); pg.wait_for_timeout(400)
        if not pg.locator('#main .act-p details.act').count(): errs.append('no ⚡ strip on the arrhythmia condition')
        # Remix prompt carries the checked next-step card
        q = {'stem': 'A 60-year-old man has palpitations, BP 78/40 and a regular narrow complex tachycardia at 190.', 'opts': ['IV adenosine', 'Synchronised DC cardioversion', 'Bisoprolol', 'Carotid sinus massage', 'IV amiodarone'], 'correct': 1, 'picked': 0, 'cond': [], 'concept': '', 'expl': '', 'optx': []}
        note = ev('q => __me12.rootNote(q)', q)
        if 'CHECKED NEXT-STEP NOTES' not in note or 'Fast heart' not in note: errs.append('Remix prompt not grounded with the action card')
        # 🔥 My misses
        ev("location.hash = 'misses'"); pg.wait_for_timeout(300)
        if 'No misses loaded yet' not in pg.text_content('#ms'): errs.append('empty state missing')
        pg.set_input_files('[data-msfile]', str(fx)); pg.wait_for_timeout(500)
        if ev('__me12.msLoad().items.length') != 3: errs.append('import should keep the 3 items with an old pick')
        if ev('__me12.cur && __me12.cur.id') != 'Q12': errs.append('never re-done misses should come first')
        cue = pg.text_content('#ms .ms-cue')
        if 'Needle decompression' in cue or 'needle' in cue.lower() or '▒▒▒' not in cue: errs.append('cue should hide the right answer: ' + cue)
        opts = [x.strip() for x in pg.locator('#ms .opts .opt span:last-child').all_text_contents()]
        if sorted(opts) != ['Chest drain', 'Needle decompression']: errs.append(f'options: {opts}')
        right = opts.index('Needle decompression') + 1
        pg.keyboard.press(str(right)); pg.wait_for_timeout(150)
        if not pg.locator('#ms .opt.right').count() or 'before any imaging' not in pg.text_content('#ms .kl'): errs.append('answer not revealed with the rule')
        it = ev("__me12.msLoad().items.find(x => x.id === 'Q12')")
        if it['box'] != 1 or it['fixed']: errs.append(f"first right answer: box {it['box']} fixed {it['fixed']}")
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        nxt = ev('__me12.cur && __me12.cur.id')
        if nxt == 'Q12': errs.append('a just-answered card came straight back')
        # wrong answer → tomorrow, box 0
        o2 = [x.strip() for x in pg.locator('#ms .opts .opt span:last-child').all_text_contents()]
        it2 = ev('__me12.cur'); wrong = o2.index(it2['mine']) + 1
        pg.keyboard.press(str(wrong)); pg.wait_for_timeout(150)
        it2 = ev(f"__me12.msLoad().items.find(x => x.id === '{it2['id']}')")
        if it2['box'] != 0 or it2['due'] != ev("__me8.rmxAddDays(__me8.rmxDay(), 1)"): errs.append('a wrong answer should come back tomorrow')
        # second right answer on another day → fixed
        ev("(() => { const x = __me12.msLoad().items.find(x => x.id === 'Q12'); x.due = '2000-01-01'; x.last = '2000-01-01'; localStorage.setItem('medengine-misses-v1', JSON.stringify(__me12.msLoad())); })()")
        pg.keyboard.press('Enter'); pg.wait_for_timeout(150)
        ev("location.hash = 'home'"); pg.wait_for_timeout(200); ev("location.hash = 'misses'"); pg.wait_for_timeout(300)
        if ev('__me12.cur && __me12.cur.id') == 'Q12':
            o3 = [x.strip() for x in pg.locator('#ms .opts .opt span:last-child').all_text_contents()]
            pg.keyboard.press(str(o3.index('Needle decompression') + 1)); pg.wait_for_timeout(150)
            if not ev("__me12.msLoad().items.find(x => x.id === 'Q12').fixed"): errs.append('right on two separate days should fix it')
        else: errs.append('a due card did not come back')
        ov('misses')
        b.close()
    return errs


if __name__ == '__main__':
    bad = 0
    for w in (1280, 820, 390):
        e = run(w); bad += len(e); print(f'{w}px STUDY v1.2 errors: {len(e)}'); [print('  -', x) for x in e[:12]]
    e = run(1280, mock=False); bad += len(e); print(f'no-runtime STUDY v1.2 errors: {len(e)}'); [print('  -', x) for x in e[:12]]
    sys.exit(1 if bad else 0)
