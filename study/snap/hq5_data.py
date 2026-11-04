"""v3.3.5 Hammer set D: data questions with MSCAA-style results tables, and gap questions for ILO topics the bank never asked.

Format, one block per question (see site/patches/v335_sba.py):

    @u 51 2N                 unit index, hammer level, pattern letter
    s: stem paragraph // next paragraph
    $ Name ; value ; range   results row (normal rows are deliberate decoys)
    ? lead-in question
    > option ; *correct ; option ; option ; option
    = why the answer is right
    ~ the old one-line flip
    c: cue | cue             thought map cues, word for word from the stem, lead-in or a results row
    m: mechanism
    g: decisive gate
    f: condition => option text
    x: option text => why it is wrong here
"""

Q = r"""
@u 51 1N
s: A 70 kg man is nil by mouth for 24 hours after a laparotomy. He is euvolaemic and is not losing fluid from drains or a nasogastric tube. // Pulse rate 78 bpm, BP 128/78 mmHg.
$ Sodium ; 139 mmol/L ; 135–146
$ Potassium ; 4.1 mmol/L ; 3.5–5.3
$ Urea ; 5.0 mmol/L ; 2.5–7.8
$ Creatinine ; 82 µmol/L ; 60–120
? Which daily maintenance prescription is most appropriate?
> About 1 litre of 5% glucose with no potassium ; *About 2 litres with 70 mmol each of sodium and potassium ; About 2 litres of 0.9% saline with no potassium ; About 3.5 litres with 140 mmol potassium ; About 4 litres with 20 mmol each of sodium and potassium
= Routine maintenance is 25 to 30 ml per kg of water a day, with about 1 mmol per kg each of sodium, potassium and chloride, and 50 to 100 g of glucose.
~ Ongoing nasogastric losses → replace them on top, usually with 0.9% saline and potassium.
c: 70 kg | nil by mouth | euvolaemic | Potassium 4.1
m: Maintenance replaces what the body loses each day through urine, sweat and breath
g: 25 to 30 ml per kg of water and 1 mmol per kg of sodium and potassium a day
f: no oral intake plus 2 litres a day of nasogastric loss => About 3.5 litres with 140 mmol potassium
x: About 1 litre of 5% glucose with no potassium => Half his water need and no potassium, so he becomes dry and hypokalaemic
x: About 2 litres of 0.9% saline with no potassium => Twice the sodium he needs and no potassium, a common cause of hyperchloraemia and low potassium
x: About 3.5 litres with 140 mmol potassium => Overload for a man with no extra losses, and twice the potassium
x: About 4 litres with 20 mmol each of sodium and potassium => Far too much water, which risks hyponatraemia and fluid overload

@u 51 2N
s: A 64 year old woman has had paralytic ileus for 3 days after a bowel resection. She is nil by mouth and her nasogastric tube is draining about 1.5 litres a day. She has been given 5% glucose only. // Pulse rate 96 bpm, BP 118/72 mmHg.
$ Sodium ; 137 mmol/L ; 135–146
$ Potassium ; 2.9 mmol/L ; 3.5–5.3
$ Chloride ; 92 mmol/L ; 95–106
$ Bicarbonate ; 31 mmol/L ; 22–30
$ Creatinine ; 76 µmol/L ; 60–120
? Which is the most appropriate fluid to replace her losses?
> 5% glucose ; *0.9% saline with 40 mmol potassium per litre ; Hartmann's solution ; Oral potassium tablets ; Potassium chloride 40 mmol IV over 10 minutes
= Gastric losses are rich in sodium, chloride and potassium. Replace them with 0.9% saline plus potassium, no faster than 10 mmol of potassium an hour peripherally.
~ Potassium 2.4 with arrhythmias → potassium through a central line on a cardiac monitor.
c: nasogastric tube is draining about 1.5 litres a day | Potassium 2.9 | Chloride 92 | Bicarbonate 31
m: Losing stomach acid takes chloride and hydrogen ions, and the kidney then wastes potassium
g: Replace gastric losses with saline that carries potassium
f: losses from a high-output ileostomy and a normal potassium => Hartmann's solution
x: 5% glucose => Glucose gives free water with no electrolytes and will drop her sodium and potassium further
x: Hartmann's solution => Has only 5 mmol of potassium per litre and less chloride than she is losing
x: Oral potassium tablets => She is nil by mouth with an ileus, so tablets will not be absorbed
x: Potassium chloride 40 mmol IV over 10 minutes => A potassium bolus can cause cardiac arrest; give at most 10 mmol an hour peripherally

@u 51 3N
s: A 52 year old woman is 2 days after an open bowel operation. She has been given 3 litres of 5% glucose a day. This morning she had a generalised seizure and is now drowsy. // GCS 12. She is euvolaemic.
$ Sodium ; 119 mmol/L ; 135–146
$ Potassium ; 3.8 mmol/L ; 3.5–5.3
$ Glucose ; 6.4 mmol/L ; 4.0–7.8
$ Serum osmolality ; 254 mOsm/kg ; 275–295
? Which is the most appropriate immediate treatment?
> 0.9% saline at 1 litre an hour ; *150 ml of 3% saline over 20 minutes ; Fluid restriction to 1 litre a day ; IV furosemide ; Oral tolvaptan
= Acute hyponatraemia with seizures is a brain emergency: a bolus of hypertonic saline, repeated if needed, aiming for a rise of about 5 mmol/L, then no more than 10 in 24 hours.
~ Chronic, mild hyponatraemia without symptoms → find the cause and correct slowly.
c: 3 litres of 5% glucose a day | generalised seizure | Sodium 119 | Serum osmolality 254
m: Free water from glucose drips swells brain cells when sodium falls fast after surgery
g: Severe symptoms such as seizures need hypertonic saline now, whatever the cause
f: no symptoms and a sodium of 129 that fell over weeks => Fluid restriction to 1 litre a day
x: 0.9% saline at 1 litre an hour => Too weak to raise sodium quickly and risks fluid overload
x: Fluid restriction to 1 litre a day => Takes days, far too slow for a fitting patient
x: IV furosemide => Does not treat cerebral oedema and can drop the sodium further
x: Oral tolvaptan => Specialist drug for chronic SIADH, too slow and she cannot swallow safely

@u 51 2N
s: An 80 year old woman has had diarrhoea and vomiting for 3 days and has hardly drunk. Her urine output is 20 ml an hour. // Pulse rate 108 bpm, BP 98/60 mmHg. Her mucous membranes are dry. Her bladder is not palpable.
$ Sodium ; 146 mmol/L ; 135–146
$ Potassium ; 4.6 mmol/L ; 3.5–5.3
$ Urea ; 24.0 mmol/L ; 2.5–7.8
$ Creatinine ; 160 µmol/L ; 60–120
$ Urine sodium ; 8 mmol/L ;
? Which is the most likely type of acute kidney injury?
> Acute interstitial nephritis ; Acute tubular necrosis ; Postrenal obstruction ; *Prerenal acute kidney injury ; Rhabdomyolysis
= The kidney is holding on to sodium and water: a low urine sodium and a urea that has risen far more than the creatinine.
~ Urine sodium over 40 with muddy brown casts → acute tubular necrosis.
c: hardly drunk | Urea 24.0 | Creatinine 160 | Urine sodium 8
m: Low blood volume makes healthy tubules reabsorb sodium, water and urea
g: Urine sodium under 20 with a high urea to creatinine ratio means a prerenal cause
f: urine sodium of 60 with granular casts after hours of hypotension => Acute tubular necrosis
f: a palpable bladder and bilateral hydronephrosis => Postrenal obstruction
x: Acute interstitial nephritis => Usually a new drug with rash, fever and white cells in the urine
x: Acute tubular necrosis => Damaged tubules waste sodium, so urine sodium would be high
x: Postrenal obstruction => The bladder is not palpable, and a scan would show hydronephrosis
x: Rhabdomyolysis => Needs a crush, a long lie or muscle injury with a very high CK

@u 51 3N
s: An 84 year old man was found on his kitchen floor, where he had lain for about 18 hours. He is alert. // There are pressure marks over his right hip and shoulder. His urine is dark. Urine dipstick shows blood 3+, but microscopy shows no red cells. ECG shows sinus rhythm with no peaked T waves.
$ Creatine kinase ; 48,000 IU/L ; 25–200
$ Potassium ; 5.9 mmol/L ; 3.5–5.3
$ Creatinine ; 210 µmol/L ; 60–120
$ Adjusted calcium ; 2.08 mmol/L ; 2.20–2.60
? Which is the most appropriate first treatment?
> Haemodialysis now ; IV calcium gluconate ; IV furosemide ; *Generous IV 0.9% saline ; Oral fluids and recheck tomorrow
= Rhabdomyolysis: muscle releases myoglobin that blocks the tubules. Early, generous IV fluids protect the kidney. Watch potassium closely.
~ Potassium 6.8 with peaked T waves → calcium gluconate first, then insulin with glucose.
c: lain for about 18 hours | blood 3+, but microscopy shows no red cells | Creatine kinase 48,000
m: Myoglobin from crushed muscle shows as blood on the dipstick and poisons the tubules
g: Rhabdomyolysis with AKI needs early IV fluids
f: potassium of 7.0 with broad complexes on the ECG => IV calcium gluconate
x: Haemodialysis now => For refractory hyperkalaemia, acidosis or overload, none of which he has yet
x: IV calcium gluconate => Protects the heart when the ECG shows hyperkalaemia; his ECG is normal
x: IV furosemide => Diuretics in a dry patient worsen the kidney injury
x: Oral fluids and recheck tomorrow => Far too slow for a CK of 48,000 with a rising creatinine

@u 51 2D
s: A 58 year old man has had potassium replaced orally and intravenously for 3 days, but it will not rise. He has taken omeprazole for 8 years. He has no diarrhoea and takes no diuretics.
$ Potassium ; 3.0 mmol/L ; 3.5–5.3
$ Magnesium ; 0.38 mmol/L ; 0.70–1.00
$ Sodium ; 139 mmol/L ; 135–146
$ Adjusted calcium ; 2.10 mmol/L ; 2.20–2.60
? Which is the most appropriate next step?
> Increase potassium to 80 mmol per litre peripherally ; *IV magnesium sulfate ; Oral sodium bicarbonate ; Start spironolactone ; Stop the potassium
= The kidney keeps wasting potassium until magnesium is replaced. Long-term PPIs are a common cause of low magnesium.
~ Magnesium normal and hypertension with low renin → think Conn's syndrome.
c: will not rise | omeprazole for 8 years | Magnesium 0.38
m: Low magnesium opens kidney potassium channels so potassium keeps leaking out
g: Refractory hypokalaemia: check and replace magnesium first
x: Increase potassium to 80 mmol per litre peripherally => Above 40 mmol per litre peripherally is unsafe, and it will still be lost while magnesium is low
x: Oral sodium bicarbonate => Alkalosis drives potassium into cells and makes the level worse
x: Start spironolactone => Treats the wrong problem and ignores the magnesium
x: Stop the potassium => He is still low; the fix is to add magnesium, not stop replacement

@u 10 2N
s: A 26 year old woman of Cypriot family origin is tired. She has regular periods that are not heavy. She eats meat. She is not pregnant. // She looks well. There is no hepatosplenomegaly.
$ Haemoglobin ; 112 g/L ; 115–150
$ MCV ; 63 fL ; 80–96
$ Red cell count ; 5.9 × 10¹²/L ; 3.8–4.8
$ Ferritin ; 85 µg/L ; 12–200
? Which is the most appropriate investigation?
> Bone marrow biopsy ; Coeliac serology ; Colonoscopy and gastroscopy ; *Haemoglobin electrophoresis ; Trial of oral iron
= Very small cells, a high red cell count and normal ferritin point to thalassaemia trait. HbA2 is raised in beta thalassaemia trait.
~ Ferritin of 5 with heavy periods → iron deficiency, oral iron.
c: Cypriot family origin | MCV 63 | Red cell count 5.9 | Ferritin 85
m: The marrow makes many small red cells because each one carries less haemoglobin
g: Microcytosis out of proportion to the anaemia with normal ferritin suggests thalassaemia trait
f: ferritin of 4 with heavy periods => Trial of oral iron
x: Bone marrow biopsy => Invasive and unnecessary; electrophoresis answers the question
x: Coeliac serology => Coeliac causes iron deficiency, but her ferritin is normal
x: Colonoscopy and gastroscopy => For iron deficiency in older patients, not a microcytosis with normal iron stores
x: Trial of oral iron => Iron does not help thalassaemia trait and can overload

@u 10 2N
s: A 62 year old woman with active rheumatoid arthritis is tired. She has no bleeding or weight loss. // Several finger joints are swollen.
$ Haemoglobin ; 104 g/L ; 115–150
$ MCV ; 84 fL ; 80–96
$ Ferritin ; 240 µg/L ; 12–200
$ Transferrin saturation ; 12% ; 20–50
$ CRP ; 34 mg/L ; <5
? Which is the most likely diagnosis?
> *Anaemia of chronic disease ; B12 deficiency ; Iron deficiency anaemia ; Sideroblastic anaemia ; Thalassaemia trait
= Inflammation raises hepcidin, which locks iron away in stores. Ferritin is normal or high, transferrin saturation low, and cells normal or slightly small.
~ Ferritin 8 → true iron deficiency, look for blood loss.
c: active rheumatoid arthritis | MCV 84 | Ferritin 240 | CRP 34
m: Hepcidin traps iron in stores so the marrow cannot use it
g: Anaemia with high ferritin, low saturation and inflammation is anaemia of chronic disease
f: ferritin of 6 with a low MCV => Iron deficiency anaemia
x: B12 deficiency => Would give a large MCV
x: Iron deficiency anaemia => Ferritin is high, so stores are full
x: Sideroblastic anaemia => Shows ringed sideroblasts with high iron saturation
x: Thalassaemia trait => Gives a very low MCV with a high red cell count

@u 10 2L
s: A 34 year old woman with systemic lupus erythematosus has become tired and yellow over 2 weeks. // She is pale and jaundiced. The spleen tip is palpable.
$ Haemoglobin ; 92 g/L ; 115–150
$ MCV ; 104 fL ; 80–96
$ Reticulocytes ; 9% ; 0.5–2.5
$ Bilirubin ; 52 µmol/L ; <17
$ ALT ; 28 IU/L ; 10–50
$ Direct antiglobulin test ; Positive ;
? Which is the most likely diagnosis?
> *Autoimmune haemolytic anaemia ; B12 deficiency ; G6PD deficiency ; Gilbert's syndrome ; Hereditary spherocytosis
= Antibodies coat red cells, so the direct antiglobulin test is positive. Reticulocytes push the MCV up and bilirubin rises with a normal ALT.
~ Negative DAT with spherocytes and a family history → hereditary spherocytosis.
c: systemic lupus erythematosus | Reticulocytes 9% | Bilirubin 52 | Direct antiglobulin test Positive
m: Autoantibodies tag red cells for destruction in the spleen
g: Haemolysis with a positive DAT is immune haemolysis
f: negative DAT, spherocytes and an affected father => Hereditary spherocytosis
f: sudden haemolysis after fava beans or nitrofurantoin => G6PD deficiency
x: B12 deficiency => Gives a high MCV but low reticulocytes and no positive DAT
x: G6PD deficiency => Triggered by oxidants and DAT negative
x: Gilbert's syndrome => Haemoglobin would be normal
x: Hereditary spherocytosis => DAT negative, usually with a family history

@u 10 3N
s: A 54 year old man is tired. He has no gut symptoms or numbness. // There is no pallor. Neurological examination is normal.
$ Haemoglobin ; 141 g/L ; 130–175
$ MCV ; 104 fL ; 80–96
$ Vitamin B12 ; 410 ng/L ; 180–900
$ Folate ; 6.2 µg/L ; >3.0
$ TSH ; 2.1 mU/L ; 0.3–4.2
$ GGT ; 210 IU/L ; <55
? Which is the most likely cause of the raised MCV?
> *Alcohol excess ; B12 deficiency ; Folate deficiency ; Hypothyroidism ; Myelodysplasia
= Alcohol enlarges red cells directly, often before any anaemia. A raised GGT supports it.
~ B12 of 90 with hypersegmented neutrophils → B12 deficiency.
c: MCV 104 | Vitamin B12 410 | TSH 2.1 | GGT 210
m: Alcohol is toxic to red cell membranes and the marrow, so cells are large
g: Macrocytosis with normal B12, folate and TSH plus a high GGT points to alcohol
f: a low B12 and hypersegmented neutrophils => B12 deficiency
x: B12 deficiency => His B12 is normal
x: Folate deficiency => His folate is normal
x: Hypothyroidism => His TSH is normal
x: Myelodysplasia => Possible in older people with cytopenias, but his blood count is otherwise normal

@u 3 2D
s: A 74 year old woman takes citalopram. She started clarithromycin for a chest infection 3 days ago. On the ward she has two brief blackouts. // The monitor shows a polymorphic broad complex tachycardia that twists around the baseline and stops by itself. Between episodes she has a pulse and the QTc is 560 ms.
$ Potassium ; 3.3 mmol/L ; 3.5–5.3
$ Magnesium ; 0.62 mmol/L ; 0.70–1.00
? Which is the most appropriate immediate drug?
> Adenosine ; IV amiodarone ; IV atropine ; *IV magnesium sulfate ; Oral flecainide
= Torsades de pointes from a long QT: IV magnesium 2 g, correct potassium and stop the QT drugs. Defibrillate if pulseless.
~ Monomorphic VT with a pulse and no long QT → amiodarone.
c: citalopram | clarithromycin | twists around the baseline | QTc is 560 ms | Magnesium 0.62
m: Drugs that block repolarisation lengthen the QT and allow twisting VT
g: Polymorphic VT with a long QT is torsades, treated with magnesium
f: regular monomorphic VT with a normal QT in a stable patient => IV amiodarone
x: Adenosine => Used for narrow complex re-entry tachycardias, not torsades
x: IV amiodarone => Lengthens the QT further and can make torsades worse
x: IV atropine => For bradycardia; it does not stop torsades
x: Oral flecainide => Too slow and dangerous in a heart with a prolonged QT

@u 3 1N
s: A 72 year old woman takes bendroflumethiazide. She has had vomiting for 3 days and now has muscle weakness and palpitations. // Pulse rate 92 bpm, regular.
$ Potassium ; 2.6 mmol/L ; 3.5–5.3
$ Sodium ; 136 mmol/L ; 135–146
$ Magnesium ; 0.78 mmol/L ; 0.70–1.00
? Which ECG change is most likely?
> Delta waves ; J waves ; Tall peaked T waves with flat P waves ; Shortened QT interval ; *U waves with flattened T waves
= Low potassium flattens the T wave, brings out a U wave, and can depress the ST segment and lengthen the QT.
~ Potassium 6.9 → peaked T waves, flat P waves and broad QRS.
c: bendroflumethiazide | vomiting | Potassium 2.6
m: Low potassium slows repolarisation so a U wave appears after the T wave
g: Hypokalaemia gives U waves; hyperkalaemia gives peaked T waves
f: potassium of 7.0 => Tall peaked T waves with flat P waves
x: Delta waves => The slurred upstroke of an accessory pathway, as in WPW
x: J waves => Seen in hypothermia
x: Tall peaked T waves with flat P waves => A sign of high potassium, not low
x: Shortened QT interval => Seen with high calcium

@u 4 2N
s: A 44 year old man has had a headache and blurred vision for 2 days. He stopped his blood pressure tablets a month ago. // BP 236/138 mmHg in both arms. Fundoscopy shows bilateral papilloedema with flame haemorrhages. Urine dipstick shows blood 2+ and protein 2+.
$ Creatinine ; 184 µmol/L ; 60–120
$ Potassium ; 3.9 mmol/L ; 3.5–5.3
$ Troponin T ; 9 ng/L ; <14
? Which is the most appropriate management?
> *Admit for IV labetalol, lowering BP slowly ; IV labetalol to a normal BP within an hour ; Oral amlodipine and GP review in a week ; Restart his tablets and recheck in a month ; Sublingual nifedipine now
= Hypertensive emergency with damage to the eyes and kidneys: admit, IV labetalol or GTN, and lower mean pressure by no more than about 25% in the first hours to protect brain perfusion.
~ BP 186/112 with no symptoms and normal fundi → urgent but oral treatment and same-day assessment.
c: BP 236/138 | papilloedema with flame haemorrhages | Creatinine 184
m: Very high pressure damages small arteries in the eye, kidney and brain
g: Severe hypertension with new organ damage is an emergency for controlled IV treatment
f: BP 186/112 with normal fundi, kidneys and no symptoms => Oral amlodipine and GP review in a week
x: IV labetalol to a normal BP within an hour => Dropping pressure fast can cause stroke or blindness because autoregulation has reset
x: Oral amlodipine and GP review in a week => Too slow with papilloedema and kidney injury
x: Restart his tablets and recheck in a month => Ignores organ damage that is happening now
x: Sublingual nifedipine now => Causes an unpredictable, sudden fall in pressure and is no longer used

@u 68 2N
s: A 19 year old woman with type 1 diabetes has vomited for a day and missed her insulin. // Pulse rate 116 bpm, BP 104/62 mmHg, respiratory rate 28 breaths per minute. She weighs 60 kg.
$ Glucose ; 28 mmol/L ; 4.0–7.8
$ Ketones ; 5.1 mmol/L ; <0.6
$ pH ; 7.12 ; 7.35–7.45
$ Bicarbonate ; 9 mmol/L ; 22–30
$ Potassium ; 5.7 mmol/L ; 3.5–5.3
? Which is the most appropriate first step?
> 0.9% saline with 40 mmol potassium in the first litre ; *1 litre of 0.9% saline over 1 hour ; IV insulin bolus of 10 units ; IV sodium bicarbonate ; Variable-rate insulin infusion
= Fluids first, then a fixed-rate insulin infusion at 0.1 units per kg per hour. Potassium is added from the second bag if it is 5.5 or below.
~ Systolic BP under 90 → 500 ml of crystalloid over 15 minutes, repeated.
c: missed her insulin | Ketones 5.1 | pH 7.12 | Potassium 5.7
m: Insulin lack lets ketones build up, and high glucose drags water out through the kidney
g: DKA starts with saline; no potassium while it is above 5.5
x: 0.9% saline with 40 mmol potassium in the first litre => Potassium is above 5.5, so none goes in the first bag
x: IV insulin bolus of 10 units => UK guidance uses a fixed-rate infusion without a bolus
x: IV sodium bicarbonate => Not used routinely; fluids and insulin clear the acid
x: Variable-rate insulin infusion => DKA needs a fixed weight-based rate to switch off ketone production

@u 68 3N
s: A 23 year old man is 4 hours into treatment for diabetic ketoacidosis with a fixed-rate insulin infusion. He has had 2 litres of 0.9% saline. He is passing urine.
$ Glucose ; 15 mmol/L ; 4.0–7.8
$ Ketones ; 3.0 mmol/L ; <0.6
$ pH ; 7.24 ; 7.35–7.45
$ Potassium ; 4.2 mmol/L ; 3.5–5.3
? How much potassium should be added to the next litre of saline?
> 20 mmol ; *40 mmol ; 60 mmol ; 80 mmol ; None
= Insulin drives potassium into cells. Between 3.5 and 5.5, add 40 mmol per litre. Under 3.5 needs senior review and more.
~ Potassium 5.8 → no potassium in that bag.
c: fixed-rate insulin infusion | passing urine | Potassium 4.2
m: Insulin and fluids move potassium into cells and out in the urine, so it falls
g: DKA potassium 3.5 to 5.5: 40 mmol per litre
f: potassium of 5.8 => None
x: 20 mmol => Too little as insulin keeps driving potassium down
x: 60 mmol => More than a peripheral bag should carry; under 3.5 needs senior review instead
x: 80 mmol => Unsafe peripherally and risks hyperkalaemia
x: None => Only when potassium is above 5.5 or there is no urine

@u 69 2D
s: A 79 year old woman with type 2 diabetes is drowsy and very dry after a week of a chest infection. // Pulse rate 112 bpm, BP 102/60 mmHg. She weighs 60 kg.
$ Glucose ; 48 mmol/L ; 4.0–7.8
$ Ketones ; 0.8 mmol/L ; <0.6
$ pH ; 7.36 ; 7.35–7.45
$ Sodium ; 152 mmol/L ; 135–146
$ Urea ; 22 mmol/L ; 2.5–7.8
? Which is the most appropriate initial management?
> 5% glucose to bring the sodium down ; Fixed-rate insulin at 0.1 units per kg per hour now ; IV 3% saline for the sodium ; *IV 0.9% saline first, insulin later if needed ; Oral fluids and gliclazide
= HHS: osmolality about 374. Fluids alone bring glucose down. Insulin at 0.05 units per kg per hour is added only if glucose stops falling, or at once if ketones are over 1.
~ Ketones 4 and pH 7.1 → DKA, fixed-rate insulin at 0.1 units per kg per hour.
c: very dry | Glucose 48 | Ketones 0.8 | Sodium 152
m: Slow-rising glucose drags water out of cells over days, making the blood very concentrated
g: HHS: replace fluid first and lower osmolality slowly
f: ketones of 4.5 with a pH of 7.12 => Fixed-rate insulin at 0.1 units per kg per hour now
x: 5% glucose to bring the sodium down => Adds glucose and drops osmolality too fast, risking cerebral oedema
x: Fixed-rate insulin at 0.1 units per kg per hour now => Insulin before fluid can crash the blood pressure and osmolality
x: IV 3% saline for the sodium => The sodium is high, not low
x: Oral fluids and gliclazide => She is drowsy and severely dry; she needs IV fluids

@u 67 3N
s: A 46 year old man with type 2 diabetes has fingerprick glucose readings of 12 to 16 mmol/L most days. He has had a recent haemolytic anaemia and has been treated for it.
$ HbA1c ; 41 mmol/mol ; 20–42
$ Haemoglobin ; 104 g/L ; 130–175
$ Reticulocytes ; 6% ; 0.5–2.5
? Which is the most likely reason his HbA1c does not match his readings?
> Iron deficiency ; Laboratory error ; Poor meter technique ; *Shortened red cell lifespan ; Very good control
= HbA1c reflects about 3 months of glucose stuck to red cells. If cells die early, there is less time to glycate, so HbA1c reads falsely low.
~ Iron deficiency with no haemolysis → HbA1c can read falsely high.
c: 12 to 16 mmol/L most days | haemolytic anaemia | Reticulocytes 6%
m: Young red cells have had less time to collect glucose
g: Haemolysis makes HbA1c falsely low; use glucose readings or fructosamine
f: iron deficiency with normal reticulocytes => Iron deficiency
x: Iron deficiency => Old red cells linger and push HbA1c up, not down
x: Laboratory error => The pattern is explained by his haemolysis
x: Poor meter technique => Repeated readings in the same range make this less likely
x: Very good control => His glucose readings are high

@u 70 3N
s: A 44 year old woman has had episodes of sweating, confusion and odd behaviour before breakfast for 3 months. She does not have diabetes. She works in a pharmacy. // During a supervised fast she becomes confused.
$ Glucose ; 2.1 mmol/L ; 4.0–7.8
$ Insulin ; High ;
$ C-peptide ; High ;
$ Sulfonylurea screen ; Negative ;
? Which is the most likely diagnosis?
> Addison's disease ; Alcohol excess ; Injected insulin ; *Insulinoma ; Sulfonylurea misuse
= High insulin with high C-peptide means the pancreas is making the insulin. A negative sulfonylurea screen leaves an insulinoma.
~ High insulin with low C-peptide → injected insulin.
c: does not have diabetes | Glucose 2.1 | C-peptide High | Sulfonylurea screen Negative
m: A tumour releases insulin even when glucose is low
g: High insulin and high C-peptide with a negative sulfonylurea screen is insulinoma
f: low C-peptide => Injected insulin
f: a positive sulfonylurea screen => Sulfonylurea misuse
x: Addison's disease => Causes low glucose with low insulin
x: Alcohol excess => Low glucose with low insulin
x: Injected insulin => C-peptide would be low because injected insulin contains none
x: Sulfonylurea misuse => The screen is negative

@u 72 2D
s: A 38 year old woman has had a painful swelling in the front of her neck for 10 days after a viral sore throat. She has palpitations. // Temperature 37.8°C, pulse rate 104 bpm. The thyroid is diffusely tender.
$ TSH ; <0.01 mU/L ; 0.3–4.2
$ Free T4 ; 38 pmol/L ; 12–22
$ ESR ; 68 mm/hr ; <20
$ TSH receptor antibodies ; Negative ;
? Which is the most appropriate treatment?
> Carbimazole ; Levothyroxine ; *NSAID and a beta-blocker ; Radioactive iodine ; Thyroidectomy
= De Quervain's thyroiditis: inflamed cells leak stored hormone. Treat pain and symptoms. Carbimazole does nothing as no new hormone is being made.
~ Painless goitre with positive TSH receptor antibodies → Graves' disease, carbimazole.
c: painful swelling | after a viral sore throat | ESR 68 | TSH receptor antibodies Negative
m: A viral inflammation breaks follicles and releases stored hormone
g: Painful thyroiditis with low uptake: treat symptoms, no antithyroid drugs
f: positive TSH receptor antibodies with eye signs => Carbimazole
x: Carbimazole => Blocks new hormone production, but this is leakage of stored hormone
x: Levothyroxine => Would worsen the thyrotoxicosis now
x: Radioactive iodine => An inflamed gland takes up almost no iodine, and it settles alone
x: Thyroidectomy => Not needed for a self-limiting inflammation

@u 72 3T
s: A 31 year old nurse has lost weight and has palpitations and a tremor. She has no eye signs and no goitre. // Pulse rate 112 bpm.
$ TSH ; <0.01 mU/L ; 0.3–4.2
$ Free T4 ; 41 pmol/L ; 12–22
$ Thyroglobulin ; Very low ;
$ Radioiodine uptake ; Absent ;
? Which is the most likely diagnosis?
> De Quervain's thyroiditis ; *Exogenous levothyroxine use ; Graves' disease ; Toxic adenoma ; Toxic multinodular goitre
= Swallowed thyroxine suppresses the gland, so uptake is absent and thyroglobulin is low. Thyroiditis also has absent uptake, but thyroglobulin is high.
~ Absent uptake with a tender gland and high thyroglobulin → thyroiditis.
c: nurse | no goitre | Thyroglobulin Very low | Radioiodine uptake Absent
m: Taking thyroxine switches off the patient's own gland
g: Thyrotoxic with low thyroglobulin and absent uptake means the hormone is coming from outside
f: a tender gland with high thyroglobulin => De Quervain's thyroiditis
x: De Quervain's thyroiditis => Thyroglobulin would be high from the damaged gland
x: Graves' disease => Diffuse high uptake and usually a goitre
x: Toxic adenoma => A single hot nodule on the scan
x: Toxic multinodular goitre => Patchy high uptake and a lumpy gland

@u 73 2N
s: A 52 year old woman had thyroid tests at a routine check. She has no symptoms. She is not pregnant or planning pregnancy.
$ TSH ; 7.2 mU/L ; 0.3–4.2
$ Free T4 ; 14 pmol/L ; 12–22
$ Thyroid peroxidase antibodies ; Positive ;
? Which is the most appropriate next step?
> Levothyroxine 100 micrograms daily ; No follow-up is needed ; Radioiodine uptake scan ; *Repeat TSH and free T4 in 3 months ; Thyroid ultrasound
= Subclinical hypothyroidism: a raised TSH with normal T4. Repeat in about 3 months, as many settle. Positive antibodies raise the yearly risk of overt hypothyroidism.
~ TSH 14 with a low free T4 → overt hypothyroidism, start levothyroxine.
c: no symptoms | TSH 7.2 | Free T4 14 | Thyroid peroxidase antibodies Positive
m: The pituitary pushes harder to keep T4 normal in a failing gland
g: Raised TSH with normal T4 and no symptoms: confirm on repeat before treating
f: free T4 of 7 with a TSH of 14 => Levothyroxine 100 micrograms daily
x: Levothyroxine 100 micrograms daily => Not started on one result in someone without symptoms
x: No follow-up is needed => Positive antibodies mean she needs monitoring
x: Radioiodine uptake scan => For thyrotoxicosis, not hypothyroidism
x: Thyroid ultrasound => Only if there is a lump or goitre

@u 73 3T
s: A 58 year old man is tired and cold. He has had headaches and has been bumping into doorframes. // There is a loss of the outer half of the visual field in both eyes.
$ TSH ; 0.8 mU/L ; 0.3–4.2
$ Free T4 ; 6 pmol/L ; 12–22
$ Sodium ; 131 mmol/L ; 135–146
? Which is the most likely diagnosis?
> Hashimoto's thyroiditis ; Over-replacement with levothyroxine ; Primary hypothyroidism ; *Secondary hypothyroidism ; Sick euthyroid syndrome
= A low T4 with an inappropriately normal TSH means the pituitary is failing. The field defect suggests a pituitary tumour. Check cortisol and give steroids before thyroxine.
~ TSH 38 with a low T4 → primary hypothyroidism.
c: bumping into doorframes | outer half of the visual field | TSH 0.8 | Free T4 6
m: A pituitary mass stops TSH release, so the thyroid is not driven
g: Low T4 with a normal or low TSH is a pituitary or hypothalamic cause
f: a TSH of 38 => Primary hypothyroidism
x: Hashimoto's thyroiditis => A primary gland failure with a high TSH
x: Over-replacement with levothyroxine => He takes none, and T4 would be high
x: Primary hypothyroidism => TSH would be high
x: Sick euthyroid syndrome => Occurs in acute illness, without a visual field defect

@u 41 1N
s: A 63 year old woman has had itch and yellow skin for 2 weeks. Her urine is dark and her stools are pale. // She is jaundiced. The abdomen is soft.
$ Bilirubin ; 78 µmol/L ; <17
$ ALP ; 480 IU/L ; 25–115
$ GGT ; 520 IU/L ; <55
$ ALT ; 90 IU/L ; 10–50
$ Albumin ; 38 g/L ; 35–50
? Which pattern do these results show?
> *Cholestatic ; Hepatitic ; Isolated unconjugated hyperbilirubinaemia ; Liver synthetic failure ; Normal
= ALP and GGT far above their limits, with a smaller ALT rise, is cholestasis. With pale stools and dark urine, look for a blocked duct with ultrasound.
~ ALT 1,200 with a mildly raised ALP → hepatitic pattern.
c: stools are pale | ALP 480 | GGT 520 | ALT 90
m: A blocked duct backs up bile and pushes enzymes from the duct lining into the blood
g: ALP and GGT rising more than ALT is cholestatic
f: ALT of 1,200 with a near-normal ALP => Hepatitic
x: Hepatitic => Would show ALT many times higher than ALP
x: Isolated unconjugated hyperbilirubinaemia => Pale stools and high ALP mean conjugated bile is blocked
x: Liver synthetic failure => Albumin is normal
x: Normal => Every enzyme is raised

@u 41 2N
s: A 22 year old man noticed yellow eyes during a bout of flu while he was eating little. He feels well otherwise. // He is mildly jaundiced. There is no liver or spleen enlargement.
$ Bilirubin ; 38 µmol/L ; <17
$ Conjugated bilirubin ; 4 µmol/L ; <7
$ ALT ; 22 IU/L ; 10–50
$ ALP ; 70 IU/L ; 25–115
$ Haemoglobin ; 152 g/L ; 130–175
$ Reticulocytes ; 1.0% ; 0.5–2.5
? Which is the most appropriate next step?
> Liver biopsy ; MRCP ; *Reassure and explain ; Stop all fatty foods ; Ultrasound abdomen
= Gilbert's syndrome: a mild unconjugated rise with fasting or illness, normal liver enzymes and no haemolysis. It is harmless.
~ Low haemoglobin with high reticulocytes → haemolysis.
c: during a bout of flu | eating little | Conjugated bilirubin 4 | Reticulocytes 1.0%
m: Lower activity of the enzyme that conjugates bilirubin shows up when fasting
g: Isolated unconjugated bilirubin with normal enzymes and no haemolysis is Gilbert's
f: a falling haemoglobin with reticulocytes of 8% => Ultrasound abdomen
x: Liver biopsy => Invasive and unhelpful in a benign condition
x: MRCP => For duct problems, which cause a conjugated rise
x: Stop all fatty foods => Fasting makes Gilbert's worse
x: Ultrasound abdomen => Not needed with normal enzymes and no symptoms

@u 43 2N
s: A 52 year old man has had severe epigastric pain going through to his back since last night. He drinks heavily. He was admitted 40 hours ago with acute pancreatitis.
$ Amylase ; 1,850 IU/L ; <100
$ White cell count ; 17.2 × 10⁹/L ; 3.8–10.0
$ Urea ; 18.0 mmol/L ; 2.5–7.8
$ Adjusted calcium ; 1.86 mmol/L ; 2.20–2.60
$ Glucose ; 8.2 mmol/L ; 4.0–7.8
$ Albumin ; 34 g/L ; 35–50
$ PaO2 breathing air ; 9.5 kPa ; 11–15
? How severe is his pancreatitis by the modified Glasgow score?
> Mild: 1 criterion ; Mild: 2 criteria ; Scoring needs a CT first ; Scoring needs amylase over 3,000 ; *Severe: 3 or more criteria
= Positive: white cells over 15, urea over 16 and calcium under 2. Glucose under 10, albumin over 32 and PaO2 over 8 are not. Amylase has no part in severity.
~ Score of 3 or more → manage in HDU or ICU.
c: 40 hours ago | White cell count 17.2 | Urea 18.0 | Adjusted calcium 1.86
m: Severe pancreatitis spills inflammation into the whole body, so cells, kidneys and calcium all change
g: Modified Glasgow: 3 or more within 48 hours is severe
f: a normal white count, urea and calcium => Mild: 1 criterion
x: Mild: 1 criterion => Three criteria are met
x: Mild: 2 criteria => White cells, urea and calcium all count
x: Scoring needs a CT first => Glasgow uses blood results within 48 hours; CT is for complications
x: Scoring needs amylase over 3,000 => Amylase level does not predict severity

@u 12 2R
s: A 72 year old man with COPD has an exacerbation. He has had nebulised salbutamol and ipratropium, prednisolone and amoxicillin, and is on 28% oxygen. // An hour later he is alert. Respiratory rate 28 breaths per minute, SpO2 89%.
$ pH ; 7.28 ; 7.35–7.45
$ PaCO2 ; 8.9 kPa ; 4.6–6.4
$ PaO2 ; 7.9 kPa ; 11–15
$ Bicarbonate ; 31 mmol/L ; 22–30
? Which is the most appropriate next step?
> 15 litres oxygen through a non-rebreather mask ; IV aminophylline ; Immediate intubation ; *Non-invasive ventilation ; Repeat the gas in 4 hours
= Acidotic type 2 respiratory failure despite full medical treatment: NIV, a bilevel mask that blows off CO2. Decide ceilings of care early.
~ pH 7.38 with a high bicarbonate → chronic compensated, continue controlled oxygen.
c: COPD | 28% oxygen | pH 7.28 | PaCO2 8.9
m: Tired breathing muscles cannot clear CO2, so acid builds up faster than the kidney can buffer
g: pH under 7.35 with PaCO2 over 6.5 after medical treatment: start NIV
f: a pH of 7.38 with the same CO2 => Repeat the gas in 4 hours
x: 15 litres oxygen through a non-rebreather mask => Uncontrolled oxygen raises CO2 further in COPD
x: IV aminophylline => Little benefit and narrow safety margin
x: Immediate intubation => He is alert; NIV comes first unless it fails or he is not protecting his airway
x: Repeat the gas in 4 hours => Delays treatment of a worsening acidosis

@u 111 3N
s: A 24 year old woman took a large number of aspirin tablets 6 hours ago. She has ringing in her ears and is breathing fast. // Respiratory rate 30 breaths per minute.
$ pH ; 7.44 ; 7.35–7.45
$ PaCO2 ; 2.9 kPa ; 4.6–6.4
$ Bicarbonate ; 14 mmol/L ; 22–30
$ Sodium ; 140 mmol/L ; 135–146
$ Chloride ; 102 mmol/L ; 95–106
? Which best describes the blood gas?
> Metabolic acidosis with full compensation ; Metabolic alkalosis with respiratory compensation ; *Mixed respiratory alkalosis and metabolic acidosis ; Normal gas ; Acute respiratory alkalosis without acidosis
= Salicylates drive breathing directly, and also cause a raised anion gap acidosis, here 24. Compensation never brings pH fully back to normal, so a normal pH means two processes.
~ pH 7.52 with low CO2 and normal bicarbonate → acute respiratory alkalosis alone.
c: aspirin | ringing in her ears | pH 7.44 | PaCO2 2.9 | Bicarbonate 14
m: Salicylate stimulates the breathing centre and also uncouples cell energy, making acid
g: Low CO2 and low bicarbonate with a normal pH is a mixed disorder
f: a normal bicarbonate of 25 => Acute respiratory alkalosis without acidosis
x: Metabolic acidosis with full compensation => Compensation alone does not normalise pH, and her CO2 is lower than expected
x: Metabolic alkalosis with respiratory compensation => Bicarbonate is low, not high
x: Normal gas => CO2 and bicarbonate are both far from normal
x: Acute respiratory alkalosis without acidosis => The low bicarbonate and raised anion gap show an added acidosis

@u 9 2N
s: A 68 year old man who smokes has had breathlessness for 6 weeks. Chest X-ray shows a right pleural effusion. A diagnostic tap is done.
$ Pleural fluid protein ; 32 g/L ;
$ Serum protein ; 64 g/L ; 60–80
$ Pleural fluid LDH ; 260 IU/L ;
$ Serum LDH ; 220 IU/L ; upper limit 250
$ Pleural fluid pH ; 7.40 ;
? Which best describes the fluid?
> Chylothorax ; Empyema ; *Exudate ; Haemothorax ; Transudate
= Light's: an exudate if the protein ratio is over 0.5, the LDH ratio over 0.6, or pleural LDH over two thirds of the serum upper limit. The LDH ratio of 1.2 decides it.
~ Pleural protein 18 with LDH 90 → transudate, as in heart failure.
c: smokes | Pleural fluid protein 32 | Pleural fluid LDH 260 | Serum LDH 220
m: Leaky inflamed or cancerous pleura lets large proteins and LDH through
g: Any one of Light's criteria makes it an exudate
f: pleural protein of 18 and LDH of 90 => Transudate
x: Chylothorax => Milky fluid with high triglycerides
x: Empyema => Pus or a pH under 7.2
x: Haemothorax => Blood with a high fluid haematocrit
x: Transudate => The LDH ratio is over 0.6

@u 9 3R
s: A 56 year old man has had pneumonia for 6 days and is not improving on antibiotics. Ultrasound shows a moderate right pleural effusion. The fluid is cloudy but not frankly purulent.
$ Pleural fluid pH ; 7.08 ;
$ Pleural fluid glucose ; 2.1 mmol/L ;
$ Pleural fluid LDH ; 1,400 IU/L ;
? Which is the most appropriate next step?
> Continue oral antibiotics ; Repeat ultrasound in 2 weeks ; Talc pleurodesis ; Therapeutic aspiration ; *Ultrasound-guided chest drain
= A complicated parapneumonic effusion, pH under 7.2, will not clear with antibiotics alone and needs a drain.
~ pH 7.40 with clear fluid → simple effusion, antibiotics alone.
c: not improving on antibiotics | Pleural fluid pH 7.08 | Pleural fluid glucose 2.1
m: Bacteria in the pleura consume glucose and make acid
g: Pleural pH under 7.2 in infection means drain it
f: a pH of 7.40 and clear fluid => Continue oral antibiotics
x: Continue oral antibiotics => Antibiotics cannot sterilise an acidic infected collection
x: Repeat ultrasound in 2 weeks => Delay lets it loculate and thicken
x: Talc pleurodesis => For recurrent malignant effusions, not infection
x: Therapeutic aspiration => Infected fluid reaccumulates; a drain is needed

@u 111 2N
s: A 36 year old man takes lithium 800 mg at 10pm each night. He feels well. A routine level was taken at 2pm the next day at a clinic visit.
$ Lithium ; 1.3 mmol/L ; 0.4–1.0
$ Creatinine ; 84 µmol/L ; 60–120
$ Sodium ; 140 mmol/L ; 135–146
? Which is the most appropriate next step?
> Halve the lithium dose ; Arrange urgent haemodialysis ; Admit for IV fluids ; *Repeat a 12-hour level ; Stop lithium today
= The reference range applies to levels taken 12 hours after the dose. At 16 hours this reads high, but he is well with normal kidney function; repeat it timed correctly before changing anything.
~ Timed 12-hour level of 1.6 with tremor and vomiting → stop lithium and admit.
c: 800 mg at 10pm | at 2pm the next day | feels well | Lithium 1.3
m: Lithium levels fall over the day after a dose, so timing changes the reading
g: Interpret lithium only on a 12-hour level
f: a 12-hour level of 1.8 with coarse tremor and diarrhoea => Stop lithium today
x: Halve the lithium dose => Changing the dose on a mistimed level risks relapse
x: Arrange urgent haemodialysis => For severe toxicity, not a well man with a mistimed level
x: Admit for IV fluids => Not needed; he is well and not dry
x: Stop lithium today => Premature; confirm with a correctly timed level first

@u 111 3T
s: A 30 year old woman has taken extra paracetamol tablets over 3 days for toothache, about 8 g a day. She is not sure of the times. She feels nauseated. Her paracetamol level is 18 mg/L.
$ ALT ; 450 IU/L ; 10–50
$ INR ; 1.6 ; 0.8–1.2
? Which is the most appropriate management?
> Activated charcoal ; Discharge as the level is low ; Plot the level on the nomogram ; Repeat the level in 4 hours ; *Start IV acetylcysteine now
= Staggered overdose: the nomogram cannot be used. Start acetylcysteine for anyone with a significant staggered dose or abnormal liver tests, whatever the level.
~ Single overdose with a known time 4 hours ago → plot the level on the nomogram.
c: over 3 days | not sure of the times | ALT 450 | INR 1.6
m: Repeated doses saturate the safe pathway, so toxic metabolite builds up despite a low level
g: Staggered overdose or unknown timing: treat without the nomogram
f: a single overdose taken exactly 4 hours ago with normal liver tests => Plot the level on the nomogram
x: Activated charcoal => Only useful within an hour of a large single dose
x: Discharge as the level is low => A low level does not exclude toxicity in a staggered overdose
x: Plot the level on the nomogram => Only valid for a single ingestion at a known time
x: Repeat the level in 4 hours => Delays treatment when the liver is already injured

@u 110 2L
s: A 58 year old man has drunk heavily for 30 years. He was treated for Wernicke's encephalopathy 2 months ago. He is now alert and attentive, but cannot remember what he did this morning. He describes going to the shops today, although he has not left the ward. // There is no flapping tremor.
$ Sodium ; 138 mmol/L ; 135–146
$ Glucose ; 5.4 mmol/L ; 4.0–7.8
$ Ammonia ; 32 µmol/L ; <50
? Which is the most likely diagnosis?
> Alzheimer's disease ; Delirium tremens ; Hepatic encephalopathy ; *Korsakoff's syndrome ; Wernicke's encephalopathy
= Korsakoff's: severe loss of new memory with confabulation, in a clear and alert person, after thiamine deficiency. It is often permanent.
~ Confusion, ataxia and eye movement problems → Wernicke's, IV Pabrinex now.
c: treated for Wernicke's encephalopathy | alert and attentive | although he has not left the ward | Ammonia 32
m: Thiamine lack damages the mamillary bodies and memory circuits
g: Alert with amnesia and confabulation after Wernicke's is Korsakoff's
f: confusion, ataxia and nystagmus => Wernicke's encephalopathy
x: Alzheimer's disease => Gradual over years with wider cognitive decline, not linked to thiamine
x: Delirium tremens => Agitated, fluctuating attention with tremor, within days of stopping alcohol
x: Hepatic encephalopathy => Ammonia is normal and there is no flapping tremor
x: Wernicke's encephalopathy => The acute triad of confusion, ataxia and eye signs; he is now alert

@u 93 2N
s: A 19 year old student has had a headache, fever and neck stiffness for 12 hours. A lumbar puncture is done after CT head.
$ CSF white cells ; 1,200 per mm³, mostly neutrophils ; <5
$ CSF protein ; 2.1 g/L ; 0.15–0.45
$ CSF glucose ; 1.0 mmol/L ;
$ Blood glucose ; 6.0 mmol/L ; 4.0–7.8
? Which is the most likely cause?
> *Bacterial meningitis ; Subarachnoid haemorrhage ; Tuberculous meningitis ; Viral encephalitis ; Viral meningitis
= Bacterial meningitis: neutrophils, high protein and a CSF to blood glucose ratio under 0.4, here 0.17.
~ Lymphocytes with normal glucose → viral meningitis.
c: 12 hours | 1,200 per mm³, mostly neutrophils | CSF glucose 1.0
m: Bacteria and neutrophils consume glucose in the CSF
g: Neutrophils with a very low glucose ratio is bacterial
f: lymphocytes with a normal glucose ratio => Viral meningitis
x: Subarachnoid haemorrhage => Red cells and xanthochromia, not neutrophils
x: Tuberculous meningitis => Lymphocytes over weeks
x: Viral encephalitis => Behaviour change and seizures with a lymphocytic CSF
x: Viral meningitis => Lymphocytes with normal glucose

@u 93 3N
s: A 34 year old man who arrived from Somalia a year ago has had a headache, weight loss and fevers for 3 weeks. He now has double vision. // There is a right sixth nerve palsy and neck stiffness.
$ CSF white cells ; 280 per mm³, mostly lymphocytes ; <5
$ CSF protein ; 2.6 g/L ; 0.15–0.45
$ CSF glucose ; 1.4 mmol/L ;
$ Blood glucose ; 5.6 mmol/L ; 4.0–7.8
? Which is the most likely diagnosis?
> Bacterial meningitis ; Cryptococcal meningitis ; Subarachnoid haemorrhage ; *Tuberculous meningitis ; Viral meningitis
= TB meningitis: weeks of illness, cranial nerve palsies from basal inflammation, lymphocytes, very high protein and low glucose.
~ Same CSF in advanced HIV with a positive antigen → cryptococcal meningitis.
c: a year ago | 3 weeks | sixth nerve palsy | mostly lymphocytes | CSF protein 2.6
m: Thick inflammation at the base of the brain traps cranial nerves
g: Subacute meningitis with lymphocytes, high protein and low glucose suggests TB
f: advanced HIV with a positive cryptococcal antigen => Cryptococcal meningitis
x: Bacterial meningitis => Hours to days with neutrophils
x: Cryptococcal meningitis => Usually in advanced HIV; antigen testing would show it
x: Subarachnoid haemorrhage => Sudden onset with blood in the CSF
x: Viral meningitis => Normal glucose and a short illness

@u 91 2N
s: A 46 year old woman had a sudden severe headache 14 hours ago. CT head is normal. A lumbar puncture is done.
$ CSF tube 1 red cells ; 3,200 per mm³ ;
$ CSF tube 3 red cells ; 3,050 per mm³ ;
$ CSF xanthochromia ; Present ;
$ CSF white cells ; 4 per mm³ ; <5
? What do these results show?
> Bacterial meningitis ; Normal ; *Subarachnoid haemorrhage ; Traumatic tap ; Viral meningitis
= Blood that does not clear between tubes, with yellow bilirubin pigment formed over 12 hours, means bleeding before the needle went in.
~ Red cells falling from 3,200 to 40 with no xanthochromia → traumatic tap.
c: sudden severe headache 14 hours ago | Tube 3 red cells 3,050 | Xanthochromia Present
m: Red cells broken down in the CSF over hours make bilirubin, which turns it yellow
g: Xanthochromia 12 hours after onset confirms subarachnoid blood
f: red cells falling to 40 in tube 3 with no xanthochromia => Traumatic tap
x: Bacterial meningitis => White cells are normal
x: Normal => Thousands of red cells and xanthochromia are not normal
x: Traumatic tap => Counts would fall across the tubes, with no xanthochromia
x: Viral meningitis => White cells are normal and there is blood

@u 28 2N
s: A 30 year old woman has bloating, loose stools and iron deficiency anaemia. She has had chest infections often. She eats gluten daily.
$ Tissue transglutaminase IgA ; Negative ;
$ Total IgA ; <0.05 g/L ; 0.7–4.0
$ Ferritin ; 7 µg/L ; 12–200
? Which is the most appropriate next step?
> Faecal calprotectin ; Gluten challenge for 6 weeks ; *IgG-based coeliac tests ; Reassure that coeliac is excluded ; Repeat tTG IgA in 6 months
= IgA deficiency is commoner in coeliac disease and makes IgA tests falsely negative. Use IgG tests and refer for biopsy if suspicion remains.
~ Normal total IgA with a negative tTG → coeliac is unlikely.
c: iron deficiency anaemia | chest infections often | Tissue transglutaminase IgA Negative | Total IgA <0.05
m: A person who makes no IgA cannot make IgA antibodies against gluten
g: Check total IgA; if low, use IgG coeliac tests
f: a normal total IgA => Faecal calprotectin
x: Faecal calprotectin => Helps with IBD, but coeliac is still untested
x: Gluten challenge for 6 weeks => She already eats gluten every day
x: Reassure that coeliac is excluded => The negative test is invalid with no IgA
x: Repeat tTG IgA in 6 months => It will be negative again for the same reason

@u 25 2R
s: A 28 year old man with ulcerative colitis has had 9 bloody stools a day for 3 days. // Temperature 37.9°C, pulse rate 104 bpm.
$ Haemoglobin ; 102 g/L ; 130–175
$ CRP ; 64 mg/L ; <5
$ Albumin ; 31 g/L ; 35–50
? Which is the most appropriate management?
> *Admit for IV hydrocortisone ; Increase oral mesalazine ; Loperamide ; Oral prednisolone at home ; Rectal mesalazine
= Acute severe colitis by Truelove and Witts: 6 or more bloody stools plus a systemic sign. Admit for IV steroids, VTE prophylaxis and daily review with the surgeons.
~ No improvement after 3 days of IV steroids → rescue with ciclosporin or infliximab, or colectomy.
c: 9 bloody stools a day | Temperature 37.9 | pulse rate 104 | Haemoglobin 102
m: Inflamed colon loses blood and protein and can dilate or perforate
g: 6 or more bloody stools with fever, tachycardia, anaemia or raised markers is acute severe colitis
f: 3 bloody stools a day with normal observations => Increase oral mesalazine
x: Increase oral mesalazine => Too weak for acute severe colitis
x: Loperamide => Antimotility drugs can trigger toxic megacolon
x: Oral prednisolone at home => He needs admission and IV steroids
x: Rectal mesalazine => For mild distal disease

@u 98 2D
s: A 62 year old man started atorvastatin 80 mg after a heart attack 2 months ago. He has aching thighs and shoulders. // There is mild proximal tenderness. His urine is not dark.
$ Creatine kinase ; 4,200 IU/L ; 25–200
$ Creatinine ; 88 µmol/L ; 60–120
$ TSH ; 1.9 mU/L ; 0.3–4.2
? Which is the most appropriate management?
> Add coenzyme Q10 and continue ; Continue and recheck in 6 weeks ; Halve the dose ; *Stop the statin and recheck CK ; Switch to simvastatin 80 mg
= CK over 5 times the upper limit with muscle symptoms: stop the statin, recheck, then reintroduce a lower dose or another statin once settled. Check TSH, as hypothyroidism raises the risk.
~ Mild aches with a normal CK → continue, or try a lower dose.
c: atorvastatin 80 mg | aching thighs and shoulders | Creatine kinase 4,200
m: High-intensity statins can injure muscle cells
g: CK over 5 times normal with symptoms: stop the statin
f: muscle aches with a normal CK => Continue and recheck in 6 weeks
x: Add coenzyme Q10 and continue => No good evidence, and the CK is too high to continue
x: Continue and recheck in 6 weeks => Risks rhabdomyolysis
x: Halve the dose => Stop first; reintroduce only once the CK settles
x: Switch to simvastatin 80 mg => Simvastatin 80 mg has the highest myopathy risk

@u 5 3R
s: A 34 year old man has had a cholesterol test because his father had a heart attack at 44. He has thickened Achilles tendons with nodules.
$ Total cholesterol ; 9.8 mmol/L ; <5.0
$ LDL cholesterol ; 7.6 mmol/L ; <3.0
$ Triglycerides ; 1.4 mmol/L ; <1.7
$ TSH ; 1.6 mU/L ; 0.3–4.2
? Which is the most appropriate next step?
> Calculate his QRISK3 score ; Lifestyle advice and recheck in a year ; Omega-3 supplements ; *Refer to a lipid clinic ; Start atorvastatin 20 mg and discharge
= Suspected familial hypercholesterolaemia: a very high LDL, tendon xanthomas and early heart disease in a parent. Refer for genetic testing, high-intensity treatment and family cascade testing.
~ Total cholesterol 6.4 with no family history → QRISK3.
c: father had a heart attack at 44 | Achilles tendons with nodules | LDL cholesterol 7.6
m: Faulty LDL receptors leave LDL in the blood from birth
g: Total cholesterol over 7.5 with premature heart disease in a relative suggests FH
f: a total cholesterol of 6.4 and no family history => Calculate his QRISK3 score
x: Calculate his QRISK3 score => QRISK3 underestimates risk in FH and is not used
x: Lifestyle advice and recheck in a year => Delays treatment of a lifelong high LDL
x: Omega-3 supplements => Do not lower LDL or events
x: Start atorvastatin 20 mg and discharge => Too weak, and misses specialist care and family testing

@u 86 2L
s: A 72 year old woman has a hot, swollen right knee for 2 days. She is otherwise well. // Knee X-ray shows a line of calcium in the cartilage. Aspirate shows weakly positively birefringent rhomboid crystals and no organisms.
$ Adjusted calcium ; 2.74 mmol/L ; 2.20–2.60
$ PTH ; 9.8 pmol/L ; 1.6–8.5
$ Ferritin ; 140 µg/L ; 12–200
$ Transferrin saturation ; 32% ; 20–50
? Which underlying condition explains her results?
> Gout ; Haemochromatosis ; *Primary hyperparathyroidism ; Rheumatoid arthritis ; Septic arthritis
= Calcium pyrophosphate crystals, pseudogout, are linked to hyperparathyroidism, haemochromatosis, hypothyroidism and low magnesium. Here calcium and PTH are both high.
~ Transferrin saturation 70% and high ferritin → haemochromatosis.
c: weakly positively birefringent rhomboid crystals | Adjusted calcium 2.74 | PTH 9.8 | Transferrin saturation 32%
m: High calcium favours calcium pyrophosphate crystals forming in cartilage
g: Pseudogout with high calcium and PTH is primary hyperparathyroidism
f: a transferrin saturation of 70% with a high ferritin => Haemochromatosis
x: Gout => Needle-shaped negatively birefringent crystals
x: Haemochromatosis => Iron studies are normal
x: Rheumatoid arthritis => Symmetrical small joint disease without crystals
x: Septic arthritis => No organisms, and the crystals explain it

@u 71 2D
s: A 58 year old man has type 2 diabetes on metformin. He feels well. A urine test has been repeated to confirm the result. // BP 138/84 mmHg.
$ Urine albumin to creatinine ratio ; 8 mg/mmol ; <3
$ eGFR ; 72 mL/min/1.73 m² ; >60
$ HbA1c ; 52 mmol/mol ; 20–42
? Which is the most appropriate next step?
> Add dapagliflozin before an ACE inhibitor ; Refer to nephrology ; Repeat the ACR in a year ; *Start an ACE inhibitor ; Stop metformin
= An ACR over 3 in diabetes means early kidney damage. Start an ACE inhibitor or ARB at the highest tolerated dose, then consider an SGLT2 inhibitor alongside.
~ ACR 80 with eGFR falling fast → nephrology referral.
c: type 2 diabetes | repeated to confirm | Urine albumin to creatinine ratio 8
m: High glomerular pressure leaks albumin; ACE inhibitors relax the outflow arteriole
g: Diabetes with ACR over 3: ACE inhibitor or ARB
f: an ACR of 80 with eGFR falling by 30% in a year => Refer to nephrology
x: Add dapagliflozin before an ACE inhibitor => The ACE inhibitor or ARB comes first
x: Refer to nephrology => Not yet needed at this ACR with a stable eGFR
x: Repeat the ACR in a year => It is already confirmed; treat now
x: Stop metformin => eGFR is 72, so metformin is safe

@u 13 3R
s: A 56 year old woman collapsed at home. CT pulmonary angiogram shows a large saddle embolus. // Pulse rate 128 bpm, BP 78/42 mmHg despite fluids. Bedside echo shows a dilated right ventricle.
$ Troponin T ; 96 ng/L ; <14
$ Lactate ; 4.8 mmol/L ; <2.0
? Which is the most appropriate treatment?
> Apixaban ; Inferior vena cava filter ; Treatment-dose LMWH and observe ; *Thrombolysis with alteplase ; Warfarin
= Massive PE with shock: thrombolysis unless there is a strong bleeding contraindication, then unfractionated heparin.
~ Stable with a normal BP but a strained right ventricle → anticoagulation and close watch.
c: saddle embolus | BP 78/42 mmHg despite fluids | dilated right ventricle
m: A clot blocking the pulmonary arteries makes the right ventricle fail and cardiac output collapse
g: PE with persistent hypotension: thrombolyse
f: BP 128/76 with a mildly strained right ventricle => Treatment-dose LMWH and observe
x: Apixaban => Too slow to rescue a failing right ventricle
x: Inferior vena cava filter => Only if anticoagulation is impossible
x: Treatment-dose LMWH and observe => For stable PE
x: Warfarin => Takes days to work

@u 32 2R
s: A 68 year old man has had two episodes of melaena since yesterday. He takes ibuprofen for knee pain. // Pulse rate 98 bpm, BP 118/72 mmHg. He looks well.
$ Haemoglobin ; 104 g/L ; 130–175
$ Urea ; 12.2 mmol/L ; 2.5–7.8
$ Platelets ; 240 × 10⁹/L ; 150–400
$ INR ; 1.0 ; 0.8–1.2
? When should endoscopy be done?
> Discharge for outpatient endoscopy ; Endoscopy in 2 weeks ; Immediate endoscopy in theatre ; *Within 24 hours of admission ; CT angiogram first
= A raised urea and low haemoglobin give a Glasgow-Blatchford score well above 0, so he needs admission and endoscopy within 24 hours. Unstable patients are scoped immediately after resuscitation.
~ Pulse 128 and BP 84/50 → resuscitate, then immediate endoscopy.
c: melaena | ibuprofen | Haemoglobin 104 | Urea 12.2
m: Blood digested in the gut raises urea
g: Stable upper GI bleed with a Blatchford score above 0: endoscopy within 24 hours
f: pulse 128 and BP 84/50 => Immediate endoscopy in theatre
x: Discharge for outpatient endoscopy => Only for a Blatchford score of 0
x: Endoscopy in 2 weeks => Far too slow for a bleed with a raised urea
x: Immediate endoscopy in theatre => For unstable patients after resuscitation
x: CT angiogram first => For bleeding that endoscopy cannot find or control

@u 32 3L
s: A 46 year old man has had several duodenal and jejunal ulcers despite high-dose omeprazole, with watery diarrhoea and weight loss. He does not take NSAIDs. H. pylori tests are negative. // Kidney stones were treated last year.
$ Fasting gastrin ; 1,200 ng/L ; <100
$ Adjusted calcium ; 2.82 mmol/L ; 2.20–2.60
$ PTH ; 12.0 pmol/L ; 1.6–8.5
? Which is the most likely diagnosis?
> Coeliac disease ; Crohn's disease ; *Gastrinoma ; H. pylori infection ; NSAID ulceration
= Zollinger-Ellison syndrome: a gastrinoma drives huge acid output, causing multiple and distal ulcers and diarrhoea. High calcium suggests MEN 1.
~ Single duodenal ulcer with positive H. pylori → eradication therapy.
c: jejunal ulcers | despite high-dose omeprazole | Fasting gastrin 1,200 | Adjusted calcium 2.82
m: A tumour making gastrin makes the stomach pour out acid
g: Multiple or distal ulcers with high gastrin suggest a gastrinoma
f: one duodenal ulcer and a positive breath test => H. pylori infection
x: Coeliac disease => Causes malabsorption but not peptic ulcers
x: Crohn's disease => Can ulcerate the bowel, but would not raise gastrin
x: H. pylori infection => Tests are negative
x: NSAID ulceration => He takes no NSAIDs

@u 21 2L
s: A 66 year old man who smokes has a central lung mass on CT. He has become confused. He is euvolaemic. Thyroid function and a short Synacthen test are normal.
$ Sodium ; 121 mmol/L ; 135–146
$ Serum osmolality ; 252 mOsm/kg ; 275–295
$ Urine osmolality ; 480 mOsm/kg ;
$ Urine sodium ; 45 mmol/L ;
? Which type of lung cancer is most likely?
> Adenocarcinoma ; Carcinoid tumour ; Mesothelioma ; *Small cell lung cancer ; Squamous cell carcinoma
= SIADH: low serum osmolality with inappropriately concentrated urine in a euvolaemic patient. Small cell tumours make ADH.
~ High calcium with low PTH → squamous cell carcinoma making PTH-related peptide.
c: central lung mass | euvolaemic | Serum osmolality 252 | Urine osmolality 480
m: Neuroendocrine tumour cells release ADH, so the kidney keeps water
g: SIADH with a central lung mass suggests small cell cancer
f: a calcium of 3.2 with a low PTH => Squamous cell carcinoma
x: Adenocarcinoma => Peripheral, in non-smokers too, not typically SIADH
x: Carcinoid tumour => Can cause flushing or Cushing's, rarely SIADH
x: Mesothelioma => A pleural tumour after asbestos
x: Squamous cell carcinoma => Linked to high calcium, not low sodium

@u 21 2N
s: A 70 year old woman with squamous cell lung cancer is confused, thirsty and constipated. An isotope bone scan shows no metastases.
$ Adjusted calcium ; 3.24 mmol/L ; 2.20–2.60
$ PTH ; 0.6 pmol/L ; 1.6–8.5
$ Phosphate ; 0.70 mmol/L ; 0.80–1.50
? Which is the most likely cause of her high calcium?
> Lytic bone metastases from the tumour ; Primary hyperparathyroidism ; *PTH-related peptide from the tumour ; Sarcoidosis ; Vitamin D toxicity
= Squamous tumours release PTH-related peptide, which acts like PTH on bone and kidney, so calcium rises, phosphate falls and real PTH is suppressed.
~ High calcium with a high PTH → primary hyperparathyroidism.
c: squamous cell lung cancer | no metastases | PTH 0.6 | Phosphate 0.70
m: A tumour hormone mimics PTH while the glands switch off
g: High calcium, suppressed PTH, low phosphate and no bone spread suggest PTH-related peptide
f: a high PTH => Primary hyperparathyroidism
x: Lytic bone metastases from the tumour => The bone scan is clear
x: Primary hyperparathyroidism => PTH would be high
x: Sarcoidosis => Raises vitamin D and calcium with a normal or high phosphate
x: Vitamin D toxicity => High phosphate and a history of supplements

@u 8 3T
s: A 70 year old man was treated for infective endocarditis of his aortic valve. Blood cultures grew Streptococcus gallolyticus. He has no gut symptoms.
$ Haemoglobin ; 98 g/L ; 130–175
$ MCV ; 74 fL ; 80–96
$ Ferritin ; 8 µg/L ; 12–200
? Which investigation is most important now?
> *Colonoscopy ; Dental review ; HIV test ; Repeat echocardiogram in a year ; Urine culture
= Strep gallolyticus, once Strep bovis, is strongly linked to colorectal cancer, and here there is iron deficiency too.
~ Viridans streptococci after dental work → dental review.
c: Streptococcus gallolyticus | MCV 74 | Ferritin 8
m: The organism enters the blood through a diseased colon wall
g: Strep gallolyticus endocarditis means look for a colonic tumour
f: Streptococcus sanguinis after a tooth extraction => Dental review
x: Dental review => For viridans streptococci
x: HIV test => Not specifically suggested by this organism
x: Repeat echocardiogram in a year => Does not address the likely source
x: Urine culture => Enterococcus links to the urinary tract, not this organism

@u 19 2L
s: A 20 year old student has had a dry cough, headache and muscle aches for 10 days. Several flatmates were also ill. He has a target-like rash on his hands. // Chest X-ray shows patchy shadowing in both lower zones.
$ Haemoglobin ; 108 g/L ; 130–175
$ Bilirubin ; 34 µmol/L ; <17
$ Reticulocytes ; 4% ; 0.5–2.5
$ Cold agglutinins ; Positive ;
? Which organism is most likely?
> Chlamydia psittaci ; Legionella pneumophila ; *Mycoplasma pneumoniae ; Staphylococcus aureus ; Streptococcus pneumoniae
= Mycoplasma: young people in close groups, a slow dry cough, extra-chest features such as erythema multiforme, and cold agglutinin haemolysis.
~ Hotel shower, low sodium and abnormal liver tests → Legionella.
c: Several flatmates were also ill | target-like rash | Cold agglutinins Positive
m: Antibodies against Mycoplasma cross-react with red cells in the cold
g: Atypical pneumonia with cold agglutinins and erythema multiforme is Mycoplasma
f: a hotel shower, sodium of 126 and a raised ALT => Legionella pneumophila
x: Chlamydia psittaci => Contact with birds
x: Legionella pneumophila => Low sodium, diarrhoea and confusion after water systems
x: Staphylococcus aureus => Severe cavitating pneumonia after flu
x: Streptococcus pneumoniae => Sudden lobar pneumonia with rusty sputum

@u 19 2N
s: A 58 year old man returned from a hotel in Spain a week ago. He has a fever, cough, diarrhoea and confusion. // Chest X-ray shows right lower lobe consolidation.
$ Sodium ; 126 mmol/L ; 135–146
$ ALT ; 120 IU/L ; 10–50
$ CRP ; 290 mg/L ; <5
? Which test is most likely to confirm the cause?
> Blood cultures ; Cold agglutinins ; Sputum Gram stain ; Throat swab for viruses ; *Urinary antigen test
= Legionella: water systems, low sodium, abnormal liver tests, diarrhoea and confusion. A urinary antigen test gives a quick answer.
~ Rusty sputum with lobar pneumonia → pneumococcal urinary antigen and blood cultures.
c: hotel in Spain | diarrhoea and confusion | Sodium 126 | ALT 120
m: Bacteria in warm water droplets are inhaled and affect many organs
g: Pneumonia with low sodium after travel and hotels suggests Legionella
f: rusty sputum in a sudden lobar pneumonia => Blood cultures
x: Blood cultures => Legionella rarely grows in standard cultures
x: Cold agglutinins => For Mycoplasma
x: Sputum Gram stain => Legionella stains poorly
x: Throat swab for viruses => Does not fit this picture

@u 0 3T
s: A 64 year old man has had central chest pain for an hour. ECG shows ST elevation in II, III and aVF and in V4R. He became hypotensive after a GTN spray. // BP 84/50 mmHg, pulse rate 58 bpm. The JVP is raised. The chest is clear. The cath lab is being prepared.
? Which is the most appropriate immediate step?
> Another GTN spray ; *IV fluid bolus ; IV furosemide ; IV morphine and nitrate infusion ; Oral bisoprolol
= Right ventricular infarction: the right ventricle depends on filling. Give fluids, avoid nitrates and diuretics, and reperfuse.
~ Raised JVP with crackles to the mid zones → left ventricular failure, cautious diuretic.
c: V4R | hypotensive after a GTN spray | JVP is raised | chest is clear
m: A stunned right ventricle needs a high filling pressure to push blood to the lungs
g: Inferior STEMI with hypotension, raised JVP and clear lungs is an RV infarct: fluids, no nitrates
f: crackles to the mid zones with a high BP => IV furosemide
x: Another GTN spray => Nitrates cut preload and deepen the hypotension
x: IV furosemide => Drops the filling the right ventricle needs
x: IV morphine and nitrate infusion => Both lower preload
x: Oral bisoprolol => Slows the heart and lowers BP further

@u 0 2L
s: A 62 year old man had a myocardial infarction 3 weeks ago. He now has sharp chest pain that is worse lying down and a fever. // Temperature 37.9°C. There is a pericardial rub. ECG shows widespread saddle-shaped ST elevation. ESR is raised.
? Which is the most likely diagnosis?
> Cardiac tamponade ; *Dressler syndrome ; Left ventricular aneurysm ; Pulmonary embolism ; Reinfarction
= Dressler syndrome is an immune pericarditis weeks after an MI or heart surgery. Treat with an NSAID or aspirin, and colchicine.
~ Pericarditis within 1 to 3 days of the MI → early post-infarct pericarditis.
c: 3 weeks ago | worse lying down | pericardial rub | ESR is raised
m: The immune system reacts against damaged heart muscle and the pericardium
g: Pericarditis weeks after an MI with fever is Dressler syndrome
f: a new pansystolic murmur and flash oedema on day 4 => Reinfarction
x: Cardiac tamponade => Low BP, raised JVP and muffled heart sounds
x: Left ventricular aneurysm => Persistent ST elevation without pain or fever
x: Pulmonary embolism => Pleuritic pain with breathlessness and hypoxia, not a rub with saddle ST changes
x: Reinfarction => Pain like the original MI with a new troponin rise in one territory

@u 0 3T
s: A 66 year old man had a large anterior myocardial infarction 6 weeks ago that was treated late. He is well. // His ECG still shows ST elevation in V1 to V4. Echo shows a thin, bulging, akinetic apex.
? Which complication most needs preventing now?
> Aortic dissection ; Complete heart block needing pacing ; *Mural thrombus with embolism ; Pericarditis ; Mitral stenosis
= A left ventricular aneurysm leaves blood still in the apex, so clot forms and can cause a stroke. Anticoagulation is often given.
~ Pericarditis with fever weeks later → Dressler syndrome.
c: treated late | still shows ST elevation | akinetic apex
m: Blood pools in a motionless scarred pouch and clots
g: Persistent ST elevation after an anterior MI with an akinetic apex is an LV aneurysm
x: Aortic dissection => Not caused by an LV aneurysm
x: Complete heart block needing pacing => Linked more to inferior MI
x: Pericarditis => Early or immune pericarditis, not the main danger now
x: Mitral stenosis => A valve disease, usually rheumatic

@u 90 3T
s: A 34 year old man has a known brain tumour. He has become drowsy over 2 hours. // GCS 9. BP 194/96 mmHg, pulse rate 46 bpm, and his breathing is irregular.
? What does this combination of signs mean?
> Autonomic dysreflexia ; Beta-blocker overdose ; Hypertensive emergency ; *Impending brain herniation ; Sepsis
= Cushing's triad, high blood pressure, slow pulse and irregular breathing, is a late sign of rising pressure in the skull. It needs urgent neurosurgical help.
~ High BP with a fast pulse and papilloedema in a known hypertensive → hypertensive emergency.
c: brain tumour | drowsy | BP 194/96 mmHg, pulse rate 46 bpm | breathing is irregular
m: The body raises BP to keep blood reaching a squeezed brainstem
g: Hypertension, bradycardia and irregular breathing with falling GCS is Cushing's triad
f: a spinal injury above T6 with a full bladder => Autonomic dysreflexia
x: Autonomic dysreflexia => Spinal cord injury above T6 with a trigger below it
x: Beta-blocker overdose => Low BP with a slow pulse
x: Hypertensive emergency => Usually a fast pulse and no falling GCS from a mass
x: Sepsis => Low BP with a fast pulse

@u 90 2T
s: A 27 year old woman with idiopathic intracranial hypertension has headaches and horizontal double vision on looking to each side. // She cannot fully abduct either eye.
? Which cranial nerve palsy is a false localising sign of raised pressure?
> *Abducens ; Facial ; Oculomotor ; Trigeminal ; Trochlear
= The sixth nerve has a long course over the skull base, so raised pressure stretches it wherever the cause lies.
~ A blown pupil with a falling GCS → third nerve compression from herniation.
c: idiopathic intracranial hypertension | cannot fully abduct either eye
m: A long thin nerve over the petrous ridge is stretched when pressure rises
g: Bilateral sixth nerve palsy with raised pressure is a false localising sign
f: a fixed dilated pupil with a falling GCS => Oculomotor
x: Facial => Not typically stretched by raised pressure
x: Oculomotor => A third nerve palsy from uncal herniation is a true localising sign
x: Trigeminal => Gives facial numbness, not double vision
x: Trochlear => Causes vertical double vision on looking down

@u 99 3L
s: A 48 year old man has had weakness and numbness in both legs and arms that has worsened slowly over 4 months. // Reflexes are absent. There is distal and proximal weakness. CSF protein is high with normal cells. Nerve conduction shows demyelination.
? Which is the most likely diagnosis?
> Hereditary motor and sensory neuropathy ; *Chronic inflammatory demyelinating polyneuropathy ; Acute inflammatory demyelinating polyneuropathy ; Motor neurone disease ; Subacute combined degeneration of the cord
= CIDP is like Guillain-Barré but progresses for over 8 weeks. Unlike GBS, it responds to steroids, and also to IVIG.
~ Rising weakness over 2 weeks after diarrhoea → Guillain-Barré syndrome.
c: worsened slowly over 4 months | Reflexes are absent | CSF protein is high | demyelination
m: The immune system strips myelin from nerve roots and nerves over months
g: Demyelinating neuropathy progressing over 8 weeks is CIDP
f: weakness rising over 2 weeks after a diarrhoeal illness => Acute inflammatory demyelinating polyneuropathy
x: Hereditary motor and sensory neuropathy => Charcot-Marie-Tooth: inherited and slow over years, with high arches
x: Acute inflammatory demyelinating polyneuropathy => Guillain-Barré syndrome, which peaks within 4 weeks
x: Motor neurone disease => No sensory loss, with brisk reflexes alongside wasting
x: Subacute combined degeneration of the cord => B12 deficiency gives brisk knee jerks with absent ankle jerks and dorsal column loss

@u 99 2L
s: A 24 year old man has tripped often since childhood. His father had the same problem. // He has high-arched feet, thin lower legs and absent ankle reflexes. There is mild distal sensory loss.
? Which is the most likely diagnosis?
> *Charcot-Marie-Tooth disease ; Diabetic neuropathy ; Friedreich's ataxia ; Guillain-Barré syndrome ; Multiple sclerosis
= Charcot-Marie-Tooth is an inherited neuropathy: pes cavus, inverted champagne bottle legs and foot drop, usually autosomal dominant.
~ Ataxia with diabetes and a cardiomyopathy in a teenager → Friedreich's ataxia.
c: since childhood | His father had the same problem | high-arched feet | thin lower legs
m: A faulty myelin or axon gene makes the longest nerves fail first
g: Lifelong distal weakness, pes cavus and an affected parent is CMT
x: Diabetic neuropathy => He has no diabetes, and it is mainly sensory
x: Friedreich's ataxia => Usually recessive with ataxia, diabetes and heart disease
x: Guillain-Barré syndrome => Acute, over days to weeks
x: Multiple sclerosis => Central signs such as brisk reflexes

@u 99 3T
s: A 52 year old woman with vasculitis has developed a right foot drop and, a month later, a left wrist drop.
? Which term best describes this pattern?
> Myopathy ; Motor neurone disease ; *Mononeuritis multiplex ; Polyradiculopathy ; Symmetrical polyneuropathy
= Damage to two or more separate named nerves, here the common peroneal and radial, is mononeuritis multiplex. Causes include vasculitis and diabetes.
~ Glove and stocking numbness → symmetrical polyneuropathy.
c: vasculitis | right foot drop | left wrist drop
m: Inflamed small arteries starve individual nerves one at a time
g: Separate nerves failing at different times is mononeuritis multiplex
f: glove and stocking numbness in both feet and hands => Symmetrical polyneuropathy
x: Myopathy => Proximal symmetrical weakness without nerve territory signs
x: Motor neurone disease => Mixed upper and lower motor neurone signs without sensory loss
x: Polyradiculopathy => Root level weakness, not single peripheral nerves
x: Symmetrical polyneuropathy => Distal and even, not patchy

@u 166 2T
s: A 64 year old man has small, irregular pupils. They constrict when he looks at a near object, but not to a bright light.
? Which condition is classically linked to these pupils?
> Holmes-Adie pupil ; Myasthenia gravis ; *Neurosyphilis ; Opioid use ; Third nerve palsy
= Argyll Robertson pupils accommodate but do not react, from damage near the midbrain. Syphilis and diabetes are causes.
~ One large pupil that reacts slowly and has reduced knee jerks → Holmes-Adie pupil.
c: small, irregular pupils | constrict when he looks at a near object | not to a bright light
m: The light reflex fibres are damaged but the near pathway is spared
g: Light-near dissociation with small irregular pupils is Argyll Robertson
f: one large pupil that constricts slowly and absent knee jerks => Holmes-Adie pupil
x: Holmes-Adie pupil => A large, slowly reacting pupil
x: Myasthenia gravis => Spares the pupils
x: Opioid use => Pinpoint pupils that still react to light
x: Third nerve palsy => A large pupil with ptosis and a down and out eye

@u 166 3T
s: A 42 year old man had neck manipulation by a chiropractor 2 days ago. He now has pain on the left side of his neck and a headache. // There is a small left pupil and mild left ptosis. An hour ago he had brief weakness of his right hand.
? Which is the most likely diagnosis?
> Left-sided cluster headache ; *Left carotid artery dissection ; Migraine with aura ; Left apical lung tumour ; Left third nerve palsy
= A torn carotid wall injures the sympathetic fibres on the artery, giving a partial Horner's syndrome, and can throw clots that cause TIA or stroke.
~ Horner's with shoulder pain and weight loss in a smoker → Pancoast tumour.
c: neck manipulation | pain on the left side of his neck | small left pupil | weakness of his right hand
m: Sympathetic fibres run on the carotid wall, which has split
g: Painful Horner's with a TIA after neck injury is carotid dissection
f: shoulder pain and weight loss in a heavy smoker => Left apical lung tumour
x: Left-sided cluster headache => Brief attacks around the eye with tearing, not a TIA
x: Migraine with aura => Does not cause Horner's syndrome
x: Left apical lung tumour => A Pancoast tumour is slow, with shoulder pain and weight loss
x: Left third nerve palsy => A large pupil, not a small one

@u 166 2D
s: A 56 year old woman has taken hydroxychloroquine for lupus for 3 years at a standard dose. She has no kidney disease and does not take tamoxifen.
? When should regular retinal screening begin?
> Before every change in dose ; Every 5 years starting from now ; Monthly from now ; When her vision changes ; *Yearly after 5 years of treatment
= Hydroxychloroquine can damage the retina. UK guidance is yearly screening after 5 years, or after 1 year if there are risk factors such as kidney disease, tamoxifen or a high dose.
~ eGFR 40 → start yearly screening after 1 year.
c: hydroxychloroquine | 3 years | no kidney disease | does not take tamoxifen
m: The drug builds up in the retinal pigment cells over years
g: Without risk factors, screen yearly once treatment has lasted 5 years
x: Before every change in dose => Not the screening rule
x: Every 5 years starting from now => Too infrequent once screening begins
x: Monthly from now => Far more than needed
x: When her vision changes => Damage is permanent by the time symptoms appear

@u 79 2D
s: A 54 year old man with gout has had a second episode of renal colic. The stone was not seen on a plain X-ray, but CT showed it clearly. His urine pH is 5.0.
? Which treatment is most likely to prevent further stones?
> Bendroflumethiazide ; Low-calcium diet ; Low-oxalate diet ; *Potassium citrate ; Reduce fluid intake
= Uric acid stones form in acid urine and are not seen on plain X-ray. Alkalinise the urine with potassium citrate, drink more and consider allopurinol.
~ Calcium oxalate stones with high urine calcium → a thiazide.
c: gout | not seen on a plain X-ray | urine pH is 5.0
m: Uric acid crystallises in acid urine
g: Radiolucent stones with gout and acid urine are uric acid; alkalinise the urine
f: calcium oxalate stones with high urinary calcium => Bendroflumethiazide
x: Bendroflumethiazide => For calcium stones with high urine calcium
x: Low-calcium diet => Raises oxalate absorption and stone risk
x: Low-oxalate diet => Helps oxalate stones, not uric acid
x: Reduce fluid intake => Concentrates the urine and causes more stones

@u 79 3L
s: A 62 year old woman has recurrent urinary infections with Proteus mirabilis. Her urine pH is 8.0. // CT shows a large branched stone filling the right renal pelvis and calyces.
? Which stone type is most likely?
> Calcium oxalate ; Calcium phosphate ; Cystine ; *Struvite ; Uric acid
= Urease-making bacteria such as Proteus split urea into ammonia, making the urine alkaline so magnesium ammonium phosphate forms staghorn stones.
~ Recurrent stones in a child with a family history and hexagonal crystals → cystine.
c: Proteus mirabilis | Her urine pH is 8.0 | large branched stone
m: Bacterial urease turns urea into ammonia and alkalinises the urine
g: Staghorn stone with a urease-making infection is struvite
f: hexagonal crystals in a young adult with an affected sibling => Cystine
x: Calcium oxalate => The commonest stone, not tied to infection
x: Calcium phosphate => Seen with renal tubular acidosis or hyperparathyroidism
x: Cystine => An inherited cause in younger people
x: Uric acid => Forms in acid urine

@u 79 3T
s: A 38 year old man with Crohn's disease had 60 cm of terminal ileum removed 2 years ago. He has had two calcium oxalate kidney stones.
? Which is the most likely mechanism of his stones?
> Excess calcium absorption from the gut ; *Fat binds calcium so more oxalate is absorbed ; High urine pH from bicarbonate loss ; Infection with urease-making bacteria ; Too much uric acid in the urine
= Without the terminal ileum, bile salts and fat reach the colon. Fat binds calcium, so oxalate stays free and is absorbed in the colon.
~ Gout with acid urine → uric acid stones.
c: Crohn's disease | 60 cm of terminal ileum removed | calcium oxalate
m: Unabsorbed fat soaks up calcium in the gut, freeing oxalate
g: Ileal disease or resection with oxalate stones is enteric hyperoxaluria
x: Excess calcium absorption from the gut => Calcium absorption is reduced, not increased
x: High urine pH from bicarbonate loss => Diarrhoea makes the urine more acid
x: Infection with urease-making bacteria => Causes struvite, not oxalate
x: Too much uric acid in the urine => Causes uric acid stones

@u 86 1L
s: A 68 year old woman has painful, knobbly swellings at the joints nearest her fingertips. She has no morning stiffness lasting more than 30 minutes.
? Which term describes these swellings?
> Bouchard's nodes ; *Heberden's nodes ; Rheumatoid nodules ; Swan neck deformity ; Tophi
= Heberden's nodes are osteophytes at the distal interphalangeal joints in osteoarthritis. Bouchard's nodes are at the proximal joints.
~ Bony swelling at the middle finger joints → Bouchard's nodes.
c: joints nearest her fingertips | no morning stiffness lasting more than 30 minutes
m: Worn cartilage triggers new bone at the joint edges
g: Bony DIP swellings in osteoarthritis are Heberden's nodes
f: bony swellings at the proximal interphalangeal joints => Bouchard's nodes
x: Bouchard's nodes => At the proximal interphalangeal joints
x: Rheumatoid nodules => Soft lumps over pressure areas such as the elbows
x: Swan neck deformity => A rheumatoid finger deformity
x: Tophi => Chalky urate deposits in chronic gout

@u 86 2L
s: A 70 year old man has had worsening right knee pain on walking for 2 years. Morning stiffness lasts 10 minutes. An X-ray is taken.
? Which X-ray finding is most typical of his likely diagnosis?
> Chondrocalcinosis of the menisci ; *Narrowed joint space with osteophytes ; Pencil-in-cup deformity ; Periarticular erosions ; Periarticular osteopenia
= Osteoarthritis shows LOSS: Loss of joint space, Osteophytes, Subchondral sclerosis and Subchondral cysts.
~ Periarticular erosions and osteopenia in the hands → rheumatoid arthritis.
c: worsening right knee pain on walking | Morning stiffness lasts 10 minutes
m: Cartilage wears away and bone remodels at the margins
g: Joint space narrowing with osteophytes is osteoarthritis
f: symmetrical hand swelling with long morning stiffness => Periarticular erosions
x: Chondrocalcinosis of the menisci => Calcium in cartilage from pyrophosphate disease
x: Pencil-in-cup deformity => Psoriatic arthritis
x: Periarticular erosions => Rheumatoid arthritis
x: Periarticular osteopenia => An early rheumatoid sign

@u 144 3L
s: A 19 year old woman has had nosebleeds since childhood, heavy periods and long bleeding after a tooth extraction. Her mother is similar. // There are no telangiectasia.
$ Platelets ; 250 × 10⁹/L ; 150–400
$ PT ; 12 seconds ; 10–14
$ APTT ; 41 seconds ; 25–35
? Which is the most likely diagnosis?
> Haemophilia A ; Hereditary haemorrhagic telangiectasia ; Immune thrombocytopenia ; *Von Willebrand disease ; Warfarin effect
= Von Willebrand disease is the commonest inherited bleeding disorder: mucosal bleeding, heavy periods, usually autosomal dominant, sometimes a long APTT as factor VIII falls.
~ A boy with bleeding into joints and a long APTT → haemophilia A.
c: nosebleeds since childhood | heavy periods | Her mother is similar | APTT 41
m: Low von Willebrand factor stops platelets sticking and lets factor VIII break down
g: Mucosal bleeding in a woman with a dominant family history and normal platelets is von Willebrand disease
f: a boy with bleeding into his knees => Haemophilia A
x: Haemophilia A => X-linked, in males, with joint and muscle bleeds
x: Hereditary haemorrhagic telangiectasia => Telangiectasia on lips and fingers
x: Immune thrombocytopenia => Platelets would be low
x: Warfarin effect => PT would be long, and she takes no warfarin

@u 144 3T
s: A 15 year old boy has had a blocked left nostril for 6 months and three heavy nosebleeds from that side. // There is a smooth red mass at the back of the left nasal cavity.
? Which is the most appropriate next step?
> Biopsy in clinic ; Cautery and discharge ; *Imaging before any biopsy ; Nasal packing and review in a month ; Steroid nasal spray
= Juvenile nasopharyngeal angiofibroma: a vascular tumour in teenage boys. Biopsy can cause torrential bleeding, so image first and refer to ENT.
~ Bleeding from Little's area in a child who picks his nose → antiseptic cream.
c: 15 year old boy | blocked left nostril | heavy nosebleeds | smooth red mass
m: A very vascular tumour grows from the back of the nose in adolescent males
g: Teenage boy, one blocked side and heavy bleeds: image, never biopsy first
f: bleeding from the front of the septum in a child who picks his nose => Cautery and discharge
x: Biopsy in clinic => Can cause life-threatening bleeding
x: Cautery and discharge => Ignores a mass at the back of the nose
x: Nasal packing and review in a month => Delays diagnosis of a tumour
x: Steroid nasal spray => For allergic rhinitis or polyps

@u 24 2L
s: Several people became ill after a takeaway meal of egg fried rice that had been left out and reheated. They started vomiting 2 hours later. Few have diarrhoea and none has a fever.
? Which organism is most likely?
> *Bacillus cereus ; Campylobacter jejuni ; Clostridium perfringens ; Norovirus ; Salmonella enteritidis
= Bacillus cereus spores survive cooking. In rice left warm, they make a toxin that causes vomiting within 1 to 6 hours.
~ Ham sandwiches and cream cakes with vomiting at 2 hours → Staph aureus.
c: egg fried rice | left out and reheated | vomiting 2 hours later
m: Spores survive cooking and make a heat-stable toxin as rice cools slowly
g: Vomiting within hours of reheated rice is Bacillus cereus
f: diarrhoea 12 hours after a large stew kept warm => Clostridium perfringens
x: Campylobacter jejuni => Bloody diarrhoea days after poultry
x: Clostridium perfringens => Watery diarrhoea 8 to 16 hours after meat stews
x: Norovirus => Spreads between people, often with diarrhoea
x: Salmonella enteritidis => Fever and diarrhoea a day or more after eggs or chicken

@u 24 3L
s: A 16 year old boy has had right lower abdominal pain, fever and diarrhoea for 4 days. His family keep pigs. // There is tenderness in the right iliac fossa. Ultrasound shows enlarged mesenteric nodes and a normal appendix.
? Which organism is most likely?
> Campylobacter jejuni ; Clostridioides difficile ; Escherichia coli O157 ; Shigella sonnei ; *Yersinia enterocolitica
= Yersinia infects the terminal ileum and mesenteric nodes, mimicking appendicitis. Pork and pigs are sources.
~ Bloody diarrhoea with low platelets and a rising creatinine in a child → E. coli O157 with HUS.
c: His family keep pigs | right iliac fossa | enlarged mesenteric nodes | normal appendix
m: The bacteria invade the ileal lymphoid tissue and swell the nearby nodes
g: Pseudoappendicitis with mesenteric adenitis and pigs is Yersinia
f: bloody diarrhoea after a petting farm with low platelets => Escherichia coli O157
x: Campylobacter jejuni => Bloody diarrhoea after poultry, not nodes with a normal appendix
x: Clostridioides difficile => After antibiotics
x: Escherichia coli O157 => Bloody diarrhoea and a risk of HUS
x: Shigella sonnei => Bloody dysentery spread between people

@u 125 2L
s: A 64 year old man has lost 9 kg over 3 months and has early fullness. He has developed dark, velvety thickened skin in both armpits. He is thin and does not have diabetes.
? Which investigation is most appropriate?
> Routine dermatology referral ; Fasting insulin ; HbA1c ; Skin biopsy ; *Urgent upper GI endoscopy
= Acanthosis nigricans in a thin older person with weight loss can signal gastric cancer. It is usually linked to insulin resistance in younger people.
~ An overweight young woman with irregular periods → insulin resistance, check HbA1c.
c: lost 9 kg | early fullness | dark, velvety thickened skin | does not have diabetes
m: Tumour growth factors drive the skin to thicken and darken
g: New acanthosis with weight loss and no insulin resistance: look for gastric cancer
f: an overweight 24 year old with irregular periods => HbA1c
x: Routine dermatology referral => Misses the likely cancer
x: Fasting insulin => Insulin resistance fits young overweight people, not this picture
x: HbA1c => He does not have diabetes, and it would not find the cause
x: Skin biopsy => The skin change is clinically clear; the cause is elsewhere

@u 96 2L
s: A 22 year old woman fainted while standing in a hot queue. A friend saw her go pale and limp, then her arms jerked for about 10 seconds. She came round within a minute and was not confused afterwards.
? Which is the most likely diagnosis?
> *Convulsive syncope ; Dissociative seizure ; Focal impaired awareness seizure ; Generalised tonic-clonic seizure ; Hypoglycaemia
= Brief jerks are common in syncope when the brain is short of blood. A clear trigger, pallor and rapid recovery without confusion point to syncope, not epilepsy.
~ A tongue bitten on the side, confusion for 20 minutes and a seizure from sleep → generalised tonic-clonic seizure.
c: standing in a hot queue | pale and limp | about 10 seconds | not confused afterwards
m: A drop in brain blood flow briefly releases jerking movements
g: Triggered faint with brief jerks and quick recovery is convulsive syncope
f: a bitten tongue and 20 minutes of confusion afterwards => Generalised tonic-clonic seizure
x: Dissociative seizure => Long episodes with eyes closed and fluctuating movements
x: Focal impaired awareness seizure => Automatisms with a blank stare, not a triggered faint
x: Generalised tonic-clonic seizure => Longer stiffening and jerking with confusion after
x: Hypoglycaemia => Sweating and confusion that improve with sugar

@u 96 3L
s: A 26 year old woman has episodes of shaking lasting 10 to 20 minutes. Her eyes are tightly closed throughout, her head moves from side to side and the movements stop and start. She cries afterwards and remembers parts of the episodes. Video EEG during an episode is normal.
? Which is the most likely diagnosis?
> Convulsive syncope ; *Dissociative seizure ; Frontal lobe epilepsy ; Generalised tonic-clonic seizure ; Status epilepticus
= Dissociative, or non-epileptic, seizures: eyes closed, side-to-side movements, waxing and waning, long duration and some recall, with a normal video EEG.
~ Brief seizures from sleep with bizarre movements and a frontal EEG focus → frontal lobe epilepsy.
c: 10 to 20 minutes | eyes are tightly closed | stop and start | Video EEG during an episode is normal
m: A functional neurological disorder causes seizure-like events without abnormal brain electricity
g: Long fluctuating episodes with closed eyes and a normal video EEG are dissociative seizures
f: short bizarre attacks from sleep with a frontal EEG focus => Frontal lobe epilepsy
x: Convulsive syncope => Seconds long, with pallor and a clear trigger
x: Frontal lobe epilepsy => Brief, often from sleep, with EEG changes
x: Generalised tonic-clonic seizure => Eyes open and the EEG would be abnormal
x: Status epilepticus => The EEG would show seizure activity

@u 153 2L
s: A 6 week old baby has noisy breathing on breathing in, worse when feeding, crying or lying on his back. He is feeding well and gaining weight. // His colour is good and there is no recession.
? Which is the most appropriate management?
> IV antibiotics ; Nebulised adrenaline ; Oral dexamethasone ; *Reassure and monitor growth ; Urgent tracheostomy
= Laryngomalacia is a floppy larynx that collapses on breathing in. It usually settles by 18 to 24 months. Refer if feeding, growth or breathing are affected.
~ Stridor with poor weight gain and apnoeas → ENT for airway assessment.
c: 6 week old | worse when feeding, crying or lying on his back | gaining weight
m: Soft laryngeal tissue folds in on breathing in
g: Thriving baby with positional inspiratory stridor is laryngomalacia
x: IV antibiotics => There is no infection
x: Nebulised adrenaline => For croup
x: Oral dexamethasone => For croup
x: Urgent tracheostomy => Not needed in a well, growing baby

@u 152 3L
s: A newborn baby goes blue when feeding and pink again when crying. A nasogastric tube cannot be passed through either nostril.
? Which is the most likely diagnosis?
> Bronchiolitis ; *Choanal atresia ; Laryngomalacia ; Oesophageal atresia ; Pierre Robin sequence
= Newborns breathe through the nose. Blocked back of the nose means cyanosis on feeding, relieved by crying through the mouth. It can be part of CHARGE.
~ Frothy saliva and choking on the first feed with the tube coiling in the chest → oesophageal atresia.
c: blue when feeding | pink again when crying | cannot be passed through either nostril
m: Newborns must breathe through the nose; crying opens the mouth
g: Cyanosis relieved by crying with no nasal passage is choanal atresia
f: frothy saliva and the tube coiling in the upper chest => Oesophageal atresia
x: Bronchiolitis => A viral illness in older infants with cough and wheeze
x: Laryngomalacia => Noisy breathing, not blocked nostrils
x: Oesophageal atresia => The tube stops in the oesophagus through the mouth or nose
x: Pierre Robin sequence => Small jaw with the tongue falling back

@u 110 2N
s: A 52 year old man who drinks 25 units a day is admitted for a hip operation. His last drink was at 8 pm last night. The nurses ask when he is most at risk of delirium tremens.
? When are delirium tremens most likely to start?
> 1 to 2 hours after his last drink ; 6 to 12 hours after his last drink ; *48 to 72 hours after his last drink ; 1 week after his last drink ; 3 weeks after his last drink
= Tremor and anxiety start within 6 to 12 hours, seizures peak at 12 to 48 hours, and delirium tremens at 48 to 72 hours. Start a chlordiazepoxide regimen and thiamine.
~ Fit at 24 hours → alcohol withdrawal seizure.
c: 25 units a day | last drink was at 8 pm last night
m: The brain, used to alcohol suppressing it, becomes overexcited when alcohol stops
g: Delirium tremens peaks 48 to 72 hours after the last drink
f: tremor, sweating and anxiety the next morning => 6 to 12 hours after his last drink
x: 1 to 2 hours after his last drink => Too early for withdrawal
x: 6 to 12 hours after his last drink => Tremor, sweating and anxiety start then
x: 1 week after his last drink => Withdrawal is usually past its peak
x: 3 weeks after his last drink => Far beyond the withdrawal window

@u 4 2L
s: A 28 year old woman has hypertension that needed three drugs to control. She does not smoke and has no family history of kidney disease. // BP 168/102 mmHg. There is a bruit in the right upper abdomen. CT angiogram shows a beaded right renal artery.
? Which is the most likely diagnosis?
> Atherosclerotic renal artery stenosis ; Coarctation of the aorta ; *Fibromuscular dysplasia ; Phaeochromocytoma ; Polycystic kidney disease
= Fibromuscular dysplasia narrows renal arteries in young women, giving a string of beads look. Angioplasty often cures the hypertension.
~ An older smoker with vascular disease and a rise in creatinine on an ACE inhibitor → atherosclerotic renal artery stenosis.
c: 28 year old woman | three drugs | bruit in the right upper abdomen | beaded right renal artery
m: Overgrown artery wall muscle forms ridges that narrow the renal artery
g: Young woman with resistant hypertension and a beaded renal artery has FMD
f: a 70 year old smoker with claudication => Atherosclerotic renal artery stenosis
x: Atherosclerotic renal artery stenosis => Older smokers with vascular disease
x: Coarctation of the aorta => Weak femoral pulses and arm to leg BP difference
x: Phaeochromocytoma => Episodes of headache, sweating and palpitations
x: Polycystic kidney disease => Large cystic kidneys and a family history

@u 13 3L
s: A 66 year old man has had three episodes of painful, red, cord-like veins in different places on his arms and legs over 2 months. He has lost 6 kg and has a dull upper abdominal ache going into his back.
? Which is the most appropriate investigation?
> *CT abdomen ; D-dimer ; Leg vein Doppler ; Thrombophilia screen ; Venous blood cultures
= Migratory thrombophlebitis, Trousseau's sign of malignancy, with weight loss and back-boring pain suggests pancreatic cancer.
~ A single tender varicose vein after a knock → superficial thrombophlebitis, compression and NSAIDs.
c: different places on his arms and legs | lost 6 kg | going into his back
m: Tumours release substances that make the blood clot easily
g: Migrating superficial clots with weight loss: look for an occult cancer
f: a single tender varicose vein after a knock => Leg vein Doppler
x: D-dimer => Raised in both clots and cancer; it does not find the cause
x: Leg vein Doppler => Ignores the weight loss and pain
x: Thrombophilia screen => Not the first test with red flags for cancer
x: Venous blood cultures => The veins are not infected

@u 13 3D
s: A 34 year old woman has had a DVT and two miscarriages after 10 weeks. Her APTT is prolonged and does not correct with normal plasma. She has no lupus symptoms.
? Which anticoagulant is most appropriate long term?
> Apixaban ; Low-dose aspirin ; Dabigatran ; Rivaroxaban ; *Warfarin
= Antiphospholipid syndrome: lupus anticoagulant prolongs the APTT in the test tube but causes clots in the body. Warfarin is used; DOACs are less safe here.
~ First provoked DVT after surgery with no antibodies → a DOAC for 3 months.
c: two miscarriages | APTT is prolonged | does not correct with normal plasma
m: Antibodies against phospholipids slow clotting tests but activate clotting in vessels
g: Thrombosis with antiphospholipid antibodies is treated with warfarin, not a DOAC
f: a single DVT after a hip operation with negative antibodies => Apixaban
x: Apixaban => DOACs have more clots than warfarin in antiphospholipid syndrome
x: Low-dose aspirin => Not enough after a venous clot
x: Dabigatran => Same concern as other DOACs here
x: Rivaroxaban => Raised clot rates in trials of high-risk antiphospholipid syndrome

@u 32 2N
s: A 58 year old man with a long history of duodenal ulcers has vomited large amounts of undigested food for a week, often hours after eating. The vomit is not bile-stained. // There is a succussion splash.
$ Sodium ; 134 mmol/L ; 135–146
$ Potassium ; 2.9 mmol/L ; 3.5–5.3
$ Chloride ; 82 mmol/L ; 95–106
$ Bicarbonate ; 38 mmol/L ; 22–30
? Which is the most likely diagnosis?
> Gastric cancer of the fundus ; *Gastric outlet obstruction ; Gastroparesis from diabetes ; Small bowel obstruction ; Zollinger-Ellison syndrome
= Scarring from duodenal ulcers can block the pylorus. Vomiting stomach acid causes a hypochloraemic hypokalaemic metabolic alkalosis.
~ Bile-stained vomiting with distension and colicky pain → small bowel obstruction.
c: long history of duodenal ulcers | not bile-stained | succussion splash | Chloride 82 | Bicarbonate 38
m: Vomiting acid loses chloride and hydrogen ions, and the kidney swaps potassium for sodium
g: Non-bilious vomiting of old food with a splash and low chloride alkalosis is gastric outlet obstruction
f: bile-stained vomiting and distended small bowel loops => Small bowel obstruction
x: Gastric cancer of the fundus => A fundal tumour does not block the outlet
x: Gastroparesis from diabetes => He has no diabetes, and ulcers explain it
x: Small bowel obstruction => Vomit would contain bile
x: Zollinger-Ellison syndrome => Causes ulcers and diarrhoea, not a splash with old food

@u 89 3T
s: A 34 year old woman has had headaches for 3 weeks, worse at home and better at work. Her two children also have headaches and nausea. The boiler has not been serviced for years.
? Which test is most appropriate?
> *Carboxyhaemoglobin level ; CT head with contrast ; Lumbar puncture ; Pulse oximetry ; Serum lead level
= Carbon monoxide: headaches in a household that improve away from home. Pulse oximetry reads falsely normal, so measure carboxyhaemoglobin on a blood gas.
~ One person, worse in the morning with vomiting and papilloedema → CT head for a mass.
c: worse at home and better at work | two children also have headaches | boiler has not been serviced
m: Carbon monoxide binds haemoglobin far more tightly than oxygen
g: Shared headaches at home that improve away suggest carbon monoxide
f: one person with morning vomiting and papilloedema => CT head with contrast
x: CT head with contrast => Does not diagnose poisoning
x: Lumbar puncture => Not indicated without signs of infection or bleeding
x: Pulse oximetry => Reads carboxyhaemoglobin as oxygenated, so looks normal
x: Serum lead level => Lead causes abdominal pain and anaemia, not a household pattern like this
"""

