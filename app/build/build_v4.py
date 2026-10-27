#!/usr/bin/env python3
"""medengine-OSCE v1.3 data: one station = one task, in the FFP station types.

Reads osce_data_v3.json (units, packs, frames, past-paper stations) and the new content in c4/, and writes
osce_data_v4.json. Past-paper stations that packed a history, an examination, results and counselling into 10
minutes are split: the history becomes a history station (same id), the explanation becomes its own talking
station (id + '-x'), and the examination findings become practice cases on the matching FFP examination."""
import json, re, pathlib, sys, copy
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from c4.common import STATIONS
from c4 import exams_med, exams_surg, exams_spec, procs, drugs, talk  # noqa: F401 (registers stations)
from c4.frames import FRAMES
from c4.redflags import RF, URG
from c4.skeletons import SKEL
from c4.exams_surg import MSK_HOOKS
from c4.drugs import FRAME as DRUG_FRAME
from c4 import posters as POSTERS

# v2.0: the hand and wrist and the shoulder examinations are not in the FFP CPSA, so they leave the app
NOT_IN_EXAM = {'E-hand', 'E-shoulder'}
SNAPDIR = HERE.parent.parent / 'study' / 'snap'

D = json.load(open(HERE / 'osce_data_v3.json', encoding='utf-8'))
OUT = HERE / 'osce_data_v4.json'

TYPES = ['hx', 'ex', 'img', 'drug', 'comm', 'proc', 'psych']
HXS = {'History', 'Open', 'Explore', 'Collateral', 'Drug history', 'Med history', 'Allergy', 'Medication review', 'ICE', 'Impact',
       'Screen', 'Intent', 'Risk', 'Risks', 'Protective', 'Mood', 'Psychosis', 'OCD', 'PTSD', 'Assess', 'MSE', 'CAGE', 'Quantify',
       'Dependence', 'Sexual', 'Current', 'Existing', 'Worries', 'Smoking', 'First', 'Knowledge', 'Brother', 'Wife', 'Perception'}
DROP = {'Examine', 'Exam', 'Examination', 'Interpret', 'ECG', 'X-ray', 'CXR', 'AXR', 'CT', 'ABG', 'ABPI', 'CBG', 'PEFR', 'Venepuncture',
        'Procedure', 'Cannula', 'A–E', 'Airway', 'Breathing', 'Circulation', 'Disability', 'Exposure', 'Danger', 'CPR', 'Arrest', 'ROSC',
        'Rhythm', 'Shock', 'Inspect', 'Feel', 'Look', 'Move', 'Special', 'Fundoscopy', 'Fields', 'Snellen', 'Rinne', 'Weber', 'Pupils',
        'Eyes', 'Neck', 'Praecordium', 'Pulse', 'Auscultate', 'Gait', 'Thomas', 'Trendelenburg', 'Range', 'Kidneys', 'Feet', 'Results',
        'LFTs', 'Describe', 'Form', 'Practical', 'Calculate', 'Chart', 'Prescribe', 'Convert', 'Once-only', 'Regular', 'PRN',
        'Breakthrough', 'PCA', 'Epidural', 'Fluids', 'VTE', 'Handover', 'SBAR', 'Reassess', 'Escalate', 'Score', 'Ix', 'Stoma', 'LP',
        'NIV', 'Aminophylline', 'Theophylline', 'Present', 'Reason', 'Reasoning', 'Differential', 'Formulate', 'Conclude', 'Thyroid',
        'Signs', 'Treat', 'Act', 'Protect', 'Sign'}
HX_DOM = re.compile(r'^(Information gathering|Communication|Clinical reasoning|Professional|Safety)', re.I)
EXPL_DOM = re.compile(r'^(Information giving|Management|Communication|Professional|Leadership|ReSPECT)', re.I)
DRUG_PP = {'PP13', 'PP39', 'PP63', 'PP73', 'PP106', 'PP03', 'PP50'}
EXMAP = {'cvs': 'E-cvs', 'resp': 'E-resp', 'abdo': 'E-abdo', 'cn': 'E-cn', 'ul': 'E-ul', 'll': 'E-ll', 'thyroid': 'E-thyroid',
         'breast': 'E-breast', 'scrotal': 'E-scrotal', 'knee': 'E-knee', 'hip': 'E-hip',
         'ent': 'E-ear', 'eye': 'E-eye', 'nodes': 'E-nodes', 'dre': 'E-dre', 'mse': 'PP61', 'skin': 'E-rash', 'bp': 'P-bpm'}
