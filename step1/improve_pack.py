#!/usr/bin/env python3
"""v3.6.1: clean and deepen the STEP1 content pack. Reads step1/pack_base.json (the v3.6.0 pack, kept unchanged as the
source), writes step1/pack.json (what site/build.py ships). Nothing is deleted: every question, arrow, card and image stays.

What it fixes
  scanned UWorld questions   page chrome (Item n of n, Mark, Previous Next, Time Spent), peer-percentage stats left in
                             options, OCR slips (brachia! → brachial, lgG → IgG, w ith → with), duplicated passages,
                             lead-ins stranded at the end of the stem, and topics filed under the wrong chapter
  4-box explanations         red flags rebuilt from the stem words the explanation actually uses, the money line from the
                             Educational Objective, inflow → outflow from the explanation's own causal sentences;
                             mechanisms borrowed from unrelated topics and template flips are replaced
  twin questions and cards   template twins ("In a follow-up twin scenario for…") are retired in favour of real twins
                             built on demand by AI in the app; Anki cards are rebuilt from the cue, answer and objective
  Mehlman arrow questions    the filler sentence added to every stem is removed and topics are re-filed by content
  glossary                   the US abbreviations and US/UK drug names return alongside the 322 general shorthand entries

Run: python3 step1/improve_pack.py   (needs `pip install wordfreq` for the OCR dictionary)
"""
import json, math, pathlib, re, sys, collections
from wordfreq import zipf_frequency

HERE = pathlib.Path(__file__).resolve().parent
D = json.loads((HERE / 'pack_base.json').read_text(encoding='utf-8'))
U, Q = D['units'], D['hq']['q']
STATS = collections.Counter()

# ------------------------------------------------------------------ vocabulary for OCR repair
corpus = collections.Counter()
def feed(t):
    for w in re.findall(r"[A-Za-z][A-Za-z'-]+", t):
        corpus[w.lower()] += 1
for p in D['pages']:
    for t in p['topics']:
        for b in t['b']:
            for l in b:
                feed(l[0])
for f in (HERE / 'src').glob('*.txt'):
    feed(f.read_text(encoding='utf-8'))
for q in Q:
    feed(q['s']); feed(' '.join(q['o'])); feed(q['w'])

def known(w):
    lw = w.lower()
    return zipf_frequency(lw, 'en') >= 2.2 or corpus[lw] >= 4

SUBS = [('!', 'l'), ('!', 'i'), ('1', 'l'), ('1', 'i'), ('1', 't'), ('1', ''), ('}', ')'), ('0', 'o'), ('rn', 'm'), ('ft', 'fl'), ('rc', 'ri'), ('fr', 'fi'),
        ("\\'l", 'w'), ("'l", 'w'), ('c', 'e'), ('e', 'c'), ('li', 'h'), ('cl', 'd'), ('ii', 'u'), ('l', 'i'), ('i', 'l'),
        ('t', 'f'), ('f', 't'), ('h', 'b'), ('n', 'u'), ('u', 'n'), ('vv', 'w'), ('5', 's'), ('8', 'B')]
FIXED = {'NAO': 'NAD+', 'NAO.': 'NAD+.', 'y-globin': 'γ-globin', 'NADH.': 'NADH.', 'lgG': 'IgG', 'lgA': 'IgA', 'lgM': 'IgM', 'lgE': 'IgE', 'lgD': 'IgD', "NAO'": 'NAD+', 'NAO+': 'NAD+', 'NAOH': 'NADH',
         'NADP+': 'NADP+', 'th.e': 'the', 'Time Soent': 'Time Spent'}

