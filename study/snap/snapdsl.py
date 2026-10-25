"""Tiny writer for 🎞️ snapshots: one call per ILO condition. Own words, UK guidance.
Lists use ';' between items and '>' between a label and its location, finding or urgency.
A piece starting with a lower-case letter is glued back onto the item before it, so a finding may contain a semicolon."""
SNAP = {}
ERR = []


def _parts(s, sep, tail=True):
    """tail=True: the separator ends each item, so a piece without it joins the next piece.
    tail=False: the separator sits mid-item; a lower-case piece without it continues the item before."""
    out, buf = [], ''
    for p in s.split(';'):
        q = p.strip()
        if not q: continue
        if sep in q:
            out.append((buf + '; ' + q) if buf else q); buf = ''
        elif tail: buf = (buf + '; ' + q) if buf else q
        elif out and q[:1].islower(): out[-1] += '; ' + q
        else: out.append(q)
    if buf: out.append(buf)
    return out


def N(units, n, o, r, m, w, s, x, t, d, h, k=None):
    if isinstance(units, int): units = [units]
    e = {'n': n, 'o': o, 'r': r, 'm': m, 'w': w,
         's': [[a.strip(), b.strip()] for a, b in (p.rsplit('>', 1) for p in _parts(s, '>'))],
         'x': [], 't': [p.strip() for p in t.split('|') if p.strip()],
         'd': [[a.strip(), b.strip()] for a, b in (p.rsplit('>', 1) for p in _parts(d, '>'))], 'h': h}
    for p in _parts(x, '>', False):
        a, b = p.split('>', 1) if '>' in p else (p, '')
        g = b.strip().endswith('*') or a.strip().endswith('*')
        e['x'].append([a.strip().rstrip('*').strip(), b.strip().rstrip('*').strip()] + ([1] if g else []))
    if not (len(e['s']) <= 5 and len(e['x']) <= 4 and len(e['t']) <= 4 and len(e['d']) <= 4): ERR.append('too many items: %s s%d x%d t%d d%d' % (n, len(e['s']), len(e['x']), len(e['t']), len(e['d'])))
    import json as _j
    if '\u2014' in _j.dumps(e, ensure_ascii=False) or '(' in _j.dumps(e, ensure_ascii=False): ERR.append('em dash or bracket in ' + n)
    if k: e['k'] = k
    for u in units:
        assert u not in SNAP, 'duplicate snapshot for unit %d' % u
        SNAP[u] = e
    return e