PRMAP = {'bpm': 'P-bpm', 'scrub': 'P-wash', 'cbg': 'P-cbg', 'inhaler': 'P-inhaler', 'pefr': 'P-pefr', 'obs': 'P-obs', 'ecg12': 'P-ecg12',
         'ecg3': 'P-ecg3', 'dip': 'P-dip', 'cann': 'P-cann', 'venep': 'P-venep', 'abg': 'P-abg', 'swab': 'P-swab', 'catm': 'P-catm',
         'catf': 'P-catf', 'fundo': 'E-fundo', 'otoscopy': 'E-ear'}
CASE_TO = {'PP70': 'E-lesion', 'PP71': 'E-rash', 'PP72': 'E-rash', 'PP74': 'E-rash', 'PP87': 'E-elbow', 'PP43': 'E-genit',
           'PP104': 'E-scrotal', 'PP60': 'E-ear', 'PP75': 'E-eye', 'PP76': 'E-eye', 'PP77': 'E-eye', 'PP78': 'E-fundo', 'PP80': 'E-nodes'}
HX_TASK = 'Take a focused history. At about 8 minutes, stop and present to the examiner: a one-line summary, the most likely diagnosis with your reasoning, what you would exclude, and the first investigations.'
PSY_TASK = 'Take a focused psychiatric history including risk, then present your summary, likely diagnosis, risk level and plan to the examiner.'
PRES_DOM = {'h': 'Presenting to the examiner', 'items': [
    {'t': 'Clear one-line summary with the key positives and negatives', 'f': 1},
    {'t': 'Most likely diagnosis with the clue that supports it', 'w': 2, 'f': 1},
    {'t': 'Names the dangerous alternative and how to exclude it', 'w': 2},
    {'t': 'Sensible first investigations'}]}
RESULTY = re.compile(r'\b(ECG|X-ray|CXR|CT|ultrasound|USS|results?|bloods? show|findings|troponin|reading|readings|spirometry|audiogram|scan)\b', re.I)


def nob(x):
    """Brackets hide key words for this reader: turn '(x)' into ', x'."""
    x = re.sub(r'\s*\(([^()]*)\)', lambda m: ', ' + m.group(1), x or '')
    return re.sub(r',\s*([.;:,])', r'\1', x).replace('(', '').replace(')', '')


def clean_t(t):
    """'Palpitations at work: sinus tachycardia vs SVT vs AF' → 'Palpitations at work'."""
    head = t.split(':')[0]
    head = re.sub(r'\s*\((?:[^()]*)\)', '', head)
    head = re.sub(r'\s*(\+|and)\s*(history|examination|exam|ECG|results?|plan|management|prescrib\w*|venepuncture|bloods|interpret\w*|explain\w*|counsel\w*)\b.*$', '', head, flags=re.I)
    head = re.sub(r'^(History|Digital rectal examination|Prescribing|Drug history)\s*\+\s*', '', head, flags=re.I)
    return head.strip(' +') or t


def door_setting(info):
    """Keep the setting sentences of a past-paper door, drop the multi-task instructions."""
    s = re.split(r'\s*(?:Tasks?:|Variant A:)', info)[0].strip()
    sents = re.split(r'(?<=[.!?])\s+', s)
    keep = [x for x in sents if not re.match(r'^(Take|Perform|Examine|Interpret|Explain|Counsel|Assess|Conduct|Review|Measure|Prescribe|Request|Ask|Discuss|Describe|State|Confirm|Diagnose|List)\b', x)]
    return ' '.join(keep).strip()


def dxlist(st):
    seen = []
    for v in st.get('vars', []):
        if v['dx'] not in seen: seen.append(v['dx'])
    return seen


