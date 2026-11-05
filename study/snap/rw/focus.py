"""Print only the clone and negative-lead-in questions for the given weeks, each clone with the question it copies."""
import json, re, sys
t = open('site/study.html').read()
D = json.loads(re.search(r'<script id="qqdata" type="application/json">(.*?)</script>', t, re.S).group(1))
BY = {q['id']: q for q in D['hq']['q']}
T = json.load(open('study/snap/rw/triage.json'))
def show(i, tag=''):
    q = BY[i]; print(f"## {i} {tag} set={q.get('set','')} k={q['k']}")
    print(q['s']); [print('LAB', *l) for l in q.get('lab', [])]
    print('Q:', q['ql']); [print(('  * ' if j == q['a'] else '  - ') + o) for j, o in enumerate(q['o'])]
for w in sys.argv[1:]:
    for i, v in T.items():
        if v['w'] != w: continue
        fl = [f for f in v['f'] if f.startswith('clone') or f in ('neg', 'abs')]
        if not fl: continue
        show(i, ','.join(fl))
        for f in fl:
            if f.startswith('clone:'): print('   ~~ copies:'); show(f[6:])
        print()
