#!/usr/bin/env python3
"""v2.7 full station cases. Reads content/cases/*.txt and merges a complete actor brief, the candidate's
station-specific questions, a filled model presentation and the next steps into every history, psychiatry and
examination station of build/osce_data_v4.json.

Case syntax (one block per case):
  === ID [K] | dx          K = the past-paper variant letter; dx is required for bank stations
  who:   name, age, job                 act:  how to play it: posture, voice, hands, affect
  open:  the opening line, verbatim     story: what they say if given space
  hpc:   Topic: answer        (repeat)  yes: present if asked    no: absent if asked
  pmh: dh: all: fh: sh:                 ice:  idea | concern | expectation
  cue:   the hidden emotional cue       ask:  a question for the candidate (repeat)
  find:  an examination finding (repeat; exam stations)
  key:   what the candidate says | why  (repeat; the station-specific questions or steps)
  rf:    red-flag question | why        (repeat)
  sum:   the summary back to the patient, verbatim
  pres:  the presentation to the examiner, verbatim
  ddx:   likely because | alternative and how to tell | must-not-miss and how to exclude
  ix:    investigations in order         mx: management       tell: the plan and safety-net to the patient, verbatim
"""
import json, glob, re, sys, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = HERE / 'osce_data_v4.json'
REP = {'hpc', 'ask', 'find', 'key', 'rf'}
ONE = {'who', 'act', 'open', 'story', 'yes', 'no', 'pmh', 'dh', 'all', 'fh', 'sh', 'ice', 'cue', 'sum', 'pres', 'ddx', 'ix', 'mx', 'tell', 'dx'}
D = json.loads(DATA.read_text(encoding='utf-8'))
ST = {s['id']: s for s in D['stations']}
TARGET = [s for s in D['stations'] if s.get('type') in ('hx', 'psych', 'ex')]
errs, cases = [], {}


def parse(path):
    cur = None
    for n, raw in enumerate(open(path, encoding='utf-8'), 1):
        ln = raw.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'): continue
        if ln.startswith('==='):
            head = ln[3:].strip(); dx = ''
            if '|' in head: head, dx = [x.strip() for x in head.split('|', 1)]
            parts = head.split(); sid = parts[0]; k = parts[1] if len(parts) > 1 else '_'
            if sid not in ST: errs.append(f'{path}:{n} unknown station {sid}'); cur = None; continue
            key = (sid, k)
            if key in cases: errs.append(f'{path}:{n} duplicate case {sid} {k}')
            cur = cases[key] = {k2: [] for k2 in REP}; cur['_src'] = f'{pathlib.Path(path).name}:{n}'
            if dx: cur['dx'] = dx
            continue
        m = re.match(r'^(\w+):\s*(.*)$', ln)
        if not m or cur is None: errs.append(f'{path}:{n} bad line {ln[:60]!r}'); continue
        k, v = m.group(1), m.group(2).strip()
        if k in REP: cur[k].append(v)
        elif k in ONE:
            if k in cur and k != 'dx': errs.append(f'{path}:{n} repeated {k}')
            cur[k] = v
        else: errs.append(f'{path}:{n} unknown key {k}')


for p in sorted(glob.glob(str(ROOT / 'content' / 'cases' / '*.txt'))): parse(p)


def pairs(lines):
    out = []
    for x in lines:
        a, _, b = x.partition('|'); out.append([a.strip(), b.strip()])
    return out


def flat(c):
    """The actor's facts as plain lines: used by the friends sheet fallback and the AI patient."""
    L = []
    if c.get('act'): L.append('How to play it: ' + c['act'])
    if c.get('open'): L.append('Your opening line: "' + c['open'] + '"')
    if c.get('story'): L.append('If they let you talk: ' + c['story'])
    for h in c['hpc']: L.append('If asked about ' + h[0].lower() + h[1:] if ':' in h else 'If asked: ' + h)
    if c.get('yes'): L.append('Yes, if asked: ' + c['yes'])
    if c.get('no'): L.append('No, if asked: ' + c['no'])
    for k, lab in (('pmh', 'Past medical history'), ('dh', 'Medicines'), ('all', 'Allergies'), ('fh', 'Family history'), ('sh', 'Social history')):
        if c.get(k): L.append(lab + ': ' + c[k])
    if c.get('ice'):
        i = [x.strip() for x in c['ice'].split('|')] + ['', '']
        L.append('ONLY IF ASKED, what you think it is: ' + i[0]); L.append('ONLY IF ASKED, your worry: ' + i[1]); L.append('ONLY IF ASKED, what you want today: ' + i[2])
    if c.get('cue'): L.append('Hidden cue: ' + c['cue'])
    for f in c['find']: L.append('Examination finding: ' + f)
    for q in c['ask']: L.append('Ask the candidate when it fits: ' + q)
    return L


