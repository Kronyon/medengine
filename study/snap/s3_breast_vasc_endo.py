from snapdsl import N

N(52, 'Fibroadenoma', 'breast', 'lump',
  'A lobule overgrows with fibrous and gland tissue → a smooth, mobile, harmless lump',
  'Women 15 to 35 · grows in pregnancy, shrinks after menopause',
  'Smooth, rubbery lump>breast; Moves freely under the fingers: breast mouse>breast; Painless>breast',
  'Triple assessment>examination, imaging, biopsy*; Ultrasound under 35>well-defined oval; Core biopsy>confirms if uncertain',
  'Reassure once confirmed | Leave it if small | Excise if over 3 cm, growing or the patient wants it out',
  'Rapid growth: phyllodes tumour>u; New lump 30+: suspected cancer pathway>c',
  'Breast mouse: young, smooth, slips away under your fingers.')

N(53, 'Fibroadenosis and breast cysts', 'breast', 'whole',
  'Hormone cycles make breast tissue lumpy and fluid-filled → tender lumps that change with the period',
  'Women 30 to 50 · cysts: just before menopause',
  'Lumpy, tender breasts before a period>breast; Smooth, round cyst that may appear quickly>breast; Both sides>lchest',
  'Triple assessment>examination, imaging, cytology*; Ultrasound>fluid-filled cyst; Aspiration>clear fluid that goes away completely',
  'Reassure, well-fitting bra, simple analgesia | Aspirate a symptomatic cyst | Refer if fluid is bloody or the lump stays',
  'Bloody aspirate or residual lump: cancer>c; Recurring cyst>u',
  'Lumpy and cyclical = hormones; one hard, fixed lump that doesn\'t change = cancer pathway.')

N(54, 'Breast abscess and mastitis', 'breast', 'skin',
  'Milk stasis or a cracked nipple lets bacteria in → the breast inflames → pus can collect',
  'Breastfeeding women · non-lactating: smokers',
  'Hot, red, tender segment of breast>breast; Fever, flu-like>head; Fluctuant lump if abscess>breast',
  'Clinical>diagnosis*; Ultrasound>abscess; Milk culture>if not improving',
  'Keep breastfeeding or expressing; warm compresses, analgesia | Flucloxacillin if not better in 12 to 24 h or infected | Abscess: needle aspiration or drainage | Non-lactating: co-amoxiclav; check for cancer',
  'Sepsis>e; Not settling: inflammatory breast cancer>c; Abscess>s',
  'Keep the milk moving: stopping feeding makes mastitis worse.')

N(55, 'Nipple discharge', 'breast', 'duct',
  'A duct secretes fluid → colour and side tell you the cause',
  'Women 40 to 60 · prolactin-raising drugs',
  'Milky from both: galactorrhoea>breast; Green or cheesy: duct ectasia>breast; Bloody from one duct: papilloma or cancer>breast',
  'Examine: one duct or many, one side or both*; Imaging: mammogram and ultrasound>age-appropriate; Prolactin, pregnancy test>milky discharge',
  'Reassure if physiological | Stop the culprit drug | Treat the cause; duct excision if troublesome or bloody',
  'Blood-stained or one-sided 50+: suspected cancer pathway>c; Milky with headache or visual loss: prolactinoma>u',
  'Many ducts, both sides = usually benign. One duct, one side, blood = investigate.')

N(56, 'Other breast lumps', 'breast', 'lump',
  'Fat necrosis, lipoma, papilloma, phyllodes → most are benign, all need triple assessment',
  'Fat necrosis: after trauma, surgery · phyllodes: 40s',
  'Hard, irregular lump after injury>breast; Soft, mobile lump: lipoma>breast; Rapidly growing lump: phyllodes>breast',
  'Triple assessment>examination, imaging, biopsy*; Imaging>ultrasound under 35, mammogram 35+',
  'Reassure if benign on triple assessment | Excise phyllodes with a margin | Excise if uncertain',
  'Any new unexplained lump 30+: suspected cancer pathway>c; Phyllodes recurrence>u',
  'Fat necrosis can mimic cancer exactly: only biopsy settles it.')

