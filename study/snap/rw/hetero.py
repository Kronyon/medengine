"""Lead-in vs option-category mismatch: a diagnosis lead-in with tests or drugs among the options, a test lead-in with
treatments, and so on. These break the MSCAA rule that all five options are the same kind of thing."""
import json, re, collections, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
src = (HERE / 'detect.py').read_text().split('out = {}')[0].replace('pathlib.Path(__file__)', 'pathlib.Path(%r)' % str(HERE / 'detect.py'))
exec(src)
T = json.load(open(HERE / 'triage.json'))
def lc(ql):
    ql = (ql or '').lower()
    if re.search(r'most likely (diagnosis|cause|explanation|underlying)|which (term|sign)|which (organism|type)', ql): return 'dx'
    if re.search(r'investigation|which test', ql): return 'test'
    if re.search(r'which (drug|antibiotic|medication|inhaler|antipsychotic)', ql): return 'drug'
    return None
BAD = []
for q in H:
    want = lc(q.get('ql'))
    if not want: continue
    off = sum(k != want and not (want == 'drug' and k == 'act') for k in (kind(x) for x in q['o']))
    if off >= 2: BAD.append(q['id'])
if __name__ == '__main__':
    BY = {q['id']: q for q in H}
    print(len(BAD), collections.Counter(T[i]['w'] for i in BAD).most_common(40))
    for i in BAD:
        q = BY[i]
        if sys.argv[1:] and T[i]['w'] not in sys.argv[1:]: continue
        print(i, T[i]['w'], '|', q['ql'][:50], '|', ' / '.join(('*' if j == q['a'] else '') + x for j, x in enumerate(q['o'])))
