#!/usr/bin/env python3
"""v3.6.2 Hammer set E: 87 paper-style SBAs from study/snap/hq6_a.py, hq6_b.py and hq6_c.py (applied once).

Written fresh in the style of the MS AKT, MSCAA and Nottingham mock papers: a 40 to 90 word stem, observations in a
second paragraph, a results table where the paper would use one, 5 alphabetical options and a standard lead-in.
Every question has a thought map, up to 3 change-the-film flips and a "why not" line for all 4 wrong options.
New off-map targets get their titles here.
Usage: python3 site/patches/v362_sba.py [--check]
"""
import importlib, json, pathlib, re, statistics, sys

SITE = pathlib.Path(__file__).resolve().parents[1]
SNAP = SITE.parent / 'study' / 'snap'
sys.path.insert(0, str(SNAP))
import hammer, maps  # noqa: E402

CHECK = '--check' in sys.argv
F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
HQ = D['hq']['q']
TITLES = {'b:hepatitis': 'Viral hepatitis', 'b:infection': 'Infection control and bloodborne viruses',
          'b:ethics': 'Ethics: the four principles', 'b:jaundice': 'Jaundice and LFT patterns',
          'b:bone': "Paget's disease and metabolic bone", 'b:inflamarthritis': 'Rheumatoid and psoriatic arthritis',
          'b:dysphagia': 'Dysphagia and pharyngeal pouch'}


def blocks(text):
    out, cur = [], None
    for raw in text.splitlines():
        ln = raw.strip()
        if not ln:
            continue
        m = re.match(r'^@(u|k)\s+(\S+)\s+(\S+)$', ln)
        if m:
            kind, tgt, hp = m.groups()
            t, k = ('u', tgt) if kind == 'u' else tgt.split(':', 1)
            cur = {'t': t, 'k': k, 'hp': hp, 'lines': []}
            out.append(cur)
        elif cur is not None:
            cur['lines'].append(ln)
        else:
            raise SystemExit('text before the first head: ' + ln)
    return out


def read(b):
    it = {'lab': [], 'c': [], 'f': [], 'x': []}
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
            else:
                a, _, t = v.partition('=>')
                it[k].append([a.strip(), t.strip()])
    return it


def options(raw):
    names = [o.lstrip('*').strip() for o in raw]
    ans = [o.lstrip('*').strip() for o in raw if o.startswith('*')]
    assert len(ans) == 1, raw
    names.sort(key=hammer.natkey)
    return names, names.index(ans[0])


def problems(q, it, raw, where):
    probe = {'src': where, 's': q['s'].replace('\n', ' ') + ' ' + q['ql'], 'o': raw, 'w': q['w'], 'f': q['f']}
    bad = hammer.lint(probe)
    for t in [q['s'], q['ql'], q['w']] + [r[0] for r in q.get('lab', [])]:
        if re.search(r'[()\[\]—]', t):
            bad.append('bracket or dash in ' + t[:40])
    mp = {'c': it['c'], 'm': it['m'], 'g': it['g'], 'f': it['f']}
    bad += maps.problems(q, mp)
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
    if sorted(i for i, _ in x) != [i for i in range(5) if i != q['a']]:
        bad.append('why-not must cover all 4 wrong options')
    for f in [mp['m'], mp['g'], q['f']] + [c for c, _ in it['f']]:
        if '(' in f:
            bad.append('bracket in map: ' + f[:40])
    tm = {'c': mp['c'], 'm': mp['m'], 'g': mp['g'], 'f': [[c, norm.index(maps.norm(t))] for c, t in mp['f'] if maps.norm(t) in norm], 'x': sorted(x)}
    return [where + ': ' + b for b in bad], tm


ERR, NEW = [], []
n = max(int(q['id'][1:]) for q in HQ)
assert not any(q.get('set') == 'E' for q in HQ), 'already applied'
for name in ('hq6_a', 'hq6_b', 'hq6_c'):
    if not (SNAP / (name + '.py')).exists():
        continue
    mod = importlib.import_module(name)
    for j, b in enumerate(blocks(mod.Q), 1):
        where = '%s #%d' % (name, j)
        try:
            it = read(b)
            raw = it['o']
            names, a = options(raw)
        except Exception as e:  # noqa: BLE001
            ERR.append(where + ': ' + str(e))
            continue
        n += 1
        q = {'id': 'h%04d' % n, 't': b['t'], 'k': b['k'], 'h': int(b['hp'][0]), 'p': b['hp'][1], 's': it['s'], 'o': names,
             'a': a, 'w': it['w'], 'f': it.get('ff', ''), 'ql': it['ql'], 'post': '', 'set': 'E'}
        if b['t'] == 'u':
            if not (0 <= int(b['k']) < len(D['units'])):
                ERR.append(where + ': no unit ' + b['k'])
        elif (b['t'] + ':' + b['k']) not in D['hq']['tt'] and (b['t'] + ':' + b['k']) not in TITLES:
            ERR.append(where + ': target needs a title ' + b['t'] + ':' + b['k'])
        if b['hp'][1] not in hammer.PAT:
            ERR.append(where + ': pattern ' + b['hp'])
        if it['lab']:
            q['lab'] = [list(r) for r in it['lab']]
        bad, tm = problems(q, it, raw, where)
        ERR += bad
        q['tm'] = tm
        NEW.append(q)

stems = [len((q['s'] + ' ' + q['ql']).split()) for q in NEW]
print(json.dumps({'new': len(NEW), 'with_table': sum(1 for q in NEW if q.get('lab')), 'stem_words_median': statistics.median(stems) if stems else 0,
                  'answer_positions': [sum(1 for q in NEW if q['a'] == i) for i in range(5)], 'errors': len(ERR)}))
if ERR:
    print('\n'.join(ERR))
    sys.exit(1)
if CHECK:
    sys.exit(0)
for k, v in TITLES.items():
    D['hq']['tt'].setdefault(k, v)
HQ += NEW
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print('applied', NEW[0]['id'], 'to', NEW[-1]['id'])
