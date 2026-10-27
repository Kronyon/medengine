from snapdsl import N

N(24, 'Infective diarrhoea', 'gut', 'small',
  'A germ or its toxin irritates the gut lining → water pours into the bowel → loose stools, cramps, sometimes blood',
  'Anyone · travellers, food outbreaks · care homes · recent antibiotics: C. difficile',
  'Watery or bloody diarrhoea>abdo; Crampy abdominal pain>epi; Vomiting>mouth; Fever>head; Dry mouth, dizzy on standing>face',
  'Stool culture and microscopy>if bloody, severe, over 7 days or a traveller*; C. difficile toxin>after antibiotics or in hospital; U&E>dehydration and AKI',
  'Oral fluids and rehydration salts; stay off work 48 h after the last episode | IV fluids if dehydrated or vomiting everything | Antibiotics only for specific bugs or if very unwell | C. difficile: stop the culprit, oral vancomycin',
  'Bloody diarrhoea with low platelets and AKI: HUS>e; Toxic megacolon in C. difficile>e; Severe dehydration in the frail>s',
  'Food poisoning clock: within 6 h = toxin from Staph or Bacillus; days later = a germ that has to grow.')

N(25, 'Inflammatory bowel disease', 'gut', 'colon',
  'The immune system attacks the gut wall → UC: continuous from the rectum up; Crohn\'s: patches anywhere, full thickness → bleeding, pain, weight loss',
  '15 to 40 · family history · Crohn\'s: smokers · UC: ex-smokers',
  'UC: bloody diarrhoea, urgency>abdo; Crohn\'s: pain, weight loss, mouth ulcers>rif; Perianal fistula in Crohn\'s>genit; Red eyes, joint pain, rashes>eyes; Tired, anaemic>all',
  'Faecal calprotectin>raised: gut inflammation; Colonoscopy with biopsies>pattern and depth*; Bloods>FBC, CRP, albumin, ferritin; MRI small bowel>Crohn\'s extent and fistulas',
  'UC mild to moderate: 5-ASA, rectal then oral | Flare not settling: oral steroids | Severe flare: admit, IV hydrocortisone | Maintain: azathioprine or biologics; surgery if failing',
  'Acute severe UC: 6+ bloody stools with fever, pulse over 90 or high CRP>e; Toxic megacolon>e; Bowel cancer risk: surveillance colonoscopy>u',
  'UC is a continuous carpet from the rectum; Crohn\'s is skip lesions from mouth to anus.')

N(26, 'Malnutrition', 'gut', 'small',
  'Intake falls below need → the body burns fat and muscle → weak, slow healing, infections',
  'Frail elderly · cancer, alcohol · eating disorders · long hospital stays',
  'Weight loss over 10% in 6 months>abdo; Muscle wasting>rarm; Poor wound healing>legs; Swollen ankles from low protein>feet',
  'MUST score>BMI, weight loss, acute illness*; Bloods>albumin, phosphate, magnesium, potassium; Dietitian review>calorie and protein needs',
  'Treat the cause; food first, fortify | Oral supplements | NG feeding if unsafe or not enough | PN only if the gut cannot be used',
  'Refeeding: phosphate, potassium and magnesium crash when feeding starts>e; Start slow: 10 kcal per kg if high risk; give thiamine>s; Pressure sores and infections>u',
  'Refeeding kills by the phosphate: start low, go slow, check bloods daily.')

N(27, 'Malabsorption', 'gut', 'small',
  'The small bowel lining or its enzymes fail → fat and vitamins pass straight through → pale greasy stools and deficiencies',
  'Coeliac, Crohn\'s · chronic pancreatitis, alcohol · after bowel surgery · CF',
  'Pale, greasy, floating stools>abdo; Weight loss>epi; Bloating>abdo; Anaemia, tired>all; Bruising from low vitamin K>skin',
  'Bloods>FBC, ferritin, B12, folate, vitamin D, clotting; Coeliac serology>tTG IgA with total IgA; Faecal elastase>low = pancreas*; Imaging or scopes>by the likely cause',
  'Treat the cause | Pancreatic enzymes with meals | Replace vitamins and iron | Dietitian: gluten-free or low-fat as needed',
  'Rapid weight loss or bleeding>u; Osteoporosis from low vitamin D>r; Lymphoma in long-standing coeliac>u',
  'Fat in the stool = pancreas or small bowel. Elastase splits the two.')

