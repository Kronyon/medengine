"""🧬 Set C: one patient, three questions, written in the official MSCAA style (vitals block, an Investigations table with
reference ranges, a decoy or two, and a comorbidity that blocks first line). For the ILO units the official papers never
asked about. Own words, UK guidance."""
Q = '''
@u 1
! Tearing pain to the back with unequal arm pressures is dissection until proven otherwise: CT angiography confirms it, and type A goes to theatre while type B gets BP control.
1L: A 64 year old man has sudden severe chest pain that tears through to his back between the shoulder blades. He has long-standing hypertension. His pulse rate is 104 bpm, BP 182/96 mmHg in the right arm and 148/80 mmHg in the left arm, and oxygen saturation 97% breathing air. There is an early diastolic murmur. Which is the most likely diagnosis?
> Acute pericarditis ; *Aortic dissection ; Oesophageal rupture ; Pulmonary embolism ; ST-elevation MI
= Tearing pain radiating to the back, a BP difference between the arms and new aortic regurgitation point to dissection of the ascending aorta.
~ Same pain with ST elevation in II, III and aVF and equal arm pressures → inferior STEMI.
2R: A 64 year old man has sudden tearing chest pain radiating to his back. His BP is 182/96 mmHg in the right arm and 148/80 mmHg in the left. His ECG shows sinus tachycardia only. His creatinine is normal. Which investigation is most likely to confirm the diagnosis?
$ Troponin T ; 0.012 µg/L ; <0.014
$ D-dimer ; 2.4 mg/L ; <0.5
$ Creatinine ; 88 µmol/L ; 60–120
> Chest X-ray ; *CT angiography of the aorta ; CT pulmonary angiogram ; Serial troponin at 3 hours ; Transthoracic echocardiogram
= CT angiography of the whole aorta is the test of choice in a stable patient. A raised D-dimer is expected and does not point to PE here; a normal X-ray does not exclude dissection.
~ Too unstable to leave the department → transoesophageal echo at the bedside or in theatre.
3D: A 70 year old woman has a type B aortic dissection confined to the descending aorta. She is alert with no limb or gut ischaemia. Her pulse rate is 96 bpm and BP 176/94 mmHg. She has asthma that needed admission to intensive care last year. Which is the most appropriate first drug to control her BP and heart rate?
> Intravenous glyceryl trinitrate ; Intravenous labetalol ; Oral amlodipine ; Oral ramipril ; *Intravenous verapamil
= Rate control comes first to cut the force on the aortic wall, usually with an IV beta-blocker such as labetalol. Severe asthma blocks beta-blockers, so a rate-limiting calcium channel blocker is used instead.
~ No asthma → IV labetalol, aiming for a heart rate under 60 and systolic BP of 100 to 120.

@u 14
! Covid-19 care is judged by oxygen: sats under 94% on air mean dexamethasone, normal sats mean none; and once dexamethasone starts, glucose needs watching.
1L: A 46 year old woman has 6 days of fever, dry cough, muscle aches and loss of smell. She is unvaccinated. Her temperature is 38.3°C, pulse rate 98 bpm, respiratory rate 24 breaths per minute and oxygen saturation 91% breathing air. Her chest X-ray shows bilateral peripheral patchy shadowing. Which is the most likely diagnosis?
> Bacterial lobar pneumonia ; *Covid-19 pneumonitis ; Influenza A ; Pulmonary embolism ; Viral bronchitis
= Anosmia, myalgia and bilateral peripheral ground-glass change in week 2 are typical of Covid-19 pneumonitis. Confirm with a PCR or lateral flow test.
~ High fever, rusty sputum and one lobe consolidated → bacterial lobar pneumonia.
2N: A 46 year old woman has Covid-19 confirmed on PCR. Her temperature is 38.0°C, pulse rate 96 bpm, respiratory rate 22 breaths per minute and oxygen saturation 92% breathing air. Which is the most appropriate additional treatment?
$ White cell count ; 5.1 × 10⁹/L ; 3.8–10.0
$ CRP ; 48 mg/L ; <5
$ Procalcitonin ; 0.08 µg/L ; <0.5
> Co-amoxiclav and clarithromycin ; *Dexamethasone 6 mg daily ; Inhaled budesonide ; Oral azithromycin ; Treatment-dose enoxaparin
= Needing oxygen with sats under 94% is the threshold for dexamethasone, which lowers mortality. A low procalcitonin argues against a bacterial co-infection, so antibiotics are not routine.
~ Sats 97% on air and well → no dexamethasone, supportive care.
3D: A 64 year old man with type 2 diabetes has Covid-19 pneumonitis needing oxygen. He takes metformin and gliclazide. Dexamethasone 6 mg daily is started. Which is the most important additional monitoring?
$ HbA1c ; 61 mmol/mol ; 20–42
$ Potassium ; 4.1 mmol/L ; 3.5–5.3
> Daily ECG ; Daily serum potassium ; *Capillary glucose before meals ; Weekly HbA1c ; Twice-daily blood cultures
= Dexamethasone raises glucose most in the afternoon and evening. Check capillary glucose regularly and adjust treatment, adding insulin if needed.
~ No diabetes → still check glucose daily while on steroids, as steroid-induced hyperglycaemia is common.

@u 18
! Acute cough is usually viral: CRP decides antibiotics in primary care, and focal signs or low sats turn bronchitis into suspected pneumonia.
1L: A 32 year old man has 10 days of cough with clear sputum after a cold. He is a non-smoker. His temperature is 37.4°C, pulse rate 82 bpm, respiratory rate 16 breaths per minute and oxygen saturation 98% breathing air. There are scattered wheezes but no focal crackles. Which is the most likely diagnosis?
> Asthma ; *Acute bronchitis ; Community-acquired pneumonia ; Pertussis ; Post-nasal drip
= A cough after a cold with normal vital signs and no focal chest signs is acute bronchitis, which usually lasts up to 3 weeks.
~ Paroxysms of cough ending in a whoop or vomiting → pertussis.
2N: A 32 year old man has 10 days of productive cough after a cold. He is well with normal observations and no focal chest signs. A point-of-care CRP is done in the surgery. Which is the most appropriate management?
$ CRP ; 18 mg/L ; <5
> *No antibiotic and safety-net advice ; Delayed amoxicillin prescription ; Oral doxycycline for 5 days ; Chest X-ray within 48 hours ; Oral prednisolone for 5 days
= NICE: CRP under 20 means no antibiotic; 20 to 100, consider a back-up prescription; over 100, give an antibiotic.
~ CRP 72 → consider a back-up prescription.
3D: A 79 year old woman with heart failure has 6 days of productive cough. She is breathless but alert. Her temperature is 37.8°C, pulse rate 96 bpm and oxygen saturation 95% breathing air. There are no focal crackles. She is allergic to penicillin. Which is the most appropriate treatment?
> Oral amoxicillin ; *Oral doxycycline ; Oral ciprofloxacin ; Oral prednisolone ; No antibiotic needed
= Older people with significant comorbidity, such as heart failure, are at higher risk, so an antibiotic is reasonable. Doxycycline is first line, and penicillin allergy blocks amoxicillin.
~ Pregnant and allergic to penicillin → clarithromycin or erythromycin.

@u 27
! Malabsorption is pinned by what is low: B12 points at the terminal ileum, iron and folate at the duodenum and jejunum, and steatorrhoea with a low faecal elastase at the pancreas.
1L: A 56 year old man who drinks heavily has pale, bulky stools that are hard to flush and has lost 6 kg. He has had several attacks of epigastric pain over the years. His HbA1c is 54 mmol/mol. Which is the most likely diagnosis?
> Coeliac disease ; *Chronic pancreatitis ; Crohn's disease ; Small bowel bacterial overgrowth ; Whipple's disease
= Alcohol, recurrent pain, steatorrhoea and new diabetes point to loss of both exocrine and endocrine pancreas.
~ Same stools in a young woman with iron deficiency and blistering itchy elbows → coeliac disease.
2N: A 56 year old man who drinks heavily has steatorrhoea and weight loss. Which investigation result best confirms pancreatic exocrine insufficiency?
$ Faecal elastase ; 62 µg/g ; >200
$ Tissue transglutaminase IgA ; 2 U/mL ; <7
$ Faecal calprotectin ; 38 µg/g ; <50
> Coeliac serology ; *Faecal elastase ; Faecal calprotectin ; Serum amylase ; Stool culture
= A faecal elastase under 100 µg/g shows severe exocrine failure. Amylase is often normal in chronic pancreatitis because little tissue is left.
~ Faecal calprotectin of 600 → inflammation, colonoscopy for IBD.
3D: A 56 year old man has chronic pancreatitis with steatorrhoea. He has stopped drinking. Which is the most appropriate treatment for his steatorrhoea?
> Low-fat diet ; Loperamide ; *Pancreatic enzymes with meals ; Proton pump inhibitor ; Cholestyramine
= Pancreatin taken with meals and snacks replaces the missing enzymes. A PPI can be added if the response is poor, as acid inactivates them.
~ Diarrhoea after a terminal ileal resection → cholestyramine for bile acid diarrhoea.

@u 29
! IBS is a positive diagnosis once red flags are absent: calprotectin and coeliac serology are the tests, and in a woman over 50 with new symptoms CA-125 comes first.
1L: A 27 year old woman has 9 months of abdominal pain relieved by opening her bowels, bloating and alternating loose and hard stools. She has not lost weight and has no rectal bleeding. Examination is normal. Which is the most likely diagnosis?
> Coeliac disease ; Crohn's disease ; Endometriosis ; *Irritable bowel syndrome ; Ovarian cancer
= Pain linked to defaecation, bloating and change in stool form for over 6 months with no red flags fits IBS.
~ Same pain with weight loss, mouth ulcers and a high calprotectin → Crohn's disease.
2N: A 27 year old woman has symptoms of IBS with no red flags. Her GP sends blood and stool tests. What do these results mean?
$ Haemoglobin ; 128 g/L ; 115–150
$ CRP ; 3 mg/L ; <5
$ Tissue transglutaminase IgA ; 1 U/mL ; <7
$ Faecal calprotectin ; 32 µg/g ; <50
> *These results support IBS ; Colonoscopy is needed ; Repeat calprotectin in 6 weeks ; Stool culture is needed ; Ultrasound is needed
= NICE: FBC, ESR or CRP, coeliac serology and faecal calprotectin. All are normal here, so IBS can be diagnosed without endoscopy.
~ Calprotectin 260 → refer for colonoscopy.
3R: A 58 year old woman has 2 months of new bloating, early fullness and looser stools. She has never had bowel problems. Examination is normal. Which is the most appropriate first investigation?
> Colonoscopy ; *Serum CA-125 ; Faecal calprotectin ; Coeliac serology ; Trial of mebeverine
= New IBS-like symptoms in a woman over 50 suggest ovarian cancer until proven otherwise. A CA-125 of 35 or more leads to an urgent pelvic ultrasound.
~ Same symptoms at 27 for years → IBS work-up.

@u 30
! A hiatus hernia that slides causes reflux and is treated with PPIs; one that rolls can twist, so vomiting and pain with an air-fluid level behind the heart is a surgical emergency.
1L: A 66 year old woman has had heartburn for years. She now has chest pain and retching but brings nothing up, and cannot pass a nasogastric tube. Her pulse rate is 112 bpm and BP 104/70 mmHg. Her chest X-ray shows an air-fluid level behind the heart. Which is the most likely diagnosis?
> Achalasia ; Boerhaave syndrome ; Inferior MI ; *Gastric volvulus ; Sliding hiatus hernia
= Pain, unproductive retching and failure to pass an NG tube is Borchardt's triad of gastric volvulus, often in a large rolling hiatus hernia.
~ Same air behind the heart with surgical emphysema after violent vomiting → Boerhaave syndrome.
2R: A 66 year old woman has a large rolling hiatus hernia with acute gastric volvulus. She is tachycardic. Which is the most appropriate next investigation?
$ Lactate ; 3.6 mmol/L ; <2.0
$ White cell count ; 15.2 × 10⁹/L ; 3.8–10.0
> Barium swallow ; *CT chest and abdomen with contrast ; Oesophageal manometry ; Plain abdominal X-ray ; Upper GI endoscopy first
= CT shows the twist and any ischaemia quickly. A rising lactate suggests the stomach is compromised and needs urgent surgery.
~ Stable woman with reflux and a small sliding hernia → no imaging; PPI and lifestyle.
3D: A 52 year old man has reflux from a small sliding hiatus hernia. He takes clopidogrel after a coronary stent. Which is the most appropriate PPI?
> Esomeprazole ; *Lansoprazole ; Omeprazole ; Ranitidine ; Sucralfate
= Omeprazole and esomeprazole reduce clopidogrel activation, so the MHRA advises avoiding them. Lansoprazole or pantoprazole are used instead.
~ No clopidogrel → any PPI, omeprazole is fine.

@u 34
! A perianal abscess is drained, not treated with antibiotics; a fistula that will not heal is mapped with MRI; recurrent or complex fistulas in a young person mean think Crohn's.
1L: A 34 year old man has 3 days of throbbing pain beside his anus that keeps him awake. His temperature is 38.1°C. There is a tender, fluctuant, red swelling 2 cm from the anal margin. Which is the most likely diagnosis?
> Anal fissure ; Pilonidal abscess ; *Perianal abscess ; Thrombosed external haemorrhoid ; Anal cancer
= A hot, tender fluctuant swelling beside the anus with fever is a perianal abscess from an infected anal gland.
~ Sudden painful blue lump at the margin with no fever → thrombosed external haemorrhoid.
2R: A 34 year old man has a perianal abscess. He is otherwise well. Which is the most appropriate management?
$ White cell count ; 13.1 × 10⁹/L ; 3.8–10.0
$ CRP ; 64 mg/L ; <5
$ Glucose ; 5.2 mmol/L ; 3.0–6.0
> Oral co-amoxiclav for 7 days ; *Incision and drainage under anaesthetic ; MRI pelvis before any surgery ; Seton insertion ; Topical diltiazem
= Pus needs drainage. Antibiotics alone do not work and are added only for cellulitis, diabetes or immunosuppression.
~ Discharge from a skin opening for months after drainage → fistula, MRI pelvis.
3T: A 22 year old woman has her third perianal abscess in a year, with two discharging openings. She has had loose stools and weight loss. Which is the most important underlying diagnosis to look for?
> Diabetes mellitus ; *Crohn's disease ; Hidradenitis suppurativa ; HIV infection ; Ulcerative colitis
= Complex or recurrent fistulas with bowel symptoms point to Crohn's disease. Check calprotectin and arrange ileocolonoscopy.
~ Same openings in both groins and armpits → hidradenitis suppurativa.

@u 35
! Haemorrhoids are graded by prolapse: 1 and 2 are banded, 3 and 4 or banding failure go to surgery; a change in bowel habit over 50 means looking higher before blaming them.
1L: A 41 year old man has bright red blood on the paper after opening his bowels for 3 weeks. There is no pain. Proctoscopy shows swellings above the dentate line that prolapse on straining and go back by themselves. Which is the most likely diagnosis?
> Anal fissure ; *Second-degree haemorrhoids ; Fourth-degree haemorrhoids ; Rectal polyp ; Rectal prolapse
= Haemorrhoids that prolapse and reduce on their own are second degree. Painless bright red bleeding is typical.
~ They prolapse and must be pushed back by hand → third degree.
2N: A 63 year old woman has bright red rectal bleeding and haemorrhoids on proctoscopy. She has had looser stools for 2 months and feels tired. Which is the most appropriate next step?
$ Haemoglobin ; 102 g/L ; 115–150
$ MCV ; 74 fL ; 80–96
$ Ferritin ; 9 µg/L ; 30–400
> Band the haemorrhoids ; *FIT and suspected cancer referral ; Fibre and fluids, review in 3 months ; Iron tablets and reassure ; Topical anaesthetic cream
= Iron deficiency anaemia and a change in bowel habit over 60 need a cancer pathway referral, whatever the proctoscopy shows.
~ A 30-year-old with normal blood count and no habit change → treat the haemorrhoids.
3D: A 45 year old man has second-degree haemorrhoids that still bleed despite fibre. He takes warfarin for a mechanical mitral valve. Which is the most appropriate next step?
> Stop warfarin for a week, then band ; *Specialist review before banding ; Haemorrhoidectomy this week ; Oral tranexamic acid ; Switch to apixaban
= Banding on anticoagulation carries a risk of delayed heavy bleeding, and warfarin for a mechanical valve cannot simply be stopped. A specialist plans bridging or another treatment.
~ No anticoagulant → rubber band ligation in clinic.

@u 36
! A fissure lies in the midline and hurts on defaecation; one that is lateral or will not heal needs a look for Crohn's, TB, HIV, syphilis or cancer.
1L: A 29 year old woman has severe tearing pain on opening her bowels for 3 weeks, lasting an hour afterwards, with a streak of bright blood. Gentle parting of the buttocks shows a split in the posterior midline. Which is the most likely diagnosis?
> *Anal fissure ; Fistula in ano ; Perianal haematoma ; Pruritus ani ; Second-degree haemorrhoids
= A posterior midline split with pain on and after defaecation is an anal fissure. Most are posterior; anterior ones are more common after childbirth.
~ A painful tender lump with a discharging opening → fistula in ano.
2T: A 31 year old man has a painless fissure on the lateral side of the anus that has not healed for 3 months. He has had diarrhoea and mouth ulcers. Which is the most likely underlying diagnosis?
> Anal cancer ; *Crohn's disease ; Haemorrhoids ; Syphilis ; Ulcerative colitis
= Fissures off the midline, painless or slow to heal suggest a secondary cause, most often Crohn's disease. Check calprotectin and refer.
~ Painful posterior midline fissure in a constipated adult → primary fissure, treat locally.
3D: A 34 year old woman has a chronic anal fissure for 8 weeks. She has frequent migraines with aura. Which is the most appropriate first treatment?
> Botulinum toxin injection ; Glyceryl trinitrate ointment ; Lateral sphincterotomy ; *Topical diltiazem ; Oral metronidazole
= GTN ointment is first line but commonly causes severe headaches, so with troublesome migraine topical diltiazem, used off label, is a sensible first choice.
~ No headache history → topical GTN for 8 weeks.

@u 38
! Lower GI bleeding is triaged with the shock index: stable bleeds are investigated as outpatients or by colonoscopy; unstable ones get CT angiography and the anticoagulant is reversed.
1L: A 79 year old woman with known diverticular disease passes a large volume of maroon and fresh red blood with clots. She has no abdominal pain. Her pulse rate is 96 bpm and BP 118/72 mmHg. Which is the most likely cause?
> Angiodysplasia ; Colorectal cancer ; *Diverticular bleed ; Haemorrhoids ; Ischaemic colitis
= A sudden, painless, large bleed in an older person with diverticula is a diverticular bleed. Most stop by themselves.
~ Left-sided pain first, then bloody diarrhoea in a vasculopath → ischaemic colitis.
2N: A 79 year old woman is passing fresh blood rectally. What is her shock index?
$ Pulse rate ; 120 bpm ; 60–100
$ Systolic BP ; 96 mmHg ; 100–140
$ Haemoglobin ; 92 g/L ; 115–150
$ Urea ; 6.1 mmol/L ; 2.5–7.8
> 0.8 ; 1.0 ; *1.25 ; 1.5 ; 2.0
= Shock index is heart rate divided by systolic BP: 120 ÷ 96. Over 1 means an unstable bleed: resuscitate and arrange CT angiography. A normal urea fits a lower rather than upper GI source.
~ Pulse 80 and systolic 128 → 0.63, stable: colonoscopy on the next list.
3D: A 79 year old woman with an unstable lower GI bleed takes apixaban for AF. She has had no dose for 6 hours. Which is the most appropriate additional treatment?
> Continue apixaban ; Fresh frozen plasma ; *Andexanet alfa or PCC ; Intravenous vitamin K ; Protamine sulfate
= Stop apixaban and, for life-threatening bleeding, reverse it with andexanet alfa or prothrombin complex concentrate as per local policy. Vitamin K reverses warfarin; protamine reverses heparin.
~ On warfarin with INR 3.4 → IV vitamin K and PCC.

@u 42
! Charcot's triad means cholangitis: antibiotics and fluids now, ultrasound for the duct, and ERCP within 24 to 48 hours; it becomes urgent when sepsis does not settle.
1L: A 74 year old woman has fever with rigors, right upper quadrant pain and yellow eyes for 2 days. Her temperature is 39.1°C, pulse rate 112 bpm and BP 104/62 mmHg. Which is the most likely diagnosis?
> Acute cholecystitis ; *Ascending cholangitis ; Acute hepatitis ; Liver abscess ; Pancreatic cancer
= Fever, jaundice and RUQ pain is Charcot's triad. Add confusion and hypotension and it is Reynolds' pentad.
~ Painless jaundice with weight loss and a palpable gallbladder → pancreatic cancer.
2N: A 74 year old woman has ascending cholangitis. Which result best shows the obstruction?
$ White cell count ; 17.6 × 10⁹/L ; 3.8–10.0
$ Bilirubin ; 86 µmol/L ; <17
$ ALT ; 140 IU/L ; 10–50
$ ALP ; 520 IU/L ; 25–115
$ Amylase ; 240 U/L ; <220
> ALT 140 ; *ALP 520 with bilirubin 86 ; Amylase 240 ; White cell count 17.6 ; Normal albumin
= An ALP far higher than ALT, with jaundice, is the cholestatic pattern of a blocked duct. The amylase is a decoy, under 3 times the limit.
~ ALT 1,500 with ALP 140 → hepatitic pattern, think viral or drug cause.
3R: A 74 year old woman with cholangitis has had IV antibiotics and fluids for 12 hours. Her BP is now 88/50 mmHg and she is more confused. Ultrasound shows a dilated common bile duct. Which is the most appropriate next step?
> Continue antibiotics, ERCP next week ; Laparoscopic cholecystectomy now ; MRCP to confirm the stone ; Percutaneous liver biopsy ; *Urgent ERCP to drain the duct
= Cholangitis that does not respond to antibiotics needs urgent biliary drainage, usually ERCP. Percutaneous drainage is the fallback if ERCP is not possible.
~ Settles quickly on antibiotics → ERCP within 72 hours on the next list.

@u 47
! PID is treated on suspicion: swabs then antibiotics without waiting; pregnancy is excluded first; an IUD can stay unless she is not improving.
1L: A 22 year old woman has 4 days of lower abdominal pain, deep pain during sex and new vaginal discharge. Her temperature is 38.0°C. There is cervical motion tenderness and bilateral adnexal tenderness. Her pregnancy test is negative. Which is the most likely diagnosis?
> Acute appendicitis ; Ectopic pregnancy ; Endometriosis ; Ovarian torsion ; *Pelvic inflammatory disease
= Lower abdominal pain with cervical motion and adnexal tenderness in a sexually active woman is PID until proven otherwise.
~ Positive pregnancy test with one-sided pain → ectopic pregnancy.
2R: A 22 year old woman has suspected PID. She is well enough to be treated at home. Which is the most appropriate approach?
$ Pregnancy test ; negative ;
$ White cell count ; 11.8 × 10⁹/L ; 3.8–10.0
$ CRP ; 46 mg/L ; <5
> Await NAAT results before treatment ; *Swabs, then antibiotics the same day ; Pelvic ultrasound before treatment ; Laparoscopy to confirm ; Treat her partner and not her
= Delaying treatment raises the risk of infertility and ectopic pregnancy. Take NAATs for chlamydia and gonorrhoea, then start ceftriaxone, doxycycline and metronidazole.
~ Unwell with a fever of 39 and a pelvic mass → admit for IV treatment and ultrasound.
3D: A 22 year old woman has PID and is allergic to cephalosporins. Which is the most appropriate regimen?
> Ceftriaxone, doxycycline and metronidazole ; *Ofloxacin and metronidazole ; Oral co-amoxiclav ; Single dose of azithromycin ; Nitrofurantoin and doxycycline
= BASHH gives oral ofloxacin with metronidazole for 14 days as an alternative when ceftriaxone cannot be used. It is avoided if gonorrhoea is likely, as resistance is common.
~ No allergy → IM ceftriaxone, then doxycycline and metronidazole for 14 days.

@u 54
! Lactational mastitis is treated while feeding continues; an abscess is aspirated under ultrasound; and a red breast that does not respond in a woman who is not feeding is inflammatory cancer until proven otherwise.
1L: A 28 year old woman is breastfeeding her 4 week old baby. She has a painful, red, wedge-shaped area on her left breast and feels flu-like. Her temperature is 38.4°C. There is no fluctuant mass. Which is the most likely diagnosis?
> Breast abscess ; Galactocele ; Inflammatory breast cancer ; *Lactational mastitis ; Periductal mastitis
= A tender red wedge with fever while breastfeeding is mastitis, usually from milk stasis with or without infection.
~ A tender fluctuant lump that persists despite antibiotics → abscess.
2R: A 28 year old breastfeeding woman has been on flucloxacillin for mastitis for 4 days. She still has a fever and now has a tender fluctuant swelling. Which is the most appropriate next step?
$ White cell count ; 14.8 × 10⁹/L ; 3.8–10.0
$ CRP ; 96 mg/L ; <5
> Change to co-amoxiclav and review in a week ; *Ultrasound with needle aspiration ; Mammogram ; Stop breastfeeding from that side ; Core biopsy of the mass
= A collection needs ultrasound-guided aspiration, repeated if needed. Feeding or expressing continues from both breasts.
~ No fluctuance and improving on antibiotics → complete the course and keep feeding.
3D: A 28 year old breastfeeding woman has mastitis. She is allergic to penicillin with a rash. Which antibiotic is most appropriate?
> Amoxicillin ; Ciprofloxacin ; *Clarithromycin ; Flucloxacillin ; Tetracycline
= Clarithromycin or erythromycin covers Staph aureus if penicillin allergic and is compatible with breastfeeding. Tetracyclines and quinolones are avoided.
~ No allergy → flucloxacillin for 10 to 14 days.

@u 56
! Every breast lump goes through triple assessment; a lump after trauma may be fat necrosis, but it still needs a core biopsy because it can mimic cancer.
1L: A 52 year old woman has a firm, irregular lump in her right breast 6 weeks after a seatbelt injury in a car crash. There is some skin tethering over it. Which is the most likely diagnosis?
> Breast abscess ; Breast cyst ; *Fat necrosis ; Fibroadenoma ; Lipoma
= Fat necrosis follows trauma or surgery and can be hard, irregular and tethered. It mimics cancer on examination and imaging.
~ A soft, mobile, doughy lump with fatty imaging → lipoma.
2R: A 52 year old woman has a hard breast lump after trauma, likely fat necrosis. Which is the most appropriate next step?
> Reassure and discharge ; Review in 3 months ; *Triple assessment with core biopsy ; Excision without imaging ; Fine needle aspiration of the lump
= Fat necrosis cannot be told from cancer by examination alone, so triple assessment with imaging and core biopsy is needed.
~ Core biopsy confirms fat necrosis → reassure, no excision needed.
3T: A 55 year old woman has a smooth, mobile, 7 cm breast mass that has grown quickly over 2 months. Core biopsy shows leaf-like stroma with high cellularity. Which is the most appropriate treatment?
> Watch and rescan in 6 months ; Tamoxifen for 5 years ; *Wide local excision with clear margins ; Adjuvant breast radiotherapy ; Enucleation of the lump
= A phyllodes tumour needs wide local excision because it recurs if margins are close. Malignant ones can spread by blood.
~ A 2 cm fibroadenoma in a 20-year-old → reassure, no routine excision.

@u 58
! A groin lump is placed by the pubic tubercle: above and medial is inguinal, below and lateral is femoral. Femoral hernias strangulate, so they are repaired urgently.
1L: A 74 year old woman has a tender, irreducible lump in her right groin for 12 hours with vomiting. The lump is below and lateral to the pubic tubercle. Her pulse rate is 108 bpm. Which is the most likely diagnosis?
> Direct inguinal hernia ; *Strangulated femoral hernia ; Inguinal lymph node ; Psoas abscess ; Saphena varix
= A tender irreducible lump below and lateral to the pubic tubercle in an older woman with obstruction is a femoral hernia, which often strangulates.
~ Soft lump that disappears on lying down with a fluid thrill on coughing → saphena varix.
2N: A 74 year old woman has an irreducible femoral hernia with vomiting. Which result most suggests the bowel is compromised?
$ White cell count ; 16.2 × 10⁹/L ; 3.8–10.0
$ CRP ; 22 mg/L ; <5
$ Lactate ; 4.1 mmol/L ; <2.0
$ Amylase ; 260 U/L ; <220
> Amylase 260 ; CRP 22 ; *Lactate 4.1 ; Tender lump ; Vomiting
= A rising lactate signals ischaemic bowel and needs emergency surgery. The slightly raised amylase is a decoy seen in many obstructions.
~ Lactate 1.2 and a soft reducible lump → elective repair soon.
3R: A 35 year old man has a reducible inguinal hernia that causes him minimal discomfort. He wants to know the next step. Which is the most appropriate management?
> Emergency repair ; *Watchful waiting or elective repair ; Fit a truss and discharge ; Urgent CT abdomen ; Ultrasound every 6 months
= Minimally symptomatic inguinal hernias in men can be watched or repaired electively. Many go on to need repair.
~ Femoral hernia of the same size → offer repair soon because of strangulation risk.

@u 59
! Aneurysms are measured, then watched or repaired by size: popliteal ones thrombose rather than rupture, and finding one means scanning the aorta and the other leg.
1L: A 69 year old man has a pulsatile, expansile swelling behind his left knee found at a check-up. He smokes. Which is the most likely diagnosis?
> Baker's cyst ; Deep vein thrombosis ; Lipoma ; *Popliteal artery aneurysm ; Sarcoma
= An expansile pulsation in the popliteal fossa is an aneurysm, the commonest peripheral aneurysm.
~ Non-pulsatile soft swelling in an arthritic knee → Baker's cyst.
2R: A 69 year old man has a 2.6 cm popliteal aneurysm. Which other investigation is most important?
> Carotid artery duplex ; Transthoracic echocardiogram ; *Ultrasound of the abdominal aorta ; Renal tract ultrasound ; Lower limb venous duplex
= Up to half have an abdominal aortic aneurysm and many have one in the other leg, so both are scanned.
~ AAA found first → scan both popliteal arteries.
3N: A 72 year old man has an abdominal aortic aneurysm on surveillance. He has no abdominal or back pain. Which is the most appropriate management?
$ Aortic diameter 12 months ago ; 4.6 cm ;
$ Aortic diameter today ; 5.3 cm ;
> Discharge from surveillance ; Repeat scan in 12 months ; *Repeat scan in 3 months ; Refer for repair within 2 weeks ; Start a beta-blocker
= 4.5 to 5.4 cm is scanned every 3 months. Referral comes at 5.5 cm, growth over 1 cm a year, or symptoms. This grew 0.7 cm, under the threshold.
~ Diameter 5.5 cm, or 4.6 to 5.7 cm in a year → refer to vascular surgery within 2 weeks.

@u 60
! Acute limb ischaemia is the 6 Ps: an embolus from AF strikes a healthy limb suddenly; heparin starts while the surgeon decides, and paralysis means hours count.
1L: A 78 year old woman with AF not on anticoagulation has a suddenly painful, cold, white right leg for 3 hours. She has no history of claudication. The foot pulses are absent; the left leg pulses are normal. Which is the most likely cause?
> Acute DVT ; *Arterial embolus ; In-situ thrombosis ; Popliteal aneurysm rupture ; Spinal stenosis
= Sudden ischaemia in a previously normal leg with a normal other side and AF suggests an embolus. Thrombosis usually happens on a background of claudication.
~ Years of claudication and weak pulses in both legs → thrombosis in situ.
2T: A 78 year old woman has acute limb ischaemia. Her foot is cold with loss of sensation in the toes and mild weakness of dorsiflexion. Which category is this?
> Category I viable ; Category IIa marginally threatened ; *Category IIb immediately threatened ; Category III irreversible ; Chronic ischaemia
= Sensory loss beyond the toes with mild to moderate weakness is IIb: it needs revascularisation now.
~ Fixed mottling with paralysis → irreversible, amputation or palliation.
3D: A 78 year old woman has acute limb ischaemia from an embolus. She had a large haemorrhagic stroke 3 weeks ago. Which is the most appropriate treatment?
> Catheter-directed thrombolysis ; *Surgical embolectomy ; IV alteplase ; Oral apixaban and review ; Watchful waiting
= Recent haemorrhagic stroke blocks thrombolysis. Surgical embolectomy under local anaesthetic removes the clot.
~ No bleeding risk and a long distal clot → catheter-directed thrombolysis is an option.

@u 65
! Swelling that pits early and later does not, with Stemmer's sign, is lymphoedema; after cancer, recurrence is excluded first; cellulitis in the limb is treated early.
1L: A 61 year old woman has a swollen right arm 2 years after mastectomy with axillary clearance and radiotherapy. The skin is thickened and she cannot pinch the skin on the back of her fingers. Which is the most likely diagnosis?
> Axillary vein thrombosis ; Cellulitis ; *Secondary lymphoedema ; Lipoedema ; Recurrent breast cancer
= Lymphoedema follows node removal and radiotherapy. A positive Stemmer's sign, being unable to pinch the skin of the digits, supports it.
~ Sudden painful swelling with dilated veins over the shoulder → axillary vein thrombosis.
2R: A 61 year old woman has new arm lymphoedema 2 years after breast cancer surgery. It developed over 6 weeks. Which is the most appropriate next step?
> Compression sleeve and review in a year ; *Breast clinic review for recurrence ; Diuretic trial ; Lymphoscintigraphy first ; Reassure
= New or worsening lymphoedema after cancer can mean axillary recurrence, so the team reassesses before starting long-term compression.
~ Stable swelling for 5 years with no new signs → lymphoedema clinic for compression and skin care.
3D: A 61 year old woman with arm lymphoedema has a hot, red, tender arm and a fever of 38.2°C. She is allergic to penicillin. Which is the most appropriate treatment?
> Ciprofloxacin ; *Clarithromycin ; Flucloxacillin ; Furosemide ; Compression bandaging
= Cellulitis in lymphoedema is usually streptococcal. The British Lymphology Society advises clarithromycin or erythromycin if penicillin allergic, and stopping compression until it settles.
~ No allergy → amoxicillin, with flucloxacillin added if Staph is suspected.

@u 66
! Raynaud's is primary in young women with no other features; ulcers, onset after 30 or tight skin mean a connective tissue disease; beta-blockers make it worse.
1L: A 38 year old woman has fingers that turn white then blue in the cold, with tight shiny skin over her fingers and difficulty swallowing. Which is the most likely underlying diagnosis?
> Primary Raynaud's ; Rheumatoid arthritis ; *Systemic sclerosis ; Systemic lupus erythematosus ; Thoracic outlet syndrome
= Raynaud's with sclerodactyly and oesophageal dysmotility suggests limited systemic sclerosis, with anti-centromere antibodies.
~ Raynaud's with a malar rash, ulcers in the mouth and joint pain → lupus.
2N: A 38 year old woman has Raynaud's with tight skin on her fingers. Which antibody result is most likely?
$ Antinuclear antibody ; positive 1:640 ; <1:80
$ Anti-centromere antibody ; positive ;
$ Anti-dsDNA ; 8 IU/mL ; <30
$ Rheumatoid factor ; 12 IU/mL ; <20
> Anti-dsDNA positive ; *Anti-centromere positive ; Anti-Jo-1 positive ; Rheumatoid factor positive ; Anti-Ro positive
= Anti-centromere fits limited cutaneous systemic sclerosis. The anti-dsDNA and RF here are within range, decoys.
~ Lung fibrosis and skin thickening up the arms → anti-Scl-70.
3D: A 56 year old man with hypertension has worse Raynaud's since a new tablet was added. Which drug is most likely to blame?
> Amlodipine ; *Bisoprolol ; Doxazosin ; Losartan ; Ramipril
= Beta-blockers cause peripheral vasoconstriction and worsen Raynaud's. Amlodipine helps it.
~ Raynaud's that limits daily life → modified-release nifedipine.
'''