def pack(c, st):
    ddx = [x.strip() for x in c.get('ddx', '').split('|')]
    return {'who': c.get('who', ''), 'act': c.get('act', ''), 'open': c.get('open', ''), 'story': c.get('story', ''),
            'hpc': [[a.strip(), b.strip()] for a, _, b in (h.partition(':') for h in c['hpc'])],
            'yes': c.get('yes', ''), 'no': c.get('no', ''), 'pmh': c.get('pmh', ''), 'dh': c.get('dh', ''), 'all': c.get('all', ''),
            'fh': c.get('fh', ''), 'sh': c.get('sh', ''), 'ice': [x.strip() for x in c.get('ice', '').split('|')] if c.get('ice') else [],
            'cue': c.get('cue', ''), 'ask': c['ask'], 'find': c['find'], 'key': pairs(c['key']), 'rf': pairs(c['rf']),
            'sum': c.get('sum', ''), 'pres': c.get('pres', ''), 'ddx': ddx if len(ddx) == 3 else [], 'ix': c.get('ix', ''), 'mx': c.get('mx', ''), 'tell': c.get('tell', '')}


def check(c, st, k):
    tag = f"{st['id']} {k} ({c['_src']})"
    ex = st.get('type') == 'ex' or bool(c['find'])
    need = ['who', 'pres', 'ddx', 'ix', 'mx'] + ([] if ex else ['open', 'pmh', 'dh', 'sh', 'ice', 'sum', 'tell'])
    for f in need:
        if not c.get(f): errs.append(f'{tag}: missing {f}')
    if not ex and len(c['hpc']) < 4: errs.append(f'{tag}: fewer than 4 hpc lines')
    if len(c['key']) < (3 if ex else 5): errs.append(f'{tag}: too few key lines')
    if ex and len(c['find']) < 2: errs.append(f'{tag}: fewer than 2 findings')
    if c.get('ddx') and len(c['ddx'].split('|')) != 3: errs.append(f'{tag}: ddx needs 3 tiers')
    txt = json.dumps(c, ensure_ascii=False)
    if '—' in txt: errs.append(f'{tag}: em dash')


used = set()
for st in TARGET:
    if st.get('pp'):
        for v in st['vars']:
            c = cases.get((st['id'], v['k']))
            if not c: continue
            used.add((st['id'], v['k'])); check(c, st, v['k'])
            v['cs'] = pack(c, st); v['a'] = flat(c)
            if c.get('dx'): v['dx'] = c['dx']
            if c['find'] and not v.get('r'): v['r'] = 'Findings: ' + ' '.join(c['find'])
    else:
        ks = sorted(k for (sid, k) in cases if sid == st['id'])
        if not ks: continue
        vs = []
        for i, k in enumerate(ks):
            c = cases[(st['id'], k)]; used.add((st['id'], k)); check(c, st, k)
            if not c.get('dx'): errs.append(f"{st['id']} {k}: bank case needs a dx")
            vk = 'ABCDEFG'[i] if k == '_' else k
            v = {'k': vk, 'who': c.get('who', ''), 'dx': c.get('dx', st['t']), 'a': flat(c), 'cs': pack(c, st),
                 'x': ' '.join(x for x in (c.get('pres', ''), 'Investigations: ' + c['ix'] if c.get('ix') else '', 'Management: ' + c['mx'] if c.get('mx') else '') if x)}
            if c['find']: v['r'] = 'Findings: ' + ' '.join(f.rstrip('.') + '.' for f in c['find'])
            vs.append(v)
        st['vars'] = vs
for key in cases:
    if key not in used: errs.append(f'case {key} not attached (wrong variant letter?)')

# coverage report
miss = []
for st in TARGET:
    if st.get('pp'): miss += [f"{st['id']} {v['k']}" for v in st['vars'] if 'cs' not in v]
    elif not st.get('vars'): miss.append(st['id'])
D['meta']['cases'] = len(used); D['meta']['casesMissing'] = len(miss)
STRICT = '--strict' in sys.argv
print(f'cases {len(used)} attached; {len(miss)} history/psych/exam cases still without a full case')
if miss and not STRICT: print('  missing (first 40):', ' '.join(miss[:40]))
if errs:
    for e in errs: print('ERR', e)
    sys.exit(1)
if STRICT and miss: sys.exit(1)
DATA.write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