def make_hx(s, psych):
    st = copy.deepcopy(s)
    st['type'] = 'psych' if psych else 'hx'
    st['t0'] = s['t']
    st['t'] = clean_t(s['t'])
    st['sub'] = ' · '.join(dxlist(s))
    setting = door_setting(s['info'])
    st['info'] = (setting + ' ' if setting else 'You are an FY1. ') + ('' if psych else '')
    st['info'] = st['info'].strip()
    st['task'] = PSY_TASK if psych else HX_TASK
    for v in st['vars']:
        if v.get('d'): v['d'] = door_setting(v['d']) or setting
        if not psych: v.pop('r', None)
    if not psych:
        st['script'] = [r for r in s['script'] if r['s'] in HXS]
        for v in st['vars']:
            st['script'].append({'s': 'Present', 'v': v['k'], 'say': 'The most likely diagnosis is ' + v['dx'][0].lower() + v['dx'][1:] + ', because ___. I would like to exclude ___.', 'why': 'Say the diagnosis and the clue that supports it: the reasoning mark.'})
        doms = [dm for dm in s['dom'] if HX_DOM.match(dm['h']) and not re.match(r'^Clinical reasoning', dm['h'], re.I)]
        reason = [dm for dm in s['dom'] if re.match(r'^Clinical reasoning', dm['h'], re.I)]
        pres = copy.deepcopy(PRES_DOM)
        for dm in reason: pres['items'] = [it for it in dm['items'] if not RESULTY.search(it['t'])] + pres['items']
        st['dom'] = doms + [pres]
        st['mv'] = {v['k']: 'In summary, ___. ' + v['x'] for v in st['vars']}
        st['money'] = 'So in summary, ___ is a ___-year-old with ___. The most likely diagnosis is ___ because ___. I would like to exclude ___, and my first investigations would be ___.'
        st['trap'] = [t for t in s['trap'] if not re.search(r'examin|ECG|X-ray|interpret', t, re.I)]
    st['fr'] = ['mhx'] if psych else ['hx']
    st['ex'] = []; st['pr'] = []
    return st


def make_twin(s, kind):
    lines = [r for r in s['script'] if r['s'] not in HXS and r['s'] not in DROP]
    doms = [dm for dm in s['dom'] if EXPL_DOM.match(dm['h'])]
    if len(lines) < 2 or not doms: return None
    st = copy.deepcopy(s)
    st['id'] = s['id'] + '-x'
    st['twin'] = 1
    st['type'] = kind
    st['t0'] = s['t']
    st['t'] = 'Explain: ' + clean_t(s['t'])
    st['sub'] = ' · '.join(dxlist(s))
    setting = door_setting(s['info'])
    st['info'] = (setting + ' ' if setting else 'You are an FY1. ') + 'You have already taken the history and the results are on the card.'
    st['task'] = 'Explain the diagnosis and the plan to the patient in plain words, check their understanding and answer their questions.'
    for v in st['vars']:
        v['d'] = (setting + ' ' if setting else '') + v['who'] + ' has ' + v['dx'][0].lower() + v['dx'][1:] + '.'
    st['script'] = lines
    st['dom'] = doms
    st['fr'] = ['expl']
    st['ex'] = []; st['pr'] = []
    return st


def make_talk(s, kind):
    st = copy.deepcopy(s)
    st['type'] = kind
    st['t0'] = s['t']
    st['t'] = clean_t(s['t']) if ':' in s['t'] else s['t']
    st['sub'] = ' · '.join(dxlist(s))
    st['script'] = [r for r in s['script'] if r['s'] not in DROP or r['s'] in ('Treat', 'Act')]
    st['dom'] = [dm for dm in s['dom'] if not re.match(r'^(Examination|Procedure)', dm['h'], re.I)]
    st['ex'] = []; st['pr'] = []
    return st


