from snapdsl import N

N(0, 'Acute coronary syndrome', 'heart', 'cor',
  'A plaque in a coronary artery cracks → a clot forms on it → the muscle downstream starves and dies',
  '50+ · men, smokers · diabetes, high BP, cholesterol · family history',
  'Crushing central chest pain over 15 min>chest; Spreads to the left arm or jaw>larm; Sweaty, grey, sick>face; Breathless>lungs',
  'ECG within 10 min>ST up in 2 neighbouring leads = STEMI*; High-sensitivity troponin>rises; repeat at 0 and 3 h for NSTEMI; Bloods>FBC, U&E, glucose, lipids',
  'Aspirin 300 mg, pain relief, oxygen only if sats under 94% | STEMI: PCI within 2 h, or a clot-busting drug | NSTEMI: GRACE score, second antiplatelet, angiogram | For life: aspirin, statin, beta-blocker, ACE inhibitor, rehab',
  'VF arrest in the first hours>e; Heart failure or cardiogenic shock>e; New murmur: papillary muscle or septal rupture>e; Pericarditis days to weeks later>s',
  'Time is muscle: every minute of a blocked artery is muscle you never get back.')

N([1, 61], 'Aortic dissection', 'heart', 'aorta',
  'A tear in the inner lining → blood splits the aortic wall → branches get cut off as it runs',
  '50 to 70 · uncontrolled high BP · Marfan\'s · cocaine, pregnancy',
  'Sudden tearing pain through to the back>back; Arm BPs differ by over 20>rarm; Pulse missing in an arm or leg>legs; Stroke or paraplegia signs>head',
  'CT angiogram of the aorta>flap splitting true and false lumen*; Chest X-ray>may show a wide mediastinum; ECG>to rule out MI; never treat as MI with clot-busters',
  'Pain relief | IV labetalol: pulse under 60, systolic 100 to 120 | Type A, ascending: emergency surgery | Type B, descending: BP control, stent if complicated',
  'Rupture and tamponade>e; Aortic regurgitation from the root>e; Gut, kidney or limb ischaemia>e',
  'MI pain builds and squeezes; dissection rips in a second and travels.')

N(2, 'Ischaemic heart disease and stable angina', 'heart', 'cor',
  'A fatty plaque narrows a coronary artery → enough flow at rest, not on effort → chest tightness that settles with rest',
  '50+ · smokers, diabetes, high BP · raised cholesterol · family history',
  'Tight chest on exertion>chest; Settles within 5 min of rest or GTN>heart; Worse in cold or after meals>lungs; Breathless on effort>lungs',
  'ECG>often normal at rest; CT coronary angiogram>first test for typical or atypical angina*; Bloods>lipids, HbA1c, FBC, TFT; Stress imaging or invasive angiogram>if CT is unclear',
  'GTN spray for attacks, plus aspirin and statin | Beta-blocker or calcium-channel blocker | Both, then long-acting nitrate, ivabradine or ranolazine | PCI or bypass if symptoms persist',
  'Pain at rest or lasting over 15 min = ACS>e; New angina or getting worse fast>s; Heart failure>u',
  'Supply versus demand: the narrow pipe copes until the heart asks for more.')

N(3, 'Arrhythmias', 'heart', 'atria',
  'The electrical wiring misfires → the heart beats too fast, too slow or chaotically → less blood pumped per minute',
  'Any age · AF: older, high BP, alcohol, thyroid · SVT: young, fit',
  'Palpitations: tap the rhythm>heart; Dizzy or fainting>head; Breathless>lungs; Chest pain>chest',
  '12-lead ECG>the rhythm in the moment*; 24 h tape or event recorder>if it comes and goes; Bloods>TFT, U&E, magnesium; Echo>structural heart disease',
  'Unstable: shock, syncope, chest pain or heart failure? Synchronised DC shock | Stable narrow regular: vagal manoeuvres, then adenosine | AF: rate control with a beta-blocker or diltiazem | AF: anticoagulate if CHA2DS2-VASc 2 or more; ablation or rhythm control for some',
  'Adverse features: shock, syncope, ischaemia, heart failure>e; Stroke from AF clot>e; Broad complex tachycardia>e',
  'First ask: is the patient stable? The rhythm comes second.')

