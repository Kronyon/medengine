#!/usr/bin/env python3
"""v3.6.3 STUDY data clean-up (applied once).

1. 54 of the 66 questions added in 3.6.0 (h1713 to h1740, h1753 to h1778) were USMLE basic science (embryology,
   genetics, electron micrographs) filed under units such as Fibroadenoma, and each showed a UWorld screenshot whose
   notes give the answer away. They leave STUDY. 49 already live in STEP1; the other 5 go to step1/from_study.json
   and join STEP1 on its next build.
2. The 12 clinical ones stay, filed where they belong; 3 that sit outside the FFP ILOs (pre-eclampsia, ectopic,
   Kawasaki) get their own clearly labelled off-map heading.
3. "Why not" lines: the 1,298 template lines ("The clinical findings instead specifically indicated X rather than
   Y") and the 542 copy-paste "Ruled out by ..., selecting X rather than Y" lines (the gate pasted under every
   wrong option) are removed. Options
   with nothing left get the matching line from your own triggers, drug, test and procedure cards when one exists.
   Hand-written lines are added by v363_hand.py.
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parents[1]
ROOT = SITE.parent
sys.path.insert(0, str(ROOT / 'study' / 'snap'))
F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
Q = D['hq']['q']
assert any(q['id'] == 'h1713' for q in Q), 'already applied'
st = {}
def bump(k, n=1): st[k] = st.get(k, 0) + n

# 1. USMLE questions out
step1 = json.loads((ROOT / 'step1' / 'pack_base.json').read_text(encoding='utf-8'))
have = {re.sub(r'\W', '', q['s'])[:60].lower() for q in step1['hq']['q']}
USMLE = {'h%04d' % n for n in list(range(1713, 1741)) + list(range(1753, 1779))}
move = [q for q in Q if q['id'] in USMLE and re.sub(r'\W', '', q['s'])[:60].lower() not in have]
(ROOT / 'step1' / 'from_study.json').write_text(json.dumps(move, ensure_ascii=False, indent=1), encoding='utf-8')
Q[:] = [q for q in Q if q['id'] not in USMLE]
bump('usmle_removed', len(USMLE)); bump('moved_to_step1', len(move))

# 2. re-file
REFILE = {'h1742': ('u', '16'), 'h1743': ('u', '45'), 'h1744': ('u', '68'), 'h1745': ('u', '72'), 'h1746': ('u', '142'),
          'h1747': ('u', '10'), 'h1748': ('u', '89'), 'h1749': ('b', 'outside'), 'h1750': ('u', '49'),
          'h1751': ('u', '101'), 'h1752': ('b', 'outside')}
D['hq']['tt']['b:outside'] = 'Outside the FFP ILOs: O&G and paediatrics'
for q in Q:
    if q['id'] in REFILE:
        q['t'], q['k'] = REFILE[q['id']]; bump('refiled')

# 3. why-not lines
from whynot_kb import match  # noqa: E402  (knowledge base built from this page's triggers, drug, test and procedure cards)
LAZY = re.compile(r'instead specifically indicated|clinical findings instead', re.I)
RULED = re.compile(r'^Ruled out by (.+?); (.+?), selecting .+ rather than .+\.?$')
for src in ('hq', 'mock', 'off'):
    for q in D[src]['q']:
        tm = q.get('tm')
        if not tm:
            continue
        flips = {i for _, i in tm.get('f', [])}
        out = []
        for i, t in tm.get('x', []):
            if LAZY.search(t):
                bump('lazy_removed'); continue
            m = RULED.match(t)
            if m:   # the same sentence pasted under every wrong option: it restates the gate, so it goes
                bump('ruled_removed'); continue
            out.append([i, t])
        got = {i for i, _ in out}
        if src == 'hq':
            for i, o in enumerate(q['o']):
                if i == q['a'] or i in got or i in flips:
                    continue
                k = match(o)
                if k:
                    out.append([i, k[1]]); bump('kb_filled')
        tm['x'] = sorted(out)
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print(json.dumps(st))
