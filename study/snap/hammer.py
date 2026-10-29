"""🔨 Hammer SBAs: original single-best-answer questions at 3 difficulty levels for every ILO condition, drug group and
intervention, written in the style of the FFP formative AKT (Nottingham + MSCAA): short stems, 5 options from one
lookalike pool, one decisive clue. Own words, UK guidance. Files hq_*.py hold Q, a text block:

    @u 12                       target: a unit index
    @d antiplatelets Antiplatelets      target: a drug group (key, then title)
    @x scores Scores                    target: an intervention group
    @b otosclerosis Otosclerosis        target: off-the-map topic seen in the mock but not an ILO title
    1L: stem ending in a question mark?      hammer 1 to 3 + pattern letter
    > option ; option ; *correct option ; option ; option
    = why the answer is right
    ~ what one change would flip it
    $ Sodium ; 128 mmol/L ; 135–145   optional Investigations rows: name ; value ; reference range (set C, MSCAA style)
    ! rule                      set C: one patient across a target's three questions (diagnosis, test, treatment); the rule that links them

Hammer: 1 = classic picture, one step. 2 = two steps, a lookalike or a number that overrides the story.
3 = the curveball: an exception, a contraindication, anatomy, the rare-but-tested variant.
Pattern: L lookalike swap, N one number overrides, T place, time or anatomy flips it, D drug culprit or drug step,
R the right rung: first step versus definitive step."""
import glob, importlib, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
PAT = {'L': 'Lookalike', 'N': 'Number', 'T': 'Place, time or anatomy', 'D': 'Drug', 'R': 'Right rung'}
US = [r'\bcolors?\b', r'\banemi', r'(?<!o)esophag', r'\bpediatric', r'\bhemoglobin', r'\bbehavior', r'\bcenter\b', r'\bedema',
      r'\bleukocyt', r'\bfetus\b', r'\btumor\b', r'\bdiarrhea', r'\bhematuria', r'\bischemi', r'\bestrogen', r'\banesthe', r'\bfeces\b']


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r'(\d+)', s.lower())]


def parse_file(text, src):
    out, err, tgt, cur, rule = [], [], None, None, ''
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line: continue
        where = f'{src}:{n}'
        m = re.match(r'^@([udxb])\s+(\S+)(?:\s+(.*))?$', line)
        if m:
            tgt = (m.group(1), m.group(2), (m.group(3) or '').strip()); rule = ''; continue
        if line.startswith('!'):
            rule = line[1:].strip(); continue
        m = re.match(r'^([123])([LNTDR]):\s*(.+)$', line)
        if m:
            if tgt is None: err.append(f'{where}: question before any @ target'); continue
            cur = {'t': tgt[0], 'k': tgt[1], 'kt': tgt[2], 'h': int(m.group(1)), 'p': m.group(2), 's': m.group(3).strip(), 'src': where}
            if rule: cur['cr'] = rule; cur['ck'] = src + ':' + tgt[0] + ':' + tgt[1]
            out.append(cur); continue
        if cur is None: err.append(f'{where}: line outside a question'); continue
        if line.startswith('>'):
            cur['o'] = [o.strip() for o in line[1:].split(' ; ')]
        elif line.startswith('='): cur['w'] = line[1:].strip()
        elif line.startswith('~'): cur['f'] = line[1:].strip()
        elif line.startswith('$'):
            parts = [x.strip() for x in line[1:].split(' ; ')]
            if not 2 <= len(parts) <= 3: err.append(f'{where}: lab row needs name ; value ; range')
            cur.setdefault('lab', []).append((parts + [''])[:3])
        else: err.append(f'{where}: cannot read "{line[:40]}"')
    return out, err