N(57, 'Breast cancer', 'breast', 'lump',
  'Duct or lobule cells mutate → a hard lump grows → it spreads to nodes, bone, liver, lung and brain',
  'Women 50+ · BRCA, family history · early periods, late menopause, HRT, obesity',
  'Hard, irregular, painless lump>breast; Skin tethering, peau d\'orange>breast; Nipple inversion or bloody discharge>breast; Armpit lump>larm',
  'Triple assessment>examination, imaging, core biopsy*; Receptors>oestrogen, progesterone, HER2; Staging>CT, bone scan if needed',
  'Surgery: wide local excision or mastectomy, plus sentinel node | Radiotherapy after WLE | ER positive: tamoxifen before menopause, letrozole after | HER2 positive: trastuzumab; chemotherapy by risk',
  'New lump 30+: suspected cancer pathway>c; Back pain with weakness: cord compression>e; High calcium: confused, constipated>s',
  'Triple assessment: feel it, picture it, biopsy it. All 3, every new lump.')

N(58, 'Hernias', 'scrot', 'canal',
  'Bowel or fat pushes through a weak spot in the abdominal wall → a bulge that comes and goes',
  'Inguinal: men · femoral: older women · heavy lifting, cough, constipation',
  'Groin lump that grows on coughing>groin; Goes back lying down>groin; Inguinal: above and medial to the pubic tubercle>groin; Femoral: below and lateral>groin',
  'Clinical examination standing and lying*; Ultrasound>if unsure',
  'Watch small painless inguinal hernias | Elective mesh repair if symptomatic | Femoral hernias: repair soon, they strangulate',
  'Irreducible, tender, red with vomiting: strangulated>e; Femoral hernia: high strangulation risk>s',
  'Inguinal = above and in from the pubic tubercle. Femoral = below and out, and dangerous.')

N(59, 'Aneurysms', 'limb', 'aorta',
  'A weak arterial wall dilates to over 1.5 times normal → it grows, clots or ruptures',
  'Older men · smokers · high BP · popliteal: often both sides',
  'Pulsatile, expansile mass>abdo; Popliteal: lump behind the knee>legs; Rupture: pain and collapse>back',
  'Ultrasound>size and growth*; CT angiogram>before repair',
  'Surveillance scans by size | Stop smoking, BP, statin | Repair: open or stent graft when big or growing',
  'Rupture>e; Clot to the leg: acute limb ischaemia>e; Popliteal aneurysm: check the other knee and the aorta>u',
  'Find one aneurysm, look for another.')

N(60, 'Acute limb ischaemia', 'limb', 'artery',
  'A clot lodges in or forms in a leg artery → blood supply stops suddenly → the leg dies within hours',
  'AF: embolus · peripheral arterial disease: thrombosis',
  'Pain>legs; Pale>legs; Pulseless>feet; Perishingly cold>feet; Paraesthesia, then paralysis>legs',
  'Clinical: the 6 Ps>diagnosis*; Handheld Doppler>no signal; CT angiogram>where the block is; ECG>AF',
  'Heparin straight away, analgesia | Emergency embolectomy or thrombolysis | Amputation if not salvageable | Find the source: AF, aneurysm',
  'Paralysis and numbness: hours left>e; Reperfusion: high potassium, compartment syndrome>e',
  'The 6 Ps: Pain, Pallor, Pulseless, Perishingly cold, Paraesthesia, Paralysis. The last 2 mean minutes count.')

N(62, 'Peripheral arterial disease', 'limb', 'artery',
  'Plaque narrows the leg arteries → muscles starve on walking → in the end, starve at rest',
  '60+ · smokers, diabetes · high BP, cholesterol',
  'Calf pain on walking, eases with rest>legs; Pain at night, better hanging the leg down>feet; Cold, hairless, shiny legs>legs; Weak or absent foot pulses>feet',
  'ABPI>under 0.9 diagnostic; under 0.5 critical*; Duplex ultrasound>site of narrowing; Bloods>lipids, HbA1c',
  'Stop smoking: the single best thing | Supervised exercise programme | Statin and clopidogrel | Angioplasty or bypass for critical ischaemia',
  'Rest pain, ulcers or gangrene: critical ischaemia>s; ABPI over 1.3: calcified vessels, unreliable>r; Sudden worsening: acute ischaemia>e',
  'Intermittent claudication is angina of the legs.')

