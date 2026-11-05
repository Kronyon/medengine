#!/usr/bin/env python3
"""v3.6.3: add the hand-written "why not" lines in study/snap/wn_hand.py to STUDY (safe to run again).
A line is only added where that option has none, so nothing already written is overwritten."""
import json, pathlib, re, sys
SITE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SITE.parent / 'study' / 'snap'))
from wn_hand import H  # noqa: E402
F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
L = 'ABCDE'; n = 0; seen = set()
for src in ('hq', 'mock', 'off'):
    for q in D[src]['q']:
        if q['id'] not in H:
            continue
        seen.add(q['id'])
        tm = q.setdefault('tm', {'c': [], 'm': '', 'g': '', 'f': [], 'x': []})
        have = {i for i, _ in tm.get('x', [])}
        for let, line in H[q['id']].items():
            i = L.index(let)
            assert i != q['a'], (q['id'], let, 'is the answer')
            if i not in have:
                tm.setdefault('x', []).append([i, line]); n += 1
        tm['x'].sort()
missing = sorted(set(H) - seen)
assert not missing, missing
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print('hand-written why-not lines added:', n, 'questions:', len(seen))
