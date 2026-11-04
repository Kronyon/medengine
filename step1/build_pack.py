#!/usr/bin/env python3
"""Compile the medengine-STEP1 content pack (step1/src/*.txt) into step1/pack.json.

Everything in src/ is written in our own words from standard Step 1 knowledge. Nothing is copied from First Aid,
Mehlman, UWorld, Boards and Beyond or Bootcamp: those books shaped the structure (chapters, one-line triggers, arrows),
not the text.

  topics_*.txt   First Aid chapters (sections), topics and red-flag trigger rows        @ / # / !
  notes_*.txt    high-yield cloze notes: drop-down blanks with written distractors       ## / > / -
  sba_*.txt      single best answer questions with the 4-box explanation                @q
  arrows_*.txt   domino arrows with roles (primary, knock-on, compensation) and flips   @ar
  path_*.txt     inflow -> outflow mechanism chains                                     @path
  eponyms.txt    eponym decoder                                                         @ep
  gloss_us.txt   US abbreviations with the UK term                                      ABBR | meaning

Run: python3 step1/build_pack.py   (writes step1/pack.json and prints counts; any content error stops the build)
"""
import json, pathlib, re, sys, unicodedata

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / 'src'
OUT = HERE / 'pack.json'
ERR = []

# USMLE Step 1 content outline systems (usmle.org, 2026) with the share of the exam each takes
SYSTEMS = [
    ['repend', '🧪 Reproductive & endocrine · 12–16%'], ['resren', '🫘 Respiratory & renal · 11–15%'],
    ['neuro', '🧠 Behaviour, nerves & senses · 10–14%'], ['blood', '🩸 Blood & immune · 9–13%'],
    ['msk', '🦴 MSK, skin & connective tissue · 8–12%'], ['multi', '🧬 Multisystem processes · 8–12%'],
    ['cardio', '❤️ Cardiovascular · 7–11%'], ['gi', '🍽️ Gastrointestinal · 6–10%'],
    ['social', '🗣️ Communication & ethics · 6–9%'], ['biostat', '📊 Biostats & epidemiology · 4–6%'],
]
SEC_SYS = {'biochem': 'multi', 'immuno': 'blood', 'micro': 'multi', 'path': 'multi', 'pharm': 'multi',
           'pubhealth': 'biostat', 'cardio': 'cardio', 'endo': 'repend', 'gi': 'gi', 'heme': 'blood', 'msk': 'msk',
           'neuro': 'neuro', 'psych': 'neuro', 'renal': 'resren', 'repro': 'repend', 'resp': 'resren'}
SEC_ORDER = ['biochem', 'immuno', 'micro', 'path', 'pharm', 'pubhealth', 'cardio', 'endo', 'gi', 'heme', 'msk',
             'neuro', 'psych', 'renal', 'repro', 'resp']
PILOT = {'renal'}
LABELS = {"D": "Definition", "R": "Risk factors", "A": "Aetiology", "P": "Pathophysiology", "Ix": "Investigations",
          "Dx": "Diagnosis", "Mx": "Management", "DDx": "Differentials", "SE": "Side effects", "AE": "Adverse effects",
          "MOA": "Mechanism of action", "Cx": "Complications", "Causes": "Causes", "Features": "Features"}
PAT = {"L": "Lookalike", "N": "Number", "T": "Place, time or anatomy", "D": "Drug", "R": "Right rung"}
DASH = re.compile('[—]')            # em dash: never
ENDASH = re.compile('[–]')          # en dash: only inside lab ranges


def err(where, msg):
    ERR.append(where + ': ' + msg)


def norm(s):
    return re.sub(r'[^a-z0-9α-ω↑↓↔]+', '', unicodedata.normalize('NFKD', s.lower()).replace('**', ''))


def plain(s):
    return s.replace('**', '')


