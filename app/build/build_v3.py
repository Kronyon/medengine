"""OSCE app v2 data build.

Inputs
  src/osce_data.json        v1 data recovered from the published page
  src/drill_ck.json         clinchers per ILO unit, from the Drill
  content/frames_why.txt    why-lines (and missing say-lines) for every frame item
  content/pp*.txt           past-paper stations

Past-paper file syntax (one station per @ block):
  @ID | Title
  src: sources            u: unit idxs        fr: frames     ex: exam ids   pr: procedure ids
  door: candidate brief
  trig: / hook: / trap:   (repeatable)
  clinch: ✅|❌|🧪 text    (repeatable)
  money: the one sentence that scores
  var: K | who | diagnosis      then  a: actor line (repeatable)  r: results  x: examiner answer
  ask: q1 | q2               (actor's planted questions)
  dom: Domain | item; item; !critical item
  s: Section | say | why     or  s[K]: ... for variant K only
"""
import json, re, glob, sys, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(f'{ROOT}/src/osce_data.json'))
CK = json.load(open(f'{ROOT}/src/drill_ck.json'))['ck']

# ---------- 1. prune and repair the bank ----------
KEEP_WD = {'WD02': [126], 'WD04': [51], 'WD05': [111], 'WD06': [10]}
UFIX = {
    'CV01': [0], 'RE12': [23], 'GI06': [29], 'NE18': [98], 'NE19': [99], 'UR08': [75], 'OA05': [86],
    'DE22': [128], 'EN17': [74, 151], 'EN19': [151], 'EX02': [9, 16, 19], 'EX03': [49, 41], 'EX08': [99],
    'EX09': [141], 'EX22': [86], 'EX28': [151], 'EX34': [166], 'PC01': [0, 3], 'PC07': [67], 'PC08': [67],
    'PC09': [67], 'PC10': [85], 'PC18': [33], 'DI23': [99], 'DI34': [13], 'CX12': [138], 'PRF21': [102],
    'RP02': [83], 'WD02': [126], 'WD04': [51], 'WD05': [111], 'WD06': [10],
}
EXFIX = {'CV06': ['cvs'], 'EX28': ['ent'], 'PC09': []}
PRFIX = {'PC09': ['ivinj']}
st = []
for s in D['stations']:
    if s['g'] == 'WD' and s['id'] not in KEEP_WD:
        continue
    if s['id'] in UFIX and not s['u']:
        s['u'] = UFIX[s['id']]
    if s['id'] in KEEP_WD:
        s['u'] = KEEP_WD[s['id']]
        s['g'] = {'WD02': 'DE', 'WD04': 'DI', 'WD05': 'MH', 'WD06': 'PC'}[s['id']]
    if s['id'] in EXFIX:
        s['ex'] = EXFIX[s['id']]
    if s['id'] in PRFIX and any(p['id'] == PRFIX[s['id']][0] for p in D['dops']):
        s['pr'] = PRFIX[s['id']]
    st.append(s)
dropped = len(D['stations']) - len(st)
D['groups'].pop('WD', None)

# ---------- 2. frame why-lines ----------
fw = {}
for ln in open(f'{ROOT}/content/frames_why.txt', encoding='utf8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'):
        continue
    key, say, why = [x.strip() for x in ln.split('|', 2)]
    fw[key] = (say, why)
miss = []
for k, f in D['frames'].items():
    n = 0
    for sec in f['secs']:
        for it in sec['items']:
            key = f'{k}.{n}'
            if key in fw:
                say, why = fw[key]
                if say and not it.get('say'):
                    it['say'] = say
                it['why'] = why
            else:
                miss.append(key)
            n += 1
if miss:
    print('frame items without why:', miss)

# ---------- 3. clinchers into packs ----------
nck = 0
for i, p in D['packs'].items():
    ck = CK.get(str(i)) or CK.get(i) or []
    if ck:
        p['ck'] = ck
        nck += len(ck)