SKEL_OF = {**{k: 'exam' for k in ('E-cvs', 'E-resp', 'E-abdo', 'E-thyroid', 'E-nodes')}, 'E-cn': 'cn', 'E-ul': 'neuro', 'E-ll': 'neuro',
           **{k: 'msk' for k in ('E-ankle', 'E-elbow', 'E-hand', 'E-knee', 'E-shoulder', 'E-hip')},
           **{k: 'intimate' for k in ('E-breast', 'E-scrotal', 'E-dre', 'E-genit')}, 'E-rash': 'skin', 'E-lesion': 'skin',
           **{k: 'senses' for k in ('E-nose', 'E-mouth', 'E-ear', 'E-anteye', 'E-eye', 'E-fundo')}, 'C-bbn': 'bbn'}
SKEL_TYPE = {'hx': 'hx', 'psych': 'psych', 'proc': 'proc', 'drug': 'counsel', 'comm': 'comm', 'img': 'img', 'ex': 'exam'}
# hooks the skeleton now carries, so the station card only holds what is special to it
DROP_HOOK = {MSK_HOOKS[0], DRUG_FRAME}
DROP_FIRST = {'E-cvs', 'E-ul', 'E-ll', 'E-breast', 'E-anteye', 'C-bbn', 'Y-mhx', 'Y-risk'}
DROP_TWO = {'E-cn', 'C-expl'}
ADD_HOOK = {
  'E-cvs': ['**AS = SAD:** severe aortic stenosis gives Syncope, Angina, Dyspnoea, with a slow-rising pulse and a soft second sound.'],
  'E-abdo': ['**Big liver, 3 Cs:** Cirrhosis early on, Cancer, Congestion from right heart failure.', '**Liver signs, hands to feet:** flap, white nails, red palms, yellow eyes, spider naevi, breasts in men, ascites, big spleen, ankle swelling.'],
  'E-resp': ['**Clubbing is never COPD alone:** think cancer, fibrosis, bronchiectasis, empyema.'],
  'E-knee': ['**Unhappy triad:** ACL, MCL and medial meniscus torn together by a twist on a planted foot.'],
  'E-ul': ['**SWIFT before you touch:** Scars, Wasting, Involuntary movements, Fasciculations, Tremor.'],
  'E-ll': ['**Gait last:** walk, heel-toe, Romberg. Romberg falls with eyes closed = sensory; wobbly with eyes open = cerebellar.'],
  'E-scrotal': ['**Lump: S S S C T F, then the 3 questions.**'],
  'E-nodes': ['**Lump: S S S C T F:** Site, Size, Shape, Consistency, Tenderness, Fixation.'],
  'D-alc': ['**CAGE, then count the units:** 2 or more yes = likely dependence.'],
}
EXTRA_DG = {
  'E-cvs': ['jvp', 'cvshands', 'clubbing'], 'E-resp': ['clubbing'], 'E-abdo': ['liversigns'], 'E-thyroid': ['lidlag'], 'E-nodes': ['lump'],
  'E-ul': ['swift', 'myoUL', 'danish'], 'E-ll': ['swift', 'myoLL', 'plantar'], 'E-cn': ['rapd'],
  'E-knee': ['kneetests'], 'E-hip': ['leglength'], 'E-ankle': ['simmonds'], 'E-hand': ['handjoints'],
  'E-breast': ['lump'], 'E-scrotal': ['lump'], 'E-ear': ['otoscope'], 'E-eye': ['confront', 'rapd'], 'E-anteye': ['rapd'],
  'P-cann': ['cannangle'], 'P-bpm': ['cuff'], 'P-catm': ['cathM'], 'P-catf': ['cathF'],
  'D-ins': ['insulin'], 'D-acoag': ['doac'], 'D-alc': ['cage', 'units'],
  'I-ecg': ['ecgrate', 'axis', 'ecgblocks'], 'I-cxr': ['hfcxr'], 'I-ct': ['ctwin'],
  'Y-mhx': ['sigecaps', 'digfast', 'cage'], 'Y-risk': ['sadpersons'], 'PP61': ['aseptic'], 'PP65': ['sadpersons'],
}
RF_DG = {'chest': ['chestpain', 'socrates'], 'palp': ['palpit'], 'vasc': ['legswell'], 'sob': ['sobtime'], 'lungca': ['ng12', 'sobtime'], 'ugi': ['ng12', 'abdopain'], 'lgi': ['ng12', 'abdopain'],
         'abdo': ['abdopain', 'socrates', 'sepsis'], 'breast': ['ng12', 'lump'], 'dm': ['insulin'], 'thyroid': ['lump'], 'uro': ['ng12'],
         'scrot': ['lump'], 'head': ['headache', 'socrates'], 'neuro': ['tunafish'], 'msk': ['tunafish', 'handjoints'],
         'psych': ['sigecaps', 'digfast', 'sadpersons', 'cage'], 'skin': ['ng12'], 'ent': ['ng12'], 'eye': ['rapd'], 'gen': ['sepsis', 'ng12']}
