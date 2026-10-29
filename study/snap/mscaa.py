"""v2.7: lay every Hammer and mock question out the way the MSCAA and MS AKT papers do.

What the official papers do, and what this applies to the 🔨 and 🎓 items:
  * ages written "54 year old", never "54-year-old"
  * the history first, then a new paragraph for observations and examination
  * every result carries its reference range in brackets, using the ranges printed in the papers themselves;
    a run of three or more results becomes an Investigations table, as in the papers
  * observations written the paper way: "pulse rate 104 bpm", "BP 104/58 mmHg", "respiratory rate 32 breaths per minute"
  * the lead-in on its own line, worded "Which is the most ...?"
  * five options in alphabetical order (numbers in ascending order); pm keeps the old to new index so saved runs survive
It also cleans the page footers ("© Medical Schools Council 2023 Page 12 of 105") out of the official justifications.
"""
import re

# name pattern, display name, unit, range: the ranges the MSCAA and MS AKT papers print
U9 = '× 10⁹/L'
AN = [
    (r'haemoglobin|Hb', 'Haemoglobin', 'g/L', None),  # sex-specific, set below
    (r'white cell count|white cells|WCC|white blood cell count', 'White cell count', U9, '3.8–10.0'),
    (r'neutrophils?(?: count)?', 'Neutrophils', U9, '2.0–7.5'),
    (r'lymphocytes?(?: count)?', 'Lymphocytes', U9, '1.1–3.3'),
    (r'eosinophils?', 'Eosinophils', U9, '0–0.4'),
    (r'platelets?(?: count)?', 'Platelets', U9, '150–400'),
    (r'MCV|mean cell volume', 'MCV', 'fL', '80–96'),
    (r'ferritin', 'Ferritin', 'µg/L', '12–200'),
    (r'sodium', 'Sodium', 'mmol/L', '135–146'),
    (r'potassium', 'Potassium', 'mmol/L', '3.5–5.3'),
    (r'urea', 'Urea', 'mmol/L', '2.5–7.8'),
    (r'creatinine', 'Creatinine', 'µmol/L', '60–120'),
    (r'eGFR', 'eGFR', 'mL/min/1.73 m²', '>60'),
    (r'chloride', 'Chloride', 'mmol/L', '95–106'),
    (r'bicarbonate|HCO3-?', 'Bicarbonate', 'mmol/L', '22–30'),
    (r'(?:adjusted |corrected )?calcium', 'Calcium', 'mmol/L', '2.2–2.6'),
    (r'phosphate', 'Phosphate', 'mmol/L', '0.8–1.5'),
    (r'magnesium', 'Magnesium', 'mmol/L', '0.7–1.0'),
    (r'albumin', 'Albumin', 'g/L', '35–50'),
    (r'bilirubin', 'Bilirubin', 'µmol/L', '<17'),
    (r'ALT|alanine (?:aminotransferase|transaminase)', 'ALT', 'IU/L', '10–50'),
    (r'AST|aspartate (?:aminotransferase|transaminase)', 'AST', 'IU/L', '10–40'),
    (r'ALP|alkaline phosphatase', 'ALP', 'IU/L', '25–115'),
    (r'GGT|γGT|gamma[- ]GT', 'GGT', 'IU/L', '9–40'),
    (r'amylase', 'Amylase', 'U/L', '<220'),
    (r'CRP|C-reactive protein', 'CRP', 'mg/L', '<5'),
    (r'ESR', 'ESR', 'mm/hr', '<20'),
    (r'fasting (?:plasma )?glucose', 'Fasting glucose', 'mmol/L', '3.0–6.0'),
    (r'(?:random |capillary |plasma |blood )*glucose', 'Glucose', 'mmol/L', '4.0–7.8'),
    (r'HbA1c|glycated haemoglobin', 'HbA1c', 'mmol/mol', '20–42'),
    (r'lactate', 'Lactate', 'mmol/L', '<2.0'),
    (r'(?:blood |capillary )?ketones', 'Ketones', 'mmol/L', '<0.6'),
    (r'TSH', 'TSH', 'mU/L', '0.3–4.2'),
    (r'free T4|fT4|free thyroxine', 'Free T4', 'pmol/L', '12–22'),
    (r'free T3|fT3', 'Free T3', 'pmol/L', '3.1–6.8'),
    (r'D-dimers?', 'D-dimer', 'mg/L', '<0.5'),
    (r'(?:high-sensitivity )?troponin(?: [TI])?(?: at \d+ hours?)?', 'Troponin', 'ng/L', '<14'),
    (r'(?:serum )?prolactin', 'Prolactin', 'mU/L', '100–500'),
    (r'(?:prothrombin time|PT)', 'PT', 'seconds', '10–12'),
    (r'APTT', 'APTT', 'seconds', '22–41'),
    (r'pH', 'pH', '', '7.35–7.45'),
    (r'PaO2|PO2|pO2', 'PaO2', 'kPa', '11–15'),
    (r'PaCO2|PCO2|pCO2', 'PaCO2', 'kPa', '4.6–6.4'),
    (r'creatine kinase|CK', 'Creatine kinase', 'U/L', '25–200'),
    (r'(?:total )?cholesterol', 'Total cholesterol', 'mmol/L', '<5.0'),
    (r'(?:serum )?lithium(?: level)?', 'Lithium', 'mmol/L', '0.4–1.0'),
    (r'(?:serum |plasma )?osmolality', 'Serum osmolality', 'mOsmol/kg', '275–295'),
    (r'(?:9 ?am )?cortisol', 'Cortisol (9am)', 'nmol/L', '200–700'),
    (r'parathyroid hormone|PTH', 'PTH', 'pmol/L', '1.6–8.5'),
]
UNITS = r'(?:× 10⁹/L|mmol/L|mmol/mol|g/L|g/dL|U/L|IU/L|µmol/L|μmol/L|umol/L|mg/L|ng/L|µg/L|nmol/L|pmol/L|mU/L|kPa|fL|mm/hr|seconds|mOsmol/kg|mOsm/kg|mL/min(?:/1\.73 ?m²|/1\.73m2)?|(?:×|x) ?10\^?9?⁹?/L)'
NOISE = re.compile(r'\b(fluid|CSF|urine|urinary|ascitic|pleural|aspirate|synovial|target|goal|aim|threshold|cut-?off|upper limit|lower limit)\b', re.I)
FILL = re.compile(r'\b(her|his|the|a|an|and|with|shows?|showed|show|results?|blood|bloods|tests?|investigations?|serum|plasma|are|is|was|were|of|on|admission|reveal|reveals|breathing|air|arterial|gas|venous|level|levels|count)\b|[\s,.;:]', re.I)