def rich_line(raw, where):
    """'text with **bold** and {{answer|d1|d2|d3}}' -> (text, bold spans, blanks). Offsets are code points, as cps() in the engine."""
    out, bolds, blanks, i, bstart = [], [], [], 0, None
    while i < len(raw):
        if raw.startswith('**', i):
            if bstart is None:
                bstart = len(out)
            else:
                if len(out) > bstart:
                    bolds.append([bstart, len(out)])
                bstart = None
            i += 2
        elif raw.startswith('{{', i):
            j = raw.find('}}', i)
            if j < 0:
                err(where, 'unclosed {{')
                break
            parts = [p.strip() for p in raw[i + 2:j].split('|')]
            ans, ds = parts[0], parts[1:]
            if len(ds) != 3:
                err(where, 'blank needs 3 distractors: ' + ans)
            dt, dn = [], []
            for d in ds[:3]:
                t, _, n = d.partition('~')
                dt.append(t.strip())
                dn.append(n.strip())
            if len({norm(x) for x in dt + [ans]}) != len(dt) + 1:
                err(where, 'distractor repeats the answer or another distractor: ' + ans)
            s0 = len(out)
            out.extend(ans)
            blanks.append([s0, len(out), 8, 0, 'custom', dt, dn])
            i = j + 2
        else:
            out.append(raw[i])
            i += 1
    if bstart is not None:
        err(where, 'unclosed **')
    return ''.join(out), bolds, blanks


# ---------------------------------------------------------------- topics and triggers
def parse_topics():
    secs, topics = [], []
    files = sorted(SRC.glob('topics_*.txt'))
    for f in files:
        sec = None
        for n, ln in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            where = f.name + ':' + str(n)
            if not ln.strip() or re.match(r'^# (medengine|Same format|Every topic|@ |# |! |Written)', ln):
                continue
            if DASH.search(ln):
                err(where, 'em dash')
            if ln.startswith('@ '):
                sid, name, fa = [x.strip() for x in ln[2:].split('|')]
                sec = {'id': sid, 'name': name, 'fa': fa}
                secs.append(sec)
            elif ln.startswith('# '):
                name, _, disc = ln[2:].partition('|')
                topics.append({'sec': sec['id'], 'name': name.strip(), 'disc': [d.strip() for d in disc.split(',') if d.strip()], 'rows': []})
            elif ln.startswith('! '):
                cue, _, lock = ln[2:].partition(' | ')
                if not lock or ln.count('**') % 2:
                    err(where, 'bad trigger row')
                topics[-1]['rows'].append([cue.strip(), lock.strip()])
            else:
                err(where, 'cannot read: ' + ln[:60])
    order = {s: i for i, s in enumerate(SEC_ORDER)}
    secs.sort(key=lambda s: order.get(s['id'], 99))
    names = [t['name'] for t in topics]
    for t in topics:
        if names.count(t['name']) > 1:
            err('topics', 'duplicate topic ' + t['name'])
        if len(t['rows']) < 2:
            err('topics', 'fewer than 2 triggers: ' + t['name'])
    topics.sort(key=lambda t: order.get(t['sec'], 99))   # stable: file order inside a section
    return secs, topics


def head_of(lock):
    """the part of a lock-in that becomes the blank: before the first colon if that is short enough, else all of it"""
    i = lock.find(':')
    return lock[:i].strip() if 0 < i <= 70 else lock.strip()


def trigger_topic(t, sec_rows):
    """every trigger row becomes a cloze line; distractors are the answers of neighbouring rows, each labelled with its own scene"""
    heads = [(plain(head_of(r[1])), r[0]) for r in t['rows']]
    blocks = []
    for k, (cue, lock) in enumerate(t['rows']):
        ans = plain(head_of(lock))
        sib = [h for j, h in enumerate(heads) if j != k]
        pool = sib + [h for h in sec_rows if h not in sib and h[0] != ans]
        seen, cand = {norm(ans)}, []
        for h, c in pool:
            nh = norm(h)
            if not nh or nh in seen or nh in norm(ans) or norm(ans) in nh:
                continue
            seen.add(nh)
            cand.append((h, c, pool.index((h, c)) >= len(sib)))
        L, W = len(ans), len(ans.split())
        cand.sort(key=lambda x: (x[2], abs(len(x[0]) - L) / 8 + abs(len(x[0].split()) - W)))
        picks = cand[:3]
        if len(picks) < 3:
            err(t['name'], 'not enough distractors for ' + ans)
            continue
        line_txt, bolds, _ = rich_line(cue + ' → ' + lock, t['name'])
        s0 = len(plain(cue)) + 3 + plain(lock).find(ans)
        if line_txt[s0:s0 + len(ans)] != ans:
            err(t['name'], 'blank offset for ' + ans)
            continue
        blank = [s0, s0 + len(ans), 8, 1, 'custom', [p[0] for p in picks], ['that one fits: ' + plain(p[1]) for p in picks]]
        blocks.append([[line_txt, 0, bolds, [blank]]])
    return {'h': t['name'] + ' · 🧲 triggers', 'b': blocks}


