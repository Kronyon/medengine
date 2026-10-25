from .common import station

DOOR = 'You are an FY1. {who} {task} Present your findings to the examiner.'

station('E-rash', 'ex', 'Describing a rash', 'Speciality', ffp='Describing a rash', u=[139, 137, 128, 134, 126, 125],
  door=DOOR.format(who='A 32-year-old man has had an itchy rash on his elbows and knees for months.', task='Examine and describe the rash.'),
  hooks=[
    '**Describe it like a phone call to a dermatologist who can\'t see it:** Where → What → Colour → Edge → Surface → What else.',
    '**Size rules:** flat under 1 cm = macule, over = patch. Raised under 1 cm = papule, over = plaque. Fluid under 0.5 cm = vesicle, over = bulla.',
    '**Press it:** fades = blanching. Doesn\'t fade under a glass = purpura: in an unwell person think meningococcal sepsis now.',
    '**Silvery scale on the extensors = psoriasis. Ill-defined, itchy, flexures = eczema. Ring with a scaly edge and clear centre = tinea.**',
  ],
  money='On the extensor surfaces of both elbows and knees, there are multiple, symmetrical, well-demarcated, salmon-pink plaques up to 4 cm across, with a silvery scale. They blanch. There is pitting of the fingernails. There are no signs of infection. These findings are consistent with **chronic plaque psoriasis**. I would ask about joint pain, and start an **emollient with a potent topical steroid and a vitamin D analogue**.',
  traps=['Naming a diagnosis before describing the morphology', 'Not checking whether it blanches', 'Forgetting the nails, scalp and mouth', 'Not palpating'],
  dg=['lesion', 'rashpat'],
  secs=[
    ('Prepare', [
      '!Consent, good light, expose the whole area; offer a chaperone || Would it be OK to look at your skin in a good light? || ',
      'Quick history: how long, itch or pain, spreading, new products or drugs, systemically unwell || || A drug started 1 to 2 weeks ago can cause a widespread rash.',
    ]),
    ('Where', [
      '!Site and distribution: flexural, extensor, sun-exposed, dermatomal, symmetrical, widespread || || The pattern often gives the diagnosis before the lesion does.',
    ]),
    ('What', [
      '!Number and morphology: macule, patch, papule, plaque, nodule, vesicle, bulla, pustule, wheal || These are plaques, as they are raised and over 1 centimetre. || Morphology words are the core of the mark scheme.',
      'Size in centimetres; shape and arrangement: annular, linear, target, grouped, discrete or merging || || A line along a scratch = Koebner\'s phenomenon, seen in psoriasis.',
    ]),
    ('Colour, edge and surface', [
      'Colour: erythematous, salmon pink, violaceous, pigmented, hypopigmented || || ',
      '!Blanching: press with a glass slide or your fingers || I\'m going to press on the rash. || Non-blanching = purpura.',
      'Edge: well demarcated or ill defined || || ',
      'Surface: scale, crust, excoriation, lichenification, ulceration, weeping || || ',
    ]),
    ('Feel and look further', [
      'Palpate with gloves: texture, warmth, tenderness || || ',
      '!Look at the nails, scalp, mouth and joints || Can I look at your nails and scalp? || Nail pits and scalp plaques support psoriasis.',
    ]),
    ('Finish and complete', [
      '!Complete: full skin check, skin scrapings for fungus, swabs if infected, biopsy if unsure, photographs || || ',
    ]),
  ],
  cases=[
    ('Plaque psoriasis', 'Well-demarcated salmon-pink plaques with silvery scale on elbows, knees and scalp; nail pitting.', '... **chronic plaque psoriasis**: emollient, potent steroid with calcipotriol; ask about joints.'),
    ('Atopic eczema', 'Ill-defined, dry, red patches in the elbow and knee creases, excoriated and lichenified.', '... **atopic eczema**: emollients, topical steroid ladder; treat infection.'),
    ('Tinea corporis', 'Single annular plaque with a scaly raised edge and clearing centre on the trunk.', '... **tinea corporis**: skin scrapings, topical terbinafine; avoid steroids.'),
    ('Shingles', 'Grouped vesicles on a red base in one dermatome on one side of the chest, painful.', '... **herpes zoster**: aciclovir within 72 hours; check the eye if the nose tip is involved.'),
    ('Meningococcal rash', 'Non-blanching purpuric spots in an unwell, feverish young adult.', '... a **non-blanching purpuric rash in an unwell patient**: meningococcal sepsis until proven otherwise; IV ceftriaxone, or IM benzylpenicillin before transfer.'),
    ('Urticaria', 'Raised, itchy, pale wheals with red flare that move around within 24 hours.', '... **urticaria**: non-sedating antihistamine; look for angioedema.'),
  ])

