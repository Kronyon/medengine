"""🧭 Master posters: one picture for a whole topic, shared by medengine-STUDY and medengine-OSCE.
The first five rebuild the AI-made infographics Nana liked, with every error fixed and the fix listed.
Own words, UK guidance. Columns: [head, text, lock-whole-line?]. Colour keys: b blue, a amber, g green, r red, p purple, t teal, s slate."""
import json

MASTER = []


def M(**m):
    m.setdefault('u', [])
    s = json.dumps(m, ensure_ascii=False)
    assert '—' not in s and '(' not in s, 'em dash or bracket in master ' + m['id']
    for c in m.get('cols', []):
        for it in c['items']:
            assert 2 <= len(it) <= 3, (m['id'], it)
    if 'mx' in m:
        w = len(m['mx']['head'])
        for r in m['mx']['rows']:
            assert len(r) == w, (m['id'], r[0])
    MASTER.append(m)


M(id='spiro', ic='🫁', t='Spirometry: obstructive or restrictive', sub='one big breath out, read 2 ways', fig='spiro', sys='resp', u=[15, 16, 17, 23, 12],
  cols=[
      {'h': 'Obstructive', 'i': '🚪', 'c': 'b', 'sub': 'The door is narrow: air leaves slowly', 'items': [
          ['FEV1', 'Low'], ['FVC', 'Normal or a little low'], ['FEV1 to FVC', 'Under 0.7: the defining number', 1],
          ['Curve', 'A slow climb that keeps creeping up for seconds'], ['Loop', 'Scooped out after the peak'],
          ['Causes', 'Asthma, COPD, bronchiectasis, CF']]},
      {'h': 'Restrictive', 'i': '📦', 'c': 'a', 'sub': 'The room is small: less air, but it leaves fast', 'items': [
          ['FEV1', 'Low'], ['FVC', 'Low, as low or lower'], ['FEV1 to FVC', 'Normal or high: 0.7 or more', 1],
          ['Curve', 'Shoots up, then flattens early at a low volume'], ['Loop', 'Same shape, just narrow'],
          ['Causes', 'Lung fibrosis, obesity, scoliosis, weak breathing muscles, pleural thickening']]},
  ],
  mx={'head': ['The question', 'The test', 'The answer'], 'rows': [
      ['Is it asthma?', 'Reversibility and FeNO', 'FEV1 rises 12% and 200 ml after salbutamol; FeNO 50 ppb or more in adults'],
      ['Is it COPD?', 'Ratio after the bronchodilator', 'Still under 0.7 after salbutamol, in a smoker or ex-smoker 35+'],
      ['Is the gas exchange surface damaged?', 'Transfer factor, TLCO', 'Low in fibrosis and emphysema; normal in asthma and chest wall causes'],
      ['Are the lungs truly small?', 'Lung volumes, TLC', 'TLC low confirms restriction; high in emphysema'],
      ['How bad is the COPD?', 'FEV1 % predicted', '80% or more mild; 50 to 79 moderate; 30 to 49 severe; under 30 very severe']]},
  hook='Obstructive: a narrow door, so air leaves slowly. Restrictive: a small room, so less air leaves, but it leaves fast.',
  fix=['Wrong: the restrictive curve was drawn as a slow climb. It should shoot up and flatten early at a low volume, because the ratio is normal or high.',
       'Exaggerated: the obstructive curve still climbs in real life, just slowly, and keeps creeping up for many seconds.',
       'Missing: the step that decides asthma: post-bronchodilator reversibility of 12% and 200 ml, plus FeNO.',
       'Missing: transfer factor, which splits lung fibrosis from chest wall and muscle causes of restriction.',
       'Missing: COPD is diagnosed on the ratio after the bronchodilator, not before.'],
  src='NICE NG245 asthma 2024, NICE NG115 COPD, ARTP spirometry standards')

