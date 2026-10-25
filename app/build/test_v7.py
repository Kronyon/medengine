#!/usr/bin/env python3
"""medengine-OSCE v1.3 tests (no network): the FFP layout. One station = one task; 7 station types;
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
    n = sum(len(x['items']) for x in DATA['ffp'])
    if n != 65: errs.append(f'FFP checklist has {n} items, expected 65')
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

        if 'v1.3.0' not in pg.text_content('#homeBtn') and width > 420: errs.append('version badge not 1.3.0')
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
        print(f'{w}px OSCE v1.3 errors: {len(e)}'); [print('  -', x) for x in e]
    sys.exit(1 if bad else 0)