N(63, 'Gangrene and ulcers', 'limb', 'skin',
  'Poor blood flow, venous pressure or numbness → skin breaks down and won\'t heal → tissue can die',
  'Arterial: smokers · venous: varicose veins, DVT · neuropathic: diabetes',
  'Arterial: punched out, painful, on toes>feet; Venous: shallow, gaiter area, inner ankle>legs; Neuropathic: painless, under pressure points>feet; Black dead tissue: gangrene>feet',
  'ABPI>before compression*; Swab only if infected>culture; X-ray>osteomyelitis under a diabetic ulcer; HbA1c>diabetes',
  'Treat the cause | Venous: compression if ABPI 0.8 or more | Arterial: revascularise | Diabetic foot: offload, debride; MDT foot team',
  'Wet gangrene or spreading infection>e; Diabetic foot ulcer: foot team within 1 working day>s; Osteomyelitis>s',
  'Arterial hurts, venous weeps, neuropathic doesn\'t feel.')

N(64, 'Varicose veins', 'limb', 'super',
  'Valves in surface veins fail → blood pools and stretches them → bulging, achy veins',
  'Women · pregnancy, standing jobs · family history, obesity',
  'Bulging, twisted leg veins>legs; Aching, heavy legs>legs; Itch, eczema, brown staining>feet; Ankle swelling>feet',
  'Duplex ultrasound>which valves leak*; ABPI>before any compression',
  'Advice: walking, raising legs, weight loss | Compression stockings if not treating | Endothermal ablation first-line | Foam sclerotherapy, then surgery',
  'Bleeding varicose vein: raise and press>s; Venous ulcer>u; Superficial thrombophlebitis near the groin: scan for DVT>s',
  'Faulty one-way valves: the blood falls back down.')

N(65, 'Lymphoedema', 'limb', 'lymph',
  'Lymph drainage is blocked or missing → protein-rich fluid collects → a firm swollen limb',
  'After cancer surgery or radiotherapy · filariasis abroad · primary: young women',
  'Swollen limb, starts in the foot>legs; Can\'t pinch the skin on the toes: Stemmer\'s sign>feet; Skin thickens over time>legs',
  'Clinical diagnosis*; Lymphoscintigraphy>if unsure; Exclude DVT, heart, kidney or liver causes',
  'Skin care, exercise | Compression garments, massage drainage | Treat cellulitis early',
  'Cellulitis>s; Rapid new swelling in a cancer patient: recurrence or DVT>u',
  'Pitting oedema is water; lymphoedema is protein and fibrosis: firm, non-pitting later.')

N(66, 'Raynaud\'s', 'limb', 'fingers',
  'Cold or stress makes finger arteries spasm → fingers go white, then blue, then red',
  'Young women · primary: no cause · secondary: scleroderma, lupus, vibrating tools',
  'White, then blue, then red fingers>hands; Numb, then throbbing>lhand; Triggered by cold>hands',
  'Clinical diagnosis*; Bloods if secondary suspected>ANA, ESR; Nailfold capillaries>abnormal in connective tissue disease',
  'Keep warm, gloves, stop smoking | Nifedipine | Specialist referral if secondary',
  'Ulcers or gangrene of fingertips>s; Onset over 30 or one-sided: look for a cause>u',
  'White, blue, red: like the French flag, wrong way round.')

N(67, 'Diabetes mellitus', 'sugar', 'islet',
  'Type 1: the immune system destroys insulin cells. Type 2: cells resist insulin → glucose stays in the blood → it damages vessels and nerves',
  'Type 1: young, thin · type 2: overweight, 40+, South Asian, African-Caribbean, family history',
  'Thirsty, passing lots of urine>mouth; Weight loss: type 1>abdo; Tired, blurred vision>eyes; Recurrent infections, thrush>genit',
  'HbA1c>48 or more*; Fasting glucose>7 or more; Random glucose>11.1 or more with symptoms; Type 1: ketones>check if unwell',
  'Type 1: basal-bolus insulin, carb counting | Type 2: lifestyle plus modified-release metformin and an SGLT2 inhibitor from diagnosis; frail: metformin alone | Artery disease: add weekly semaglutide | Not at target: DPP-4, pioglitazone, sulfonylurea, GLP-1, then insulin',
  'DKA or HHS>e; Hypos on insulin or sulfonylureas>s; Annual review: eyes, feet, kidneys, BP, lipids>r',
  'Type 1 has no insulin; type 2 has insulin that isn\'t listened to.')