M(id='ms', ic='🫀', t='Mitral stenosis', sub='a slit the left atrium has to squeeze through', fig='ms', sys='cardio', u=[7, 3, 8],
  cols=[
      {'h': 'What goes wrong', 'i': '🧬', 'c': 'p', 'items': [
          ['Chain', 'Rheumatic fever years before → the leaflets fuse and stiffen → the left atrium strains and swells → AF and clots; pressure backs into the lungs'],
          ['Commonest cause', 'Rheumatic heart disease, especially if born where it is common'],
          ['In the elderly', 'Calcium building up in the mitral ring: mitral annular calcification'],
          ['Back pressure', 'Breathless, coughing blood, pulmonary hypertension']]},
      {'h': 'Spot it', 'i': '👀', 'c': 't', 'items': [
          ['Face', 'Malar flush: rosy purple cheeks'], ['Pulse', 'Often irregularly irregular: AF'], ['Apex', 'Tapping, not displaced'],
          ['Listen', 'Loud S1, an opening snap, then a low rumble in diastole at the apex', 1], ['How', 'Bell, patient rolled onto the left side, breath held out']]},
      {'h': 'Prove and grade', 'i': '🧪', 'c': 'b', 'items': [
          ['Echo', 'Valve area and the pressure gradient'], ['Severe', 'Valve area 1.5 cm² or less', 1], ['Very severe', 'Under 1.0 cm²'],
          ['ECG', 'AF, or a broad notched P wave from the big atrium'], ['Chest X-ray', 'Big left atrium: straight left heart border, splayed carina']]},
      {'h': 'Treat', 'i': '💊', 'c': 'g', 'items': [
          ['AF with moderate or severe MS', 'Warfarin, not a DOAC', 1], ['AF with mild MS', 'A DOAC is fine'],
          ['Symptoms', 'Rate control, diuretics'], ['Severe with symptoms', 'Balloon valvotomy if the valve suits it; otherwise valve replacement']]},
  ],
  hook='The left atrium pushes through a slit, swells, fibrillates and clots. Moderate or severe MS with AF means warfarin.',
  fix=['Right: warfarin for AF with moderate or severe MS, a DOAC only for mild MS. Keep it.',
       'Missing: the grading. Severe is a valve area of 1.5 cm² or less; very severe is under 1.0.',
       'Missing: the cause in older people, mitral annular calcification.'],
  src='ESC 2021 and ACC/AHA 2020 valve guidelines, INVICTUS trial')

M(id='uveitis', ic='👁️', t='Anterior uveitis', sub='a sticky, spasming iris', fig='eye', sys='eye', u=[158, 154, 159],
  cols=[
      {'h': 'Why it happens', 'i': '🧬', 'c': 'p', 'items': [
          ['Chain', 'Immune attack on the iris and ciliary body → white cells and protein leak into the front chamber → the iris spasms and sticks to the lens'],
          ['HLA-B27 group', 'Ankylosing spondylitis, reactive arthritis, psoriatic arthritis, IBD', 1],
          ['Not HLA-B27', 'Sarcoid, Behçet\'s, herpes, TB, syphilis; JIA in children']]},
      {'h': 'Spot it', 'i': '👀', 'c': 't', 'items': [
          ['Pain', 'An ache, worse when reading: the iris spasms as it focuses'], ['Light', 'Hurts, even shone in the other eye'],
          ['Red', 'A ring of red hugging the cornea'], ['Pupil', 'Small from spasm; irregular where it sticks to the lens'],
          ['Slit lamp', 'Cells and flare; a white fluid level if severe', 1]]},
      {'h': 'Treat', 'i': '💊', 'c': 'g', 'items': [
          ['Same day', 'Eye casualty and a slit lamp', 1], ['Steroid drops', 'Started by the eye team, once herpes of the cornea is excluded'],
          ['Cyclopentolate drops', 'Eases spasm pain and stops the iris sticking'], ['Then', 'Hunt the systemic cause: back, joints, gut, skin']]},
  ],
  foot=[['The pupil test', 'Uveitis small and irregular; acute glaucoma mid-dilated and fixed; conjunctivitis normal'],
        ['The red pattern', 'Uveitis hugs the cornea; conjunctivitis is worst at the edges, away from the cornea']],
  hook='Iritis: small sticky pupil, a ring of red, light hurts. Steroid drops only after the slit lamp has excluded herpes.',
  fix=['Wrong: Behçet\'s and sarcoid sat in the HLA-B27 box. They are separate causes; Behçet\'s links to HLA-B51.',
       'Missing: psoriatic arthritis belongs in the HLA-B27 group.',
       'Unclear: the pupil is small from spasm and irregular because the iris sticks to the lens.',
       'Unsafe as written: steroid drops start after an ophthalmologist has excluded herpes keratitis on the slit lamp.',
       'Missing: dilating drops also stop the iris sticking, not just the pain.'],
  src='NICE CKS red eye, Royal College of Ophthalmologists, EyeRounds HLA-B27 uveitis')

