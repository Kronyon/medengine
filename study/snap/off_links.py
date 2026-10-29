"""🧬 How the official papers repeat themselves: groups of questions (official papers and my mock) that share one scene.
Ids: 'mla1:17' = MS AKT practice paper 1 Q17; 'p2019:5' = MSCAA December 2019 Q5; 'mock:93' = my mock Q93.
Kinds:
  clone  🔥 the same question, word for word or nearly, in two papers (or the same image reused)
  chain  ⛓️ the same patient, sliced at a different step: diagnosis, then investigation, then treatment
  block  🚫 the first-line answer, then the one comorbidity, job or setting that blocks it
  decoy  ⚠️ a lab value just over the line, nowhere near the diagnostic threshold
  matrix 🧮 one decision grid tested from every angle across papers
  twin   🔗 the same mechanism or trap in a different patient
Each group: (kind, title, the rule that solves all of them, [ids])."""
GROUPS = [
    ('clone', 'Shingles around the eye', 'Treated herpes zoster ophthalmicus in a well 45-year-old usually resolves completely; an older age or eye involvement changes the outlook.', ['mla1:17', 'mock:93']),
    ('clone', 'Diastolic murmur in AF', 'A diastolic murmur at the apex with AF in an older woman is mitral stenosis; ejection systolic to the carotids is aortic stenosis.', ['mla1:93', 'mock:48']),
    ('clone', 'Smoking and birthweight', 'Exposure recorded first, outcome measured later = prospective cohort; outcome first, then look back = case-control.', ['p2018:6', 'p2019:33', 'p2017:42', 'mla2:76']),
    ('clone', 'One chest X-ray, two answers', 'The same film of multiple nodules is granulomatosis with polyangiitis in a woman with sinus, nose and kidney signs, and metastatic cancer in a 76-year-old losing weight. The story picks the answer, not the picture.', ['mla1:57', 'p2020:44', 'mock:30']),
    ('chain', 'Renal colic', 'Loin to groin colic with blood in the urine: NSAID first for pain (diclofenac), non-contrast CT KUB to confirm, drain if infected and obstructed.', ['mla2:98', 'mock:89', 'p2020:12', 'p2018:28']),
    ('chain', 'Ulcerative colitis with cholestasis', 'UC with a raised ALP and GGT: the diagnosis is primary sclerosing cholangitis, the test that shows it is MRCP.', ['mla1:64', 'p2017:13']),
    ('chain', 'Biliary colic', 'Pain for an hour after meals, then gone: ultrasound to find the stone, then laparoscopic cholecystectomy. Fever and a high CRP make it cholecystitis.', ['mla1:44', 'p2018:40', 'mock:60', 'mla1:99', 'p2020:1', 'mock:55', 'mock:59', 'mock:98']),
    ('chain', 'Nephrotic syndrome', 'Oedema, albumin under 25 and a protein:creatinine ratio over 300: diagnose nephrotic syndrome, biopsy to find the cause in adults, furosemide for the oedema.', ['p2019:5', 'p2018:50', 'mla1:20', 'p2020:34']),
    ('chain', 'Cancer and back pain: the cord ladder', 'Recognise cord compression, give dexamethasone 16 mg, MRI the whole spine within 24 hours, then radiotherapy or surgery.', ['p2017:3', 'p2019:30', 'p2020:39', 'p2017:30', 'mla2:24', 'mock:67', 'mla2:97']),
    ('chain', 'Thunderclap headache', 'Peak within a minute is the red flag. CT within 6 hours that is normal rules it out; after 6 hours a normal CT needs an LP at 12 hours.', ['mla1:55', 'p2017:47', 'p2020:46', 'p2018:41']),
    ('chain', 'Stiff shoulders and hips', 'Over 50, morning stiffness for hours, high ESR, normal CK: polymyalgia rheumatica, prednisolone. Jaw pain or visual loss makes it GCA.', ['p2018:2', 'p2019:27', 'mla2:93', 'p2017:48', 'mla2:57']),
    ('chain', 'Hypoglycaemia', 'Conscious and able to swallow → oral glucose; unconscious with IV access → 75 mL of 20% glucose; no access → IM glucagon.', ['p2019:9', 'p2020:15', 'mla1:45']),
    ('chain', 'Opioid maths', 'Oral morphine ÷ 2 = 24-hour subcutaneous morphine; ÷ 3 = diamorphine. Breakthrough = one sixth of the 24-hour total. Add the breakthrough used to the new regular dose.', ['p2020:3', 'p2019:20', 'mla2:82', 'mock:99', 'p2020:5']),
    ('chain', 'Myasthenia and its mimics', 'Fatigable ptosis and diplopia → myasthenia; monitor breathing with FVC; reversal is with neostigmine.', ['mla1:3', 'p2020:49', 'p2018:27', 'mla2:71']),
    ('block', 'Delirium that needs a drug', 'Haloperidol if a drug is needed; Parkinson\'s blocks antipsychotics → lorazepam; dying → midazolam.', ['p2018:25', 'p2017:2', 'p2017:38', 'mla1:24']),
    ('block', 'Acute gout', 'NSAID or colchicine and keep the allopurinol going; CKD stage 4 blocks NSAIDs → oral prednisolone.', ['p2018:31', 'p2017:35', 'mla2:19', 'mla2:51']),
    ('block', 'Nerve pain', 'Amitriptyline, duloxetine, gabapentin or pregabalin; eGFR under 30 blocks duloxetine → amitriptyline.', ['p2020:5', 'mla1:40']),
    ('block', 'Osteoarthritis pain', 'Exercise, paracetamol, topical NSAID; kidney or heart disease blocks oral NSAIDs → regular co-codamol; BMI 48 → bariatric referral.', ['mla2:2', 'p2020:25', 'mla1:86', 'p2018:26']),
    ('block', 'Who can have what', 'A job that needs alertness blocks sedating antihistamines (loratadine); a past DVT blocks co-cyprindiol (lymecycline); severe COPD blocks systemic opioids (epidural); LV failure lowers maintenance fluid to 25 mL/kg.', ['mla1:15', 'mla1:61', 'p2017:41', 'p2018:24']),
    ('block', 'Blood pressure steps', 'Diabetes or under 55 → ACE inhibitor; Black African or Caribbean → amlodipine; creatinine up under 30% on an ACE inhibitor → repeat in 2 weeks; eGFR under 30 with oedema → furosemide, not a thiazide.', ['mla1:34', 'p2017:43', 'p2019:32', 'p2020:13', 'p2020:34', 'p2018:18', 'mock:78', 'mock:90']),
    ('decoy', 'CK in the hundreds after a long lie', 'A CK of 840 to 870 is minor muscle injury. The AKI comes from hypovolaemia: low BP, high urea, high haemoglobin. Rhabdomyolysis needs a CK in the thousands with dark urine.', ['mla1:9', 'p2017:8']),
    ('decoy', 'Amylase just over the line', 'An amylase of 222 against a limit of 220 is not pancreatitis, which needs over 3 times the limit. RUQ pain, fever and a high CRP with a normal bilirubin = acute cholecystitis.', ['p2020:1', 'mla1:7']),
    ('decoy', 'Mildly raised numbers that mean nothing', 'Troponin 0.025 with saddle ST elevation = pericarditis; testosterone 3.5 in a woman = PCOS, over 5 = tumour; ESR 12 with a frozen shoulder = adhesive capsulitis.', ['p2019:21', 'p2017:28', 'p2020:28', 'p2020:9']),
    ('matrix', 'Anticoagulation grid', 'CHA2DS2-VASc 0 → nothing; AF after a stroke → DOAC; forgets warfarin → DOAC with a dosette; mechanical valve → warfarin only; INR high, no bleed → withhold; major bleed → IV vitamin K and PCC; PE after a recent bleed → IV unfractionated heparin you can switch off.', ['p2017:22', 'p2017:5', 'mla1:53', 'p2020:10', 'p2018:5', 'mla1:6', 'p2018:49', 'mla1:32', 'p2020:8', 'mock:100']),
    ('matrix', 'Calcium grid', 'High calcium + high PTH = primary hyperparathyroidism; high calcium + suppressed PTH = malignancy, myeloma or sarcoidosis; low calcium + high PTH + high ALP = osteomalacia; lithium with polyuria → check calcium.', ['p2017:21', 'mla1:62', 'mla1:69', 'p2019:2', 'p2017:49', 'p2017:4', 'mla2:4']),
    ('matrix', 'Blood gas grid', 'High CO2 with low pH and a normal bicarbonate = acute type 2 failure; high bicarbonate = chronic. Acidotic COPD on oxygen → NIV. Rising CO2 in asthma = exhaustion.', ['p2019:50', 'p2017:15', 'mla2:99', 'mock:46']),
    ('matrix', 'Why is the urine output low?', 'Low BP, fast pulse, low JVP within a day = prerenal, give fluid; raised JVP and crackles = cardiogenic; no response after days = ATN; full bladder = obstruction.', ['p2020:42', 'p2019:3', 'mla1:28', 'mock:77', 'mla2:80', 'mla2:95']),
    ('twin', 'Painful red eye with poor vision', 'Pain plus reduced acuity, photophobia or a hazy cornea = same-day eye referral; normal acuity and gritty = primary care.', ['p2019:29', 'mla1:38', 'mock:14', 'mock:31', 'p2018:44', 'mla1:13']),
    ('twin', 'Sudden visual loss', 'Pain on eye movement with an RAPD = optic neuritis; cherry-red spot = CRAO; haemorrhages in one sector = branch vein; flashes then a curtain = detachment.', ['mla1:16', 'mock:32', 'mla1:36', 'p2017:1', 'p2019:11']),
    ('twin', 'Hearing loss and vertigo', 'One-sided sensorineural loss with facial numbness → MRI internal acoustic meatus; vertigo under a minute on turning → BPPV, Dix–Hallpike.', ['p2020:20', 'p2020:30', 'mla2:70', 'p2019:22', 'p2018:32']),
    ('twin', 'Hot swollen joint', 'Aspirate before antibiotics, but a negative Gram stain does not rule out sepsis: start IV flucloxacillin if it looks septic.', ['p2020:14', 'mock:74', 'mla2:51', 'p2017:12']),
    ('twin', 'Pain out of proportion', 'AF or a recent arterial procedure, severe pain, a normal X-ray and a high lactate = mesenteric ischaemia.', ['p2020:7', 'mock:37']),
    ('twin', 'Steroids and the adrenal', 'Low sodium, high potassium, low glucose and a postural drop = adrenal insufficiency; check cortisol and ACTH, and a short Synacthen before stopping long-term steroids.', ['p2020:38', 'mock:52']),
    ('twin', 'Lithium after diarrhoea', 'Dehydration on lithium with coarse tremor and confusion = toxicity; same-day assessment and a level.', ['p2019:34', 'mock:19', 'p2017:4']),
    ('twin', 'Blood in the urine after a sore throat', 'Within a few days of the infection = IgA nephropathy; 1 to 3 weeks later with a low C3 = post-streptococcal.', ['p2017:32', 'mock:80']),
    ('twin', 'Where gonads drain', 'Testis and ovary start in the abdomen and drain to the para-aortic nodes; scrotal skin drains to the inguinal nodes.', ['p2018:39', 'mock:38']),
    ('twin', 'Breast lumps', 'Mobile painless lump in a young woman = fibroadenoma; cyclical nodularity and a cyst that empties = fibrocystic; any lump = triple assessment with core biopsy.', ['p2018:37', 'p2019:31', 'mla2:84', 'mla2:86', 'mock:69', 'mock:70']),
    ('twin', 'Headache after a spinal', 'Worse standing, better lying flat = low pressure headache; if it persists → epidural blood patch.', ['p2018:13', 'mock:91']),
    ('twin', 'B12 and the spinal cord', 'Absent ankle jerks with brisk knees and extensor plantars plus lost vibration and position sense = B12 deficiency.', ['p2019:1', 'mla1:14']),
    ('twin', 'TB drugs', 'Eyes → ethambutol; orange urine → rifampicin; tingling feet → isoniazid; gout → pyrazinamide.', ['mla1:60', 'p2019:46']),
    ('twin', 'Glandular fever', 'Sore throat, nodes, splenomegaly and atypical lymphocytes → EBV test; amoxicillin causes a rash.', ['mla1:58', 'p2019:41']),
    ('twin', 'Sudden breathlessness after a procedure or in asthma', 'Pleuritic pain and a missing lung edge = pneumothorax; days after surgery with a fast pulse = PE.', ['p2017:26', 'p2018:29', 'p2020:31', 'mla2:94', 'p2017:17', 'p2018:14']),
    ('twin', 'Subdural, extradural, subarachnoid', 'Lucid interval after a blow to the temple = extradural, middle meningeal artery; gradual confusion in an older drinker = subdural, bridging veins.', ['p2020:43', 'mla2:46', 'mla1:32']),
    ('twin', 'Thyroid in women', 'Painless thyroiditis months after birth → propranolol; eye signs and a high uptake = Graves\', antibodies to the TSH receptor.', ['mla1:22', 'p2019:35']),
    ('twin', 'Bleeding and clotting together', 'Sepsis, burns or trauma with low platelets, long PT and APTT and low fibrinogen = DIC.', ['p2018:47', 'p2019:17', 'p2020:19']),
]