def fix_token(tok):
    if tok in FIXED:
        return FIXED[tok]
    core = re.match(r"^([\"(\[]*)(.*?)([\"').,;:\]]*)$", tok)
    pre, w, post = core.groups()
    if w and re.search(r'[a-z]\d[A-Za-z]', w):
        c2 = re.sub(r'(?<=[a-z])\d(?=[A-Za-z])', '', w).lower() if w[0].islower() else w[0] + re.sub(r'(?<=[a-z])\d(?=[A-Za-z])', '', w[1:]).lower()
        if known(c2):
            STATS['ocr_word'] += 1
            return pre + c2 + post
    if not w or not re.search('[A-Za-z]', w) or known(w) or len(w) < 4:
        return tok
    if re.fullmatch(r"[A-Z0-9+\-/]+", w):          # abbreviations, genes, ions
        return tok
    for a, b in SUBS:
        i = w.find(a)
        while i >= 0:
            cand = w[:i] + b + w[i + len(a):]
            if known(cand) and cand.lower() != w.lower():
                STATS['ocr_word'] += 1
                return pre + cand + post
            i = w.find(a, i + 1)
    return tok

def fix_text(t):
    if not t:
        return t
    t = t.replace("\\'", "'").replace('}', ')')
    t = re.sub(r"\b([A-Za-z]) ?'V([a-z]+)", lambda m: (m.group(1) + 'w' + m.group(2)) if known(m.group(1) + 'w' + m.group(2)) else m.group(0), t)
    t = re.sub(r'\b([a-z]{2,})- ([a-z]{2,})\b', lambda m: (m.group(1) + m.group(2)) if known(m.group(1) + m.group(2)) else m.group(0), t)
    t = re.sub(r'^[:;.,\s]*(?:DJ|D|0|O|□|\[\])\s+(?=[A-Z])', '', t)
    t = re.sub(r'(\d)\. (\d)', r'\1.\2', t)                     # 1. 70 → 1.70
    t = re.sub(r'\s+([.,;:])(?=\s|$)', r'\1', t)                # space before punctuation
    t = re.sub(r'\b([a-z]) ([a-z]{2,})\b', lambda m: (m.group(1) + m.group(2)) if known(m.group(1) + m.group(2)) and not known(m.group(2)) else m.group(0), t)
    t = re.sub(r'\b([a-z]{2,}) ([a-z]{1,2})\b', lambda m: (m.group(1) + m.group(2)) if known(m.group(1) + m.group(2)) and not known(m.group(1)) and m.group(2) not in ('a', 'an', 'as', 'at', 'be', 'by', 'do', 'go', 'he', 'if', 'in', 'is', 'it', 'me', 'my', 'no', 'of', 'on', 'or', 'so', 'to', 'up', 'us', 'we') else m.group(0), t)
    return ' '.join(fix_token(x) for x in t.split(' '))

# ------------------------------------------------------------------ scanned-page clean-up
CHROME = [r'(?:Next\s+)?Item:\s*\d+\s*of\s*\d+.*?(?:Previous\s+Next|Next\s+Item:|$)', r'User\s+Id:\s*\S+', r'Q\.\s*Id:\s*\d+\s*[\[(]\d+[\])]',
          r'Time\s+S[po]ent:\s*\d+\s*(?:seconds?|minutes?|secs?)?', r'\bII?\s*f\'\s*Mark\b', r'<::!?\s*C>', r'-{3,}', r'Explanation:\s*']

def is_junk_token(tok):
    letters = sum(c.isalpha() for c in tok)
    return len(tok) <= 2 and not tok.isalnum() or (len(tok) > 0 and letters / len(tok) < 0.5 and not re.fullmatch(r'[\d.,%/()\-+]+', tok))

def strip_garble(t):
    toks = t.split(' ')
    out, run = [], []
    for tok in toks:
        if tok and is_junk_token(tok):
            run.append(tok)
            continue
        if len(run) < 3:
            out.extend(run)
        else:
            STATS['garble_run'] += 1
        run = []
        out.append(tok)
    if len(run) < 3:
        out.extend(run)
    return re.sub(r'\s{2,}', ' ', ' '.join(out)).strip()