N(28, 'Coeliac disease', 'gut', 'small',
  'Gluten triggers an immune attack → the villi flatten → less surface to absorb food and iron',
  'Any age · type 1 diabetes, thyroid disease · family history · Down\'s',
  'Diarrhoea, bloating>abdo; Iron deficiency anaemia>all; Weight loss, tired>epi; Itchy blisters on elbows: dermatitis herpetiformis>rarm',
  'tTG IgA with total IgA, while eating gluten>raised; Duodenal biopsy>villous atrophy, more lymphocytes*; Bloods>FBC, ferritin, folate, B12, calcium',
  'Lifelong strict gluten-free diet | Dietitian and coeliac charity | Replace iron, folate, calcium, vitamin D | Check bone density; pneumococcal vaccine',
  'Not better on diet: hidden gluten or lymphoma>u; Osteoporosis>r; Small bowel lymphoma>u',
  'Test while still eating gluten, or the test lies.')

N(29, 'Irritable bowel syndrome', 'gut', 'colon',
  'The gut and brain talk too loudly → normal stretching feels painful → bowel habit swings, no damage',
  '20 to 40 · women more · stress, anxiety · after gastroenteritis',
  'Pain relieved by opening bowels>abdo; Bloating>abdo; Alternating diarrhoea and constipation>lif; Mucus in stool>genit',
  'Positive diagnosis after 6 months of symptoms>pain eased by opening bowels or tied to a habit change, plus 2 of: straining or urgency, bloating, worse after eating, mucus*; Bloods>FBC, CRP, coeliac serology; Faecal calprotectin>to exclude IBD',
  'Explain, reassure; regular meals, fibre, fluids | Antispasmodic for pain; loperamide or laxative by habit | Low FODMAP diet with a dietitian | Low-dose amitriptyline; CBT',
  '60+ with change in bowel habit: cancer>c; Rectal bleeding or weight loss>c; Raised calprotectin: IBD>u',
  'IBS has no alarm features. If any red flag appears, it isn\'t IBS until proved.')

N(30, 'Hiatus hernia', 'gut', 'wall',
  'Part of the stomach slides up through the diaphragm gap → the valve weakens → acid refluxes',
  'Older adults · obesity · pregnancy',
  'Heartburn>chest; Acid in the mouth>mouth; Worse lying down or bending>epi; Rolling type: fullness after eating>epi',
  'OGD>hernia and oesophagitis*; Barium swallow>size and type; Often seen by chance on CT>r',
  'Lose weight, raise the head of the bed | PPI | Surgery if severe or rolling type with symptoms',
  'Rolling hernia volvulus: pain, retching, can\'t vomit>e; Dysphagia>c; Bleeding, anaemia>u',
  'Sliding = most, causes reflux. Rolling = less common, can twist.')

N(31, 'GORD', 'gut', 'oes',
  'The lower oesophageal valve relaxes → acid splashes up → the oesophagus lining burns',
  'Adults · obesity, smoking, alcohol · pregnancy · large meals at night',
  'Heartburn after food>chest; Acid regurgitation>mouth; Night cough>lungs; Worse lying or bending>epi',
  'Clinical diagnosis if no alarm features*; OGD>55+ with weight loss, or dysphagia at any age; H. pylori test>if dyspepsia',
  'Lifestyle: weight loss, smaller meals, stop smoking, raise the bed | Full-dose PPI for 4 to 8 weeks | Lowest dose that works, or on demand | Surgery if refractory',
  'Dysphagia at any age: suspected cancer pathway>c; 55+ with weight loss and reflux>c; Barrett\'s on OGD: surveillance>u',
  'Acid travelling the wrong way: fix the valve habits before the drugs.')

N(32, 'Peptic ulcer disease', 'gut', 'duod',
  'H. pylori or NSAIDs strip the protective mucus → acid eats into the lining → an ulcer that can bleed or perforate',
  'H. pylori infection · NSAIDs, aspirin, steroids · smokers',
  'Epigastric burning pain>epi; Duodenal: better with food; gastric: worse>epi; Vomiting blood or coffee grounds>mouth; Black tarry stool>genit',
  'H. pylori test: breath or stool antigen, off PPI 2 weeks>positive; OGD>ulcer and biopsy if gastric*; FBC>anaemia',
  'Stop NSAIDs if possible | PPI for 8 weeks | H. pylori: triple therapy, 7 days; retest | Repeat OGD for gastric ulcers to check healing',
  'Haematemesis or melaena: Glasgow-Blatchford score, OGD within 24 h>e; Sudden severe pain, rigid abdomen: perforation>e; Weight loss with a gastric ulcer: cancer>c',
  'H. pylori and NSAIDs cause nearly all ulcers. Remove both and most heal.')

