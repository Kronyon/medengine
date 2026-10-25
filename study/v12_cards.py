#!/usr/bin/env python3
"""medengine v1.2: ⚡ First move vs cure cards, plus one new Why card (nerve injuries).
Rules: every line moves (→), key words bold, no brackets, no em dashes, UK guidance only (NICE, Resus Council UK,
BTS, JBDS, BASHH). Lines start with 🔴 unstable, 🟢 stable, or 1️⃣ 2️⃣ 🎯 steps where that is the decision.
Writes v12_content.json: {"act": [...], "path_add": [...]}"""
import json, pathlib

ACT = []
def act(i, t, u, *l): ACT.append({'id': i, 't': t, 'u': u, 'l': list(l)})

# ---------------- cardiovascular ----------------
act('tachy', 'Fast heart: unstable vs stable', [3],
 '🔴 **Unstable**: shock, syncope, chest pain or heart failure → **synchronised DC cardioversion** under sedation → up to 3 shocks → then **IV amiodarone**.',
 '🟢 **Stable, narrow and regular**: SVT → 1️⃣ **vagal manoeuvres**, Valsalva or carotid sinus massage → 2️⃣ **IV adenosine as a rapid bolus**, 6 → 12 → 18 mg → 🎯 recurrent SVT → **catheter ablation** cures it.',
 '🟢 **Stable AF** → **rate control** with a beta-blocker or diltiazem → onset under 48 hours → rhythm control is an option → stroke risk by **CHA2DS2-VASc**, bleeding risk by **ORBIT** → anticoagulate with a **DOAC**.',
 '🟢 **Stable broad complex**, likely VT → **IV amiodarone** → turns unstable → **cardioversion**.')
act('brady', 'Slow heart: adverse signs decide', [3, 0],
 '🔴 **Adverse signs**: shock, syncope, heart failure, ischaemia → 1️⃣ **IV atropine 500 micrograms**, repeated up to 3 mg → 2️⃣ still slow → **transcutaneous pacing** or other drugs → 🎯 permanent pacemaker.',
 '🟢 **No adverse signs and no asystole risk** → **monitor and correct reversible causes**: beta-blockers, digoxin, low potassium, hypothyroidism.',
 'Asystole risk even when stable → Mobitz II, complete heart block with a broad QRS, pauses over 3 seconds → **arrange pacing**. Complete heart block after an **inferior MI** → often answers to **atropine** and recovers.')
act('acs', 'Chest pain: the community call, STEMI vs NSTEMI', [0, 2],
 '**Community**, pain in the last 12 hours with ECG changes or still ongoing → **aspirin 300 mg + emergency ambulance admission** → pain 12 to 72 hours ago and settled → **same-day assessment**.',
 '**STEMI** → aspirin + a second antiplatelet → **primary PCI** if within 12 hours and deliverable within **120 minutes** of when fibrinolysis could be given → otherwise **fibrinolysis** straight away → PCI uses a **drug-eluting stent**.',
 '**NSTEMI or unstable angina** → aspirin + an antithrombin such as fondaparinux → **GRACE** score → intermediate or high risk → **angiography within 72 hours**.',
 '**Oxygen only if sats are under 94%** → pain → GTN → still in pain → **IV morphine** with an antiemetic.')
act('hf_act', 'Heart failure: acute fluid vs the chronic drug ladder', [6],
 '🔴 **Acute pulmonary oedema** → **sit upright** → oxygen if hypoxic → **IV furosemide** → still struggling → CPAP → opioids not routinely.',
 '🟢 **Chronic reduced ejection fraction** → 1️⃣ **ACE inhibitor + beta-blocker** → 2️⃣ still symptomatic → add an **MRA**, spironolactone or **eplerenone**, and an **SGLT2 inhibitor** → specialist options: sacubitril-valsartan, ivabradine, digoxin.',
 'Every patient → **loop diuretic** for congestion → **annual flu vaccine** and a one-off pneumococcal vaccine → cardiac rehabilitation.')
act('htn_act', 'Hypertension: the NICE ladder', [4],
 '1️⃣ Under 55 and not Black African or Caribbean, or **diabetes at any age** → **ACE inhibitor or ARB** → 55 or over, or Black African or Caribbean without diabetes → **calcium channel blocker**.',
 '2️⃣ Add the other, or a **thiazide-like diuretic** such as **indapamide** → 3️⃣ **A + C + D** together.',
 '4️⃣ Check adherence → **potassium 4.5 or less** → **spironolactone** → **above 4.5** → alpha-blocker or beta-blocker → specialist.',
 '🔴 **180/120 or more** with retinal haemorrhage, papilloedema or life-threatening symptoms → **same-day specialist referral**.')
act('pe_act', 'Suspected PE: Wells picks the first test', [13],
 '🔴 **Massive PE with hypotension** → **thrombolysis with alteplase**.',
 '🟢 **Wells 4 or less** → 1️⃣ **D-dimer** → positive → 2️⃣ **CTPA**. **Wells over 4** → **CTPA** straight away → interim anticoagulation if it is delayed.',
 'Confirmed → **DOAC** such as apixaban or rivaroxaban → **3 months** if provoked, longer if unprovoked → CTPA unsuitable, as in severe renal impairment → **V/Q scan**.')
act('dvt_act', 'Suspected DVT: scan, then decide', [13],
 '1️⃣ **Wells 2 or more** → **proximal leg ultrasound within 4 hours** → delayed → interim anticoagulation. **Wells under 2** → **D-dimer** first.',
 'Ultrasound negative but **D-dimer positive** → **stop anticoagulation** → **repeat the scan in 6 to 8 days**.',
 'Confirmed → **DOAC**. A hot, red, swollen calf → **scan for DVT before calling it cellulitis**.')
act('as_act', 'Aortic stenosis: symptoms decide', [7],
 '🟢 **No symptoms**, even if severe → **regular cardiology review** with echo → replace only if the ventricle starts failing.',
 '🔴 **Symptoms**: angina, syncope, breathlessness → **valve replacement** → **TAVI** for older or higher-risk patients → surgical replacement for younger, fitter patients.')
act('aaa_act', 'Abdominal aortic aneurysm: size sets the clock', [44, 59],
 'Screening → **men at 65** → 3 to 4.4 cm → **yearly** scan → 4.5 to 5.4 cm → **3-monthly** scan.',
 '**5.5 cm or more**, growing over 1 cm a year, or symptomatic → **refer within 2 weeks** for repair.',
 '🔴 **Rupture**: low BP, pulsatile mass, back pain → **straight to theatre** → permissive hypotension on the way.')