def clean_expl(w):
    if not w:
        return w, ''
    for c in CHROME:
        w2 = re.sub(c, ' ', w, flags=re.S)
        if w2 != w:
            STATS['chrome'] += 1
        w = w2
    w = strip_garble(w)
    eo = ''
    m = re.search(r'Educational\s+Objective:\s*(.*)$', w, re.S)
    if m:
        eo, w = m.group(1).strip(), w[:m.start()].strip()
    # the same passage often appears twice (the page reflowed); keep the first full copy
    head = w[:60]
    if len(head) >= 40:
        j = w.find(head, 40)
        if j > 0:
            w = w[:j].strip()
            STATS['duplicate_passage'] += 1
    w = re.sub(r'\s+\.', '.', w)
    w = re.sub(r'(?<=[a-z])\.(?=\s*$)', '…', w) if re.search(r'\b(the|of|and|on|to|a|in|with|for)\.$', w) else w
    return fix_text(w).strip(' .') + ('' if w.endswith('…') else '.'), fix_text(eo).strip()

PCT = re.compile(r'\s*[\[(]\s*\d[\d\s.,]*%\s*[\])]|\s*\[\s*\d+\s*\d*\s*%?\s*\]$')

def clean_option(o):
    o2 = PCT.sub('', o).strip()
    if o2 != o:
        STATS['peer_stat_removed'] += 1
    return fix_text(o2)

GENERIC_QL = {'Which of the following is the most likely explanation or finding in this patient?'}

def restore_leadin(q):
    s = q['s'].rstrip()
    if q['ql'][:1].islower():                       # the lead-in was cut mid-word: "...the following radiogr." + "aphic findings..."
        m0 = re.search(r'((?:Which|What|The|This|In|A|An|If)\b[^.?!]*?)\.?$', s)
        if m0:
            frag = m0.group(1)
            q['ql'] = frag + ('' if re.search(r'[a-z]$', frag) and q['ql'][:1].islower() and not frag.endswith(' ') else ' ') + q['ql']
            q['s'] = s[:m0.start()].rstrip()
            STATS['leadin_rejoined'] += 1
            return
    m = re.search(r'([^.?!]*?(?:Which|which|What|what|most likely|best explains|is most|are most|would most|most appropriate|following)[^.?!]*[:?])$', s)
    if q['ql'] in GENERIC_QL and m and len(m.group(1).split()) >= 3:
        q['ql'] = m.group(1).strip()
        if q['ql'].endswith(':'):
            q['ql'] = q['ql'][:-1].rstrip() + ':'
        q['s'] = s[:m.start()].rstrip()
        STATS['leadin_restored'] += 1
    q['ql'] = re.sub(r'best explains: the', 'best explains the', q['ql'])

# ------------------------------------------------------------------ topic re-filing by content (tf-idf)
STOP = set('''the and with for that this from which have has had are was were been being into than then them they their there these those
what when where while about after before over under very more most less least such only also other some each both between because through
during would could should patient patients following likely years year old woman man male female presents present shows showed history
physical examination reveals reveal normal increased decreased increase decrease level levels findings finding cause caused causes'''.split())

def toks(t):
    return [w for w in re.findall(r'[a-z][a-z0-9-]{2,}', t.lower()) if w not in STOP]

topic_doc = [collections.Counter() for _ in U]
for i, u in enumerate(U):
    for w in toks(u['name']):
        topic_doc[i][w] += 6
for ki, row in D['trg']['c'].items():
    for w in toks(' '.join(row)):
        topic_doc[int(ki)][w] += 2
for h in D['hunt']:
    pass
for i, u in enumerate(U):
    for hid in u.get('hunt', []):
        for w in toks(D['hunt'][hid][1] + ' ' + D['hunt'][hid][2]):
            topic_doc[i][w] += 2
    for n, ti in u['refs']:
        page = next(p for p in D['pages'] if p['n'] == n)
        for b in page['topics'][ti]['b']:
            for l in b:
                for w in toks(l[0]):
                    topic_doc[i][w] += 1
df = collections.Counter(w for d in topic_doc for w in d)
NT = len(U)
idf = {w: math.log((NT + 1) / (c + 0.5)) for w, c in df.items()}

def vec(c):
    v = {w: (1 + math.log(n)) * idf.get(w, 0) for w, n in c.items() if w in idf}
    norm = math.sqrt(sum(x * x for x in v.values())) or 1
    return {w: x / norm for w, x in v.items()}