N(4, 'Hypertension', 'heart', 'lv',
  'Stiff arteries and salt, kidney and hormone signals → the pressure stays high → the heart thickens and vessels wear out silently',
  'Increasing with age · Black African or Caribbean · obesity, salt, alcohol · under 40: look for a cause',
  'Usually nothing at all>all; Headache if very high>head; Found at a check-up>rarm',
  'Clinic BP 140 over 90 or more>then confirm out of clinic; Home or ambulatory average 135 over 85 or more>confirms it*; End-organ check>urine ACR, U&E, HbA1c, lipids, ECG, fundi; QRISK3>cardiovascular risk',
  'Lifestyle, then ACE inhibitor or ARB if under 55 or diabetic; CCB if 55+ or Black African or Caribbean | Add the other one or a thiazide-like diuretic | All three: ACE inhibitor or ARB, CCB, thiazide-like | Step 4: spironolactone if potassium 4.5 or less, else alpha or beta-blocker',
  '180 over 120 with papilloedema or retinal bleeds>s; Chest pain, confusion, AKI>e; Stroke, MI, kidney damage over years>r',
  'The silent killer: no symptoms, all the damage. Treat the number before it treats you.')

N(5, 'Hyperlipidaemia', 'heart', 'cor',
  'Too much LDL in the blood → it slips into artery walls → plaques grow and narrow the arteries',
  'Any adult · diet, obesity, diabetes, hypothyroidism · familial: young, strong family history',
  'Usually nothing>all; Tendon xanthomas on the knuckles or Achilles>hands; Yellow lid plaques>eyes; Arcus under 45>eyes',
  'Non-fasting lipid profile>total, HDL, non-HDL, triglycerides; QRISK3>10 or more = offer a statin*; TFT, LFT, HbA1c, U&E>secondary causes and baseline',
  'Diet, exercise, stop smoking | Primary prevention: atorvastatin 20 mg; aim for a 40% fall in non-HDL | Secondary prevention: atorvastatin 80 mg; aim for LDL 2.0 or less | Not at target: add ezetimibe, then inclisiran or a PCSK9 inhibitor if eligible',
  'Muscle pain on a statin: check CK>u; Total cholesterol over 7.5 with family history: think familial>u; Triglycerides over 20: pancreatitis risk>s',
  'LDL is the plaque builder; statins turn down the liver\'s cholesterol factory.')

N(6, 'Heart failure', 'heart', 'lv',
  'The pump weakens or stiffens → blood backs up into the lungs and legs → the body holds on to salt and water',
  '65+ · after MI, high BP, valve disease · AF, alcohol, cardiomyopathy',
  'Breathless on effort and lying flat>lungs; Waking breathless at night>chest; Swollen ankles>feet; Raised JVP>neck; Tired, fewer stairs>legs',
  'NT-proBNP>over 2000 = specialist and echo within 2 weeks*; Echo>ejection fraction: reduced if 40% or less; Chest X-ray>bat wings, Kerley B, big heart, effusions; ECG and bloods>U&E, FBC, TFT',
  'Loop diuretic for fluid | Reduced EF: ACE inhibitor or ARNI, plus beta-blocker | Add spironolactone and an SGLT2 inhibitor: the four pillars | Device: ICD or CRT if still weak',
  'Pink frothy sputum, can\'t lie flat: acute pulmonary oedema>e; Potassium or creatinine climbing on treatment>u; Daily weight up 2 kg in 3 days>s',
  'Left side fails: lungs flood. Right side fails: legs and liver swell.')

N(7, 'Heart valve disease', 'heart', 'aov',
  'A valve narrows or leaks → the chamber behind works harder → it thickens or stretches, then fails',
  'AS: 70+, calcified or bicuspid at 50s · MR: after MI, prolapse · rheumatic fever history',
  'AS: Syncope, Angina, Dyspnoea>chest; AS: slow-rising pulse>rarm; Murmur on auscultation>heart; Breathless, tired>lungs',
  'Echo>valve area, gradient and how the ventricle is coping*; ECG>LVH, AF; Chest X-ray>big heart or congestion',
  'Watch and repeat echo if no symptoms | Treat AF and heart failure | AS with symptoms: valve replacement, surgical or TAVI | Severe MR: repair or replace',
  'AS with syncope or angina: high risk of sudden death>s; Fever plus a murmur = endocarditis>e; Sudden new MR after MI>e',
  'AS = SAD; aortic stenosis is the murmur that goes to the neck, MR goes to the armpit.')

