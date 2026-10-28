#!/usr/bin/env python3
"""medengine-OSCE v2.0 tests (no network): 🗺️ posters.
Content: every ILO unit has a condition poster and every condition a lookalike on one shared axis; the 24 FFP examinations
have a route and the 15 procedures a storyboard; 14 master posters, and the 5 that rebuild the AI-made infographics list
their fixes; no em dashes, brackets or American spellings; the hand and shoulder examinations are gone.
Browser: 🗺️ Poster is the first mode; every station renders a poster with nothing undefined or empty; 🔒 Lock, N and
▶ Walk; ⚡ Last 2 min and the 8:00 collapse; ILO pages open on their poster; the hub and every master poster with its
figure; search finds posters; ⌘F / Ctrl+F jumps to search; no page overflow at 3 widths; dark mode recolours the badges."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'out' / 'index.html'
DATA = json.load(open(ROOT / 'build' / 'osce_data_v4.json', encoding='utf-8'))
US = re.compile(r'\bcolors?\b|\banemi|(?<!o)esophag|\bpediatric|\bhemoglobin|\bbehavior|\bcenter\b|\bfavor|\bleukocyte|\bgynecol|\bdiarrhea|\bedema\b|\bhematol', re.I)
FIXED = {'spiro', 'ms', 'uveitis', 'throat', 'ct'}


def flat(x):
    return ' '.join(flat(y) for y in x) if isinstance(x, list) else ' '.join(flat(v) for v in x.values()) if isinstance(x, dict) else str(x)


def audit():
    errs = []
    U, SN, M, PO = DATA['units'], DATA['snap'], DATA['master'], DATA['po']
    if sorted(map(int, SN)) != list(range(len(U))): errs.append('every ILO unit needs a condition poster')
    for k, s in SN.items():
        b = flat(s)
        if re.search(r'[()\[\]—]', b): errs.append(f'poster {k}: bracket or em dash')
        if US.search(b): errs.append(f'poster {k}: American spelling "{US.search(b).group(0)}"')
        if s.get('k') != 't':
            v = s.get('v')
            if not v or not 4 <= len(v) <= 5: errs.append(f'poster {k} {s["n"]}: no lookalike')
            elif v[2] == v[3] or not v[1]: errs.append(f'poster {k}: lookalike has no shared axis or two equal sides')
        if not any(len(x) > 2 for x in s['x']): errs.append(f'poster {k}: no ★ test')
        if '→' not in s['m']: errs.append(f'poster {k}: the mechanism has no arrows')
    ids = [m['id'] for m in M]
    if len(M) != 14 or len(set(ids)) != 14: errs.append(f'expected 14 distinct master posters, got {len(M)}')
    for m in M:
        b = flat({k: v for k, v in m.items() if k not in ('id', 'fig', 'sys', 'ic')})
        if re.search(r'[()—]', b): errs.append(f'master {m["id"]}: bracket or em dash')
        if US.search(b): errs.append(f'master {m["id"]}: American spelling "{US.search(b).group(0)}"')
        if not m.get('src'): errs.append(f'master {m["id"]}: no source')
        if not m.get('hook'): errs.append(f'master {m["id"]}: no hook')
        if any(not 0 <= u < len(U) for u in m.get('u', [])): errs.append(f'master {m["id"]}: bad unit link')
        if m['id'] in FIXED and len(m.get('fix', [])) < 3: errs.append(f'master {m["id"]}: list what the AI version got wrong')
        if 'mx' in m and any(len(r) != len(m['mx']['head']) for r in m['mx']['rows']): errs.append(f'master {m["id"]}: ragged matrix')
    ex = sorted(s['id'] for s in DATA['stations'] if s['type'] == 'ex')
    pr = sorted(s['id'] for s in DATA['stations'] if s['type'] == 'proc')
    if sorted(PO['routes']) != ex or len(ex) != 24: errs.append(f'routes {len(PO["routes"])} vs exams {len(ex)}')
    if sorted(PO['story']) != pr or len(pr) != 15: errs.append(f'stories {len(PO["story"])} vs procedures {len(pr)}')
    for k, r in PO['routes'].items():
        if not 3 <= len(r['pins']) <= 9: errs.append(f'route {k}: {len(r["pins"])} pins')
        if not r['props'] or not r['done']: errs.append(f'route {k}: no props or no completion')
        if not all('→' in h for h in r['hunt']) or not 3 <= len(r['hunt']) <= 5: errs.append(f'route {k}: hunt lines need clue → answer')
    for k, s in PO['story'].items():
        if len(s['fail']) != 3 or not s['nums']: errs.append(f'story {k}: 3 fail lines and some numbers')
    b = flat(PO)
    if re.search(r'[()—]', b): errs.append('station posters: bracket or em dash')
    if US.search(b): errs.append(f'station posters: American spelling "{US.search(b).group(0)}"')
    if any(s['id'] in ('E-hand', 'E-shoulder') for s in DATA['stations']): errs.append('hand or shoulder examination still present')
    if any(e['id'] in ('hand', 'shoulder') for e in DATA['exams']): errs.append('hand or shoulder exam guide still present')
    names = [it['n'] for sec in DATA['ffp'] for it in sec['items']]
    if len(names) != 63 or any('MSK Hand' in n or 'Shoulder' in n for n in names): errs.append(f'FFP list should be 63 items without hand or shoulder: {len(names)}')
    return errs


def run(width):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(700)
        ev = pg.evaluate

        def over(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')

        def go(h, t=250):
            ev(f"location.hash = '{h}'"); pg.wait_for_timeout(t)

        if width > 420 and not re.search(r'v2\.[0-9]\.[0-9]', pg.text_content('#homeBtn')): errs.append('version badge not 2.x')
        if not pg.locator('#nav [data-v="posters"]').count(): errs.append('nav has no Posters button')
        if ev("MODES[0][0]") != 'poster': errs.append('Poster should be the first mode')
        # every station, every kind
        if width == 1280:
            bad = ev("""async () => { const out = []; for (const s of ST) { location.hash = 's-' + s.id; await new Promise(r => setTimeout(r, 12)); const po = document.querySelector('#posterCard .po');
              if (!po) { out.push(s.id + ' none'); continue; } const t = po.textContent; if (/undefined|NaN|\\[object/.test(t)) out.push(s.id + ' undefined');
              if ([...po.querySelectorAll('.po-items li')].some(li => li.textContent.trim() === '…')) out.push(s.id + ' empty corner');
              const want = typeOf(s) === 'ex' ? 'po-route' : typeOf(s) === 'proc' ? 'po-story' : 'po-corners'; if (!po.classList.contains(want)) out.push(s.id + ' not ' + want); } return out; }""")
            if bad: errs.append('station posters: ' + str(bad[:8]))
        # a history station: the 10-minute clock
        go('s-PP01', 350)
        if not pg.locator('#modeSeg [data-mode="poster"].on').count(): errs.append('station did not open on Poster')
        if pg.locator('#posterCard .po-corners .po-4 > .po-z').count() != 4: errs.append('history poster should have 4 corners')
        if pg.locator('#posterCard .po-clock span').count() != 4: errs.append('history poster has no 4-part clock')
        if not pg.locator('#scriptCard').is_hidden(): errs.append('script shows in Poster mode')
        pg.click('#posterCard [data-polock]'); pg.wait_for_timeout(60)
        n0 = pg.locator('#posterCard .pz.rv').count(); pg.keyboard.press('n'); pg.wait_for_timeout(40)
        if pg.locator('#posterCard .pz.rv').count() != n0 + 1: errs.append('N did not reveal a pill')
        pg.locator('#posterCard .pz:not(.rv)').first.click(); pg.wait_for_timeout(40)
        if pg.locator('#posterCard .pz.rv').count() != n0 + 2: errs.append('tap did not reveal a pill')
        pg.keyboard.press('l'); pg.wait_for_timeout(40)
        if pg.locator('#posterCard .po.lock').count(): errs.append('L did not unlock')
        pg.click('#posterCard [data-poplay]'); pg.wait_for_timeout(250)
        if pg.locator('#posterCard .po.walking [data-ord].on').count() != 1: errs.append('Walk it did not spotlight one zone')
        pg.click('#posterCard [data-poplay]')
        pg.click('#posterCard [data-posprint]'); pg.wait_for_timeout(60)
        if not pg.locator('#posterCard .po.sprint').count() or pg.locator('#posterCard .q-tl').is_visible(): errs.append('Last 2 min did not collapse to the plan')
        pg.click('#posterCard [data-posprint]'); pg.wait_for_timeout(40)
        ev("cur.left = 121"); pg.click('[data-timer]'); pg.wait_for_timeout(1300); pg.click('[data-timer]')
        if not pg.locator('#posterCard .po.sprint').count(): errs.append('8:00 did not collapse the poster to the plan')
        over('history poster')
        # an exam route and a procedure storyboard
        go('s-E-cvs', 300)
        if pg.locator('#posterCard .po-pins li').count() != len(DATA['po']['routes']['E-cvs']['pins']): errs.append('CVS route pins do not match the data')
        if pg.locator('#posterCard .po-route .po-pin').count() != pg.locator('#posterCard .po-pins li').count(): errs.append('CVS map pins do not match the list')
        over('exam route')
        go('s-E-fundo', 300)
        if not pg.locator('#posterCard .po-head').count(): errs.append('fundoscopy should walk round a head')
        go('s-P-dip', 300)
        if pg.locator('#posterCard .po-frame').count() != 3 or pg.locator('#posterCard .po-fail').count() != 3: errs.append('urine dip storyboard needs 3 frames and 3 fail lines')
        if 'early-morning ACR' not in pg.text_content('#posterCard'): errs.append('urine dip storyboard lost the proteinuria plan')
        over('procedure story')
        go('s-P-ecg3', 300)
        if any(pg.locator(f'#posterCard .po-frame >> nth={i}').locator('li').count() == 0 for i in range(3)): errs.append('3-lead ECG storyboard has an empty frame')
        # a drug station: the plan fork follows the chosen case
        go('s-D-htn', 300)
        pg.select_option('#varSel', 'B'); pg.wait_for_timeout(200)
        t = pg.text_content('#posterCard .q-br')
        if t.find('Case B') < 0 or t.find('Case B') > t.find('Case A'): errs.append('the chosen case should lead the plan corner')
        # ILO page, hub, masters
        go('u158', 250)
        if not pg.locator('#main .po-cond').count(): errs.append('ILO page did not open on its poster')
        go('posters', 300)
        if pg.locator('#main .tile[data-mp]').count() != 14: errs.append('hub should show 14 master posters')
        if pg.locator('#main [data-stpo^="E-"]').count() != 24 or pg.locator('#main [data-stpo^="P-"]').count() != 15: errs.append('hub should list 24 routes and 15 storyboards')
        n0 = pg.locator('#poWall .chip').count(); pg.fill('#poQ', 'eye'); pg.wait_for_timeout(400)
        n1 = pg.locator('#poWall .chip').count()
        if not 0 < n1 < n0: errs.append(f'condition wall filter did not narrow: {n0} → {n1}')
        pg.fill('#poQ', ''); pg.wait_for_timeout(250)
        over('posters hub')
        for m in DATA['master']:
            go('mp-' + m['id'], 120)
            if not pg.locator('#main .po-split').count(): errs.append(f'master {m["id"]} did not render'); continue
            if m.get('fig') and not pg.locator('#main .po-fig svg').count(): errs.append(f'master {m["id"]}: figure missing')
            if re.search(r'undefined|NaN', pg.text_content('#main .po-split')): errs.append(f'master {m["id"]}: undefined text')
            if width == 1280 and m.get('fig'):
                wide = ev("""() => { const s = document.querySelector('#main .po-fig svg'); const vb = s.viewBox.baseVal; return [...s.querySelectorAll('text')].filter(t => { const b = t.getBBox(); return b.x < -1 || b.x + b.width > vb.width + 1; }).map(t => t.textContent).slice(0, 3); }""")
                if wide: errs.append(f'master {m["id"]}: figure text spills out: {wide}')
            over('master ' + m['id'])
        # search and ⌘F / Ctrl+F
        go('home', 200)
        pg.keyboard.press('Control+f'); pg.wait_for_timeout(80)
        if not ev("document.activeElement && document.activeElement.id === 'q'"): errs.append('Ctrl+F did not focus the search bar')
        pg.keyboard.type('spirometry'); pg.wait_for_timeout(450)
        if not pg.locator('#main [data-mp="spiro"]').count(): errs.append('search did not find the spirometry poster')
        b.close()
    return errs


def dark():
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1280, 'height': 900}, color_scheme='dark')
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri() + '#s-PP01'); pg.wait_for_timeout(500)
        on = pg.evaluate("getComputedStyle(document.querySelector('#posterCard .po')).getPropertyValue('--po-on').trim()")
        if on != '#0d1416': errs.append('dark mode: badge text colour not switched: ' + on)
        b.close()
    return errs


if __name__ == '__main__':
    a = audit(); bad = len(a)
    print('content audit errors:', bad); [print('  -', x) for x in a[:30]]
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px OSCE v2.0 errors: {len(e)}'); [print('  -', x) for x in e]
    e = dark(); bad += len(e); print('dark mode errors:', len(e)); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