TV = [vec(d) for d in topic_doc]
inv = collections.defaultdict(list)
for i, v in enumerate(TV):
    for w, x in v.items():
        inv[w].append((i, x))

def best_topics(text_weighted):
    qv = vec(text_weighted)
    sc = collections.Counter()
    for w, x in qv.items():
        for i, y in inv.get(w, []):
            sc[i] += x * y
    return sc.most_common(3)

def q_text(q, eo=''):
    c = collections.Counter()
    for w in toks(q['s'] + ' ' + q['ql']):
        c[w] += 1
    for w in toks(q['o'][q['a']]):
        c[w] += 3
    for w in toks(eo):
        c[w] += 2
    for w in toks(q.get('w', '')[:900]):
        c[w] += 1
    return c

# ------------------------------------------------------------------ 4-box from the question's own words
CAUSAL = re.compile(r'\b(leads? to|results? in|caus(e|es|ed|ing)|due to|because|therefore|which (then )?|triggers?|inhibits?|stimulates?|increases?|decreases?|reduces?|blocks?|→|->|producing|activates?|impairs?)\b', re.I)

def sentences(t):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z(])', t) if len(s.split()) >= 5]

def short(s, n=34):
    w = s.split()
    return s if len(w) <= n else ' '.join(w[:n]).rstrip(',;:') + '…'

def cues_for(q, ref):
    s = q['s']
    ref_t = set(toks(ref))
    words = list(re.finditer(r"\S+", s))
    best = []
    for m in re.finditer(r'[^,.;:]+', s):
        seg = m.group(0).strip()
        if len(seg.split()) < 2:
            continue
        ws = toks(seg)
        score = sum(idf.get(w, 1.5) for w in ws if w in ref_t) + 0.6 * len(re.findall(r'\d', seg) and [1] or [])
        if score <= 0:
            continue
        parts = seg.split()
        if len(parts) > 12:                      # keep the strongest 8-word window
            bw, bs = parts[:8], -1
            for k in range(len(parts) - 7):
                win = parts[k:k + 8]
                sc = sum(idf.get(w, 1.5) for w in toks(' '.join(win)) if w in ref_t)
                if sc > bs:
                    bw, bs = win, sc
            seg = ' '.join(bw)
        seg = seg.strip(' ()"\'')
        edge = {'and', 'an', 'a', 'the', 'with', 'in', 'its', 'of', 'to', 'for', 'is', 'are', 'was', 'his', 'her', 'their', 'that', 'which', 'on', 'at', 'by', 'or'}
        ps = seg.split()
        while ps and ps[0].lower() in edge:
            ps = ps[1:]
        while ps and ps[-1].lower().strip('.,') in edge:
            ps = ps[:-1]
        seg = ' '.join(ps)
        if len(ps) < 2:
            continue
        if seg and seg in s:
            best.append((score, seg))
    best.sort(key=lambda x: -x[0])
    out = []
    for _, seg in best:
        if not any(seg in o or o in seg for o in out):
            out.append(seg)
        if len(out) == 3:
            break
    return out

def mech_for(w, eo):
    ss = [x for x in sentences(w) if CAUSAL.search(x)]
    if not ss:
        ss = sentences(w)[:2]
    ss = sorted(ss[:5], key=len)[:3]
    order = [x for x in sentences(w) if x in ss]
    return ' → '.join(short(x.rstrip('.'), 26) for x in order) or short(eo, 30)

def whynot_for(q, w):
    out = []
    ans_words = set(toks(q['o'][q['a']]))
    ss = sentences(w)
    for i, o in enumerate(q['o']):
        if i == q['a']:
            continue
        keys = [k for k in toks(o) if k not in ans_words and len(k) >= 4]
        hit = next((x for x in ss if keys and any(re.search(r'\b' + re.escape(k), x, re.I) for k in keys)), None)
        if hit:
            out.append([i, short(hit, 40)])
    return out