N(33, 'Colorectal cancer', 'gut', 'sig',
  'A polyp in the bowel lining picks up mutations → it turns into cancer over years → bleeds and blocks',
  '60+ · family history, polyps · IBD · red meat, smoking, obesity',
  'Change in bowel habit>lif; Rectal bleeding>genit; Iron deficiency anaemia>all; Weight loss>abdo; Mass on examination>rif',
  'FIT>10 or more = suspected cancer pathway*; Colonoscopy with biopsy>tissue diagnosis*; CT chest, abdomen, pelvis>staging; CEA>baseline and follow-up',
  'Suspected cancer pathway | Surgery: resection by site; stent if obstructed | Chemotherapy, radiotherapy for rectal tumours | Follow-up with CT and CEA',
  'Large bowel obstruction>e; Perforation>e; Liver spread: jaundice>u',
  'Right-sided bleeds silently: anaemia. Left-sided blocks and changes the habit.')

N(34, 'Perianal abscess and fistula', 'gut', 'anus',
  'An anal gland blocks and gets infected → pus collects beside the anus → it can tunnel to the skin as a fistula',
  'Young adults · men more · Crohn\'s, diabetes',
  'Throbbing pain by the anus, worse sitting>genit; Hot red swelling>genit; Fever>head; Fistula: discharge from a skin opening>genit',
  'Clinical examination>tender fluctuant swelling*; MRI pelvis>complex or recurrent fistula; Glucose>diabetes',
  'Incision and drainage under anaesthetic | Analgesia; antibiotics only if spreading or immunosuppressed | Fistula: seton or fistulotomy | Look for Crohn\'s if recurrent',
  'Sepsis or Fournier\'s gangrene>e; Diabetic or immunosuppressed>s; Recurrent: Crohn\'s>u',
  'Pus needs a knife, not antibiotics.')

N(35, 'Haemorrhoids', 'gut', 'anus',
  'The cushions lining the anal canal swell and slip down → they bleed bright red on straining',
  'Constipation, straining · pregnancy · low-fibre diet',
  'Bright red blood on the paper>genit; Painless unless thrombosed>genit; Lump at the anus>genit; Itch>genit',
  'Examination and proctoscopy>internal piles above the dentate line*; FIT or colonoscopy>if bleeding with alarm features or 50+',
  'Fibre, fluids, don\'t strain | Topical soothing creams | Banding for grade 1 to 3 | Surgery for large or grade 4',
  'Change in bowel habit or anaemia: exclude cancer>c; Thrombosed pile: very painful purple lump>s; Heavy bleeding>u',
  'Bright red, painless, on the paper. Dark or mixed in = look higher.')

N(36, 'Anal fissure', 'gut', 'anus',
  'Hard stool tears the anal lining → the sphincter spasms → the tear cannot heal',
  'Young adults · constipation · Crohn\'s if off the midline',
  'Severe pain on passing stool, like glass>genit; Bright red blood>genit; Sentinel skin tag>genit',
  'Clinical: midline posterior tear on gentle inspection*; Avoid DRE if too painful; Atypical site: Crohn\'s, HIV, cancer>u',
  'Fibre, fluids, laxatives; sitz baths | Topical lidocaine for pain | GTN or diltiazem ointment for 6 to 8 weeks | Botox or sphincterotomy if chronic',
  'Off the midline: think Crohn\'s, TB, HIV, cancer>u; Chronic over 6 weeks>u',
  'Pain like passing glass plus blood on the paper = fissure. Relax the sphincter, the tear heals.')

N(37, 'Diverticular disease', 'gut', 'sig',
  'Pressure pushes the lining out through weak spots → pouches form in the sigmoid → they can trap stool and get infected',
  '60+ · low-fibre diet · obesity, NSAIDs',
  'Left lower abdominal pain>lif; Fever, tender LIF: diverticulitis>lif; Change in bowel habit>abdo; Painless bleeding>genit',
  'CRP and FBC>infection; CT abdomen>diverticulitis, abscess, perforation*; Colonoscopy later>exclude cancer',
  'Diverticulosis: high fibre | Uncomplicated diverticulitis: analgesia, fluids, antibiotics only if unwell | Admit if pain uncontrolled or complications | Abscess drained; surgery if perforated',
  'Perforation: rigid abdomen>e; Abscess or fistula to bladder: air in urine>s; Heavy rectal bleeding>e',
  'Left-sided appendicitis of older people.')