N(68, 'Diabetic ketoacidosis', 'sugar', 'blood',
  'No insulin → fat breaks down into ketones → blood turns acidic and the kidneys dump water',
  'Type 1 · new diagnosis · missed insulin, infection',
  'Vomiting, abdominal pain>abdo; Deep sighing breaths: Kussmaul>lungs; Pear drops breath>mouth; Dehydrated, drowsy>mind',
  'Ketones>3 or more, or urine ++*; Glucose>over 11, or known diabetes; Venous gas>pH under 7.3 or bicarbonate under 15; U&E>potassium',
  'Fluids: 0.9% saline, 1 litre over 1 h if not shocked | Fixed-rate insulin 0.1 units per kg per hour; keep basal insulin | Potassium in the fluids once under 5.5; glucose when under 14 | Find the trigger',
  'Shock or pH under 7.1>e; Cerebral oedema in young people>e; Hypokalaemia from insulin>e',
  'Fluids first, insulin second, watch the potassium third.')

N(69, 'Hyperosmolar hyperglycaemic state', 'sugar', 'blood',
  'Some insulin, not enough → glucose climbs very high without ketones → extreme dehydration over days',
  'Older people with type 2 · infection, stroke, steroids',
  'Very dry, confused>mind; Weak, drowsy>head; Passing lots of urine, then little>supra; Clots and strokes>head',
  'Glucose>usually over 30*; Osmolality>over 320; Ketones>low; U&E>AKI, sodium',
  'IV 0.9% saline slowly, replace over 48 h | Insulin only if ketones or glucose stops falling | LMWH clot prophylaxis | Find the trigger',
  'Falling osmolality too fast: brain swelling>e; Clots: stroke, MI, DVT>e; High mortality in the elderly>e',
  'DKA is fast and acidic; HHS is slow and thick.')

N(70, 'Hypoglycaemia', 'sugar', 'blood',
  'Too much insulin or a sulfonylurea for the food eaten → glucose falls under 4 → the brain runs out of fuel',
  'Insulin and sulfonylurea users · alcohol · missed meals, exercise',
  'Shaky, sweaty, hungry>hands; Palpitations>heart; Confused, odd behaviour>mind; Fits or coma>head',
  'Capillary glucose>under 4*; Ask about drugs, alcohol, timing; Recurrent unexplained: C-peptide>insulinoma or covert insulin',
  'Awake: 15 to 20 g fast sugar, recheck in 15 min | Then a starchy snack | Can\'t swallow: IM glucagon or IV glucose 10%',
  'Unconscious or fitting>e; Sulfonylurea hypo: admit, it recurs>s; Driving: must tell the DVLA if severe>r',
  'Four is the floor; 15 and 15.')

N(71, 'Diabetic complications', 'sugar', 'vessel',
  'Years of high sugar damage small and large vessels → eyes, kidneys and nerves fail; hearts and brains clot',
  'Long-standing, poorly controlled diabetes · smokers · high BP',
  'Blurred vision: retinopathy>eyes; Protein in urine: nephropathy>loin; Numb feet in a stocking pattern>feet; Foot ulcers>feet; Heart attack, stroke>heart',
  'Annual retinal screening>photos*; Urine ACR and eGFR>kidneys; Foot check>monofilament, pulses; HbA1c, BP, lipids>risk',
  'Tight glucose and BP control | ACE inhibitor or ARB if ACR raised; SGLT2 inhibitor | Statin | Laser or eye injections; foot team for ulcers',
  'Sudden visual loss: vitreous bleed>e; Hot swollen foot: Charcot foot>s; Infected foot ulcer>s',
  'Micro: eyes, kidneys, nerves. Macro: heart, brain, legs. One annual review catches them all.')

