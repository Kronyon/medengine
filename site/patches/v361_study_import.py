#!/usr/bin/env python3
"""v3.6.1: bring the v3.6.0 STUDY changes into site/study.html and repair what the automated pass broke (applied once).

Kept from 3.6.0: the 66 new Hammer SBAs (h1713 onward) with their images, the extra official-paper images, the header
link to medengine-STEP1, and the thought-map check that counts why-not lines.
Repaired:
  - 308 stems had one of 11 stock sentences glued on ("During the medication review in the GP surgery…", "Baseline
    observations show a temperature of 36.7°C…"). They added reading time and no information, so they come off.
  - Flips were padded to four per question with generated lines ("in h0011 (A 28 year old woman…), ruled out by…",
    "he is haemodynamically stable" for a woman). Every hand-written flip is restored; generated padding that carried a
    real teaching sentence moves to "Why not the others" for that option; the rest is dropped.
Usage: python3 site/patches/v361_study_import.py /path/to/v3.6.0/study.html
"""
import collections, json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parents[1]
F = SITE / 'study.html'
cur = F.read_text(encoding='utf-8')
new = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
RX = re.compile(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', re.S)
O = json.loads(RX.search(cur).group(2))
N = json.loads(RX.search(new).group(2))
assert 'h1713' not in {q['id'] for q in O['hq']['q']}, 'already applied'
om = {q['id']: q for q in O['hq']['q']}
st = collections.Counter()

# stock sentences glued onto stems
glued = collections.Counter()
for q in N['hq']['q']:
    o = om.get(q['id'])
    if o and q['s'] != o['s'] and q['s'].startswith(o['s']):
        for s in re.split(r'(?<=\.)\s+', q['s'][len(o['s']):].strip()):
            glued[s] += 1
STOCK = {s for s, n in glued.items() if n >= 5}

def unstock(s):
    for x in STOCK:
        if x in s:
            s = s.replace(' ' + x, '').replace(x, '')
            st['stock_sentence'] += 1
    return s.strip()

all_new = collections.Counter(f[0] for q in N['hq']['q'] for f in q.get('tm', {}).get('f', []))
all_x = collections.Counter(x[1] for q in N['hq']['q'] for x in q.get('tm', {}).get('x', []))
TPL = re.compile(r'^(?:Vs [^:]{1,120}\(\d+, h\d{4}\):\s*[^-]*-\s*)?in h\d{4} \([^)]*\),\s*', re.I)
JUNK = re.compile(r'ruled out by .*selecting|selecting .* rather than', re.I)

for q in N['hq']['q']:
    o = om.get(q['id'])
    q['s'] = unstock(q['s'])
    tm = q.get('tm') or {}
    old_f = (o or {}).get('tm', {}).get('f', [])
    keep = [list(f) for f in old_f]
    xs = {i: t for i, t in (o or {}).get('tm', {}).get('x', [])}
    for i, t in tm.get('x', []):
        body = TPL.sub('', t).strip()
        if i in xs or i == q['a'] or not body or JUNK.search(body) or all_x[t] >= 5:
            if i not in xs:
                st['whynot_padding_dropped'] += 1
            continue
        xs[i] = body[0].upper() + body[1:]
    have = {f[1] for f in keep}
    for cond, i in tm.get('f', []):
        if [cond, i] in keep:
            continue
        if TPL.match(cond) or cond.startswith('Vs '):
            body = TPL.sub('', cond).strip()
            if body and not JUNK.search(body) and i not in xs and i != q['a']:
                xs[i] = body[0].upper() + body[1:]
                st['padding_to_whynot'] += 1
            else:
                st['padding_dropped'] += 1
            continue
        if all_new[cond] >= 3 or re.fullmatch(r'(he|she|the patient) (is|was) [a-z ]{3,30}', cond):   # stock lines
            st['generic_dropped'] += 1
            continue
        if i not in have and i != q['a']:
            keep.append([cond, i]); have.add(i)
            st['new_flip_kept'] += 1
    if tm:
        tm['f'] = sorted(keep, key=lambda f: f[1])
        tm['x'] = sorted([[i, t] for i, t in xs.items()], key=lambda x: x[0])
        if o and o.get('tm', {}).get('f') and q.get('f') and TPL.match(q['f']):
            q['f'] = o.get('f', '')
    st['questions'] += 1

O['hq'] = N['hq']
O['mock'], O['off'] = N['mock'], N['off']
cur = cur[:RX.search(cur).start(2)] + json.dumps(O, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + cur[RX.search(cur).end(2):]

# the two engine edits from 3.6.0
def must(a, b):
    global cur
    assert cur.count(a) == 1, a[:80]
    cur = cur.replace(a, b)
must('<span class="word">medengine-STUDY</span><small>v3.4.0</small></button>\n',
     '<span class="word">medengine-STUDY</span><small>v3.4.0</small></button>\n  <a class="oscelink" href="step1.html" title="Open medengine-STEP1: USMLE Step 1"><span class="od">s1</span>medengine-STEP1 ↗</a>\n')
must("    const fSet = new Set(((q.tm && q.tm.f) || []).map(x => x[1]));",
     "    const fSet = new Set(((q.tm && q.tm.f) || []).map(x => x[1]).concat(((q.tm && q.tm.x) || []).map(x => x[0])));")
F.write_text(cur, encoding='utf-8')
print(json.dumps(dict(st)))