N(38, 'Lower GI bleed', 'gut', 'rect',
  'A bleeding point in the colon or rectum → blood passes from below → often stops on its own',
  'Older people · diverticula, piles, angiodysplasia · cancer, IBD · anticoagulants',
  'Fresh red blood or clots from the rectum>genit; Dizzy, pale>face; Fast pulse, low BP>heart; Abdominal pain if ischaemic>abdo',
  'Shock index: pulse over BP>over 1 = unstable; Bloods>FBC, U&E, clotting, group and save; CT angiogram>if unstable*; Colonoscopy>once stable',
  'ABCDE; two large cannulas, fluids, blood | Stop or reverse anticoagulants | Unstable: CT angiogram, then embolisation | Stable: colonoscopy; surgery if all else fails',
  'Shock>e; Heavy fresh bleeding with high urea: could be upper GI>e; Repeat bleeds>u',
  'Very heavy fresh blood plus a high urea can still be an upper GI bleed rushing through.')

N(39, 'Constipation', 'gut', 'colon',
  'Stool moves too slowly → more water is absorbed → hard, infrequent stools',
  'Elderly · low fibre and fluid · opioids, iron · immobility, hypothyroidism, high calcium',
  'Fewer than 3 stools a week>abdo; Hard stools, straining>genit; Bloating>abdo; Overflow diarrhoea in the elderly>lif',
  'History: drugs, diet, red flags>main tool*; Bloods if needed>TFT, calcium, glucose; Rectal exam>impaction',
  'Fibre, fluids, exercise | Bulk laxative; then osmotic: macrogol | Stimulant: senna, especially with opioids | Enema for impaction',
  'New change 60+ or weight loss, bleeding: cancer>c; Absolute constipation with vomiting: obstruction>e; Faecal impaction causing delirium>s',
  'Any patient on regular opioids gets a stimulant laxative with them.')

N(40, 'Appendicitis', 'gut', 'app',
  'The appendix opening blocks → bacteria multiply → it swells, then can burst',
  '10 to 20 · any age',
  'Central pain moving to the right iliac fossa>rif; Off food, nausea>epi; Low fever>head; Pain on coughing, guarding>rif',
  'Clinical with Alvarado>pain shift, RIF tenderness, fever, raised white count*; Bloods>raised WCC and CRP; Pregnancy test>every woman of child-bearing age; Ultrasound or CT>if unsure',
  'Nil by mouth, IV fluids, analgesia | IV antibiotics | Laparoscopic appendicectomy',
  'Perforation and peritonitis>e; Appendix abscess or mass>s; Ectopic pregnancy mimics it>e',
  'Pain starts in the middle, then moves to McBurney\'s point as the parietal peritoneum gets involved.')

N(41, 'Gallstones, biliary colic and cholecystitis', 'hepat', 'gb',
  'Cholesterol crystals form stones → a stone blocks the gallbladder neck → colic; if it stays stuck, the wall inflames',
  'Fat, female, forty, fertile · rapid weight loss · haemolysis',
  'Right upper pain after fatty food>ruq; Pain to the right shoulder tip>rarm; Fever with cholecystitis>head; Murphy\'s sign: stops breathing in when pressed>ruq',
  'Ultrasound abdomen>stones, thick wall, fluid around*; LFTs>usually normal unless a duct stone; FBC, CRP>inflammation',
  'Analgesia, NSAID or opioid | Cholecystitis: IV fluids, antibiotics | Laparoscopic cholecystectomy within 1 week | Duct stones: ERCP',
  'Jaundice, fever and pain: cholangitis>e; Pancreatitis from a stone>e; Empyema or perforation>e',
  'Biliary colic comes and goes; cholecystitis stays and adds a fever.')

N(42, 'Acute cholangitis', 'hepat', 'duct',
  'A stone or tumour blocks the bile duct → bile stagnates and gets infected → bacteria pour into the blood',
  'Gallstones · after ERCP · strictures, cancer',
  'Fever and rigors>head; Jaundice>eyes; Right upper pain>ruq; Confusion and low BP: Reynolds\' pentad>mind',
  'Bloods>raised bilirubin, ALP, WCC, CRP; Blood cultures>the bug; Ultrasound>dilated ducts*; MRCP>stone or stricture',
  'Sepsis six | IV antibiotics | ERCP to drain within 24 to 48 h, sooner if septic',
  'Septic shock>e; Liver abscess>e; Kidney failure>e',
  'Charcot\'s triad: fever, jaundice, right upper pain. Drain it or it kills.')