def lint(q):
    e, w = [], q['src']
    for k in ('o', 'w', 'f'):
        if not q.get(k): e.append(f'{w}: missing {k}')
    if e: return e
    if len(q['o']) != 5: e.append(f'{w}: needs 5 options, has {len(q["o"])}')
    stars = [o for o in q['o'] if o.startswith('*')]
    if len(stars) != 1: e.append(f'{w}: needs exactly one * answer')
    names = [o.lstrip('*').strip() for o in q['o']]
    if len(set(n.lower() for n in names)) != len(names): e.append(f'{w}: duplicate options')
    if not q['s'].endswith('?'): e.append(f'{w}: stem should end with a question')
    blob = ' '.join([q['s'], q['w'], q['f']] + names)
    if re.search(r'[—–]', blob): e.append(f'{w}: em or en dash')
    if re.search(r'[()\[\]]', blob): e.append(f'{w}: brackets')
    for u in US:
        if re.search(u, blob, re.I): e.append(f'{w}: US spelling {u}')
    if len(q['s']) > 700: e.append(f'{w}: stem too long')
    # no give-aways: the answer must not stand out by length, and distractors must not carry absolute words
    L = [len(n) for n in names]; ai = [i for i, o in enumerate(q['o']) if o.startswith('*')][0]
    rest = max(L[:ai] + L[ai + 1:])
    if L[ai] - rest >= 12 and L[ai] > rest * 1.4: e.append(f'{w}: answer much longer than every distractor')
    ABS = re.compile(r'\b(only|alone|never|always|ever|nothing|indefinitely|for life|permanently|straight away|at once)\b', re.I)
    if any(ABS.search(n) for i, n in enumerate(names) if i != ai) and not ABS.search(names[ai]) and 'Progestogen-only' not in ' '.join(names): e.append(f'{w}: absolute word in a distractor')
    return e


def build(units):
    # order fixes the question ids (h0001...), which key saved progress: sets A and B sorted together as v2.4 shipped, then set C after
    files = sorted(glob.glob(str(HERE / 'hq_*.py')) + glob.glob(str(HERE / 'hq2_*.py'))) + sorted(glob.glob(str(HERE / 'hq3_*.py')))
    qs, err = [], []
    for f in files:
        mod = importlib.import_module(pathlib.Path(f).stem)
        got, e = parse_file(mod.Q, pathlib.Path(f).name); qs += got; err += e
    titles = {}
    for q in qs:
        err += lint(q)
        if q['src'].startswith('hq3_') and not q.get('cr'): err.append(f'{q["src"]}: set C questions need a ! rule for their patient')
        if q['t'] == 'u':
            if not q['k'].isdigit() or int(q['k']) >= len(units): err.append(f'{q["src"]}: unit {q["k"]} does not exist')
        else:
            if not q['kt'] and q['k'] not in titles: err.append(f'{q["src"]}: {q["t"]} {q["k"]} needs a title the first time')
            if q['kt']: titles[q['t'] + ':' + q['k']] = q['kt']
            titles.setdefault(q['k'], q['kt'])
    # every target gets one question at each hammer level
    by = {}
    for q in qs: by.setdefault((q['t'], q['k']), []).append(q['h'])
    for (t, k), hs in by.items():
        if not (hs.count(1) == hs.count(2) == hs.count(3) >= 1 and len(hs) == 3 * hs.count(1)): err.append(f'{t} {k}: hammers {sorted(hs)}, want each of 1, 2 and 3 the same number of times')
    if err: raise SystemExit('hammer errors:\n  ' + '\n  '.join(err[:60]))
    out, n = [], 0
    for q in qs:
        names = [o.lstrip('*').strip() for o in q['o']]
        ans = names[[i for i, o in enumerate(q['o']) if o.startswith('*')][0]]
        names.sort(key=natkey)
        n += 1
        it = {'id': 'h%04d' % n, 't': q['t'], 'k': q['k'], 'h': q['h'], 'p': q['p'], 's': q['s'], 'o': names, 'a': names.index(ans), 'w': q['w'], 'f': q['f']}
        for k in ('lab', 'cr', 'ck'):
            if q.get(k): it[k] = q[k]
        out.append(it)
    tt = {}
    for q in qs:
        if q['t'] != 'u' and q['kt']: tt[q['t'] + ':' + q['k']] = q['kt']
    return {'q': out, 'tt': tt, 'pat': PAT}


def units_covered(H, units):
    return sorted({int(q['k']) for q in H['q'] if q['t'] == 'u'})