N(72, 'Thyrotoxicosis', 'neck', 'thyroid',
  'The thyroid makes too much hormone → everything speeds up',
  'Women 20 to 50 · Graves\': smokers · toxic nodules: older',
  'Weight loss, heat intolerance>abdo; Tremor, sweaty>hands; Fast or irregular pulse>heart; Goitre>neck; Bulging eyes: Graves\'>eyes',
  'TSH>suppressed; Free T4 and T3>raised*; TSH receptor antibodies>Graves\'; Uptake scan>nodule or thyroiditis',
  'Beta-blocker for symptoms | Carbimazole: titrate or block and replace | Radioiodine | Surgery if large goitre or eye disease',
  'Thyroid storm: fever, AF, confusion>e; Carbimazole: sore throat = check neutrophils now>e; Eye disease: double vision, visual loss>s',
  'Graves\' is the only cause with eyes and shins.')

N(73, 'Hypothyroidism', 'neck', 'thyroid',
  'The thyroid makes too little hormone → everything slows down',
  'Women · Hashimoto\'s, after radioiodine or surgery · amiodarone, lithium',
  'Tired, weight gain>abdo; Cold intolerance>all; Dry skin, hair loss>head; Constipation>abdo; Slow pulse, slow-relaxing reflexes>legs',
  'TSH>raised*; Free T4>low; TPO antibodies>Hashimoto\'s',
  'Levothyroxine on an empty stomach | Start low in the elderly or heart disease | Check TSH every 6 to 8 weeks until stable, then yearly',
  'Myxoedema coma: cold, drowsy, slow>e; Starting levothyroxine in angina: chest pain>s; Pregnancy: increase the dose>u',
  'Hypo is slow and cold; hyper is fast and hot.')

N(74, 'Thyroid cancer', 'neck', 'nodule',
  'A thyroid cell mutates → a nodule grows → it may spread to neck nodes',
  'Women · radiation to the neck in childhood · family history',
  'Painless neck lump that moves on swallowing>neck; Hoarse voice>throat; Hard, fixed lump or nodes>neck',
  'TFT>usually normal; Ultrasound>suspicious features*; Fine needle aspiration>cell type',
  'Suspected cancer pathway | Thyroidectomy | Radioiodine after surgery for papillary or follicular | Levothyroxine to suppress TSH',
  'Stridor or rapidly growing lump>e; Unexplained thyroid lump: suspected cancer pathway>c',
  'Papillary is commonest and kindest; anaplastic is rare and fast.')

N(75, 'BPH and urethral stricture', 'uro', 'prostate',
  'The prostate enlarges, or scar narrows the urethra → urine flow is squeezed → the bladder struggles to empty',
  'BPH: men 50+ · stricture: after catheters, STIs, trauma',
  'Weak stream, hesitancy>genit; Dribbling after>genit; Frequency, getting up at night>supra; Feeling of not emptying>supra',
  'Urine dip>infection, blood; DRE>smooth, enlarged, not hard*; PSA>after counselling, to look for cancer; U&E, flow rate, bladder scan>kidneys and emptying',
  'Watch, reduce evening fluids, caffeine | Alpha-blocker: tamsulosin | Add 5-alpha reductase inhibitor if big prostate | TURP; stricture: dilatation or urethrotomy',
  'Acute urinary retention: painful, can\'t pass urine: catheter>e; Chronic retention with high creatinine>s; Hard craggy prostate>c',
  'Tamsulosin relaxes the muscle now; finasteride shrinks the gland over months.')

N(76, 'Prostate cancer', 'uro', 'prostate',
  'Prostate cells mutate → a slow tumour grows from the outer zone → it spreads to bone',
  'Men 50+ · Black men · family history, BRCA2',
  'Often no symptoms>genit; Urinary symptoms>supra; Bone pain, back pain>back; Hard, irregular prostate on DRE>genit',
  'PSA>age-specific threshold; MRI prostate>first; Biopsy>Gleason grade*; Bone scan or PSMA PET>staging',
  'Suspected cancer pathway | Low risk: active surveillance | Localised: radical prostatectomy or radiotherapy | Spread: hormone therapy, chemotherapy',
  'Back pain with leg weakness: cord compression, dexamethasone and MRI>e; Hard prostate on DRE: suspected cancer pathway>c; High calcium>s',
  'PSA is a smoke alarm, not a diagnosis: MRI then biopsy.')

