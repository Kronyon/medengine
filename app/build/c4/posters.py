"""🗺️ OSCE station posters, own words, UK guidance.
ROUTES: every FFP examination as a route walked around a body or a head: props before you touch, numbered pins in the
order you examine, what to hunt for, and how to complete. Pins are 'Label: cue>place'.
STORY: every DOPS as 3 frames (set up → do it → finish and act) built from the station's own steps, plus the one move
that fails each frame and the numbers to know. History, psychiatry, drug, communication and imaging posters are built in
the app from each station's own data, so they never drift from the checklist."""

BODY = {'head', 'mind', 'eyes', 'face', 'ear', 'nose', 'mouth', 'neck', 'chest', 'lchest', 'heart', 'lungs', 'breast', 'back', 'epi', 'ruq', 'luq', 'abdo', 'loin',
        'rif', 'lif', 'supra', 'groin', 'genit', 'rarm', 'larm', 'hands', 'lhand', 'joints', 'legs', 'lleg', 'feet', 'skin', 'all'}
HEAD = {'top', 'forehead', 'eyes', 'reye', 'leye', 'brow', 'nose', 'mouth', 'tongue', 'cheek', 'face', 'rear', 'lear', 'ear', 'jaw', 'neck', 'thyroid', 'throat',
        'nodes', 'shoulder', 'back', 'hands', 'all'}