M(id='throat', ic='👅', t='Sore throat: FeverPAIN and Centor', sub='score it, then the plan picks itself', fig='throat', sys='ent', u=[151, 145, 143],
  cols=[
      {'h': 'FeverPAIN', 'i': '🔢', 'c': 'a', 'sub': '1 point each, 0 to 5', 'items': [
          ['F', 'Fever in the last 24 h', 1], ['P', 'Purulence: pus on the tonsils'], ['A', 'Attended within 3 days of onset'],
          ['I', 'Inflamed tonsils, severely'], ['N', 'No cough or cold']]},
      {'h': 'Centor', 'i': '🔢', 'c': 'b', 'sub': '1 point each, 0 to 4', 'items': [
          ['1', 'Tonsil exudate'], ['2', 'Tender front neck nodes'], ['3', 'History of fever over 38°C', 1], ['4', 'No cough']]},
      {'h': 'Act', 'i': '💊', 'c': 'g', 'items': [
          ['FeverPAIN 0 to 1, Centor 0 to 2', 'No antibiotic: pain relief, fluids, come back if worse'],
          ['FeverPAIN 2 to 3', 'No antibiotic, or a back-up prescription'],
          ['FeverPAIN 4 to 5, Centor 3 to 4', 'Immediate or back-up antibiotic'],
          ['First choice', 'Phenoxymethylpenicillin for 5 to 10 days', 1],
          ['Penicillin allergy', 'Clarithromycin 5 days; erythromycin 5 days if pregnant'],
          ['Avoid', 'Amoxicillin: a rash in glandular fever']]},
      {'h': 'Red flags', 'i': '🚩', 'c': 'r', 'items': [
          ['Quinsy', 'One side bulges, uvula pushed away, can\'t open the mouth: ENT same day'],
          ['Airway', 'Stridor, drooling, can\'t swallow saliva: emergency'],
          ['Glandular fever', 'Back neck nodes, big spleen, tired for weeks'],
          ['Low white cells', 'Sore throat on carbimazole or chemotherapy: FBC today']]},
  ],
  hook='Score the throat, then read the plan: 0 to 1 none, 2 to 3 none or back-up, 4 to 5 immediate or back-up.',
  fix=['Wrong: the fever criteria were swapped. FeverPAIN counts fever in the last 24 h; Centor counts a history of fever over 38°C.',
       'Missing: the NICE action for each score band, especially FeverPAIN 2 to 3: no antibiotic or a back-up prescription.',
       'Missing: the drug and the course: phenoxymethylpenicillin 5 to 10 days; clarithromycin or erythromycin if allergic.',
       'Missing: never amoxicillin, because of the glandular fever rash.'],
  src='NICE NG84 sore throat, acute: antimicrobial prescribing')