# ---------- 4. past-paper stations ----------
KIND = {'✅': 'in', '❌': 'out', '🧪': 'lab'}
def kind_for(fr):
    if 'presc' in fr: return 'Prescription task'
    if 'acute' in fr: return 'Focused clinical task (A–E)'
    if 'ex' in fr: return 'Examination and findings'
    if 'proc' in fr: return 'Practical task and completion'
    if fr and fr[0] in ('expl', 'counsel', 'bbn'): return 'Explanation and shared plan'
    if 'prof' in fr: return 'Professional decision'
    if 'di' in fr and 'hx' not in fr and 'mhx' not in fr: return 'Results interpretation'
    return 'Focused clinical task'

pp, errs, conts = [], [], []
def blank(sid, title):
    return {'id': sid, 'g': 'PP', 'pp': 1, 'add': False, 't': title, 'src': '', 'u': [], 'fr': [], 'ex': [], 'pr': [],
            'info': '', 'task': '', 'trig': [], 'hook': [], 'clinch': [], 'money': '', 'trap': [], 'vars': [], 'ask': [],
            'dom': [], 'script': []}
for path in sorted(glob.glob(f'{ROOT}/content/pp*.txt')):
    cur = None; var = None
    for raw in open(path, encoding='utf8'):
        ln = raw.rstrip('\n')
        if not ln.strip() or ln.startswith('#'):
            continue
        if ln.startswith('@+'):
            cur = blank(ln[2:].strip(), ''); cur['_cont'] = 1; conts.append(cur); var = None
            continue
        if ln.startswith('@'):
            sid, title = [x.strip() for x in ln[1:].split('|', 1)]
            cur = {'id': sid, 'g': 'PP', 'pp': 1, 'add': False, 't': title, 'src': '', 'u': [], 'fr': [], 'ex': [], 'pr': [],
                   'info': '', 'task': '', 'trig': [], 'hook': [], 'clinch': [], 'money': '', 'trap': [], 'vars': [], 'ask': [],
                   'dom': [], 'script': []}
            pp.append(cur); var = None
            continue
        m = re.match(r'^(\w+)(\[(\w)\])?:\s*(.*)$', ln)
        if not m or cur is None:
            errs.append((path, ln[:80])); continue
        key, vk, val = m.group(1), m.group(3), m.group(4).strip()
        if key == 'src': cur['src'] = (cur['src'] + ' · ' + val) if cur['src'] else val
        elif key == 'u': cur['u'] = [int(x) for x in re.split(r'[,\s]+', val) if x]
        elif key in ('fr', 'ex', 'pr'): cur[key] = [x for x in re.split(r'[,\s]+', val) if x]
        elif key == 'door': cur['info'] = val
        elif key in ('trig', 'hook', 'trap'): cur[key].append(val)
        elif key == 'clinch':
            sym = val[:1]
            cur['clinch'].append([KIND.get(sym, 'in'), val[1:].strip() if sym in KIND else val])
        elif key == 'money': cur['money'] = val
        elif key == 'var':
            k, who, dx = [x.strip() for x in val.split('|', 2)]
            var = {'k': k, 'who': who, 'dx': dx, 'a': [], 'r': '', 'x': ''}
            cur['vars'].append(var)
        elif key == 'a': var['a'].append(val)
        elif key == 'd': var['d'] = val
        elif key == 'm': var['m'] = val
        elif key == 'r': var['r'] = (var['r'] + ' ' + val).strip()
        elif key == 'x': var['x'] = (var['x'] + ' ' + val).strip()
        elif key == 'ask': cur['ask'] = [x.strip() for x in val.split('|') if x.strip()]
        elif key == 'dom':
            h, items = [x.strip() for x in val.split('|', 1)]
            its = []
            for t in [x.strip() for x in items.split(';') if x.strip()]:
                w = 2 if t.startswith('!') else 1
                its.append({'t': t.lstrip('!').strip(), 'w': w} if w == 2 else {'t': t})
            cur['dom'].append({'h': h, 'items': its})
        elif key == 's':
            parts = [x.strip() for x in val.split('|')]
            if len(parts) < 3:
                errs.append((path, 'script needs 3 parts: ' + ln[:80])); continue
            sec, say, why = parts[0], parts[1], ' | '.join(parts[2:])
            row = {'s': sec, 'say': say, 'why': why}
            if vk: row['v'] = vk
            cur['script'].append(row)
        else:
            errs.append((path, 'unknown key ' + key))