# fixes to existing questions: id -> fields to replace (options use * for the answer; tm rebuilt from the given map lines)
FIX = r"""
@fix h0446
? How often should his lithium level be checked?
> Every 3 months ; *Every 6 months ; Every 12 months ; Monthly ; Weekly
= Levels weekly after a dose change until stable, every 3 months for the first year, then every 6 months if stable. Stay at 3 months for older people, interacting drugs, poor adherence or a last level of 0.8 or more.
~ Last level 0.9 or a new ACE inhibitor → keep checking every 3 months.
c: taken lithium for 2 years | stable for over a year | 0.6 mmol/L
m: Lithium has a narrow range; checks space out once it is stable
g: After the first year, stable lithium is checked every 6 months
f: a level of 0.9 or a new ACE inhibitor => Every 3 months
x: Every 3 months => The rule for the first year or for higher-risk patients, which he is not
x: Every 12 months => Too infrequent for a drug with a narrow range
x: Monthly => More often than needed when stable
x: Weekly => Only after starting or changing the dose

@fix h1469
> Hyperglycaemia ; Hypernatraemia ; Hypertension ; *Tension pneumothorax ; Ventricular tachycardia
= 4 Hs: hypoxia, hypovolaemia, hypo or hyperkalaemia and other metabolic causes, hypothermia or hyperthermia. 4 Ts: thrombosis, tension pneumothorax, tamponade, toxins.
c: car crash | reversible causes
m: The 4 Hs and 4 Ts list the causes of arrest that can be fixed
g: Tension pneumothorax is one of the 4 Ts
x: Hyperglycaemia => Not one of the listed reversible causes of arrest
x: Hypernatraemia => Not one of the listed reversible causes
x: Hypertension => Arrest causes low pressure; hypertension is not on the list
x: Ventricular tachycardia => A rhythm to shock, not a cause in the 4 Hs and 4 Ts

@fix h1458
> 1 to 4 ; *About 1 to 1 ; 4 to 1 ; 10 to 1 ; Red cells without plasma
c: major haemorrhage protocol | tranexamic acid
m: Early plasma replaces clotting factors lost with blood
g: Major haemorrhage: red cells to plasma about 1 to 1
x: 1 to 4 => Too little oxygen carrying with too much volume
x: 4 to 1 => Dilutes clotting factors and worsens trauma coagulopathy
x: 10 to 1 => Severe dilutional coagulopathy
x: Red cells without plasma => No clotting factors at all

@fix h0794
> Amoxicillin and continue mesalazine ; *Check a full blood count urgently ; Double the dose ; Gargle and review in 1 week ; Switch to sulfasalazine
c: mesalazine | sore throat, fever and mouth ulcers
m: Aminosalicylates can rarely cause blood dyscrasias
g: Infection symptoms on mesalazine: check a full blood count urgently
x: Amoxicillin and continue mesalazine => Treats a guess and keeps the possible cause going without checking neutrophils
x: Double the dose => Would worsen any marrow suppression
x: Gargle and review in 1 week => Delays finding neutropenia
x: Switch to sulfasalazine => Also an aminosalicylate with the same risk

@fix h0738
? What is the most she can take in a single day for a short time?
= Up to 12 inhalations a day can be used for a short time. Regular use of more than 8 a day needs urgent review.

@fix h0659
lab LDL cholesterol 2.9 mmol/L (<5.0) => LDL cholesterol 2.9 mmol/L (<3.0)

@fix h1305
= Anion gap is sodium minus the sum of chloride and bicarbonate: 138 minus 128 is 10, which is normal. Normal-gap acidosis with low potassium means bicarbonate lost from the gut or the kidney.

@fix h1504
s: A 24 year old woman was diagnosed with pelvic inflammatory disease 2 weeks ago and treated with antibiotics. She now has sharp pain under the right ribs that is worse on breathing in. Temperature 37.8°C. There is right upper quadrant tenderness. Liver tests are normal. Pregnancy test is negative.
? Which is the most likely diagnosis?
> Acute cholecystitis ; *Fitz-Hugh-Curtis syndrome ; Hepatitis A ; Pulmonary embolism ; Right lower lobe pneumonia
= Fitz-Hugh-Curtis syndrome is inflammation of the liver capsule from chlamydia or gonorrhoea spreading up from the pelvis, giving right upper quadrant pain with normal liver tests.
~ Gallstones on ultrasound with a positive Murphy's sign → acute cholecystitis.
c: pelvic inflammatory disease 2 weeks ago | worse on breathing in | Liver tests are normal
m: Pelvic infection tracks up the paracolic gutter to inflame the liver capsule
g: Right upper quadrant pain after PID with normal liver tests is Fitz-Hugh-Curtis
f: gallstones and a positive Murphy's sign on ultrasound => Acute cholecystitis
x: Acute cholecystitis => Ultrasound would show gallstones and a thick wall
x: Hepatitis A => Liver tests would be very high
x: Pulmonary embolism => Breathless and hypoxic with risk factors
x: Right lower lobe pneumonia => Cough and crackles with consolidation

@fix h1626
s: A 74 year old man had cataract surgery on his right eye 14 months ago. His vision has slowly become misty again over 3 months. The eye is not painful or red. Visual acuity is 6/18 in the right eye. There is a hazy membrane behind the lens implant.
? Which is the most appropriate treatment?
> Intravitreal antibiotics ; Repeat cataract surgery ; Steroid eye drops ; *YAG laser capsulotomy ; New glasses
= Posterior capsule opacification is the commonest late problem after cataract surgery. A YAG laser makes a clear opening in the clouded capsule in a few minutes.
~ A painful red eye with pus 3 days after surgery → endophthalmitis.
c: 14 months ago | slowly become misty | not painful or red | hazy membrane behind the lens implant
m: Leftover lens cells grow across the back of the capsule and cloud it
g: Gradual blur months after surgery with a hazy capsule is posterior capsule opacification
f: a painful red eye with pus 3 days after surgery => Intravitreal antibiotics
x: Intravitreal antibiotics => For endophthalmitis, which is painful and early
x: Repeat cataract surgery => Not needed; a laser opens the capsule
x: Steroid eye drops => For inflammation, which he does not have
x: New glasses => Will not clear a clouded capsule

@fix h0843
labset Urate ; 0.72 mmol/L ; 0.20–0.43

@fix h0533
labset lipase ; 1800 IU/L ; <60
"""