station('E-lesion', 'ex', 'Describing pigmented and non-pigmented lesions', 'Speciality', ffp='Pigmented & non-pigmented lesions', u=[122, 123, 124, 139],
  door=DOOR.format(who='A 64-year-old retired builder has a mole on his back that his wife says has changed.', task='Examine and describe the lesion.'),
  hooks=[
    '**ABCDE:** Asymmetry, Border irregular, Colour varied, Diameter over 6 mm, Evolving.',
    '**Weighted 7-point checklist:** change in size, shape or colour = 2 points each; 7 mm or more, inflamed, oozing, altered sensation = 1 each. **3 or more → suspected cancer referral.**',
    '**Pearly rolled edge + tiny vessels + slow = BCC. Crusted, fast, tender = SCC.**',
    '**Stuck-on, waxy, warty = seborrhoeic keratosis,** harmless.',
    '**The ugly duckling:** one mole that looks unlike all the others.',
  ],
  money='On the left upper back, there is a single, 9 mm, asymmetrical, pigmented macule with an irregular border and variable brown and black colour. It has grown over the last 3 months. It scores 5 on the weighted 7-point checklist. There are no palpable lymph nodes. These findings are **suspicious of melanoma**. I would refer him on the **suspected cancer pathway** for dermatology assessment and excision biopsy.',
  traps=['Not measuring the lesion', 'Not scoring the 7-point checklist out loud', 'Forgetting the regional lymph nodes', 'Not checking the rest of the skin'],
  dg=['abcde', 'lesion'],
  secs=[
    ('Prepare and ask', [
      '!Consent, good light, chaperone if needed || || ',
      'How long, has it changed in size, shape or colour, itch, bleeding, sun exposure and burns, sunbeds, family history, immunosuppression || Have you noticed it change at all? || Change is the strongest warning sign.',
    ]),
    ('Describe', [
      '!Site, number, size measured in mm, shape, colour, border, surface || It is a single 9 millimetre pigmented lesion on the left upper back. || ',
      '!ABCDE out loud || || ',
      '!Score the weighted 7-point checklist || || ',
    ]),
    ('Feel and check', [
      'Palpate: raised, firm, tender, fixed || || ',
      'Dermatoscope if available || || ',
      '!Check the rest of the skin and the regional lymph nodes || || ',
    ]),
    ('Finish and complete', [
      '!Plan: suspected cancer pathway for suspected melanoma or SCC; routine referral for most BCCs || || NICE NG12.',
    ]),
  ],
  cases=[
    ('Melanoma', 'Asymmetrical, irregular, multicoloured 9 mm lesion that has grown.', '... **suspicious of melanoma**: suspected cancer pathway; excision biopsy.'),
    ('Basal cell carcinoma', 'Pearly nodule with a rolled edge, telangiectasia and central ulcer on the side of the nose.', '... a **BCC**: usually a routine dermatology referral; excision or Mohs surgery.'),
    ('Squamous cell carcinoma', 'Rapidly growing, crusted, tender nodule on the back of the hand of a transplant patient.', '... **suspicious of SCC**: suspected cancer pathway.'),
    ('Seborrhoeic keratosis', 'Multiple brown, waxy, warty stuck-on plaques on the back.', '... **seborrhoeic keratoses**: reassure.'),
    ('Benign naevus', 'Small, symmetrical, uniformly brown mole with a smooth border, unchanged for years.', '... a **benign melanocytic naevus**: reassure and safety-net about change.'),
  ])

