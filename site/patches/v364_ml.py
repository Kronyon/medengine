#!/usr/bin/env python3
"""v3.6.4: flag the questions behind the 🎓 Mock-like chip (safe to run again; recomputes every flag).
Mock-like = the b targets (built from your mock's own topics), set E (paper-style), and condition questions whose
lead-in asks for the diagnosis or cause, as 55% of your mock does. Clones are left out unless rebuilt."""
import json, re, pathlib, collections
SITE = pathlib.Path(__file__).resolve().parents[1]
F = SITE / 'study.html'
T = json.loads((SITE.parent / 'study' / 'snap' / 'rw' / 'triage.json').read_text())
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
DX = re.compile(r'most likely (diagnosis|cause|explanation|underlying)|which (term|sign) (best )?describes|which sign is', re.I)
n = 0
pool = []
for q in D['hq']['q']:
    rebuilt = any(pm[0] is None for _, pm in q.get('pmv', []))
    fl = T[q['id']]['f']
    clone = any(f.startswith('clone') for f in fl) and not rebuilt
    ml = (q['t'] == 'b' or q.get('set') == 'E' or (q['t'] == 'u' and DX.search(q.get('ql') or ''))) and not clone
    if ml: q['ml'] = 1; n += 1
    else:
        q.pop('ml', None)
        # v3.6.9: management and investigation questions join so the chip matches the mock's lead-in mix
        # (mock: 53% diagnosis, 47% management, investigation and other; the chip was 84% diagnosis).
        if q['t'] in ('u', 'b') and not clone and not any(f.split(':')[0] in ('len', 'frame', 'neg', 'abs', 'clone') for f in fl):
            pool.append(q)
ndx = sum(1 for q in D['hq']['q'] if q.get('ml') and DX.search(q.get('ql') or ''))
want = round(ndx * 47 / 53) - (n - ndx)
pool.sort(key=lambda q: (not q.get('rw'), q['id']))   # questions already reviewed in a rewrite batch first
for q in pool[:max(0, want)]: q['ml'] = 1; n += 1
# v3.6.9: week weights so a shuffled Mock-like run follows the mock (q.mw = mock share / chip share for that week)
U = D['units']
wk = lambda q: U[int(q['k'])]['w'] if q['t'] == 'u' else 'b'
mockw = collections.Counter(U[q['u']]['w'] for q in D['mock']['q'] if isinstance(q.get('u'), int))
mlq = [q for q in D['hq']['q'] if q.get('ml')]
chipw = collections.Counter(wk(q) for q in mlq)
tot_m = sum(mockw.values()); tot_c = len(mlq); bshare = chipw['b'] / tot_c
for q in D['hq']['q']: q.pop('mw', None)
for q in mlq:
    w = wk(q)
    if w == 'b': continue
    share = mockw.get(w, 0.5) / tot_m * (1 - bshare)
    q['mw'] = round(max(0.2, share / (chipw[w] / tot_c)), 3)
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print('mock-like questions:', n)
