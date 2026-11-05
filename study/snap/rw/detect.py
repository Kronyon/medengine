#!/usr/bin/env python3
"""v3.6.4 weak-question detector for the Hammer bank. Writes rw/triage.json and rw/<week>.txt dumps for hand review.
Signals: length give-away, mixed option categories, absolute words in distractors, clones, negative lead-in,
non-vignette framing. Read-only: it never changes study.html."""
import json, re, collections, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
SITE = HERE.parents[2] / 'site'
p = (SITE / 'study.html').read_text(encoding='utf-8')
D = json.loads(re.search(r'<script id="qqdata" type="application/json">(.*?)</script>', p, re.S).group(1))
H = D['hq']['q']; U = D['units']
TEST = re.compile(r'\b(scan|x-ray|ct|mri|mr |ultrasound|test|biopsy|serology|culture|swab|ecg|echo\w*|level|count|assay|\w+scopy|\w+gram|\w+graphy|measurement|screen|aspirat\w* for|study|studies|electrophoresis|antibod|titre|profile|function tests?|monitoring|film|stain|pcr|dipstick|audiometry|fundoscopy|tonometry|perimetry|fields|index)\b', re.I)
ACT = re.compile(r'^(refer|admit|discharge|reassur|review|start|stop|continue|arrange|advise|repeat|reduce|increase|switch|add|give|treat|observe|watch|no |nil|urgent|routine|same-day|immediate|call|inform|tell|explain|assess|offer|apply|section|detain|remove|insert|open|fix|drain|excis|incis|surgical|emergency|elective|conservative|lifestyle|weight|exercise|support|counsel|psycho|cbt|therap|wait|safety)', re.I)
PROC = re.compile(r'(ectomy|otomy|ostomy|plasty|pexy|repair|drainage|ablation|ligation|banding|fixation|replacement|graft|bypass|stent|decompression|irrigation|injection|cryotherapy|laser|surgery|manoeuvre|cardioversion|pacing|transfusion|dialysis|thrombectomy|embolisation)', re.I)
DRUG = re.compile(r'(cream|ointment|gel|drops|lotion|shampoo|spray|tablets?|patch|inhaler|\bmg\b|micrograms|\biv\b|\boral\b|\btopical\b|\bim\b|nebulised|infusion|mab\b|pril\b|sartan\b|olol\b|azole\b|cillin\b|mycin\b|floxacin\b|statin\b|dipine\b|azepam\b|oxetine\b|aline\b|pram\b|done\b|parin\b|xaban\b|gatran\b|sone\b|olone\b|thiazide|semide|ide\b|ine\b|ate\b|cin\b|vir\b)', re.I)
def kind(o):
    t = o.strip()
    if re.match(r'^[<>]?\d', t): return 'num'
    if ACT.match(t) or PROC.search(t): return 'act'
    if TEST.search(t): return 'test'
    if DRUG.search(t): return 'drug'
    return 'dx'
ABS = re.compile(r'\b(only|alone|never|always|ever|nothing|indefinitely|for life|permanently|straight away|at once)\b', re.I)
NEG = re.compile(r'\b(not|least|except|against|unsafe|avoid\w*|contraindicat\w*)\b', re.I)
FRAME = re.compile(r'\b(asks|wants to know|medical student|is choosing|is reviewing|the team plans|pharmacist|reminds the team|is being consented|consenting|is deciding)\b', re.I)
WEEK = {i: u['w'] for i, u in enumerate(U)}
def week(q):
    if q['t'] == 'u': return WEEK[int(q['k'])]
    return q['t'] + ':' + q['k'].split(':')[0]
def ws(t): return set(re.findall(r'[a-z]{4,}', t.lower()))
ans_lead = collections.Counter((q['o'][q['a']].lower(), (q.get('ql') or '').lower()) for q in H)
seen = {}
first_of = {}
for q in H:  # clone = same answer and same lead-in as an earlier question, or a near-identical stem with the same answer
    k = (q['o'][q['a']].lower(), (q.get('ql') or '').lower())
    first_of.setdefault(k, q['id'])
S = [(q['id'], ws(q['s']), q['o'][q['a']].lower()) for q in H]
near = {}
for i in range(len(S)):
    for j in range(i + 1, len(S)):
        a, b = S[i][1], S[j][1]
        if a and b and S[i][2] == S[j][2] and len(a & b) / len(a | b) >= 0.5: near[S[j][0]] = S[i][0]
out = {}
for q in H:
    o = q['o']; a = q['a']; L = [len(x) for x in o]; rest = sorted(L[:a] + L[a + 1:], reverse=True)
    f = []
    if L[a] > rest[0] and L[a] - rest[0] > 3 and L[a] > rest[0] * 1.15: f.append('len')
    ka = kind(o[a]); kd = [kind(x) for i, x in enumerate(o) if i != a]
    if sum(k != ka for k in kd) >= 2: f.append('mix')
    if any(ABS.search(x) for i, x in enumerate(o) if i != a) and not ABS.search(o[a]): f.append('abs')
    k = (o[a].lower(), (q.get('ql') or '').lower())
    if first_of[k] != q['id']: f.append('clone:' + first_of[k])
    elif q['id'] in near: f.append('clone:' + near[q['id']])
    if NEG.search(q.get('ql') or ''): f.append('neg')
    if FRAME.search(q['s']): f.append('frame')
    out[q['id']] = {'w': week(q), 'f': f}
(HERE / 'triage.json').write_text(json.dumps(out, indent=0))
c = collections.Counter(x for v in out.values() for x in [y.split(':')[0] for y in v['f']])
print('flags across', len(H), dict(c), '| any flag:', sum(bool(v['f']) for v in out.values()))
bw = collections.Counter(v['w'] for v in out.values())
fw = collections.Counter(v['w'] for v in out.values() if v['f'])
for w in sorted(bw, key=lambda x: -bw[x])[:40]: print(f'  {w:18s} {bw[w]:4d} flagged {fw[w]}')
def dump(ids, name):
    with open(HERE / (name + '.txt'), 'w') as fh:
        for q in H:
            if q['id'] not in ids: continue
            fh.write(f"## {q['id']} [{','.join(out[q['id']]['f'])}] {((U[int(q['k'])]['name']) if q['t']=='u' else q['t']+':'+q['k'])}\n{q['s']}\n")
            if q.get('lab'): fh.write('LAB ' + '; '.join(' '.join(map(str, r)) for r in q['lab']) + '\n')
            fh.write('Q: ' + (q.get('ql') or '') + '\n')
            for i, x in enumerate(q['o']): fh.write(f"  {'*' if i == q['a'] else '-'} {x}\n")
for wk in sys.argv[1:]:
    dump({i for i, v in out.items() if v['w'] == wk or (wk == 'b' and v['w'].startswith('b:'))}, wk)
