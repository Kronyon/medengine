#!/usr/bin/env python3
"""v3.3.5 SBA audit fixes for site/study.html (applied once; kept as a record).

  1. corrections: h0446 (wrong answer: stable lithium is checked every 6 months), h1469 (hyperthermia is one of the
     4 Hs, so two answers were right), h1458 and h0794 (options that did not fit the question), h0738 (lead-in),
     h0659 (LDL range), h1305 (anion gap wording), and the two near-identical clones h1504 and h1626 rewritten
     as new angles on the same topic
  2. inline results moved into an Investigations table where a stem lists 2 or more, as the MSCAA and MS AKT
     papers do; a question keeps its prose if any thought-map cue would stop matching
  3. Hammer set D: new questions from study/snap/hq5_data.py, mostly data interpretation with results tables
     and normal decoy rows, plus ILO topics no question asked; every distractor gets a "why not" line
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parents[1]
SNAP = SITE.parent / 'study' / 'snap'
sys.path.insert(0, str(SNAP))
import hammer, maps, hq5_data  # noqa: E402

F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
HQ = D['hq']['q']
BY = {q['id']: q for q in HQ}
assert len(HQ) == 1632 and 'h1633' not in BY, 'already applied?'
ABS = re.compile(r'\b(only|alone|never|always|ever|nothing|indefinitely|for life|permanently|straight away|at once)\b', re.I)
stats = {'fixed': 0, 'tabled': 0, 'table_skipped': 0, 'new': 0, 'new_with_table': 0}


def blocks(text, head):
    out, cur = [], None
    for raw in text.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        m = re.match(r'^@' + head + r'\s+(.*)$', ln)
        if m:
            cur = {'head': m.group(1).split(), 'lines': []}
            out.append(cur)
        elif cur is not None:
            cur['lines'].append(ln)
    return out


def read(b):
    it = {'lab': [], 'c': [], 'f': [], 'x': [], 'subs': []}
    for ln in b['lines']:
        if ln.startswith('$'):
            parts = [p.strip() for p in ln[1:].split(';')]
            it['lab'].append((parts + ['', ''])[:3])
        elif ln.startswith('?'):
            it['ql'] = ln[1:].strip()
        elif ln.startswith('>'):
            it['o'] = [o.strip() for o in ln[1:].split(' ; ')]
        elif ln.startswith('='):
            it['w'] = ln[1:].strip()
        elif ln.startswith('~'):
            it['ff'] = ln[1:].strip()
        elif ln.startswith('labset '):
            it.setdefault('labset', []).append([x.strip() for x in ln[7:].split(';')])
        elif ln.startswith('lab '):
            a, _, b2 = ln[4:].partition(' => ')
            it['subs'].append((a.strip(), b2.strip()))
        else:
            m = re.match(r'^(s|c|m|g|f|x):\s*(.*)$', ln)
            assert m, 'cannot read: ' + ln
            k, v = m.groups()
            if k == 's':
                it['s'] = v.replace(' // ', '\n')
            elif k == 'c':
                it['c'] += [x.strip() for x in v.split('|') if x.strip()]
            elif k in ('m', 'g'):
                it[k] = v
            elif k == 'f':
                a, _, t = v.partition('=>')
                it['f'].append([a.strip(), t.strip()])
            else:
                a, _, t = v.partition('=>')
                it['x'].append([a.strip(), t.strip()])
    return it


def options(raw):
    names = [o.lstrip('*').strip() for o in raw]
    ans = [o.lstrip('*').strip() for o in raw if o.startswith('*')]
    assert len(ans) == 1, raw
    names.sort(key=hammer.natkey)
    return names, names.index(ans[0])


def map_for(q, it, where):
    mp = {'c': it['c'], 'm': it['m'], 'g': it['g'], 'f': it['f']}
    bad = maps.problems(q, mp)
    norm = [maps.norm(o) for o in q['o']]
    x = []
    for opt, why in it['x']:
        if maps.norm(opt) not in norm:
            bad.append('why-not names no option: ' + opt)
            continue
        i = norm.index(maps.norm(opt))
        if i == q['a']:
            bad.append('why-not given for the answer')
        if re.search(r'[—–]', why):
            bad.append('dash in why-not: ' + why[:40])
        x.append([i, why])
    if it['x'] and sorted(i for i, _ in x) != [i for i in range(5) if i != q['a']]:
        bad.append('why-not must cover all 4 wrong options')
    assert not bad, where + ': ' + '; '.join(bad)
    tm = {'c': mp['c'], 'm': mp['m'], 'g': mp['g'], 'f': [[c, norm.index(maps.norm(t))] for c, t in mp['f']]}
    if x:
        tm['x'] = sorted(x)
    return tm


def lint(q, raw, where):
    probe = {'src': where, 's': q['s'].replace('\n', ' ') + ' ' + q['ql'], 'o': raw, 'w': q['w'], 'f': q['f']}
    e = hammer.lint(probe)
    for t in [q['s'], q['ql'], q['w']] + [r[0] for r in q.get('lab', [])]:
        if re.search(r'[()\[\]—]', t):
            e.append(where + ': bracket or dash in ' + t[:40])
    assert not e, '\n'.join(e)


# ---- 1. corrections ----
for b in blocks(hq5_data.FIX, 'fix'):
    qid = b['head'][0]
    q = BY[qid]
    it = read(b)
    raw = None
    if 's' in it:
        q['s'] = it['s']
    for a, b2 in it['subs']:
        assert q['s'].count(a) == 1, (qid, a)
        q['s'] = q['s'].replace(a, b2)
    for row in it.get('labset', []):
        hit = [r for r in q['lab'] if r[0] == row[0]]
        assert len(hit) == 1, (qid, row)
        hit[0][:] = row
    if 'ql' in it:
        q['ql'] = it['ql']
    if 'o' in it:
        raw = it['o']
        q['o'], q['a'] = options(raw)
    if 'w' in it:
        q['w'] = it['w']
    if 'ff' in it:
        q['f'] = it['ff']
    if it['c']:
        q['tm'] = map_for(q, it, qid)
    else:
        for c, i in q['tm'].get('f', []):
            assert 0 <= i < 5 and i != q['a'], qid
    if raw:
        lint(q, raw, qid)
    stats['fixed'] += 1

# ---- 2. inline results into an Investigations table ----
RES = re.compile(r'(?:(?<=^)|(?<=\. )|(?<=\n))(?P<name>[A-Z][A-Za-z0-9 \-\'’]{1,48}?) (?P<val>(?:[<>]\s?)?\d[\d.,]*(?: ?(?:×|x) ?10⁹/L| ?[A-Za-zµ%³²⁹°/·\.]+(?:/[A-Za-z0-9.²³ ]+?)?)?) \((?P<ref>[<>]?[\d.,–\- <>]+[^()]*?)\)\.(?= |$|\n)')


def to_table(s):
    rows, spans = [], []
    for m in RES.finditer(s):
        name = m.group('name').strip()
        if len(name.split()) > 6 or re.search(r'\b(is|was|has|had|are|shows?|taken|after|her|his)\b', name, re.I):
            continue
        rows.append([name, m.group('val').strip(), m.group('ref').strip()])
        spans.append(m.span())
    if len(rows) < 2:
        return None
    def tidy(t):
        t = re.sub(r'[ ]{2,}', ' ', t)
        t = re.sub(r' *\n *', '\n', t)
        return re.sub(r'\n{2,}', '\n', t).strip()
    out, post = s[:spans[-1][1]], s[spans[-1][1]:]
    for a, b in reversed(spans):
        out = out[:a] + out[b:]
    return tidy(out), rows, tidy(post)  # text after the results sits under the table, as on the papers


for q in HQ:
    if q.get('lab'):
        continue
    got = to_table(q['s'])
    if not got:
        continue
    trial = dict(q, s=got[0], lab=got[1], post=got[2])
    tm = q.get('tm') or {}
    mp = {'c': tm.get('c', []), 'm': tm.get('m', 'x'), 'g': tm.get('g', 'x'), 'f': [[c, q['o'][i]] for c, i in tm.get('f', [])]}
    if tm and [b for b in maps.problems(trial, mp) if b.startswith('cue')]:
        stats['table_skipped'] += 1
        continue
    q['s'], q['lab'], q['post'] = got
    stats['tabled'] += 1

# ---- 3. Hammer set D ----
ERR = []
n = max(int(q['id'][1:]) for q in HQ)
for b in blocks(hq5_data.Q, 'u'):
    unit, hp = b['head']
    it = read(b)
    n += 1
    qid = 'h%04d' % n
    raw = it['o']
    names, a = options(raw)
    q = {'id': qid, 't': 'u', 'k': unit, 'h': int(hp[0]), 'p': hp[1], 's': it['s'], 'o': names, 'a': a,
         'w': it['w'], 'f': it['ff'], 'ql': it['ql'], 'post': ''}
    assert 0 <= int(unit) < len(D['units']) and hp[1] in hammer.PAT, qid
    if it['lab']:
        q['lab'] = it['lab']
        stats['new_with_table'] += 1
    try:
        lint(q, raw, qid)
        q['tm'] = map_for(q, it, qid)
    except AssertionError as e:
        ERR.append(str(e))
        continue
    HQ.append(q)
    stats['new'] += 1

assert not ERR, '\n'.join(ERR)
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print(json.dumps(stats))
