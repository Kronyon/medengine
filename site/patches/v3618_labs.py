#!/usr/bin/env python3
"""v3.6.18: Pastest-style data reading, reverse engineered and applied to 50 Hammer questions.
What makes a good Pastest data question (and the MSCAA papers, where 34 to 38% of items carry results):
  1. Numbers, not adjectives: "calcitonin 850 ng/L (<10)" instead of "calcitonin is markedly elevated", so you read
     the value against the range yourself.
  2. Noise around the signal: the deciding value sits among normal ones, so you have to scan and triage.
  3. A trap value where real life has one: a mildly raised CRP in biliary colic, a raised LDH in testicular lymphoma,
     a PSA inside the range with a craggy prostate, an ALT under three times the limit on a statin.
  4. A staged reveal: history and examination, then the table, then the imaging line, then the question.
Only the stem changes (words moved into a table, imaging moved below it). Options, answers and explanations are
untouched, so saved runs are safe; a saved highlight on a changed sentence may need redoing."""
import json, pathlib, re
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
m = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', s, re.S)
D = json.loads(m.group(2))
W = '× 10⁹/L'
# qid: ([(old text, new text), ...], lab rows, post text or None)
R = {
 'h0121': ([(' Serum calcitonin is markedly elevated and TSH is normal.', '')],
           [['Calcitonin', '850 ng/L', '<10'], ['TSH', '1.6 mU/L', '0.3–4.2'], ['Free T4', '15 pmol/L', '12–22'], ['Adjusted calcium', '2.36 mmol/L', '2.2–2.6']], None),
 'h0123': ([(' TSH is normal.', '')], [['TSH', '1.9 mU/L', '0.3–4.2'], ['Free T4', '16 pmol/L', '12–22']], None),
 'h0125': ([(' Serum PSA and creatinine are normal.', '')], [['PSA', '2.6 ng/mL', '<4.5'], ['Creatinine', '88 µmol/L', '60–120'], ['eGFR', '79 mL/min/1.73 m²', '>60']], None),
 'h0138': ([(' Serum calcium, phosphate, parathyroid hormone and urate are normal.', '')],
           [['Adjusted calcium', '2.41 mmol/L', '2.2–2.6'], ['Phosphate', '1.05 mmol/L', '0.8–1.5'], ['PTH', '4.1 pmol/L', '1.6–6.9'], ['Urate', '0.34 mmol/L', '0.20–0.42']], None),
 'h0141': ([], [['White cell count', '17.8 ' + W, '3.8–10.0'], ['Neutrophils', '15.1 ' + W, '2.0–7.5'], ['CRP', '186 mg/L', '<5'], ['Creatinine', '74 µmol/L', '45–90'], ['Lactate', '1.6 mmol/L', '<2.0']], None),
 'h0153': ([(' Serum AFP and beta-hCG are within normal limits.', '')], [['AFP', '4 kU/L', '<10'], ['Beta-hCG', '<2 IU/L', '<5'], ['LDH', '610 U/L', '135–225']], None),
 'h0250': ([(' Abdominal examination, full blood count and serum IgA tissue transglutaminase antibody with total IgA are all normal.', ' Abdominal examination is normal.')],
           [['Haemoglobin', '128 g/L', '115–155'], ['MCV', '88 fL', '80–100'], ['Ferritin', '46 µg/L', '15–150'], ['IgA tTG antibody', '1.2 U/mL', '<7'], ['Total IgA', '2.1 g/L', '0.8–4.0']], None),
 'h0252': ([(' Blood tests show elevated serum folate, low serum vitamin B12 and negative IgA tissue transglutaminase antibodies.', '')],
           [['Haemoglobin', '108 g/L', '115–155'], ['MCV', '104 fL', '80–100'], ['Vitamin B12', '112 ng/L', '200–900'], ['Serum folate', '24.1 µg/L', '3.0–20.0'], ['IgA tTG antibody', '0.8 U/mL', '<7']], None),
 'h0257': ([(' Abdominal examination, full blood count, CRP, IgA tissue transglutaminase and faecal calprotectin are all normal, confirming diarrhoea-predominant irritable bowel syndrome.', ' Abdominal examination is normal. Diarrhoea-predominant irritable bowel syndrome is diagnosed.')],
           [['Haemoglobin', '148 g/L', '130–175'], ['CRP', '2 mg/L', '<5'], ['IgA tTG antibody', '0.9 U/mL', '<7'], ['Faecal calprotectin', '22 µg/g', '<50']], None),
 'h0258': ([(' Coeliac serology and faecal calprotectin are normal.', '')], [['IgA tTG antibody', '1.1 U/mL', '<7'], ['Total IgA', '1.9 g/L', '0.8–4.0'], ['Faecal calprotectin', '31 µg/g', '<50']], None),
 'h0520': ([(' Abdominal and rectal examinations, blood count, TSH and calcium are normal.', ' Abdominal and rectal examinations are normal.')],
           [['Haemoglobin', '131 g/L', '115–155'], ['TSH', '2.2 mU/L', '0.3–4.2'], ['Adjusted calcium', '2.34 mmol/L', '2.2–2.6']], None),
 'h0527': ([(' White cell count normal. Liver function tests normal. Ultrasound shows multiple gallstones with a normal gallbladder wall and bile duct.', '')],
           [['White cell count', '8.9 ' + W, '3.8–10.0'], ['CRP', '6 mg/L', '<5'], ['Bilirubin', '12 µmol/L', '<17'], ['ALT', '28 IU/L', '10–50'], ['ALP', '92 IU/L', '25–115'], ['Amylase', '64 U/L', '<100']],
           'Ultrasound shows multiple gallstones with a normal gallbladder wall and bile duct.'),
 'h0532': ([(' Lipase is 6 times the upper limit of normal. A diagnosis of acute pancreatitis is made.', '')],
           [['Lipase', '960 U/L', '<160'], ['White cell count', '13.4 ' + W, '3.8–10.0'], ['Bilirubin', '16 µmol/L', '<17'], ['ALT', '34 IU/L', '10–50'], ['Adjusted calcium', '2.31 mmol/L', '2.2–2.6'], ['Triglycerides', '1.6 mmol/L', '<1.7']],
           'A diagnosis of acute pancreatitis is made.'),
 'h0534': ([(' Amylase is 8 times the upper limit of normal. Triglycerides and calcium are normal. Ultrasound shows no gallstones.', '')],
           [['Amylase', '820 U/L', '<100'], ['Triglycerides', '1.4 mmol/L', '<1.7'], ['Adjusted calcium', '2.38 mmol/L', '2.2–2.6'], ['ALT', '30 IU/L', '10–50'], ['Bilirubin', '11 µmol/L', '<17']],
           'Ultrasound shows no gallstones.'),
 'h0546': ([(' Liver function tests are normal and hepatobiliary ultrasound shows a thin-walled gallbladder without calculi.', '')],
           [['White cell count', '12.1 ' + W, '3.8–10.0'], ['CRP', '64 mg/L', '<5'], ['Bilirubin', '14 µmol/L', '<17'], ['ALT', '32 IU/L', '10–50'], ['ALP', '88 IU/L', '25–115']],
           'Hepatobiliary ultrasound shows a thin-walled gallbladder without calculi.'),
 'h0577': ([(' Thyroid function and glucose are normal.', '')], [['TSH', '1.4 mU/L', '0.3–4.2'], ['Free T4', '17 pmol/L', '12–22'], ['Random glucose', '7.1 mmol/L', '<11.1'], ['Sodium', '139 mmol/L', '135–145']], None),
 'h0614': ([(' Creatinine is mildly raised.', '')], [['Creatinine', '98 µmol/L', '25–60'], ['Urea', '9.8 mmol/L', '2.5–6.5'], ['Potassium', '5.1 mmol/L', '3.5–5.3'], ['Albumin', '36 g/L', '35–50']], None),
 'h0621': ([(' White cell count normal. CRP 8 mg/L (<5). INR 6.4.', '')], [['Haemoglobin', '118 g/L', '130–175'], ['White cell count', '7.6 ' + W, '3.8–10.0'], ['CRP', '8 mg/L', '<5'], ['INR', '6.4', 'target 2.0–3.0']], None),
 'h0636': ([(' Liver function is normal.', '')], [['Bilirubin', '13 µmol/L', '<17'], ['ALT', '22 IU/L', '10–50'], ['Albumin', '39 g/L', '35–50'], ['Potassium', '5.2 mmol/L', '3.5–5.3']], None),
 'h0656': ([(' Serum electrolytes, eGFR, HbA1c and urine albumin-to-creatinine ratio are all normal.', '')],
           [['Sodium', '140 mmol/L', '135–145'], ['Potassium', '4.3 mmol/L', '3.5–5.3'], ['eGFR', '88 mL/min/1.73 m²', '>60'], ['HbA1c', '39 mmol/mol', '20–42'], ['Urine ACR', '1.1 mg/mmol', '<3.0']], None),
 'h0669': ([(' Blood tests show eosinophils 1.8 x 10^9/L (0.04-0.40), total IgE 1,450 kU/L (<100) and positive Aspergillus fumigatus-specific IgE. CT thorax shows central bronchiectasis.', '')],
           [['Eosinophils', '1.8 ' + W, '0.04–0.40'], ['Total IgE', '1450 kU/L', '<100'], ['Aspergillus fumigatus-specific IgE', 'Positive', 'Negative']], 'CT thorax shows central bronchiectasis.'),
 'h0717': ([(' Total cholesterol has fallen from 6.4 mmol/L to 4.1 mmol/L. Serum ALT is 92 IU/L (normal range 10-50 IU/L) and bilirubin is 12 micromol/L (<17).', ' His results are shown.')],
           [['Total cholesterol', '4.1 mmol/L (was 6.4)', '<5.0'], ['ALT', '92 IU/L', '10–50'], ['Bilirubin', '12 µmol/L', '<17'], ['ALP', '84 IU/L', '25–115'], ['Creatine kinase', '140 U/L', '40–320']], None),
 'h0792': ([(' Coeliac serology is negative. Faecal calprotectin is mildly raised. Colonoscopy shows a normal-looking colon, but biopsies show increased lymphocytes in the lining.', '')],
           [['Haemoglobin', '128 g/L', '115–155'], ['CRP', '3 mg/L', '<5'], ['IgA tTG antibody', '0.7 U/mL', '<7'], ['Faecal calprotectin', '86 µg/g', '<50']],
           'Colonoscopy shows a normal-looking colon, but biopsies show increased lymphocytes in the lining.'),
 'h0827': ([(' Glucose 5.2 mmol/L (4.0–7.8). Calcium is normal. After water deprivation his urine osmolality stays at 200 mOsm/kg. After desmopressin it rises to 700 mOsm/kg.', '')],
           [['Glucose', '5.2 mmol/L', '4.0–7.8'], ['Adjusted calcium', '2.39 mmol/L', '2.2–2.6'], ['Sodium', '146 mmol/L', '135–145'], ['Urine osmolality after water deprivation', '200 mOsm/kg', '>600'], ['Urine osmolality after desmopressin', '700 mOsm/kg', '']], None),
 'h0879': ([(' A pregnancy test is negative. Prolactin 1800 mU/L (100–500). Thyroid function is normal.', '')],
           [['Urine beta-hCG', 'Negative', ''], ['Prolactin', '1800 mU/L', '100–500'], ['TSH', '2.1 mU/L', '0.3–4.2']], None),
 'h0993': ([('after an incidental fasting plasma glucose of 8.6 mmol/L and HbA1c of 58 mmol/mol (20-42).', 'after an incidental raised fasting glucose.'),
            (', has a BMI of 21 kg/m2, and has negative anti-GAD, IA-2 and ZnT8 autoantibodies with a normal fasting C-peptide.', ' and has a BMI of 21 kg/m2.')],
           [['Fasting glucose', '8.6 mmol/L', '<6.1'], ['HbA1c', '58 mmol/mol', '20–42'], ['Anti-GAD antibodies', 'Negative', ''], ['IA-2 and ZnT8 antibodies', 'Negative', ''], ['Fasting C-peptide', '0.62 nmol/L', '0.26–1.03']], None),
 'h1006': ([(' TSH is <0.01 mU/L and free T4 is 48 pmol/L (12-22).', '')], [['TSH', '<0.01 mU/L', '0.3–4.2'], ['Free T4', '48 pmol/L', '12–22'], ['Free T3', '16.2 pmol/L', '3.1–6.8']], None),
 'h1101': ([(' Haemoglobin, platelets and creatinine are currently normal.', '')], [['Haemoglobin', '132 g/L', '115–155'], ['White cell count', '12.8 ' + W, '3.8–10.0'], ['Platelets', '238 ' + W, '150–400'], ['Creatinine', '71 µmol/L', '45–90']], None),
 'h1107': ([(' Platelet count, prothrombin time and activated partial thromboplastin time are all normal.', '')], [['Haemoglobin', '112 g/L', '130–175'], ['Platelets', '246 ' + W, '150–400'], ['Prothrombin time', '12.1 s', '10–14'], ['APTT', '31 s', '25–37']], None),
 'h1112': ([(' A serum IgA tissue transglutaminase antibody test sent last week is negative with a normal total serum IgA.', ' Blood tests sent last week are shown.')],
           [['IgA tTG antibody', '1.4 U/mL', '<7'], ['Total IgA', '1.8 g/L', '0.8–4.0'], ['Haemoglobin', '141 g/L', '130–175']], None),
 'h1126': ([(' Urine dipstick is normal and serum PSA is 1.2 ng/mL (<4.5).', ' Urine dipstick is normal.')], [['PSA', '1.2 ng/mL', '<4.5'], ['Creatinine', '84 µmol/L', '60–120']], None),
 'h1129': ([(' Urine dipstick is negative and serum PSA is 3.0 ng/mL (<4.5).', ' Urine dipstick is negative.')], [['PSA', '3.0 ng/mL', '<4.5'], ['Creatinine', '92 µmol/L', '60–120']], None),
 'h1130': ([('after two consecutive serum PSA measurements of 7.8 ng/mL and 8.2 ng/mL (age-specific reference <4.5).', 'after two raised PSA results.'),
            (' Midstream urine culture is negative and his eGFR is 84 mL/min/1.73 m².', ' Midstream urine culture is negative.')],
           [['PSA (first)', '7.8 ng/mL', '<4.5'], ['PSA (repeat)', '8.2 ng/mL', '<4.5'], ['eGFR', '84 mL/min/1.73 m²', '>60']], None),
 'h1133': ([(' Urine culture is sterile and white cell count is 13.2 × 10⁹/L (3.8-10.0).', ' Urine culture is sterile.')],
           [['Haemoglobin', '128 g/L', '115–155'], ['White cell count', '13.2 ' + W, '3.8–10.0'], ['eGFR', '76 mL/min/1.73 m²', '>60']], None),
 'h1356': ([(' Lactate is normal. Colonoscopy shows a 6 cm segment of inflamed colon near the splenic flexure, with a sharp line between it and normal mucosa. The rectum is normal.', '')],
           [['Haemoglobin', '129 g/L', '130–175'], ['White cell count', '13.6 ' + W, '3.8–10.0'], ['CRP', '74 mg/L', '<5'], ['Lactate', '1.4 mmol/L', '<2.0']],
           'Colonoscopy shows a 6 cm segment of inflamed colon near the splenic flexure, with a sharp line between it and normal mucosa. The rectum is normal.'),
 'h1372': ([(' Her serum calcium, phosphate, alkaline phosphatase, parathyroid hormone and 25-hydroxyvitamin D levels are normal. Dual-energy X-ray absorptiometry (DEXA) scanning of the lumbar spine and femoral neck is performed and reports a femoral neck T-score of -2.8.', '')],
           [['Adjusted calcium', '2.35 mmol/L', '2.2–2.6'], ['Phosphate', '1.10 mmol/L', '0.8–1.5'], ['ALP', '96 IU/L', '25–115'], ['PTH', '4.8 pmol/L', '1.6–6.9'], ['25-hydroxyvitamin D', '62 nmol/L', '>50']],
           'DEXA scanning of the lumbar spine and femoral neck reports a femoral neck T-score of -2.8.'),
 'h1683': ([(' ECG shows widespread concave ST elevation and PR depression, with raised ESR and CRP.', ' ECG shows widespread concave ST elevation and PR depression.')],
           [['White cell count', '11.6 ' + W, '3.8–10.0'], ['CRP', '86 mg/L', '<5'], ['ESR', '64 mm/hour', '<20'], ['High-sensitivity troponin T', '12 ng/L', '<14']], None),
 'h1817': ([(' Troponin is not raised.', '')], [['High-sensitivity troponin T at 0 hours', '8 ng/L', '<14'], ['High-sensitivity troponin T at 3 hours', '9 ng/L', '<14']], None),
 'h1833': ([(' A full blood count, renal function and HbA1c are normal.', '')], [['Haemoglobin', '146 g/L', '130–175'], ['eGFR', '82 mL/min/1.73 m²', '>60'], ['HbA1c', '40 mmol/mol', '20–42'], ['Total cholesterol', '5.9 mmol/L', '<5.0']], None),
 'h0445': ([(' Thyroid function is normal and urine drug screen is negative.', '')], [['TSH', '1.8 mU/L', '0.3–4.2'], ['Free T4', '15 pmol/L', '12–22'], ['Urine drug screen', 'Negative', '']], None),
 'h0448': ([(' Thyroid function and ECG are normal.', ' Her ECG is normal.')], [['TSH', '2.0 mU/L', '0.3–4.2'], ['Free T4', '14 pmol/L', '12–22'], ['Random glucose', '5.4 mmol/L', '<11.1']], None),
 'h1195': ([(' Urine drug screen and thyroid function are normal.', '')], [['TSH', '1.1 mU/L', '0.3–4.2'], ['Free T4', '16 pmol/L', '12–22'], ['Urine drug screen', 'Negative', '']], None),
 'h0475': ([(' Creatine kinase is normal.', '')], [['Creatine kinase', '110 U/L', '40–320'], ['Sodium', '142 mmol/L', '135–145'], ['Urea', '8.6 mmol/L', '2.5–7.8']], None),
 'h0476': ([(' He is afebrile and his creatine kinase is normal.', ' He is afebrile.')], [['Creatine kinase', '96 U/L', '40–320'], ['Urea', '8.9 mmol/L', '2.5–7.8'], ['Creatinine', '104 µmol/L', '60–120']], None),
 'h1225': ([(' Creatine kinase is normal.', '')], [['Creatine kinase', '120 U/L', '40–320'], ['White cell count', '7.4 ' + W, '3.8–10.0']], None),
 'h0469': ([(' Liver function and INR are normal.', '')], [['Paracetamol level at 4 hours', '160 mg/L', 'treatment line 100'], ['ALT', '24 IU/L', '10–50'], ['INR', '1.0', '0.8–1.2']], None),
 'h0458': ([(' During an episode, her glucose is 1.8 mmol/L (4.0–7.8). Plasma insulin is high and C-peptide is low. A sulfonylurea screen is negative.', ' Blood taken during an episode is shown.')],
           [['Glucose', '1.8 mmol/L', '4.0–7.8'], ['Insulin', '480 pmol/L', '<20 when hypoglycaemic'], ['C-peptide', '<0.1 nmol/L', '0.26–1.03'], ['Sulfonylurea screen', 'Negative', '']], None),
 'h0597': ([(' Serum albumin, creatinine and urine dipstick are normal.', ' Urine dipstick is normal.')], [['Albumin', '41 g/L', '35–50'], ['Creatinine', '76 µmol/L', '45–90'], ['Sodium', '139 mmol/L', '135–145']], None),
 'h0648': ([(' Urine output and renal function are normal. CT aortogram demonstrates a descending thoracic aortic dissection distal to the left subclavian artery without malperfusion.', ' Urine output is normal.')],
           [['Haemoglobin', '138 g/L', '130–175'], ['Creatinine', '88 µmol/L', '60–120'], ['Lactate', '1.2 mmol/L', '<2.0']],
           'CT aortogram demonstrates a descending thoracic aortic dissection distal to the left subclavian artery without malperfusion.'),
 'h0334': ([(' ECG confirms atrial fibrillation and thyroid function is normal.', ' ECG confirms atrial fibrillation.')], [['TSH', '2.3 mU/L', '0.3–4.2'], ['Potassium', '4.1 mmol/L', '3.5–5.3'], ['Creatinine', '79 µmol/L', '45–90']], None),
 'h0367': ([(' Full blood count, ferritin, thyroid function, NT-proBNP, 12-lead ECG and chest radiograph are all normal.', ' A 12-lead ECG and chest radiograph are normal.')],
           [['Haemoglobin', '134 g/L', '115–155'], ['Ferritin', '58 µg/L', '15–150'], ['TSH', '1.9 mU/L', '0.3–4.2'], ['NT-proBNP', '62 ng/L', '<400']], None),
 'h0406': ([(', and lumbar puncture opening pressure is 35 cm H2O with normal CSF constituents.', '. A lumbar puncture is performed.')],
           [['CSF opening pressure', '35 cm H₂O', '10–25'], ['CSF protein', '0.28 g/L', '0.15–0.45'], ['CSF glucose', '3.4 mmol/L', '2.5–4.4'], ['CSF white cells', '1 /mm³', '<5']], None),
}
n = 0
for q in D['hq']['q']:
    if q['id'] not in R: continue
    subs, lab, post = R.pop(q['id'])
    assert not q.get('lab') and not (q.get('post') or '').strip(), q['id']
    for old, new in subs:   # a space in the old text matches any whitespace: sentences may sit on a new line
        rx = re.compile(r'\s+'.join(re.escape(w) for w in old.split(' ')) if old.startswith(' ') else r'\s+'.join(re.escape(w) for w in old.split(' ')))
        hits = rx.findall(q['s'])
        assert len(hits) == 1, (q['id'], old[:60], len(hits))
        q['s'] = rx.sub(lambda _: new, q['s'])
    q['s'] = re.sub(r'[ \t]+\n', '\n', q['s']).rstrip()
    q['lab'] = lab
    if post: q['post'] = post
    n += 1
assert not R, list(R)
s = s[:m.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + s[m.end(2):]
F.write_text(s, encoding='utf-8')
print('Pastest-style lab tables added to %d questions' % n)