M(id='ct', ic='🩻', t='CT with or without contrast', sub='plain for blood, bone and stone; dye for vessels, masses and pus', fig='ct', sys='imaging', u=[91, 92, 79, 13, 1, 45, 95, 33],
  cols=[
      {'h': 'Without contrast', 'i': '⚪', 'c': 'b', 'sub': 'Already bright or dark on its own: dye would hide it', 'items': [
          ['Head', 'Stroke and head injury: is there blood?', 1], ['Kidneys', 'CT KUB for stones'],
          ['Lungs', 'High-resolution CT for fibrosis'], ['Bone', 'Fractures, the spine']]},
      {'h': 'With contrast', 'i': '🔆', 'c': 'a', 'sub': 'Iodine dye in the blood: vessels and well-supplied tissue light up', 'items': [
          ['Vessels', 'CT angiogram: PE, dissection, aneurysm, the stroke artery', 1], ['Masses', 'Cancer staging; an abscess shows a bright rim'],
          ['Abdomen', 'Most acute abdomens: collections, perforation, bowel'], ['Timing', 'Arterial phase for bleeding and vessels; portal venous phase for organs']]},
      {'h': 'Before the dye', 'i': '🚩', 'c': 'r', 'items': [
          ['Ask', 'Any previous reaction to iodinated contrast: that is the allergy question', 1],
          ['Myth', 'Shellfish or iodine allergy does not predict a contrast reaction'],
          ['Kidneys', 'Check eGFR if at risk; IV fluids for those at risk of contrast-associated AKI'],
          ['Metformin', 'eGFR 60 or more: carry on. Under 60: the referring team decides on a 48 h pause'],
          ['Previous reaction', 'No routine steroid cover in the UK: the radiologist picks another agent or test']]},
  ],
  hook='Plain for blood, bone and stone. Dye for vessels, masses and pus.',
  fix=['Wrong: an iodine or shellfish allergy is a myth as a contrast risk. Ask about a previous contrast reaction.',
       'Wrong: routine steroid premedication is not recommended in the UK.',
       'Wrong: metformin is not stopped for everyone; only when eGFR is under 60 after discussion, or in AKI.',
       'Updated term: contrast-associated AKI. IV fluids only for those at risk.',
       'Over-simplified: "unstable means no contrast" is not a rule; CT angiography is often exactly what a bleeding patient needs.',
       'Over-claimed: PID is not usually a CT diagnosis; swabs and ultrasound lead.'],
  src='Royal College of Radiologists contrast standards, ESUR contrast media guideline')

M(id='redeye', ic='🔴', t='The red eye', sub='4 questions: vision, pain, light, pupil', sys='eye', u=[154, 155, 156, 157, 158, 159, 160, 167],
  cols=[
      {'h': 'Usually safe', 'i': '🟢', 'c': 'g', 'items': [
          ['Vision', 'Normal'], ['Pain', 'Gritty or itchy, not painful'], ['Pupil', 'Normal'],
          ['Examples', 'Conjunctivitis, blepharitis, subconjunctival bleed, episcleritis']]},
      {'h': 'Same-day eye casualty', 'i': '🔴', 'c': 'r', 'items': [
          ['Any one of', 'Reduced vision, real pain, light hurts, an odd pupil', 1], ['Contact lens', 'Plus a painful red eye: keratitis'],
          ['Chemicals', 'Irrigate for 20 min first, then refer'], ['Examples', 'Uveitis, acute glaucoma, keratitis, scleritis, injury']]},
  ],
  mx={'head': ['', 'Conjunctivitis', 'Anterior uveitis', 'Acute angle closure', 'Keratitis', 'Scleritis', 'Subconjunctival bleed'], 'rows': [
      ['Pain', 'Gritty', 'Ache, worse reading', 'Severe, headache, vomiting', 'Severe, something in the eye', 'Deep, boring, wakes at night', 'None'],
      ['Vision', 'Normal', 'Blurred', 'Very blurred, halos', 'Blurred', 'Normal or reduced', 'Normal'],
      ['Light', 'Fine', 'Hurts', 'Hurts', 'Hurts', 'Some', 'Fine'],
      ['Red pattern', 'Everywhere, most at the edges', 'Ring round the cornea', 'Whole eye, hazy cornea', 'Round the cornea, a white spot', 'Deep purple patch', 'Flat bright red patch'],
      ['Pupil', 'Normal', 'Small, irregular', 'Mid-dilated, fixed', 'Normal or small', 'Normal', 'Normal'],
      ['Clue', 'Discharge, a cold, hay fever', 'HLA-B27 back or joint disease', 'Older, long-sighted, dim light', 'Contact lens wearer', 'RA, vasculitis', 'Straining, warfarin, high BP'],
      ['Act', 'Self-care; chloramphenicol if bacterial', 'Same day', 'Emergency: pilocarpine, acetazolamide, then laser', 'Same day; never steroid drops unsupervised', 'Same day', 'Reassure; check BP and INR']]},
  hook='Ask 4 questions: vision, pain, light, pupil. One abnormal answer = same day.',
  src='NICE CKS red eye, Royal College of Ophthalmologists')