RF_OF_U = {}
for _sh in RF:
    for _u in _sh['u']: RF_OF_U.setdefault(_u, []).append(_sh['id'])
STOP = set('that this with from your have what about they them their then when were been into does over more than also some only just very will would could should there which where while after before'.split())


def toks(x):
    return {w for w in re.findall(r"[a-z]{4,}", (x or '').lower()) if w not in STOP}


def _pool(rows):
    return [(toks((r.get('t') or '') + ' ' + (r.get('say') or '') + ' ' + (r.get('why') or '') + ' ' + (r.get('s') or '')), r) for r in rows if r.get('say') or r.get('why')]


FRAME_POOL = []


def _best(a, pool, need):
    best, sc = None, 0
    for b, r in pool:
        k = len(a & b)
        v = k / len(a) if (k >= 2 or len(a) == 1) else 0
        if v > sc: best, sc = r, v
    return best if sc >= need else None


GEN_I = [
  (r'one-line summary|concise summary|^summar', 'So, to summarise: a ___-year-old with ___, the key positives are ___ and importantly no ___.', 'One sentence with the positives and the negatives that matter shows the examiner your thinking.'),
  (r'first investigations|^investigations|bloods', 'I would like to start with bedside tests, then bloods, then imaging: ___.', 'Each test should answer a question; say which one.'),
  (r'differential|diagnosis', 'The most likely diagnosis is ___ because ___. The important one to exclude is ___.', 'Say the diagnosis and the clue that clinches it, then the dangerous alternative.'),
  (r'follow.?up', 'Let\'s book a review in ___ to see how things are going.', 'A specific follow-up date closes the loop.'),
  (r'chunks? and checks?|checks understanding|teach.?back', 'Does that make sense so far? ... Could you tell me in your own words what we\'ve agreed?', 'Chunk and check, then teach-back: the strongest Information-giving marks.'),
  (r'\bice\b|ideas|concerns|knowledge and fear', 'What have you been thinking might be going on? Is anything worrying you in particular?', 'The actor has a hidden worry waiting to be asked.'),
  (r'^fh$|family', 'Does anything run in the family?', 'Family history unlocks risk.'),
  (r'^pmh$|past medical|previous episodes|cardiac history', 'Have you had any other medical problems, or anything like this before?', 'The past often explains the present: MJ THREADS.'),
  (r'^sh\b|social|smoking|alcohol|occupation', 'Do you smoke? How much do you drink in a week? What do you do for work? Who is at home?', 'SADDO: Smoking, Alcohol, Drugs, Driving, Occupation.'),
  (r'drug|medication|allerg|adherence', 'What medicines do you take, including any you buy yourself? Any allergies?', 'Drug causes are a favourite twist; ask the allergic reaction too.'),
  (r'non.?judgement|respect|dignity|empath|calm', 'That sounds really difficult. Thank you for telling me.', 'Name the emotion and stay non-judgemental: Communication 3 becomes 4.'),
  (r'jargon', 'That means ___, in plain words.', 'Every unexplained term costs a Communication mark.'),
  (r'answers questions|invites questions', 'What questions do you have for me?', 'The actor has a briefed question; you need to answer it to score.'),
  (r'open question|listens|allows time', 'In your own words, what\'s been happening?', 'Open first, then let them talk.'),
  (r'structured|before, during, after', 'Tell me what happened before, during and after.', 'A clear order the examiner can follow scores Organisation.'),
  (r'lifestyle|diet|exercise|weight', 'Small changes like ___ make a real difference. Which feels doable for you?', 'Advice tied to their life, agreed with them.'),
  (r'risk factors', 'Do you smoke, have high blood pressure, diabetes, or high cholesterol?', 'Risk factors move the probability.'),
  (r'warning shot', 'I\'m afraid the results are not what we hoped.', 'A warning shot prepares them for the news.'),
  (r'consent', 'Is it OK if I go ahead?', 'Consent before anything else.'),
  (r'chaperone', 'Would you like a chaperone with us?', 'Offering a chaperone is a professionalism must.'),
  (r'safety.?net', 'If you get ___, call 999 or come straight back.', 'Specific safety-netting is a safety mark.'),
  (r'leaflet', 'I\'ll give you a leaflet to take away.', 'Written information backs up what you said.'),
  (r'pregnan', 'Is there any chance you could be pregnant?', 'Pregnancy changes tests and treatment.'),
  (r'analgesia|pain relief', 'Let\'s get your pain under control first.', 'Analgesia early is good care and a mark.'),
  (r'management options|options', 'There are a few options; let me go through them and see what suits you.', 'Shared decision-making.'),
]


