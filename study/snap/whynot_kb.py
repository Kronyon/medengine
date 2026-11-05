"""Match an answer option to your own trigger, drug, test, procedure and snapshot cards, for a why-not line."""
import json,re,collections
h=open(__import__('pathlib').Path(__file__).resolve().parents[2] / 'site' / 'study.html', encoding='utf-8').read()
D=json.loads(re.search(r'<script id="qqdata" type="application/json">(.*?)</script>',h,re.S).group(1))
def clean(s): return re.sub(r'\*\*|__','',s or '').strip()
STOP=set('the a an of and or with in on to for by from acute chronic disease syndrome'.split())
def toks(s): return [w for w in re.findall(r"[a-z0-9']+",clean(s).lower()) if w not in STOP]
KB=[]  # (head, text, kind)
for cue,ans in D['trg']['c'].values():
    head=clean(ans).split(':')[0]; KB.append((head,'Classic picture: '+clean(cue)+'. '+clean(ans),'c'))
for grp in D['trg']['sc']:
    for row in grp[2]:
        KB.append((clean(row[2]).split(':')[0],'Classic picture: '+clean(row[1]),'c'))
for kind in ('dr','ix','mx'):
    for grp in D['trg'][kind]:
        for row in grp[2]:
            KB.append((clean(row[0]),'Used for: '+clean(row[2]),kind))
for r in D['hunt']:
    if len(r)>=3:
        a=clean(r[2]); head=re.split(r'\s*(?:→|:|\(|;)\s*',a)[0]
        KB.append((head,'Classic picture: '+clean(r[1]),'h'))
for k,s in D['snap'].items():
    if not isinstance(s,dict) or 'n' not in s: continue
    sig=', '.join(clean(x[0]) for x in s.get('s',[])[:3])
    KB.append((s['n'],'Typical: '+clean(s.get('w',''))+(('; '+sig) if sig else ''),'s'))
def match(opt):
    ot=toks(opt)
    if not ot: return None
    best=None
    for head,text,kind in KB:
        ht=toks(head)
        if not ht: continue
        inter=len(set(ot)&set(ht))
        if not inter: continue
        sc=inter/len(set(ot)|set(ht))
        if clean(head).lower()==clean(opt).lower(): sc=2
        if sc>=0.75 and (best is None or sc>best[0] or (sc==best[0] and kind=='c')):
            best=(sc,text,kind,head)
    return best
