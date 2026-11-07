#!/usr/bin/env python3
"""v3.6.17: tooltips read the words around a term.
1. Compound terms get their own card and win over the single word inside them: "ST depression" is an ECG sign, not
   low mood; "respiratory depression", "idiopathic intracranial hypertension", "pulmonary/portal hypertension",
   "eczema herpeticum", "venous eczema", "gestational diabetes", "Ludwig's angina", "dopamine antagonist" and others.
   Some phrases are claimed but never underlined ("stroke volume"), so the word inside them is left alone.
2. A context guard: a word is not underlined when its neighbour changes its meaning and no compound card exists
   (e.g. "marrow depression", "ocular hypertension", "insulin sensitivity", "dopamine receptor")."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')


def must(old, new):
    global s
    assert s.count(old) == 1, ('found %d' % s.count(old), old[:90])
    s = s.replace(old, new)


COMP = r"""  /* v3.6.17 compound terms: they outrank the single word inside them */
  [
    [['ST depression', 'ST-segment depression', 'ST segment depression'], 'jg', 'ST depression', 'Horizontal or downsloping ST depression means subendocardial ischaemia: NSTEMI or unstable angina, with the troponin deciding which. It is also the reciprocal change of a STEMI, and a "reverse tick" scoop with digoxin.', '➔ Suspected ACS: aspirin, serial troponin, GRACE score'],
    [['ST elevation', 'ST-segment elevation', 'ST segment elevation'], 'jg', 'ST elevation', 'New ST elevation in two contiguous leads means STEMI until proven otherwise. Widespread saddle-shaped ST elevation with PR depression means pericarditis.', '➔ STEMI: aspirin and primary PCI'],
    [['PR depression', 'PR-segment depression'], 'jg', 'PR depression', 'Widespread PR depression with saddle-shaped ST elevation is the ECG of acute pericarditis.', '➔ NSAID plus colchicine'],
    [['respiratory depression'], 'jg', 'Respiratory depression', 'Slow, shallow breathing from opioids, benzodiazepines or sedation; pinpoint pupils point to an opioid.', '➔ Opioid: IV naloxone and airway support'],
    [['idiopathic intracranial hypertension', 'benign intracranial hypertension'], 'c', 'Idiopathic intracranial hypertension', 'Young woman with a high BMI, headache worse lying down or in the morning, papilloedema and normal imaging; may have a sixth nerve palsy.', '➔ Weight loss and acetazolamide; urgent if vision is threatened'],
    [['raised intracranial pressure'], 'c', 'Raised intracranial pressure', 'Headache worse lying down and on coughing, vomiting, papilloedema; late signs are a falling GCS, bradycardia and hypertension (Cushing\'s reflex).', '➔ Urgent CT; no lumbar puncture until imaged'],
    [['pulmonary hypertension'], 'c', 'Pulmonary hypertension', 'Raised pressure in the pulmonary arteries: exertional breathlessness, loud P2, right heart strain; usually from left heart or lung disease.', '➔ Echo first; right heart catheter confirms; treat the cause'],
    [['portal hypertension'], 'c', 'Portal hypertension', 'Raised portal pressure, usually from cirrhosis: varices, ascites, splenomegaly, caput medusae.', '➔ Varices: carvedilol; bleeding: terlipressin and band ligation'],
    [['eczema herpeticum'], 'c', 'Eczema herpeticum', 'Known eczema with painful clustered punched-out erosions and fever: herpes simplex spreading through broken skin.', '➔ Same day: aciclovir (IV if unwell) and urgent referral'],
    [['venous eczema', 'varicose eczema', 'stasis eczema'], 'c', 'Venous eczema', 'Itchy, scaly lower-leg skin with brown haemosiderin staining and oedema from venous hypertension.', '➔ Emollient, topical steroid for flares, compression once ABPI allows'],
    [['gestational diabetes'], 'c', 'Gestational diabetes', 'Diabetes first found in pregnancy on a 75 g OGTT: fasting 5.6 mmol/L or more, or 2-hour 7.8 mmol/L or more (NICE).', '➔ Diet and exercise, then metformin; insulin if fasting is 7.0 or more at diagnosis'],
    [['gestational hypertension', 'pregnancy-induced hypertension'], 'c', 'Gestational hypertension', 'New hypertension after 20 weeks without proteinuria; with proteinuria or organ involvement it is pre-eclampsia.', '➔ Labetalol first line; check urine protein and bloods'],
    [["Ludwig's angina"], 'c', "Ludwig's angina", 'Spreading cellulitis of the floor of the mouth, usually from a lower molar: drooling, a raised tongue and a woody neck threaten the airway.', '➔ Secure the airway, IV antibiotics, maxillofacial surgeons'],
    [['dopamine antagonist', 'dopamine antagonists', 'dopamine-blocking'], 'dr', 'Dopamine antagonists', 'Block D2 receptors: antiemetics (metoclopramide, domperidone) and antipsychotics.', '', 'Metoclopramide or haloperidol in Parkinson\'s ➔ worsens rigidity; use domperidone'],
    [['insulin resistance'], 'jg', 'Insulin resistance', 'Cells respond poorly to insulin: central obesity, acanthosis nigricans, PCOS and type 2 diabetes.', ''],
    [['bipolar depression'], 'c', 'Bipolar depression', 'A depressive episode in someone with bipolar disorder: an antidepressant alone can tip them into mania.', '➔ Quetiapine or lurasidone; never an antidepressant without a mood stabiliser'],
    [['postnatal depression', 'postpartum depression', 'perinatal depression'], 'c', 'Postnatal depression', 'Low mood, anhedonia and guilt starting within a year of birth, lasting over 2 weeks; screen with the Edinburgh scale.', '➔ Guided self-help or CBT; sertraline if breastfeeding'],
    [['herpes simplex encephalitis', 'HSV encephalitis'], 'c', 'Herpes simplex encephalitis', 'Fever, confusion, odd behaviour or seizures; temporal lobe changes on MRI; HSV PCR in the CSF.', '➔ IV aciclovir at once, before results'],
  ].forEach(([names, t, h, l, a, w]) => { const e = {t, h, l, a: a || '', w: w || ''}; names.forEach(n => add(n, e, -1)); });
  /* claimed but never underlined, so the single word inside is left alone */
  ['stroke volume', 'shock wave', 'cardiac asthma', 'clotting factors', 'pain relief', 'asthma nurse', 'insulin sensitivity', 'stroke unit', 'dopamine receptor', 'dopamine receptors', 'marrow depression', 'bone marrow depression', 'myocardial depression', 'CNS depression', 'depression of consciousness', 'ocular hypertension', 'white coat hypertension']
    .forEach(n => { const k = n.toLowerCase(); if (!map.has(k)) map.set(k, {p: -2, k: n, cs: false, e: {skip: true, id: -1}}); });
  (D.jg || []).forEach(j => {"""
must("  (D.jg || []).forEach(j => {", COMP)

must("""        const v = tt.map.get(mt[1].toLowerCase());
        if (!v || (v.cs && mt[1] !== v.k) || seen.has(v.e.id)) continue;""",
     """        const v = tt.map.get(mt[1].toLowerCase());
        if (!v || v.e.skip || (v.cs && mt[1] !== v.k) || seen.has(v.e.id) || ttCtxBad(mt[1].toLowerCase(), s, mt.index, mt.index + mt[0].length)) continue;""")

must("function ttWrap(m){", r"""/* a neighbouring word that changes the meaning, with no compound card for it: leave the word plain */
const TT_CTX = {
  depression: {pre: /^(st|pr|segment|respiratory|cns|marrow|myocardial|ventilatory|cardiac)$/},
  hypertension: {pre: /^(intracranial|pulmonary|portal|ocular|venous|coat|renovascular)$/},
  eczema: {post: /^(herpeticum)$/},
  angina: {pre: /^(ludwig's|ludwig’s|vincent's|vincent’s|ludwig|vincent)$/},
  stroke: {post: /^(volume|unit|work)$/},
  insulin: {post: /^(resistance|sensitivity|secretion|levels?)$/},
  dopamine: {post: /^(antagonists?|agonists?|receptors?|blockers?|blocking)$/},
  asthma: {pre: /^(cardiac)$/},
  shock: {post: /^(wave|waves)$/},
  diabetes: {pre: /^(gestational)$/, post: /^(insipidus)$/},
  ulcer: {pre: /^(corneal|venous|arterial|pressure|neuropathic|marjolin's|aphthous|rodent)$/},
  anaemia: {pre: /^(sickle)$/},
  psychosis: {pre: /^(steroid|puerperal|postpartum|drug-induced|korsakoff)$/}
};
function ttCtxBad(key, s, a, b){
  const c = TT_CTX[key]; if (!c) return false;
  const pre = (s.slice(Math.max(0, a - 30), a).match(/([A-Za-z0-9'’]+)[\s-]*$/) || [])[1], post = (s.slice(b, b + 30).match(/^[\s-]*([A-Za-z0-9'’]+)/) || [])[1];
  return !!((c.pre && pre && c.pre.test(pre.toLowerCase())) || (c.post && post && c.post.test(post.toLowerCase())));
}
function ttWrap(m){""")

F.write_text(s, encoding='utf-8'); print('v3617 tt ok')