station('E-nose', 'ex', 'Nasal cavity examination', 'Speciality', ffp='Nasal Cavity', u=[144, 150, 147],
  door=DOOR.format(who='A 45-year-old woman has had a blocked nose on the right for 3 months.', task='Examine the nose.'),
  hooks=[
    '**Outside, airflow, inside:** look at the nose from the front, side and above; test each nostril; then look inside with the speculum or otoscope.',
    '**Poke test:** a polyp is grey, like a peeled grape, and has no feeling. A turbinate is pink and sensitive.',
    '**Little\'s area on the front of the septum causes about 90% of nosebleeds.**',
    '**One-sided polyp, blood-stained discharge or blockage in an adult = refer to exclude a tumour.**',
    '**Septal haematoma after a broken nose = drain it today,** or the cartilage dies and the nose collapses.',
  ],
  money='On examination of this lady\'s nose, the external nose was straight with no swelling. Airflow was reduced through the right nostril. On anterior rhinoscopy, the septum was central. There was a smooth, grey, insensate mass in the right nasal cavity. The left side was normal. These findings are consistent with a **right nasal polyp**. As it is **one-sided**, I would refer to ENT for **nasendoscopy** to exclude a tumour.',
  traps=['Forgetting to test each nostril\'s airflow', 'Not tipping the nose up to see the vestibule', 'Forgetting to say nasendoscopy'],
  dg=['nose'],
  secs=[
    ('Look outside', [
      '!Consent; sit opposite at the same level; inspect from the front, side and above for deviation, swelling, skin changes || I\'m going to look at your nose from a few angles. || ',
      'Lift the tip with your thumb to see the vestibule || || ',
    ]),
    ('Airflow', [
      'Block one nostril at a time and ask them to sniff, or hold a cold metal tongue depressor under the nose and look for misting || Could you breathe in through your nose while I block one side? || ',
    ]),
    ('Look inside', [
      '!Anterior rhinoscopy with a Thudichum speculum or an otoscope with a large speculum: septum, Little\'s area, inferior turbinates, polyps, discharge, crusting || I\'m going to look inside your nose with a light; it shouldn\'t hurt. || ',
    ]),
    ('Feel', [
      'Palpate over the frontal and maxillary sinuses for tenderness; feel the nasal bones || || ',
    ]),
    ('Finish and complete', [
      '!Complete: examine the mouth, ears and neck nodes; nasendoscopy; smell test || To complete, I would examine the throat, ears and neck, and arrange nasendoscopy. || ',
    ]),
  ],
  cases=[
    ('Nasal polyps', 'Bilateral grey insensate masses, reduced smell, asthma.', '... **bilateral nasal polyps**: steroid nasal drops; one-sided ones need ENT referral.'),
    ('Allergic rhinitis', 'Pale, swollen, boggy inferior turbinates with clear discharge.', '... **allergic rhinitis**: antihistamine and steroid nasal spray.'),
    ('Epistaxis from Little\'s area', 'Prominent vessels with a clot on the front of the septum.', '... **anterior epistaxis**: first aid, then silver nitrate cautery.'),
    ('Deviated septum', 'Septum bowed to the left, blocking the left nostril.', '... a **deviated nasal septum**: septoplasty if symptomatic.'),
    ('Septal haematoma', 'Boggy, red, bilateral swelling of the septum after a punch.', '... a **septal haematoma**: same-day ENT drainage.'),
  ])