# ---------------------------------------------------------------- cloze notes
def parse_notes():
    out = {}
    for f in sorted(SRC.glob('notes_*.txt')):
        cur = blk = None
        for n, ln in enumerate(f.read_text(encoding='utf-8').splitlines(), 1):
            where = f.name + ':' + str(n)
            if not ln.strip() or ln.startswith('#!'):
                continue
            if DASH.search(ln):
                err(where, 'em dash')
            if ln.startswith('## '):
                name, _, sub = ln[3:].partition(' | ')
                cur = {'h': (sub or name).strip(), 'b': []}
                out.setdefault(name.strip(), []).append(cur)
                blk = None
                continue
            m = re.match(r'^(\s*)([>-])\s+(.*)$', ln)
            if not m or cur is None:
                err(where, 'cannot read: ' + ln[:60])
                continue
            ind, kind, body = m.groups()
            if kind == '>' or blk is None:
                blk = []
                cur['b'].append(blk)
            pre = '' if kind == '>' else ('- ' if ind else '• ')
            text, bolds, blanks = rich_line(pre + body, where)
            blk.append([text, 1 if ind else 0, bolds, blanks])
    # blank density: the first blank of each block is level 1, the first of every other line 2, the rest 3
    for name, tops in out.items():
        for top in tops:
            for blk in top['b']:
                first = True
                for line in blk:
                    for ci, c in enumerate(line[3]):
                        c[3] = 1 if first else 2 if ci == 0 else 3
                        first = False
    return out


# ---------------------------------------------------------------- questions
def natkey(s):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r'(\d+)', s)]


def blocks_of(text, head):
    out, cur = [], None
    for raw in text.splitlines():
        ln = raw.strip()
        if not ln or ln.startswith('#'):
            continue
        m = re.match(r'^@' + head + r'\s+(.*)$', ln)
        if m:
            cur = {'head': m.group(1), 'lines': []}
            out.append(cur)
        elif cur is not None:
            cur['lines'].append(ln)
    return out


def cue_re(c):
    return re.compile(re.escape(c.strip()).replace(r'\ ', r'\s+'), re.I)


ABS = re.compile(r'\b(always|never|only|all|none)\b', re.I)