def old_x(q):
    good = []
    for i, txt in (q.get('tm') or {}).get('x', []):
        t = re.sub(r'^\([^)]{1,80}\)\s*', '', txt).strip()
        t = re.sub(r'^(Vs |for )?[^:]{0,90}\(QID \d+\)[^:]*:\s*', '', t)
        if len(t.split()) >= 5 and 'in this' not in t[:20] and 'vignette' not in t[:60]:
            good.append([i, fix_text(short(t, 45))])
    return good

def pattern(q):
    ql = q['ql'].lower()
    if all(re.search(r'\d', o) for o in q['o']):
        return 'N'
    if re.search(r'drug|medication|treat|therapy|pharmaco|agent|mechanism of action|adverse effect|side effect|inhibit', ql):
        return 'D'
    if re.search(r'where|location|structure|nerve|artery|vein|muscle|site|injur|derived|embryolog|lesion|region|segment', ql):
        return 'T'
    if re.search(r'next step|most appropriate|best initial|management', ql):
        return 'R'
    if re.search(r'diagnosis|most likely cause|which of the following conditions|organism|pathogen', ql):
        return 'L'
    return 'M'

def cards_for(q, unit_name, eo, xs):
    ans = q['o'][q['a']]
    cues = q['tm'].get('c', [])
    front = ('; '.join(c[0].upper() + c[1:] for c in cues[:3]) + '. ' if cues else '') + q['ql']
    back = '**' + ans + '**' + (': ' + short(eo, 40) if eo else '')
    cards = [[front, back]]
    for i, t in xs[:2]:
        cards.append([unit_name + ': why is it not ' + q['o'][i] + '?', t])
    return cards

def norm_ok(h, ans):
    return h.lower() != ans.lower() and h.lower() not in ans.lower() and ans.lower() not in h.lower()

def arrows_of(o):
    return dict((k.strip(), v.strip()) for k, v in (part.split(':', 1) for part in o.split(' · ') if ':' in part))

ARW = {'↑': 'up', '↓': 'down', '↔': 'unchanged'}
def mehlman_x(q):
    """For arrow-profile options, name exactly which arrows are wrong and what they should be."""
    right = arrows_of(q['o'][q['a']])
    if len(right) < 2:
        return []
    out = []
    for i, o in enumerate(q['o']):
        if i == q['a']:
            continue
        mine = arrows_of(o)
        bad = [k for k in right if k in mine and mine[k] != right[k]]
        if bad:
            t = '; '.join(k + ' is ' + ARW.get(right[k], right[k]) + ', not ' + ARW.get(mine[k], mine[k]) for k in bad)
            out.append([i, t[0].upper() + t[1:]])
    if out:
        STATS['mehlman_whynot_written'] += len(out)
    return out

TEMPLATE_TWIN = re.compile(r'follow-up twin scenario|consider a patient whose presentation is modified', re.I)

# your hand-written questions (src/sba_*.txt): 3.6.0 gave them made-up UWorld ids, which must not get them rebuilt
MINE_STEMS = set()
for f in (HERE / 'src').glob('sba_*.txt'):
    for ln in f.read_text(encoding='utf-8').splitlines():
        if ln.startswith('s: '):
            MINE_STEMS.add(re.sub(r'\W+', '', ln[3:].split('//')[0])[:80].lower())