station('E-mouth', 'ex', 'Oral cavity examination', 'Speciality', ffp='Oral Cavity', u=[151, 143, 145],
  door=DOOR.format(who='A 58-year-old smoker has a sore patch on the side of his tongue for 5 weeks.', task='Examine the mouth.'),
  hooks=[
    '**Lips → cheeks → gums and teeth → roof → tongue top, sides, underneath → floor → throat.** Lift and look under, or you miss the commonest cancer sites.',
    '**Any ulcer or red or white patch for over 3 weeks = suspected cancer referral.**',
    '**White patch that wipes off = thrush. Won\'t wipe off = leukoplakia.**',
    '**Quinsy:** can\'t open the mouth, hot-potato voice, uvula pushed to the other side.',
  ],
  money='On examination of this gentleman\'s mouth, using a light and two tongue depressors, the lips, cheeks, gums and palate were normal. On the right lateral border of the tongue there was a 1.5 cm, painless, firm ulcer with a raised, rolled edge. There was a firm right submandibular lymph node. These findings are **suspicious of squamous cell carcinoma of the tongue**. I would refer him on the **suspected cancer pathway** to oral and maxillofacial surgery or ENT.',
  traps=['Not removing dentures', 'Forgetting to lift the tongue and look at the floor of the mouth', 'Forgetting the neck nodes'],
  dg=['mouth'],
  secs=[
    ('Prepare', [
      '!Consent, gloves, pen torch, two tongue depressors; remove dentures || Do you wear dentures? Could you take them out for me? || ',
    ]),
    ('Look in order', [
      'Lips and corners of the mouth || || Cracks at the corners = angular cheilitis: iron, B vitamins, thrush.',
      'Cheeks: both sides, with the parotid duct opening opposite the upper second molar || || ',
      'Gums and teeth || || ',
      'Hard and soft palate || || ',
      '!Tongue: top, both sides, then lift it to see underneath and the floor of the mouth || Could you touch the roof of your mouth with your tongue? || The side and underneath of the tongue are the commonest oral cancer sites.',
      'Throat: tonsils, uvula, back wall; say ahh || Could you say ahh? || ',
      'Stick the tongue out || || It deviates toward a twelfth nerve lesion.',
    ]),
    ('Feel', [
      'Bimanual palpation of the floor of the mouth and submandibular gland, with consent || || A stone in the duct can be felt.',
      '!Neck lymph nodes || || ',
    ]),
    ('Finish and complete', [
      '!Complete: examine the ears and nose; refer ulcers or patches over 3 weeks on the suspected cancer pathway || || ',
    ]),
  ],
  cases=[
    ('Oral cancer', 'Painless firm ulcer with a rolled edge on the side of the tongue for 5 weeks; neck node.', '... **suspicious of oral SCC**: suspected cancer pathway.'),
    ('Tonsillitis', 'Large red tonsils with white exudate, tender neck nodes, fever.', '... **acute tonsillitis**: FeverPAIN score; antibiotics only if the score is high.'),
    ('Quinsy', 'Trismus, one-sided bulge above the tonsil, uvula pushed away.', '... a **peritonsillar abscess**: same-day ENT for drainage and IV antibiotics.'),
    ('Oral thrush', 'White plaques that wipe off leaving red areas, in an inhaled steroid user.', '... **oral candidiasis**: nystatin or miconazole; rinse after the inhaler.'),
    ('Leukoplakia', 'White patch on the cheek that won\'t wipe off, in a smoker.', '... **leukoplakia**, a premalignant patch: refer for biopsy.'),
  ])

