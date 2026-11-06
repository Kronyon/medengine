#!/usr/bin/env python3
"""v3.6.13: import the Hammer bank rewritten by Antigravity (v3.6.12) on top of the v3.6.10 build, with save safety.

v3.6.12 changed the options of 754 questions but wrote run-migration entries for only 105, and 56 of those mapped
picks to the wrong option. Here every question whose options changed gets one correct entry at data version 13:
old option index -> index of the same text in the new list, or a full clear when the answer itself changed
(a pick made on a different question is not carried over). v3.6.12's own version 13/14 entries are dropped.
Runs saved on v3.6.10 or earlier (data version 12 or below) move correctly; runs saved on v3.6.12 itself (14) are left
alone, because they were made on this text. Text polish (no option order change): >= <= -> ug cm2, spaced dashes,
LaTeX, and the "Under NICE guidelines," prefix MSCAA never puts in a lead-in."""
import json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
F = ROOT / 'site' / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2)); HQ = D['hq']
IMP = json.loads((ROOT / 'study' / 'snap' / 'rw' / 'import_v3612.json').read_text(encoding='utf-8'))
OLD = {q['id']: q for q in HQ['q']}
assert HQ.get('ov') == 12, 'expected the v3.6.10 build (data version 12) before the import, got %s' % HQ.get('ov')
norm = lambda t: re.sub(r'\s+', ' ', t).strip().lower()
toks = lambda t: set(re.findall(r'[a-z0-9]+', norm(t).replace('-', ' ')))
def same(a, b):
    # the same option after light rewording ("Sulfonylurea hypoglycaemia" / "Sulfonylurea-induced hypoglycaemia")
    if norm(a) == norm(b): return True
    A, B = toks(a), toks(b)
    return bool(A and B) and (A <= B or B <= A or len(A & B) / len(A | B) >= 0.6)
def match(t, opts):
    hits = [j for j, u in enumerate(opts) if norm(u) == norm(t)] or [j for j, u in enumerate(opts) if same(t, u)]
    return hits[0] if len(hits) == 1 else None

def polish(t):
    if not isinstance(t, str): return t
    t = t.replace('>=', '≥').replace('<=', '≤').replace('->', '→')
    t = re.sub(r'(\d) ?ug\b', r'\1 µg', t); t = re.sub(r'\bcm2\b', 'cm²', t); t = re.sub(r'\bmm3\b', 'mm³', t)
    t = re.sub(r'\$([^$]{1,80})\$', lambda m: m.group(1).replace('\\div', '÷').replace('\\times', '×').replace('\\', ''), t)
    t = re.sub(r'\b([VL])(\d+)–\1?(\d+)\b', r'\1\2 to \1\3', t)            # V1–V4 -> V1 to V4 (an en dash only inside numeric ranges)
    t = re.sub(r' [–—] ', ', ', t); t = t.replace('—', ', ')
    t = re.sub(r'\b(locali|organi|recogni|minimi|stabili|hospitali|characteri|categori|prioriti|summari|utili|optimi|immobili|immuni|sensiti|anaestheti|visuali|catheteri|randomi|standardi)z(e|ed|es|ing|ation|ations)\b', r'\1s\2', t)
    t = re.sub(r'\b(Locali|Organi|Recogni|Minimi|Stabili|Hospitali|Characteri|Categori|Prioriti|Summari|Utili|Optimi|Immobili|Immuni|Sensiti|Anaestheti|Visuali|Catheteri|Randomi|Standardi)z', r'\1s', t)
    return t
def deep(x):
    if isinstance(x, str): return polish(x)
    if isinstance(x, list): return [deep(v) for v in x]
    if isinstance(x, dict): return {k: (v if k in ('id', 'k', 't', 'set', 'pmv', 'lab') else deep(v)) for k, v in x.items()}
    return x
GUIDE = re.compile(r'^(?:Under|According to|Per|Following|Based on)\s+(?:the\s+)?[^,?]{2,90}?(?:guidelines?|guidance|criteria|recommendations|standards|pathway)(?:\s*\(\d{4}\))?,\s*', re.I)

moved = cleared = stripped = 0
new_q = []
for q in IMP['hq_q']:
    q = deep(q); o = OLD[q['id']]
    if q.get('lab'): q['lab'] = [[polish(c) if i < 2 else c for i, c in enumerate(r)] for r in q['lab']]
    ql = q.get('ql', ''); m = GUIDE.match(ql)
    if m: rest = ql[m.end():]; q['ql'] = rest[:1].upper() + rest[1:]; stripped += 1
    pmv = [p for p in o.get('pmv', []) if p[0] <= 12]          # the v3.6.10 history, untouched
    if [norm(t) for t in q['o']] != [norm(t) for t in o['o']]:
        if match(o['o'][o['a']], q['o']) != q['a']: perm = [None] * len(o['o']); cleared += 1   # a different answer: a different question
        else:
            perm = [match(t, q['o']) for t in o['o']]
            if len({v for v in perm if v is not None}) < len([v for v in perm if v is not None]): perm = [None] * len(o['o']); cleared += 1
            else: moved += 1
        pmv.append([13, perm])
    if pmv: q['pmv'] = pmv
    else: q.pop('pmv', None)
    q.pop('ml', None); q.pop('mw', None)                       # Mock-like is recomputed by v364_ml.py
    new_q.append(q)
HQ['q'] = new_q; HQ['ov'] = 14                                  # 14 = the version v3.6.12 shipped, so its runs stay put
for x in D['off']['q']:
    if x['id'] in IMP['off_w']: x['w'] = IMP['off_w'][x['id']]
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print(f'v3.6.12 bank imported: {len(new_q)} questions | picks moved by text {moved} | rebuilt (picks cleared) {cleared} | guideline prefixes removed from lead-ins {stripped}')