M(id='dizzy', ic='🌀', t='Dizziness and hearing', sub='time the spin, then check the hearing', sys='ent', u=[140, 142, 146],
  mx={'head': ['', 'BPPV', 'Vestibular neuritis', 'Labyrinthitis', 'Ménière\'s', 'Acoustic neuroma', 'Posterior stroke'], 'rows': [
      ['How long', 'Seconds', 'Days, constant', 'Days, constant', 'Hours, in attacks', 'Months of unsteadiness', 'Sudden, persists'],
      ['Trigger', 'Rolling over, looking up', 'After a cold', 'After a cold', 'None, comes in clusters', 'None', 'None; vascular risk factors'],
      ['Hearing', 'Normal', 'Normal', 'Lost on one side', 'Fluctuating low-tone loss, fullness, tinnitus', 'One-sided loss and tinnitus', 'Usually normal'],
      ['Key test', 'Dix-Hallpike', 'HINTS: abnormal head impulse', 'Audiogram', 'Audiogram: low tones', 'MRI internal auditory meatus', 'HINTS: normal head impulse; MRI'],
      ['Treat', 'Epley manoeuvre', 'Short prochlorperazine, balance exercises', 'Short prochlorperazine, balance exercises', 'Betahistine, low salt; tell the DVLA', 'Watch, radiosurgery or surgery', 'Stroke pathway']]},
  foot=[['HINTS', 'Head Impulse, Nystagmus, Test of Skew: only for constant dizziness. A normal head impulse in a constantly dizzy patient is the worrying sign.'],
        ['Hearing tells the level', 'No hearing loss: balance nerve or crystals. Hearing loss: the inner ear or the nerve itself.']],
  hook='Seconds = BPPV, hours = Ménière\'s, days = neuritis; days plus deafness = labyrinthitis. New neuro signs = stroke.',
  src='NICE CKS vertigo, ENT UK')

M(id='stable', ic='⚡', t='Stable or unstable: the first move', sub='fix the physiology before you chase the diagnosis', fig='fork', sys='acute', u=[3, 11, 68, 13, 46, 96, 126, 32, 38, 51],
  mx={'head': ['', 'Unstable means', 'First move', 'Then', 'The trap'], 'rows': [
      ['Fast heart rhythm', 'Shock, fainting, chest pain, heart failure', 'Synchronised DC shock', 'Stable and narrow: vagal manoeuvres, then adenosine', 'Adenosine before vagal manoeuvres'],
      ['Tension pneumothorax', 'Trachea shifted, low BP', 'Needle decompression', 'Chest drain; X-ray afterwards', 'Waiting for the X-ray'],
      ['DKA', 'Systolic under 90', '500 ml 0.9% saline over 15 min', 'Not shocked: 1 litre over 1 h, then fixed-rate insulin', 'Insulin before fluids'],
      ['Upper GI bleed', 'Shock index over 1', 'Resuscitate, blood, Blatchford score', 'OGD straight after resuscitation if unstable; within 24 h if not', 'Scoping before resuscitating'],
      ['Pulmonary embolism', 'Systolic under 90: massive', 'Thrombolysis', 'Stable: CTPA, then a DOAC', 'CTPA in a crashing patient'],
      ['Anaphylaxis', 'Airway, breathing or circulation problem', 'IM adrenaline 0.5 mg, repeat at 5 min', 'Oxygen, IV fluids; antihistamine and steroid are not first-line', 'Antihistamine first'],
      ['Sepsis', 'NEWS2 7 or more, or a red flag', 'Cultures, then antibiotics within 1 hour', 'Fluids, lactate, control the source', 'Waiting for results'],
      ['Status epilepticus', 'Fitting over 5 min', 'Buccal midazolam or IV lorazepam', 'Repeat once at 5 to 10 min, then levetiracetam, phenytoin or valproate', 'Waiting it out'],
      ['High potassium', 'ECG changes', 'IV calcium gluconate 10%, 30 ml', 'Insulin with glucose, then remove the potassium', 'Insulin before calcium']]},
  hook='Is the patient stable? Ask that before you name the disease. Unstable: the first move. Stable: the cure.',
  src='Resuscitation Council UK, JBDS DKA 2023, NICE NG51 sepsis, UK Kidney Association hyperkalaemia')