_by = {x['id']: x for x in pp}
for c in conts:
    s0 = _by.get(c['id'])
    if not s0: errs.append((c['id'], 'continuation for unknown station')); continue
    if c['src']: s0['src'] = s0['src'] + ' · ' + c['src']
    for k in ('trig', 'hook', 'clinch', 'trap', 'vars', 'ask', 'dom', 'script'):
        s0[k] = s0[k] + c[k]
    for f in ('u', 'ex', 'pr', 'fr'):
        for x in c[f]:
            if x not in s0[f]: s0[f].append(x)
def _num(s):
    m = re.match(r'PP(\d+)', s['id']); return int(m.group(1)) if m else 999
pp.sort(key=_num)
for s in pp:
    s['k'] = kind_for(s['fr'])
    s['task'] = ''
    for u in s['u']:
        if not (0 <= u < len(D['units'])):
            errs.append((s['id'], f'bad unit {u}'))
    for e in s['ex']:
        if not any(x['id'] == e for x in D['exams']): errs.append((s['id'], 'bad exam ' + e))
    for p in s['pr']:
        if not any(x['id'] == p for x in D['dops']): errs.append((s['id'], 'bad proc ' + p))
    for f in s['fr']:
        if f not in D['frames']: errs.append((s['id'], 'bad frame ' + f))
    if not s['vars']: errs.append((s['id'], 'no variants'))
    if not s['dom']: errs.append((s['id'], 'no domains'))
    vks = {v['k'] for v in s['vars']}
    if len(vks) != len(s['vars']): errs.append((s['id'], 'duplicate case keys'))
    for v in s['vars']:
        if 'm' in v:
            s.setdefault('mv', {})[v['k']] = s['money'] if v['m'] == '=' else v['m']
            del v['m']
    for row in s['script']:
        if row.get('v') and row['v'] not in vks: errs.append((s['id'], 'script variant ' + row['v']))
    txt = json.dumps(s, ensure_ascii=False)
    if '—' in txt: errs.append((s['id'], 'em dash'))

# per-case money lines
byid = {x['id']: x for x in pp}
for ln in open(f'{ROOT}/content/money_by_case.txt', encoding='utf8'):
    ln = ln.rstrip('\n')
    if not ln.strip() or ln.startswith('#'):
        continue
    head, txt = [x.strip() for x in ln.split('|', 1)]
    sid, k = head.split()
    if sid not in byid: errs.append((sid, 'money for unknown station')); continue
    s0 = byid[sid]
    if k not in {v['k'] for v in s0['vars']}: errs.append((sid, 'money for unknown case ' + k)); continue
    s0.setdefault('mv', {})[k] = s0['money'] if txt == '=' else txt
for s0 in pp:
    if len(s0['vars']) > 1:
        miss = [v['k'] for v in s0['vars'] if v['k'] not in s0.get('mv', {})]
        if miss: errs.append((s0['id'], 'no money line for cases ' + ','.join(miss)))
    if '—' in json.dumps(s0.get('mv', {}), ensure_ascii=False): errs.append((s0['id'], 'em dash in money'))

