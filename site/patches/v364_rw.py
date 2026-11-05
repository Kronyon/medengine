#!/usr/bin/env python3
"""v3.6.4 Hammer rewrites (safe to run again; it applies only entries not yet in the page).

Each study/snap/rw/rw_NN_*.py holds R = {qid: entry}. An entry:
  'o':  [(old option text, new option text, why-not line), ...]
        why-not line: a new sentence for a new or reworded distractor; 'keep' keeps the line already there
        (use only when the meaning is unchanged, e.g. a length tweak); None for the answer itself.
  'f':  {new option text: flip condition}   optional "change the film" lines for new distractors
  'x':  {option text: why-not}               optional new why-not for an option whose text is unchanged
  'new': {s, lab, ql, o, a, w, ff, c, m, g, flip, x}   a clone rebuilt as a different question (answer text in a)
  'ql': new lead-in                            optional
  's':  [(old stem text, new stem text)]      optional
  'w', 'g', 'm', 'ff':                         optional new explanation, gate, mechanism, lookalike line

What it does per question: swaps the texts, re-sorts the options alphabetically when they were alphabetical before,
moves the answer, why-not lines and flips to the new letters, drops flips that described a replaced option, and
records the letter map in q.pmv so saved runs move with it (engine: hqMig). Checks: 5 different options, one answer,
every wrong option has a why-not line or a flip, no dashes, no absolute word only in a distractor, and the answer does
not stand out by length (more than 15% and 3 characters longer than every distractor)."""
import json, re, sys, glob, importlib.util, pathlib
SITE = pathlib.Path(__file__).resolve().parents[1]
RW = SITE.parent / 'study' / 'snap' / 'rw'
F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2)); HQ = D['hq']; BY = {q['id']: q for q in HQ['q']}
DASH = re.compile(r'—|(?<!\d)–|–(?!\d)')   # an en dash is allowed only inside a reference range (4.0–7.8)
ABS = re.compile(r'\b(only|alone|never|always|ever|nothing|indefinitely|for life|permanently|straight away|at once)\b', re.I)
R = {}; VER = {}
# each rw_NN_*.py file is one published batch and gets its own data version (3 + NN - 1), so a run saved
# between two batches is moved only by the batches after it. Never change option order in a published file:
# add a new numbered file instead.
for f in sorted(glob.glob(str(RW / 'rw_[0-9][0-9]_*.py'))):
    spec = importlib.util.spec_from_file_location(pathlib.Path(f).stem, f); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    n = int(pathlib.Path(f).stem.split('_')[1])
    for k, v in m.R.items():
        if k in R and set(v) == {'x'}:   # a why-not-only entry merges into an earlier rewrite of the same question
            R[k].setdefault('x', {}).update(v['x']); continue
        if k in R and set(R[k]) == {'x'}:   # an earlier why-not-only entry folds into this rewrite
            v = dict(v); v['x'] = {**R[k]['x'], **v.get('x', {})}; R[k] = v; VER[k] = 2 + n; continue
        assert k not in R, ('duplicate entry', k, f)
        R[k] = v; VER[k] = 2 + n
done = skipped = 0; errs = []
def isalpha(o): k = [x.lower() for x in o]; return k == sorted(k)
def replace_whole(q, n):
    """a clone rebuilt as a new question: everything replaced, old picks for it are cleared"""
    if q['s'] == n['s'] and q['o'] == sorted(n['o'], key=str.lower): return False
    o = sorted(n['o'], key=str.lower); a = o.index(n['a'])
    q['s'] = n['s']; q['lab'] = n.get('lab', []); q['ql'] = n['ql']; q['o'] = o; q['a'] = a
    q['w'] = n['w']; q['f'] = n.get('ff', ''); q.pop('img', None)
    q['tm'] = {'c': n['c'], 'm': n['m'], 'g': n['g'],
               'f': [[c, o.index(t)] for t, c in n.get('flip', {}).items()],
               'x': sorted([[o.index(t), w] for t, w in n['x'].items()])}
    q.setdefault('pmv', []).append([ver, [None] * 5])
    return True