act('limb_act', 'Leg arteries and veins: test first', [60, 62, 63, 127],
 '🔴 **Acute limb ischaemia**: pale, pulseless, painful, cold, numb, weak → **IV heparin** → **urgent vascular** review → embolectomy, thrombolysis or bypass → look for **AF** as the source.',
 '🟢 **Claudication** → **ABPI** under 0.9 → **supervised exercise**, statin, **clopidogrel**, stop smoking → critical ischaemia or failure → **angioplasty or bypass**.',
 '**Leg ulcer** → 1️⃣ **ABPI first** → 0.8 or above and no arterial disease → 🎯 **compression bandaging** for a venous ulcer.')

# ---------------- respiratory ----------------
act('asthma_act', 'Acute asthma: grade it, then climb', [15],
 'Grade it → **moderate**: PEF 50 to 75% → **severe**: PEF 33 to 50%, RR 25 or more, HR 110 or more, cannot finish sentences → **life-threatening**: PEF under 33%, **sats under 92%**, silent chest, exhaustion, confusion, a **normal CO2** → **near-fatal**: **raised CO2** or needing ventilation.',
 '1️⃣ **Oxygen** to 94 to 98% → **salbutamol nebs**, back to back if severe → **prednisolone** 40 to 50 mg → 2️⃣ severe or not responding → add **ipratropium** → 3️⃣ **IV magnesium**.',
 '🔴 **Life-threatening or near-fatal** → **senior help and call ICU** early → IV hydrocortisone if tablets are impossible.')
act('copd_act', 'COPD: oxygen target and the exacerbation ladder', [16, 12],
 '🔴 **Critically ill** → start **15 L via a non-rebreathe mask** → titrate down → known CO2 retainer, once stable → **88 to 92%** via a **Venturi** mask.',
 '**Exacerbation** → nebulised **salbutamol and ipratropium** → **prednisolone 30 mg for 5 days** → **antibiotics** if sputum is purulent → still acidotic, pH under 7.35 with CO2 over 6.5 → **NIV**.',
 '**Stable** → LABA + LAMA → asthmatic features → add an ICS → still exacerbating as a non-smoker → consider **azithromycin**; once a LAMA such as tiotropium starts → **stop ipratropium**.')
act('ptx_act', 'Pneumothorax: tension vs the rest', [11],
 '🔴 **Tension**: deviated trachea, hypotension → **needle decompression immediately, before any X-ray** → then a **chest drain**.',
 '🟢 **Primary** with few symptoms → **conservative** with follow-up → symptomatic → **needle aspiration** or an ambulatory device → **secondary**, with lung disease → admit, usually a **drain**.',
 'Persistent air leak or recurrence → **VATS pleurodesis** → no flying until it has resolved.')
act('pneu_act', 'Pneumonia: CURB-65 sets the place, clues name the bug', [19],
 '**CURB-65**: confusion, urea over 7, RR 30 or more, low BP, age 65 or more → 0 to 1 → **home** with amoxicillin → 2 → consider **hospital** → 3 or more → **urgent admission**, think ICU.',
 'Clues → **Mycoplasma**: young, dry cough, target rash, haemolysis → **Legionella**: air conditioning, **low sodium**, deranged LFTs → **Klebsiella**: alcohol, upper lobe, redcurrant jelly sputum → **Staph aureus**: after influenza, cavities.',
 'Persistent symptoms or a high cancer risk → **repeat chest X-ray at 6 weeks**.')

# ---------------- GI and surgery ----------------
act('sepsis_act', 'Sepsis: the first hour', [46],
 '1️⃣ Suspect it → **blood cultures, then antibiotics**, without delaying them → IV antibiotics within the hour → lactate → fluids → urine output.',
 'Low BP or lactate 4 or more → **fluid boluses** → still low → **noradrenaline**, the first-line vasopressor → ICU.',
 '**Neutropenic sepsis** → IV **piperacillin-tazobactam** within 1 hour → do not wait for the count.')
act('ugib_act', 'Upper GI bleed: resuscitate, score, scope', [32],
 '1️⃣ **ABCDE**, two large-bore cannulas → transfuse if needed → **Glasgow-Blatchford** score → 2️⃣ unstable → **endoscopy straight after resuscitation** → stable → **endoscopy within 24 hours**.',
 '**Variceal** → **terlipressin + antibiotics** before endoscopy → **band ligation** → still bleeding → TIPS.',
 '**Peptic ulcer** → endoscopic therapy → **PPI after endoscopy** → test and treat H. pylori.')
act('perf_act', 'Suspected perforation: picture first, then theatre', [45, 32],
 '1️⃣ **Erect chest X-ray** → free air under the diaphragm → negative but still suspected → **CT** → resuscitate, antibiotics → 🎯 **laparotomy** or laparoscopic repair.',
 'Vomiting then chest pain and surgical emphysema → **Boerhaave\'s** → CT with contrast → surgery.')
act('uc_act', 'UC flare: mild vs acute severe', [25],
 '🟢 **Mild to moderate**, systemically well → 1️⃣ **rectal mesalazine** → 2️⃣ add **oral mesalazine** → 3️⃣ **oral prednisolone**.',
 '🔴 **Acute severe**: 6 or more bloody stools a day plus fever, tachycardia, anaemia or high ESR → **urgent admission** → **IV hydrocortisone** → no response by day 3 → **ciclosporin or infliximab**, or surgery.',
 'Refractory or toxic megacolon → 🎯 **colectomy** → elective cure → **panproctocolectomy** with an end ileostomy or a pouch.')
act('biliary_act', 'Gallstones: where the stone is decides the move', [41, 42, 43],
 '**Biliary colic** → analgesia → **elective laparoscopic cholecystectomy**. **Acute cholecystitis** → IV antibiotics → **cholecystectomy within 1 week**.',
 '**Cholangitis** → resuscitate, antibiotics → **ERCP to drain the duct** → then cholecystectomy.',
 '**Acute pancreatitis** → fluids, analgesia, **early oral feeding**, no routine nil by mouth → ERCP only with cholangitis or a blocked duct → gallstone cause → **cholecystectomy in the same admission**.')
act('coeliac_act', 'Coeliac: bloods on gluten, then biopsy', [28, 27],
 '1️⃣ Eating gluten for **at least 6 weeks** → **IgA tTG plus total IgA** → IgA deficient → an IgG-based test.',
 '2️⃣ Positive → **duodenal biopsy** confirms it → 🎯 **lifelong gluten-free diet** → check bones, iron and folate.')