station('E-ear', 'ex', 'Otoscopy and hearing', 'Speciality', ffp='Otoscopy + Hearing', u=[149, 148, 140, 146],
  door=DOOR.format(who='A 40-year-old man has had hearing loss in his left ear for 2 months.', task='Examine the ears and test his hearing.'),
  hooks=[
    '**Good ear first.** Pull the pinna **up and back** in adults; just back in children.',
    '**Hold the otoscope like a pen with your little finger braced on the cheek,** so a sudden move won\'t push it in.',
    '**Cone of light points to the nose:** 5 o\'clock in the right ear, 7 o\'clock in the left.',
    '**Weber goes to the BAD ear in conductive loss and the GOOD ear in sensorineural loss.**',
    '**Rinne negative = bone louder than air = conductive loss in that ear.**',
    '**One-sided sensorineural loss or tinnitus = MRI to exclude an acoustic neuroma.**',
  ],
  money='On examination, the left pinna and canal were normal. The left tympanic membrane was dull and retracted with a fluid level. The right ear was normal. The whisper test was reduced on the left. Rinne\'s test was negative on the left and positive on the right, and Weber\'s lateralised to the left. These findings are consistent with a **left conductive hearing loss due to otitis media with effusion**. In an adult with one-sided glue ear I would refer to ENT to examine the **postnasal space**.',
  traps=['Wrong pinna direction', 'Not bracing the hand holding the otoscope', 'Mixing up Rinne\'s and Weber\'s interpretation', 'Using a speculum that is too small, or not changing it'],
  dg=['drum', 'rinne'],
  secs=[
    ('Look and feel', [
      '!Ask about pain or discharge; start with the good ear || Is either ear sore, or has anything come out? || ',
      'Pinna front and behind, the mastoid, scars; press the tragus || || Tragal tenderness = otitis externa.',
    ]),
    ('Otoscopy', [
      '!Largest comfortable speculum, new; hold like a pen and brace on the cheek; pull the pinna up and back || I\'m going to gently pull your ear and look inside with a light. || ',
      'Canal: wax, discharge, swelling, foreign body || || ',
      '!Drum: colour, cone of light, handle of malleus, the attic, bulging or retraction, perforation, fluid level, grommet || || The attic at the top is where cholesteatoma hides.',
    ]),
    ('Hearing', [
      '!Whispered voice test: mask the other ear by rubbing the tragus, whisper a number and a letter from arm\'s length || Repeat what I whisper. || ',
      '!Rinne\'s: 512 Hz fork on the mastoid, then beside the ear || Which is louder: here, or here? || Normal: air louder than bone = Rinne positive.',
      '!Weber\'s: fork in the middle of the forehead || Where do you hear it: left, right or in the middle? || ',
    ]),
    ('Finish and complete', [
      '!Complete: cranial nerves V and VII, nose and throat, formal audiometry and tympanometry || To complete, I would arrange an audiogram and tympanometry. || ',
    ]),
  ],
  cases=[
    ('Acute otitis media', 'Red, bulging drum with no cone of light; pain and fever.', '... **acute otitis media**: analgesia; most settle in 3 days; antibiotics if very unwell or discharging.'),
    ('Glue ear', 'Dull, retracted drum with a fluid level and bubbles; conductive loss.', '... **otitis media with effusion**; one-sided in an adult needs the postnasal space checked.'),
    ('Otitis externa', 'Swollen, tender canal with debris; tragal tenderness; drum hard to see.', '... **otitis externa**: aural toilet and topical antibiotic with steroid drops.'),
    ('Perforation', 'Hole in the lower drum with a dry canal.', '... a **tympanic membrane perforation**: keep the ear dry; most heal in 6 weeks.'),
    ('Cholesteatoma', 'Crust or white mass in the attic with foul-smelling discharge.', '... suspected **cholesteatoma**: ENT referral for surgery.'),
    ('Acoustic neuroma', 'Normal drums; left sensorineural loss: Rinne positive both sides, Weber to the right.', '... a **left sensorineural hearing loss**: MRI of the internal auditory meatus to exclude a vestibular schwannoma.'),
  ])