ROUTES = {
    'E-cvs': dict(map='body', props=['WIPER', 'Sit at 45°', 'Chest exposed', 'Chaperone offered', 'Bell and diaphragm'], pins=[
        'End of the bed: breathless, pale, malar flush; GTN spray, scars, pacemaker>all',
        'Hands: capillary refill, clubbing, splinters, Janeway lesions, xanthomata>hands',
        'Pulses: rate and rhythm, radio-radial; collapsing; BP in both arms>rarm',
        'Face and neck: pallor, arcus, central cyanosis; JVP; one carotid>neck',
        'Praecordium: scars, apex, heaves, thrills; 4 areas, timed on the carotid>heart',
        'Manoeuvres: rolled left for MS; sitting forward for AR; breath held out>lchest',
        'Back and legs: lung bases, sacral and ankle oedema>legs'],
        hunt=['Slow-rising pulse, ejection murmur to the carotids → aortic stenosis', 'Pansystolic murmur to the armpit → mitral regurgitation',
              'Collapsing pulse, early diastolic murmur sitting forward → aortic regurgitation', 'Malar flush, irregular pulse, rumble at the apex → mitral stenosis',
              'Sternotomy scar plus a metallic click → a mechanical valve: ask about warfarin'],
        done=['ECG', 'Echo', 'Observations and BP', 'Urine dip', 'Fundoscopy']),
    'E-resp': dict(map='body', props=['WIPER', 'Sit at 45°', 'Chest exposed', 'Spot inhalers, oxygen, sputum pot'], pins=[
        'End of the bed: breathless, accessory muscles, pursed lips; oxygen and its flow>all',
        'Hands: clubbing, tar staining, cyanosis; tremor; CO2 flap; pulse and breathing rate>hands',
        'Face: pallor, Horner\'s, central cyanosis; JVP>face',
        'Trachea and nodes: warn first; cricosternal distance; nodes from behind>neck',
        'Front: expansion, percussion, breath sounds, vocal resonance, side to side>chest',
        'Back: the same 4 again; sacral oedema>back'],
        hunt=['Stony dull, quiet, reduced resonance → effusion', 'Dull, bronchial breathing, crackles → consolidation', 'Hyper-resonant and quiet on one side → pneumothorax',
              'Fine crackles at both bases plus clubbing → fibrosis', 'Barrel chest, wheeze, pursed lips → COPD'],
        done=['Sats and observations', 'Peak flow or spirometry', 'Sputum sample', 'Chest X-ray', 'ABG if unwell']),
    'E-cn': dict(map='head', props=['WIPER', 'Sit level, 1 metre away', 'Snellen chart', 'Pen torch', 'Red hatpin', 'Cotton wool', '512 Hz fork', 'Cup of water'], pins=[
        'I: any change in smell or taste?>nose',
        'II: acuity, pupils with a swinging torch, fields, fundi>reye',
        'III, IV, VI: the H pattern; double vision, nystagmus>leye',
        'V: light touch in 3 zones; clench; say corneal reflex and jaw jerk>cheek',
        'VII: eyebrows up, eyes shut, cheeks puffed, teeth>face',
        'VIII: whisper test; offer Rinne and Weber>ear',
        'IX, X: say ahh, cough, a sip of water>mouth',
        'XI: shrug, turn the head against your hand>shoulder',
        'XII: tongue at rest, then out and side to side>tongue'],
        hunt=['Forehead spared → upper motor neurone: stroke', 'Forehead weak too → lower motor neurone: Bell\'s palsy', 'Eye down and out, droop, big pupil → third nerve palsy',
              'Can\'t look out to one side → sixth nerve palsy', 'Outer halves of both fields gone → bitemporal: pituitary'],
        done=['Limb neurological examination', 'Fundoscopy', 'Formal fields and audiometry', 'MRI if a lesion is suspected']),
    'E-ul': dict(map='body', props=['WIPER', 'Both arms exposed', 'Tendon hammer', '128 Hz fork', 'Neurotip', 'Cotton wool'], pins=[
        'Look: wasting, fasciculation, tremor; pronator drift>rarm',
        'Tone: wrist and elbow, both sides>larm',
        'Power: shoulder C5, elbow bend C5 to 6, straighten C7, wrist C6, fingers C7 to T1>rarm',
        'Reflexes: biceps C5 to 6, supinator C6, triceps C7>larm',
        'Coordination: finger to nose, rapid alternating movements>hands',
        'Sensation: each dermatome, then joint position and vibration>lhand'],
        hunt=['Weak, wasted, reflexes lost, fasciculation → lower motor neurone', 'Weak, stiff, brisk reflexes, drift → upper motor neurone',
              'Numb thumb to ring finger, weak thumb lift → carpal tunnel', 'Numb little finger, weak finger spreading → ulnar nerve', 'One dermatome numb, its reflex lost → radiculopathy'],
        done=['Lower limb neurological examination', 'Cervical spine', 'Nerve conduction studies', 'MRI']),
    'E-ll': dict(map='body', props=['WIPER', 'Legs exposed, groin covered', 'Tendon hammer', '128 Hz fork', 'Neurotip'], pins=[
        'Look: wasting, fasciculation, scars, footwear>legs',
        'Tone: roll the leg, lift the knee; ankle clonus>lleg',
        'Power: hip bend L1 to 2, knee straighten L3 to 4, foot up L4, big toe L5, foot down S1>legs',
        'Reflexes: knee L3 to 4, ankle S1 to 2, plantars>lleg',
        'Coordination: heel down the shin>feet',
        'Sensation: dermatomes from a sternum reference; is there a level?>abdo',
        'Gait: walk, heel to toe, Romberg>all'],
        hunt=['A sensory level, brisk reflexes, upgoing plantars → cord compression', 'Saddle numbness, retention, weak legs → cauda equina',
              'Numb in a stocking, ankle jerks lost → peripheral neuropathy', 'Foot drop with weak inversion and back pain → L5 root', 'Rising weakness, reflexes gone → Guillain-Barré'],
        done=['Upper limbs', 'Saddle sensation and anal tone', 'Bladder scan', 'Whole spine MRI if cord compression is possible']),
    'E-abdo': dict(map='body', props=['WIPER', 'Lying flat, one pillow', 'Expose nipples to knees', 'Ask where it hurts'], pins=[
        'End of the bed: jaundice, cachexia, distension, scars, stoma>all',
        'Hands: clubbing, white nails, red palms, Dupuytren\'s; liver flap>hands',
        'Face, neck, chest: yellow sclera, pallor, mouth; Virchow\'s node; spider naevi>neck',
        'Palpate all 9 regions: light, then deep, watching the face>abdo',
        'Organs: liver and spleen from the right iliac fossa; kidneys; aorta>ruq',
        'Percuss and listen: shifting dullness; bowel sounds, bruits>lif'],
        hunt=['Jaundice, red palms, spider naevi, ascites → chronic liver disease', 'Mass growing from the left upper quadrant toward the right iliac fossa, with a notch → spleen',
              'Pulsatile, expansile mass above the umbilicus → AAA', 'Iliac fossa scar over a mass → renal transplant', 'Spout in the right iliac fossa → ileostomy; flush on the left → colostomy'],
        done=['Hernial orifices', 'External genitalia', 'Digital rectal examination', 'Urine dip', 'Bloods and imaging']),
    'E-thyroid': dict(map='head', props=['WIPER', 'A chair you can stand behind', 'Glass of water', 'Sheet of paper', 'Tendon hammer'], pins=[
        'Look from the front: swelling; a sip of water: does it rise?>thyroid',
        'Tongue out: rises with the tongue → thyroglossal cyst>tongue',
        'Feel from behind: isthmus, both lobes, nodules; can you get below it?>neck',
        'Nodes and trachea; percuss the sternum; listen for a bruit>nodes',
        'Hands: sweaty, tremor under paper; pulse>hands',
        'Eyes: proptosis from above, lid retraction, lid lag, movements>eyes',
        'Status: reflexes, rise from a chair, shins>back'],
        hunt=['Smooth diffuse goitre with eye signs and a bruit → Graves\'', 'Lumpy goitre, older, no eye signs → multinodular', 'Single hard nodule with nodes → cancer pathway',
              'Dry, slow, cold, slow-relaxing reflexes → hypothyroid'],
        done=['TFTs and antibodies', 'Ultrasound', 'Fine needle aspiration of any nodule']),
    'E-ankle': dict(map='body', props=['WIPER', 'Both legs bare to the knee', 'Shoes and socks off', 'Ask about pain first'], pins=[
        'Look standing: arches, bunions, toes; tiptoe; walk; shoe wear>feet',
        'Feel: warmth, pulses, capillary refill; the Ottawa points; the Achilles>lleg',
        'Move: ankle up and down; heel in and out; midfoot; toes>feet',
        'Special: Simmonds\' squeeze; say the Ottawa decision>legs'],
        hunt=['Tender at the back edge or tip of a malleolus, or can\'t take 4 steps → X-ray', 'Calf squeeze doesn\'t point the foot → Achilles rupture',
              'Hot red big toe joint → gout', 'Bony bump at the big toe base → hallux valgus'],
        done=['Examine the knee', 'Neurovascular status', 'X-ray if Ottawa positive']),
    'E-elbow': dict(map='body', props=['WIPER', 'Both arms exposed', 'Ask about pain first'], pins=[
        'Look: carrying angle, swelling over the point, nodules, psoriasis>rarm',
        'Feel: both epicondyles, olecranon, radial head; ulnar nerve>larm',
        'Move: bend and straighten; palms up and down, elbows tucked in>rarm',
        'Special: Cozen\'s for tennis; resisted wrist flexion for golfer\'s; hand to mouth>lhand'],
        hunt=['Outer bump hurts on resisted wrist extension → tennis elbow', 'Inner bump hurts on resisted wrist flexion → golfer\'s elbow',
              'Soft swelling over the point of the elbow → olecranon bursitis', 'Firm nodules on the forearm → rheumatoid'],
        done=['Shoulder and wrist', 'Neurovascular check of the hand', 'X-ray']),
    'E-knee': dict(map='body', props=['WIPER', 'Both legs exposed, shorts on', 'Ask about pain first'], pins=[
        'Look standing: bow or knock knees, wasting, swelling, scars, a Baker\'s cyst>legs',
        'Feel: warmth; sweep test, patellar tap; joint lines with the knee bent>lleg',
        'Move: active, then passive, feeling for crepitus>legs',
        'Ligaments: collaterals at 20 to 30°; sag, then the drawers at 90°>lleg',
        'Walk and function>all'],
        hunt=['Twist, swelling within hours, positive anterior drawer → ACL', 'Joint line pain, locking, swelling the next day → meniscus',
              'Hot, swollen, can\'t move it, fever → septic arthritis: aspirate', 'Bony swelling, crepitus, bow legs → osteoarthritis'],
        done=['Examine the hip', 'Neurovascular status', 'X-ray; MRI for ligaments']),
    'E-hip': dict(map='body', props=['WIPER', 'Legs exposed, underwear on', 'Tape measure', 'Ask about pain first'], pins=[
        'Look standing: scars, wasting; walk; Trendelenburg on each leg>groin',
        'Lying: how the leg lies; true and apparent length>legs',
        'Feel: the greater trochanter>lleg',
        'Move: flexion; rotation at 90°; abduction with the other hip fixed>legs',
        'Thomas\' test for a fixed flexion deformity>lleg'],
        hunt=['Short, externally rotated leg after a fall → fractured neck of femur', 'Stiff painful hip, internal rotation lost first → osteoarthritis',
              'Pain lying on that side, tender trochanter → trochanteric bursitis', 'Pelvis drops on the other side when standing on this leg → weak abductors'],
        done=['Knee and lumbar spine', 'Neurovascular status', 'X-ray of the pelvis and hip']),
    'E-breast': dict(map='body', props=['WIPER', 'Chaperone, always', 'Expose to the waist', 'Ask about pain and lumps first'], pins=[
        'Look sitting: arms relaxed, hands on hips, arms up>breast',
        'Signs: asymmetry, dimpling, peau d\'orange, nipple inversion, discharge>chest',
        'Feel lying at 45°, hand behind the head: 4 quadrants, the tail, behind the nipple>breast',
        'Describe a lump: clock position, distance from the nipple, size, feel, fixed?>lchest',
        'Nodes: the 5 axillary groups, then above the collarbone>larm'],
        hunt=['Hard, irregular, fixed, tethered → suspected cancer pathway', 'Smooth, mobile, rubbery in a young woman → fibroadenoma',
              'Smooth, round, quick to appear near menopause → cyst', 'Hot, red, tender while breastfeeding → abscess'],
        done=['Triple assessment', 'Suspected cancer pathway if concerned', 'Abdomen for liver spread']),
    'E-scrotal': dict(map='body', props=['WIPER', 'Chaperone', 'Expose umbilicus to knees', 'Pen torch', 'Standing and lying'], pins=[
        'Look: skin, swelling, the lie of each testis>genit',
        'Feel the normal side first: testis, epididymis, cord>genit',
        'Any swelling: get above it? separate? lights up?>genit',
        'Cough impulse; varicocele standing and straining>groin'],
        hunt=['Hard lump in the testis itself → suspected cancer pathway', 'Can get above it, lights up, testis inside → hydrocele',
              'Separate, above and behind, lights up → epididymal cyst', 'Bag of worms that goes lying down → varicocele', 'Can\'t get above it, cough impulse → inguinal hernia'],
        done=['Abdomen for para-aortic nodes', 'Urgent ultrasound', 'Tumour markers for a testis lump']),
    'E-dre': dict(map='body', props=['WIPER', 'Chaperone, always', 'Left side, knees up', 'Gloves, lubricant, tissues'], pins=[
        'Look: tags, piles, fissure, fistula, warts, blood; bear down>genit',
        'Feel: tone and squeeze; sensation>genit',
        'Sweep all the way round; prostate at 12 o\'clock>supra',
        'Check the glove: blood, mucus, melaena>all'],
        hunt=['Smooth, enlarged, groove still there → BPH', 'Hard, craggy, groove lost → prostate cancer', 'Hard mass in the wall, blood on the glove → rectal cancer',
              'Lax tone, numb saddle → cauda equina'],
        done=['Abdominal examination', 'Urine dip', 'PSA after counselling', 'Bladder scan']),
    'E-genit': dict(map='body', props=['WIPER', 'Chaperone', 'Gloves', 'Good light', 'Expose umbilicus to knees'], pins=[
        'Groin: nodes, lumps, cough impulse>groin',
        'Penis: shaft, then retract the foreskin: glans and meatus; replace it>genit',
        'Scrotum and testes>genit'],
        hunt=['Painful grouped blisters → herpes', 'Painless firm single ulcer → primary syphilis', 'Cauliflower lumps → warts', 'Foreskin stuck back and swollen → paraphimosis: reduce now'],
        done=['Swabs and urine NAAT', 'Sexual health screen including HIV and syphilis', 'Partner notification']),
    'E-rash': dict(map='body', props=['WIPER', 'Good light', 'A glass to press on', 'Gloves', 'Ask: how long, itch, new products or drugs'], pins=[
        'Where: site and pattern: flexures, extensors, sun-exposed, one dermatome, symmetrical>skin',
        'What: number, type of lesion, size, shape, arrangement>skin',
        'Colour, edge, surface; does it blanch?>skin',
        'Feel it; then nails, scalp, mouth, joints>hands'],
        hunt=['Silvery plaques on elbows and knees, pitted nails → psoriasis', 'Itchy dry flexures → eczema', 'Ring with a scaly edge, clear centre → tinea',
              'Painful band of blisters on one side → shingles', 'Non-blanching rash in an unwell patient → meningococcal: emergency'],
        done=['Full skin check', 'Scrapings for fungus; swabs if infected', 'Biopsy if unsure']),
    'E-lesion': dict(map='body', props=['WIPER', 'Good light', 'Ruler', 'Dermatoscope', 'Ask: changed? itch? bleeding?'], pins=[
        'Describe: site, number, size in mm, shape, colour, border, surface>skin',
        'ABCDE out loud; score the weighted 7-point checklist>skin',
        'Feel: raised, firm, tender, fixed>skin',
        'The rest of the skin and the nearby nodes>larm'],
        hunt=['Changing, irregular, several colours, over 6 mm → melanoma: cancer pathway', 'Pearly, rolled edge, tiny vessels → BCC: routine',
              'Crusted, tender, growing nodule → SCC: cancer pathway', 'Stuck-on, warty, greasy → seborrhoeic keratosis'],
        done=['Dermatoscopy and photographs', 'Suspected cancer pathway for melanoma or SCC', 'Excision biopsy']),
    'E-nose': dict(map='head', props=['WIPER', 'Sit opposite at the same level', 'Thudichum speculum or otoscope', 'Cold metal spatula'], pins=[
        'Outside: from the front, the side and above; lift the tip>nose',
        'Airflow: block one side and sniff; misting on cold metal>nose',
        'Inside: septum, turbinates, polyps, a bleeding point>nose',
        'Feel: sinuses for tenderness; neck nodes>cheek'],
        hunt=['Pale grey grapes that don\'t hurt to touch → polyps', 'Pale swollen turbinates, sneezing → allergic rhinitis',
              'Bleeding point at the front of the septum → Little\'s area', 'Boggy septal swelling after an injury → haematoma: drain today'],
        done=['Mouth, ears and neck nodes', 'Nasendoscopy', 'Smell testing']),
    'E-mouth': dict(map='head', props=['WIPER', 'Gloves', 'Pen torch', '2 tongue depressors', 'Dentures out'], pins=[
        'Lips and the corners of the mouth>mouth',
        'Cheeks and the parotid duct; gums and teeth>cheek',
        'Palate; tongue on every side and underneath; floor of the mouth>tongue',
        'Throat: tonsils, uvula, back wall>throat',
        'Feel: floor of the mouth with both hands; neck nodes>nodes'],
        hunt=['Ulcer or red or white patch over 3 weeks → cancer pathway', 'Swollen tonsils with pus, front neck nodes → tonsillitis',
              'One side bulges, uvula pushed away → quinsy: ENT today', 'White plaques that wipe off → thrush'],
        done=['Ears and nose', 'Suspected cancer referral for an ulcer over 3 weeks']),
    'E-ear': dict(map='head', props=['WIPER', 'Otoscope with a new speculum', '512 Hz fork', 'Start with the good ear'], pins=[
        'Look and feel: pinna, behind it, the mastoid; press the tragus>rear',
        'Otoscope: pull up and back, brace your hand on the cheek>rear',
        'Drum: colour, light reflex, malleus handle, the attic>rear',
        'Hearing: whisper test, rubbing the other tragus>lear',
        'Rinne: on the mastoid, then beside the ear>lear',
        'Weber: in the middle of the forehead>forehead'],
        hunt=['Red bulging drum in an unwell child → otitis media', 'Dull retracted drum, hearing loss → glue ear', 'Swollen painful canal, worse pulling the ear → otitis externa',
              'A hole in the drum → perforation', 'Rinne positive both sides, Weber to the good ear → sensorineural loss on the bad side'],
        done=['Cranial nerves V and VII', 'Nose and throat', 'Audiometry and tympanometry']),
    'E-nodes': dict(map='body', props=['WIPER', 'Patient seated, you behind', 'Head tilted slightly forward'], pins=[
        'Neck in order: under the chin and jaw, front and back of the neck, above the collarbone>neck',
        'Describe a node: site, size, feel, tender, mobile, matted>neck',
        'Armpit: 5 groups, taking the weight of the arm>larm',
        'Groin: along the ligament>groin'],
        hunt=['Small, tender, with a sore throat → reactive', 'Back neck nodes, big spleen, tired teenager → glandular fever',
              'Rubbery, painless, several areas, night sweats → lymphoma', 'Hard fixed node above the left collarbone → Virchow\'s: stomach cancer'],
        done=['Examine the area that drains to it', 'Liver and spleen', 'FBC, film, ESR', 'Ultrasound and biopsy']),
    'E-anteye': dict(map='head', props=['WIPER', 'Snellen chart', 'Pen torch with a blue light', 'Fluorescein', 'Cotton bud to evert the lid'], pins=[
        'Acuity first, with glasses; pinhole>reye',
        'Lids and lashes>brow',
        'Conjunctiva and sclera: the pattern of red, discharge>leye',
        'Cornea: clarity; fluorescein for ulcers>reye',
        'Front chamber: depth, a pus or blood level>leye',
        'Pupils: shape, size, direct and consensual>eyes'],
        hunt=['Gritty, sticky, vision normal → conjunctivitis', 'Small irregular pupil, ring of red, light hurts → uveitis',
              'Hard eye, mid-dilated pupil, halos, vomiting → acute angle closure', 'Branching ulcer on fluorescein → herpes: no steroid drops', 'Flat bright red patch, no pain → subconjunctival bleed'],
        done=['Eye movements', 'Fundoscopy', 'Eye pressure', 'Same-day eye casualty for any red flag']),
    'E-eye': dict(map='head', props=['WIPER', 'Snellen at 6 metres', 'Pinhole', 'Red hatpin', 'Sit 1 metre opposite, eyes level'], pins=[
        'Acuity: each eye with glasses on; record 6 over the line>reye',
        'Worse than 6/9: pinhole; can\'t read the top letter: fingers, hand, light>leye',
        'Fields: a wiggling finger in from each quadrant, one eye at a time>reye',
        'Central field and blind spot with the red pin>leye'],
        hunt=['Outer halves of both fields gone → bitemporal: pituitary', 'The same half gone in both eyes → homonymous: behind the chiasm',
              'An upper quarter gone on one side → temporal lobe', 'Sudden painless loss, pale retina → CRAO', 'Painful eye movements, colours fade → optic neuritis'],
        done=['Pupils', 'Eye movements', 'Fundoscopy', 'Colour vision', 'Formal perimetry']),
    'E-fundo': dict(map='head', props=['WIPER', 'Dim the room', 'Say you would dilate with tropicamide', 'Ophthalmoscope', 'Patient fixes on a far point'], pins=[
        'Right eye: your right hand and right eye; red reflex from 50 cm>reye',
        'Come in 15° from the side to find the disc: colour, margins, cup>reye',
        'Vessels in 4 directions; the macula last>reye',
        'Left eye: your left hand and left eye>leye'],
        hunt=['Dots, blots, hard exudates → background diabetic retinopathy', 'New fragile vessels → proliferative: urgent referral',
              'Silver wiring, AV nipping, flame bleeds → hypertensive', 'Swollen blurred discs on both sides → papilloedema', 'Pale retina, cherry-red spot → CRAO; bleeds everywhere → CRVO'],
        done=['Acuity, fields and pupils', 'Retinal photographs', 'Refer as needed']),
}