act('dyspepsia_act', 'Reflux and dyspepsia: treat first, scope for red flags', [31, 30, 32],
 '1️⃣ No red flags → lifestyle + **full-dose PPI for 4 weeks**, or **test and treat H. pylori**.',
 '🔴 **Dysphagia**, or **55 or over** with weight loss and upper abdominal pain or reflux → **2-week-wait OGD**.',
 "**Barrett's** → **high-dose PPI + endoscopic surveillance** → dysplasia → endoscopic therapy.")
act('fissure_act', 'Anal fissure: acute vs chronic', [36, 35],
 '🟢 **Acute, under 6 weeks** → **high-fibre diet, fluids, bulk-forming laxatives**, analgesia.',
 '**Chronic, over 6 weeks** → **topical GTN** for 6 to 8 weeks → still failing → **botulinum toxin or lateral sphincterotomy**.')
act('divert_act', 'Diverticulitis: home vs hospital', [37],
 '🟢 **Uncomplicated** and coping at home → analgesia → **oral antibiotics** if systemically unwell or high risk → return if the pain worsens.',
 '🔴 Uncontrolled pain, **abscess, perforation, bleeding**, cannot keep fluids down → **admit** → **CT abdomen and pelvis** → IV antibiotics → drainage, or a **Hartmann\'s** for perforation.',
 'Prevention → **high-fibre diet**: fruit, vegetables, wholegrains.')
act('hernia_act', 'Hernias: routine vs urgent vs emergency', [58],
 '🟢 **Inguinal**, reducible → **routine repair** → minimal symptoms → watchful waiting is reasonable.',
 '**Femoral** → **urgent repair**, because the narrow neck strangulates.',
 '🔴 **Irreducible and painful** → **incarcerated** → loses its blood supply → **strangulated**: tender, red, unwell → **emergency surgery** → open repair if bowel may need resecting.',
 'Deep ring test → pressure over the deep ring **holds back** an **indirect** hernia → a **direct** hernia still bulges through.')
act('colon_act', 'Bowel cancer surgery: the site picks the operation', [33],
 '**Caecum or ascending colon** → **right hemicolectomy** → transverse → extended right hemicolectomy.',
 '**Descending colon** → **left hemicolectomy** → sigmoid → sigmoid colectomy.',
 '**Upper and mid rectum** → **anterior resection** → **low rectum near the anal verge** → **abdominoperineal resection** with a permanent colostomy.',
 '🔴 **Emergency** left-sided obstruction or perforation → **Hartmann\'s** with an end colostomy. Symptoms or iron deficiency → **FIT first** → positive → 2-week-wait colonoscopy.')
act('obstr_act', 'Bowel obstruction: drip and suck vs theatre', [48],
 '🟢 **Adhesions, no strangulation** → **drip and suck**: NG tube, IV fluids, nil by mouth, correct potassium → **CT** to find the cause.',
 '🔴 **Strangulation**: constant pain, peritonism, fever, raised lactate, or a closed loop → **emergency surgery**.',
 '**Sigmoid volvulus** → **flexible sigmoidoscopy** to decompress → recurrent → sigmoid colectomy.')
act('breast_act', 'Breast: who gets the 2-week wait, and which hormone drug', [57, 52, 53, 56, 55],
 '**2-week wait** → **30 or over** with an unexplained lump → **50 or over** with discharge, retraction or change in one nipple → skin changes that suggest cancer → nipple eczema that will not settle.',
 '**Under 30** with a lump → **non-urgent referral**.',
 'Treatment → **wide local excision** → **whole breast radiotherapy** → **ER positive**: premenopausal → **tamoxifen**, postmenopausal → **aromatase inhibitor** such as anastrozole → **HER2 positive** → trastuzumab.')

# ---------------- endocrine, renal, urology ----------------
act('dka_act', 'DKA vs HHS: fluids first', [68, 69, 67],
 '**DKA** → 1️⃣ **1 L 0.9% saline over 1 hour**, a faster bolus if systolic BP is under 90 → 2️⃣ **fixed-rate IV insulin 0.1 units/kg/hour** → keep the long-acting insulin → **potassium** in the fluids after the first litre, guided by levels → glucose under 14 → add **10% glucose**.',
 '**HHS** → **fluids alone first**, more slowly → insulin only if glucose stops falling or ketones are significant → **VTE prophylaxis**.',
 'Any confused or drowsy diabetic → **check capillary glucose first**.')
act('hypo_act', 'Hypoglycaemia: conscious vs not', [70, 67],
 '🟢 **Alert and swallowing** → **15 to 20 g fast-acting glucose** → recheck in 15 minutes → then a long-acting carbohydrate.',
 '🔴 **Drowsy or unconscious** → **IV 10% glucose**, or **IM glucagon** without IV access → glucagon fails after alcohol or starvation because the liver has no glycogen left.',
 'Driving on insulin → **tell the DVLA** → keep hypo awareness → check glucose before driving and at least every 2 hours.')
act('thyroid_act', 'Thyroid: block the symptoms, then the source', [72, 73],
 '1️⃣ Symptomatic thyrotoxicosis → **propranolol** → **thyroiditis** → propranolol alone, because nothing is being overmade.',
 '**Graves** → **carbimazole or radioactive iodine** → not in pregnancy → nodules or relapse → surgery.',
 '🔴 **Thyroid storm**: fever, fast AF, confusion → propranolol, propylthiouracil, steroids → ICU. 🔴 **Myxoedema coma**: cold, slow, confused → **IV levothyroxine + IV hydrocortisone**.')
act('adrenal_act', 'Adrenal crisis: hydrocortisone now', [51, 46],
 '🔴 Collapse, low BP, low sodium, high potassium in someone on steroids or with Addison\'s → **IV hydrocortisone 100 mg** immediately → **IV fluids** → do not wait for results.',
 'Prevention → **sick day rules**: double the steroid dose with fever → emergency injection kit → steroid card.',
 'Suspected Conn\'s → **aldosterone to renin ratio** → suspected Addison\'s → **short Synacthen test**.')
act('hyperk_act', 'Hyperkalaemia: protect, shift, remove', [51],
 '1️⃣ **ECG changes**, or potassium 6.5 or more → **IV calcium gluconate** protects the heart → 2️⃣ **insulin with glucose** and **salbutamol nebs** shift potassium into cells → 3️⃣ remove it → stop the causes, binders, dialysis.',
 'Causes → **AKI**, ACE inhibitors, spironolactone, NSAIDs, trimethoprim → a **haemolysed sample** is a false alarm.')