station('E-nodes', 'ex', 'Lymph node examination', 'Speciality', ffp='Lymph node exam', u=[145, 57, 20, 151],
  door=DOOR.format(who='A 24-year-old has noticed lumps in her neck for 4 weeks, with night sweats.', task='Examine her lymph nodes.'),
  hooks=[
    '**Neck from behind, in a loop:** under the chin → under the jaw → front of the ear → behind the ear → back of the head → down the back of the neck → above the collarbone → up the front of the neck.',
    '**Describe like a lump:** site, size, shape, consistency, tender, fixed, matted, overlying skin.',
    '**Soft and tender = reactive. Rubbery and painless = lymphoma. Hard and fixed = cancer.**',
    '**Left supraclavicular node = Virchow\'s:** look in the abdomen for a gastric cancer.',
    '**Always examine where it drains from, and the liver and spleen.**',
  ],
  money='On examination, there were multiple, painless, rubbery lymph nodes up to 2.5 cm in the right anterior and posterior cervical chains and right supraclavicular fossa. They were mobile and not tender. There was no axillary or inguinal lymphadenopathy and no hepatosplenomegaly. With her night sweats, these findings are **concerning for lymphoma**. I would request an **FBC, blood film, LDH**, and refer urgently for **lymph node biopsy**.',
  traps=['Missing the supraclavicular fossa', 'Not examining from behind', 'Forgetting the liver and spleen', 'Not examining the drainage area'],
  dg=['nodes'],
  secs=[
    ('Head and neck', [
      '!Consent; stand behind the seated patient with the head tilted slightly forward || I\'m going to stand behind you and feel the glands in your neck. || Tilting forward relaxes the neck muscles.',
      '!Feel with the pads of the fingers in order: submental, submandibular, preauricular, postauricular, occipital, posterior triangle, supraclavicular, anterior chain || || A fixed order means none are missed.',
      '!Describe any node: site, size, consistency, tenderness, mobility, matting, overlying skin || || ',
    ]),
    ('Axilla', [
      'Take the weight of the arm; feel the 5 groups: anterior, posterior, medial, lateral, apical || Let me hold your arm; let it go relaxed. || ',
    ]),
    ('Groin', [
      'Inguinal nodes along the ligament and down the long saphenous vein || || ',
    ]),
    ('Finish and complete', [
      '!Complete: examine the drainage areas, the liver and spleen; FBC, blood film, biopsy if persistent or suspicious || To complete, I would examine the abdomen for the liver and spleen. || ',
    ]),
  ],
  cases=[
    ('Reactive nodes', 'Soft, tender, mobile jaw nodes with tonsillitis.', '... **reactive cervical lymphadenopathy**: treat the cause and review.'),
    ('Glandular fever', 'Tender posterior cervical nodes, exudative tonsils and an enlarged spleen.', '... **infectious mononucleosis**: monospot, avoid contact sport for 4 weeks.'),
    ('Lymphoma', 'Painless rubbery nodes in several areas, night sweats, weight loss.', '... **concerning for lymphoma**: FBC, film, LDH, urgent biopsy.'),
    ('Metastatic node', 'Hard, fixed, painless node in the neck of a smoker with a hoarse voice.', '... a **probable metastatic node**: urgent ENT referral.'),
    ('Virchow\'s node', 'Hard left supraclavicular node with weight loss and indigestion.', '... **Troisier\'s sign**: urgent upper GI endoscopy for gastric cancer.'),
  ])

station('E-anteye', 'ex', 'Anterior eye examination', 'Speciality', ffp='Anterior Eye', u=[154, 156, 157, 158, 160, 159],
  door=DOOR.format(who='A 35-year-old contact lens wearer has a painful red right eye.', task='Examine the front of the eye.'),
  hooks=[
    '**Acuity first, every time.**',
    '**Front to back:** lids and lashes → conjunctiva → sclera → cornea → anterior chamber → iris → pupil.',
    '**Red-eye red flags:** reduced vision, real pain, light sensitivity, redness ringing the cornea, a strange pupil, contact lens use → same-day eye casualty.',
    '**Dendritic ulcer staining green with fluorescein = herpes. Never give steroid drops.**',
    '**Sticky, gritty, both eyes, vision fine = conjunctivitis.**',
  ],
  money='On examination of this gentleman\'s right eye, visual acuity was 6/18, improving to 6/12 with pinhole. There was redness ringing the cornea. With fluorescein and a blue light, there was a branching, staining ulcer on the cornea. The pupil was normal. These findings are consistent with **herpes simplex keratitis**. I would refer him **to eye casualty the same day** and avoid steroid drops.',
  traps=['Not checking acuity first', 'Not using fluorescein', 'Forgetting to evert the upper lid for a foreign body', 'Not checking the pupils'],
  dg=['redeye'],
  secs=[
    ('Acuity first', [
      '!Visual acuity in each eye with glasses or contact lenses as worn; pinhole || Cover your left eye and read the lowest line you can. || ',
    ]),
    ('Look, front to back', [
      'Lids and lashes: swelling, crusting, inturned lashes, stye, droop || || ',
      '!Conjunctiva and sclera: pull the lower lid down; pattern of redness, discharge || Look up for me. || Redness concentrated around the cornea = a deeper problem.',
      '!Cornea: clarity; fluorescein with a blue light for ulcers or abrasions || I\'m going to put in a drop of orange dye; it might sting briefly. || ',
      'Anterior chamber: depth, pus level, blood level || || ',
      '!Pupils: shape, size, direct and consensual responses || || Small irregular pupil = anterior uveitis; fixed mid-dilated = acute angle closure.',
      'Evert the upper lid if a foreign body is suspected || || ',
    ]),
    ('Finish and complete', [
      '!Complete: eye movements, fundoscopy, intraocular pressure, slit lamp; same-day referral for any red flag || || ',
    ]),
  ],
  cases=[
    ('Bacterial conjunctivitis', 'Both eyes red and sticky, normal acuity and pupils.', '... **bacterial conjunctivitis**: clean the lids; chloramphenicol drops if it doesn\'t settle.'),
    ('Acute angle-closure glaucoma', 'Very painful red eye, haloes, hazy cornea, fixed mid-dilated pupil, vomiting.', '... **acute angle-closure glaucoma**: emergency eye referral; lie flat, acetazolamide and pilocarpine.'),
    ('Anterior uveitis', 'Painful red eye with light sensitivity, redness around the cornea, small irregular pupil; ankylosing spondylitis.', '... **anterior uveitis**: same-day eye clinic for steroid drops.'),
    ('Herpes keratitis', 'Branching ulcer staining green with fluorescein.', '... **HSV keratitis**: same-day eye casualty; antiviral; no steroid.'),
    ('Subconjunctival haemorrhage', 'Painless bright red patch on the white of the eye, normal vision.', '... a **subconjunctival haemorrhage**: reassure, check blood pressure and INR if on warfarin.'),
  ])