N(8, 'Infective endocarditis', 'heart', 'mv',
  'Germs land on a damaged or artificial valve → a vegetation grows → bits fly off and the valve leaks',
  'IV drug users: right side, S. aureus · prosthetic or damaged valves · recent dental or line procedures',
  'Fever and a new murmur>heart; Splinters, Janeway lesions, Osler nodes>hands; Roth spots>eyes; Stroke or emboli>head; Tired, weight loss>all',
  'Blood cultures: 3 sets from different sites before antibiotics>the bug*; Echo, transoesophageal if needed>vegetation; Urine>microscopic haematuria; CRP, ESR, FBC>inflammation',
  'Start IV antibiotics after cultures, guided by microbiology | Treat for 4 to 6 weeks | Surgery: heart failure, abscess, big vegetation, failing antibiotics',
  'Heart failure from a wrecked valve>e; Septic emboli: brain, spleen, kidney>e; Heart block on ECG = root abscess>e',
  'Fever plus a new murmur is endocarditis until 3 blood cultures say otherwise.')

N(9, 'Pleural effusion', 'lungs', 'pleura',
  'Fluid collects between the lung and chest wall → the lung is squashed → breathless and dull at the base',
  'Transudate: heart, liver or kidney failure · exudate: pneumonia, cancer, TB, PE',
  'Breathless>lungs; Stony dull to percussion>chest; Quiet breath sounds at the base>lungs; Trachea pushed away if huge>neck',
  'Chest X-ray>meniscus, blunt angle*; Ultrasound-guided tap>protein, LDH, pH, glucose, cytology, culture; Light\'s criteria>exudate if fluid to serum protein over 0.5 or LDH over 0.6',
  'Treat the cause: diuretics for heart failure | Drain if large or symptomatic, slowly | Infected, pH under 7.2: chest drain | Recurrent cancer effusion: pleurodesis or indwelling catheter',
  'Empyema: fever, pus, pH under 7.2>e; New one-sided effusion in a smoker = cancer until proved otherwise>c; Re-expansion oedema if drained too fast>s',
  'Transudate leaks from pressure; exudate pours from inflammation. Protein tells you which.')

N(10, 'Anaemia', 'blood', 'rbc',
  'Too little haemoglobin → less oxygen carried → the heart beats faster to make up for it',
  'Women with heavy periods · older people: GI bleeding · poor diet, vegans · chronic disease',
  'Tired, breathless>lungs; Pale conjunctiva>eyes; Fast pulse, flow murmur>heart; Angular cheilitis, spoon nails>hands',
  'FBC and MCV>small, normal or big cells*; Iron studies, B12, folate>which ingredient is missing; Reticulocytes, film>bleeding or breakdown; FIT or scopes>iron deficiency over 60 or in men',
  'Find and treat the cause first | Iron: ferrous sulfate once daily, recheck in 2 to 4 weeks | B12: IM hydroxocobalamin; folate tablets once B12 is replaced | Transfuse only if severe or bleeding',
  'Iron deficiency in a man or post-menopausal woman: GI cancer pathway>c; Chest pain or heart failure from anaemia>s; Low platelets and white cells too: marrow>u',
  'Small cells = iron; big cells = B12, folate or alcohol; normal cells = chronic disease or bleeding.')

N(11, 'Pneumothorax', 'lungs', 'air',
  'Air leaks into the pleural space → the lung falls away from the chest wall → sudden one-sided breathlessness',
  'Tall thin young men · smokers · COPD, asthma · trauma',
  'Sudden one-sided sharp chest pain>chest; Breathless>lungs; Hyper-resonant, quiet side>lchest; Tension: trachea shifted, low BP>neck',
  'Chest X-ray>a visible rim, no lung markings beyond it*; CT>if unclear or COPD; Tension: treat first, X-ray after',
  'Small, no symptoms: watch and repeat X-ray | Symptomatic primary: needle aspiration, or ambulatory device | Secondary or failed aspiration: chest drain | Recurrent: surgery; no flying until resolved',
  'Tension: shock, shifted trachea>e; Needle decompression 2nd space midclavicular or 5th mid-axillary>e; Bilateral or in COPD>e',
  'Tension is a clinical diagnosis: decompress first, X-ray later.')