for qid, e in R.items():
    q = BY.get(qid); assert q, qid
    ver = VER[qid]
    if 'new' in e:
        if not replace_whole(q, e['new']): skipped += 1; continue
        o = q['o']; a = q['a']; tm = q['tm']
        cov = {i for i, _ in tm['x']} | {i for _, i in tm['f']}
        gap = [o[i] for i in range(5) if i != a and i not in cov]
        if gap: errs.append(f'{qid}: no why-not for {gap}')
        if len({x.lower() for x in o}) != 5: errs.append(f'{qid}: duplicate options')
        if DASH.search(json.dumps({k: v for k, v in e['new'].items() if k != 'lab'}, ensure_ascii=False)): errs.append(f'{qid}: dash')
        L = [len(x) for x in o]; rest = max(L[:a] + L[a + 1:])
        if L[a] > rest and L[a] - rest > 3 and L[a] > rest * 1.15: errs.append(f'{qid}: answer stands out by length')
        if any(ABS.search(x) for i, x in enumerate(o) if i != a) and not ABS.search(o[a]): errs.append(f'{qid}: absolute word only in a distractor')
        q['rw'] = ver; done += 1; continue
    pairs = e.get('o', [])
    olds = [a for a, b, c in pairs]; news = [b for a, b, c in pairs]
    if pairs and all(n in q['o'] for n in news) and not all(o in q['o'] for o in olds if o not in news):
        skipped += 1; continue  # already applied
    if not pairs and e.get('ql') and q.get('ql') == e['ql']: skipped += 1; continue
    miss = [o for o in olds if o not in q['o']]
    if miss: errs.append(f'{qid}: option not found {miss}'); continue
    old = q['o'][:]; ans_old = old[q['a']]
    new = old[:]; why = {}; changed = set()
    for a, b, c in pairs:
        i = old.index(a); new[i] = b
        if i == q['a']:
            assert c is None, (qid, 'answer gets no why-not', a)
        else:
            if c is None: errs.append(f'{qid}: distractor {a!r} needs a why-not line or keep'); continue
            if c != 'keep': why[b] = c; changed.add(i)
    ans_new = new[q['a']]
    order = sorted(range(5), key=lambda i: new[i].lower()) if isalpha(old) else list(range(5))
    pm = [order.index(i) for i in range(5)]   # old letter -> new letter
    tm = q.setdefault('tm', {'c': [], 'm': '', 'g': '', 'f': [], 'x': []})
    xs = {i: t for i, t in tm.get('x', [])}
    nx = []
    for i in range(5):
        if i == q['a']: continue
        t = why.get(new[i]) if i in changed else xs.get(i)
        if t: nx.append([pm[i], t])
    ren = {a: b for a, b, c in pairs}
    for txt, w in (e.get('x') or {}).items():   # rewritten why-not (keys may name an option before its rename)
        txt = ren.get(txt, txt)
        assert txt in new and new.index(txt) != q['a'], (qid, 'x for unknown option', txt)
        i = new.index(txt); nx = [r for r in nx if r[0] != pm[i]] + [[pm[i], w]]
    nf = [[c, pm[i]] for c, i in tm.get('f', []) if i not in changed]
    for txt, cond in (e.get('f') or {}).items():
        assert txt in new, (qid, 'flip for unknown option', txt)
        nf.append([cond, pm[new.index(txt)]])
    q['o'] = [new[i] for i in order]; q['a'] = pm[q['a']]
    tm['x'] = sorted(nx); tm['f'] = nf
    if e.get('ql'): q['ql'] = e['ql']
    for k in ('w', 'g', 'm'):   # explanation, gate and mechanism when the answer itself changes
        if k in e:
            if k == 'w': q['w'] = e[k]
            else: tm[k] = e[k]
    if 'ff' in e: q['f'] = e['ff']
    for a, b in e.get('s', []):
        if a not in q['s']: errs.append(f'{qid}: stem text not found {a[:40]!r}'); continue
        q['s'] = q['s'].replace(a, b)
    if pm != list(range(5)): q.setdefault('pmv', []).append([ver, pm])
    # checks
    o = q['o']; a = q['a']
    if len({x.lower() for x in o}) != 5: errs.append(f'{qid}: duplicate options {o}')
    if o[a] != ans_new: errs.append(f'{qid}: answer moved wrongly')
    cov = {i for i, _ in tm['x']} | {i for _, i in tm['f']}
    gap = [o[i] for i in range(5) if i != a and i not in cov]
    if gap: errs.append(f'{qid}: no why-not for {gap}')
    blob = ' '.join(o + [t for _, t in tm['x']] + [c for c, _ in tm['f']] + [q['s'], q.get('ql', '')])
    if DASH.search(blob): errs.append(f'{qid}: dash')
    if any(ABS.search(x) for i, x in enumerate(o) if i != a) and not ABS.search(o[a]): errs.append(f'{qid}: absolute word only in a distractor')
    L = [len(x) for x in o]; rest = max(L[:a] + L[a + 1:])
    if pairs and L[a] > rest and L[a] - rest > 3 and L[a] > rest * 1.15: errs.append(f'{qid}: answer still stands out by length ({L[a]} vs {rest})')
    q['rw'] = ver; done += 1
if errs:
    print('\n'.join(errs)); sys.exit('NOT WRITTEN: fix the entries above')
if done:
    HQ['ov'] = max(HQ.get('ov', 2), max(VER[k] for k in R))
    page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
    F.write_text(page, encoding='utf-8')
print(f'rewrites applied: {done}, already in: {skipped}, data version {HQ.get("ov", 2)}')