N(77, 'Bladder cancer', 'uro', 'bladder',
  'Smoking or chemicals damage the bladder lining → a tumour grows → it bleeds painlessly',
  '60+ · smokers · dye, rubber, chemical workers',
  'Painless visible haematuria>supra; Frequency, urgency>supra; Recurrent UTIs>supra',
  'Urine dip and culture>exclude infection; Cystoscopy>sees and biopsies it*; CT urogram>upper tract',
  'Suspected cancer pathway | TURBT | BCG into the bladder for high-risk superficial | Cystectomy or radiotherapy if invasive',
  '45+ with unexplained visible haematuria: suspected cancer pathway>c; Clot retention>e',
  'Painless visible haematuria is cancer until a cystoscope says otherwise.')

N(78, 'Renal cancer', 'uro', 'kid',
  'Kidney tubule cells mutate → a tumour grows silently → found by chance or with blood in the urine',
  '60+ · smokers · obesity, high BP · dialysis, von Hippel-Lindau',
  'Haematuria>loin; Loin pain>loin; Loin mass>loin; Often found by chance on a scan>abdo',
  'CT abdomen with contrast>mass*; Bloods>FBC: polycythaemia or anaemia, calcium; Biopsy sometimes',
  'Suspected cancer pathway | Partial or radical nephrectomy | Ablation for small tumours | Immunotherapy or targeted drugs if spread',
  'Visible haematuria 45+>c; Left varicocele in a man: renal vein invasion>u; High calcium>s',
  'Haematuria, loin pain, loin mass: the classic triad, but most are found by accident on scans.')

N(79, 'Urinary tract stones', 'uro', 'ureter',
  'Calcium or urate crystallises in concentrated urine → a stone forms → it jams in the ureter and spasms',
  'Men 30 to 60 · dehydration · high calcium, gout · previous stones',
  'Severe colicky loin pain to the groin>loin; Can\'t keep still>abdo; Haematuria>supra; Nausea, vomiting>mouth',
  'Urine dip>blood; Non-contrast CT KUB within 24 h>the stone*; Bloods>U&E, calcium, urate; Pregnancy or under 16: ultrasound',
  'NSAID for pain | Under 10 mm: watch, alpha-blocker may help | Shockwave lithotripsy or ureteroscopy | Drink 2.5 to 3 litres a day',
  'Stone with fever: infected obstructed kidney, decompress now>e; Single kidney or AKI>e; Pain not controlled>s',
  'An infected obstructed kidney is pus under pressure: drain it today.')

N(80, 'Urinary tract infection', 'uro', 'bladder',
  'Gut bacteria climb the urethra → the bladder inflames → they can reach the kidney',
  'Women · pregnancy · catheters, diabetes · men: always a complicated UTI',
  'Burning on passing urine>genit; Frequency, urgency>supra; Suprapubic pain>supra; Kidney: fever, loin pain, vomiting>loin; Elderly: confusion>mind',
  'Urine dip>nitrites and leucocytes, under 65 women*; MSU culture>men, pregnant, over 65, failed treatment; Bloods if pyelonephritis>U&E, cultures',
  'Women: nitrofurantoin 3 days, or trimethoprim | Men or pregnant: 7 days; pregnancy: no trimethoprim in first trimester | Pyelonephritis: cefalexin or co-amoxiclav 7 to 10 days | Recurrent: prevention advice, consider prophylaxis',
  'Urosepsis>e; Pyelonephritis in pregnancy>s; Obstructed infected kidney>e',
  'Don\'t dip the over 65s: their urine is often colonised. Treat symptoms, not dipsticks.')