def parse_sba(unit_of):
    qs = []
    for f in sorted(SRC.glob('sba_*.txt')):
        for b in blocks_of(f.read_text(encoding='utf-8'), 'q'):
            topic, _, hp = [x.strip() for x in b['head'].partition('|')]
            where = f.name + ' ' + topic + ' #' + str(len(qs) + 1)
            it = {'lab': [], 'c': [], 'f': [], 'x': []}
            for ln in b['lines']:
                if ln.startswith('$'):
                    it['lab'].append(([p.strip() for p in ln[1:].split(';')] + ['', ''])[:3])
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
                    if not m:
                        err(where, 'cannot read: ' + ln[:50])
                        continue
                    k, v = m.groups()
                    if k == 's':
                        it['s'] = v.replace(' // ', '\n')
                    elif k == 'c':
                        it['c'] += [x.strip() for x in v.split('|') if x.strip()]
                    elif k in 'mg':
                        it[k] = v
                    else:
                        a, _, t = v.partition('=>')
                        it[k].append([a.strip(), t.strip()])
            need = [k for k in ('s', 'ql', 'o', 'w', 'ff', 'm', 'g') if not it.get(k)]
            if need:
                err(where, 'missing ' + ', '.join(need))
                continue
            if topic not in unit_of:
                err(where, 'unknown topic')
                continue
            raw = it['o']
            ans = [o.lstrip('*').strip() for o in raw if o.startswith('*')]
            names = sorted([o.lstrip('*').strip() for o in raw], key=natkey)
            if len(raw) != 5 or len(ans) != 1 or len(set(map(norm, names))) != 5:
                err(where, '5 different options with one * answer')
                continue
            a = names.index(ans[0])
            q = {'id': 's%04d' % (len(qs) + 1), 't': 'u', 'k': str(unit_of[topic]), 'h': int(hp[0]), 'p': hp[1],
                 's': it['s'], 'o': names, 'a': a, 'w': it['w'], 'f': it['ff'], 'ql': it['ql'], 'post': ''}
            if it['lab']:
                q['lab'] = it['lab']
            if hp[1] not in PAT or not 1 <= int(hp[0]) <= 3:
                err(where, 'head needs 1-3 and one of ' + ''.join(PAT))
            # every field: no em dash; en dash only in lab ranges
            for t in [q['s'], q['ql'], q['w'], q['f'], it['m'], it['g']] + names + [c for c in it['c']] + [x[1] for x in it['f'] + it['x']] + [r[0] + r[1] for r in it['lab']]:
                if DASH.search(t) or ENDASH.search(t):
                    err(where, 'dash in ' + t[:40])
            words = len(re.findall(r"[A-Za-z0-9']+", q['s']))
            if not 35 <= words <= 120:
                err(where, 'stem is %d words (aim for 40 to 100)' % words)
            if not re.match(r'^An? ', q['s']):
                err(where, 'stem should open "A ..." or "An ..." (who the patient is)')
            pool = ' '.join([q['s'], q['ql']] + [r[0] + ' ' + r[1] for r in it['lab']])
            if len(it['c']) < 2:
                err(where, 'needs 2 or more red-flag cues')
            for c in it['c']:
                if not cue_re(c).search(pool):
                    err(where, 'cue not in the stem: ' + c)
            nm = [norm(o) for o in names]
            fl, xs = [], []
            for cond, opt in it['f']:
                if norm(opt) not in nm:
                    err(where, 'flip names no option: ' + opt)
                    continue
                fl.append([cond, nm.index(norm(opt))])
            for opt, why in it['x']:
                if norm(opt) not in nm:
                    err(where, 'why-not names no option: ' + opt)
                    continue
                xs.append([nm.index(norm(opt)), why])
            wrong = [i for i in range(5) if i != a]
            if sorted(i for _, i in fl) != wrong:
                err(where, 'needs one 🔀 flip for each of the 4 wrong options')
            if sorted(i for i, _ in xs) != wrong:
                err(where, 'needs one why-not for each of the 4 wrong options')
            longest = max(len(names[i]) for i in wrong)
            if len(names[a]) > 1.7 * longest + 12:
                err(where, 'answer is much longer than every distractor')
            if ABS.search(names[a]) is None and any(ABS.search(names[i]) for i in wrong):
                err(where, 'absolute word in a distractor only')
            q['tm'] = {'c': it['c'], 'm': it['m'], 'g': it['g'], 'f': sorted(fl, key=lambda x: x[1]), 'x': sorted(xs)}
            qs.append(q)
    return qs


# ---------------------------------------------------------------- arrows, mechanisms, eponyms, glossary
def parse_vars(v, where):
    out, roles = [], ''
    for part in v.split(' ; '):
        m = re.match(r'^(.+?)\s*=\s*([↑↓↔]+)\s*([pkc-])?$', part.strip())
        if not m:
            err(where, 'arrow row: ' + part)
            continue
        out.append([m.group(1).strip(), m.group(2)])
        roles += m.group(3) or '-'
    return out, (roles if roles.strip('-') else '')


