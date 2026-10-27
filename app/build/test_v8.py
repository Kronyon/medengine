#!/usr/bin/env python3
"""medengine-OSCE v1.4 tests, kept green for v2.0 (stations now open on 🗺️ Poster, so the old checks switch to Script first): v1.3 checks plus red flags for every unit, skeleton cards, test-me pictures, history close.
v1.3 tests (no network): the FFP layout. One station = one task; 7 station types;
FFP checklist links; history stations carry no examination or counselling; AI only on talking stations;
pictures play and step; imaging case pictures hide their labels outside Script; old links still land;
no horizontal overflow at 3 widths; content audit."""
import json, pathlib, re, sys
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / 'out' / 'index.html'
DATA = json.load(open(ROOT / 'build' / 'osce_data_v4.json', encoding='utf-8'))
MOCK = """
window.claude = { use: async (cap) => {
  if (cap === 'sample') { const f = async (turns, o) => { window.__turns = turns; const t = '[Examiner] Please present the film.'; if (o && o.onText) o.onText({text: t}); return {text: t}; };
    f.json = async (p) => { window.__prompt = p; return {global: 4, verdict: 'Solid', domains: [{score: 3, why: 'ok'}], ticked: [], summary: 'Good.', fixes: [{issue: 'x', better: 'y'}]}; }; return f; }
  return null; } };
"""
TYPES = ['hx', 'ex', 'img', 'drug', 'comm', 'proc', 'psych']


def audit():
    errs = []
    for s in DATA['stations']:
        if not s.get('core') or s.get('pp'): continue
        blob = json.dumps({k: s.get(k) for k in ('t', 'info', 'task', 'secs', 'hooks', 'money', 'traps', 'cases', 'vars', 'ask')}, ensure_ascii=False)
        if '—' in blob: errs.append('em dash in ' + s['id'])
        if '(' in blob: errs.append('bracket in ' + s['id'] + ': ' + blob[blob.index('(') - 30: blob.index('(') + 30])
        for w in ('color', 'anemia', 'esophag', 'pediatric', 'hemoglobin', 'behavior', 'center '):
            if w in blob.lower(): errs.append(f'American spelling "{w}" in ' + s['id'])
    for s in DATA['stations']:
        if s['type'] == 'hx' and s.get('pp'):
            bad = [r['s'] for r in s['script'] if r['s'] in ('Examine', 'Interpret', 'Counsel', 'Prescribe', 'Procedure')]
            if bad: errs.append(s['id'] + ' history still has ' + str(set(bad)))
            if any(re.match(r'^(Examination|Management|Prescribing|Procedure)', d['h']) for d in s['dom']): errs.append(s['id'] + ' history still marks exam or management')
    cov = {u for r in DATA['rf'] for u in r['u']}
    miss = [u for u in range(len(DATA['units'])) if u not in cov]
    if miss: errs.append('units with no red-flag sheet: ' + str(miss))
    for r in DATA['rf']:
        for row in r['rows']:
            if len(row) != 4 or row[2] not in DATA['urg']: errs.append('bad red-flag row in ' + r['id'])
    blob = json.dumps([DATA['rf'], DATA['skel'], {k: DATA['frames'][k] for k in ('hx', 'mhx', 'open', 'hxclose', 'pres')}], ensure_ascii=False)
    if '—' in blob: errs.append('em dash in red flags, skeletons or frames')
    if '(' in blob: errs.append('bracket in red flags, skeletons or frames: ' + blob[blob.index('(') - 40: blob.index('(') + 20])
    for w in (r'\bcolors?\b', r'\banemia', r'(?<!o)esophag', r'\bpediatric', r'\bhemoglobin', r'behavior', r'\bcenter\b'):
        if re.search(w, blob, re.I): errs.append(f'American spelling "{w}" in red flags or skeletons')
    for s in DATA['stations']:
        if s.get('skel') not in DATA['skel']: errs.append('no skeleton for ' + s['id'])
        if s['type'] in ('hx', 'psych') and not s.get('rf'): pass
        for h in s.get('hooks') or []:
            if h.startswith('**Why → How → Watch → Check') or h.startswith('**Look → Feel → Move → Special tests'): errs.append('generic hook left in ' + s['id'])
    n_hx = sum(len(sc['items']) for sc in DATA['frames']['hx']['secs'])
    if n_hx > 13: errs.append(f'history skeleton has {n_hx} items; keep it to 13 or fewer')
    n = sum(len(x['items']) for x in DATA['ffp'])
    if n != 63: errs.append(f'FFP checklist has {n} items, expected 63: hand and shoulder are out')
    return errs


