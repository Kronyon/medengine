"""v3.6.2 Hammer set E, part 2 of 3 (format in hq6_a.py)."""

Q = r"""
@u 161 2T
s: A 7 year old boy has had a cold for 5 days and now has a swollen, red left eye and a fever. He says it hurts to look around. // Temperature 38.9°C. The left upper and lower lids are swollen and red. The eye is pushed forward, its movements are reduced and painful, and visual acuity is 6/12 in the left eye and 6/6 in the right.
? From which structure has the infection most likely spread?
> Dental abscess ; *Ethmoid sinus ; Frontal sinus ; Lacrimal sac ; Maxillary sinus
= Proptosis, painful restricted eye movements and reduced acuity mean the infection is behind the orbital septum: orbital cellulitis. In children it usually spreads from the ethmoid sinuses through the paper-thin lamina papyracea of the medial orbital wall. He needs admission, IV antibiotics and an urgent CT of the orbits and sinuses.
~ Swollen red lids with normal eye movements and acuity and no proptosis → preseptal cellulitis.
c: cold for 5 days | hurts to look around | pushed forward | movements are reduced and painful | 6/12
m: Ethmoid infection crosses the lamina papyracea into the orbit behind the septum
g: Orbital cellulitis in a child after a cold → ethmoid sinusitis
f: a tender red swelling just below the inner corner of the eye with a watery eye => Lacrimal sac
f: a 16 year old with frontal headache and a soft boggy swelling of the forehead above the eyebrow => Frontal sinus
x: Dental abscess => Spreads to the face or maxillary sinus and is an uncommon source in a child after a cold
x: Frontal sinus => The frontal sinuses are small and poorly developed at this age
x: Lacrimal sac => Dacryocystitis causes a swelling at the inner canthus and rarely orbital cellulitis
x: Maxillary sinus => Can spread through the orbital floor but is a far less common source than the ethmoids

@u 158 2R
s: A 28 year old man with ankylosing spondylitis has had a painful red right eye for 2 days. Bright light makes it worse and his vision is slightly blurred. // Visual acuity is 6/9 in the right eye. The redness is most marked around the cornea, and the right pupil is small and irregular. There is no discharge.
? Which is the most appropriate management?
> Chloramphenicol eye drops and review in 5 days ; Lubricating eye drops ; Prescribe topical prednisolone drops ; Routine optometrist review ; *Same-day referral to ophthalmology
= Pain, photophobia, blurred vision, redness around the cornea and a small irregular pupil in someone with ankylosing spondylitis is acute anterior uveitis. It needs same-day slit lamp examination by ophthalmology to confirm it and start steroid and dilating drops. Steroid drops should not be started without slit lamp examination, because they can worsen herpes keratitis.
~ Gritty red eyes with sticky discharge, normal acuity and normal pupils → conjunctivitis managed in primary care.
c: ankylosing spondylitis | Bright light makes it worse | vision is slightly blurred | around the cornea | small and irregular
m: Inflammation of the iris and ciliary body constricts the pupil and makes it stick to the lens, and moving the iris in light hurts
g: Painful red eye with photophobia, reduced vision and an irregular pupil → same-day ophthalmology
f: gritty red eyes with sticky discharge, normal vision and normal pupils => Chloramphenicol eye drops and review in 5 days
f: gritty dry eyes at the end of the day with normal vision and no redness at rest => Lubricating eye drops
x: Chloramphenicol eye drops and review in 5 days => Treats bacterial conjunctivitis, which does not reduce vision or change the pupil
x: Lubricating eye drops => For dry eye, which does not cause photophobia with an irregular pupil
x: Prescribe topical prednisolone drops => Steroid drops need slit lamp confirmation first, as they can worsen herpes keratitis
x: Routine optometrist review => Too slow; a red eye with reduced vision needs same-day specialist review

@u 165 2L
s: A 79 year old woman says that over the past 3 weeks straight lines in her newspaper look wavy and there is a grey patch in the centre of her vision in the left eye. She smokes 10 cigarettes a day. // Visual acuity is 6/36 in the left eye and 6/9 in the right. Amsler grid testing shows distorted lines in the centre on the left. Fundoscopy shows a raised grey-green area with a small haemorrhage at the left macula.
? Which is the most likely diagnosis?
> Cataract ; Central retinal vein occlusion ; Dry age-related macular degeneration ; Retinal detachment ; *Wet age-related macular degeneration
= Distortion of straight lines with a central blind spot developing over weeks in an older smoker, with a raised macular lesion and haemorrhage, is wet age-related macular degeneration. New vessels leak fluid and blood under the macula. She needs referral to a macular clinic within days for anti-VEGF injections.
~ Gradual central blurring over years with yellow drusen and no distortion → dry AMD.
c: past 3 weeks | look wavy | grey patch in the centre | smokes | small haemorrhage at the left macula
m: Choroidal new vessels grow through Bruch's membrane and leak under the macula, lifting and distorting the photoreceptors
g: Wavy lines and a central blind spot developing over weeks → wet AMD
f: slow central blurring over years with yellow drusen and no distortion => Dry age-related macular degeneration
f: sudden painless loss of vision with haemorrhages scattered through all 4 quadrants => Central retinal vein occlusion
f: flashes, floaters and a curtain spreading in from one side => Retinal detachment
x: Cataract => Causes gradual glare and blurring without distortion or a macular haemorrhage
x: Central retinal vein occlusion => Causes sudden painless loss with haemorrhages throughout the retina
x: Dry age-related macular degeneration => Progresses over years with drusen, without new vessels or haemorrhage
x: Retinal detachment => Starts with flashes and floaters and a peripheral curtain, not central distortion

@u 164 2D
s: A 64 year old man with polymyalgia rheumatica has taken oral prednisolone for 3 years. Over 6 months his vision has become hazy, he is dazzled by oncoming headlights at night and he finds reading harder. // Visual acuity is 6/18 in both eyes. Intraocular pressures are 16 and 17 mmHg. The red reflex is dull, with a dark central shadow in both eyes. The fundi are hard to see but appear normal.
? Which is the most likely cause of his visual symptoms?
> Age-related macular degeneration ; *Cataract ; Diabetic retinopathy ; Open-angle glaucoma ; Retinal vein occlusion
= Long-term corticosteroids cause posterior subcapsular cataract, which lies in the visual axis and gives early glare from headlights and trouble reading. A dull red reflex with a central shadow confirms an opacity in the lens. Steroids can also raise intraocular pressure, but his pressures are normal.
~ Intraocular pressure of 32 mmHg with cupped discs and peripheral field loss on steroids → open-angle glaucoma.
c: oral prednisolone for 3 years | dazzled by oncoming headlights | Intraocular pressures are 16 and 17 | red reflex is dull | dark central shadow
m: Steroids alter the lens epithelium so opaque fibres collect under the posterior capsule in the visual axis
g: Long-term steroids with glare and a dull red reflex → posterior subcapsular cataract
f: intraocular pressure of 32 mmHg with cupped optic discs and peripheral field loss => Open-angle glaucoma
f: dot and blot haemorrhages and hard exudates with a raised HbA1c => Diabetic retinopathy
x: Age-related macular degeneration => Distorts central vision but does not dull the red reflex
x: Diabetic retinopathy => Steroids can cause diabetes, but the fundi look normal and the problem is in the lens
x: Open-angle glaucoma => Steroids can cause it, but his pressures are normal and glaucoma spares central vision until late
x: Retinal vein occlusion => Causes sudden painless loss with retinal haemorrhages

@u 166 2R
s: A 52 year old man is sent to his GP by his optometrist after a routine eye test. He has occasional headaches but otherwise feels well. He has not seen a doctor for 10 years. // The optometrist reports narrowed arterioles with a copper wire appearance, nipping where arteries cross veins, flame-shaped haemorrhages and cotton wool spots in both eyes. The optic discs are normal.
? Which is the most appropriate next step?
> Check fasting glucose ; Fluorescein angiography ; *Measure his blood pressure ; Refer for carotid Doppler ultrasound ; Urgent CT head
= Copper wiring, arteriovenous nipping, flame haemorrhages and cotton wool spots are hypertensive retinopathy, so the first step is to measure his blood pressure. NICE advises same-day specialist referral if the blood pressure is 180/120 mmHg or more with retinal haemorrhage or papilloedema.
~ Dot and blot haemorrhages, microaneurysms and hard exudates → diabetic retinopathy: check glucose or HbA1c.
c: optometrist | not seen a doctor for 10 years | copper wire | nipping where arteries cross veins | flame-shaped haemorrhages
m: Chronic high pressure thickens arteriolar walls, and sharp rises damage capillaries so the nerve fibre layer infarcts as cotton wool spots
g: Copper wiring, AV nipping and flame haemorrhages → measure the blood pressure
f: dot and blot haemorrhages, microaneurysms and hard exudates in a man who is always thirsty => Check fasting glucose
f: loss of vision in one eye for 4 minutes like a curtain coming down, with a carotid bruit => Refer for carotid Doppler ultrasound
x: Check fasting glucose => Diabetic retinopathy gives dot and blot haemorrhages and microaneurysms, not copper wiring
x: Fluorescein angiography => A specialist test that does not come before measuring his blood pressure
x: Refer for carotid Doppler ultrasound => For amaurosis fugax or retinal emboli, not this pattern
x: Urgent CT head => His discs are normal and he has no neurological signs

@u 55 2L
s: A 44 year old woman has noticed blood-stained discharge from her right nipple on several occasions over 6 weeks. It comes from a single opening on the nipple. She is not breastfeeding and takes no medication. // There is no palpable lump, skin change or nipple retraction. Pressure at the 9 o'clock position at the edge of the areola produces a bead of bloody fluid from one duct.
? Which is the most likely cause?
> Duct ectasia ; *Intraductal papilloma ; Paget's disease of the nipple ; Periductal mastitis ; Prolactinoma
= Bloody discharge from a single duct with no lump in a woman in her 40s is most often an intraductal papilloma, a benign wart-like growth in a large duct near the nipple. Ductal carcinoma in situ must be excluded, so she needs triple assessment at the breast clinic.
~ Thick green or cream discharge from several ducts with a slit-like retracted nipple around the menopause → duct ectasia.
c: blood-stained discharge | single opening | 6 weeks | no palpable lump | one duct
m: A fragile papillary growth in a large duct under the areola bleeds and drains through one opening
g: Bloody discharge from one duct with no lump → intraductal papilloma
f: thick green discharge from several ducts with a slit-like nipple retraction in a 54 year old => Duct ectasia
f: milky discharge from both breasts, missed periods and headaches => Prolactinoma
f: a crusted eczema-like nipple that has spread onto the areola => Paget's disease of the nipple
x: Duct ectasia => Gives thick coloured discharge from several ducts around the menopause, often with slit-like retraction
x: Paget's disease of the nipple => Causes an eczema-like rash on the nipple, not discharge from one duct with a normal nipple
x: Periductal mastitis => Affects young smokers with pain, inflammation and sometimes an abscess
x: Prolactinoma => Causes milky discharge from many ducts in both breasts, not blood from one duct

@u 54 1D
s: A 27 year old woman who is breastfeeding her 3 week old baby has had a painful, red, wedge-shaped area on her left breast for 2 days, with fever and aches. She has kept breastfeeding from both sides and expressing, but it is no better after 24 hours. She has no allergies. // Temperature 38.4°C. There is a tender, warm, red area in the upper outer quadrant with no fluctuant swelling.
? Which is the most appropriate management?
> Cabergoline to stop lactation ; Clarithromycin ; *Flucloxacillin and continue breastfeeding ; Incision and drainage ; Stop breastfeeding from the left breast
= Lactational mastitis that has not improved after 12 to 24 hours of effective milk removal needs an antibiotic. Flucloxacillin for 10 to 14 days covers Staphylococcus aureus. Breastfeeding should continue from both breasts, because emptying the breast helps recovery and the milk is safe for the baby.
~ A tender fluctuant lump → breast abscess, usually treated with ultrasound-guided aspiration and antibiotics.
c: breastfeeding | wedge-shaped | no better after 24 hours | no allergies | no fluctuant swelling
m: Milk stasis lets Staphylococcus aureus from the baby's mouth or the nipple multiply in the breast
g: Mastitis not settling after 24 hours of milk removal → flucloxacillin, and keep feeding
f: a penicillin allergy with a rash => Clarithromycin
f: a large abscess that has failed repeated needle aspiration, with thinned skin over it => Incision and drainage
x: Cabergoline to stop lactation => Not needed; stopping feeds causes milk stasis and makes mastitis worse
x: Clarithromycin => For penicillin allergy, and she has none
x: Incision and drainage => For an abscess that fails aspiration, and she has no fluctuant swelling
x: Stop breastfeeding from the left breast => Stopping causes milk stasis and raises the risk of an abscess

@u 81 1L
s: A 64 year old man has noticed a painless swelling of his right scrotum that has grown slowly over 8 months. It feels heavy by the end of the day. // There is a smooth, non-tender, fluctuant swelling of the right hemiscrotum. The examiner can get above it, and the testis cannot be felt separately from it. It glows brightly when a pen torch is held against it.
? Which is the most likely diagnosis?
> Epididymal cyst ; *Hydrocele ; Indirect inguinal hernia ; Testicular tumour ; Varicocele
= A painless fluctuant scrotal swelling that transilluminates, that the examiner can get above and in which the testis cannot be felt separately, is a hydrocele: fluid in the tunica vaginalis around the testis. An ultrasound is advised to check the testis inside, especially in younger men.
~ A transilluminating swelling above and behind the testis that can be felt separately from it → epididymal cyst.
c: painless | grown slowly over 8 months | can get above it | testis cannot be felt separately | glows brightly
m: Fluid collects between the layers of the tunica vaginalis, which wrap around the front and sides of the testis
g: Transilluminates, can get above it and the testis is not felt separately → hydrocele
f: a transilluminating swelling above and behind the testis, which is felt separately => Epididymal cyst
f: a swelling the examiner cannot get above, with a cough impulse => Indirect inguinal hernia
f: a soft swelling like a bag of worms above the left testis that empties on lying down => Varicocele
x: Epididymal cyst => Transilluminates but sits above and behind a testis that is felt separately
x: Indirect inguinal hernia => The examiner cannot get above it, and there may be a cough impulse
x: Testicular tumour => A hard, irregular lump in the testis that does not transilluminate
x: Varicocele => Feels like a bag of worms, usually on the left, and does not transilluminate

@k d:ccb 3D
s: A 38 year old woman has had episodes of central chest tightness at rest for 2 months, mostly between 4 and 6 am, lasting 10 minutes and easing with glyceryl trinitrate spray. She smokes. During an episode in the emergency department her ECG shows ST elevation in leads II, III and aVF that settles completely within 15 minutes. Troponin is not raised. Coronary angiography shows smooth, unobstructed coronary arteries. She is started on diltiazem.
? Which is the main purpose of diltiazem in her treatment?
> Lower her heart rate to reduce oxygen demand ; Prevent platelet aggregation on a ruptured plaque ; *Prevent spasm of the coronary arteries ; Reduce afterload to improve ventricular function ; Stabilise atheromatous plaques
= Chest pain at rest in the early morning, transient ST elevation that resolves, no troponin rise and normal coronary arteries are vasospastic, or Prinzmetal, angina. Calcium channel blockers relax vascular smooth muscle and are first line to prevent coronary artery spasm. Beta-blockers alone can make spasm worse, and stopping smoking matters.
~ Exertional angina with a fixed stenosis → the aim of treatment is to reduce oxygen demand, usually with a beta-blocker.
c: at rest | between 4 and 6 am | ST elevation | settles completely | smooth, unobstructed coronary arteries
m: Calcium entry drives contraction of coronary smooth muscle, so blocking it stops the artery clamping shut
g: Rest angina with transient ST elevation and normal arteries → calcium channel blocker to prevent spasm
f: exertional angina from a fixed 90% stenosis with a resting heart rate of 96 bpm => Lower her heart rate to reduce oxygen demand
x: Lower her heart rate to reduce oxygen demand => How rate-limiting drugs help fixed stenosis, but her arteries are smooth
x: Prevent platelet aggregation on a ruptured plaque => Antiplatelets do this, and she has no plaque or troponin rise
x: Reduce afterload to improve ventricular function => A minor effect, and her ventricle is not failing
x: Stabilise atheromatous plaques => Statins do this, and her arteries have no atheroma

@u 94 1L
s: A 34 year old woman has had a fever and headache for 3 days. Today her partner found her confused and saying strange things, and she then had a seizure. // Temperature 38.8°C, GCS 12. There is no neck stiffness or rash. MRI shows high signal in the left temporal lobe.
$ CSF white cells ; 85 per µL, mostly lymphocytes ; <5
$ CSF protein ; 0.82 g/L ; 0.15–0.45
$ CSF to blood glucose ratio ; 0.62 ; >0.6
$ CSF Gram stain ; no organisms seen ;
? Which is the most likely diagnosis?
> Bacterial meningitis ; Brain abscess ; *Herpes simplex encephalitis ; Subarachnoid haemorrhage ; Tuberculous meningitis
= Fever with confusion, odd behaviour and a seizure, a lymphocytic CSF with a normal glucose ratio and temporal lobe change on MRI are herpes simplex encephalitis. IV aciclovir should start as soon as it is suspected, without waiting for the CSF HSV PCR.
~ Fever, neck stiffness and a turbid CSF full of neutrophils with a low glucose → bacterial meningitis.
c: saying strange things | seizure | no neck stiffness | left temporal lobe | CSF white cells 85
m: HSV reaches the temporal lobes along olfactory and trigeminal pathways and causes haemorrhagic inflammation there
g: Fever, behaviour change, seizures and temporal lobe change → HSV encephalitis: give aciclovir
f: neck stiffness, a purpuric rash and CSF with 2000 neutrophils and a low glucose => Bacterial meningitis
f: a ring-enhancing lesion on contrast CT in a man with a dental abscess => Brain abscess
f: weeks of headache and cranial nerve palsies in a man from Pakistan with a CSF glucose ratio of 0.3 => Tuberculous meningitis
x: Bacterial meningitis => Gives a neutrophil CSF with a low glucose and usually neck stiffness
x: Brain abscess => Shows a ring-enhancing mass rather than diffuse temporal lobe change
x: Subarachnoid haemorrhage => Starts with a thunderclap headache rather than days of fever, and the CSF shows blood or xanthochromia
x: Tuberculous meningitis => Develops over weeks with a very low CSF glucose

@u 91 2R
s: A 46 year old woman had a sudden, severe occipital headache while lifting a box 14 hours ago, the worst she has ever had. It reached its peak within a minute. She vomited once. // GCS 15. There is mild neck stiffness and no focal neurological deficit. A CT head performed 13 hours after the onset of the headache is normal.
? Which is the most appropriate next step?
> CT head in 24 hours ; Discharge with analgesia ; *Lumbar puncture ; MRI brain as an outpatient ; Start oral nimodipine
= A thunderclap headache peaking within a minute is subarachnoid haemorrhage until proven otherwise. CT is very sensitive within 6 hours of onset, but after 6 hours a normal CT does not exclude it. NICE advises a lumbar puncture at least 12 hours after the headache began, looking for xanthochromia.
~ Normal CT done within 6 hours of onset → SAH is very unlikely and a lumbar puncture is not routinely needed.
c: reached its peak within a minute | 14 hours ago | neck stiffness | CT head performed 13 hours after the onset
m: Red cells in the CSF break down to bilirubin over about 12 hours, giving xanthochromia that lasts up to 2 weeks
g: Thunderclap headache with a normal CT after 6 hours → LP at 12 hours or more for xanthochromia
f: SAH confirmed on CT from a posterior communicating artery aneurysm awaiting coiling => Start oral nimodipine
x: CT head in 24 hours => CT sensitivity falls further with time, so repeating it does not exclude SAH
x: Discharge with analgesia => Missing a warning bleed risks a fatal rebleed
x: MRI brain as an outpatient => Far too slow for a possible aneurysmal bleed
x: Start oral nimodipine => Given once SAH is confirmed, to reduce delayed cerebral ischaemia from vasospasm

@u 42 1L
s: A 74 year old woman has had pain in the right upper abdomen for 2 days, with rigors and yellow skin since yesterday. She had biliary colic 6 months ago and is on the waiting list for a cholecystectomy. // Temperature 39.1°C, pulse rate 112 bpm, BP 104/66 mmHg. She is jaundiced and tender in the right upper quadrant.
$ Bilirubin ; 78 µmol/L ; <17
$ ALP ; 412 IU/L ; 25–115
$ ALT ; 96 IU/L ; 10–50
$ White cell count ; 18.6 × 10⁹/L ; 4.0–11.0
$ Amylase ; 64 U/L ; <100
? Which is the most likely diagnosis?
> Acute cholecystitis ; Acute pancreatitis ; *Ascending cholangitis ; Biliary colic ; Hepatitis A
= Fever with rigors, right upper quadrant pain and jaundice is Charcot's triad of ascending cholangitis: a stone blocks the common bile duct and the trapped bile becomes infected. The obstructive LFTs and normal amylase fit. She needs blood cultures, IV antibiotics, fluids and drainage of the bile duct, usually by ERCP.
~ Fever and right upper quadrant pain with Murphy's sign but a normal bilirubin → acute cholecystitis.
c: rigors | yellow skin | biliary colic 6 months ago | Temperature 39.1 | ALP 412
m: A stone in the common bile duct stops bile flow, and bacteria climb from the duodenum into the stagnant bile
g: Fever, RUQ pain and jaundice → cholangitis needing antibiotics and drainage
f: fever and right upper quadrant pain with Murphy's sign and a normal bilirubin => Acute cholecystitis
f: epigastric pain going through to the back with an amylase of 1600 => Acute pancreatitis
f: an hour of right upper quadrant pain after a fatty meal with normal blood tests and no fever => Biliary colic
x: Acute cholecystitis => Inflammation of the gallbladder does not usually cause jaundice or an obstructive picture
x: Acute pancreatitis => The amylase is normal
x: Biliary colic => Brief pain without fever, rigors or jaundice
x: Hepatitis A => Raises the ALT far more than the ALP and does not cause rigors

@k x:lowerscope 2R
s: A 66 year old man has had looser, more frequent stools for 7 weeks. The change began during a 3 week visit to family in India. Two stool cultures and microscopy for ova, cysts and parasites were negative. He has lost 4 kg and feels tired. // Abdominal and rectal examinations are normal.
$ Haemoglobin ; 104 g/L ; 130–175
$ MCV ; 73 fL ; 80–96
$ Ferritin ; 9 µg/L ; 12–200
$ Faecal immunochemical test ; 186 µg Hb/g faeces ; <10
? Which is the most appropriate investigation to confirm the diagnosis?
> Abdominal ultrasound ; *Colonoscopy ; Repeat stool culture ; Serology for Entamoeba histolytica ; Tissue transglutaminase antibody
= A persistent change in bowel habit with weight loss, iron deficiency anaemia and a strongly positive FIT in a man over 60 needs a suspected cancer referral, and colonoscopy with biopsy confirms colorectal cancer. The trip to India is a distractor: negative stool tests and a blood-loss anaemia point to a bowel lesion rather than an infection.
~ Bloody diarrhoea, fever and a liver abscess after the same trip → amoebiasis, treated with metronidazole.
c: 7 weeks | India | microscopy for ova, cysts and parasites were negative | lost 4 kg | Faecal immunochemical test 186
m: A bleeding colonic tumour loses iron slowly and changes bowel habit as it narrows the lumen
g: Over 60 with changed bowel habit, iron deficiency and a positive FIT → colonoscopy, whatever the travel history
f: bloody diarrhoea, fever and a tender liver with a cystic lesion after the same trip => Serology for Entamoeba histolytica
f: a 30 year old with bloating, iron deficiency and a normal FIT whose diarrhoea began long before the trip => Tissue transglutaminase antibody
x: Abdominal ultrasound => Cannot see the colonic lining and gives no tissue diagnosis
x: Repeat stool culture => Two negative sets and a blood-loss anaemia make infection unlikely
x: Serology for Entamoeba histolytica => Amoebiasis gives bloody diarrhoea or a liver abscess, not this picture with negative microscopy
x: Tissue transglutaminase antibody => Worth testing in iron deficiency, but coeliac disease does not explain a strongly positive FIT

@k d:atypicals 2D
s: A 26 year old woman with schizophrenia has been well on risperidone for 8 months with no psychotic symptoms. She has not had a period for 5 months, has noticed milky discharge from both nipples and is upset by a reduced sex drive. A pregnancy test is negative. She wants to stay on an antipsychotic. // Her BMI is 31 kg/m².
$ Prolactin ; 2850 mIU/L ; <500
$ HbA1c ; 44 mmol/mol ; 20–42
? Which is the most appropriate antipsychotic to switch to?
> Amisulpride ; *Aripiprazole ; Haloperidol ; Olanzapine ; Sulpiride
= Risperidone has caused hyperprolactinaemia, with amenorrhoea, galactorrhoea and a low libido. Aripiprazole is a partial dopamine agonist that does not raise prolactin and often lowers it, and it has a low risk of weight gain and diabetes, which matters with her BMI and HbA1c. Amisulpride, sulpiride and haloperidol all raise prolactin, and olanzapine causes the most weight gain.
~ Schizophrenia that has not responded to 2 adequate antipsychotic trials → clozapine.
c: risperidone | not had a period for 5 months | milky discharge | Prolactin 2850 | HbA1c 44
m: Dopamine normally holds back prolactin release, and D2 blockade in the tuberoinfundibular pathway lifts that brake
g: Antipsychotic hyperprolactinaemia with metabolic risk → aripiprazole
x: Amisulpride => Raises prolactin even more than risperidone
x: Haloperidol => A potent D2 blocker that raises prolactin and causes extrapyramidal side effects
x: Olanzapine => Raises prolactin less but causes marked weight gain and diabetes, and she is already at risk
x: Sulpiride => Raises prolactin markedly

@k b:jaundice 1L
s: A 21 year old man noticed that the whites of his eyes turned yellow during a 2 day stomach bug, when he was eating very little. He otherwise felt well, and the yellow has nearly gone. // Examination is normal, with no liver or spleen enlargement.
$ Bilirubin ; 41 µmol/L ; <17
$ Conjugated bilirubin ; 4 µmol/L ; <7
$ ALT ; 22 IU/L ; 10–50
$ ALP ; 74 IU/L ; 25–115
$ Haemoglobin ; 152 g/L ; 130–175
$ Reticulocytes ; 1.1% ; 0.5–2.5
? Which is the most likely diagnosis?
> Crigler-Najjar syndrome ; Dubin-Johnson syndrome ; *Gilbert syndrome ; Haemolytic anaemia ; Hepatitis A
= A mild unconjugated hyperbilirubinaemia that appears with fasting or illness, with normal liver enzymes, haemoglobin and reticulocytes, is Gilbert syndrome. Reduced UDP-glucuronosyltransferase activity slows conjugation. It is harmless, needs no treatment and affects about 1 in 20 people.
~ Raised unconjugated bilirubin with a low haemoglobin and raised reticulocytes and LDH → haemolytic anaemia.
c: stomach bug | eating very little | Conjugated bilirubin 4 | ALT 22 | Reticulocytes 1.1
m: Glucuronidation of bilirubin is slow, and fasting or illness tips the balance so unconjugated bilirubin builds up
g: Isolated unconjugated bilirubin with fasting, normal LFTs and no haemolysis → Gilbert syndrome
f: a falling haemoglobin, reticulocytes of 8% and a raised LDH => Haemolytic anaemia
f: a newborn with severe unconjugated jaundice that needs phototherapy for months => Crigler-Najjar syndrome
f: a raised conjugated bilirubin with normal enzymes and a black liver on biopsy => Dubin-Johnson syndrome
x: Crigler-Najjar syndrome => Causes severe unconjugated jaundice from birth
x: Dubin-Johnson syndrome => Raises conjugated bilirubin, which is normal here
x: Haemolytic anaemia => His haemoglobin and reticulocytes are normal
x: Hepatitis A => Would raise the ALT many times over

@u 43 1L
s: A 47 year old man has had severe constant epigastric pain going through to his back for 8 hours, with repeated vomiting. He drinks about 50 units of alcohol a week. Sitting forward eases the pain a little. // Temperature 37.8°C, pulse rate 108 bpm, BP 122/76 mmHg. The epigastrium is tender with guarding.
$ Amylase ; 1640 U/L ; <100
$ ALT ; 64 IU/L ; 10–50
$ Bilirubin ; 21 µmol/L ; <17
$ Adjusted calcium ; 2.14 mmol/L ; 2.20–2.60
$ Troponin T ; 8 ng/L ; <14
? Which is the most likely diagnosis?
> Acute cholecystitis ; *Acute pancreatitis ; Inferior myocardial infarction ; Perforated duodenal ulcer ; Ruptured abdominal aortic aneurysm
= Severe epigastric pain going through to the back, eased by sitting forward, with vomiting in a heavy drinker and an amylase more than 3 times the upper limit is acute pancreatitis. Gallstones and alcohol cause most cases. Severity is scored with the modified Glasgow criteria, and a low calcium is one of them.
~ Sudden pain with a rigid abdomen and free gas under the diaphragm → perforated duodenal ulcer, though the amylase can be mildly raised.
c: through to his back | 50 units | Sitting forward eases | Amylase 1640 | Troponin T 8
m: Pancreatic enzymes activate inside the gland and digest it, and leaking enzymes inflame the retroperitoneum
g: Epigastric pain to the back with amylase over 3 times normal → acute pancreatitis
f: sudden pain, a board-like abdomen and free air under the diaphragm on an erect chest X-ray => Perforated duodenal ulcer
f: right upper quadrant pain, Murphy's sign and a thickened gallbladder wall with a normal amylase => Acute cholecystitis
f: a 74 year old smoker with back pain, collapse and a pulsatile mass => Ruptured abdominal aortic aneurysm
x: Acute cholecystitis => Pain is in the right upper quadrant with Murphy's sign, and amylase is not this high
x: Inferior myocardial infarction => Can cause epigastric pain, but the troponin is normal
x: Perforated duodenal ulcer => Gives sudden peritonitis with a rigid abdomen, and the amylase is rarely over 1000
x: Ruptured abdominal aortic aneurysm => Unlikely at 47 with a normal blood pressure and no pulsatile mass

@u 10 2L
s: A 62 year old woman has had tiredness for 4 months and pins and needles in both feet for 6 weeks. She has vitiligo and hypothyroidism treated with levothyroxine. She eats meat and drinks no alcohol. // Her tongue is smooth and red. Vibration sense and joint position sense are reduced in both feet.
$ Haemoglobin ; 92 g/L ; 115–150
$ MCV ; 114 fL ; 80–96
$ Platelets ; 142 × 10⁹/L ; 150–400
$ TSH ; 2.1 mU/L ; 0.3–4.2
$ Folate ; 6.2 µg/L ; >3.0
? Which is the most likely cause of her anaemia?
> Alcohol excess ; Folate deficiency ; Hypothyroidism ; Myelodysplastic syndrome ; *Vitamin B12 deficiency
= A macrocytic anaemia with glossitis and loss of vibration and joint position sense in a woman with other autoimmune conditions is vitamin B12 deficiency, most likely from pernicious anaemia. Her folate is normal and she is euthyroid. Neurological features mean prompt IM hydroxocobalamin, and folic acid must not be given on its own.
~ Macrocytic anaemia with a low folate, a poor diet and no neurological signs → folate deficiency.
c: pins and needles | vitiligo | smooth and red | Vibration sense and joint position sense | MCV 114
m: Autoantibodies destroy gastric parietal cells and intrinsic factor, so B12 is not absorbed and both DNA synthesis and myelin suffer
g: Macrocytosis with dorsal column signs and autoimmunity → B12 deficiency
f: a folate of 1.4, a poor diet and no neurological signs => Folate deficiency
f: a raised GGT, 60 units a week and an MCV of 104 with a normal haemoglobin => Alcohol excess
f: an 80 year old with low counts in all 3 cell lines and dysplastic cells on the blood film => Myelodysplastic syndrome
x: Alcohol excess => She does not drink
x: Folate deficiency => Her folate is normal, and folate deficiency does not damage the dorsal columns
x: Hypothyroidism => Can cause a mild macrocytosis, but her TSH is normal on treatment
x: Myelodysplastic syndrome => Possible at this age, but her neurological signs and autoimmunity point to B12

@u 74 2R
s: A 39 year old woman has noticed a painless lump in the front of her neck for 2 months. She feels well. // There is a firm 2.5 cm nodule in the right lobe of the thyroid that moves on swallowing. There is no lymphadenopathy. Ultrasound shows a solid hypoechoic nodule with microcalcifications and irregular margins, graded U4.
$ TSH ; 1.8 mU/L ; 0.3–4.2
$ Free T4 ; 15 pmol/L ; 12–22
? Which is the most appropriate next investigation?
> CT of neck and chest ; Radioisotope thyroid uptake scan ; Serum calcitonin ; Thyroid peroxidase antibodies ; *Ultrasound-guided fine needle aspiration
= A euthyroid woman with a solid nodule that has suspicious ultrasound features, graded U4, needs ultrasound-guided fine needle aspiration for cytology, reported on the Thy scale. The result decides between surgery and surveillance. An uptake scan is for nodules with a low TSH, to look for a hot nodule.
~ Thyroid nodule with a suppressed TSH and raised free T4 → radioisotope uptake scan to look for a toxic nodule.
c: painless lump | moves on swallowing | microcalcifications and irregular margins | U4 | TSH 1.8
m: Cells drawn from the nodule show whether the follicular cells are benign, indeterminate or malignant
g: Euthyroid solid nodule with suspicious ultrasound → US-guided FNA
f: a nodule with a TSH below 0.01 and a raised free T4 => Radioisotope thyroid uptake scan
f: a nodule with diarrhoea, flushing and a family history of phaeochromocytoma => Serum calcitonin
x: CT of neck and chest => For staging once cancer is confirmed, or for retrosternal extension
x: Radioisotope thyroid uptake scan => Used when the TSH is low, and hot nodules are rarely malignant
x: Serum calcitonin => Checked when medullary carcinoma is suspected, as in MEN 2
x: Thyroid peroxidase antibodies => Support autoimmune thyroiditis but do not assess a nodule

@u 72 1L
s: A 33 year old woman has felt anxious and shaky for 3 months. She has lost 5 kg despite eating more, her periods have become lighter and she cannot tolerate warm rooms. Her GP had suggested anxiety. // Pulse rate 112 bpm, irregularly irregular. She has a fine tremor, warm moist skin and lid lag.
$ TSH ; <0.01 mU/L ; 0.3–4.2
$ Free T4 ; 41 pmol/L ; 12–22
$ Haemoglobin ; 131 g/L ; 115–150
? Which is the most likely diagnosis?
> Excess caffeine intake ; Generalised anxiety disorder ; Perimenopause ; Phaeochromocytoma ; *Thyrotoxicosis
= Weight loss with a large appetite, heat intolerance, tremor, lid lag, lighter periods and atrial fibrillation with a suppressed TSH and high free T4 are thyrotoxicosis. Anxiety can mimic the symptoms but does not change thyroid function. The next step is to find the cause, such as Graves' disease, with TSH receptor antibodies.
~ Episodes of headache, sweating and palpitations with surges in blood pressure and normal thyroid tests → phaeochromocytoma.
c: lost 5 kg despite eating more | cannot tolerate warm rooms | irregularly irregular | lid lag | TSH <0.01
m: Excess thyroid hormone raises the metabolic rate and sensitises tissues to adrenaline
g: Suppressed TSH with a high free T4 and hypermetabolic symptoms → thyrotoxicosis
f: episodes of headache, sweating and palpitations with a BP of 220/120 mmHg and normal thyroid tests => Phaeochromocytoma
f: hot flushes and irregular periods in a 49 year old with a normal TSH and a raised FSH => Perimenopause
x: Excess caffeine intake => Causes tremor and palpitations but not weight loss with abnormal thyroid tests
x: Generalised anxiety disorder => Mimics the symptoms but does not suppress the TSH or cause lid lag
x: Perimenopause => Unlikely at 33, and it causes flushes rather than heat intolerance with weight loss
x: Phaeochromocytoma => Causes episodes with hypertension, and her thyroid tests are abnormal

@u 163 1L
s: A 68 year old man had sudden loss of vision in his left eye this morning, like a curtain coming down from above. It lasted 4 minutes and then fully recovered. He has no headache, jaw pain or scalp tenderness. He smokes and has type 2 diabetes. // Visual acuity is 6/6 in both eyes. Fundoscopy is normal. There is a left carotid bruit. ESR is 12 mm/h.
? Which is the most likely diagnosis?
> *Amaurosis fugax ; Central retinal artery occlusion ; Migraine with aura ; Retinal detachment ; Vitreous haemorrhage
= Transient painless loss of vision in one eye, like a curtain, lasting minutes with full recovery, is amaurosis fugax: a retinal TIA, usually from a carotid embolus. The bruit and his vascular risk factors fit. He needs aspirin 300 mg, same-day TIA assessment and carotid Doppler imaging.
~ Sudden painless loss that does not recover, with a cherry-red spot at the macula → central retinal artery occlusion.
c: like a curtain coming down | lasted 4 minutes and then fully recovered | no headache, jaw pain or scalp tenderness | left carotid bruit | ESR is 12
m: A cholesterol or platelet embolus from the carotid briefly blocks the central retinal artery and then breaks up
g: Transient monocular curtain lasting minutes → amaurosis fugax, treated as a TIA
f: loss of vision that does not recover, with a cherry-red spot at the macula => Central retinal artery occlusion
f: shimmering zigzag lines in both visual fields over 20 minutes followed by headache => Migraine with aura
f: flashes and floaters then a shadow spreading in from one side that persists => Retinal detachment
x: Central retinal artery occlusion => The loss persists, with a pale retina and a cherry-red spot
x: Migraine with aura => Gives positive visual symptoms building over 5 to 60 minutes, usually in both visual fields
x: Retinal detachment => Starts with flashes and floaters and does not recover within minutes
x: Vitreous haemorrhage => Gives floaters or loss that persists, and the fundal view would be obscured

@k b:bone 2L
s: A 73 year old man has had a dull ache in his right shin for a year, worse at night. His wife says his hats no longer fit and he has become slightly deaf. He feels otherwise well. // His right tibia is bowed and warm to touch.
$ ALP ; 584 IU/L ; 25–115
$ Adjusted calcium ; 2.38 mmol/L ; 2.20–2.60
$ Phosphate ; 1.04 mmol/L ; 0.80–1.50
$ PTH ; 4.2 pmol/L ; 1.6–8.5
$ PSA ; 1.8 µg/L ; <4.5
? Which is the most likely diagnosis?
> Bone metastases ; Multiple myeloma ; Osteomalacia ; *Paget's disease of bone ; Primary hyperparathyroidism
= A very high ALP with a normal calcium, phosphate and PTH, bone pain, a bowed warm tibia, an enlarging skull and deafness are Paget's disease of bone: overactive, disordered remodelling makes bone bigger but weaker. X-rays and an isotope bone scan show its extent, and bisphosphonates treat the pain.
~ New severe localised pain and swelling in a bone already affected by Paget's → osteosarcoma, needing an urgent X-ray and referral.
c: worse at night | hats no longer fit | slightly deaf | bowed and warm | ALP 584
m: Overactive osteoclasts and then chaotic osteoblasts lay down large, vascular, weak bone
g: Isolated very high ALP with normal calcium and a bowed warm bone → Paget's disease
f: a PSA of 86 with back pain and sclerotic lesions in the spine => Bone metastases
f: a low calcium and phosphate, a raised PTH and proximal muscle weakness => Osteomalacia
f: a calcium of 2.9 with a raised PTH and kidney stones => Primary hyperparathyroidism
x: Bone metastases => Possible in an older man, but his PSA is normal and the skull and bowing changes fit Paget's
x: Multiple myeloma => Usually leaves the ALP normal and raises the calcium
x: Osteomalacia => Lowers calcium and phosphate and raises the PTH
x: Primary hyperparathyroidism => Raises the calcium and PTH, both normal here

@k d:ssris 2D
s: An 81 year old woman has become confused and unsteady over 5 days. Three weeks ago she started 2 new medicines: one for low mood and paracetamol for knee pain. Her other medicines are amlodipine, atorvastatin and levothyroxine, all unchanged for years. // She appears euvolaemic, with moist mucous membranes, no oedema and a BP of 138/82 mmHg with no postural drop.
$ Sodium ; 119 mmol/L ; 135–146
$ Potassium ; 4.2 mmol/L ; 3.5–5.3
$ Serum osmolality ; 252 mOsm/kg ; 275–295
$ Urine osmolality ; 486 mOsm/kg ;
$ Urine sodium ; 54 mmol/L ;
$ TSH ; 2.4 mU/L ; 0.3–4.2
? Which drug is most likely to have caused her hyponatraemia?
> Amlodipine ; Atorvastatin ; *Fluoxetine ; Levothyroxine ; Paracetamol
= Euvolaemic hyponatraemia with a low serum osmolality, inappropriately concentrated urine and a high urine sodium is SIADH. SSRIs such as fluoxetine are a common cause, especially in older people in the first few weeks. Her thyroid function is normal. Stop the SSRI and restrict fluids.
~ A postural drop, dry mucous membranes and a recently started thiazide → hypovolaemic hyponatraemia from the diuretic.
c: confused and unsteady | Three weeks ago | euvolaemic | Urine osmolality 486 | Urine sodium 54
m: SSRIs increase ADH release, so the kidney holds on to free water and dilutes the plasma sodium
g: Euvolaemic hyponatraemia with concentrated urine after starting an SSRI → SIADH from the SSRI
x: Amlodipine => Causes ankle oedema and flushing, not SIADH, and the dose has not changed
x: Atorvastatin => Not a cause of hyponatraemia, and it has not changed
x: Levothyroxine => Treats hypothyroidism, which can lower sodium, and her TSH shows good replacement
x: Paracetamol => Not a cause of SIADH

@k x:echo 3R
s: A 66 year old man with long-standing hypertension has sudden tearing chest pain going through to his back. In the resuscitation room he deteriorates. // Pulse rate 118 bpm, BP 84/50 mmHg in the right arm and 62/40 mmHg in the left arm. There is a new early diastolic murmur. He is intubated and ventilated and is too unstable to leave the department. ECG shows sinus tachycardia without ST elevation.
? Which is the most appropriate imaging to confirm the diagnosis?
> Chest X-ray ; CT aortogram ; MR angiography ; *Transoesophageal echocardiography ; Transthoracic echocardiography
= Tearing pain to the back, a difference in blood pressure between the arms and new aortic regurgitation are a type A aortic dissection. CT aortography is the usual first test in a stable patient, but he is too unstable to travel to the scanner. Bedside transoesophageal echocardiography shows the intimal flap, the aortic valve and any tamponade, and can be done in the resuscitation room or theatre.
~ The same pain in a patient who is stable → CT aortogram of the whole aorta.
c: tearing chest pain going through to his back | 84/50 mmHg in the right arm and 62/40 mmHg in the left arm | early diastolic murmur | too unstable to leave the department
m: The probe sits in the oesophagus right behind the ascending aorta, so the flap is seen clearly without moving him
g: Suspected dissection: stable → CT aortogram; too unstable to move → bedside TOE
f: a haemodynamically stable patient with normal renal function => CT aortogram
x: Chest X-ray => May show a widened mediastinum but can be normal and cannot confirm dissection
x: CT aortogram => First choice when stable, but he cannot safely leave the resuscitation room
x: MR angiography => Accurate but slow and not possible in an unstable ventilated patient
x: Transthoracic echocardiography => Useful for tamponade and aortic regurgitation, but it misses much of the ascending aorta and arch

@u 12 2N
s: A 29 year old man is found unresponsive at home with an empty bottle of methadone beside him. // Respiratory rate 6/min, oxygen saturation 84% breathing air, pulse rate 64 bpm, BP 112/70 mmHg. His pupils are pinpoint. An arterial blood gas is taken breathing air.
$ pH ; 7.24 ; 7.35–7.45
$ PaCO2 ; 8.6 kPa ; 4.6–6.4
$ PaO2 ; 7.4 kPa ; 11–15
$ Bicarbonate ; 26 mmol/L ; 22–30
$ Lactate ; 1.2 mmol/L ; <2.0
? Which is the most likely acid-base disturbance?
> Compensated metabolic acidosis ; Metabolic alkalosis ; Mixed respiratory and metabolic acidosis ; *Respiratory acidosis ; Respiratory alkalosis
= The pH is low and the PaCO2 high, so the primary problem is a respiratory acidosis from opioid-induced hypoventilation. The bicarbonate is normal because the kidneys have not had time to compensate, so it is acute. A normal lactate and bicarbonate rule out a metabolic acidosis. He needs naloxone and support for his breathing.
~ The same gas with a bicarbonate of 34 in a man with severe COPD → chronic respiratory acidosis with metabolic compensation.
c: methadone | Respiratory rate 6/min | pinpoint | pH 7.24 | PaCO2 8.6
m: Opioids blunt the brainstem response to CO2, so breathing slows and CO2 builds up as carbonic acid
g: Low pH with a high CO2 and normal bicarbonate → acute respiratory acidosis
f: a pH of 7.12, PaCO2 of 8.6 and bicarbonate of 14 with a lactate of 9 after a long seizure => Mixed respiratory and metabolic acidosis
f: a pH of 7.52 and PaCO2 of 3.1 in a panic attack with tingling fingers => Respiratory alkalosis
f: a pH of 7.50 with a bicarbonate of 38 after days of vomiting => Metabolic alkalosis
x: Compensated metabolic acidosis => Would show a low bicarbonate and a low CO2
x: Metabolic alkalosis => Needs a high pH and a high bicarbonate
x: Mixed respiratory and metabolic acidosis => Would also need a low bicarbonate or a high lactate
x: Respiratory alkalosis => Needs a low CO2 and a high pH

@u 2 2R
s: A 58 year old man has had central chest tightness for 6 weeks when walking uphill, easing within 3 minutes of rest. He smokes and has hypertension. // Examination is normal. His resting ECG is normal. A full blood count, renal function and HbA1c are normal.
? Which is the most appropriate first-line investigation?
> *CT coronary angiography ; Exercise ECG ; Invasive coronary angiography ; Myocardial perfusion scan ; Serial troponin
= Chest tightness brought on by exertion and relieved by rest within 5 minutes is typical angina. NICE recommends CT coronary angiography as the first-line test for stable chest pain that could be angina, rather than an exercise ECG. Functional imaging follows if CT is inconclusive, and invasive angiography if revascularisation is being considered.
~ CT shows a stenosis of uncertain significance → functional imaging such as a myocardial perfusion scan.
c: 6 weeks | walking uphill | easing within 3 minutes of rest | resting ECG is normal
m: CT shows the coronary lumen and plaque directly and rules out disease with a high negative predictive value
g: Possible stable angina → CT coronary angiography first
f: CT shows a 50% to 70% stenosis of uncertain functional significance => Myocardial perfusion scan
f: angina persists despite 2 anti-anginal drugs and revascularisation is being considered => Invasive coronary angiography
f: the same pain at rest for 40 minutes this morning => Serial troponin
x: Exercise ECG => No longer recommended to diagnose stable angina, as it misses and over-calls disease
x: Invasive coronary angiography => Kept for when revascularisation is being considered
x: Myocardial perfusion scan => Second line when CT is inconclusive or shows disease of uncertain significance
x: Serial troponin => For suspected acute coronary syndrome, and his pain is stable and exertional

@u 24 2L
s: A 4 year old girl has had high fever and frequent small stools with blood and mucus for 2 days. Today she had a brief generalised seizure while febrile. Three other children at her nursery have had similar diarrhoea this week. The family has no pets and has not travelled. // Temperature 39.6°C. She has lower abdominal tenderness and strains often but passes little.
? Which is the most likely causative organism?
> Campylobacter jejuni ; Escherichia coli O157 ; Rotavirus ; Salmonella enteritidis ; *Shigella sonnei
= High fever, small bloody mucoid stools with straining, a febrile seizure and an outbreak in a nursery point to Shigella, which needs very few organisms to spread from person to person. Shigella sonnei is the usual species in the UK. Stool culture confirms it, and it is notifiable.
~ Bloody diarrhoea with little fever, then pallor, bruising and reduced urine a week later → E. coli O157 with haemolytic uraemic syndrome.
c: high fever | blood and mucus | seizure | nursery | strains often but passes little
m: Shigella invades the colonic lining and spreads from cell to cell, causing ulcerating dysentery, and it often triggers seizures in young children
g: Bloody dysentery with high fever, a seizure and a nursery outbreak → Shigella
f: bloody diarrhoea with little fever, then pallor, bruising and reduced urine a week later => Escherichia coli O157
f: an adult with crampy pain and bloody diarrhoea after undercooked chicken at a barbecue => Campylobacter jejuni
f: a 1 year old with vomiting and watery diarrhoea without blood in winter => Rotavirus
x: Campylobacter jejuni => The commonest UK cause of bloody diarrhoea, but it is foodborne, usually from poultry, and rarely spreads through a nursery
x: Escherichia coli O157 => Often causes bloody diarrhoea with little or no fever
x: Rotavirus => Causes watery diarrhoea and vomiting without blood
x: Salmonella enteritidis => Usually foodborne from eggs or poultry, with watery rather than dysenteric stools

@u 108 2L
s: A 17 year old girl is brought to her GP by her mother, who has noticed she is eating very little and running every day. She has not had a period for 5 months. She says she is still too fat and is frightened of gaining weight. She denies bingeing or vomiting. // Height 1.65 m, weight 43 kg, BMI 15.8 kg/m². Pulse rate 48 bpm. She has fine downy hair on her arms.
$ Potassium ; 4.0 mmol/L ; 3.5–5.3
$ Glucose ; 3.9 mmol/L ; 4.0–7.8
? Which is the most likely diagnosis?
> *Anorexia nervosa ; Atypical anorexia nervosa ; Avoidant restrictive food intake disorder ; Bulimia nervosa ; Hyperthyroidism
= Restriction and exercise leading to a very low BMI, an intense fear of weight gain with a distorted view of her body, amenorrhoea, bradycardia and lanugo hair are anorexia nervosa. Without bingeing or vomiting her potassium is normal. A BMI this low with a pulse under 50 needs urgent medical assessment of risk.
~ A normal BMI with regular binges followed by vomiting and a low potassium → bulimia nervosa.
c: eating very little | running every day | too fat | frightened of gaining weight | BMI 15.8
m: Starvation shuts down the hypothalamic-pituitary-ovarian axis and slows the heart, while the fear of weight gain keeps the restriction going
g: Low BMI with fear of weight gain and restriction → anorexia nervosa
f: a BMI of 22 with weekly binges followed by vomiting and a potassium of 3.0 => Bulimia nervosa
f: restricts food because of a fear of choking, with no concern about weight or shape => Avoidant restrictive food intake disorder
f: the same fears and restriction after losing 15 kg, but with a BMI of 21 => Atypical anorexia nervosa
x: Atypical anorexia nervosa => Used when the features are present but weight is still in the normal range
x: Avoidant restrictive food intake disorder => Restriction is driven by sensory dislike or fear of choking, not by weight or shape
x: Bulimia nervosa => Needs bingeing with compensation, usually at a normal weight
x: Hyperthyroidism => Causes weight loss with a fast pulse and no fear of weight gain

@u 19 2N
s: A 68 year old man has had a cough with green sputum, fever and right-sided pleuritic pain for 3 days. He is orientated in time, place and person. He has no allergies. // Temperature 38.4°C, pulse rate 96 bpm, respiratory rate 22/min, BP 128/76 mmHg, oxygen saturation 95% breathing air. There is bronchial breathing at the right base. Chest X-ray shows right lower lobe consolidation.
$ Urea ; 6.2 mmol/L ; 2.5–7.8
$ CRP ; 164 mg/L ; <5
$ White cell count ; 15.8 × 10⁹/L ; 4.0–11.0
? Which is the most appropriate management?
> Admit for IV co-amoxiclav and clarithromycin ; Admit for oral amoxicillin and clarithromycin ; Oral clarithromycin at home for 5 days ; *Oral amoxicillin at home for 5 days ; Oral doxycycline at home for 5 days
= His CURB-65 score is 1, for age 65 or over: he is not confused, his urea is 7 or less, his respiratory rate is under 30 and his blood pressure is normal. This is low-severity community-acquired pneumonia, which NICE advises treating at home with oral amoxicillin for 5 days, with advice to return if he worsens.
~ CURB-65 of 3, such as confusion, a urea of 9 and age over 65 → high severity: admit for IV co-amoxiclav plus clarithromycin.
c: orientated in time, place and person | no allergies | respiratory rate 22/min | BP 128/76 | Urea 6.2
m: CURB-65 predicts 30-day mortality, and low scores do well with an oral narrow-spectrum penicillin
g: CURB-65 of 0 or 1 → home with oral amoxicillin for 5 days
f: confusion, a urea of 9.4 and a respiratory rate of 32 => Admit for IV co-amoxiclav and clarithromycin
f: the same picture with a penicillin allergy that caused anaphylaxis => Oral clarithromycin at home for 5 days
f: a CURB-65 score of 2 => Admit for oral amoxicillin and clarithromycin
x: Admit for IV co-amoxiclav and clarithromycin => For high-severity pneumonia, CURB-65 of 3 to 5
x: Admit for oral amoxicillin and clarithromycin => For moderate severity, CURB-65 of 2, usually with hospital assessment
x: Oral clarithromycin at home for 5 days => An alternative for penicillin allergy, and he has none
x: Oral doxycycline at home for 5 days => Another penicillin allergy alternative, and he has no allergy

@u 78 2L
s: A 41 year old man has had pain in both flanks for months and passed red urine twice in the past year. His mother started dialysis at 55, and his uncle died suddenly from a brain haemorrhage. // BP 162/98 mmHg. Both flanks contain large, irregular, ballotable masses. He has had no weight loss or fever and has no varicocele.
$ Creatinine ; 148 µmol/L ; 60–120
$ Haemoglobin ; 158 g/L ; 130–175
$ Urine dipstick blood ; 2+ ; negative
? Which is the most likely diagnosis?
> Bilateral hydronephrosis ; *Polycystic kidney disease ; Renal cell carcinoma ; Tuberous sclerosis ; Wilms' tumour
= Bilateral irregular ballotable kidneys, hypertension, haematuria, a raised creatinine and a family history of kidney failure and brain haemorrhage are autosomal dominant polycystic kidney disease. Berry aneurysms cluster in some families. Ultrasound confirms many cysts in both kidneys.
~ One kidney mass with haematuria, weight loss, a new left varicocele and polycythaemia → renal cell carcinoma.
c: both flanks | mother started dialysis | brain haemorrhage | large, irregular, ballotable | no weight loss
m: PKD1 or PKD2 mutations let cysts grow from the tubules until they crowd out working nephrons and stretch the capsule
g: Bilateral big kidneys, hypertension and a family history of dialysis or SAH → ADPKD
f: a single loin mass with weight loss, a new left varicocele and a haemoglobin of 192 => Renal cell carcinoma
f: a 3 year old with a smooth abdominal mass on one side that does not cross the midline => Wilms' tumour
f: facial angiofibromas, seizures and ash leaf macules with kidney masses => Tuberous sclerosis
x: Bilateral hydronephrosis => Usually from bladder outflow obstruction, with smooth kidneys and no family history
x: Renal cell carcinoma => Usually a single mass, and he has no weight loss or varicocele
x: Tuberous sclerosis => Causes kidney angiomyolipomas with skin and neurological signs, which he lacks
x: Wilms' tumour => A tumour of young children

@k x:lp 2T
s: A 24 year old man has had a headache, fever and vomiting for 18 hours and is drowsy but rousable. A lumbar puncture is being considered. // Temperature 39.1°C, GCS 14. He has neck stiffness and Kernig's sign is positive. There is no rash. Fundoscopy shows swollen optic discs with blurred margins in both eyes.
? Which finding is the strongest reason to delay the lumbar puncture?
> Fever of 39.1°C ; GCS of 14 ; Kernig's sign ; Neck stiffness ; *Papilloedema
= Papilloedema is a sign of raised intracranial pressure, and a lumbar puncture then risks herniation of the brain through the foramen magnum. Give IV antibiotics immediately and arrange a CT head before any lumbar puncture. Fever, neck stiffness and Kernig's sign are reasons to suspect meningitis, not reasons to delay.
~ A rapidly spreading purpuric rash with shock → treat as meningococcal sepsis and do not delay antibiotics for a lumbar puncture.
c: drowsy but rousable | swollen optic discs with blurred margins | neck stiffness | Kernig's sign is positive
m: Removing CSF from below drops the pressure beneath a brain already under high pressure, so it can cone downwards
g: Papilloedema or other signs of raised ICP → antibiotics now and CT first, lumbar puncture later
x: Fever of 39.1°C => Expected in meningitis and does not make a lumbar puncture dangerous
x: GCS of 14 => Only mildly reduced; a GCS below 9 or a fall of 3 points or more would be a contraindication
x: Kernig's sign => A sign of meningeal irritation that supports doing the lumbar puncture
x: Neck stiffness => Points to meningitis and is a reason for the lumbar puncture, not against it
"""