N(43, 'Acute pancreatitis', 'hepat', 'panc',
  'Gallstones or alcohol trigger enzyme release inside the pancreas → it digests itself → inflammation spreads through the body',
  'Gallstones: older women · alcohol: men · drugs, high triglycerides, trauma, ERCP',
  'Severe epigastric pain through to the back>epi; Better sitting forward>back; Vomiting>mouth; Bruising on flanks or navel>loin',
  'Serum lipase or amylase>over 3 times normal*; Ultrasound>gallstones; Glasgow score>severity at 48 h; CT>if unsure or not improving',
  'Goal-directed IV fluids, analgesia, oxygen if needed | Early feeding; no routine antibiotics | Gallstones: ERCP if obstructed; cholecystectomy same admission | Alcohol: stop, support',
  'Severe: organ failure, high Glasgow score>e; Necrosis or pseudocyst>s; Low calcium, ARDS>e',
  'GET SMASHED: Gallstones, Ethanol, Trauma, Steroids, Mumps, Autoimmune, Scorpion, Hyperlipidaemia, ERCP, Drugs.')

N(44, 'Abdominal aortic aneurysm', 'limb', 'aorta',
  'The aortic wall weakens and balloons → it grows slowly → past 5.5 cm the risk of rupture climbs',
  '65+ men · smokers · high BP · family history',
  'Usually silent, found on screening>abdo; Pulsatile, expansile mass>abdo; Rupture: sudden pain to the back>back; Collapse, low BP>heart',
  'Ultrasound>diameter, men 65+ screening*; CT angiogram>planning repair or suspected rupture',
  'Under 4.5 cm: yearly scan; 4.5 to 5.4: 3-monthly | Stop smoking, BP and statin | 5.5 cm+, growing over 1 cm a year, or symptoms: repair | Rupture: permissive hypotension, theatre',
  'Rupture: pain plus shock>e; Tender aneurysm>e; Leg ischaemia from emboli>e',
  'Known AAA plus back pain plus low BP = rupture until proven otherwise.')

N(45, 'GI perforation and peritonitis', 'gut', 'perit',
  'A hole in the gut lets air and contents out → the peritoneum inflames → sepsis follows fast',
  'Peptic ulcer, diverticulitis, appendicitis · bowel obstruction · after scopes',
  'Sudden severe pain>abdo; Rigid, board-like abdomen>abdo; Lying still, pain on any movement>abdo; Fever, fast pulse>heart',
  'Erect chest X-ray>air under the diaphragm; CT abdomen>free air and the source*; Bloods>lactate, FBC, CRP, amylase, group and save',
  'Sepsis six, nil by mouth, NG tube | IV antibiotics, fluids, analgesia | Emergency laparotomy or laparoscopy',
  'Septic shock>e; Raised lactate>e; Elderly may have few signs>e',
  'Rigid abdomen with free air = surgeon now.')

N(46, 'Sepsis', 'blood', 'flow',
  'An infection triggers an out-of-control body response → vessels leak and dilate → organs lose perfusion',
  'Any age · extremes of age · immunosuppressed, diabetes · lines, recent surgery',
  'High or very low temperature>head; New confusion>mind; Breathing fast>lungs; Fast pulse, low BP>heart; Mottled skin, no urine>skin',
  'NEWS2>5 or more, or a red flag; Lactate>over 2 is worrying, over 4 high risk*; Blood cultures>before antibiotics; Source>urine, CXR, wounds',
  'Sepsis six within 1 hour: oxygen, cultures, IV antibiotics, fluids, lactate, urine output | Find and control the source | Vasopressors in ICU if BP doesn\'t respond',
  'Systolic 90 or less, lactate over 4>e; Neutropenic sepsis: antibiotics within 1 hour>e; No urine for 18 h>e',
  'Give 3, take 3, within 1 hour.')

N(47, 'Pelvic inflammatory disease', 'gut', 'perit',
  'Chlamydia or gonorrhoea climb from the cervix → the tubes and pelvis inflame → scarring blocks the tubes',
  'Sexually active young women · new partners · IUD insertion',
  'Lower abdominal pain>supra; Abnormal discharge>genit; Pain during sex>genit; Fever>head; Cervical motion tenderness>supra',
  'Pregnancy test>exclude ectopic first*; Swabs>chlamydia and gonorrhoea NAAT; Bloods>CRP, WCC',
  'Start antibiotics on suspicion: ceftriaxone IM, then doxycycline and metronidazole for 14 days | No sex until treated; partner notification | Admit if severe or pregnant',
  'Ectopic pregnancy mimics it>e; Tubo-ovarian abscess>e; Infertility and ectopic later>r',
  'Treat early on suspicion: every flare scars the tubes.')