def _rx(name):
    return re.compile(r'(?<![\w/])(?:(?:her|his|the|a|an|serum|plasma)\s+)?(' + name + r')(?:\s+(?:level|levels|concentration|count))?'
                      r'(?:\s+(?:is|was|are|of|now|has fallen to|rose to|has risen to|:)){0,2}\s*(?:of\s+)?(-?\d+(?:\.\d+)?)\s*(' + UNITS + r')?'
                      r'(?!\s*(?:to|-|–)\s*\d)(?![\d/%])(?!\.\d)(?:\s*\(\s*([<>≤≥]?\s*\d[\d.]*(?:\s*[-–]\s*[\d.]+)?)\s*\))?', re.I)


RX = [(_rx(a[0]), a) for a in AN]


def _sex(s):
    t = ' ' + s.lower() + ' '
    f = len(re.findall(r'\b(woman|girl|she|her|female|mother|pregnant)\b', t)); m = len(re.findall(r'\b(man|boy|he|his|male|father)\b', t))
    return 'f' if f > m else 'm' if m > f else ''


def _range(a, sex):
    if a[1] == 'Haemoglobin':
        return '115–150' if sex == 'f' else '130–175' if sex == 'm' else '115–175'
    return a[3]


BARE_OK = re.compile(r'\s*(?:$|[,.;:)]|(?:and|with|but|on|after|in|at|which|while|despite|or)\b)', re.I)
NEED_UNIT = {'PT', 'APTT', 'Creatine kinase', 'Cortisol (9am)', 'PTH', 'Ferritin', 'MCV', 'D-dimer', 'Magnesium', 'Phosphate'}


def _matches(sent):
    """every result in a sentence: (start, end, analyte, value, unit), overlaps resolved left to right"""
    hits = []
    for rx, a in RX:
        for m in rx.finditer(sent):
            if NOISE.search(sent[max(0, m.start() - 28):m.start(2)]): continue
            unit = m.group(3) or ''
            if not unit and a[2]:
                if a[1] in NEED_UNIT or not BARE_OK.match(sent[m.end():]): continue
            hits.append((m.start(), m.start() + len(m.group(0).rstrip()), a, m.group(2), unit, (m.group(4) or '').replace('-', '–').replace(' ', '')))
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    out, at = [], -1
    for h in hits:
        if h[0] >= at: out.append(h); at = h[1]
    return out


def _sentences(s):
    return [x for x in re.split(r'(?<=[.!?])\s+(?=[A-Z(])', s.strip()) if x.strip()]


EXAM = re.compile(r'\b(temperature|pulse|heart rate|\bBP\b|blood pressure|mmHg|bpm|respiratory rate|saturation|SpO2|on examination|examination (?:shows|reveals|finds)|auscultation|palpable|crackles|murmur|GCS|Glasgow|tender|JVP|oedema|abdomen is|chest is)\b', re.I)


