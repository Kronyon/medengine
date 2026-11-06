#!/usr/bin/env python3
"""v3.6.14: the My-mock why-not (x) and flip (f) lines that had been matched from the wrong card (an antiemetic "to prevent
rises in intraocular pressure", "UC is a continuous carpet" under a pain question, carpal tunnel under hay fever...).
Each is rewritten for its own question. Options are untouched, so saved runs are unaffected."""
import json, pathlib, re
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
m = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', s, re.S)
D = json.loads(m.group(2))
L = 'ABCDE'
FIX = [
 ('m005', 'f', 'A', 'fever, confusion and seizures with no new serotonergic drug'),
 ('m011', 'f', 'A', 'itchy flexural plaques since childhood with asthma or hay fever'),
 ('m018', 'x', 'E', 'Primary psychosis means hallucinations or fixed delusions without a trigger; this mood change began with high-dose steroids, so the steroid is the cause.'),
 ('m019', 'f', 'B', 'no new drug or illness, with elation, pressured speech and no sleep for days'),
 ('m020', 'f', 'E', 'sudden pleuritic pain with one hyperresonant side and absent breath sounds'),
 ('m022', 'f', 'B', 'nosebleeds, haematuria and cavitating nodules with a positive c-ANCA'),
 ('m023', 'f', 'D', 'the question asked which feature supports a deep vein thrombosis'),
 ('m024', 'f', 'C', 'low mood, loss of interest and poor sleep for over 2 weeks'),
 ('m025', 'f', 'C', 'low mood, loss of interest and poor sleep for over 2 weeks'),
 ('m030', 'f', 'C', 'nosebleeds with a BP of 210/120 and a normal septum'),
 ('m030', 'f', 'D', 'a slowly growing woody mass with sinuses discharging yellow sulphur granules'),
 ('m037', 'f', 'A', 'ischaemia from the splenic flexure down to the upper rectum'),
 ('m041', 'f', 'A', 'a COPD patient who is drowsy on high-flow oxygen'),
 ('m041', 'f', 'C', 'pale and breathless with a suspected bleed or anaemia'),
 ('m041', 'f', 'D', 'the question asked about fitness for a lobectomy, not the cause of acute pain'),
 ('m043', 'f', 'A', 'a COPD flare with Gram-negative coccobacilli in the sputum'),
 ('m049', 'f', 'A', 'proximal muscle pain with a very high CK'),
 ('m049', 'f', 'D', 'a high potassium and a falling eGFR soon after starting it'),
 ('m051', 'f', 'B', 'thirst, polyuria and weight loss with a high glucose'),
 ('m052', 'f', 'B', 'pituitary surgery with suspected growth hormone and ACTH deficiency'),
 ('m055', 'f', 'E', 'a rigid, silent abdomen with free gas under the diaphragm'),
 ('m059', 'f', 'A', 'jaundice with weight loss and a suspected pancreatic mass'),
 ('m061', 'f', 'E', 'lung cancer with a swollen face and arms and distended neck veins'),
 ('m065', 'f', 'A', 'after an elective total knee replacement, where NICE allows aspirin'),
 ('m066', 'f', 'A', 'morning stiffness over an hour with swollen joints that ease with movement'),
 ('m070', 'f', 'C', 'a smooth fluctuant lump that appeared suddenly in a woman in her 40s'),
 ('m072', 'f', 'C', 'a seroconversion illness with rash and sore throat weeks after unprotected sex'),
 ('m077', 'f', 'B', 'fever and low blood pressure with a urinary or chest source'),
 ('m077', 'f', 'C', 'haematuria, proteinuria and red cell casts after a sore throat'),
 ('m078', 'f', 'E', 'insulin and glucose are running and you need a second drug to shift potassium'),
 ('m080', 'f', 'B', 'heavy proteinuria and oedema in an adult with anti-PLA2R antibodies'),
 ('m082', 'x', 'E', 'Shigella gives bloody diarrhoea within days, not a high fever with a slow pulse and constipation first.'),
 ('m085', 'f', 'B', 'poor eye contact, rigid routines and no friendships since early childhood'),
 ('m086', 'x', 'C', 'Oral steroids are not used for seasonal allergic symptoms like these; an oral antihistamine comes first.'),
 ('m088', 'f', 'B', 'an older patient with iron deficiency anaemia and a right iliac fossa mass'),
 ('m089', 'x', 'D', 'A plain X-ray misses small and radiolucent stones; non-contrast CT is the most sensitive test.'),
 ('m091', 'f', 'C', 'a subarachnoid haemorrhage, to prevent delayed ischaemia'),
 ('m091', 'f', 'D', 'enhancement from an inflammatory pachymeningitis such as sarcoidosis'),
 ('m092', 'x', 'A', 'Antiemetics treat nausea and vomiting; they do not dry airway secretions, which needs an antimuscarinic such as hyoscine butylbromide.'),
 ('m092', 'f', 'C', 'agitated delirium or nausea in the last days'),
 ('m096', 'f', 'A', 'one-sided hearing loss and tinnitus with gradual imbalance'),
 ('m096', 'f', 'E', 'vertigo with double vision, slurred speech or limb ataxia'),
]
B = {q['id']: q for q in D['mock']['q']}
n = 0
for qid, kind, let, new in FIX:
    q = B[qid]; i = L.index(let); tm = q['tm']
    rows = tm['x'] if kind == 'x' else tm['f']
    hit = [r for r in rows if (r[0] if kind == 'x' else r[1]) == i]
    assert len(hit) == 1, (qid, kind, let, len(hit))
    if kind == 'x': hit[0][1] = new
    else: hit[0][0] = new
    n += 1
assert B['m079']['ql'] == 'Which the most appropriate management plan?'
B['m079']['ql'] = 'Which is the most appropriate management plan?'
s = s[:m.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + s[m.end(2):]
F.write_text(s, encoding='utf-8')
print('mock why-not and flip lines fixed:', n)