act('aki_act', 'AKI: stop, fluid, scan', [51, 85],
 '1️⃣ **Stop nephrotoxic drugs**: NSAIDs, ACE inhibitors, metformin, gentamicin → **fluids** if dry → watch urine output and creatinine.',
 'Suspected obstruction → **renal ultrasound within 24 hours** → bilateral hydronephrosis → **nephrostomy** → bladder outlet block → catheter → then watch for **post-obstructive diuresis**.',
 'Contrast in a high-risk patient → **IV 0.9% saline before and after**, not acetylcysteine. 🔴 Refractory high potassium, acidosis, fluid overload → **dialysis**.')
act('stones_act', 'Renal colic: pain, picture, size', [79],
 '1️⃣ **NSAID first**, such as diclofenac by any route → NSAIDs unsuitable → **IV paracetamol** → opioids last → 2️⃣ **non-contrast CT KUB**.',
 '🟢 Under 5 mm → **watchful waiting** → ureteric stone under 10 mm → **alpha-blocker** to help it pass → larger or stuck → **shockwave lithotripsy or ureteroscopy** → renal stone over 20 mm → **PCNL**.',
 '🔴 **Obstructed and infected kidney** → **urgent decompression** with a nephrostomy or stent, plus antibiotics.')
act('uti_act', 'UTI: who gets what', [80, 85],
 '**Non-pregnant woman** → **nitrofurantoin 3 days** if eGFR is 45 or more → **man** → **7 days** plus culture → **pregnant** → culture + 7 days.',
 '**Catheter with no symptoms** → bacteria are expected → **no treatment**.',
 '**Pyelonephritis** → cefalexin or co-amoxiclav, a longer course → septic → admit.')
act('scrotal_act', 'Acute scrotum and urology cancers: who goes now', [83, 82, 77, 78, 84],
 '🔴 **Suspected torsion** → **urgent exploration**, no scan delay → viable → **bilateral orchidopexy** → dead testis → orchidectomy.',
 '**Epididymo-orchitis** → STI risk → **ceftriaxone IM once + doxycycline** for 10 to 14 days → enteric cause in older men → a **quinolone** such as ofloxacin.',
 '**2-week wait** → **45 or over** with unexplained visible haematuria → **60 or over** with non-visible haematuria plus dysuria or a raised white count. Testicular lump → **ultrasound** first.')

# ---------------- neuro, ID, eye, ENT, psych, tox, haem, palliative ----------------
act('se_act', 'Status epilepticus: the 5-minute clock', [96],
 '1️⃣ **5 minutes** of seizure → **benzodiazepine**: IV lorazepam, or buccal midazolam outside hospital → 2️⃣ still seizing 5 to 10 minutes later → **repeat once**.',
 '3️⃣ Still seizing → IV **levetiracetam, phenytoin or valproate** → 🎯 refractory → **anaesthesia and intubation** in ICU.',
 'Check **glucose** early → alcohol or malnourished → **IV thiamine**.')
act('sah_act', 'Thunderclap headache: CT, then LP', [91, 89],
 '1️⃣ **Non-contrast CT head** → done within 6 hours of onset and normal → SAH effectively excluded.',
 '2️⃣ Normal CT after 6 hours → **LP at least 12 hours after onset** → **xanthochromia**.',
 'Confirmed → **CT angiography** → **nimodipine** against vasospasm → coiling or clipping.')
act('mening_act', 'Meningitis: give it, then confirm', [93],
 '🔴 **Community** with a **non-blanching rash** → **IM or IV benzylpenicillin** → do not delay transfer.',
 '**Hospital** → cultures, **meningococcal PCR** → **IV ceftriaxone** → **add amoxicillin if over 60 or immunocompromised**, for Listeria → **dexamethasone** for suspected bacterial meningitis → LP if safe.',
 '**Close contacts** → **single dose of oral ciprofloxacin** → tell public health. Viral → **supportive care only**.')
act('cdiff_act', 'C. difficile and food poisoning: the ladder and the clock', [24],
 '1️⃣ **First episode** → stop the culprit antibiotic → **oral vancomycin** → 2️⃣ no response or **recurrence within 12 weeks** → **oral fidaxomicin**.',
 '🔴 **Life-threatening**: low BP, ileus, toxic megacolon → **oral vancomycin + IV metronidazole** → surgical review.',
 'Food poisoning by timing → vomiting **1 to 6 hours** after food → **Staph aureus** or **B. cereus** → weeks of greasy, bloated diarrhoea → **Giardia** → bloody diarrhoea then low platelets and AKI → **E. coli O157**.')
act('tb_act', 'Tuberculosis: which test, when', [20],
 'Suspected active TB → 1️⃣ **chest X-ray** → 2️⃣ **sputum** for smear, culture and NAAT → culture is the gold standard.',
 '**Latent TB screening**, as before anti-TNF → **IGRA or Mantoux** → plus a chest X-ray.',
 'Every TB patient → **HIV test** → RIPE: rifampicin, isoniazid, pyrazinamide, ethambutol → **isoniazid** causes neuropathy → give **pyridoxine**.')
act('skin_act', 'Skin: treat, cut or refer', [131, 132, 122, 123, 124],
 '**Cellulitis** → **oral flucloxacillin** → penicillin allergy → **clarithromycin** → allergic and pregnant → **erythromycin**.',
 '🔴 **Necrotising fasciitis** → **urgent surgical debridement** + IV antibiotics.',
 'Suspected **melanoma or SCC** → **2-week wait** → suspected BCC → routine referral → **excision with histology**.')
act('eye_act', 'Eye emergencies: who goes today', [160, 162, 165, 163, 161],
 '🔴 **Acute angle closure** → same-day eye unit → pilocarpine, timolol and IV **acetazolamide** → 🎯 **laser peripheral iridotomy** to both eyes.',
 '🔴 **Central retinal artery occlusion**: sudden painless loss, cherry-red spot → **immediate ophthalmology** → ESR for **GCA**. Vein occlusion → haemorrhages everywhere.',
 '**Wet AMD** → **urgent referral** → intravitreal **anti-VEGF** such as bevacizumab. **Retinal detachment** → same-day surgery. **Orbital cellulitis** → admit, IV antibiotics, CT.')