def parse_arrows(unit_of):
    ars = []
    for f in sorted(SRC.glob('arrows_*.txt')):
        for b in blocks_of(f.read_text(encoding='utf-8'), 'ar'):
            aid, _, fam = [x.strip() for x in b['head'].partition('|')]
            where = f.name + ' ' + aid
            a = {'id': 's1-' + aid, 'f': fam, 'u': [], 'm': [], 'uk': '', 'fl': []}
            cur = a
            for ln in b['lines']:
                if ln.startswith('>>'):
                    cur = {'t': ln[2:].strip(), 'm': []}
                    a['fl'].append(cur)
                    continue
                m = re.match(r'^(u|s|v|k|m|uk):\s*(.*)$', ln)
                if not m:
                    err(where, 'cannot read: ' + ln[:50])
                    continue
                k, val = m.groups()
                if DASH.search(val):
                    err(where, 'em dash')
                if k == 'u':
                    for t in val.split(' ; '):
                        if t.strip() in unit_of:
                            a['u'].append(unit_of[t.strip()])
                        else:
                            err(where, 'unknown topic ' + t)
                elif k == 'v':
                    cur['v'], r = parse_vars(val, where)
                    if r:
                        cur['r'] = r
                elif k == 'm':
                    cur['m'] = [x.strip() for x in val.split(' // ')]
                else:
                    cur[k] = val
            for x in [a] + a['fl']:
                if not x.get('s') or not x.get('v') or not x.get('k'):
                    err(where, 'arrow needs s, v and k')
            if not a['u']:
                err(where, 'arrow needs a topic')
            ars.append(a)
    return ars


def parse_path(unit_of):
    out = []
    for f in sorted(SRC.glob('path_*.txt')):
        for b in blocks_of(f.read_text(encoding='utf-8'), 'path'):
            pid, _, title = [x.strip() for x in b['head'].partition('|')]
            p = {'id': 's1-' + pid, 't': title, 'l': [], 'u': []}
            for ln in b['lines']:
                if ln.startswith('u:'):
                    for t in ln[2:].split(' ; '):
                        if t.strip() in unit_of:
                            p['u'].append(unit_of[t.strip()])
                        else:
                            err(f.name + ' ' + pid, 'unknown topic ' + t)
                elif ln.startswith('- '):
                    p['l'].append(ln[2:].strip())
                else:
                    err(f.name + ' ' + pid, 'cannot read: ' + ln[:50])
            if len(p['l']) < 2 or not p['u']:
                err(f.name + ' ' + pid, 'needs 2+ chain lines and a topic')
            out.append(p)
    return out


def parse_eponyms(unit_of):
    out = []
    f = SRC / 'eponyms.txt'
    if not f.exists():
        return out
    for b in blocks_of(f.read_text(encoding='utf-8'), 'ep'):
        t, _, al = [x.strip() for x in b['head'].partition('|')]
        e = {'t': t, 'al': [x.strip() for x in al.split(';') if x.strip()], 'u': []}
        for ln in b['lines']:
            m = re.match(r'^(f|h|x|m|u):\s*(.*)$', ln)
            if not m:
                err('eponyms ' + t, 'cannot read: ' + ln[:50])
                continue
            k, v = m.groups()
            if DASH.search(v):
                err('eponyms ' + t, 'em dash')
            if k == 'u':
                for x in v.split(' ; '):
                    if x.strip() in unit_of:
                        e['u'].append(unit_of[x.strip()])
                    else:
                        err('eponyms ' + t, 'unknown topic ' + x)
            else:
                e[k] = v
        if not all(e.get(k) for k in 'fhxm'):
            err('eponyms ' + t, 'needs f, h, x and m')
        out.append(e)
    return out


def parse_gloss():
    f = SRC / 'gloss_us.txt'
    out = []
    if f.exists():
        for ln in f.read_text(encoding='utf-8').splitlines():
            if ln.strip() and not ln.startswith('#'):
                a, _, b = ln.partition(' | ')
                if not b:
                    err('gloss', ln)
                out.append([a.strip(), b.strip()])
    return out