def gen_info(t):
    tl = t.lower()
    for rx, say, why in GEN_I:
        if re.search(rx, tl): return {'say': say, 'why': why}
    return None


def attach_info(st):
    """Give each past-paper mark-scheme item the words and the why from the closest script line, else the closest skeleton line."""
    pool = _pool(st.get('script', []))
    n = 0
    for dm in st.get('dom', []):
        for it in dm['items']:
            if it.get('say') or it.get('why'): continue
            a = toks(it['t']) or {it['t'].lower()}
            r = _best(a, pool, 0.34) or gen_info(it['t']) or _best(a, FRAME_POOL, 0.5)
            if r:
                if r.get('say'): it['say'] = r['say']
                if r.get('why'): it['why'] = r['why']
                n += 1
    return n


def finish(out):
    got = tot = 0
    fr = dict(D['frames']); fr.update(FRAMES)
    for k in ('open', 'xopen', 'hx', 'mhx', 'pres', 'close', 'hxclose'):
        FRAME_POOL.extend(_pool([it for sc in fr[k]['secs'] for it in sc['items']]))
    for st in out:
        sid, ty = st['id'], st['type']
        k = SKEL_OF.get(sid) or ('bbn' if 'bbn' in st.get('fr', []) and ty == 'comm' else SKEL_TYPE[ty])
        st['skel'] = k
        if st.get('hooks'):
            h = [x for x in st['hooks'] if x not in DROP_HOOK]
            if sid in DROP_FIRST: h = h[1:]
            if sid in DROP_TWO: h = h[2:]
            st['hooks'] = ADD_HOOK.get(sid, []) + h
        if ty in ('hx', 'psych'):
            ids = []
            for u in st.get('u', []):
                for r in RF_OF_U.get(u, []):
                    if r not in ids: ids.append(r)
            if ty == 'psych' and 'psych' not in ids: ids.insert(0, 'psych')
            st['rf'] = ids[:2]
        dg = list(st.get('dg', []))
        for x in EXTRA_DG.get(sid, []):
            if x not in dg: dg.append(x)
        if ty in ('hx', 'psych') and not st.get('core'):
            for r in st.get('rf', []):
                for x in RF_DG.get(r, []):
                    if x not in dg and len(dg) < 4: dg.append(x)
            nm = ' '.join(D['units'][u]['name'].lower() for u in st.get('u', []) if u < len(D['units']))
            if 'alcohol' in nm or 'alcohol' in st['t'].lower():
                for x in ('cage', 'units'):
                    if x not in dg: dg.insert(0, x)
                dg = dg[:4]
        if dg: st['dg'] = dg
        if st.get('pp'):
            tot += sum(len(dm['items']) for dm in st.get('dom', []))
            got += attach_info(st)
    for u in range(len(D['units'])): assert u in RF_OF_U, 'no red-flag sheet for unit %d' % u
    for st in out: assert st['skel'] in SKEL, st['id']
    print('i attached', got, 'of', tot, 'past-paper items')