def _obs(t):
    t = re.sub(r'(\d+(?:\.\d)?) ?°C', r'\1°C', t)
    t = re.sub(r'\b(?:heart rate|pulse rate|pulse)( is| of)? (\d{2,3})(?: ?bpm)?\b', r'pulse rate\1 \2 bpm', t)
    t = re.sub(r'\bblood pressure( is| of)? (\d{2,3}/\d{2,3})(?: ?mmHg)?', r'BP\1 \2 mmHg', t)
    t = re.sub(r'\bBP( is| of)? (\d{2,3}/\d{2,3})(?! ?mmHg)', r'BP\1 \2 mmHg', t)
    t = re.sub(r'\brespiratory rate( is| of)? (\d{1,2})(?: ?/min| breaths per minute| breaths/min)?\b', r'respiratory rate\1 \2 breaths per minute', t)
    t = re.sub(r'\b(?:oxygen saturations?|saturations|sats)( are| is| of)? (\d{2,3}) ?%', lambda m: 'SpO2' + (' is' if m.group(1) else '') + ' ' + m.group(2) + '%', t)
    return t


def _lead(q):
    q = q.strip()
    q = re.sub(r'^What is the most\b', 'Which is the most', q)
    q = re.sub(r'^What is the best\b', 'Which is the most appropriate', q)
    q = re.sub(r'^What would be the most\b', 'Which is the most', q)
    q = re.sub(r'^What (?=[a-z]+(?: [a-z]+)? (?:is|are|would|should|will|best|most)\b)', 'Which ', q)
    q = re.sub(r'^What is the (first|next|initial|immediate|definitive|single) ', r'Which is the most appropriate \1 ', q) if re.match(r'^What is the (first|next|initial|immediate|definitive|single) (step|treatment|management|action|investigation|test|drug)', q) else q
    return q


def _nat(x):
    return [(0, float(t.replace(',', ''))) if re.fullmatch(r'\d[\d,]*(?:\.\d+)?', t) else (1, t.lower()) for t in re.findall(r'\d[\d,]*(?:\.\d+)?|\D+', x)]


def _order(o):
    """alphabetical with numbers compared as numbers; a list the writer ordered by size (three or more options with numbers in them) is kept"""
    if sum(bool(re.search(r'\d', x)) for x in o) >= 3 and not all(re.match(r'\s*[<>≤≥]?\d', x) for x in o): return list(range(len(o)))
    return sorted(range(len(o)), key=lambda i: _nat(o[i]))


def _art(m):
    n = m.group(2); v = n.startswith('8') or n in ('11', '18')
    w = 'an' if v else 'a'
    return (w.capitalize() if m.group(1)[0] == 'A' else w) + ' ' + n


