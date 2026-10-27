#!/usr/bin/env python3
"""medengine v1.0 tests (no network): the new mechanism cards are in the Pathoma library, linked to their ILO
conditions and shown on the condition page; Remix picks the card that names the most options, shows it in the
lineup and puts it in the AI prompt as checked notes; nothing overflows at 3 widths."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).resolve().parent
PAGE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE / 'index.html').resolve()
MOCK = "window.claude={use:async c=>c==='user'?{id:async()=>'u1'}:c==='db'?{doc:()=>({get:async()=>({exists:false}),set:async()=>{}})}:null};"
V10 = json.load(open(HERE / 'v10_content.json', encoding='utf-8'))['path_add']
GALL = {'stem': 'A 70-year-old woman has RUQ pain, fever of 39°C and jaundice. She is hypotensive.', 'opts': ['Biliary colic', 'Acute cholecystitis', 'Ascending cholangitis', 'Acute pancreatitis', 'Hepatitis A'], 'correct': 2, 'picked': 1, 'cond': [], 'concept': '', 'expl': '', 'optx': []}


def audit():
    errs = []
    for r in V10:
        if '—' in json.dumps(r, ensure_ascii=False): errs.append('em dash in ' + r['id'])
        if not 2 <= len(r['l']) <= 4: errs.append(f"{r['id']}: {len(r['l'])} lines")
        for l in r['l']:
            if len(l.split()) > 75: errs.append(f"{r['id']}: line too long ({len(l.split())} words)")
            if '**' not in l: errs.append(f"{r['id']}: a line has no bold key words")
            if l.count('**') % 2: errs.append(f"{r['id']}: unbalanced bold")
            if '(' in l or '[' in l: errs.append(f"{r['id']}: brackets hide key words")
    return errs


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
        if not re.search(r'v1\.[1-9]\.\d|v1\.0\.0|v2\.\d+\.\d', pg.text_content('#homeBtn')): errs.append('version not v1.x')
        D = ev("JSON.parse(document.getElementById('qqdata').textContent)")
        ids = [r['id'] for r in D['path']]
        if len(ids) != len(set(ids)): errs.append('duplicate Pathoma ids')
        for r in V10:
            if r['id'] not in ids: errs.append('missing card ' + r['id']); continue
            i = ids.index(r['id'])
            for u in r['u']:
                if i not in D['units'][u].get('pa', []): errs.append(f"{r['id']} not linked to unit {u}")
        # condition page shows the new card (bowel obstruction)
        ev("location.hash = 'u48-think'"); pg.wait_for_timeout(500)
        t = pg.text_content('#main')
        if 'Bowel obstruction: small vs large' not in t: errs.append('condition page does not show the new card')
        else:
            pg.click('#main details.pa summary:has-text("Bowel obstruction")'); pg.wait_for_timeout(100)
            if pg.locator('#main details.pa[open] b').count() < 3: errs.append('card opens without bold key words')
        o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        if o > 1: errs.append(f'condition page overflow {o}px')
        # Remix picks the card that names the most options, and grounds the AI with it
        if ev('q => __me8.rootPick(q, -1)', GALL) != 'gsladder': errs.append('gallstone question should pick the gallstone ladder: ' + str(ev('q => __me8.rootPick(q, -1)', GALL)))
        calls = []
        ev("""() => { window.__p = []; __me8.setAi(Object.assign(async () => ({text: ''}), {json: async (p) => { window.__p.push(p); return {film: 'x', clue: '', code: 'a vs b', rows: [{if: 'pain settles in hours', hook: 'h', how: 'w'}, {if: 'over 6 hours with fever', hook: 'h', how: 'w'}, {if: 'fever, jaundice, low BP', hook: 'h', how: 'w'}, {if: 'pain to the back, high amylase', hook: 'h', how: 'w'}, {if: '', hook: 'h', how: ''}]}; }, limits: async () => ({maxPromptBytes: 262144})})); }""")
        ev("location.hash = 'remix'"); pg.wait_for_timeout(300)
        ev("""(t) => { const dt = new DataTransfer(); dt.setData('text/plain', t); document.body.dispatchEvent(new ClipboardEvent('paste', {clipboardData: dt, bubbles: true, cancelable: true})); }""",
           GALL['stem'] + '\nWhat is the most likely diagnosis?\n' + '\n'.join(GALL['opts']) + '\nAscending cholangitis is correct. Charcot triad.')
        pg.wait_for_timeout(200); pg.click('[data-rmxp="1"]'); pg.wait_for_timeout(50)
        pg.keyboard.press('Enter'); pg.wait_for_timeout(400)
        pp = ev('window.__p[0] || ""')
        if 'CHECKED MECHANISM NOTES' not in pp or 'gallstone ladder' not in pp.lower(): errs.append('AI prompt not grounded with the checked card')
        if '**' in pp.split('CHECKED MECHANISM NOTES')[-1].split('Reply with ONLY')[0]: errs.append('bold markers leaked into the checked notes')
        for _ in range(4):
            if ev('__me8.rmx.i >= __me8.rmx.card.c.beats.length'): break
            a = ev('__me8.rmx.card.c.beats[__me8.rmx.i].ans'); pg.keyboard.press(str(a + 1)); pg.wait_for_timeout(50); pg.keyboard.press('Enter'); pg.wait_for_timeout(60)
        if not pg.locator('#rmx .rmx-lineup details.whyc').count() or 'gallstone ladder' not in pg.text_content('#rmx .rmx-lineup details.whyc summary').lower(): errs.append('lineup does not show the gallstone ladder')
        o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
        if o > 1: errs.append(f'remix overflow {o}px')
        b.close()
    return errs


if __name__ == '__main__':
    bad = len(audit()); print('content audit errors:', bad); [print('  -', x) for x in audit()]
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px STUDY v1.0 errors: {len(e)}'); [print('  -', x) for x in e]
    e = run(1280, mock=False); bad += len(e)
    print(f'no-runtime STUDY v1.0 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