act('ent_act', 'ENT: treat vs refer', [151, 148, 144, 150],
 '**Sore throat** → **FeverPAIN** 0 to 1 → no antibiotics → 2 to 3 → delayed prescription → 4 or more → **phenoxymethylpenicillin**, or **clarithromycin** if allergic.',
 '**Otitis externa** → **topical drops** such as ciprofloxacin → a diabetic with severe pain → **malignant otitis externa** → urgent ENT.',
 'Chronic nasal symptoms → **intranasal steroid** first. Persistent unexplained neck lump or hoarseness → **2-week wait**.')
act('psych_act', 'Psychiatric drug emergencies: stop, cool, reverse', [101, 112, 103, 111],
 '**Acute dystonia** → **procyclidine** → **NMS** → stop the antipsychotic, cool, fluids → dantrolene or bromocriptine.',
 '**Serotonin syndrome** → stop serotonergic drugs → benzodiazepines → **cyproheptadine**. **Lithium toxicity** → stop it → **IV fluids** → dialysis if severe.',
 'Raised prolactin on an antipsychotic → switch to **aripiprazole**. Depression with poor sleep and appetite → **mirtazapine** is a sensible first choice.')
act('tox_act', 'Antidotes: the poison picks the key', [111],
 '**Paracetamol** → **acetylcysteine** → staggered or unclear timing → start straight away. **Opioids** → **naloxone**.',
 '**Beta-blocker** bradycardia → **atropine**, then **glucagon**. **Tricyclics** with a wide QRS → **IV sodium bicarbonate**.',
 '**Iron** → **desferrioxamine**. **Ethylene glycol or methanol** → **fomepizole**. **Organophosphates** → **atropine**. **Digoxin** → antibody fragments. **Lithium** → **IV saline**, dialysis if severe.')
act('anaemia_act', 'Anaemia: test before you treat', [10],
 'Microcytic → **ferritin** → low → oral iron → **find the cause** → men, and women after the menopause → **FIT and lower GI referral**.',
 '**CKD anaemia** → 1️⃣ **iron studies** and correct the iron → 2️⃣ only then **erythropoiesis-stimulating agents**.',
 '**B12 and folate both low** → 1️⃣ **IM B12 first** → 2️⃣ then **folic acid**. On **methotrexate** → weekly **folic acid**, never B12. Warm autoimmune haemolysis → **steroids**, rituximab if refractory.')
act('opioid_act', 'Opioid maths: divide and switch', [50, 88],
 'Oral **codeine or tramadol** → **divide by 10** → the oral morphine dose.',
 'Oral morphine → **subcutaneous morphine**: **divide by 2** → subcutaneous diamorphine: divide by 3.',
 '**Breakthrough** dose → **one sixth** of the 24-hour total. **Severe CKD** → avoid morphine and codeine → **buprenorphine or fentanyl**.')


# ---------------- v1.2.1: every remaining ILO condition ----------------
act('dissect_act', 'Aortic dissection: type A vs type B', [1, 61],
 '1️⃣ Suspected and stable → **CT angiography** → unstable → bedside echo → **never thrombolyse** a possible dissection.',
 '🔴 **Type A**, involving the ascending aorta → **emergency surgery** → control BP and pain on the way.',
 '🟢 **Type B**, descending only → **IV labetalol** to bring BP and heart rate down → rupture, malperfusion or expansion → **endovascular repair**.')
act('lipid_act', 'Lipids: who gets which statin', [5],
 'Primary prevention → **QRISK3 10% or more** → lifestyle + **atorvastatin 20 mg** → CKD or type 1 diabetes → also offered.',
 'Established cardiovascular disease → **atorvastatin 80 mg** → recheck at 3 months → aim for a **40% or more fall in non-HDL** → not reached → adherence, then a higher dose or ezetimibe.',
 'LFTs before, at 3 and at 12 months → muscle pain → **CK** → suspected familial hypercholesterolaemia → **specialist and family testing**.')
act('ie_act', 'Infective endocarditis: cultures before antibiotics', [8],
 '1️⃣ Fever plus a murmur, new emboli or a valve history → **3 sets of blood cultures** from separate sites **before antibiotics** → **echo**, transthoracic then transoesophageal → **Duke criteria**.',
 '2️⃣ Empirical IV antibiotics by local guidance → adjusted to the organism → **weeks** of IV treatment.',
 '🔴 **Heart failure, abscess, uncontrolled infection or large vegetations with emboli** → **cardiac surgery**.')
act('effusion_act', 'Pleural effusion: tap or treat the cause', [9],
 '1️⃣ **Chest X-ray** → bilateral with obvious heart failure → **treat the failure**, no tap unless it behaves oddly.',
 '2️⃣ Unilateral or unexplained → **ultrasound-guided aspiration**: protein, LDH, pH, glucose, cytology, culture → **Light\'s criteria** sorts transudate from exudate.',
 '🔴 **pH under 7.2**, pus or organisms → **chest drain** for empyema → malignant and recurrent → **pleurodesis or an indwelling catheter**.')
act('chestinf_act', 'Bronchitis vs Covid vs bronchiectasis: who needs what', [18, 14, 17],
 '**Acute bronchitis** → self-care, no antibiotics for most → frail, comorbid or systemically unwell → antibiotics → **CRP** helps: under 20 → none, 20 to 100 → delayed, over 100 → offer.',
 '**Covid-19** → low oxygen → oxygen to target → needs oxygen → **dexamethasone** → high-risk patients early on → antivirals.',
 '**Bronchiectasis** → daily **airway clearance physiotherapy** → sputum culture each exacerbation → **14 days of antibiotics** → frequent exacerbations → specialist long-term macrolide.')
act('lungca_act', 'Lung cancer and fibrotic lung: refer, image, treat', [21, 22, 23],
 '**Urgent chest X-ray** → 40 or over with two unexplained symptoms such as cough, breathlessness, weight loss or chest pain, or one if a smoker → **haemoptysis at 40 or over** or a suspicious X-ray → **2-week wait**.',
 '**Non-small cell, early** → **surgery**, usually lobectomy → **small cell** → chemotherapy → **SVC obstruction** → steroids and a stent → **hypercalcaemia** → IV fluids then bisphosphonate.',
 'Fibrosis → **HRCT** → IPF → antifibrotics, pirfenidone or nintedanib → **hypersensitivity pneumonitis** → remove the exposure, steroids → asbestos disease → industrial injuries compensation.')