def fmt(q):
    s = re.sub(r'\b(\d+)-(year|month|week|day)-old\b', r'\1 \2 old', q['s'])
    s = re.sub(r'\b([Aa]n?) (\d+)(?= (?:year|month|week|day) old)', _art, s)
    s = re.sub(r'(?<!\w)[x×] ?10\^?9/L', '× 10⁹/L', s)
    sex = _sex(s)
    ql = q.get('ql', '')
    if not ql:
        m = re.search(r'((?:Which|What|How|Where|When|Who|Why|In which|In what|At what|To what)[^?]*\?)\s*$', s)
        if m and s[:m.start()].strip(): ql, s = m.group(1), s[:m.start()].strip()
    ql = _lead(ql) if ql else ql
    explicit = '\n' in s.strip()
    lab = [list(r) for r in (q.get('lab') or [])]
    pre, post, tab_at = [], [], None   # lists of paragraphs, each a list of sentences
    for para in [p for p in s.split('\n') if p.strip()] if explicit else [s]:
        cur_pre, cur_post = [], []
        for x in [_obs(x) for x in _sentences(para)]:
            x = re.sub(r'\bInvestigations?:\s*', '', x) if tab_at is None and len(_matches(x)) >= 3 else x
            hs = _matches(x)
            left = x
            for h in reversed(hs): left = left[:h[0]] + left[h[1]:]
            leftover = FILL.sub('', re.sub(r'\([^)]*\)', '', left))
            if len(hs) >= 3 and len(leftover) <= 12 and tab_at is None:
                for h in hs:
                    a = h[2]; unit = h[4] or a[2]
                    lab.append([a[1], (h[3] + (' ' + unit if unit else '')).strip(), h[5] or _range(a, sex)])
                note = re.search(r'\(([^)]*AKI[^)]*)\)', x)
                if note: cur_post.append(note.group(1)[0].upper() + note.group(1)[1:] + '.')
                tab_at = len(pre)
                continue
            if hs:
                for h in reversed(hs):
                    a = h[2]; rg = _range(a, sex); unit = h[4]
                    if not rg or h[5]: continue
                    add = ('' if unit or not a[2] else ' ' + a[2]) + ' (' + rg + ')'
                    x = x[:h[1]].rstrip() + add + x[h[1]:]
            (cur_post if tab_at is not None else cur_pre).append(x)
        if cur_pre: pre.append(cur_pre)
        if cur_post: post.append(cur_post)
    if explicit:
        paras = [' '.join(p) for p in pre]
    else:
        # history, then a fresh paragraph at the first observation or examination sentence
        flat_pre = [x for p in pre for x in p]
        paras, cur = [], []
        for i, x in enumerate(flat_pre):
            if i and cur and EXAM.search(x) and not any(EXAM.search(y) for y in cur): paras.append(' '.join(cur)); cur = []
            cur.append(x)
        if cur: paras.append(' '.join(cur))
    post = ['\n'.join(' '.join(p) for p in post)] if post else []
    q['s'] = '\n'.join(paras)
    q['post'] = post[0] if post else ''
    q['ql'] = ql
    for r in lab:
        r[1] = re.sub(r'\s*;\s*$', '', r[1])
        if not r[2] and re.match(r'^-?\d', r[1]):
            a = next((a for rx, a in RX if re.fullmatch(r'(?i)(?:serum |plasma )?(?:' + a[0] + ')', r[0].strip())), None)
            if a and not re.match(r'(?i)csf|urin|pleural|fluid', r[0]): r[2] = _range(a, sex) or ''
    if lab: q['lab'] = lab
    # options: alphabetical, numbers ascending, as in the papers
    order = _order(q['o'])
    if order != list(range(len(order))):
        q['pm'] = [order.index(i) for i in range(len(order))]
        q['o'] = [q['o'][i] for i in order]
        q['a'] = q['pm'][q['a']]
    return q


FOOT = re.compile(r'\s*©\s*Medical Schools Council[^.]*?(?:Page \d+ of \d+)?\s*$|\s*Page \d+ of \d+\s*$')


VDIR = __import__('pathlib').Path(__file__).resolve().parent / 'vignettes'


def vignettes():
    """v2.7.1: full MSCAA-length rewrites of the Hammer stems, one block per question:
    @id, then one line per paragraph, then ?the lead-in. Options, answer, why and flip are untouched."""
    V, cur = {}, None
    for f in sorted(VDIR.glob('*.txt')):
        for n, ln in enumerate(open(f, encoding='utf-8'), 1):
            ln = ln.rstrip()
            if not ln or ln.startswith('#'): continue
            if ln.startswith('@'):
                cur = ln[1:].strip()
                if cur in V: raise SystemExit(f'{f.name}:{n} duplicate vignette {cur}')
                V[cur] = {'p': [], 'q': ''}
            elif ln.startswith('?'): V[cur]['q'] = ln[1:].strip()
            else: V[cur]['p'].append(ln.strip())
    for k, v in V.items():
        if not v['p'] or not v['q'].endswith('?'): raise SystemExit(f'vignette {k} needs paragraphs and a lead-in ending in ?')
    return V


def apply(D):
    V = vignettes()
    ids = {q['id'] for q in D['hq']['q']}
    bad = [k for k in V if k not in ids]
    if bad: raise SystemExit('vignettes for unknown ids: ' + ' '.join(bad[:10]))
    for q in D['hq']['q']:
        if q['id'] in V:
            q['s'] = '\n'.join(V[q['id']]['p']); q['ql'] = V[q['id']]['q']; q.pop('lab', None); q['vg'] = 1
    for q in D['hq']['q']: fmt(q)
    for q in D['mock']['q']: fmt(q)
    for q in D['off']['q']:
        for k in ('w', 's', 'post', 'ql'):
            if q.get(k): q[k] = re.sub(r'\s*(?:Copyright\s*)?©\s*(?:\d{4}\s*-?\s*)?Medical Schools Council(?:\s*\d{4})?\s*(?:Page \d+ of \d+)?', '', q[k]).strip()
        lab = q.get('lab') or []
        for r in lab:
            m = re.match(r'^(.*?\S)\s*\((\d[^)]*)\)\s*(Mean cell volume \(MCV\))\s*(.*)$', r[1])
            if m:  # one PDF row swallowed the next one
                i = lab.index(r); lab.insert(i + 1, ['Mean cell volume (MCV)', m.group(4), r[2]]); r[1], r[2] = m.group(1), m.group(2); break
        q['lab'] = [r for r in lab if r[0].strip() and r[0].strip().lower() != 'today' or r[1].strip()]
