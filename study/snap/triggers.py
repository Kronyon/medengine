"""🧲 Triggers: joins t_cond, t_bugs and t_drugs into D['trg'] and lints them (no brackets, no em dashes, British spelling,
one '|' per line, short lines, balanced bold). check(units, ilo_text) also reports ILO bugs and drugs with no trigger."""
import re
from t_cond import COND
from t_bugs import BUG, SCENES
from t_drugs import DRUGS
from t_ix import IX
from t_mx import MX

US = [r'\bcolors?\b', r'\banemi', r'\besophag', r'\bpediatric', r'\bhemoglobin', r'\bbehavior', r'\bcenter\b',
      r'\bedema', r'\bleukocyt', r'\bfetus\b', r'\btumor\b', r'\bdiarrhea', r'\bhematuria', r'\bischemi', r'\bestrogen']
PICS = {'pill', 'inh', 'iv', 'inj', 'cream', 'drop', 'patch', 'spray', 'proc'}
IXPICS = {'score', 'lab', 'xray', 'ct', 'mri', 'us', 'scope', 'ecg', 'bed'}
MXPICS = {'cut', 'needle', 'drain', 'shock', 'device', 'scope', 'laser', 'ray', 'air', 'bag', 'talk', 'law', 'bed', 'cream'}
MORPH = {'gpc_cl', 'gpc_ch', 'gpc_pr', 'gnc', 'gncb', 'gnr', 'gncv', 'gpr', 'gprs', 'gpbr', 'afb', 'spiro', 'nowall', 'intra',
         'venv', 'vnak', 'yeast', 'yeastc', 'mould', 'proto', 'mite', 'louse', 'worm'}


def lint(where, s, clue_max=150, ans_max=120):
    err = []
    if re.search(r'[()\[\]—–]', s): err.append(f'{where}: bracket or dash')
    for w in US:
        if re.search(w, s, re.I): err.append(f'{where}: US spelling {w}')
    if s.count('**') % 2: err.append(f'{where}: unbalanced bold')
    if '|' in s:
        if s.count('|') != 1: err.append(f'{where}: needs exactly one |')
        c, a = [x.strip() for x in s.split('|')]
        if not c or not a: err.append(f'{where}: empty side')
        if len(c.replace('**', '')) > clue_max: err.append(f'{where}: clue too long')
        if len(a.replace('**', '')) > ans_max: err.append(f'{where}: answer too long')
    return err


def split(s):
    c, a = s.split('|'); return [c.strip(), a.strip()]


def build(n_units):
    err = []
    miss = [i for i in range(n_units) if i not in COND]
    if miss: err.append(f'units without a ⭐ trigger: {miss}')
    for k, s in COND.items():
        if '|' not in s: err.append(f'cond {k}: no |')
        err += lint(f'cond {k}', s)
    used = set()
    for title, ic, lines in SCENES:
        for key, s in lines:
            if key not in BUG: err.append(f'scene {title}: unknown bug {key}')
            used.add(key); err += lint(f'bug {key}', s)
            if '|' not in s: err.append(f'bug {key}: no |')
    for k, (n, al, m) in BUG.items():
        if m not in MORPH: err.append(f'bug {k}: picture {m}')
        if k not in used: err.append(f'bug {k} has no trigger line')
        err += lint(f'bug name {k}', n + ' ' + al)
    names = set()
    for title, ic, items in DRUGS + IX + MX:
        for name, pic, use, cats in items:
            if pic not in PICS | IXPICS | MXPICS: err.append(f'drug {name}: picture {pic}')
            if name in names: err.append(f'drug {name}: duplicate')
            names.add(name)
            err += lint(f'drug {name}', name + ' ' + use, clue_max=150)
            if '|' in use: err.append(f'drug {name}: use line must not contain |')
            if not cats: err.append(f'drug {name}: no catch')
            for c in cats:
                if '|' not in c: err.append(f'drug {name}: catch has no |')
                err += lint(f'drug {name} catch', c)
    if err: raise SystemExit('trigger errors:\n  ' + '\n  '.join(err[:40]))
    return {
        'c': {str(k): split(v) for k, v in sorted(COND.items())},
        'bug': {k: list(v) for k, v in BUG.items()},
        'sc': [[t, ic, [[k] + split(s) for k, s in lines]] for t, ic, lines in SCENES],
        'dr': [[t, ic, [[n, p, u, [split(c) for c in cs]] for n, p, u, cs in items]] for t, ic, items in DRUGS],
        'ix': [[t, ic, [[n, p, u, [split(c) for c in cs]] for n, p, u, cs in items]] for t, ic, items in IX],
        'mx': [[t, ic, [[n, p, u, [split(c) for c in cs]] for n, p, u, cs in items]] for t, ic, items in MX],
    }


def count(T):
    return len(T['c']) + sum(len(x[2]) for x in T['sc']) + sum(1 + len(d[3]) for g in T['dr'] + T['ix'] + T['mx'] for d in g[2])