M(id='antidotes', ic='🧯', t='Antidotes', sub='each poison has a home and a key', sys='acute', u=[111, 110, 101, 112],
  mx={'head': ['Poison', 'Clue', 'Antidote', 'Note'], 'rows': [
      ['Paracetamol', 'Often no symptoms early; level at 4 h', 'Acetylcysteine', 'Staggered or unknown timing: treat regardless of the level'],
      ['Opioids', 'Pinpoint pupils, slow breathing', 'Naloxone', 'Wears off first: repeat doses or an infusion'],
      ['Benzodiazepines', 'Drowsy, breathing usually fine', 'Flumazenil, rarely', 'Can trigger fits in dependence or mixed overdose'],
      ['Tricyclics', 'Dilated pupils, broad QRS, fits', 'Sodium bicarbonate', 'For a QRS over 100 ms or arrhythmia'],
      ['Warfarin', 'Bleeding with a high INR', 'Vitamin K', 'Major bleed: add prothrombin complex'],
      ['Heparin', 'Bleeding on heparin', 'Protamine', 'Only partly reverses LMWH'],
      ['Dabigatran', 'Bleeding', 'Idarucizumab', 'Binds the drug directly'],
      ['Apixaban, rivaroxaban', 'Bleeding', 'Andexanet alfa', 'Or prothrombin complex'],
      ['Iron', 'Vomiting, gut bleeding, then shock', 'Desferrioxamine', 'Grabs the iron'],
      ['Methanol, ethylene glycol', 'Drunk without the smell, high anion gap, blurred vision', 'Fomepizole', 'Stops the liver making the toxic acids; dialysis if severe'],
      ['Digoxin', 'Nausea, yellow vision, arrhythmia', 'Digoxin-specific antibody fragments', 'Check potassium'],
      ['Beta-blockers', 'Slow pulse, low BP', 'Glucagon; high-dose insulin', 'Atropine first for the slow pulse'],
      ['Organophosphates', 'Wet: sweat, saliva, diarrhoea, small pupils', 'Atropine', 'Plus pralidoxime'],
      ['Cyanide', 'Smoke inhalation, very high lactate', 'Hydroxocobalamin', ''],
      ['Carbon monoxide', 'Headache, sats look normal', '100% oxygen', 'Hyperbaric for some'],
      ['Lithium', 'Coarse tremor, vomiting, confusion', 'No antidote: fluids', 'Haemodialysis if severe']]},
  hook='DesFERRIoxamine grabs FERRous iron. FOMEpizole stops the liver turning antifreeze and meths into poison.',
  src='TOXBASE, BNF')

M(id='opioids', ic='💊', t='Pain ladder and opioid maths', sub='climb as pain rises; convert before you switch', fig='ladder', sys='drugs', u=[50],
  cols=[
      {'h': 'Conversions to oral morphine', 'i': '🔢', 'c': 'b', 'items': [
          ['Codeine', 'Divide by 10', 1], ['Tramadol', 'Divide by 10', 1], ['Oral morphine → oral oxycodone', 'Divide by 1.5 to 2', 1],
          ['Oral morphine → SC morphine', 'Divide by 2', 1], ['Oral morphine → SC diamorphine', 'Divide by 3', 1]]},
      {'h': 'Doses', 'i': '💊', 'c': 'g', 'items': [
          ['Starting, opioid-naive', 'Oral morphine 20 to 30 mg a day, plus as-needed doses'],
          ['Breakthrough', 'A sixth to a tenth of the 24 h dose', 1], ['Review', 'Add up the as-needed doses each day and fold them in']]},
      {'h': 'Safety', 'i': '🚩', 'c': 'r', 'items': [
          ['Kidneys', 'eGFR under 30: avoid morphine; seek advice, oxycodone or alfentanil at lower doses'],
          ['Toxicity', 'Pinpoint pupils, drowsy, slow breathing: naloxone'], ['Every opioid', 'A laxative from day 1'],
          ['Patches', 'Not for acute or unstable pain']]},
  ],
  hook='Codeine and tramadol divide by 10. Oral to SC morphine divide by 2, to SC diamorphine by 3. Breakthrough is a sixth to a tenth.',
  src='NICE CG140 palliative opioids, BNF, Faculty of Pain Medicine Opioids Aware')