N(81, 'Diseases of the penis and scrotum', 'scrot', 'penis',
  'Foreskin, fluid collections and veins misbehave → most are benign; a few are emergencies',
  'Any age man · phimosis: boys and older men · hydrocele: babies and adults',
  'Foreskin won\'t retract: phimosis>genit; Retracted and stuck, swollen: paraphimosis>genit; Painless sac that lights up: hydrocele>genit; Bag of worms on the left: varicocele>genit',
  'Examination: get above it? separate from testis? transilluminates?*; Ultrasound scrotum>any doubt or adult hydrocele',
  'Phimosis: steroid cream, circumcision if needed | Paraphimosis: reduce now: ice, squeeze, push | Hydrocele: watch or repair | Varicocele: usually leave',
  'Paraphimosis>e; Priapism over 4 h>e; New varicocele that doesn\'t go lying down: renal mass>u',
  'Three questions solve every scrotal lump: above it, separate, lights up.')

N(82, 'Epididymitis and orchitis', 'scrot', 'epi',
  'Infection travels down the vas → the epididymis then testis inflame → gradual swelling and pain',
  'Under 35: chlamydia, gonorrhoea · over 35: E. coli from the urine · mumps',
  'Gradual onset testicular pain>genit; Swollen tender epididymis>genit; Lifting the testis eases it>genit; Dysuria, discharge>genit',
  'Urine NAAT and MSU>the bug*; Ultrasound if any doubt>exclude torsion',
  'Rule out torsion first | Under 35: ceftriaxone plus doxycycline | Over 35: ofloxacin or levofloxacin | Scrotal support, analgesia',
  'Can\'t exclude torsion: theatre>e; Abscess>s; Infertility after mumps orchitis>r',
  'Torsion is sudden; epididymitis is gradual. When unsure, explore.')

N(83, 'Testicular torsion', 'scrot', 'cord',
  'The testis twists on its cord → its blood supply is cut off → it dies within about 6 hours',
  'Boys and young men 12 to 25 · bell-clapper anatomy · after exercise or at night',
  'Sudden severe testicular pain>genit; Nausea, vomiting>mouth; High-riding, horizontal testis>genit; Absent cremasteric reflex>legs',
  'Clinical diagnosis: don\'t wait for a scan*; Ultrasound only if it will not delay theatre',
  'Analgesia | Emergency surgical exploration | Untwist and fix both testes; remove if dead',
  'Over 6 hours: testis likely lost>e; Abdominal pain in a boy: check the testes>e',
  'Sudden pain in a young testis = theatre now. Time is testis.')

N(84, 'Testicular cancer', 'scrot', 'testis',
  'A germ cell in the testis mutates → a painless hard lump grows → spreads to para-aortic nodes',
  'Men 15 to 45 · undescended testis · family history',
  'Painless, hard lump in the testis>genit; Heavy, dragging scrotum>genit; Gynaecomastia>breast; Back pain from nodes>back',
  'Ultrasound scrotum>solid mass in the testis*; Tumour markers>AFP, beta-hCG, LDH; CT chest, abdomen, pelvis>staging',
  'Suspected cancer pathway | Radical inguinal orchidectomy; sperm banking first | Chemotherapy or radiotherapy by type | Follow-up with markers and scans',
  'Any solid lump in the testis: suspected cancer pathway>c; Breathless with lung spread>u',
  'Seminoma: older, radiosensitive. Teratoma: younger, AFP and hCG. Both highly curable.')

N(85, 'Urinary catheterisation', 'uro', 'urethra',
  'A tube drains the bladder through the urethra → for retention, monitoring or surgery → every day in place raises infection risk',
  'Retention · strict fluid balance · surgery · incontinence when nothing else works',
  'Painful palpable bladder in retention>supra; Residual volume on bladder scan>supra; Blocked or bypassing catheter>genit',
  'Bladder scan>residual volume*; Urine output hourly>after insertion; Culture only if symptomatic>not routine',
  'Consent, chaperone, aseptic technique | Men: penis up at 90°, to the hilt, urine, then inflate 10 ml | Replace the foreskin | Remove as soon as not needed; trial without catheter',
  'Paraphimosis from forgetting the foreskin>e; Urethral trauma: blood, can\'t pass>s; Catheter UTI with fever>s',
  'Urine first, balloon second, foreskin back third.', k='t')
