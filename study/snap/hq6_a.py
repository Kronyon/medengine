"""v3.6.2 Hammer set E, part 1 of 3: paper-style SBAs written fresh around core FFP AKT topics.

Same format as hq5_data.py, plus a head for targets that are not ILO units:
    @u 74 2T             ILO unit index, hammer level, pattern letter
    @k b:hepatitis 2L    any other target (b: off-map topic, d: drug group, x: test or procedure)
"""

Q = r"""
@u 74 2T
s: A 46 year old woman had a total thyroidectomy for a multinodular goitre yesterday. Today her voice is hoarse and breathy and her cough is weak. She has no tingling around her mouth and the wound is flat and dry. // Pulse rate 84 bpm, BP 126/80 mmHg, oxygen saturation 97% breathing air. Flexible nasendoscopy shows the left vocal cord fixed close to the midline.
$ Adjusted calcium ; 2.31 mmol/L ; 2.20–2.60
? Which is the most likely cause of her voice change?
> External branch of superior laryngeal nerve injury ; Hypocalcaemia from parathyroid injury ; Laryngeal oedema from intubation ; Neck haematoma ; *Recurrent laryngeal nerve injury
= The recurrent laryngeal nerve supplies every intrinsic muscle of the larynx except cricothyroid. Injury paralyses the cord on that side close to the midline, so the voice is hoarse and breathy and the cough is weak. It is the complication patients are warned about before thyroid surgery.
~ Voice tires and cannot reach high notes but both cords move → external branch of the superior laryngeal nerve.
c: hoarse and breathy | cough is weak | left vocal cord fixed close to the midline | Adjusted calcium 2.31
m: The recurrent laryngeal nerve runs beside the inferior thyroid artery, and stretch or division leaves the cord paralysed near the midline
g: Hoarse voice and weak cough with a fixed cord after thyroidectomy is recurrent laryngeal nerve injury
f: perioral tingling and an adjusted calcium of 1.85 on day 1 => Hypocalcaemia from parathyroid injury
f: a rapidly swelling tense neck and stridor 4 hours after surgery => Neck haematoma
f: a voice that tires and cannot reach high notes with both cords moving => External branch of superior laryngeal nerve injury
x: External branch of superior laryngeal nerve injury => Weakens cricothyroid, so pitch and stamina suffer, but the cords move and the cough is strong
x: Hypocalcaemia from parathyroid injury => Her calcium is normal and she has no tingling or cramps
x: Laryngeal oedema from intubation => Gives a hoarse voice that settles over a day or two with both cords moving
x: Neck haematoma => The wound is flat and dry; a haematoma causes swelling and stridor, not one fixed cord

@u 36 2R
s: A 34 year old man has had pain on opening his bowels for 9 weeks, like passing broken glass, with bright red blood on the paper. He has used a bulk-forming laxative and lidocaine ointment for 6 weeks with little change. // Gentle parting of the buttocks shows a longitudinal tear in the posterior midline with a skin tag at its lower end.
? Which is the most appropriate treatment?
> Haemorrhoidal rubber band ligation ; Lateral internal sphincterotomy ; Oral metronidazole ; Topical hydrocortisone ; *Topical glyceryl trinitrate
= A fissure present for more than 6 weeks is chronic. NICE advises topical glyceryl trinitrate 0.4% twice a day for 6 to 8 weeks, alongside the laxative, to relax the internal sphincter and let the tear heal. Surgery is kept for fissures that fail medical treatment.
~ Fissure for 10 days → stool softeners and a short course of topical lidocaine; GTN is for chronic fissures.
c: 9 weeks | lidocaine ointment for 6 weeks | posterior midline | skin tag
m: Sphincter spasm cuts blood flow to the posterior midline, so the tear cannot heal until the sphincter relaxes
g: Fissure beyond 6 weeks despite laxatives → topical GTN
f: failure of 8 weeks of GTN followed by diltiazem ointment => Lateral internal sphincterotomy
f: painless bright red bleeding with a lump that prolapses and reduces itself => Haemorrhoidal rubber band ligation
x: Haemorrhoidal rubber band ligation => Treats internal haemorrhoids, which bleed painlessly, not a tear in the anoderm
x: Lateral internal sphincterotomy => Effective but risks incontinence, so it follows failed medical treatment
x: Oral metronidazole => Used for perianal sepsis, and he has no abscess or fistula
x: Topical hydrocortisone => Soothes itching but does not relax the sphincter or heal a chronic fissure

@u 48 1L
s: An 82 year old man in a nursing home has had increasing abdominal distension and no bowel movement or flatus for 3 days. He has long-standing constipation and Parkinson's disease. His abdomen is hugely distended, tympanic and only mildly tender. // Pulse rate 96 bpm, BP 132/78 mmHg. An abdominal X-ray shows a large dilated loop of bowel shaped like an inverted U, rising from the left iliac fossa towards the right upper quadrant.
? Which is the most likely diagnosis?
> Caecal volvulus ; Colonic pseudo-obstruction ; Obstructing sigmoid carcinoma ; *Sigmoid volvulus ; Toxic megacolon
= An elderly, constipated man with gross distension and a coffee bean loop rising from the left iliac fossa has a sigmoid volvulus: the sigmoid twists on its long mesentery. Without signs of ischaemia it is decompressed with flexible sigmoidoscopy and a flatus tube.
~ The dilated loop starts in the right iliac fossa and points to the left upper quadrant → caecal volvulus.
c: nursing home | Parkinson's disease | hugely distended | inverted U | left iliac fossa
m: A long redundant sigmoid mesentery lets the loop twist, closing both ends so gas cannot escape
g: Coffee bean loop from the left iliac fossa in a constipated elderly patient → sigmoid volvulus
f: a dilated loop from the right iliac fossa pointing to the left upper quadrant => Caecal volvulus
f: the whole colon dilated with no transition point after a hip operation => Colonic pseudo-obstruction
f: bloody diarrhoea, fever and a transverse colon over 6 cm wide in ulcerative colitis => Toxic megacolon
x: Caecal volvulus => Arises from the right iliac fossa and is more common in younger adults
x: Colonic pseudo-obstruction => Dilates the colon diffusely with no single twisted loop
x: Obstructing sigmoid carcinoma => Follows weeks of changing bowel habit and gives a cut-off, not one twisted loop
x: Toxic megacolon => Follows colitis or C. difficile with bloody diarrhoea and systemic toxicity

@u 37 2L
s: A 71 year old woman has had constant left lower abdominal pain for 2 days with fever and loss of appetite. She has had intermittent constipation for years. She opened her bowels today and is passing flatus. // Temperature 38.3°C, pulse rate 98 bpm, BP 134/80 mmHg. There is tenderness and guarding in the left iliac fossa. The abdomen is not distended.
$ White cell count ; 15.2 × 10⁹/L ; 4.0–11.0
$ CRP ; 128 mg/L ; <5
$ Haemoglobin ; 128 g/L ; 115–150
$ Lactate ; 1.3 mmol/L ; <2.0
? Which is the most likely diagnosis?
> *Acute diverticulitis ; Colorectal carcinoma ; Ischaemic colitis ; Ovarian torsion ; Sigmoid volvulus
= Left iliac fossa pain with fever, local guarding and raised inflammatory markers in an older adult is acute diverticulitis, an inflamed sigmoid diverticulum. She is still passing stool and flatus with no distension, so this is not obstruction or volvulus.
~ Sudden pain then bloody diarrhoea in a woman with atrial fibrillation and a raised lactate → ischaemic colitis.
c: left lower abdominal pain for 2 days | fever | passing flatus | left iliac fossa | White cell count 15.2
m: A faecolith blocks the neck of a sigmoid diverticulum, bacteria multiply and the wall becomes inflamed
g: LIF pain, fever and a raised WCC and CRP with the bowels still working → diverticulitis
f: sudden pain followed by bloody diarrhoea in a woman with atrial fibrillation => Ischaemic colitis
f: gross distension and absolute constipation with a coffee bean loop on X-ray => Sigmoid volvulus
f: 3 months of looser stools, weight loss and a microcytic anaemia => Colorectal carcinoma
x: Colorectal carcinoma => Causes a change in bowel habit, weight loss and anaemia, and her haemoglobin is normal
x: Ischaemic colitis => Presents with sudden pain and bloody diarrhoea, and her lactate is normal
x: Ovarian torsion => Gives sudden severe one-sided pain with vomiting, usually in younger women, and fever comes late
x: Sigmoid volvulus => She is passing flatus and the abdomen is not distended

@u 48 2L
s: A 68 year old man has had colicky lower abdominal pain and a swollen abdomen for 4 days. He has not opened his bowels or passed flatus for 2 days and has started to vomit. Over the past 3 months his stools have become looser and he has lost 6 kg. He has never had abdominal surgery. // The abdomen is distended and tympanic with high-pitched bowel sounds. There are no hernias. An abdominal X-ray shows dilated colon down to the sigmoid with no gas in the rectum.
$ Haemoglobin ; 101 g/L ; 130–175
$ MCV ; 74 fL ; 80–96
$ CRP ; 18 mg/L ; <5
? Which is the most likely cause of his bowel obstruction?
> Adhesions ; *Colorectal carcinoma ; Diverticular stricture ; Obstructed inguinal hernia ; Sigmoid volvulus
= Large bowel obstruction after months of changing bowel habit, weight loss and an iron deficiency picture is colorectal carcinoma until proven otherwise. It is the commonest cause of large bowel obstruction in the UK. He needs a CT of abdomen and pelvis to confirm the level, stage the tumour and plan decompression.
~ Previous laparotomy with dilated small bowel and a collapsed colon → adhesions.
c: looser and he has lost 6 kg | never had abdominal surgery | no hernias | dilated colon down to the sigmoid | MCV 74
m: A tumour slowly narrows the lumen, bleeds occultly and finally closes the bowel
g: Large bowel obstruction plus weight loss and a microcytic anaemia → colorectal carcinoma
f: a previous laparotomy with dilated small bowel and a collapsed colon => Adhesions
f: an irreducible tender lump above and medial to the pubic tubercle => Obstructed inguinal hernia
f: years of left iliac fossa pain attacks and a smooth tapering narrowing without weight loss => Diverticular stricture
x: Adhesions => Cause small bowel obstruction after previous surgery, and he has had none
x: Diverticular stricture => Can obstruct the colon but does not explain weight loss and iron deficiency
x: Obstructed inguinal hernia => There are no hernias on examination
x: Sigmoid volvulus => Gives one twisted loop with sudden distension, not months of weight loss

@u 33 2T
s: A 63 year old man has had rectal bleeding mixed with his stool and a feeling of incomplete emptying for 2 months. Flexible sigmoidoscopy shows an ulcerated mass with rolled edges 6 cm from the anal verge, and a biopsy is taken.
? Which is the most likely histological type?
> *Adenocarcinoma ; Carcinoid tumour ; Gastrointestinal stromal tumour ; Lymphoma ; Squamous cell carcinoma
= Six centimetres from the anal verge is the rectum, which is lined by glandular columnar epithelium, so well over 90% of cancers there are adenocarcinomas. Squamous cell carcinoma arises in the anal canal, below the dentate line, within about 4 cm of the verge.
~ An ulcerated lesion at the anal margin in a man with HIV and anal warts → squamous cell carcinoma.
c: mixed with his stool | ulcerated mass with rolled edges | 6 cm from the anal verge
m: Columnar mucosa above the dentate line becomes an adenoma and then an adenocarcinoma
g: Rectum means a glandular lining and adenocarcinoma; the anal canal means squamous
f: an ulcerated lesion at the anal margin in a man with HIV and anal warts => Squamous cell carcinoma
f: flushing, diarrhoea and wheeze with liver metastases => Carcinoid tumour
x: Carcinoid tumour => Rare in the rectum and usually a small yellow submucosal nodule, not an ulcer with rolled edges
x: Gastrointestinal stromal tumour => A submucosal tumour most often in the stomach, rarely an ulcerated rectal mass
x: Lymphoma => Rare in the rectum and usually seen with immunosuppression or systemic symptoms
x: Squamous cell carcinoma => Belongs to the anal canal below the dentate line, closer to the verge than 6 cm

@u 77 1L
s: A 69 year old man has passed blood in his urine on and off for 3 weeks. It is painless and sometimes contains small clots. He smoked 30 cigarettes a day for 40 years and worked in a rubber factory. He has not travelled outside Europe. // Abdominal and rectal examinations are normal. Urine culture shows no growth. Flexible cystoscopy shows a papillary tumour on the bladder wall.
? Which is the most likely histological type?
> Adenocarcinoma ; Renal cell carcinoma ; Small cell carcinoma ; Squamous cell carcinoma ; *Transitional cell carcinoma
= Over 90% of bladder cancers in the UK are transitional cell, now called urothelial, carcinoma. Smoking and aromatic amines from the rubber and dye industries are the classic causes, and the usual tumour is papillary and presents with painless visible haematuria.
~ Grew up beside the Nile with recurrent schistosomiasis → squamous cell carcinoma of the bladder.
c: painless | smoked 30 cigarettes a day for 40 years | rubber factory | not travelled outside Europe | papillary tumour
m: Carcinogens concentrated in urine sit against the urothelium and drive papillary growth
g: Painless haematuria with smoking or dye work and a papillary bladder tumour → transitional cell carcinoma
f: recurrent schistosomiasis while growing up in Egypt => Squamous cell carcinoma
f: a tumour at the bladder dome arising from a urachal remnant => Adenocarcinoma
f: a solid kidney mass on CT with a new left varicocele => Renal cell carcinoma
x: Adenocarcinoma => Rare, arising from urachal remnants at the dome or after bladder exstrophy
x: Renal cell carcinoma => Arises in the kidney, and cystoscopy has found the tumour in the bladder
x: Small cell carcinoma => Very rare in the bladder and solid rather than papillary
x: Squamous cell carcinoma => Linked to schistosomiasis or long-term catheters, and he has neither

@u 109 2L
s: A 32 year old man is brought to his GP by his sister, who is worried that he has no friends. He works night shifts alone as a security guard and spends his free time doing jigsaws. He says he has never wanted a close relationship and does not mind what others think of him. He shows little emotion during the consultation. // He has no unusual beliefs, odd speech or perceptual disturbances and is not low in mood.
? Which is the most likely diagnosis?
> Autism spectrum disorder ; Avoidant personality disorder ; *Schizoid personality disorder ; Schizophrenia ; Schizotypal personality disorder
= He is detached by preference: he wants no relationships, is indifferent to praise or criticism and shows flat emotion. That is schizoid personality disorder. Schizotypal adds odd beliefs and speech, and people with avoidant personality disorder want relationships but fear rejection.
~ Wants friends but avoids them for fear of being judged → avoidant personality disorder.
c: never wanted a close relationship | does not mind what others think | little emotion | no unusual beliefs, odd speech or perceptual disturbances
m: A lifelong preference for solitude and emotional coldness without the odd thinking of the schizophrenia spectrum
g: Does not want people, flat affect and no odd beliefs → schizoid
f: magical thinking, odd speech and believing strangers' comments are about him => Schizotypal personality disorder
f: longs for friends but avoids them because he expects to be ridiculed => Avoidant personality disorder
f: rigid routines, intense narrow interests and social difficulty since early childhood => Autism spectrum disorder
x: Autism spectrum disorder => Needs social communication difficulty and restricted, repetitive behaviour from early childhood, which is not described
x: Avoidant personality disorder => Avoidant people want relationships and fear rejection, but he does not want them
x: Schizophrenia => Needs psychotic symptoms, and he has no unusual beliefs or perceptual disturbance
x: Schizotypal personality disorder => Adds eccentric beliefs, odd speech and ideas of reference, all absent here

@u 0 2D
s: A 61 year old man has had central chest tightness at rest for 2 hours. He takes no regular medication and has no history of bleeding. // Pulse rate 88 bpm, BP 148/90 mmHg. His ECG shows 1 mm ST depression in leads V4 to V6. He has been given aspirin 300 mg and fondaparinux. Coronary angiography is planned within 72 hours.
$ High-sensitivity troponin T at 0 hours ; 58 ng/L ; <14
$ High-sensitivity troponin T at 1 hour ; 112 ng/L ; <14
$ Haemoglobin ; 146 g/L ; 130–175
$ Creatinine ; 88 µmol/L ; 60–120
? Which drug should be added to aspirin?
> Apixaban ; Clopidogrel ; Dipyridamole ; *Ticagrelor ; Warfarin
= A rising troponin with ST depression and no ST elevation is an NSTEMI. NICE recommends dual antiplatelet therapy with aspirin and ticagrelor for 12 months unless the bleeding risk is high, when clopidogrel is used instead. He has no bleeding history and a normal haemoglobin.
~ A previous intracranial bleed or other high bleeding risk → clopidogrel with aspirin.
c: chest tightness at rest | no history of bleeding | 1 mm ST depression | troponin T at 1 hour 112
m: Blocking the platelet P2Y12 receptor on top of aspirin stops more clot forming on the ruptured plaque
g: NSTEMI with a normal bleeding risk → aspirin plus ticagrelor for 12 months
f: a previous haemorrhagic stroke and a transfusion for a bleeding ulcer last year => Clopidogrel
x: Apixaban => An anticoagulant, added only when there is another reason such as atrial fibrillation
x: Clopidogrel => A weaker P2Y12 blocker kept for high bleeding risk or when ticagrelor cannot be used
x: Dipyridamole => Used after ischaemic stroke, not in acute coronary syndrome
x: Warfarin => Has no place in acute coronary syndrome without another indication

@u 15 2L
s: A 26 year old woman has had a cough and wheeze for 4 months, worse at night and after running. She has never smoked. She had eczema as a child. Her chest X-ray is normal. // Spirometry is performed before and 15 minutes after salbutamol.
$ FEV1 before salbutamol ; 2.41 L ; predicted 3.20
$ FEV1 after salbutamol ; 2.86 L ;
$ FEV1/FVC before salbutamol ; 0.64 ; >0.70
$ Blood eosinophils ; 0.62 × 10⁹/L ; 0.0–0.4
? Which is the most likely diagnosis?
> *Asthma ; Chronic obstructive pulmonary disease ; Gastro-oesophageal reflux disease ; Pulmonary sarcoidosis ; Vocal cord dysfunction
= Symptoms that vary and are worse at night and with exercise, atopy, obstruction that improves by 450 ml, 19%, after salbutamol and raised eosinophils fit asthma. Reversibility of at least 12% and 200 ml supports the diagnosis. The normal chest X-ray argues against sarcoidosis.
~ A 40 pack-year smoker whose obstruction barely changes with salbutamol → COPD.
c: worse at night and after running | never smoked | eczema as a child | chest X-ray is normal | FEV1 after salbutamol 2.86
m: Eosinophilic airway inflammation makes smooth muscle twitchy, so narrowing comes and goes and reverses with a bronchodilator
g: Reversible obstruction of at least 12% and 200 ml with atopy → asthma
f: a 40 pack-year smoker whose FEV1 rises by 50 ml after salbutamol => Chronic obstructive pulmonary disease
f: dry cough, erythema nodosum and bilateral hilar lymphadenopathy on X-ray => Pulmonary sarcoidosis
f: noisy breathing in, normal spirometry between attacks and a flattened inspiratory loop => Vocal cord dysfunction
x: Chronic obstructive pulmonary disease => She is a young non-smoker and her obstruction is largely reversible
x: Gastro-oesophageal reflux disease => Can cause a night cough but not reversible airflow obstruction
x: Pulmonary sarcoidosis => Usually shows hilar lymphadenopathy on the X-ray and a restrictive pattern
x: Vocal cord dysfunction => Narrows the larynx on breathing in, with a normal FEV1 and no response to salbutamol

@u 22 2L
s: A 66 year old man has had increasing breathlessness on exertion for 2 years and a cough productive of black sputum. He worked underground in a coal mine for 28 years and has never smoked. // There are fine crackles at both apices. Chest X-ray shows multiple small rounded nodules, most numerous in the upper zones, with no pleural thickening.
? Which is the most likely diagnosis?
> Asbestosis ; *Coal workers' pneumoconiosis ; Hypersensitivity pneumonitis ; Silicosis ; Tuberculosis
= Years of coal dust, black sputum and small rounded upper zone nodules are coal workers' pneumoconiosis. Silicosis also gives upper zone nodules, but it follows quarrying, sandblasting or stonework and classically causes eggshell calcification of the hilar nodes. Asbestosis affects the lower zones with pleural plaques.
~ A sandblaster with eggshell calcification of the hilar nodes → silicosis.
c: black sputum | coal mine for 28 years | upper zones | no pleural thickening
m: Inhaled coal dust is taken up by alveolar macrophages, which collect around respiratory bronchioles and form nodules
g: Coal miner with upper zone nodules and black sputum → coal workers' pneumoconiosis
f: 20 years of sandblasting and eggshell calcification of the hilar lymph nodes => Silicosis
f: lagging pipes in a shipyard, calcified pleural plaques and lower zone fibrosis => Asbestosis
f: a pigeon keeper with fevers a few hours after cleaning the loft => Hypersensitivity pneumonitis
x: Asbestosis => Causes lower zone fibrosis with pleural plaques, and his changes are upper zone without pleural disease
x: Hypersensitivity pneumonitis => Follows organic antigens such as birds or mouldy hay, not coal dust
x: Silicosis => Follows quartz exposure in quarrying or sandblasting, typically with eggshell hilar calcification
x: Tuberculosis => Would bring weight loss, night sweats and cavitation rather than many small nodules over 2 years

@u 17 1L
s: A 48 year old woman has coughed up large amounts of thick yellow-green sputum every day for several years, about a cupful a day. She had severe whooping cough as a child. She has had 4 chest infections this year. She has never smoked. // Her fingers are clubbed. There are coarse inspiratory crackles at both lung bases that change after coughing.
? Which is the most likely diagnosis?
> Asthma ; *Bronchiectasis ; Chronic obstructive pulmonary disease ; Idiopathic pulmonary fibrosis ; Lung abscess
= Daily copious purulent sputum, recurrent infections, whooping cough in childhood and coarse crackles that shift with coughing are bronchiectasis: permanently dilated bronchi that pool mucus. Clubbing is common. The diagnosis is confirmed on high-resolution CT.
~ Fine dry crackles at the end of inspiration that do not clear with coughing, and no sputum → idiopathic pulmonary fibrosis.
c: about a cupful a day | whooping cough as a child | 4 chest infections | never smoked | coarse inspiratory crackles
m: Infection damages the bronchial wall, the airways dilate, mucus pools and infection recurs in a vicious cycle
g: Daily copious purulent sputum, recurrent infections and coarse crackles → bronchiectasis
f: fine dry end-inspiratory crackles, clubbing and no sputum in a 70 year old => Idiopathic pulmonary fibrosis
f: a 2 week illness with swinging fever, foul sputum and a cavity with a fluid level after a seizure => Lung abscess
f: a 40 pack-year smoker with slowly worsening breathlessness and winter infections => Chronic obstructive pulmonary disease
x: Asthma => Causes variable wheeze and cough without daily purulent sputum or clubbing
x: Chronic obstructive pulmonary disease => She has never smoked, and her sputum volume is far higher than COPD usually produces
x: Idiopathic pulmonary fibrosis => Gives fine dry crackles that do not change with coughing and little sputum
x: Lung abscess => An acute illness with a cavity, not years of daily sputum

@u 17 2R
s: A 55 year old man has had a daily cough with 2 tablespoons of purulent sputum for 3 years and has needed 5 courses of antibiotics in the past year. He has rheumatoid arthritis. // There are coarse crackles at the right base. Chest X-ray shows thickened bronchial walls at the right base with tramline shadows. Spirometry shows mild airflow obstruction.
? Which investigation is most likely to confirm the diagnosis?
> Bronchoscopy ; *High-resolution CT of chest ; Repeat chest X-ray in 6 weeks ; Spirometry with bronchodilator reversibility ; Sputum culture
= Bronchiectasis is diagnosed on high-resolution CT, which shows bronchi wider than the artery beside them, the signet ring sign, and bronchi that fail to taper. Rheumatoid arthritis is a recognised cause. Sputum culture guides antibiotics but does not make the diagnosis.
~ Persistent collapse of one lobe with haemoptysis in a smoker → bronchoscopy to look for an obstructing tumour.
c: purulent sputum for 3 years | 5 courses of antibiotics | rheumatoid arthritis | tramline shadows
m: Dilated thick-walled airways are seen directly on thin CT slices, larger than the vessel beside them
g: Suspected bronchiectasis → HRCT confirms it
f: persistent right lower lobe collapse and haemoptysis in a 60 pack-year smoker => Bronchoscopy
f: the diagnosis is already known and the question is which antibiotic to give for this exacerbation => Sputum culture
x: Bronchoscopy => Looks for an obstructing lesion or foreign body, not the airway dilatation itself
x: Repeat chest X-ray in 6 weeks => Used after pneumonia to check resolution, and X-ray misses much bronchiectasis
x: Spirometry with bronchodilator reversibility => Tests for asthma and measures obstruction but cannot show dilated bronchi
x: Sputum culture => Identifies organisms such as Pseudomonas to guide treatment, not the structural diagnosis

@u 20 1L
s: A 34 year old man who moved from Somalia 2 years ago has had a cough for 8 weeks, with drenching night sweats and 7 kg weight loss. Last week he coughed up streaks of blood. He lives in a shared hostel. // Temperature 37.9°C. Chest X-ray shows patchy consolidation with a cavity in the right upper lobe.
? Which is the most likely diagnosis?
> Aspergilloma ; Community-acquired pneumonia ; Lung cancer ; Sarcoidosis ; *Tuberculosis
= Weeks of cough, night sweats, weight loss and haemoptysis in a man from a high-incidence country living in crowded housing, with an upper lobe cavity, is pulmonary tuberculosis until proven otherwise. He needs 3 sputum samples for acid-fast bacilli and isolation while he may be infectious.
~ A ball inside an old upper lobe cavity with a crescent of air around it → aspergilloma.
c: Somalia | 8 weeks | drenching night sweats | 7 kg weight loss | cavity in the right upper lobe
m: Mycobacteria thrive in the oxygen-rich apices, and caseating necrosis empties into a bronchus to leave a cavity
g: Chronic cough, sweats, weight loss and an upper lobe cavity in someone from a high-incidence country → TB
f: a mobile mass inside an old cavity with a crescent of air around it => Aspergilloma
f: 3 days of fever, pleuritic pain and lobar consolidation without a cavity => Community-acquired pneumonia
f: a 72 year old heavy smoker with haemoptysis and a hilar mass but no fever or sweats => Lung cancer
x: Aspergilloma => Grows in an existing cavity and causes haemoptysis, but not this febrile illness with weight loss
x: Community-acquired pneumonia => An acute illness over days, not 8 weeks of sweats and weight loss
x: Lung cancer => Can cavitate, but his age, origin, fevers and sweats point to infection
x: Sarcoidosis => Causes hilar lymphadenopathy and does not usually cavitate or cause haemoptysis

@u 137 2D
s: A 57 year old man's psoriasis has flared over the past 5 weeks. He has well-demarcated salmon-pink plaques with silvery scale on his elbows, knees and lower back that had been controlled for years with an emollient and calcipotriol. Six weeks ago his cardiologist added a regular drug for exertional angina. He drinks 6 units of alcohol a week and has had no recent sore throat.
? Which drug is most likely to have caused the flare?
> Amlodipine ; *Atenolol ; Isosorbide mononitrate ; Nicorandil ; Ranolazine
= Beta-blockers are a classic trigger for psoriasis flares, along with lithium, antimalarials, NSAIDs and the withdrawal of oral steroids. The flare began within weeks of a new regular anti-anginal, and atenolol is the only beta-blocker offered.
~ Flare after a course of oral prednisolone is stopped, or after lithium is started → those drugs instead.
c: flared over the past 5 weeks | Six weeks ago | exertional angina | 6 units | no recent sore throat
m: Beta-blockade alters signalling in keratinocytes and can trigger or worsen psoriatic plaques
g: Psoriasis flare after a new beta-blocker → stop or switch the beta-blocker
f: large painful mouth and perianal ulcers after starting a potassium channel opener => Nicorandil
f: ankle swelling and flushing with no change in the skin => Amlodipine
x: Amlodipine => Causes ankle oedema and flushing, not a psoriasis flare
x: Isosorbide mononitrate => Causes headache and postural hypotension
x: Nicorandil => Causes painful oral, anal and skin ulcers rather than psoriatic plaques
x: Ranolazine => Can prolong the QT interval but is not a recognised psoriasis trigger

@u 135 1D
s: A 24 year old woman has had intense itching for 3 weeks, worst at night. Her partner has started itching too. // There are small red papules and short grey wavy tracks between her fingers and on the inner wrists, with excoriated papules around her waist. Her face is spared. She is not pregnant and has no allergies.
? Which is the most appropriate treatment?
> Aqueous cream ; Malathion lotion ; Oral cetirizine ; Oral ivermectin ; *Permethrin cream
= Night itch, burrows in the finger webs and wrists and an itchy partner are scabies. First line is permethrin 5% cream over the whole body from the neck down, left on for 8 to 12 hours and repeated after 7 days. All household and close contacts are treated at the same time, even without symptoms.
~ Permethrin allergy → malathion 0.5% lotion; crusted scabies in an immunosuppressed patient → oral ivermectin as well.
c: worst at night | partner has started itching | between her fingers | inner wrists | no allergies
m: Sarcoptes mites burrow in the stratum corneum, and the itch is a delayed hypersensitivity to the mites and their faeces
g: Burrows, night itch and itchy contacts → permethrin for her and every contact, twice 7 days apart
f: a known allergy to permethrin => Malathion lotion
f: thick crusted plaques teeming with mites in a man on long-term immunosuppression => Oral ivermectin
x: Aqueous cream => An emollient that does not kill mites
x: Malathion lotion => Second line, used when permethrin cannot be
x: Oral cetirizine => Can ease the itch but does not treat the infestation
x: Oral ivermectin => Kept for crusted scabies or treatment failure

@k b:hepatitis 2L
s: A 58 year old man has had 10 days of malaise and nausea followed by yellow eyes and dark urine. He lives in Hampshire and has not travelled abroad. He enjoys barbecued pork sausages and wild boar. He completed courses of hepatitis A and B vaccine last year before a cruise. He drinks 8 units of alcohol a week and takes no medication.
$ Bilirubin ; 96 µmol/L ; <17
$ ALT ; 1840 IU/L ; 10–50
$ ALP ; 168 IU/L ; 25–115
$ Hepatitis A IgM ; negative ;
$ Hepatitis B surface antigen ; negative ;
? Which is the most likely cause?
> Alcoholic hepatitis ; Epstein-Barr virus ; Hepatitis A ; Hepatitis C ; *Hepatitis E
= Hepatitis E is now one of the commonest causes of acute viral hepatitis in the UK, and most infections caught here come from undercooked pork, game and processed pork products. He is vaccinated against A and B and both tests are negative, and hepatitis C rarely causes acute jaundice. Most cases clear without treatment.
~ Unvaccinated, positive hepatitis A IgM after eating shellfish abroad → hepatitis A.
c: not travelled abroad | barbecued pork sausages and wild boar | hepatitis A and B vaccine | ALT 1840 | Hepatitis A IgM negative
m: Hepatitis E genotype 3 lives in pigs, and undercooked pork delivers the virus to the liver through the gut
g: Acute hepatitis in the UK with pork exposure and negative A and B → hepatitis E
f: unvaccinated, with a positive hepatitis A IgM after eating shellfish abroad => Hepatitis A
f: AST twice the ALT, ALT under 300 and 15 years of heavy drinking => Alcoholic hepatitis
f: a 19 year old with a sore throat, tonsillar exudate and splenomegaly => Epstein-Barr virus
x: Alcoholic hepatitis => He drinks little, and alcohol rarely pushes the ALT above 300 or makes it higher than the AST
x: Epstein-Barr virus => Gives a sore throat, lymphadenopathy and a milder hepatitis in young adults
x: Hepatitis A => He is vaccinated and the IgM is negative
x: Hepatitis C => Acute infection is usually silent, and he has no injecting or blood exposure

@u 77 2R
s: A 52 year old woman has noticed red urine on 2 occasions in the past fortnight. She has no pain, fever or urinary frequency. She smokes 15 cigarettes a day. // Abdominal examination is normal.
$ Urine dipstick blood ; 3+ ; negative
$ Urine dipstick nitrite ; negative ; negative
$ Urine dipstick leucocytes ; negative ; negative
$ Midstream urine culture ; no growth ;
$ eGFR ; >90 mL/min/1.73m² ; >60
? Which is the most appropriate next step?
> Prescribe nitrofurantoin and review in 1 week ; Reassure and repeat dipstick in 3 months ; Refer for routine renal ultrasound ; *Refer urgently to urology ; Send urine for cytology
= NICE recommends a suspected cancer referral to urology for anyone aged 45 or over with unexplained visible haematuria and no urinary infection. She is a smoker with painless visible haematuria and sterile urine. She needs cystoscopy and imaging of the upper tracts on the 2 week pathway.
~ Dysuria, nitrites and a culture growing E. coli → treat the infection and refer if the blood persists after treatment.
c: red urine on 2 occasions | no pain, fever or urinary frequency | smokes 15 cigarettes | Midstream urine culture no growth
m: Painless bleeding from the urothelium is bladder cancer until cystoscopy shows otherwise
g: Aged 45 or over with unexplained visible haematuria → suspected cancer referral to urology
f: dysuria with nitrite and leucocytes positive and a culture growing E. coli => Prescribe nitrofurantoin and review in 1 week
x: Prescribe nitrofurantoin and review in 1 week => There is no infection, so an antibiotic delays the diagnosis
x: Reassure and repeat dipstick in 3 months => Visible haematuria in a smoker over 45 cannot wait 3 months
x: Refer for routine renal ultrasound => Ultrasound misses many bladder tumours, and the pathway should be urgent
x: Send urine for cytology => Misses many low-grade tumours and does not replace cystoscopy

@u 79 2L
s: A 38 year old man has had sudden severe pain in his right loin for 3 hours, coming in waves and spreading to the groin. He cannot keep still and has vomited twice. // Temperature 37.1°C, pulse rate 104 bpm, BP 142/86 mmHg. The abdomen is soft with mild right loin tenderness.
$ Urine dipstick blood ; 3+ ; negative
$ Urine dipstick nitrite ; negative ; negative
$ White cell count ; 9.8 × 10⁹/L ; 4.0–11.0
$ CRP ; 6 mg/L ; <5
$ Creatinine ; 92 µmol/L ; 60–120
? Which is the most likely diagnosis?
> Acute appendicitis ; Acute pyelonephritis ; Leaking abdominal aortic aneurysm ; Testicular torsion ; *Ureteric calculus
= Sudden colicky loin to groin pain in a restless patient with blood on dipstick and no fever is renal colic from a ureteric stone. A normal temperature and inflammatory markers argue against pyelonephritis. He needs a non-contrast CT KUB within 24 hours and NSAID analgesia.
~ Fever of 39°C, rigors, constant loin pain and nitrites → acute pyelonephritis; fever with an obstructing stone → urgent decompression.
c: coming in waves and spreading to the groin | cannot keep still | Temperature 37.1 | Urine dipstick blood 3+ | White cell count 9.8
m: A stone impacts at a narrow point of the ureter, and peristalsis against it causes colic and bleeding
g: Restless loin to groin colic with haematuria and no fever → ureteric stone
f: fever of 39°C, rigors, constant loin pain and nitrite positive urine => Acute pyelonephritis
f: a 72 year old smoker with loin pain, hypotension and a pulsatile mass => Leaking abdominal aortic aneurysm
f: central abdominal pain moving to the right iliac fossa with anorexia => Acute appendicitis
x: Acute appendicitis => Pain settles in the right iliac fossa with peritonism, and patients lie still
x: Acute pyelonephritis => Needs fever, constant loin pain and raised inflammatory markers, all absent
x: Leaking abdominal aortic aneurysm => Unlikely at 38 with a normal blood pressure, though it must be considered in older patients with loin pain
x: Testicular torsion => Presents with scrotal pain and a tender high-riding testis

@k b:glomerulo 2L
s: A 9 year old boy has had dark brown urine and puffy eyes for 2 days. Two weeks ago he had a sore throat with fever that settled without antibiotics. // BP 134/88 mmHg. There is periorbital swelling and mild ankle swelling.
$ Urine dipstick blood ; 3+ ; negative
$ Urine dipstick protein ; 2+ ; negative
$ Creatinine ; 88 µmol/L ; 25–60
$ Complement C3 ; 0.31 g/L ; 0.75–1.65
$ Anti-streptolysin O titre ; 640 IU/mL ; <200
? Which is the most likely diagnosis?
> Henoch-Schönlein purpura nephritis ; IgA nephropathy ; Minimal change disease ; *Post-streptococcal glomerulonephritis ; Urinary tract infection
= A nephritic picture, with haematuria, hypertension, oedema and a raised creatinine, 1 to 3 weeks after a streptococcal throat infection is post-streptococcal glomerulonephritis. A low C3 and a high anti-streptolysin O titre support it. Most children recover with supportive care.
~ Visible haematuria a day or two after a sore throat with normal complement → IgA nephropathy.
c: dark brown urine | Two weeks ago | sore throat | Complement C3 0.31 | Anti-streptolysin O titre 640
m: Immune complexes against streptococcal antigens lodge in the glomeruli and activate complement, which is used up
g: Nephritic picture 2 weeks after a sore throat with a low C3 → post-streptococcal GN
f: visible haematuria starting a day after a sore throat with normal complement => IgA nephropathy
f: heavy proteinuria, a low albumin and gross oedema with a normal blood pressure and no blood => Minimal change disease
f: a purpuric rash on the buttocks and legs with joint and abdominal pain => Henoch-Schönlein purpura nephritis
x: Henoch-Schönlein purpura nephritis => Needs the purpuric rash, abdominal pain and arthritis, which he does not have
x: IgA nephropathy => Bleeding starts within 1 to 2 days of the infection and complement is normal
x: Minimal change disease => Gives nephrotic syndrome with heavy proteinuria and no blood or hypertension
x: Urinary tract infection => Does not cause hypertension, oedema, a low complement or a raised titre

@u 133 2L
s: A 23 year old woman has had a painful lump on the sole of her foot for 3 months, beneath the ball of the second toe. It hurts most when she squeezes it from side to side. She swims twice a week. // There is a 6 mm rough raised lesion that interrupts the normal skin lines. After gentle paring with a scalpel, several pinpoint black dots appear.
? Which is the most likely diagnosis?
> Acral lentiginous melanoma ; Callus ; Hard corn ; *Plantar wart ; Seborrhoeic keratosis
= Plantar warts are caused by human papillomavirus. They interrupt the skin lines, hurt most when squeezed from side to side and show black dots of clotted capillaries when pared. Calluses and corns keep the skin lines and hurt on direct pressure, and a corn shows a translucent central core when pared.
~ Pain on direct pressure and a translucent central core when pared → hard corn.
c: squeezes it from side to side | swims | interrupts the normal skin lines | pinpoint black dots
m: HPV makes keratinocytes overgrow around small capillaries that clot and show as black dots
g: Black dots, broken skin lines and pain on pinching → plantar wart
f: pain on direct pressure and a translucent central core after paring => Hard corn
f: a diffuse yellow thickening over a pressure point with the skin lines preserved => Callus
f: an enlarging irregular brown-black patch on the sole with pigment spreading onto the nail fold => Acral lentiginous melanoma
x: Acral lentiginous melanoma => An irregular pigmented patch, not a rough papule with pinpoint dots after paring
x: Callus => A diffuse thickening with the skin lines running through it
x: Hard corn => Keeps the skin lines, hurts on direct pressure and has a translucent core
x: Seborrhoeic keratosis => A stuck-on warty lesion of older skin that does not occur on the sole

@u 123 1L
s: A 74 year old retired farmer has had a slowly growing lesion beside his nose for 18 months. It sometimes bleeds and scabs, then appears to heal. // There is an 8 mm pearly nodule with a rolled edge, fine branching blood vessels over its surface and a small central crust. There are no palpable lymph nodes.
? Which is the most likely diagnosis?
> *Basal cell carcinoma ; Keratoacanthoma ; Nodular melanoma ; Seborrhoeic keratosis ; Squamous cell carcinoma
= A slowly growing pearly nodule with a rolled edge, surface telangiectasia and a central crust that bleeds and heals, on sun-damaged facial skin, is a nodular basal cell carcinoma. It invades locally but almost never spreads, so the nodes are not involved. NICE advises a routine rather than a suspected cancer referral.
~ A tender crusted nodule on the lower lip that grew over 8 weeks → squamous cell carcinoma.
c: slowly growing | 18 months | bleeds and scabs, then appears to heal | pearly nodule with a rolled edge | fine branching blood vessels
m: Nests of basal keratinocyte tumour cells push the skin up into a translucent nodule with stretched vessels on top
g: Pearly rolled edge, telangiectasia and slow growth → BCC
f: a tender crusted nodule on the lower lip that grew over 8 weeks => Squamous cell carcinoma
f: a dome-shaped nodule with a central keratin plug that grew over 4 weeks and is now shrinking => Keratoacanthoma
f: a rapidly growing black nodule that bleeds on touch => Nodular melanoma
x: Keratoacanthoma => Grows within weeks with a central keratin plug and may shrink on its own
x: Nodular melanoma => Usually pigmented and fast growing, not pearly over 18 months
x: Seborrhoeic keratosis => A stuck-on warty plaque without a rolled pearly edge
x: Squamous cell carcinoma => Faster growing, crusted and tender, and can spread to nodes

@u 138 2D
s: A 19 year old woman has moderate acne on her face, chest and back with many inflamed papules and pustules but no nodules or scarring. It has not improved after 12 weeks of lymecycline with topical adapalene and benzoyl peroxide. She also asks for contraception. She does not smoke, has no migraine and no personal or family history of venous thrombosis. Her BMI is 23 kg/m².
? Which is the most appropriate next treatment?
> *Co-cyprindiol ; Desogestrel ; Doxycycline ; Oral isotretinoin ; Topical clindamycin
= Co-cyprindiol, a combined pill containing the anti-androgen cyproterone, is licensed for acne in women when topical treatment and oral antibiotics have failed, and it is also a contraceptive. She has no risk factors for thrombosis. It carries more thrombosis risk than other combined pills, so it is stopped about 3 months after the acne settles.
~ Nodules, cysts or scarring, or failure of 2 full courses of treatment → refer to dermatology for isotretinoin.
c: moderate acne | no nodules or scarring | 12 weeks of lymecycline | asks for contraception | no personal or family history of venous thrombosis
m: Cyproterone blocks androgen receptors and ethinylestradiol lowers free testosterone, so sebum production falls
g: Failed topical treatment and oral antibiotic, wants contraception, low thrombosis risk → co-cyprindiol
f: nodules and cysts with early scarring despite 2 full courses of treatment => Oral isotretinoin
x: Desogestrel => A progestogen-only pill that can worsen acne and does not treat it
x: Doxycycline => Switching to another tetracycline after one has failed adds resistance without benefit
x: Oral isotretinoin => For severe, nodular or scarring acne under a dermatologist, and she has none of these
x: Topical clindamycin => A topical antibiotic on its own breeds resistance and is weaker than what has already failed

@u 143 2R
s: A 44 year old man has had a severe sore throat for 12 hours and now cannot swallow his saliva. His voice is muffled and he is sitting upright, leaning forward and drooling. // Temperature 39.2°C, pulse rate 118 bpm, respiratory rate 26/min, oxygen saturation 93% breathing air. There is soft inspiratory stridor.
? Which is the most appropriate immediate action?
> *Call a senior anaesthetist to secure the airway ; Examine the throat with a tongue depressor ; Give IV ceftriaxone ; Lateral neck X-ray ; Take a throat swab
= Drooling, a muffled voice, sitting forward and stridor with fever are acute epiglottitis, which can obstruct the airway completely without warning. The priority is a senior anaesthetist and an ENT surgeon to secure the airway, ideally in theatre. Do not lie him flat or examine the throat. IV antibiotics follow once the airway is safe.
~ A one-sided tonsillar swelling, trismus and a deviated uvula with a safe airway → peritonsillar abscess for needle aspiration.
c: cannot swallow his saliva | muffled | leaning forward and drooling | inspiratory stridor | oxygen saturation 93%
m: A swollen epiglottis can be sucked into the laryngeal inlet, and distress or instruments can trigger complete obstruction
g: Epiglottitis with stridor → the airway first, by a senior anaesthetist, before anything else
f: the airway has already been secured by intubation in theatre => Give IV ceftriaxone
x: Examine the throat with a tongue depressor => May provoke laryngospasm and complete obstruction
x: Give IV ceftriaxone => Needed soon, but securing the airway takes priority while there is stridor
x: Lateral neck X-ray => Shows the thumb sign but wastes time and takes him away from airway support
x: Take a throat swab => Can trigger obstruction and does not change immediate management

@u 25 2D
s: A 31 year old woman with ulcerative colitis extending to the hepatic flexure has had 4 loose stools a day with some blood for 10 days. She is otherwise well and takes no regular medication. // Temperature 36.9°C, pulse rate 78 bpm.
$ Haemoglobin ; 128 g/L ; 115–150
$ CRP ; 14 mg/L ; <5
$ Albumin ; 39 g/L ; 35–50
? Which is the most appropriate treatment to induce remission?
> Infliximab ; IV hydrocortisone ; Oral azathioprine ; *Oral mesalazine ; Oral prednisolone
= Fewer than 6 stools a day with no fever, tachycardia or anaemia is a mild to moderate flare. For extensive disease NICE advises a high-dose oral aminosalicylate such as mesalazine, often with a topical one. Oral prednisolone is added if there is no response after about 4 weeks.
~ 8 bloody stools a day, fever and tachycardia → acute severe colitis: admit for IV hydrocortisone.
c: extending to the hepatic flexure | 4 loose stools a day | Temperature 36.9 | pulse rate 78 | Haemoglobin 128
m: Mesalazine acts on the inflamed colonic lining and damps down local prostaglandin and leukotriene production
g: Mild to moderate extensive UC → high-dose oral aminosalicylate
f: 8 bloody stools a day, a temperature of 38°C and a pulse rate of 104 bpm => IV hydrocortisone
f: no improvement after 4 weeks of high-dose mesalazine => Oral prednisolone
f: 2 or more flares needing steroids in the past year => Oral azathioprine
x: Infliximab => Kept for severe or steroid-refractory disease
x: IV hydrocortisone => For acute severe colitis, and she has no systemic features
x: Oral azathioprine => Maintains remission in steroid-dependent disease but takes months to work
x: Oral prednisolone => Second line if the aminosalicylate fails

@u 28 1L
s: A 29 year old woman has had bloating, loose pale stools and tiredness for 8 months. She has type 1 diabetes. She eats a normal diet including bread and pasta. // Abdominal examination is normal.
$ Haemoglobin ; 104 g/L ; 115–150
$ MCV ; 76 fL ; 80–96
$ Ferritin ; 6 µg/L ; 12–200
$ Tissue transglutaminase IgA ; 128 U/mL ; <7
$ Total IgA ; 2.1 g/L ; 0.7–4.0
? Which is the most likely diagnosis?
> *Coeliac disease ; Crohn's disease ; Giardiasis ; Irritable bowel syndrome ; Lactose intolerance
= Bloating, pale loose stools and iron deficiency with a strongly positive tTG IgA and a normal total IgA in a woman with type 1 diabetes is coeliac disease. She must keep eating gluten until a duodenal biopsy confirms villous atrophy and crypt hyperplasia.
~ Low total IgA → tTG IgA can be falsely negative, so test IgG-based antibodies.
c: loose pale stools | type 1 diabetes | bread and pasta | Ferritin 6 | Tissue transglutaminase IgA 128
m: Gluten triggers T cell damage to the proximal small bowel, so iron, folate and fat are poorly absorbed
g: Strongly positive tTG with normal IgA while eating gluten → coeliac disease
f: diarrhoea starting after drinking stream water on a camping trip, with negative antibody tests => Giardiasis
f: mouth ulcers, weight loss, a raised CRP and a tender right iliac fossa mass => Crohn's disease
f: bloating and wind only after milk, with normal blood tests => Lactose intolerance
x: Crohn's disease => Can cause iron deficiency, but the strongly positive tTG with normal IgA points to coeliac disease
x: Giardiasis => Follows untreated water and does not raise tTG
x: Irritable bowel syndrome => Does not cause iron deficiency or a positive tTG
x: Lactose intolerance => Causes bloating after dairy without anaemia or antibodies

@k d:neuropathic 1D
s: A 63 year old man with type 2 diabetes has had burning pain and pins and needles in both feet for 6 months, worst at night and disturbing his sleep. Paracetamol has not helped. // There is reduced sensation to monofilament and vibration up to the ankles in a stocking distribution. Foot pulses are present and the skin is intact. His eGFR is 74 mL/min/1.73m².
? Which is the most appropriate treatment?
> *Amitriptyline ; Codeine phosphate ; Ibuprofen ; Topical capsaicin ; Tramadol
= Burning pain that is worse at night with stocking sensory loss is painful diabetic neuropathy. NICE offers amitriptyline, duloxetine, gabapentin or pregabalin first line, switching between them if one fails. Start low at night and warn about drowsiness and a dry mouth.
~ Neuropathic pain confined to a small area in someone who cannot take oral drugs → topical capsaicin.
c: burning pain and pins and needles | worst at night | Paracetamol has not helped | stocking distribution
m: A tricyclic boosts descending noradrenaline and serotonin inhibition in the spinal cord and dampens pain signals
g: Neuropathic pain → amitriptyline, duloxetine, gabapentin or pregabalin
f: a small patch of post-herpetic pain in a man who cannot tolerate oral drugs => Topical capsaicin
f: severe acute pain needing short-term rescue while a first-line drug is increased => Tramadol
x: Codeine phosphate => Weak opioids do little for neuropathic pain and add constipation and drowsiness
x: Ibuprofen => NSAIDs do not help neuropathic pain and can harm the kidneys in diabetes
x: Topical capsaicin => For localised neuropathic pain when oral drugs are unsuitable
x: Tramadol => Used only as short-term rescue for acute neuropathic pain, not as long-term treatment

@k b:infection 2R
s: A 36 year old man with chronic hepatitis B is admitted to a medical ward with cellulitis of the leg. He is hepatitis B e antigen positive. A student nurse asks what extra precautions are needed when caring for him. // He has no cough, diarrhoea or open wounds, and he is not bleeding.
? Which is the most appropriate infection control approach?
> Airborne precautions with an FFP3 mask ; Contact precautions with a side room, gloves and apron ; Droplet precautions with a surgical mask ; Protective isolation in a positive pressure room ; *Standard precautions with safe handling of sharps
= Hepatitis B spreads by blood and body fluids, through sharps injuries, sex and from mother to baby, not through the air or by touch. Standard precautions apply to every patient: hand hygiene, gloves for contact with blood, and careful use and disposal of sharps. A mask adds nothing. Staff should be vaccinated and know their antibody level.
~ Smear-positive pulmonary TB or suspected measles → airborne precautions with an FFP3 mask in a negative pressure room.
c: chronic hepatitis B | e antigen positive | no cough, diarrhoea or open wounds | not bleeding
m: The virus needs a route into the blood, so the risk is a needlestick or splash, not breathing near him
g: Bloodborne virus → standard precautions and sharps safety, no mask needed
f: smear-positive cavitating pulmonary tuberculosis => Airborne precautions with an FFP3 mask
f: profuse diarrhoea with a positive C. difficile toxin => Contact precautions with a side room, gloves and apron
f: influenza A with a cough => Droplet precautions with a surgical mask
x: Airborne precautions with an FFP3 mask => For tuberculosis, measles and chickenpox, which spread through the air
x: Contact precautions with a side room, gloves and apron => For C. difficile, MRSA and norovirus, which spread by touch and surfaces
x: Droplet precautions with a surgical mask => For influenza and other respiratory droplets, not bloodborne viruses
x: Protective isolation in a positive pressure room => Protects severely immunosuppressed patients from others

@k b:ethics 1R
s: A 42 year old woman who is a Jehovah's Witness has a haemoglobin of 64 g/L from heavy menstrual bleeding. The team explains that a blood transfusion would help her quickly. She understands, remembers and weighs the information, and clearly declines blood while accepting iron and tranexamic acid. Her doctor documents her decision and does not transfuse.
? Which ethical principle is the doctor mainly respecting?
> *Autonomy ; Beneficence ; Justice ; Non-maleficence ; Veracity
= Autonomy is the right of a person with capacity to make decisions about their own body, even ones others think unwise. She has capacity, so her refusal of blood must be respected. Beneficence would push towards transfusion, and justice is about fair use of resources.
~ The doctor gives her the full truth about the risks even though it upsets her → veracity.
c: understands, remembers and weighs | clearly declines blood | does not transfuse
m: An informed refusal by an adult with capacity overrides the clinician's view of what is best
g: Capacity plus an informed refusal that is respected → autonomy
f: the team pushes for transfusion because it would help her most => Beneficence
f: a scarce bed is given to the patient with the greatest clinical need => Justice
f: the doctor avoids a drug because its harms outweigh its benefits => Non-maleficence
x: Beneficence => Acting for her good would favour transfusion, which is being set aside
x: Justice => Concerns fairness and the distribution of resources
x: Non-maleficence => Means avoiding harm, but withholding blood increases her risk
x: Veracity => Means honesty, which is part of consent but not the principle at stake in this decision

@k x:cxr 2L
s: A 78 year old man has become very breathless over 6 hours and cannot lie flat. He had a myocardial infarction 3 years ago. // Pulse rate 112 bpm, BP 168/96 mmHg, respiratory rate 30/min, oxygen saturation 86% breathing air. There are crackles up to both mid zones. Chest X-ray shows bilateral perihilar shadowing in a bat's wing pattern, upper lobe blood diversion, Kerley B lines at the bases and small bilateral pleural effusions.
$ NT-proBNP ; 6800 ng/L ; <400
$ CRP ; 9 mg/L ; <5
? Which is the most likely diagnosis?
> Acute respiratory distress syndrome ; *Acute pulmonary oedema ; Bilateral pneumonia ; Lymphangitis carcinomatosa ; Pulmonary embolism
= Orthopnoea, bilateral crackles, a very high NT-proBNP and the classic X-ray signs are acute pulmonary oedema from left ventricular failure: bat's wing shadowing, upper lobe diversion, Kerley B lines and effusions. Treat with oxygen, sitting him up and IV furosemide, with nitrates if the blood pressure allows.
~ Bilateral shadowing with a normal heart size and no effusions 2 days into severe pancreatitis → ARDS.
c: cannot lie flat | myocardial infarction 3 years ago | bat's wing | Kerley B lines | NT-proBNP 6800
m: A failing left ventricle raises pulmonary venous pressure until fluid leaks into the interstitium and then the alveoli
g: Bat's wing shadowing, upper lobe diversion, Kerley B lines, effusions and a high BNP → pulmonary oedema
f: bilateral infiltrates with a normal heart size 2 days into severe acute pancreatitis => Acute respiratory distress syndrome
f: fever, purulent sputum and consolidation with air bronchograms in both lower lobes => Bilateral pneumonia
f: sudden pleuritic pain and a clear chest X-ray after a long flight => Pulmonary embolism
x: Acute respiratory distress syndrome => Follows a major insult such as sepsis or pancreatitis, with normal left heart pressures
x: Bilateral pneumonia => Brings fever and a high CRP, and does not cause upper lobe diversion or a raised BNP
x: Lymphangitis carcinomatosa => Develops over weeks in someone with known cancer and does not raise BNP like this
x: Pulmonary embolism => Usually gives a near-normal X-ray, not bat's wing shadowing
"""