STORY = {
    'P-bpm': dict(fail=['Wrong cuff, or the arm not supported at heart level', 'Letting the air out too fast', 'Not acting on 180 over 120'], nums=[
        ['Rest first', '5 minutes seated'], ['Cuff', 'bladder covers about 80% of the arm'], ['Inflate', '20 to 30 mmHg past where the pulse vanished'],
        ['Deflate', '2 to 3 mmHg per second'], ['140 over 90 or more in clinic', 'offer home or ambulatory monitoring'], ['Postural drop', '20 systolic or 10 diastolic within 3 min']]),
    'P-wash': dict(fail=['A watch, rings or long sleeves', 'Missing the thumbs and fingertips', 'Turning the tap off with clean hands'], nums=[
        ['Soap and water', '40 to 60 seconds'], ['Alcohol gel', '20 to 30 seconds'], ['Soap, never gel', 'diarrhoea, C. difficile, visibly dirty hands'],
        ['5 moments', 'before the patient, before a clean task, after body fluid, after the patient, after the surroundings']]),
    'P-cbg': dict(fail=['Not checking the meter control and strip expiry', 'Pricking the pad or milking the finger', 'Not acting on the number'], nums=[
        ['Hypo', 'under 4 mmol/L: treat now'], ['Type 1 over 11', 'check ketones'], ['Site', 'side of the fingertip, middle or ring finger']]),
    'P-inhaler': dict(fail=['Teaching before watching their technique', 'A fast breath with a metered-dose inhaler, or no breath hold', 'No teach-back'], nums=[
        ['Breath in', 'slow and deep for a metered-dose inhaler'], ['Hold', '10 seconds'], ['Between puffs', '30 to 60 seconds'],
        ['Steroid inhaler', 'rinse and spit'], ['Spacer', 'one puff at a time; wash monthly, air dry']]),
    'P-pefr': dict(fail=['Not resetting the pointer', 'Fingers over the scale, or only 1 blow', 'Not comparing with their best or predicted'], nums=[
        ['Blows', 'best of 3'], ['Acute severe asthma', '33 to 50% of best or predicted'], ['Life-threatening', 'under 33%'], ['Variability', 'over 20% supports asthma']]),
    'P-obs': dict(fail=['Telling them you are counting their breathing', 'A cold finger or the wrong cuff', 'Scoring without acting'], nums=[
        ['NEWS2 3 in one parameter', 'urgent ward review'], ['NEWS2 5 or 6', 'urgent response'], ['NEWS2 7 or more', 'emergency response'],
        ['SpO2 scale 2', 'target 88 to 92% if they retain CO2'], ['New confusion', 'scores 3 on its own']]),
    'P-ecg12': dict(fail=['No chaperone or exposure without consent', 'Chest leads in the wrong spaces', 'Not labelling the trace or showing it to a senior'], nums=[
        ['V1', '4th space, right sternal edge'], ['V2', '4th space, left sternal edge'], ['V4', '5th space, midclavicular line'], ['V3', 'between V2 and V4'],
        ['V5, V6', 'level with V4, front and mid armpit lines'], ['Limb leads', 'Ride Your Green Bike: red right arm, yellow left arm, green left leg, black right leg'],
        ['Paper', '25 mm/s, 10 mm/mV']]),
    'P-ecg3': dict(fail=['Leads on the wrong side', 'Not checking the trace', 'No alarm limits'], nums=[
        ['Red', 'right shoulder'], ['Yellow', 'left shoulder'], ['Green', 'lower left chest'], ['View', 'lead II']]),
    'P-dip': dict(fail=['An old sample or out-of-date strips', 'Reading every pad at the same moment', 'Reporting protein with no plan'],
                  more=['Protein → BP, U&E and eGFR, early-morning ACR, MSU to rule out infection, HbA1c; repeat to confirm'],
                  nums=[['Nitrites and leucocytes', 'UTI likely; culture if pregnant, male, a child or treatment failed'],
                        ['Blood alone', 'exclude infection and periods, repeat; visible 45+ or non-visible 60+ with symptoms: cancer pathway'],
                        ['Protein', 'confirm with ACR: 3 mg/mmol or more is raised; 70 or more needs a kidney referral'],
                        ['Glucose', 'capillary glucose and HbA1c'], ['Ketones with glucose', 'think DKA']]),
    'P-cann': dict(fail=['No allergy check, or not letting the chlorhexidine dry', 'Pushing on after the flashback without dropping the angle', 'No flush, no documentation'], nums=[
        ['Angle', '10 to 30 degrees, bevel up'], ['Skin prep', '2% chlorhexidine in 70% alcohol: 30 seconds, then dry'],
        ['Size', 'pink 20G routine; green 18G or grey 16G for fast fluids or blood'], ['Attempts', 'stop after 2 and ask for help']]),
    'P-venep': dict(fail=['No check of which arm to avoid', 'Taking the needle out before the tourniquet', 'Labelling away from the bedside'], nums=[
        ['Angle', 'about 30 degrees, bevel up'], ['Tourniquet', 'under 1 minute'], ['Order of draw', 'cultures, blue, gold or red, green, purple, grey']]),
    'P-abg': dict(fail=['Skipping the modified Allen\'s test or the anticoagulant check', 'Pulling on the plunger instead of letting it fill', 'Not recording the inspired oxygen'], nums=[
        ['Angle', '30 to 45 degrees, bevel up'], ['Press', '5 minutes or more, longer if anticoagulated'], ['Analyse', 'within 10 to 15 minutes'],
        ['Normal', 'pH 7.35 to 7.45; PaCO2 4.7 to 6.0; PaO2 over 10 kPa on air; bicarbonate 22 to 26']]),
    'P-swab': dict(fail=['No eye protection or mask', 'Missing the tonsils or the back of the throat', 'Unlabelled sample, no clinical details'], nums=[
        ['Order', 'throat first, then the nose, with the same swab'], ['Nose', 'along the floor, about 2 cm in, rotate'], ['Wound', 'clean with saline, then zig-zag while rotating']]),
    'P-catm': dict(fail=['No allergy check, especially latex and lidocaine', 'Not waiting 3 to 5 minutes for the gel', 'Inflating before urine flows, or leaving the foreskin back'], nums=[
        ['Catheter', '12 to 14 Ch'], ['Gel', 'lidocaine, wait 3 to 5 minutes'], ['Balloon', '10 ml sterile water, only after urine flows'], ['Penis', 'held upright at 90 degrees']]),
    'P-catf': dict(fail=['No chaperone', 'Letting go of the labia and contaminating the field', 'Inflating before urine flows'], nums=[
        ['Catheter', '12 to 14 Ch, female length'], ['Insert', 'until urine flows, then 2 cm more'], ['Balloon', '10 ml sterile water']]),
}


