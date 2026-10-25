"""medengine-OSCE v1.3 content helpers. All content in these files is written in our own words from UK guidance
(NICE, BNF, Resuscitation Council UK, DVLA, GMC). Item strings use a tiny format:
    '!what you do || what you say || why it scores'
A leading ! marks a critical item. The say and why parts are optional."""

STATIONS = []


def item(s):
    w = 2 if s.startswith('!') else 1
    s = s.lstrip('!').strip()
    parts = [p.strip() for p in s.split('||')]
    it = {'t': parts[0]}
    if len(parts) > 1 and parts[1]: it['say'] = parts[1]
    if len(parts) > 2 and parts[2]: it['why'] = parts[2]
    if w == 2: it['w'] = 2
    return it


def mksecs(spec):
    return [{'h': h, 'items': [item(x) for x in xs]} for h, xs in spec]


def station(id, type, t, grp, secs=(), hooks=(), money='', traps=(), dg=(), cases=(), vars=(), ask=(), door='', task='',
            u=(), ffp='', wrap=None, talk=None):
    st = {'id': id, 'type': type, 't': t, 'grp': grp, 'secs': mksecs(secs), 'hooks': list(hooks), 'money': money,
          'traps': list(traps), 'dg': list(dg), 'u': list(u), 'info': door, 'task': task, 'ffp': ffp}
    if cases: st['cases'] = [{'dx': c[0], 'f': c[1], 'p': c[2]} for c in cases]
    if vars: st['vars'] = [dict(v) for v in vars]
    if ask: st['ask'] = list(ask)
    if wrap: st['wrap'] = wrap
    STATIONS.append(st)
    return st


def V(k, who, dx, a, r, x, d=None, img=None):
    v = {'k': k, 'who': who, 'dx': dx, 'a': list(a), 'r': r, 'x': x}
    if d: v['d'] = d
    if img: v['img'] = img
    return v