act('nutrition_act', 'Malnutrition and refeeding: screen, feed slowly, replace', [26],
 '1️⃣ **MUST** screen everyone admitted → score 2 or more → **dietitian** → oral first → unsafe swallow → **NG feeding** → gut not working → parenteral nutrition.',
 '🔴 **High refeeding risk**: very low BMI, little intake for days, low potassium, phosphate or magnesium → **start feeding slowly** → **thiamine and B vitamins before feeding** → check and replace phosphate, potassium and magnesium daily.')
act('bowel_act', 'IBS and constipation: exclude, then step up', [29, 39],
 '**IBS** → exclude red flags → FBC, CRP, coeliac serology, **calprotectin** → regular meals, adjust fibre → pain → **antispasmodic** → diarrhoea → **loperamide** → constipation → laxative, not lactulose → still bad → low-dose tricyclic → low FODMAP with a dietitian.',
 '**Constipation** → red flags → 2-week wait → 1️⃣ **bulk-forming**, ispaghula → 2️⃣ **osmotic**, macrogol → 3️⃣ **stimulant**, senna → **opioid-induced** → osmotic + stimulant, avoid bulk-forming → **impaction** → high-dose macrogol or enemas.')
act('perianal_act', 'Perianal abscess and fistula: drain it, then map it', [34],
 '**Perianal abscess** → **incision and drainage**, antibiotics alone are not enough.',
 '**Fistula** → **MRI pelvis** maps the tract → seton or fistulotomy → recurrent or complex → **think Crohn\'s** → gastroenterology.')
act('lgib_act', 'Lower GI bleed: unstable vs stable', [38],
 '🔴 **Unstable**, shock index over 1 → resuscitate → **CT angiography** → bleeding point found → **embolisation** → upper GI source possible → OGD.',
 '🟢 **Stable** → **Oakland score** → 8 or less → discharge for outpatient tests → over 8 → admit for colonoscopy → most diverticular and angiodysplasia bleeds **stop by themselves**.')
act('appendix_act', 'Appendicitis: confirm, then remove', [40],
 '1️⃣ Bloods, **pregnancy test**, urinalysis → young women and children → **ultrasound** → adults with doubt → **CT**.',
 '2️⃣ **Laparoscopic appendicectomy** + antibiotics → **appendix mass** → antibiotics, drain any abscess → later interval surgery → 🔴 **perforation** → urgent surgery.')
act('pid_act', 'PID: treat on suspicion', [47],
 '1️⃣ **Pregnancy test** and **NAAT swabs** for chlamydia and gonorrhoea → **start treatment straight away**, do not wait for results.',
 '2️⃣ **IM ceftriaxone once + oral doxycycline and metronidazole for 14 days** → coil in situ → can stay unless no better in 72 hours → **partner notification**.',
 '🔴 Pregnant, very unwell, **tubo-ovarian abscess** or no improvement → **admit** for IV antibiotics → ectopic must be excluded.')
act('acuteabdo_act', 'Abdominal pain: rule out the killers first', [49],
 '1️⃣ **ABCDE** → **pregnancy test** in every woman who could be pregnant → bloods with **amylase or lipase, lactate, group and save** → ECG for inferior MI.',
 '🔴 The killers → **ruptured AAA**, **ruptured ectopic**, **perforation**, **mesenteric ischaemia**, DKA → straight to the right pathway: theatre, CT angiography, erect chest X-ray, glucose and ketones.',
 '**Ectopic** → stable, small, low hCG → methotrexate or watch → **ruptured or unstable** → **laparoscopic salpingectomy**.')
act('mastitis_act', 'Mastitis and breast abscess: keep feeding, then treat', [54],
 '🟢 **Lactational mastitis** → **keep breastfeeding or expressing**, analgesia, warm compresses → not settling in 12 to 24 hours, or infected nipple → **flucloxacillin**, or erythromycin if allergic.',
 '**Abscess**, a fluctuant tender lump → **ultrasound** → **needle aspiration** or incision and drainage → non-lactational in a smoker → periductal mastitis → antibiotics and breast referral.')
act('veins_act', "Varicose veins, lymphoedema and Raynaud's: when to refer", [64, 65, 66],
 '**Varicose veins** → refer if symptomatic, skin changes, ulcer, bleeding or thrombophlebitis → **duplex** → **endothermal ablation** first → then sclerotherapy or surgery → **bleeding varicosity** → elevate, press, urgent vascular.',
 '**Lymphoedema** → **compression garments**, skin care, exercise, lymphatic drainage → treat **cellulitis** early because it worsens the swelling.',
 "**Raynaud's** → keep warm, stop smoking, avoid beta-blockers → **nifedipine** → **secondary features**: onset after 30, asymmetric, ulcers, systemic symptoms → rheumatology.")
act('dmcomp_act', 'Diabetes: the yearly review that prevents complications', [71, 67],
 '**Every year** → **retinal screening**, urine **ACR and eGFR**, **10 g monofilament** foot check, BP, lipids → HbA1c target usually **48**, or 53 on drugs that cause hypos.',
 'ACR 3 or more → **ACE inhibitor or ARB** → type 2 → add an **SGLT2 inhibitor** → painful neuropathy → **amitriptyline, duloxetine, gabapentin or pregabalin**.',
 '🔴 **Active diabetic foot problem**: ulcer, infection, ischaemia, Charcot → **multidisciplinary foot team within 1 working day**.')
act('thyroidca_act', 'Thyroid lump and cancer: scan, needle, operate', [74],
 '1️⃣ **TFTs** → **ultrasound** with a U grade → suspicious → **FNA** → unexplained lump with red flags → **2-week wait**.',
 '**Papillary or follicular** → **thyroidectomy** ± radioiodine → levothyroxine to suppress TSH → **medullary** → calcitonin, RET testing, total thyroidectomy → **anaplastic** → palliative.',
 'After surgery → check **calcium** for parathyroid damage → hoarse voice → recurrent laryngeal nerve.')
act('bph_act', 'BPH and urethral stricture: assess, then tablets, then surgery', [75, 85],
 '1️⃣ LUTS → **IPSS**, DRE, urinalysis, counselled PSA, **frequency-volume chart** → voiding symptoms → **alpha-blocker**, tamsulosin.',
 '2️⃣ Prostate over 30 g or PSA over 1.4 → add a **5-alpha reductase inhibitor**, finasteride, which takes months → storage symptoms → antimuscarinic → refractory or complications → **TURP**.',
 '🔴 **Acute retention** → **catheter** → chronic high-pressure retention with AKI → catheterise and watch for **post-obstructive diuresis**. **Urethral stricture** → urethrotomy or dilatation.')