N(12, 'Respiratory failure and acid-base', 'lungs', 'alv',
  'Lungs fail to swap gases → oxygen falls, with or without CO2 rising → the blood turns acidic',
  'Type 1: pneumonia, PE, oedema · type 2: COPD, opioids, neuromuscular weakness',
  'Breathless, using extra muscles>neck; Blue lips>mouth; CO2 rise: flap, bounding pulse>hands; Drowsy, confused>head',
  'Arterial blood gas>pH, PaO2, PaCO2, bicarbonate*; Type 1: low O2, normal or low CO2>oxygenation; Type 2: low O2, high CO2>ventilation',
  'Treat the cause | Oxygen: target 94 to 98%, or 88 to 92% if CO2 retainer | Type 2 with pH under 7.35: NIV | Intubate if failing NIV',
  'pH under 7.25 with rising CO2>e; Drowsy CO2 narcosis>e; Exhausted, tiring breathing>e',
  'ROME: Respiratory Opposite, Metabolic Equal. Then check whether the other system is compensating.')

N(13, 'VTE and pulmonary embolism', 'limb', 'vein',
  'Slow flow, damaged vein and sticky blood → a clot forms in a deep leg vein → it can break off to the lungs',
  'After surgery or immobility · cancer, pregnancy, the pill · previous clot',
  'One swollen, tender calf>legs; Sudden breathlessness>lungs; Pleuritic chest pain>chest; Coughing blood>mouth; Fast pulse, low sats>heart',
  'Wells score>likely or unlikely; D-dimer>only if unlikely: normal rules it out; Leg ultrasound>DVT*; CTPA>PE*',
  'Start a DOAC while you wait, if no contraindication | Apixaban or rivaroxaban for at least 3 months | Provoked: 3 months; unprovoked: consider longer | Massive PE with shock: thrombolysis',
  'PE with low BP: massive>e; Right heart strain on echo or CT>e; Unprovoked clot: look for cancer clinically>u',
  'Virchow\'s triad: slow flow, damaged wall, sticky blood. Find which corner the patient sits in.')

N(14, 'Covid-19', 'lungs', 'both',
  'Coronavirus enters cells in the airway → inflammation spreads into the lungs → oxygen falls, sometimes with clots',
  'Older people · obesity, diabetes, immunosuppressed · unvaccinated',
  'Fever and new cough>lungs; Loss of smell or taste>nose; Breathless, low sats>chest; Tired, aches>all',
  'Lateral flow or PCR swab>confirms the virus*; Sats and NEWS2>how sick; Chest X-ray>patchy changes both sides',
  'Most: rest, fluids, paracetamol at home | Antivirals for high-risk adults in the community | Hospital, needing oxygen: dexamethasone, VTE prophylaxis | Worse: IL-6 blocker, CPAP or ICU',
  'Sats under 92% or falling>e; Breathless at rest>e; Long Covid symptoms over 12 weeks>r',
  'Silent hypoxia: sats can fall before the patient feels breathless. Measure, don\'t guess.')

N(15, 'Asthma', 'lungs', 'airway',
  'Allergic inflammation in the airways → they twitch and narrow → wheeze that comes and goes',
  'Children and young adults · eczema, hay fever · family history · NSAIDs, beta-blockers, cold, exercise',
  'Wheeze, worse at night and early morning>chest; Cough, especially at night>lungs; Tight chest>lchest; Triggered by cold, exercise, pets>all',
  'FeNO>raised: 50 or more in adults; Spirometry with reversibility>FEV1 rises 12% and 200 ml*; Peak flow diary>20% variability',
  'Low-dose ICS-formoterol as needed | Daily MART: ICS-formoterol morning and evening plus as needed | Moderate-dose MART | Then check FeNO and eosinophils, specialist add-ons',
  'Can\'t finish sentences, PEF under 50%>e; Silent chest, sats under 92%, exhausted: life-threatening>e; Reliever on 3 or more days a week, or waking at night: not controlled>u',
  'Inflammation is the fire, the reliever is the bucket. Treat the fire with a steroid inhaler.')

