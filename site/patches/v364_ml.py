#!/usr/bin/env python3
"""v3.6.4: flag the questions behind the 🎓 Mock-like chip (safe to run again; recomputes every flag).
Mock-like = the b targets (built from your mock's own topics), set E (paper-style), and condition questions whose
lead-in asks for the diagnosis or cause, as 55% of your mock does. Clones are left out unless rebuilt."""
import json, re, pathlib
SITE = pathlib.Path(__file__).resolve().parents[1]
F = SITE / 'study.html'
T = json.loads((SITE.parent / 'study' / 'snap' / 'rw' / 'triage.json').read_text())
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
DX = re.compile(r'most likely (diagnosis|cause|explanation|underlying)|which (term|sign) (best )?describes|which sign is', re.I)
n = 0
for q in D['hq']['q']:
    rebuilt = any(pm[0] is None for _, pm in q.get('pmv', []))
    clone = any(f.startswith('clone') for f in T[q['id']]['f']) and not rebuilt
    ml = (q['t'] == 'b' or q.get('set') == 'E' or (q['t'] == 'u' and DX.search(q.get('ql') or ''))) and not clone
    if ml: q['ml'] = 1; n += 1
    else: q.pop('ml', None)
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print('mock-like questions:', n)
