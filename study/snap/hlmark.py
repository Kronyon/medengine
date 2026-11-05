"""🧲 Triggers: highlights and stacks for the 1,975 word-hunt clues (hl_*.py, one file per ILO system).
Each file holds MARKS, a text block:
    # Stack label            starts a stack: the shared scene, like High-Yield's left column
    123: phrase; phrase      hunt 123: highlight these exact phrases in its clue (the words that flip the answer)
    123: =                   keep the highlight the clue already has
    123: phrase >> new answer   also replace the answer (used to correct an answer to current UK guidance)
apply(D) checks every clue in every unit is covered once, in contiguous stacks, every phrase is found, then writes the
** marks into D['hunt'] and the stacks into D['hst'] = {unit: [[label, [hunt ids]], ...]}."""
import glob, importlib, pathlib, re

HERE = pathlib.Path(__file__).resolve().parent


def parse(text, src):
    stacks, cur, err = [], None, []
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line: continue
        if line.startswith('#'):
            cur = [line.lstrip('#').strip(), []]; stacks.append(cur); continue
        m = re.match(r'^(\d+)\s*:\s*(.*)$', line)
        if not m: err.append(f'{src}:{n}: cannot read "{line[:50]}"'); continue
        if cur is None: err.append(f'{src}:{n}: line before any # stack'); continue
        cur[1].append((int(m.group(1)), m.group(2).strip()))
    return stacks, err


def mark(clue, spec):
    plain = clue.replace('**', '')
    if spec == '=':
        if '**' not in clue: return None, 'keeps a highlight it does not have'
        return clue, ''
    phrases = [p.strip() for p in spec.split(';') if p.strip()]
    if not phrases: return None, 'no phrase'
    spans = []
    for p in phrases:
        i = plain.find(p)
        if i < 0: return None, f'phrase not found: "{p}"'
        spans.append((i, i + len(p)))
    spans.sort()
    for a, b in zip(spans, spans[1:]):
        if b[0] < a[1]: return None, 'phrases overlap'
    out, j = '', 0
    for a, b in spans: out += plain[j:a] + '**' + plain[a:b] + '**'; j = b
    return out + plain[j:], ''


def apply(D):
    H, U = D['hunt'], D['units']
    owner = {}
    for ui, u in enumerate(U):
        for h in u.get('hunt', []): owner.setdefault(h, ui)
    files = sorted(glob.glob(str(HERE / 'hl_*.py')))
    err, done, hst, fixes = [], {}, {}, {}
    for f in files:
        mod = importlib.import_module(pathlib.Path(f).stem)
        stacks, e = parse(mod.MARKS, pathlib.Path(f).name); err += e
        for label, items in stacks:
            if len({owner.get(h) for h, _ in items}) > 1: err.append(f'{pathlib.Path(f).name}: stack "{label}" spans two conditions: add a # line')
            if not label: err.append(f'{f}: empty stack label')
            if len(label) > 40: err.append(f'stack label too long: {label}')
            if re.search(r'[()\[\]—–]', label): err.append(f'stack label has bracket or dash: {label}')
            for hid, spec in items:
                spec, _, newans = spec.partition(' >> ')
                if newans:
                    if re.search(r'[()\[\]—–]', newans): err.append(f'hunt {hid}: new answer has a bracket or dash')
                    fixes[hid] = newans.strip()
                if hid in done: err.append(f'hunt {hid} marked twice'); continue
                if hid >= len(H): err.append(f'hunt {hid} does not exist'); continue
                new, why = mark(H[hid][1], spec)
                if why: err.append(f'hunt {hid}: {why}'); continue
                done[hid] = new
                ui = owner[hid]; st = hst.setdefault(ui, [])
                if st and st[-1][0] == label and st[-1][2] == f: st[-1][1].append(hid)
                else: st.append([label, [hid], f])
    for ui, st in hst.items():
        labels = [s[0] for s in st]
        if len(labels) != len(set(labels)): err.append(f'unit {ui} {U[ui]["name"]}: a stack is split in two: {labels}')
    if files:
        miss = [h for h in range(len(H)) if h not in done]
        if miss: err.append(f'{len(miss)} clues not marked, e.g. {miss[:8]}')
    if err: raise SystemExit('highlight errors:\n  ' + '\n  '.join(err[:40]))
    for hid, new in done.items(): H[hid][1] = new
    for hid, ans in fixes.items(): H[hid][2] = ans
    D['hst'] = {str(ui): [[s[0], s[1]] for s in st] for ui, st in sorted(hst.items())}
    return len(done)