# ------------------------------------------------------------------ run
for q in Q:
    is_mine = re.sub(r'\W+', '', q['s'])[:80].lower() in MINE_STEMS
    if is_mine:
        q['src'] = 'medengine'
        if not q.get('uw_qid') and str(q.get('uworld_qid', '')).startswith('UW-'):
            q.pop('uworld_qid', None)
        STATS['mine_kept_with_flips'] += 1
    is_uw = not is_mine and bool(q.get('uw_qid') or q.get('uworld_qid'))
    is_mh = q.get('src') == 'Mehlman HY Arrows'
    if q.get('tw') and TEMPLATE_TWIN.search(q['tw'].get('s', '')):
        del q['tw']
        STATS['template_twin_retired'] += 1
    if is_uw:
        q['src'] = 'UWorld'
        q['s'] = fix_text(re.sub(r'\s{2,}', ' ', q['s']))
        q['o'] = [clean_option(o) for o in q['o']]
        if len(set(o.lower() for o in q['o'])) < len(q['o']):
            STATS['options_collided'] += 1
        q['w'], eo = clean_expl(q['w'])
        restore_leadin(q)
        old_k = q['k']
        top = best_topics(q_text(q, eo))
        cur = next((s for i, s in top if str(i) == old_k), None)
        if top and (cur is None or cur < 0.72 * top[0][1]) and top[0][1] > 0.08:
            q['k'] = str(top[0][0])
            STATS['refiled'] += 1
        ref = (eo + ' ' + q['w'] + ' ' + q['o'][q['a']])
        xs = old_x(q) or whynot_for(q, q['w'])
        g2 = ' '.join(sentences(eo)[:2]) if eo else ''
        tm = {'c': cues_for(q, ref), 'g': short(g2 or eo or (sentences(q['w']) or [q['w']])[0], 55), 'm': mech_for(q['w'], eo), 'f': [], 'x': xs}
        if len(tm['c']) < 2:
            tm['c'] = cues_for(q, ref + ' ' + q['s'])
        q['tm'] = tm
        q['f'] = ''
        q['eo'] = eo
        q['p'] = pattern(q)
        q['cards'] = cards_for(q, U[int(q['k'])]['name'], eo, xs)
        STATS['uworld_rebuilt'] += 1
    elif is_mh and not is_mine:
        q['s'] = re.sub(r'\s*During physiological assessment of [^.]*\.', '', q['s']).strip()
        top = best_topics(q_text(q, q['w']))
        cur = next((s for i, s in top if str(i) == q['k']), None)
        if top and (cur is None or cur < 0.72 * top[0][1]) and top[0][1] > 0.08:
            q['k'] = str(top[0][0])
            STATS['refiled'] += 1
        scene = re.split(r'[Ww]hat (?:are|will|change|is|happens|would)', re.sub(r'^\[Mehlman Arrow #\d+\]\s*', '', q['s']))[0]
        cues = [c.strip(' .,?') for c in re.split(r'\+|,', scene) if len(c.strip(' .,?').split()) >= 2 and c.strip(' .,?') in q['s']][:4]
        body = re.sub(r'^Correct arrow profile:[^.]*\.\s*', '', q['w'])
        q['tm'] = {'c': cues if cues else [c for c in q['tm'].get('c', []) if not c.startswith('[')], 'g': short((sentences(body) or [body])[0], 45),
                   'm': mech_for(body, ''), 'f': [], 'x': mehlman_x(q)}
        q['f'] = ''
        q['p'] = 'M'
        q['cards'] = cards_for(q, U[int(q['k'])]['name'], short((sentences(body) or [body])[0], 45), [])
        STATS['mehlman_rebuilt'] += 1
    else:
        tm = q.get('tm') or {}
        q['cards'] = cards_for(q, U[int(q['k'])]['name'], tm.get('g', ''), tm.get('x', [])[:2])
    q['w'] = q['w'].replace('->', '→')

D['hq']['pat'] = dict(D['hq']['pat'], M='Mechanism', I='Image')

# US abbreviations and drug names back alongside the general shorthand list
us = []
for ln in (HERE / 'src' / 'gloss_us.txt').read_text(encoding='utf-8').splitlines():
    if ln.strip() and not ln.startswith('#'):
        a, _, b = ln.partition(' | ')
        us.append([a.strip(), b.strip()])
have = {g[0].lower() for g in D['gloss']}
D['gloss'] = us + [g for g in D['gloss'] if g[0].lower() not in {u[0].lower() for u in us}]
STATS['gloss_us_back'] = sum(1 for u in us if u[0].lower() not in have)

# posters copied from STUDY point at STUDY topic numbers: re-file them by title
for m in D.get('master', []):
    top = best_topics(collections.Counter(toks(m.get('t', '') + ' ' + m.get('sub', '')) * 3))
    if top:
        m['u'] = [top[0][0]]
        STATS['poster_refiled'] += 1