# ---------------------------------------------------------------- assemble
def build():
    secs, topics = parse_topics()
    unit_of = {t['name']: i for i, t in enumerate(topics)}
    notes = parse_notes()
    for name in notes:
        if name not in unit_of:
            err('notes', 'unknown topic ' + name)
    pages, units, hunt, star = [], [], [], {}
    for si, s in enumerate(secs):
        ts = [(i, t) for i, t in enumerate(topics) if t['sec'] == s['id']]
        sec_rows = [(plain(head_of(r[1])), r[0]) for _, t in ts for r in t['rows']]
        page = {'n': si + 1, 'code': s['fa'], 'ch': s['id'], 'title': s['name'], 'topics': [], 'sup': 0, 'src': 'step1'}
        for i, t in ts:
            refs = []
            for top in notes.get(t['name'], []):
                refs.append([page['n'], len(page['topics'])])
                page['topics'].append(top)
            refs.append([page['n'], len(page['topics'])])
            page['topics'].append(trigger_topic(t, sec_rows))
            star[str(i)] = t['rows'][0]
            ids = []
            for cue, lock in t['rows'][1:]:
                ids.append(len(hunt))
                hunt.append(['?', cue, lock, 'H'])
            sysid = 'social' if 'ethics' in t['disc'] else SEC_SYS.get(s['id'], 'multi')
            units.append({'w': s['id'], 'name': t['name'], 'refs': refs, 'note': '', 'sup': 0, 'hunt': ids, 'ar': [], 'cs': [],
                          'pa': [], 'ck': [], 'acts': [], 'act': '', 'ix1': '', 'disc': t['disc'], 'sys': sysid,
                          'pilot': 1 if s['id'] in PILOT else 0})
        pages.append(page)
    ars = parse_arrows(unit_of)
    for ai, a in enumerate(ars):
        for u in a['u']:
            units[u]['ar'].append(ai)
    paths = parse_path(unit_of)
    for pi, p in enumerate(paths):
        for u in p['u']:
            units[u]['pa'].append(pi)
    qs = parse_sba(unit_of)
    jg = parse_eponyms(unit_of)
    gloss = parse_gloss()
    if ERR:
        print('\n'.join(ERR[:80]), file=sys.stderr)
        print('%d content errors' % len(ERR), file=sys.stderr)
        sys.exit(1)
    used = {u['sys'] for u in units}
    D = {'pages': pages, 'pools': {}, 'gloss': gloss, 'weeks': [{'id': s['id'], 'name': s['name']} for s in secs],
         'units': units, 'labels': LABELS, 'src': {}, 'fw': [], 'why': [], 'hunt': hunt, 'ar': ars, 'key': [], 'cases': [],
         'path': paths, 'upd': {}, 'jg': jg, 'spdl': {}, 'act': [], 'snap': {}, 'master': [], 'hst': {},
         'trg': {'c': star, 'bug': {}, 'sc': [], 'dr': [], 'ix': [], 'mx': []},
         'hq': {'q': qs, 'tt': {}, 'pat': PAT, 'al': {}}, 'mock': {'q': []}, 'off': {'pp': {}, 'q': [], 'img': {}, 'g': []},
         'dgu': {}, 's1': {'sys': [s for s in SYSTEMS if s[0] in used], 'pilot': sorted(PILOT)}}
    OUT.write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    blanks = sum(len(l[3]) for p in pages for t in p['topics'] for b in t['b'] for l in b)
    print(json.dumps({'sections': len(secs), 'topics': len(units), 'trigger_rows': sum(len(t['rows']) for t in topics),
                      'note_topics': sum(len(v) for v in notes.values()), 'blanks': blanks, 'sba': len(qs), 'arrows': len(ars),
                      'flips': sum(len(a['fl']) for a in ars), 'mechanisms': len(paths), 'eponyms': len(jg), 'gloss': len(gloss),
                      'kb': round(OUT.stat().st_size / 1024)}))
    return D


if __name__ == '__main__':
    build()