station('E-eye', 'ex', 'Full eye examination: acuity and visual fields', 'Speciality', ffp='Full Eye Exam (VA + Fields)', u=[166, 160, 163, 165],
  door=DOOR.format(who='A 60-year-old man keeps bumping into door frames on his left.', task='Check his visual acuity and visual fields.'),
  hooks=[
    '**Acuity is a fraction:** distance from the chart over the line read. 6/6 normal; 6/60 = top letter only.',
    '**Pinhole fixes it = glasses problem. Pinhole doesn\'t fix it = eye disease.**',
    '**Fields like a mirror:** they cover their left eye, you close your right eye. You are the control.',
    '**Where the field loss is tells you where the lesion is:** one eye = optic nerve; both outer halves = chiasm; same side of both eyes = behind the chiasm.',
    '**Pie in the sky = temporal lobe. Pie on the floor = parietal lobe.**',
  ],
  money='On examination, visual acuity was 6/6 in both eyes. On confrontation, there was loss of the left half of the visual field in both eyes, a **left homonymous hemianopia**. The pupils were normal. This suggests a lesion behind the optic chiasm on the **right side**, most commonly a **posterior cerebral artery stroke**. I would like urgent **CT head**, fundoscopy and formal perimetry.',
  traps=['Testing fields with both eyes open', 'Sitting too close or not at eye level', 'Not using pinhole when acuity is reduced', 'Forgetting the central field and blind spot with a red pin'],
  dg=['fields', 'snellen'],
  secs=[
    ('Visual acuity', [
      '!Snellen at 6 metres, with distance glasses, one eye covered || Read the lowest line you can, with your left eye covered. || ',
      '!Record as 6 over the line number; add pinhole if worse than 6/9 || Now look through this little hole. || ',
      'If they can\'t read the top letter: count fingers, hand movements, light perception || || ',
      'Near vision with a reading chart || || ',
    ]),
    ('Visual fields', [
      '!Sit 1 metre opposite at the same eye level; patient covers their left eye, you close your right || Cover your left eye with your hand, and keep looking at my nose. || ',
      '!Bring a wiggling finger in from beyond the edge in each of the 4 quadrants, halfway between you || Say now as soon as you see my finger move. || ',
      'Central field and blind spot with a red hatpin; visual inattention with both hands || || ',
      'Repeat for the other eye || || ',
    ]),
    ('Finish and complete', [
      '!Complete: pupils, eye movements, fundoscopy, colour vision, formal perimetry || || ',
    ]),
  ],
  cases=[
    ('Bitemporal hemianopia', 'Both outer halves missing.', '... a **chiasmal lesion**, most often a pituitary adenoma: MRI and pituitary bloods.'),
    ('Homonymous hemianopia', 'Left half missing in both eyes.', '... a **right post-chiasmal lesion**, often a stroke: CT head.'),
    ('Superior quadrantanopia', 'Upper left quarter missing in both eyes.', '... a **right temporal lobe lesion**: pie in the sky.'),
    ('Central scotoma', 'Reduced acuity, a central blind area and red desaturation in one eye.', '... **optic neuritis** or macular disease.'),
    ('Tunnel vision', 'Constricted fields in both eyes with cupped discs.', '... consistent with **chronic open-angle glaucoma**.'),
    ('Refractive error', 'Acuity 6/24, improves to 6/6 with pinhole.', '... a **refractive error**: an optician for glasses.'),
  ])