N(16, 'COPD', 'lungs', 'airway',
  'Smoke damages the airways and air sacs → air gets trapped → slowly worsening breathlessness that does not reverse',
  '35+ · smokers or ex-smokers · fumes, dust at work · alpha-1 antitrypsin if young',
  'Breathless on exertion>lungs; Daily productive cough>chest; Wheeze, frequent winter chest infections>lchest; Barrel chest, pursed lips>mouth',
  'Spirometry>FEV1 to FVC ratio under 0.7 after bronchodilator*; Chest X-ray>hyperinflation, rule out cancer; FBC>polycythaemia, anaemia; BMI and MRC score',
  'Stop smoking, vaccines, pulmonary rehab | SABA or SAMA as needed | LAMA plus LABA; add ICS if asthma features or high eosinophils | Oxygen if PaO2 under 7.3 and not smoking',
  'Exacerbation: oxygen 88 to 92%, nebulisers, prednisolone>s; Rising CO2 with pH under 7.35: NIV>e; Weight loss or haemoptysis: cancer>c',
  'Asthma swings and reverses; COPD only goes one way, slowly down.')

N(17, 'Bronchiectasis', 'lungs', 'airway',
  'Infection or poor clearance scars the airways → they widen permanently → mucus pools and keeps getting infected',
  'After severe childhood infection · cystic fibrosis · immune deficiency · ABPA',
  'Daily cough with lots of sputum>chest; Repeated chest infections>lungs; Coughing blood>mouth; Coarse crackles, clubbing>hands',
  'High-resolution CT>airway wider than the vessel beside it*; Sputum culture>Pseudomonas, H. influenzae; Immunoglobulins, CF tests>the cause',
  'Airway clearance physiotherapy daily | Antibiotics for flares, guided by sputum | Long-term macrolide if 3 or more flares a year | Vaccines, treat the cause',
  'Massive haemoptysis>e; Pseudomonas growing for the first time: eradicate>u; Breathless and low sats in a flare>s',
  'Wide pipes, stagnant mucus, endless infections. Clearance is the treatment, not just antibiotics.')

N(18, 'Acute bronchitis', 'lungs', 'airway',
  'A virus inflames the large airways → cough with or without phlegm → settles on its own in about 3 weeks',
  'Any age · winter · smokers',
  'Cough, maybe with phlegm>chest; Mild wheeze>lungs; Low-grade fever>all; Chest clear or scattered wheeze>lchest',
  'Clinical diagnosis>no tests needed in most*; CRP at the bedside>if unsure about pneumonia: under 20 means no antibiotic',
  'Explain it lasts about 3 weeks | Fluids, rest, paracetamol, honey | Antibiotic only if frail, other illness or CRP over 100 | Back-up script if CRP 20 to 100',
  'Breathless, fast breathing, focal crackles: pneumonia>s; Cough over 3 weeks in a smoker: X-ray>u; Coughing blood>u',
  'A virus with a long tail: the cough outlasts the infection.')

N(19, 'Pneumonia', 'lungs', 'alv',
  'Germs reach the air sacs → they fill with pus and fluid → that part of the lung stops swapping gas',
  'Older people, smokers · COPD, diabetes · in hospital 48 h or more: HAP',
  'Fever, cough with sputum>chest; Pleuritic chest pain>lchest; Fast breathing>lungs; Confusion in the elderly>head; Dull, crackles, bronchial breathing>lungs',
  'Chest X-ray>consolidation*; CURB-65>Confusion, Urea over 7, RR 30+, BP under 90 or 60, 65+; Bloods, sputum and blood cultures>bug and severity',
  'CURB-65 0 to 1: amoxicillin at home | 2: hospital, amoxicillin plus clarithromycin | 3 to 5: IV co-amoxiclav plus clarithromycin | Oxygen, fluids; repeat X-ray at 6 weeks if smoker or 50+',
  'Sepsis or CURB-65 3 or more>e; Empyema: fever not settling>s; Not clearing: hidden cancer>u',
  'CURB-65 tells you where the patient sleeps tonight: home, ward or intensive care.')