act('prostateca_act', 'Prostate cancer: MRI first, then risk decides', [76],
 '1️⃣ PSA raised for age or a hard nodule on DRE → **2-week wait** → **multiparametric MRI first** → then biopsy.',
 '2️⃣ Low risk, localised → **active surveillance** → intermediate or high → **radical prostatectomy or radiotherapy** with hormones → metastatic → **androgen deprivation**, an LHRH agonist with anti-androgen cover for the flare.',
 '🔴 Back pain with leg weakness → **metastatic spinal cord compression** → **dexamethasone + MRI within 24 hours** → radiotherapy or surgery.')
act('penis_act', 'Penis and scrotum: which lump or problem is urgent', [81],
 '🔴 **Paraphimosis** → reduce it now with ice, compression and gentle pressure → **priapism** over 4 hours → **emergency aspiration**.',
 '**Balanitis** → hygiene, topical antifungal or mild steroid → **phimosis** in adults → steroid cream → circumcision if persistent.',
 'Adult **hydrocele** → **ultrasound** to exclude a tumour → **varicocele** that is new, right-sided or does not empty lying down → **renal imaging** → epididymal cyst → reassure.')
act('oa_act', 'Osteoarthritis and joint replacement: core first, then the knife', [86, 87],
 '1️⃣ Clinical diagnosis → 45 or over, pain with use, morning stiffness under 30 minutes → **exercise and weight loss** for everyone → knee or hand → **topical NSAID** → 2️⃣ **oral NSAID + PPI** → short-term relief → intra-articular steroid.',
 '🎯 Severe pain or loss of function despite this → **joint replacement**.',
 'After replacement → **VTE prophylaxis** → hot, painful joint → **infection** → urgent orthopaedics → posterior hip approach → **dislocation precautions**.')
act('cns_act', 'Raised ICP, bleeds and brain infections: what to do first', [90, 92, 94, 95],
 '🔴 **Raised ICP** → head up 30 degrees, airway, treat the cause → **mannitol or hypertonic saline** → GCS 8 or less → **intubate** → **no LP**.',
 '**Subdural**: acute with mass effect → **craniotomy** → chronic and symptomatic → **burr hole drainage** → reverse anticoagulation → **extradural** → urgent evacuation.',
 '**Encephalitis** → **IV aciclovir immediately** → MRI, LP for HSV PCR, EEG. **Brain abscess** → **IV ceftriaxone + metronidazole** → neurosurgical drainage → find the source: ears, sinuses, teeth, heart.')
act('neuromusc_act', 'MND, GBS, myasthenia and palsies: support the breathing', [97, 98, 99],
 '**Guillain–Barré** → monitor **FVC** → **IV immunoglobulin** or plasma exchange → no steroids → falling FVC → ICU.',
 '**Myasthenia** → **pyridostigmine** → steroids or azathioprine → CT chest for **thymoma** → 🔴 **crisis** → IVIG or plasma exchange + ventilatory support.',
 '**MND** → **riluzole** → breathing failing → **NIV** prolongs life → swallow failing → gastrostomy. **Carpal tunnel** → splint or steroid injection → surgery if severe.')
act('psychosis_act', 'First episode psychosis: refer fast, monitor the body', [100],
 '1️⃣ **Early intervention in psychosis team** within 2 weeks → oral antipsychotic + **CBT for psychosis** + family intervention.',
 'Before and during treatment → **weight, waist, BP, glucose or HbA1c, lipids, prolactin**, ECG if risk → two antipsychotics failed → **clozapine** with blood count monitoring.',
 '🔴 **Acute agitation** → de-escalation → oral lorazepam or an antipsychotic → refused and still a risk → **IM rapid tranquillisation**.')
act('depression_act', 'Depression: risk first, then severity picks the treatment', [102],
 '1️⃣ **Risk first** → active plan or intent → **crisis team or urgent psychiatry** → safety plan.',
 '**Less severe** → guided self-help, CBT or group exercise → **more severe** → **CBT + an SSRI** such as sertraline → review at **2 weeks**, or **1 week** if under 25 or at risk.',
 'Remission → continue **at least 6 months** → stop slowly to avoid discontinuation symptoms → severe, life-threatening or with psychosis → **ECT**.')
act('anxiety_act', 'Anxiety, PTSD, OCD, phobias and adjustment: therapy first', [104, 105, 106, 118, 117],
 '**GAD** → education → low-intensity self-help → **CBT or applied relaxation, or an SSRI** such as sertraline → **panic** → CBT or SSRI → **no benzodiazepines**.',
 '**PTSD** → **trauma-focused CBT or EMDR** → drug only if preferred → venlafaxine or an SSRI. **OCD** → **CBT with exposure and response prevention** → SSRI → both.',
 '**Phobia** → **graded exposure** → **adjustment disorder** → support, problem-solving, short-term help.')
act('edperinatal_act', 'Eating disorders, perinatal illness and unexplained symptoms', [108, 115, 107],
 '**Eating disorder** → **specialist eating disorder service** → anorexia → eating-disorder-focused therapy, family therapy if young → 🔴 medically unstable: very low weight, bradycardia, low BP, low potassium → **admit** with refeeding precautions.',
 '**Postpartum psychosis** → **emergency** → mother and baby unit → **postnatal depression** → guided self-help or CBT → **sertraline** if breastfeeding → avoid **valproate** in anyone who could become pregnant.',
 '**Medically unexplained symptoms** → one named clinician, **regular scheduled appointments**, avoid repeated tests → CBT.')
act('neurodev_act', 'Personality, neurodevelopment and catatonia: who needs what', [109, 119, 114, 120, 121, 113],
 '**EUPD** → **DBT** → crisis plan → medication only short-term in crises. **ADHD** → specialist diagnosis → **methylphenidate**, or lisdexamfetamine in adults → monitor **height, weight, BP and pulse**.',
 '**Autism** → specialist diagnosis → **reasonable adjustments**, treat co-occurring conditions → **conduct disorder or ODD** → **parent training programmes**.',
 '**Intellectual disability** → reasonable adjustments, **annual health check**, capacity per decision → new behaviour → **look for pain or illness first**. **Catatonia** → **lorazepam** → **ECT**.')
act('alcohol_act', 'Alcohol and drugs: withdrawal, Wernicke, relapse', [110],
 '🔴 **Withdrawal** → **chlordiazepoxide** reducing regimen → seizures → lorazepam → **delirium tremens** at 48 to 72 hours → admit.',
 'Any risk of Wernicke\'s → **IV Pabrinex before glucose** → confusion, eye signs, ataxia → high-dose IV thiamine.',
 'Staying off → **acamprosate or naltrexone** → disulfiram as a deterrent → **opioid dependence** → methadone or buprenorphine → overdose → **naloxone**.')