station('E-fundo', 'ex', 'Fundoscopy', 'Speciality', ffp='Fundoscopy', u=[166, 71, 4, 90, 163, 165],
  door=DOOR.format(who='A 62-year-old man with type 2 diabetes and high blood pressure attends for review.', task='Perform fundoscopy on the model.'),
  hooks=[
    '**Right eye, right hand, your right eye.** Swap for the left.',
    '**Red reflex from arm\'s length first,** then come in 15 degrees from the side to land on the disc.',
    '**Disc → vessels in all 4 directions → macula last,** because looking at the light dazzles them.',
    '**Diabetic: dots, blots and hard exudates; then cotton wool spots; then new vessels = proliferative, needs laser.**',
    '**Blurred disc margins = papilloedema = raised pressure in the head.**',
    '**Artery blocked = pale retina with a cherry-red spot. Vein blocked = haemorrhages everywhere.**',
  ],
  money='On fundoscopy of the right eye, the red reflex was present. The disc was pink with clear margins and a cup-to-disc ratio of 0.3. There were scattered dot and blot haemorrhages with hard exudates, but no new vessels and no exudates near the macula. These findings are consistent with **background diabetic retinopathy**. I would continue **annual retinal screening** and optimise his glucose, blood pressure and lipids.',
  traps=['Using the wrong eye or hand', 'Not checking the red reflex first', 'Looking at the macula first and dazzling the patient', 'Forgetting to mention dilating drops and driving'],
  dg=['fundus'],
  secs=[
    ('Prepare', [
      '!Dim the room; say you would dilate with tropicamide after checking for angle-closure risk, and that they can\'t drive for some hours || I would use dilating drops, which blur your vision for a few hours, so no driving. || ',
      'Patient fixes on a distant point over your shoulder || Keep looking at that spot on the wall, even if I get in the way. || ',
    ]),
    ('Look', [
      '!Right eye: your right hand and right eye; red reflex from about 50 cm || || No red reflex = cataract; a white reflex in a child = retinoblastoma.',
      '!Come in 15 degrees from the side to find the disc; focus with the dial || || ',
      '!Disc: colour, margins, cup-to-disc ratio || || Pale = optic atrophy; big cup = glaucoma; blurred = papilloedema.',
      '!Vessels in all 4 directions: AV nipping, haemorrhages, exudates, cotton wool spots, new vessels || || ',
      'Macula last: ask them to look into the light briefly || Look straight at the light for one second. || ',
      'Repeat for the left eye with your left hand and left eye || || ',
    ]),
    ('Finish and complete', [
      '!Complete: acuity, fields, pupils; retinal photographs; refer as needed || || ',
    ]),
  ],
  cases=[
    ('Background diabetic retinopathy', 'Dot and blot haemorrhages and hard exudates; no new vessels.', '... **background diabetic retinopathy**: annual screening, control risk factors.'),
    ('Proliferative diabetic retinopathy', 'New fragile vessels on the disc with cotton wool spots.', '... **proliferative diabetic retinopathy**: urgent ophthalmology for laser.'),
    ('Hypertensive retinopathy', 'AV nipping, silver wiring, flame haemorrhages; swollen disc in severe cases.', '... **hypertensive retinopathy**; with disc swelling it is malignant hypertension: admit.'),
    ('Papilloedema', 'Blurred, swollen disc margins in both eyes, no venous pulsation.', '... **papilloedema**: urgent CT head for raised intracranial pressure.'),
    ('Central retinal artery occlusion', 'Pale white retina with a cherry-red spot; sudden painless loss of vision.', '... **CRAO**: emergency eye referral; check ESR and CRP for giant cell arteritis.'),
    ('Central retinal vein occlusion', 'Haemorrhages in all four quadrants and swollen veins.', '... **CRVO**: eye referral; check blood pressure, glucose and lipids.'),
  ])