def check(stations):
    """Fail the build if a poster points at a station that is not there, or a pin at a place the map doesn't have."""
    ids = {s['id']: s for s in stations}
    exs = sorted(s['id'] for s in stations if s['type'] == 'ex')
    prs = sorted(s['id'] for s in stations if s['type'] == 'proc')
    assert sorted(ROUTES) == exs, ('exam routes', set(ROUTES) ^ set(exs))
    assert sorted(STORY) == prs, ('procedure stories', set(STORY) ^ set(prs))
    out = {'routes': {}, 'story': {}}
    for k, r in ROUTES.items():
        places = HEAD if r['map'] == 'head' else BODY
        pins = []
        for p in r['pins']:
            body, loc = p.rsplit('>', 1)
            lab, cue = body.split(':', 1) if ':' in body else (body, '')
            assert loc in places, (k, loc)
            pins.append([lab.strip(), loc.strip(), cue.strip()])
        out['routes'][k] = {'map': r['map'], 'props': r['props'], 'pins': pins, 'hunt': r['hunt'], 'done': r['done']}
    for k, s in STORY.items():
        assert len(s['fail']) == 3, k
        out['story'][k] = s
    import json
    blob = json.dumps(out, ensure_ascii=False)
    assert '—' not in blob and '(' not in blob, 'em dash or bracket in station posters'
    return out