N(48, 'Intestinal obstruction and volvulus', 'gut', 'small',
  'Something blocks the bowel → gas and fluid build up behind it → vomiting, distension, risk of strangulation',
  'Small bowel: adhesions, hernias · large bowel: cancer, volvulus',
  'Colicky abdominal pain>abdo; Vomiting: early in small bowel>mouth; Distension>abdo; No stool or wind>genit; Tinkling bowel sounds>abdo',
  'AXR>dilated loops: small over 3 cm, large over 6, caecum over 9; CT abdomen>level and cause*; Bloods>U&E, lactate',
  'Drip and suck: IV fluids, NG tube, nil by mouth | Adhesions: often settle with conservative care | Sigmoid volvulus: decompress with a flexible scope | Surgery for strangulation, hernia or cancer',
  'Strangulation: constant pain, fever, raised lactate>e; Caecum over 12 cm: about to perforate>e; Low potassium and AKI>s',
  'Small bowel vomits early; large bowel distends early. Coffee bean = volvulus.')

N(49, 'Abdominal pain: the differentials', 'gut', 'perit',
  'Where the pain is → what lies beneath → the pattern and the patient narrow it down',
  'Any age · always ask: pregnant? · older: think vascular first',
  'Right upper: gallbladder, liver>ruq; Epigastric: ulcer, pancreas, heart>epi; Right iliac fossa: appendix, ectopic, ovary>rif; Loin to groin colic: stone>loin; Left iliac fossa: diverticulitis>lif',
  'Pregnancy test>every woman of child-bearing age*; Urine dip>stones, infection; Bloods>FBC, CRP, LFT, lipase, lactate; Imaging by site>ultrasound or CT',
  'ABCDE and analgesia: don\'t withhold it | Nil by mouth if surgical | Imaging to confirm | Treat the cause',
  'Pain out of proportion to signs: ischaemic bowel>e; Older person with back pain and low BP: AAA>e; Pregnant with pain and bleeding: ectopic>e',
  'Map the abdomen into 9 regions, then ask which organ lives there.', k='t')

N([50, 88], 'WHO pain ladder and analgesics', 'blood', 'drug',
  'Pain signals travel from tissue to brain → drugs block them at different points → climb the ladder as pain needs',
  'Every patient in pain · check kidneys, liver, age, other drugs',
  'Mild pain>all; Moderate pain>abdo; Severe pain>back; Nerve pain: burning, shooting>legs',
  'Pain score>before and after each step*; Renal function>NSAIDs, morphine dosing; Respiratory rate and sedation>on opioids',
  'Step 1: paracetamol, plus NSAID if safe | Step 2: weak opioid: codeine or tramadol | Step 3: strong opioid: morphine; adjuvants at any step | Nerve pain: amitriptyline, duloxetine, gabapentin, pregabalin',
  'Opioid toxicity: pinpoint pupils, breathing under 8: naloxone>e; NSAIDs: GI bleed, AKI, asthma>s; Constipation on opioids: laxative from day 1>r',
  'Climb the ladder as pain rises; stay on step 1 drugs as you go up.', k='t')

N(51, 'IV fluids, electrolytes and NG tubes', 'blood', 'fluid',
  'Water and salts are lost or not taken in → replace what is missing, then what is maintained → check daily',
  'Nil by mouth · vomiting, diarrhoea, bleeding · heart or kidney failure needs care',
  'Thirst, dry mouth>mouth; Low BP, fast pulse>heart; Low urine output>supra; Cool peripheries>hands',
  'U&E daily>sodium, potassium, creatinine*; Fluid balance and daily weight>in versus out; NG tube position>pH 5.5 or less, or chest X-ray',
  'Resuscitation: 500 ml crystalloid over 15 min, reassess | Maintenance: 25 to 30 ml per kg per day | Potassium about 1 mmol per kg per day; glucose 50 to 100 g | Replace ongoing losses on top',
  'Hyperkalaemia with ECG changes: calcium gluconate>e; Sodium correction too fast: brain damage>s; Fluid overload in heart failure>s',
  'Resuscitate fast, maintain slowly, measure every day.', k='t')
