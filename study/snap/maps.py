"""⚡ Thought maps: cue → mechanism → decisive gate → answer, with 🔀 flips to the runner-up options.

Source: study/snap/maps/m*.txt, one block per question:

    @o-mla1-006
    c: metal mitral valve | INR is 5.1 | no signs of bleeding
    m: Too much warfarin raises bleeding risk, but nothing is bleeding yet
    g: INR 5 to 8 with no bleeding
    f: INR over 8, still no bleeding => Give vitamin K orally
    f: Any major bleed, whatever the INR => Give vitamin K intravenously

c  the cues, each copied word for word from the stem, lead-in or a results row ("Ferritin 9 µg/L")
m  the mechanism in one line
g  the threshold or fact that decides between the options
f  a one-feature change => the exact text of the option it would make right (2 or 3 lines)

apply(D) attaches q['tm'] = {'c': [...], 'm': str, 'g': str, 'f': [[condition, option index], ...]}.
It runs after mscaa.apply, so option indices are the final, alphabetised ones.
"""
import pathlib, re

HERE = pathlib.Path(__file__).resolve().parent
MAPS = HERE / 'maps'


def parse():
    out, cur = {}, None
    for f in sorted(MAPS.glob('m*.txt')):
        for ln in f.read_text(encoding='utf-8').splitlines():
            ln = ln.rstrip()
            if not ln or ln.startswith('#'):
                continue
            if ln.startswith('@'):
                cur = out.setdefault(ln[1:].strip(), {'c': [], 'm': '', 'g': '', 'f': [], 'src': f.name})
                continue
            m = re.match(r'^([cmgf]):\s*(.*)$', ln)
            if not m or cur is None:
                raise ValueError(f'{f.name}: bad line {ln!r}')
            k, v = m.groups()
            if k == 'c':
                cur['c'] += [x.strip() for x in v.split('|') if x.strip()]
            elif k == 'f':
                a, _, b = v.partition('=>')
                cur['f'].append([a.strip(), b.strip()])
            else:
                cur[k] = v.strip()
    return out


def norm(s):
    return re.sub(r'\s+', ' ', s.replace(' ', ' ')).strip().lower()


def haystack(q):
    rows = [norm(r[0] + ' ' + r[1]) for r in q.get('lab') or []]
    return norm(' '.join([q.get('s', ''), q.get('post', ''), q.get('ql', '')])), rows


def problems(q, mp):
    """Everything wrong with one map, as a list of strings."""
    bad = []
    text, rows = haystack(q)
    if not 1 <= len(mp['c']) <= 5:
        bad.append('needs 1 to 5 cues')
    for c in mp['c']:
        n = norm(c)
        if n not in text and not any(n in r for r in rows):
            bad.append('cue not in stem: ' + c)
    if not mp['m'] or not mp['g']:
        bad.append('missing mechanism or gate')
    if len(mp['f']) > 3:
        bad.append('at most 3 flips')
    opts = [norm(o) for o in q['o']]
    for cond, tgt in mp['f']:
        if norm(tgt) not in opts:
            bad.append('flip target is not an option: ' + tgt)
        elif opts.index(norm(tgt)) == q['a']:
            bad.append('flip points at the right answer: ' + tgt)
        if not cond:
            bad.append('empty flip condition')
    for s in [mp['m'], mp['g']] + [f[0] for f in mp['f']]:
        if re.search(r'[—–]', s) or re.search(r'\((?![\d<>.])', s):
            bad.append('dash or bracket in: ' + s[:40])
    return bad


def apply(D, strict=False):
    M = parse()
    items = {q['id']: q for k in ('hq', 'mock', 'off') for q in D[k]['q']}
    errs = []
    for qid, mp in M.items():
        q = items.get(qid)
        if not q:
            errs.append(qid + ': no such question')
            continue
        bad = problems(q, mp)
        if bad:
            errs += [qid + ': ' + b for b in bad]
            continue
        opts = [norm(o) for o in q['o']]
        q['tm'] = {'c': mp['c'], 'm': mp['m'], 'g': mp['g'], 'f': [[c, opts.index(norm(t))] for c, t in mp['f']]}
    if errs and strict:
        raise SystemExit('thought maps:\n' + '\n'.join(errs[:60]))
    return M, errs


if __name__ == '__main__':
    import json, sys
    page = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / 'medengine-study.html').read_text(encoding='utf-8')
    D = json.loads(re.search(r'<script id="qqdata" type="application/json">(.*?)</script>', page, re.S).group(1))
    for k in ('hq', 'mock', 'off'):
        for q in D[k]['q']:
            q.pop('tm', None)
    M, errs = apply(D)
    tot = sum(len(D[k]['q']) for k in ('hq', 'mock', 'off'))
    print(f'{len(M)} maps for {tot} questions; {len(errs)} problems')
    print('\n'.join(errs[:80]))