# ------------------------------------------------------------------ notes: lines from your own notes that were pinned to the wrong answer
# "🔎 Mehlman / NBME High-Yield Rule" and "🧬 Pathoma / First Aid pearl" lines were dealt round-robin to the answers of
# whichever topic they landed in (aminocaproic acid → Psoriasis). Each line is re-filed to the topic its words belong
# to, its blank goes on the answer it actually describes, and if no answer fits it stays as a plain fact with no blank.
page_by_n = {p['n']: p for p in D['pages']}
def unit_topics(u):
    tr = nt = None
    for n, ti in u['refs']:
        t = page_by_n[n]['topics'][ti]
        if '🧲' in t['h']:
            tr = t
        else:
            nt = t
    return tr, nt
HEADS = {}
for i, u in enumerate(U):
    tr, nt = unit_topics(u)
    hs = []
    for b in (tr or {'b': []})['b']:
        for l in b:
            for c in l[3][:1]:
                hs.append((l[0][c[0]:c[1]], l[0]))
    HEADS[i] = hs
RULE = re.compile(r'^• (🔎 Mehlman / NBME High-Yield Rule|🧬 Pathoma / First Aid pearl): ')
OUTLINE = re.compile(r'\b[A-F]\. [A-Z][a-z]+.*\b[B-G]\. [A-Z]')
def head_score(h, line, body):
    nm = set(toks(h)); bt = set(toks(body))
    abbr = set(re.findall(r'\b[A-Z][A-Z0-9]{1,6}\b', body)) & set(re.findall(r'\b[A-Z][A-Z0-9]{1,6}\b', line))
    return 3 * len(nm & bt) / max(1, len(nm)) * (1 if nm & bt else 0) + 0.5 * len((set(toks(line)) - nm) & bt) + 2 * len(abbr)
moved = collections.defaultdict(list)
for i, u in enumerate(U):
    tr, nt = unit_topics(u)
    if not nt:
        continue
    for b in nt['b']:
        keep = []
        for l in b:
            m = RULE.match(l[0])
            if not m:
                keep.append(l)
                continue
            body = l[0][m.end():]
            body = body.rsplit(' → ', 1)[0] if ' → ' in body else body
            body = re.sub(r'\s+-\s+[A-Z][a-z]+ Page [\d. ]+.*$', '', body).strip()
            body = re.sub(r'[-–\s]+$', '', body)
            if OUTLINE.search(body) or len(toks(body)) < 3 or re.search(r'\.(jpe?g|png|gif)$', body, re.I):
                STATS['note_outline_heading_dropped'] += 1
                continue
            top = best_topics(collections.Counter(toks(body)))
            tgt = top[0][0] if top and top[0][1] > 0.12 else i
            if tgt != i:
                STATS['note_line_refiled'] += 1
            moved[tgt].append((m.group(1), body))
        b[:] = keep
    nt['b'] = [b for b in nt['b'] if b and not (len(b) == 1 and not b[0][3] and b[0][0].endswith(':'))]
for tgt, items in moved.items():
    tr, nt = unit_topics(U[tgt])
    if not nt:
        continue
    blk = [['📎 From your notes, filed here by what they say:', 0, [], []]]
    for lab, body in items:
        hs = HEADS.get(tgt, [])
        sc = sorted(((head_score(h, ln, body), h) for h, ln in hs), reverse=True)
        text = '• ' + lab + ': ' + body
        blanks = []
        if sc and sc[0][0] >= 2.5 and (len(sc) == 1 or sc[0][0] > sc[1][0]) and sc[0][1].lower() not in body.lower():
            ans = sc[0][1]
            ds = [h for _, h in sc[1:] if norm_ok(h, ans)][:3]
            if len(ds) == 3:
                s0 = len(text) + 3
                text += ' → ' + ans
                blanks = [[s0, s0 + len(ans), 8, 2, 'custom', ds, ['', '', '']]]
                STATS['note_blank_on_right_answer'] += 1
        if not blanks:
            STATS['note_plain_fact'] += 1
        blk.append([text, 0, [], blanks])
    nt['b'].append(blk)
(HERE / 'pack.json').write_text(json.dumps(D, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
print(json.dumps(dict(STATS), indent=1))