act('delirium_act', 'Delirium: find the cause, calm without drugs', [116],
 '1️⃣ **4AT** → hunt the cause: infection, drugs, **retention, constipation**, pain, hypoxia, salts, glucose → treat it.',
 '2️⃣ **Non-drug care** → glasses and hearing aids, orientation, sleep, mobility, familiar faces → most settle as the cause is treated.',
 '🔴 Distressed or a risk to themselves or others → short-term low-dose **haloperidol** → **avoid** in Parkinson\'s or Lewy body dementia.')
act('derm_act', 'Urticaria, eczema, psoriasis and acne: the step-up', [126, 128, 137, 138],
 '**Urticaria** → **non-sedating antihistamine** → up to four times the dose → chronic → specialist. 🔴 **Anaphylaxis** → **IM adrenaline 500 micrograms**, repeat after 5 minutes.',
 '**Eczema** → **lots of emollient** → flares → topical steroid by strength and site → infected → flucloxacillin → 🔴 **eczema herpeticum** → urgent aciclovir → contact dermatitis → patch test and avoid.',
 '**Psoriasis** → **potent steroid + vitamin D analogue** → then a **4-week break** from potent steroids → phototherapy → methotrexate → biologics.',
 '**Acne** → topical combination for 12 weeks → moderate to severe → add **oral lymecycline or doxycycline** → severe, scarring or failing → **refer for isotretinoin**.')
act('skininf_act', 'Skin infections and infestations: the first line', [130, 129, 133, 134, 135, 136],
 '**Impetigo** → localised → **hydrogen peroxide 1% cream** → topical fusidic acid → widespread or unwell → **flucloxacillin** → off school until crusted or 48 hours of antibiotics. **Folliculitis** → hygiene, topical antiseptic.',
 '**Warts** → leave them → salicylic acid → cryotherapy. **Tinea** of skin → **topical terbinafine** → scalp or nails → **oral** treatment after confirming the fungus.',
 '**Scabies** → **permethrin 5%** to the whole body → **repeat after 7 days** → treat everyone in the household at once → itch can last weeks. **Head lice** → only if live lice → wet combing or dimeticone → repeat after 7 days.')
act('skinsys_act', 'Skin failure and skin signs of disease: act on these', [139, 125],
 '🔴 **Erythroderma or SJS/TEN** → **acute skin failure** → stop the culprit drug, such as allopurinol, anticonvulsants or sulfonamides → admit: fluids, warmth, infection control, nutrition.',
 '**Erythema nodosum** → look for **strep throat, sarcoid, TB, IBD**, pregnancy or the pill → **pyoderma gangrenosum** → IBD or RA → steroids, **no debridement**.',
 'Sudden **acanthosis nigricans** → insulin resistance or a hidden **gastric cancer**.')
act('entkids_act', 'Ears, throats and airways in children', [149, 143, 145, 153, 152],
 '**Otitis media** → analgesia, most settle in 3 days → **amoxicillin** if systemically unwell, under 2 with both ears, discharge, or not improving → **glue ear** → watch 3 months → hearing test → grommets or hearing aids.',
 '🔴 **Epiglottitis** → do not examine the throat → senior anaesthetist and ENT → secure the airway → IV ceftriaxone. **Croup** → **single dose of oral dexamethasone** → severe → nebulised adrenaline and oxygen.',
 '**Glandular fever** → supportive → **no contact sport** while the spleen is big → avoid amoxicillin. Failed newborn hearing screen or speech delay → **audiology**.')
act('vertigo_act', "Vertigo, Ménière's, acoustic neuroma and Bell's palsy", [142, 146, 140, 141, 147],
 '**BPPV** → **Dix–Hallpike** → **Epley manoeuvre**, no drugs → **vestibular neuritis** → prochlorperazine for a few days only → vestibular rehabilitation.',
 "**Ménière's** → ENT → prochlorperazine for attacks → betahistine to prevent → tell the DVLA. **One-sided hearing loss or tinnitus** → **MRI internal auditory meatus**. New neuro signs or a central HINTS exam → **stroke pathway**.",
 "**Bell's palsy** within 72 hours → **prednisolone** → **eye protection**: lubricants and taping at night → forehead spared → stroke pathway. **Sleep apnoea** → Epworth and a sleep study → **CPAP**.")
act('eyemore_act', 'Red eye, cataract and trauma: treat vs same-day', [154, 155, 156, 157, 158, 159, 164, 166, 167],
 '**Conjunctivitis** → mostly self-limiting → severe bacterial → **chloramphenicol drops** → allergic → antihistamine drops. **Blepharitis** → warm compresses and lid hygiene.',
 '🔴 Same day → **keratitis** in a contact lens wearer → stop lenses, no steroids → **uveitis** → steroid and dilating drops → **scleritis** → systemic treatment → **herpes dendritic ulcer** → topical aciclovir.',
 '🔴 **Chemical injury** → **irrigate immediately** for at least 20 minutes, check pH → **penetrating injury** → shield, no pressure → **corneal abrasion** → fluorescein, chloramphenicol. **Cataract** → surgery when it limits life.')

PATH = [{'id': 'nerves', 't': 'Nerve injuries: where the bone breaks, which nerve stops', 'u': [99], 'l': [
 '**Surgical neck of humerus** → **axillary nerve** → numb patch over the deltoid, weak shoulder → **midshaft humerus** → **radial nerve** in its groove → **wrist drop** → so test **wrist extension**.',
 '**Medial epicondyle** → **ulnar nerve** → claw hand, weak finger spreading → **wrist** → **median nerve** in the carpal tunnel → numb thumb side, thenar wasting → **splint first**, surgery if severe.',
 '**Posterior hip dislocation or posterior hip surgery** → **sciatic nerve** → **foot drop**, weakness below the knee → the leg lies short, internally rotated and adducted.',
 '**Fibular neck**, a tight cast or lithotomy stirrups → **common peroneal nerve** → **foot drop**, numb top of the foot. **Inguinal hernia repair** → **ilioinguinal nerve** → numb groin and scrotum.']}]

json.dump({'_about': 'medengine v1.2: ⚡ First move vs cure cards and one new Why card. Own words, UK guidance.', 'act': ACT, 'path_add': PATH},
          open(pathlib.Path(__file__).with_name('v12_content.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(len(ACT), 'action cards,', len(PATH), 'why card')