def run(width):
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={'width': width, 'height': 900})
        ctx.add_init_script(MOCK)
        ctx.route(re.compile(r'^https?://.*'), lambda r: r.abort())
        pg = ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.goto(PAGE.as_uri()); pg.wait_for_timeout(700)
        ev = pg.evaluate

        def over(label):
            o = ev('document.documentElement.scrollWidth - document.documentElement.clientWidth')
            if o > 1: errs.append(f'{label}: overflow {o}px')

        if not re.search(r'v(1\.4|2\.\d)\.\d', pg.text_content('#homeBtn')) and width > 420: errs.append('version badge not 1.4+')
        if pg.locator('#main .tiles [data-ty]').count() != 7: errs.append('home should show 7 type tiles')
        if pg.locator('#nav [data-ty]').count() != 7: errs.append('nav should have 7 type buttons')
        ids = ev("FFP.flatMap(x => x.items.flatMap(it => it.s))")
        missing = ev("ids => ids.filter(id => !getStation(id))", ids)
        if missing: errs.append('FFP items link to missing stations: ' + str(missing))
        over('home')
        for t in TYPES:
            pg.click(f'#nav [data-ty="{t}"]'); pg.wait_for_timeout(120)
            n = pg.locator('#main [data-st]').count()
            if n < 3 and t != 'img': errs.append(f'type {t} lists only {n}')
            over('type ' + t)
        pg.click('#nav [data-ty="hx"]'); pg.wait_for_timeout(100)
        n0 = pg.locator('#main [data-st]').count(); pg.fill('#tQ', 'asthma'); pg.wait_for_timeout(400)
        n1 = pg.locator('#main [data-st]').count()
        if not 0 < n1 < n0: errs.append(f'history filter did not narrow: {n0} → {n1}')
        pg.fill('#tQ', ''); pg.wait_for_timeout(300)
        # AI only on talking stations
        ev("location.hash = 's-E-cvs'"); pg.wait_for_timeout(300)
        pg.click('[data-mode="script"]'); pg.wait_for_timeout(80)
        if pg.locator('[data-mode="ai"]').count(): errs.append('exam station should not offer AI')
        if not pg.locator('#dgCard .dg').count(): errs.append('exam station has no pictures')
        cap0 = pg.text_content('#dgCard .dg-cap'); pg.click('#dgCard [data-dgn="1"]'); pg.wait_for_timeout(80)
        if pg.text_content('#dgCard .dg-cap') == cap0: errs.append('next step did not change the picture')
        pg.click('#dgCard [data-dgp]'); pg.wait_for_timeout(2600)
        if ev("+document.querySelector('#dgCard .dg').dataset.i") < 2: errs.append('play did not advance the picture')
        pg.click('#dgCard [data-dgp]')
        if pg.locator('#dgCard [data-dgpick]').count() >= 2:
            pg.click('#dgCard [data-dgpick="1"]'); pg.wait_for_timeout(80)
            if 'Murmur' not in pg.text_content('#dgCard .dg-head'): errs.append('picture chips did not switch picture')
        pg.click('[data-mode="script"]'); pg.wait_for_timeout(80)
        if pg.locator('#casesCard').is_hidden() or not pg.locator('#casesCard .case').count(): errs.append('exam cases missing in Script')
        else:
            pg.click('#casesCard .case [data-reveal]'); pg.wait_for_timeout(50)
            if 'Aortic stenosis' not in pg.text_content('#casesCard'): errs.append('case reveal failed')
        txt = pg.text_content('#scriptCard')
        if 'WIPER' not in txt and 'Introduce yourself' not in txt: errs.append('exam script missing the WIPER opening')
        over('station E-cvs')
        ev("location.hash = 's-PP01'"); pg.wait_for_timeout(300)
        if not pg.locator('[data-mode="ai"]').count(): errs.append('history station should offer AI')
        if not pg.locator('#skelCard').count() or 'SOCRATES' not in pg.text_content('#skelCard'): errs.append('history skeleton card missing')
        if not pg.locator('#rfCard .rfr').count(): errs.append('red-flag card missing on a history station')
        if not pg.locator('#dgCard .dg').count(): errs.append('history station has no pictures')
        if ev("cur.secs[cur.secs.length - 1].key") != 'hxclose': errs.append('history checklist should close with hxclose')
        # test me: hide words, tap to reveal, reset on step
        pg.check('[data-dgtest]'); pg.wait_for_timeout(60)
        if not ev("document.body.classList.contains('dg-testing')"): errs.append('test-me did not switch on')
        pg.click('#dgCard .dg-stage'); pg.wait_for_timeout(40)
        if not ev("document.querySelector('#dgCard .dg').classList.contains('dg-rev')"): errs.append('test-me tap did not reveal')
        if pg.locator('#dgCard [data-dgn="1"]').count():
            pg.click('#dgCard [data-dgn="1"]'); pg.wait_for_timeout(40)
            if ev("document.querySelector('#dgCard .dg').classList.contains('dg-rev')"): errs.append('test-me reveal did not reset on the next step')
        pg.uncheck('[data-dgtest]'); pg.wait_for_timeout(40)
        # red-flag browser
        ev("location.hash = 'rf'"); pg.wait_for_timeout(250)
        n0 = pg.locator('#rfList details').count()
        if n0 < 20: errs.append(f'red-flag view lists only {n0} sheets')
        pg.fill('#rfQ', 'testis'); pg.wait_for_timeout(400)
        n1 = pg.locator('#rfList details').count()
        if not 0 < n1 < n0: errs.append(f'red-flag filter did not narrow: {n0} → {n1}')
        pg.fill('#rfQ', ''); pg.wait_for_timeout(300)
        over('red flags')
        ev("location.hash = 's-E-ul'"); pg.wait_for_timeout(300)
        if 'SWIFT' not in pg.text_content('#skelCard'): errs.append('neuro skeleton should carry SWIFT')
        ev("location.hash = 's-PP01'"); pg.wait_for_timeout(300)
        if 'present to the examiner' not in pg.text_content('#briefP + .task').lower(): errs.append('history door does not ask to present')
        # AI flow and marking
        pg.click('[data-mode="ai"]'); pg.wait_for_timeout(80)
        pg.fill('#say', 'Hello, what brought you in?'); pg.click('[data-send]'); pg.wait_for_timeout(300)
        pg.fill('#say', 'When did it start?'); pg.click('[data-send]'); pg.wait_for_timeout(300)
        pg.click('[data-grade]'); pg.wait_for_timeout(800)
        if 'Domain scores' not in pg.text_content('#aiOut'): errs.append('AI marking did not render domain scores')
        pg.click('[data-mode="script"]'); pg.wait_for_timeout(80)
        # imaging: examiner viva, picture, labels hidden outside Script
        ev("location.hash = 's-I-cxr'"); pg.wait_for_timeout(300)
        if not pg.locator('#caseImg svg').count(): errs.append('imaging case picture missing')
        pg.click('[data-mode="tick"]'); pg.wait_for_timeout(80)
        if ev("document.getElementById('caseImg').classList.contains('lab')"): errs.append('answer labels visible in Tick mode')
        pg.click('[data-mode="ai"]'); pg.wait_for_timeout(80)
        pg.fill('#say', 'This is a PA chest X-ray'); pg.click('[data-send]'); pg.wait_for_timeout(300)
        if 'EXAMINER' not in json.dumps(ev('window.__turns || []')): errs.append('imaging AI is not playing the examiner')
        pg.click('[data-mode="script"]'); pg.wait_for_timeout(80)
        over('station I-cxr')
        ev("location.hash = 's-D-htn'"); pg.wait_for_timeout(300)
        if pg.locator('#varSel option').count() < 3: errs.append('drug station should have cases')
        over('station D-htn')
        # old links still land
        ev("location.hash = 'e-cvs'"); pg.wait_for_timeout(250)
        if not ev("route.v === 'station' && route.id === 'E-cvs'"): errs.append('old #e-cvs link did not open the new exam')
        ev("location.hash = 'p-ecg12'"); pg.wait_for_timeout(250)
        if not ev("route.v === 'station' && route.id === 'P-ecg12'"): errs.append('old #p-ecg12 link did not open the new procedure')
        ev("location.hash = 'u12'"); pg.wait_for_timeout(250)
        if not ev("route.v === 'ilo'"): errs.append('ILO link broken')
        # every core station opens in every mode without errors
        if width == 1280:
            for sid in ev("ST.filter(s => s.core || s.pp).map(s => s.id)"):
                ev(f"location.hash = 's-{sid}'"); pg.wait_for_timeout(25)
                for md in ev("[...document.querySelectorAll('#modeSeg [data-mode]')].map(b => b.dataset.mode).filter(m => m !== 'voice')"):
                    pg.click(f'[data-mode="{md}"]')
            bad = ev("""() => { const out = []; DG.list().forEach(id => { const w = document.createElement('div'); w.innerHTML = DG.html(id); document.body.appendChild(w); const f = w.firstChild; for (let i = 0; i < DG.n(id); i++) { DG.show(f, i); if (/unavailable/.test(f.innerHTML) || f.querySelector('.dg-stage').innerHTML.length < 40) out.push(id + ':' + i); } w.remove(); }); return out; }""")
            if bad: errs.append('pictures failing: ' + str(bad[:8]))
            need = ev("[...new Set(ST.flatMap(s => s.dg || []))].filter(id => !DG.has(id))")
            if need: errs.append('stations reference missing pictures: ' + str(need))
        b.close()
    return errs


if __name__ == '__main__':
    a = audit(); bad = len(a)
    print('content audit errors:', bad); [print('  -', x) for x in a[:20]]
    for w in (1280, 820, 390):
        e = run(w); bad += len(e)
        print(f'{w}px OSCE v1.4 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