N(20, 'Tuberculosis', 'lungs', 'apex',
  'TB bacteria hide in the upper lobes → the immune system walls them off → they reactivate when defences drop',
  'Born in a high-TB country · HIV, homeless, prison · close contacts',
  'Cough over 3 weeks>chest; Night sweats>all; Weight loss>abdo; Coughing blood>mouth; Fever>head',
  'Chest X-ray>upper lobe shadowing or cavity; Sputum x 3>smear and culture for acid-fast bacilli*; PCR>fast confirmation and resistance; IGRA or Mantoux>latent TB',
  'RIPE for 2 months: rifampicin, isoniazid, pyrazinamide, ethambutol | Then rifampicin and isoniazid for 4 more months | Directly observed if adherence is a risk | Notify public health; trace contacts',
  'Rifampicin turns urine orange, reduces the pill>r; Isoniazid: neuropathy, give pyridoxine>r; Ethambutol: check vision>u; Liver tests on treatment>u',
  'RIPE: rifampicin = red urine, isoniazid = neuropathy, pyrazinamide = gout, ethambutol = eyes.')

N(21, 'Lung cancer', 'lungs', 'lung',
  'Smoking damages the airway lining → mutations build up → a tumour grows and spreads early',
  '40+ · smokers · asbestos · family history',
  'Cough that won\'t go>chest; Coughing blood>mouth; Weight loss>abdo; Hoarse voice>neck; Clubbing>hands',
  'Chest X-ray>first test; CT chest>staging; PET-CT>spread; Biopsy>small cell or non-small cell*',
  'Suspected cancer pathway | Surgery if early non-small cell | Radiotherapy and chemotherapy | Immunotherapy or targeted drugs by mutation',
  'Superior vena cava obstruction: swollen face and arms>e; High calcium from bone or PTH-like hormone>s; Spinal cord compression>e; Low sodium from SIADH in small cell>s',
  'Small cell is fast and makes hormones; non-small cell is slower and sometimes operable.')

N(22, 'Occupational and asbestos-related lung disease', 'lungs', 'pleura',
  'Dust breathed in at work → it scars the lungs or pleura → decades later the damage shows',
  'Builders, shipyard, plumbers: asbestos · miners: coal, silica · farmers: mouldy hay',
  'Breathless, worse over years>lungs; Dry cough>chest; Clubbing>hands; Chest pain with mesothelioma>lchest',
  'Occupational history>job by job, decades back*; Chest X-ray and CT>pleural plaques, fibrosis, mass; Biopsy>mesothelioma',
  'Remove exposure, stop smoking: it multiplies the risk | Pulmonary rehab, oxygen | Mesothelioma: oncology, palliative care | Compensation advice and coroner reporting',
  'One-sided effusion with chest pain in an ex-builder: mesothelioma>c; Lung cancer risk much higher with smoking>c',
  'Asbestos timeline: plaques are a marker, fibrosis is the damage, mesothelioma is the cancer, 30 years later.')

N(23, 'Fibrotic lung disease and hypersensitivity pneumonitis', 'lungs', 'base',
  'Repeated injury makes the lung lay down scar → the air sacs stiffen → oxygen can\'t cross',
  'IPF: 60+ men, smokers · EAA: birds, mouldy hay · drugs: amiodarone, methotrexate, nitrofurantoin',
  'Slowly worsening breathlessness>lungs; Dry cough>chest; Fine crackles at the bases like velcro>lungs; Clubbing>hands',
  'High-resolution CT>honeycombing at the bases*; Spirometry>restrictive: FVC low, ratio normal or high; Transfer factor>low; Bloods>autoimmune and precipitins',
  'Stop the exposure or the drug | IPF: antifibrotic pirfenidone or nintedanib | EAA: avoid antigen, steroids | Oxygen, rehab, transplant assessment',
  'Acute flare with sudden worsening>e; Falling oxygen at rest>s; Weight loss: check for cancer>u',
  'Velcro crackles at the bases plus clubbing = fibrosis. Upper zone = EAA or TB; lower zone = IPF.')