def main():
    by = {s['id']: s for s in STATIONS}
    out, cases = [], {}
    for s in D['stations']:
        if not s.get('pp'): continue
        fr = set(s['fr'])
        hx = bool({'hx', 'mhx'} & fr)
        psych = 'mhx' in fr
        if hx:
            out.append(make_hx(s, psych))
            if {'expl', 'counsel', 'bbn'} & fr and not psych:
                tw = make_twin(s, 'drug' if s['id'] in DRUG_PP or 'counsel' in fr else 'comm')
                if tw: out.append(tw)
        elif fr <= {'expl', 'counsel', 'bbn', 'prof', 'plan', 'ebm', 'di'} and fr & {'expl', 'counsel', 'bbn', 'prof'}:
            out.append(make_talk(s, 'drug' if s['id'] in DRUG_PP else 'comm'))
        elif s['id'] == 'PP03':
            tw = make_twin(s, 'drug')
            if tw: tw['t'] = 'Explain: new AF and anticoagulation'; out.append(tw)
        # examination findings → practice cases on the FFP examination
        targets = [CASE_TO[s['id']]] if s['id'] in CASE_TO else [EXMAP[e] for e in s['ex'] if EXMAP.get(e, '').startswith('E-')]
        if 'ex' in fr or s['id'] in CASE_TO:
            for tid in targets:
                for v in s['vars']:
                    if v.get('r'): cases.setdefault(tid, []).append({'dx': nob(v['dx']), 'f': nob(v['r']), 'p': nob((s.get('mv') or {}).get(v['k']) or v['x']), 'src': s['id']})
    # PP61 and PP65 are the FFP MSE and suicide risk stations
    for st in out:
        if st['id'] == 'PP61': st.update(t='Mental state examination', ffp='MSE', core=1)
        if st['id'] == 'PP65': st.update(t='Suicide risk assessment', ffp='Suicide Risk Assessment', core=1)
    # bank history stations → single-task history or psych stations
    seen_t = {st['t'].lower() for st in out}
    for s in D['stations']:
        if s.get('pp') or not ({'hx', 'mhx'} & set(s['fr'])): continue
        psych = 'mhx' in s['fr'] or s['g'] == 'MH'
        st = {k: s[k] for k in ('id', 'g', 't', 'u', 'k') if k in s}
        if st['t'].lower() in seen_t: continue
        seen_t.add(st['t'].lower())
        sents = re.split(r'(?<=[.!?])\s+', s['info'])
        st['info'] = ' '.join(x for x in sents if not RESULTY.search(x)).strip() or sents[0]
        st['task'] = PSY_TASK if psych else HX_TASK
        st['type'] = 'psych' if psych else 'hx'
        st['fr'] = ['mhx' if psych else 'hx', 'pres']
        st['ex'] = []; st['pr'] = []
        if s.get('cmp'): st['cmp'] = s['cmp']
        st['bank'] = 1
        out.append(st)
    # authored stations, with past-paper findings appended as extra cases
    for st in STATIONS:
        if st['id'] in NOT_IN_EXAM: continue
        st = copy.deepcopy(st)
        if st['type'] == 'ex':
            st['wrap'] = ['xopen', 'xclose']
            have = {c['dx'].lower() for c in st.get('cases', [])}
            for c in cases.get(st['id'], []):
                if c['dx'].lower() not in have and len(st.get('cases', [])) < 10:
                    st.setdefault('cases', []).append(c); have.add(c['dx'].lower())
        elif st['type'] == 'proc': st['wrap'] = ['popen', 'pclose']
        else: st['wrap'] = ['open', 'close']
        st['core'] = 1
        st['fr'] = {'ex': ['ex'], 'proc': ['proc'], 'drug': ['counsel'], 'comm': ['expl'], 'psych': ['mhx'], 'img': ['di'], 'hx': ['hx']}[st['type']]
        st['ex'] = []; st['pr'] = []
        out.append(st)

    # v1.4: skeletons, red flags, more pictures, "i" on past-paper items
    finish(out)
    ids = [s['id'] for s in out]
    assert len(ids) == len(set(ids)), [i for i in ids if ids.count(i) > 1]
    for s in out: assert s['type'] in TYPES, s['id']
    # the FFP checklist, in the order of the paper list
    FFP = [
        ('Medicine', ['Cardiovascular', 'Respiratory', 'Cranial nerve', 'PNS', 'Abdominal', 'Thyroid']),
        ('Surgery', ['MSK Ankle + Foot', 'MSK Elbow', 'MSK Knee', 'MSK Hip', 'Breast', 'Testicular', 'DRE', 'External Genitalia']),
        ('Speciality', ['Describing a rash', 'Pigmented & non-pigmented lesions', 'Nasal Cavity', 'Oral Cavity', 'Otoscopy + Hearing', 'Lymph node exam', 'Anterior Eye', 'Full Eye Exam (VA + Fields)', 'Fundoscopy']),
        ('Psychiatry', ['Mental Health History', 'MSE', 'Risk Assessment', 'Suicide Risk Assessment']),
        ('DOPS and procedures', ['BP', 'Hand washing', 'Blood glucose', 'Inhaler technique', 'Peak flow', 'Basic physiological obs', '12-lead ECG', '3-lead ECG', 'Urine dipstick', 'IV cannulation', 'Venepuncture', 'ABG', 'Swabs (viral & bacterial)', 'Male & Female Catheterisation']),
        ('Communication', ['Breaking Bad News (SPIKES)', 'Explaining a diagnosis', 'Antibiotic Stewardship']),
        ('Drug counselling', ['Asthma/COPD meds', 'Steroids', 'Hypertension drugs', 'Heart Failure drugs', 'Antipsychotics', 'Anti-depressants', 'Diabetes', 'Thyroid meds', 'Alcohol maintenance & withdrawal', 'NSAIDs & PPIs', 'Stroke prevention & anticoagulation', 'Long-term oxygen', 'QRISK & CHADSVASC-2', 'ORBIT score/falls', 'Diabetes medications']),
        ('Imaging', ['Respiratory CXR', 'Abdominal X-ray', 'Chest + Abdominal CT', '12-lead ECG interpretation']),
    ]
    ffp = []
    for sec, names in FFP:
        rows = []
        for n in names:
            sids = [s['id'] for s in out if s.get('ffp') == n]
            assert sids, 'no station for FFP item ' + n
            rows.append({'n': n, 's': sids})
        ffp.append({'h': sec, 'items': rows})
    frames = dict(D['frames']); frames.update(FRAMES)
    data = {k: D[k] for k in ('units', 'weeks', 'exams', 'dops', 'packs', 'groups', 'fw')}
    data['exams'] = [e for e in data['exams'] if e['id'] not in ('hand', 'shoulder')]
    data.update(rf=RF, urg=URG, skel=SKEL)
    # v2.0 🗺️ posters: condition posters and master posters shared with medengine-STUDY, plus routes and storyboards for stations
    sys.path.insert(0, str(SNAPDIR))
    import importlib, glob as _glob, snapdsl, master
    for _f in sorted(_glob.glob(str(SNAPDIR / 's[0-9]_*.py'))): importlib.import_module(pathlib.Path(_f).stem)
    if snapdsl.ERR: raise SystemExit('snapshot errors: ' + '; '.join(snapdsl.ERR))
    assert sorted(snapdsl.SNAP) == list(range(len(D['units']))), 'every ILO unit needs a poster'
    data['snap'] = {str(k): v for k, v in sorted(snapdsl.SNAP.items())}
    data['master'] = master.MASTER
    data['po'] = POSTERS.check(out)
    data.update(stations=out, frames=frames, ffp=ffp, exmap=EXMAP, prmap=PRMAP,
                meta={'v': 4, 'n': len(out), 'by': {t: sum(1 for s in out if s['type'] == t) for t in TYPES}})
    OUT.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print('stations', len(out), data['meta']['by'], 'bytes', OUT.stat().st_size)


if __name__ == '__main__':
    main()