M(id='nerves', ic='🦴', t='Nerve injuries: where they break', sub='the injury picks the nerve; the nerve picks the loss', fig='nerves', sys='msk', u=[99, 97],
  mx={'head': ['Nerve', 'Injured by', 'Can\'t do', 'Numb patch'], 'rows': [
      ['Axillary', 'Shoulder dislocation, humeral neck fracture', 'Lift the arm out sideways', 'The regimental badge patch'],
      ['Radial', 'Humerus shaft fracture', 'Lift the wrist: wrist drop', 'Back of the thumb web'],
      ['Median', 'Carpal tunnel; supracondylar fracture', 'Lift the thumb away from the palm', 'Thumb, index, middle fingers'],
      ['Ulnar', 'Elbow injury, leaning on the elbow', 'Spread the fingers; claw of ring and little', 'Little finger and half the ring'],
      ['Long thoracic', 'Axillary surgery, heavy bags', 'Hold the shoulder blade flat: winging', 'None'],
      ['Brachial plexus', 'Shoulder pulled down at birth; arm yanked up', 'Erb\'s C5 to 6: waiter\'s tip. Klumpke C8 to T1: claw', 'Outer arm; inner forearm'],
      ['Sciatic', 'Posterior hip dislocation, hip surgery', 'Bend the knee; foot drop', 'Below the knee except the inner leg'],
      ['Common peroneal', 'Fibula neck fracture, tight cast, crossed legs', 'Lift the foot and turn it out: foot drop', 'Top of the foot and outer shin'],
      ['Tibial', 'Injury behind the knee', 'Point the foot, stand on tiptoe', 'The sole'],
      ['Femoral', 'Pelvic injury, groin lines', 'Straighten the knee; knee jerk lost', 'Front of the thigh, inner leg'],
      ['Superior gluteal', 'Hip surgery, buttock injection', 'Keep the pelvis level: Trendelenburg gait', 'None']]},
  hook='Shoulder out → axillary → numb badge. Humerus shaft → radial → wrist drop. Elbow → ulnar → claw. Fibula neck → peroneal → foot drop.',
  src='Oxford Handbook of Clinical Medicine, Orthobullets')

M(id='bowel', ic='🧩', t='Bowel operations, stomas and hernias', sub='the tumour\'s address picks the operation', fig='colon', sys='surg', u=[33, 37, 48, 58, 25],
  cols=[
      {'h': 'Operations by site', 'i': '🔪', 'c': 'b', 'items': [
          ['Caecum, ascending, hepatic flexure', 'Right hemicolectomy', 1], ['Transverse', 'Extended right hemicolectomy', 1],
          ['Splenic flexure, descending', 'Left hemicolectomy', 1], ['Sigmoid', 'Sigmoid colectomy', 1],
          ['Upper and mid rectum', 'Anterior resection', 1], ['Low rectum into the anus', 'Abdominoperineal resection: permanent colostomy', 1],
          ['Emergency on the left', 'Hartmann\'s: resect, end colostomy, close the rectal stump, rejoin later', 1]]},
      {'h': 'Stomas', 'i': '⭕', 'c': 'a', 'items': [
          ['Ileostomy', 'Right side, spouted, liquid output: small bowel juice burns skin'],
          ['Colostomy', 'Left side, flush with the skin, formed stool'],
          ['Loop ileostomy', 'Temporary, protects a low join while it heals'], ['Urostomy', 'Right side, spouted, urine: ileal conduit']]},
      {'h': 'Hernias', 'i': '🫃', 'c': 'p', 'items': [
          ['Inguinal', 'Above and in from the pubic tubercle; men'], ['Femoral', 'Below and out; older women; strangulates: repair soon', 1],
          ['Indirect inguinal', 'Through the deep ring: controlled by pressing over it'], ['Direct inguinal', 'Through the back wall: still bulges'],
          ['Incisional', 'Through an old scar'], ['Umbilical', 'At the navel; in babies most close on their own']]},
  ],
  hook='Right side → right hemi. Left side → left hemi. Rectum → anterior resection. Into the anus → APR, permanent bag. Emergency → Hartmann\'s.',
  src='ACPGBI, NICE NG151 colorectal cancer')