# ---------- 5. frameworks (v3) ----------
FW = {'uni': [], 'list': []}
stids = {x['id'] for x in pp} | {x['id'] for x in st}
fw = None; mem = None
for path in sorted(glob.glob(f'{ROOT}/content/fw*.txt')):
    for raw in open(path, encoding='utf8'):
        ln = raw.rstrip('\n')
        if not ln.strip() or ln.startswith('#'): continue
        if ln.startswith('@@@'):
            fw = 'UNI'; mem = None; continue
        if ln.startswith('@@'):
            fid, icon, title, blurb = [x.strip() for x in ln[2:].split('|', 3)]
            fw = {'id': fid, 'i': icon, 't': title, 'b': blurb, 'steps': [], 'nn': [], 'm': []}; FW['list'].append(fw); mem = None; continue
        if ln.startswith('@'):
            mid, title, sts, us = [x.strip() for x in ln[1:].split('|', 3)]
            mem = {'id': mid, 't': title, 'st': [x for x in re.split(r'[,\s]+', sts) if x], 'u': [int(x) for x in re.split(r'[,\s]+', us) if x], 'use': '', 'ch': {}, 'tree': [], 'nn': [], 'pearl': ''}
            fw['m'].append(mem)
            for x in mem['st']:
                if x not in stids: errs.append((fid + '/' + mid, 'unknown station ' + x))
            for x in mem['u']:
                if not (0 <= x < len(D['units'])): errs.append((fid + '/' + mid, 'bad unit %d' % x))
            continue
        m = re.match(r'^(\w+):\s*(.*)$', ln)
        if not m: errs.append((path, 'fw line ' + ln[:60])); continue
        key, val = m.group(1), m.group(2).strip()
        if fw == 'UNI':
            if key != 'nn': errs.append(('UNI', key)); continue
            a = [x.strip() for x in val.split('|', 2)]
            FW['uni'].append({'t': a[0], 'say': '' if a[1] == '-' else a[1], 'why': a[2]}); continue
        if mem is None:
            if key == 'step':
                k, ttl, say, why = [x.strip() for x in val.split('|', 3)]
                FW['list'][-1]['steps'].append({'k': k, 't': ttl.lstrip('!'), 'nn': 1 if ttl.startswith('!') else 0, 'say': '' if say == '-' else say, 'why': why})
            elif key == 'nn': fw['nn'].append(val)
            else: errs.append((fw['id'], 'fw key ' + key))
            continue
        if key == 'use': mem['use'] = val
        elif key == 'ch':
            k, txt = [x.strip() for x in val.split('|', 1)]
            if k not in {s_['k'] for s_ in fw['steps']}: errs.append((fw['id'] + '/' + mem['id'], 'unknown step ' + k))
            mem['ch'][k] = txt
        elif key == 'tree':
            b, leaves = [x.strip() for x in val.split('|', 1)]
            mem['tree'].append([b, [x.strip() for x in leaves.split(';') if x.strip()]])
        elif key == 'nn': mem['nn'].append(val)
        elif key == 'pearl': mem['pearl'] = val
        else: errs.append((fw['id'] + '/' + mem['id'], 'member key ' + key))
if '—' in json.dumps(FW, ensure_ascii=False): errs.append(('FW', 'em dash'))
D['fw'] = FW

if errs:
    for e in errs: print('ERR', e)
    sys.exit(1)

D['groups'] = dict([('PP', 'Past papers (Nottingham)')] + list(D['groups'].items()))
D['stations'] = pp + st
D['meta'] = {'v': 3, 'fw': len(FW['list']), 'fwm': sum(len(f['m']) for f in FW['list']), 'pp': len(pp), 'bank': len(st), 'dropped': dropped, 'ck': nck}
out = f'{ROOT}/build/osce_data_v3.json'
json.dump(D, open(out, 'w'), ensure_ascii=False, separators=(',', ':'))
print('past-paper stations', len(pp), 'variants', sum(len(s['vars']) for s in pp), 'script lines', sum(len(s['script']) for s in pp))
print('bank stations', len(st), 'dropped', dropped, 'clinchers', nck, 'size KB', os.path.getsize(out) // 1024)