M(id='antibodies', ic='🧷', t='Antibodies: give each one an address', sub='pin the antibody to the organ it attacks', fig='abmap', sys='immuno', u=[28, 72, 73, 66, 98, 125, 97],
  mx={'head': ['Antibody', 'Disease', 'Clue'], 'rows': [
      ['ANA', 'SLE and many others', 'Sensitive, not specific: a door opener'],
      ['Anti-dsDNA', 'SLE', 'Specific; rises with kidney flares'],
      ['Anti-Smith', 'SLE', 'Very specific'],
      ['Anti-histone', 'Drug-induced lupus', 'Hydralazine, procainamide, isoniazid'],
      ['Anti-Ro, anti-La', 'Sjögren\'s', 'Dry eyes and mouth; heart block in the baby'],
      ['Anti-centromere', 'Limited systemic sclerosis', 'Hands and face; pulmonary hypertension later'],
      ['Anti-Scl-70', 'Diffuse systemic sclerosis', 'Spreads to the trunk; lung fibrosis'],
      ['Anti-Jo-1', 'Polymyositis, dermatomyositis', 'With lung fibrosis'],
      ['Anti-CCP', 'Rheumatoid arthritis', 'Specific; predicts erosions'],
      ['Rheumatoid factor', 'Rheumatoid arthritis', 'Sensitive, less specific'],
      ['c-ANCA', 'Granulomatosis with polyangiitis', 'Nose, lungs, kidneys'],
      ['p-ANCA', 'Microscopic polyangiitis, EGPA', 'EGPA: asthma plus eosinophils'],
      ['Anti-GBM', 'Goodpasture\'s', 'Coughing blood plus kidney failure'],
      ['Anticardiolipin, lupus anticoagulant', 'Antiphospholipid syndrome', 'Clots and miscarriages'],
      ['Anti-mitochondrial', 'Primary biliary cholangitis', 'Itchy middle-aged woman, high ALP'],
      ['Anti-smooth muscle', 'Autoimmune hepatitis', 'Young woman, high ALT'],
      ['Anti-tTG, anti-endomysial', 'Coeliac disease', 'Test while eating gluten'],
      ['Anti-TPO', 'Hashimoto\'s', 'Underactive thyroid'],
      ['TSH receptor antibodies', 'Graves\'', 'Overactive thyroid with eyes'],
      ['Anti-AChR', 'Myasthenia gravis', 'Fatigable, droopy eyes'],
      ['Anti-VGCC', 'Lambert-Eaton', 'Improves with use; small cell lung cancer'],
      ['Anti-intrinsic factor', 'Pernicious anaemia', 'Low B12'],
      ['Anti-GAD', 'Type 1 diabetes', 'With islet cell antibodies'],
      ['Anti-NMDA receptor', 'Autoimmune encephalitis', 'Psychosis, fits; ovarian teratoma']]},
  hook='Cardiolipin clots the pipes; CCP crushes the knuckles. Each antibody lives at its organ.',
  src='Oxford Handbook of Clinical Medicine, British Society for Rheumatology')

M(id='murmurs', ic='🎧', t='Four murmurs on one axis', sub='S1, systole, S2, diastole: where each one sits', fig='murmur', sys='cardio', u=[7, 8, 6],
  mx={'head': ['', 'Aortic stenosis', 'Mitral regurgitation', 'Aortic regurgitation', 'Mitral stenosis'], 'rows': [
      ['Timing', 'Ejection systolic', 'Pansystolic', 'Early diastolic', 'Mid-diastolic'],
      ['Shape', 'Rises and falls: a diamond', 'Flat: a box', 'Falls away: a slope', 'Snap, then a low rumble'],
      ['Loudest', 'Right 2nd space by the sternum', 'Apex', 'Left sternal edge', 'Apex, with the bell'],
      ['Goes to', 'The carotids', 'The armpit', 'Down the left sternal edge', 'Nowhere'],
      ['Best heard', 'Breath held out', 'Breath held out', 'Sitting forward, breath held out', 'Rolled onto the left side'],
      ['Pulse and signs', 'Slow-rising, narrow pulse pressure', 'Apex displaced', 'Collapsing, wide pulse pressure', 'AF, malar flush, tapping apex'],
      ['Commonest cause', 'Age-related calcification; bicuspid valve', 'Prolapse, after MI', 'Aortic root dilatation; bicuspid; endocarditis', 'Rheumatic fever']]},
  hook='ARMS rest in diastole: AR and MS are the diastolic pair. AS and MR fill systole.',
  src='Oxford Handbook of Clinical Medicine, ESC 2021 valve guideline')

if __name__ == '__main__':
    import sys
    json.dump(MASTER, open(sys.argv[1], 'w'), ensure_ascii=False)
    print(len(MASTER), 'master posters')
