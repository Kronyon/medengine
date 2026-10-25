from .common import station

DOOR = 'You are an FY1. {who} Examine their {sys}, then present your findings to the examiner. You have 10 minutes: aim to finish examining by 7 and present in the last 2 to 3.'

station('E-cvs', 'ex', 'Cardiovascular examination', 'Medicine', ffp='Cardiovascular', u=[7, 6, 8, 3],
  door=DOOR.format(who='A 68-year-old man has been referred by his GP with a murmur.', sys='cardiovascular system'),
  hooks=[
    '**Outside in:** end of the bed → hands → pulse → face → neck → chest → back → legs. The examiner can follow a story.',
    '**All Physicians Take Money:** Aortic 2nd right space, Pulmonary 2nd left, Tricuspid 4th left at the sternal edge, Mitral 5th space in the midclavicular line.',
    '**Time every murmur on the carotid:** murmur with the pulse = systolic; murmur between pulses = diastolic.',
    '**The two hunting positions:** left side + breath out + bell at the apex finds **mitral stenosis**; sit forward + breath out + left sternal edge finds **aortic regurgitation**.',
    '**AS goes up to the neck, MR goes out to the armpit.**',
  ],
  money='On examination of this gentleman\'s cardiovascular system, he was comfortable at rest. His pulse was 72 and regular and slow-rising, with a narrow pulse pressure: blood pressure 115 over 90. The apex was undisplaced. There was a harsh ejection systolic murmur loudest in the aortic area radiating to the carotids, with a soft second heart sound. There were no signs of heart failure. These findings are consistent with **aortic stenosis**. To complete my examination, I would like an **ECG, an echocardiogram**, a urine dip and fundoscopy.',
  traps=['Pressing both carotids at once', 'Listening without timing the murmur against the carotid', 'Forgetting the two manoeuvres for the quiet diastolic murmurs', 'Not saying how you would complete the examination'],
  dg=['ausc', 'murmurs'],
  secs=[
    ('From the end of the bed', [
      '!Position at 45 degrees and expose the chest; offer a chaperone || Could you sit back at about 45 degrees and take your top off down to the waist? Would you like someone else in the room? || 45 degrees is the angle for the JVP, so set it before anything else.',
      'Look and say out loud: breathless, pale, cyanosed, malar flush || Standing at the end of the bed, he is comfortable at rest with no obvious breathlessness or cyanosis. || The examiner can only mark what you say, so narrate what you see.',
      'Scars and clues: midline sternotomy, left thoracotomy, pacemaker box under the left collarbone, leg vein harvest scar, GTN spray, oxygen || I can see no scars, and no medication or oxygen around the bed. || A sternotomy means bypass or a valve; a leg scar means vein harvested for a bypass.',
    ]),
    ('Hands', [
      'Temperature and capillary refill, under 2 seconds || Your hands are nice and warm. || Cold peripheries suggest poor output.',
      'Clubbing, splinter haemorrhages, Janeway lesions, Osler nodes || I\'m looking at your nails and fingertips. || Endocarditis signs. Osler = **Ouch**: painful pulp nodes; Janeway = painless palm spots.',
      'Tendon xanthomata and nicotine staining || || Xanthomata point to familial hypercholesterolaemia.',
    ]),
    ('Pulses and blood pressure', [
      '!Radial pulse: rate and rhythm for 30 seconds || I\'m just going to feel your pulse. || An irregular rhythm changes the whole presentation, so find it early.',
      'Radio-radial delay, and say radio-femoral delay || I would also check for radio-femoral delay. || Radio-femoral delay = coarctation of the aorta.',
      'Collapsing pulse: ask about shoulder pain first, then lift the arm with your palm across the wrist || Do you have any pain in your shoulders? I\'m going to lift your arm up quickly. || In aortic regurgitation the pulse slaps your palm and falls away.',
      'Blood pressure, offered in both arms || I would like to measure your blood pressure in both arms. || A difference over 20 suggests dissection; a narrow pulse pressure fits aortic stenosis.',
    ]),
    ('Face and neck', [
      'Eyes: conjunctival pallor, corneal arcus, xanthelasma || Could you look up for me while I gently pull down your lower eyelid? || Pallor = anaemia; xanthelasma = high cholesterol.',
      'Mouth: central cyanosis under the tongue, teeth, high-arched palate || Could you open your mouth and lift your tongue? || Bad teeth seed endocarditis; a high-arched palate hints at Marfan syndrome.',
      '!JVP: head turned slightly left, look between the two heads of sternocleidomastoid, height above the sternal angle; hepatojugular reflux || I\'m going to press on your tummy for a moment. Tell me if it\'s sore. || Over 3 cm = raised: fluid overload or right heart failure. The JVP has two waves, cannot be felt and rises when you press the liver.',
      '!Carotid pulse character, one side only || I\'m going to feel the pulse in your neck. || Never both together: you can drop the blood pressure. Slow-rising = aortic stenosis.',
    ]),
    ('Praecordium', [
      'Inspect: scars, pacemaker, visible pulsation || || ',
      '!Apex beat: 5th space, midclavicular line; is it displaced, heaving or tapping? || I\'m going to feel for your heartbeat here. || Displaced = dilated left ventricle; heaving = pressure overload; tapping = mitral stenosis.',
      'Heaves at the left sternal edge and thrills over each valve area || || A heave = right ventricular hypertrophy; a thrill is a murmur loud enough to feel.',
      '!Listen in all 4 areas with the diaphragm while feeling the carotid, then the bell at the apex || I\'m going to listen to your heart now. || Timing against the carotid tells you systolic or diastolic in one move.',
      '!Two manoeuvres: left side with breath held out for mitral stenosis; sitting forward with breath out at the left sternal edge for aortic regurgitation || Could you roll onto your left side, breathe all the way out and hold it for me? || These catch the quiet diastolic murmurs that examiners love.',
      'Listen for radiation: carotids for AS, axilla for MR || || Where it travels tells you which valve.',
    ]),
    ('Back and legs', [
      'Lung bases for crackles and sacral oedema || Could you sit forward for me? Deep breaths in and out through your mouth. || Crackles = left heart failure; sacral oedema = fluid when in bed.',
      'Ankle oedema: press for 15 seconds and find the top level; leg vein harvest scar || I\'m going to press on your ankles; tell me if it hurts. || How far up it pits shows how much fluid.',
      'Say you would feel the peripheral pulses || I would also like to feel the pulses in your feet. || ',
    ]),
    ('Finish and complete', [
      'Thank, cover, wash hands || Thank you, that\'s all. Let me help you get dressed. || ',
      '!Complete the examination: ECG, echocardiogram, observations including temperature, urine dip, fundoscopy || To complete my examination, I would like to do an ECG, an echocardiogram, a urine dip and fundoscopy. || Completion is a marked line in every exam station.',
    ]),
  ],
  cases=[
    ('Aortic stenosis', 'Slow-rising pulse, narrow pulse pressure, undisplaced heaving apex, harsh ejection systolic murmur loudest at the right second space radiating to both carotids, soft second heart sound.', 'These findings are consistent with **aortic stenosis**. I would like an ECG and echo. If severe and symptomatic, the treatment is valve replacement: surgical or TAVI.'),
    ('Mitral regurgitation', 'Displaced apex, pansystolic murmur loudest at the apex radiating to the axilla, irregularly irregular pulse.', '... a pansystolic murmur at the apex radiating to the axilla, consistent with **mitral regurgitation**, with atrial fibrillation.'),
    ('Aortic regurgitation', 'Collapsing pulse, wide pulse pressure, displaced apex, early diastolic murmur at the left sternal edge heard best sitting forward in expiration.', '... consistent with **aortic regurgitation**. I would look for causes: endocarditis, Marfan syndrome, ankylosing spondylitis.'),
    ('Mitral stenosis', 'Malar flush, irregularly irregular pulse, tapping undisplaced apex, loud first heart sound, low rumbling mid-diastolic murmur at the apex in the left lateral position.', '... consistent with **mitral stenosis** with atrial fibrillation. He will need anticoagulation and an echo.'),
    ('Metallic valve', 'Midline sternotomy scar, a crisp metallic click audible without a stethoscope.', '... consistent with a **metallic valve replacement**. He will be on lifelong warfarin; I would check his INR and look for signs of endocarditis or valve failure.'),
    ('Heart failure', 'Raised JVP at 6 cm, displaced apex, third heart sound, fine crackles at both bases, pitting oedema to the knees.', '... signs of **congestive cardiac failure**. I would like an ECG, chest X-ray, BNP and echocardiogram.'),
  ])

station('E-resp', 'ex', 'Respiratory examination', 'Medicine', ffp='Respiratory', u=[16, 9, 11, 19, 23, 17, 21],
  door=DOOR.format(who='A 72-year-old woman has been increasingly breathless over the last few weeks.', sys='respiratory system'),
  hooks=[
    '**Front, then back, the same 4 moves:** expansion → percussion → breath sounds → vocal resonance.',
    '**Which side?** The trachea and expansion tell you. **What is it?** Percussion and breath sounds tell you.',
    '**Dull + bronchial breathing = consolidation. Stony dull + nothing to hear = effusion. Hyper-resonant + nothing to hear = pneumothorax.**',
    '**The trachea gets pulled toward collapse; pushed away by a tension pneumothorax or a big effusion.**',
    'Count the breathing rate while you pretend to take the pulse, so they don\'t change it.',
  ],
  money='On examination of this lady\'s respiratory system, she was breathless at rest with a respiratory rate of 24 and oxygen saturations of 92% on air. There was no clubbing. The trachea was central. Expansion was reduced on the left. Percussion was stony dull at the left base with absent breath sounds and reduced vocal resonance. These findings are consistent with a **left pleural effusion**. To complete my examination I would like a **chest X-ray**, observations, and a pleural tap for analysis if it is confirmed.',
  traps=['Telling the patient you are counting their breathing', 'Percussing only one side instead of comparing side to side', 'Forgetting the axillae and the apices', 'Missing the cervical and supraclavicular nodes'],
  dg=['lungs', 'lungsigns'],
  secs=[
    ('From the end of the bed', [
      '!Sit the patient at 45 degrees with the chest exposed; offer a chaperone || Could you sit back for me and take your top off? Would you like a chaperone? || ',
      'Say what you see: breathless at rest, accessory muscles, pursed lips, cyanosis, wasting || She is breathless at rest, using her accessory muscles. || Pursed lips = COPD; wasting = cancer or end-stage disease.',
      'Around the bed: inhalers, oxygen and the flow, sputum pot, nebuliser || I can see an inhaler and oxygen at 2 litres. || These are free clues: an examiner has put them there.',
      'Chest shape and scars: barrel chest, pectus, thoracotomy scar, radiotherapy marks || || A scar may mean a lobectomy: the side will be quiet and the trachea pulled.',
    ]),
    ('Hands and pulse', [
      '!Clubbing, tar staining, peripheral cyanosis || Can I look at your hands? || Clubbing = cancer, fibrosis or bronchiectasis; COPD alone does not cause clubbing.',
      'Fine tremor; CO2 retention flap with the arms out and wrists cocked back for 30 seconds || Hold your arms out and push your hands back like you\'re stopping traffic. || Tremor = salbutamol; a flap = carbon dioxide retention.',
      '!Pulse and respiratory rate, counted without telling them || || The respiratory rate is the vital sign most often guessed. Count it.',
    ]),
    ('Face and neck', [
      'Eyes: pallor, Horner\'s syndrome; mouth: central cyanosis || || Horner\'s on one side = an apical tumour pressing on the sympathetic chain.',
      'JVP || || Raised in cor pulmonale.',
      '!Trachea: warn first, then check it is central; cricosternal distance || This might feel a bit uncomfortable. || Shifted trachea gives you the side and the type of problem.',
      'Lymph nodes from behind: cervical and supraclavicular || I\'m going to feel the glands in your neck from behind. || Hard nodes may be lung cancer spread.',
    ]),
    ('Front of the chest', [
      '!Expansion: hands on the lower ribs, thumbs meeting; big breath in || Take a big breath in for me. || The side that moves less is the side of the problem.',
      '!Percussion: compare side to side, top to bottom, including the collarbones and axillae || I\'m going to tap on your chest. || Comparing left with right is the whole point of percussion.',
      '!Breath sounds with the diaphragm, comparing sides, including the axillae || Breathe in and out through your mouth. || Bronchial breathing, crackles and wheeze each point to a diagnosis.',
      'Vocal resonance: say ninety-nine || Each time I put the stethoscope on, say ninety-nine. || Louder over consolidation; quieter over fluid or air.',
    ]),
    ('Back of the chest', [
      '!Repeat at the back: expansion, percussion, breath sounds, vocal resonance || Could you lean forward and cross your arms? || Crossing the arms moves the scapulae out of the way.',
      'Sacral and ankle oedema || || Cor pulmonale from chronic lung disease.',
    ]),
    ('Finish and complete', [
      'Thank, cover, wash hands || || ',
      '!Complete: oxygen saturations, peak flow, sputum sample, chest X-ray, ABG if unwell || To complete my examination I would like observations, a peak flow, a sputum sample and a chest X-ray. || ',
    ]),
  ],
  cases=[
    ('Consolidation', 'Reduced expansion right base, dull to percussion, bronchial breathing, coarse crackles, increased vocal resonance, fever.', '... consistent with **right lower lobe consolidation**, most likely a community-acquired pneumonia. I would calculate CURB-65 and request a chest X-ray.'),
    ('Pleural effusion', 'Reduced expansion left, stony dull left base, absent breath sounds, reduced vocal resonance.', '... consistent with a **left pleural effusion**: chest X-ray, then pleural tap for protein, LDH, pH, microscopy and cytology.'),
    ('Pneumothorax', 'Reduced expansion right, hyper-resonant percussion, absent breath sounds, trachea central.', '... consistent with a **right pneumothorax**. If the trachea were deviated away with low blood pressure, I would treat it as tension: needle decompression.'),
    ('COPD', 'Pursed lips, barrel chest, reduced cricosternal distance, hyper-resonant chest, widespread wheeze, prolonged expiration, tar staining.', '... consistent with **COPD**. I would like spirometry and a chest X-ray.'),
    ('Pulmonary fibrosis', 'Clubbing, reduced expansion bilaterally, fine end-inspiratory crackles at both bases like Velcro.', '... consistent with **pulmonary fibrosis**. I would like a high-resolution CT and lung function tests.'),
    ('Lobectomy', 'Right thoracotomy scar, trachea pulled to the right, reduced expansion and dull percussion at the right upper zone.', '... consistent with a previous **right upper lobectomy**, most likely for lung cancer.'),
  ])

station('E-cn', 'ex', 'Cranial nerve examination', 'Medicine', ffp='Cranial nerve', u=[141, 89, 90, 99, 166],
  door=DOOR.format(who='A 54-year-old woman noticed her face looked different this morning.', sys='cranial nerves'),
  hooks=[
    '**Walk the head from top to bottom:** I smell, II see, III IV VI move the eyes, V feel and chew, VII face, VIII hear, IX X say ahh, XI shrug, XII tongue.',
    '**LR6 SO4, the rest are 3:** lateral rectus = VI, superior oblique = IV.',
    '**Forehead spared = stroke. Forehead weak too = Bell\'s.** The forehead has a backup supply from both hemispheres.',
    '**The tongue points TO the lesion; the uvula points AWAY.**',
    '**Third nerve palsy = down and out with a droopy lid.** A blown pupil too = compression: aneurysm until proven otherwise.',
  ],
  money='On examination of this lady\'s cranial nerves, there was weakness of the whole right side of the face, including the forehead, with inability to close the right eye. The other cranial nerves were intact. These findings are consistent with a **right lower motor neurone facial nerve palsy**, most likely **Bell\'s palsy**. I would examine the ears for vesicles, and start **prednisolone within 72 hours** with eye protection.',
  traps=['Forgetting to ask about smell and taste', 'Testing visual fields with both eyes open', 'Pushing the jaw sideways instead of testing opening against resistance', 'Not saying whether the forehead is involved'],
  dg=['cn12', 'eyeH', 'fields', 'face7'],
  secs=[
    ('Set up', [
      '!Sit level with the patient, 1 metre away; ask about any changes in smell, vision, hearing or swallowing || Have you noticed any changes in your sense of smell or taste, your vision, hearing or swallowing? || Asking covers I and VIII quickly and shows you are thinking.',
    ]),
    ('II: the eyes', [
      '!Visual acuity each eye with glasses, Snellen chart || Cover your left eye and read the lowest line you can. || Acuity always comes first in any eye exam.',
      '!Pupils: size and shape, direct and consensual light, swinging torch, accommodation || Look at the far wall for me. Now look at my finger. || A relative afferent pupillary defect = optic nerve damage.',
      '!Visual fields by confrontation, one eye at a time || Cover your right eye, and look at my nose. Tell me when you see my finger wiggle. || The field pattern points to where the lesion is.',
      'Offer fundoscopy || I would like to look at the back of the eyes. || Papilloedema means raised pressure in the head.',
    ]),
    ('III, IV, VI: eye movements', [
      '!H pattern with the head still; ask about double vision; look for nystagmus || Keep your head still and follow my finger with your eyes. Tell me if you see double. || Double vision in one direction tells you which muscle is weak.',
    ]),
    ('V: trigeminal', [
      'Light touch on forehead, cheek and jaw, both sides || Close your eyes and say yes when you feel me touch. Does it feel the same on both sides? || V1, V2, V3 each have their own patch.',
      'Clench the teeth while you feel masseter and temporalis; open the mouth against your hand || Clench your teeth. Now open your mouth and don\'t let me close it. || The jaw deviates toward the weak side.',
      'Say: corneal reflex and jaw jerk || I would test the corneal reflex and the jaw jerk. || A brisk jaw jerk = upper motor neurone lesion above the pons.',
    ]),
    ('VII: facial', [
      '!Raise the eyebrows, screw the eyes shut, puff the cheeks, show the teeth || Raise your eyebrows. Screw your eyes shut and don\'t let me open them. Blow out your cheeks. Show me your teeth. || The forehead decides stroke versus Bell\'s.',
      'Ask about taste and sound sensitivity || Has food tasted different, or have sounds seemed louder? || ',
    ]),
    ('VIII: hearing', [
      'Whisper test in each ear while rubbing the other tragus; offer Rinne and Weber || I\'m going to whisper a number; tell me what you hear. || ',
    ]),
    ('IX, X, XI, XII', [
      'Say ahh: watch the uvula; cough; sip of water || Open your mouth and say ahh. || The uvula moves away from the weak side.',
      'Shrug the shoulders and turn the head against resistance || Shrug your shoulders and don\'t let me push them down. || XI: trapezius and sternocleidomastoid.',
      '!Tongue: wasting and fasciculations at rest, then stick it out and push into each cheek || Leave your tongue relaxed in your mouth. Now stick it out. || Fasciculations = lower motor neurone, such as motor neurone disease.',
    ]),
    ('Finish and complete', [
      '!Complete: full neurological examination of the limbs, fundoscopy, and imaging if a central cause is suspected || To complete my examination I would examine the limbs and the fundi. || ',
    ]),
  ],
  cases=[
    ('Bell\'s palsy', 'Whole right side of the face weak including the forehead, cannot close the right eye; nothing else abnormal.', '... a **lower motor neurone** right facial palsy, most likely Bell\'s palsy: prednisolone within 72 hours, eye protection, check the ears for vesicles.'),
    ('Stroke', 'Left lower face weak but the forehead moves normally; left homonymous hemianopia.', '... an **upper motor neurone** facial weakness with a field defect, consistent with a **right hemisphere stroke**: urgent CT head and the stroke pathway.'),
    ('Third nerve palsy', 'Right eye down and out, complete ptosis, fixed dilated pupil.', '... a **right third nerve palsy with pupil involvement**: a compressive cause such as a posterior communicating artery aneurysm must be excluded urgently with CT angiography.'),
    ('Sixth nerve palsy', 'Cannot move the left eye outward; double vision worse looking left.', '... a **left sixth nerve palsy**. It can be a false localising sign of raised intracranial pressure, so I would look for papilloedema.'),
    ('Bitemporal hemianopia', 'Both outer halves of the visual fields missing.', '... a **bitemporal hemianopia**, a lesion at the optic chiasm, most often a pituitary adenoma: MRI pituitary and pituitary bloods.'),
  ])

station('E-ul', 'ex', 'PNS: upper limb neurological examination', 'Medicine', ffp='PNS', u=[99, 97, 98],
  door=DOOR.format(who='A 45-year-old man has tingling and weakness in his right hand.', sys='upper limbs neurologically'),
  hooks=[
    '**Look, Tone, Power, Reflexes, Coordination, Sensation:** the same order every time, so you never skip one.',
    '**Reflex roots, count up:** 5, 6 pick up sticks = biceps and supinator; 7, 8 lay them straight = triceps.',
    '**Upper motor neurone goes UP:** tone up, reflexes up. **Lower motor neurone goes DOWN:** tone down, reflexes down, wasting and twitching.',
    '**Pronator drift:** arms out, palms up, eyes closed: the weak arm sinks and turns over = upper motor neurone.',
    '**Power out of 5:** 0 nothing, 1 flicker, 2 moves with gravity removed, 3 against gravity, 4 against some resistance, 5 normal.',
  ],
  money='On examination of this gentleman\'s upper limbs, there was no wasting or fasciculation. Tone was normal. There was weakness of elbow flexion and wrist extension on the right, graded 4 out of 5. The right biceps and supinator reflexes were reduced. There was reduced sensation over the right thumb and lateral forearm. These findings are consistent with a **right C6 radiculopathy**. I would like to examine the neck and arrange an **MRI of the cervical spine**.',
  traps=['Not checking for pain before moving the arm', 'Testing power without fixing the joint above', 'Forgetting reinforcement when a reflex seems absent', 'Testing sensation without a reference point on the sternum'],
  dg=['dermUL', 'reflex', 'umnlmn'],
  secs=[
    ('Look', [
      '!Expose both arms; ask about pain || Is there any pain anywhere before I start? || ',
      'Wasting, fasciculations, tremor, scars, posture || || Wasting of the small hand muscles points to the lower motor neurone or T1.',
      'Pronator drift: arms out, palms up, eyes closed for 20 seconds || Hold your arms out with your palms up, and close your eyes. || ',
    ]),
    ('Tone', [
      'Rotate the wrist and bend the elbow, both sides || Let your arm go floppy; let me do all the work. || Increased tone = upper motor neurone; cogwheel = Parkinson\'s.',
    ]),
    ('Power: fix above, test the movement', [
      '!Shoulder abduction C5, elbow flexion C5 and C6, elbow extension C7 || Arms up like a chicken; don\'t let me push down. Pull me towards you. Push me away. || Each movement maps to a root, so a pattern of weakness names the root.',
      '!Wrist extension C6, finger extension C7, finger flexion C8, finger abduction T1, thumb abduction T1 || Cock your wrist back. Squeeze my fingers. Spread your fingers apart. Point your thumb to the ceiling. || ',
    ]),
    ('Reflexes', [
      '!Biceps C5 and C6, supinator C6, triceps C7, compare sides; reinforce if absent || Clench your teeth for me. || Reinforcement stops you calling a normal reflex absent.',
    ]),
    ('Coordination', [
      'Finger to nose, quickly; rapid alternating movements || Touch my finger, then your nose, as fast as you can. || Overshoot and clumsy alternating movements = cerebellar.',
    ]),
    ('Sensation', [
      '!Light touch and pinprick in each dermatome, starting with a reference on the sternum: C5 shoulder badge, C6 thumb, C7 middle finger, C8 little finger, T1 inner forearm || Close your eyes. Does this feel the same as on your chest? || ',
      'Proprioception at the thumb tip; vibration with a 128 Hz fork on the finger joint || Is your thumb pointing up or down? || ',
    ]),
    ('Finish and complete', [
      '!Complete: lower limb neurological examination, cervical spine, and imaging as indicated || To complete, I would examine the lower limbs and the neck. || ',
    ]),
  ],
  cases=[
    ('C6 radiculopathy', 'Weak elbow flexion and wrist extension, reduced biceps and supinator reflexes, numb thumb.', '... a **right C6 radiculopathy**: MRI cervical spine; urgent if there is myelopathy.'),
    ('Carpal tunnel syndrome', 'Thenar wasting, weak thumb abduction, numbness of the thumb, index, middle and half the ring finger; positive Tinel\'s and Phalen\'s.', '... **carpal tunnel syndrome**: nerve conduction studies, wrist splint at night, steroid injection, or surgical release.'),
    ('Ulnar nerve lesion', 'Wasting of the first dorsal interosseous, weak finger abduction, numb little finger and half the ring finger, positive Froment\'s sign.', '... an **ulnar nerve palsy**, often compressed at the elbow.'),
    ('Upper motor neurone weakness', 'Right pronator drift, increased tone, brisk reflexes, weak extensors more than flexors.', '... an **upper motor neurone** lesion, such as a left hemisphere stroke: CT head.'),
  ])

station('E-ll', 'ex', 'PNS: lower limb neurological examination', 'Medicine', ffp='PNS', u=[99, 90, 71, 97],
  door=DOOR.format(who='A 62-year-old man with prostate cancer has had weakness in both legs for 2 days.', sys='lower limbs neurologically'),
  hooks=[
    '**Look, Tone, Power, Reflexes, Coordination, Sensation, Gait.**',
    '**1, 2 buckle my shoe = ankle S1 and S2; 3, 4 kick the door = knee L3 and L4.**',
    '**L4 inside of the shin, L5 top of the foot and big toe, S1 outside of the foot and sole.**',
    '**Upstairs Babinski = upper motor neurone.** Big toe goes up.',
    '**Cancer + back pain + leg weakness = cord compression until proven otherwise:** MRI whole spine within 24 hours, dexamethasone.',
  ],
  money='On examination of this gentleman\'s lower limbs, tone was increased bilaterally with 4 beats of ankle clonus. There was weakness of hip flexion graded 3 out of 5 on both sides. Knee and ankle reflexes were brisk and plantars were upgoing. There was a sensory level at T10. These findings are consistent with **spinal cord compression**, which in a man with prostate cancer is most likely metastatic. This is an emergency: I would give **dexamethasone** and arrange a **whole-spine MRI** within 24 hours.',
  traps=['Forgetting to roll and lift the legs for tone', 'Not testing for ankle clonus', 'Missing the sensory level on the trunk', 'Forgetting gait and Romberg\'s'],
  dg=['dermLL', 'reflex', 'umnlmn'],
  secs=[
    ('Look', [
      '!Expose the legs, keep the groin covered, ask about pain || || ',
      'Wasting, fasciculation, scars, deformity, footwear || || ',
    ]),
    ('Tone', [
      '!Roll the legs; lift the knee quickly; test for ankle clonus || Let your legs go floppy. || The heel should stay on the bed. More than 3 beats of clonus = upper motor neurone.',
    ]),
    ('Power', [
      '!Hip flexion L1 L2, hip extension L5 S1, knee extension L3 L4, knee flexion L5 S1 || Lift your leg up and don\'t let me push it down. Push down into the bed. Kick me away. Pull your heel to your bottom. || ',
      '!Ankle dorsiflexion L4, plantarflexion S1, big toe extension L5 || Point your toes to the ceiling. Push down like on a pedal. Lift your big toe. || Weak big toe extension = L5, the classic foot drop root.',
    ]),
    ('Reflexes', [
      '!Knee L3 L4, ankle S1 S2, plantar response || Relax your leg on my arm. || ',
    ]),
    ('Coordination', [
      'Heel down the shin, both sides || Run your heel down your shin and back up. || ',
    ]),
    ('Sensation', [
      '!Light touch and pinprick by dermatome from a sternum reference; look for a sensory level on the trunk || Tell me when it changes. || A sensory level on the trunk means the spinal cord.',
      'Proprioception at the big toe; vibration at the big toe joint || || Glove and stocking loss = peripheral neuropathy.',
    ]),
    ('Gait', [
      'Walk, heel-toe walking, Romberg\'s test || Stand with your feet together and close your eyes. I\'ll be right here. || Romberg\'s positive = sensory ataxia: proprioception is lost.',
    ]),
    ('Finish and complete', [
      '!Complete: upper limbs, back and saddle sensation, anal tone, bladder scan || To complete, I would check saddle sensation, anal tone and a bladder scan. || Cauda equina and cord compression are the emergencies.',
    ]),
  ],
  cases=[
    ('Cord compression', 'Bilateral increased tone, clonus, weakness, brisk reflexes, upgoing plantars, sensory level at T10.', '... **spinal cord compression**: dexamethasone, whole-spine MRI within 24 hours, oncology and spinal teams.'),
    ('Peripheral neuropathy', 'Absent ankle reflexes, reduced vibration and pinprick in a stocking distribution, positive Romberg\'s.', '... a **sensory peripheral neuropathy**: glucose, B12, alcohol history, thyroid.'),
    ('L5 radiculopathy', 'Weak big toe extension and dorsiflexion, numb top of the foot, normal reflexes.', '... a **left L5 radiculopathy**, often a disc prolapse.'),
    ('Cauda equina', 'Bilateral leg weakness, absent ankle reflexes, saddle numbness, reduced anal tone, painless retention.', '... **cauda equina syndrome**: an emergency MRI and neurosurgical referral.'),
  ])

station('E-abdo', 'ex', 'Abdominal examination', 'Medicine', ffp='Abdominal', u=[25, 41, 49, 44, 33],
  door=DOOR.format(who='A 58-year-old man with a history of heavy drinking has a swollen tummy.', sys='abdomen'),
  hooks=[
    '**Hands → face → neck → lie flat:** arms by the sides, head on one pillow.',
    '**Kneel and watch the face** while you palpate. A wince scores more than a guess.',
    '**Liver and spleen start low in the right iliac fossa** and move up with each breath, so you never miss a huge organ.',
    '**Spleen vs kidney:** spleen moves with breathing, has a notch, you can\'t get above it; kidney you can ballot and get above.',
    '**Shifting dullness:** percuss to dull, keep your finger there, roll them toward you, wait 30 seconds, percuss again.',
  ],
  money='On examination of this gentleman\'s abdomen, he was jaundiced with multiple spider naevi, palmar erythema and gynaecomastia. The abdomen was distended with shifting dullness. The liver edge was not palpable and there was a spleen palpable 3 cm below the left costal margin. These findings suggest **chronic liver disease with portal hypertension and ascites**. To complete, I would examine the hernial orifices and external genitalia, perform a DRE, dip the urine, and request **LFTs, clotting, an ultrasound and a diagnostic ascitic tap**.',
  traps=['Not asking about pain before palpating', 'Palpating with the fingertips instead of the flat of the hand', 'Starting the liver at the costal margin', 'Forgetting to say hernial orifices, genitalia and DRE'],
  dg=['abdo9', 'organs'],
  secs=[
    ('From the end of the bed', [
      '!Lying flat, one pillow, arms by the sides; expose nipples to knees but keep the groin covered; chaperone || Could you lie flat with your arms by your side? || ',
      'Jaundice, cachexia, distension, scars, stoma, drains || || Know the scars: Kocher\'s = gallbladder; Lanz or McBurney\'s = appendix; midline laparotomy.',
    ]),
    ('Hands and arms', [
      'Clubbing, leuconychia, koilonychia, palmar erythema, Dupuytren\'s contracture || || White nails = low albumin; spoon nails = iron deficiency.',
      '!Liver flap: arms out, wrists cocked back for 30 seconds || || Asterixis = liver failure.',
      'Bruising, scratch marks, spider naevi on the arms and chest || || More than 5 spider naevi = chronic liver disease.',
    ]),
    ('Face, neck and chest', [
      'Sclera for jaundice, conjunctival pallor, mouth ulcers, angular stomatitis || || Mouth ulcers point to Crohn\'s.',
      '!Left supraclavicular node: Virchow\'s node || || A hard node here = Troisier\'s sign, gastric cancer.',
      'Gynaecomastia || || ',
    ]),
    ('Palpation', [
      '!Ask where it hurts, kneel at bed level, watch the face; light palpation in all 9 regions starting away from the pain || Is there any pain in your tummy? I\'ll start away from it, and please tell me if anything hurts. || ',
      'Deep palpation of all 9 regions || || ',
      '!Liver: from the right iliac fossa upward, rising with each breath in || Take deep breaths in and out for me. || ',
      'Gallbladder: Murphy\'s sign || || Pain stopping the breath in = acute cholecystitis.',
      '!Spleen: from the right iliac fossa diagonally to the left upper quadrant; kidneys by ballotting || || ',
      'Aorta: two hands above the umbilicus; expansile means your fingers move apart || || An expansile mass = aneurysm.',
    ]),
    ('Percussion and auscultation', [
      'Percuss the liver and spleen; shifting dullness if distended || I\'m going to roll you towards me and wait a moment. || ',
      'Bowel sounds, renal and aortic bruits || || Tinkling = obstruction; silence = ileus or peritonitis.',
    ]),
    ('Finish and complete', [
      '!Complete: hernial orifices, external genitalia, digital rectal examination, urine dip || To complete my examination, I would like to examine the hernial orifices and external genitalia, perform a rectal examination and dip the urine. || ',
    ]),
  ],
  cases=[
    ('Chronic liver disease with ascites', 'Jaundice, spider naevi, palmar erythema, gynaecomastia, flap, shifting dullness, splenomegaly.', '... **chronic liver disease with portal hypertension**: LFTs, clotting, ultrasound, ascitic tap.'),
    ('Hepatosplenomegaly', 'Smooth liver edge 4 cm below the costal margin, spleen 5 cm, lymph nodes in the neck.', '... **hepatosplenomegaly with lymphadenopathy**: think lymphoma or leukaemia; blood film and imaging.'),
    ('Abdominal aortic aneurysm', 'Pulsatile expansile mass above the umbilicus.', '... a probable **abdominal aortic aneurysm**: ultrasound to measure it; over 5.5 cm or symptomatic needs vascular repair.'),
    ('Renal transplant', 'Curved scar in the right iliac fossa with a smooth firm mass beneath; fistula in the left arm.', '... a **functioning renal transplant** with an arteriovenous fistula from previous dialysis.'),
    ('Ileostomy vs colostomy', 'Spouted stoma in the right iliac fossa with liquid output.', '... an **ileostomy**: spouted because small bowel output is irritant. A colostomy is flush, usually on the left, with formed stool.'),
  ])

station('E-thyroid', 'ex', 'Thyroid examination', 'Medicine', ffp='Thyroid', u=[72, 73, 74],
  door=DOOR.format(who='A 34-year-old woman has lost weight and feels anxious and hot all the time.', sys='thyroid status and neck'),
  hooks=[
    '**Look, swallow, tongue:** a goitre rises when they swallow; a thyroglossal cyst rises when they stick the tongue out.',
    '**Hyper = fast and hot:** sweaty, tremor, fast or irregular pulse, lid lag, brisk reflexes. **Hypo = slow and cold:** dry, slow pulse, slow-relaxing reflexes.',
    '**Only Graves\' gives the eyes and the shins:** bulging eyes, double vision, pretibial myxoedema.',
    'Feel the gland **from behind**, look at it **from the front**.',
  ],
  money='On examination, this lady was thin and anxious with warm sweaty hands, a fine tremor and a pulse of 110 and regular. She had lid retraction and lid lag with proptosis. There was a smooth, diffuse, non-tender goitre that moved on swallowing, with a bruit. These findings are consistent with **Graves\' disease**. I would like **TFTs and TSH receptor antibodies**, and refer to endocrinology and the eye clinic.',
  traps=['Not offering a glass of water to swallow', 'Forgetting to look from behind and above for proptosis', 'Missing the lymph nodes', 'Forgetting proximal myopathy and reflexes'],
  dg=['thyroid'],
  secs=[
    ('Look at the neck', [
      '!Inspect from the front, neck slightly extended; swallow a sip of water; stick out the tongue || Could you take a sip of water and hold it... now swallow. Could you stick your tongue out? || Movement on swallowing proves it is thyroid.',
    ]),
    ('Feel from behind', [
      '!Find the isthmus below the cricoid; feel each lobe; swallow again || I\'m going to stand behind you and feel your neck. Take another sip and swallow. || ',
      'Size, smooth or nodular, tender, can you get below it || || Can\'t get below it = may extend behind the sternum.',
      'Cervical lymph nodes || || Hard nodes with a nodule = cancer concern.',
      'Trachea position; percuss the sternum for retrosternal extension; listen for a bruit || || A bruit = Graves\', with increased blood flow.',
    ]),
    ('Thyroid status', [
      '!Hands: sweaty or dry, tremor with a sheet of paper on outstretched hands, palmar erythema, acropachy || Hold your arms out straight. || ',
      '!Pulse: rate and rhythm || || AF in an older person can be the only sign of hyperthyroidism.',
      '!Eyes: proptosis from behind and above, lid retraction, lid lag, eye movements and double vision || Follow my finger up and down. || Lid lag = white sclera above the iris as the eye looks down.',
      'Reflexes: biceps or ankle relaxation; proximal myopathy: stand up with arms crossed || Could you stand up without using your arms? || Slow-relaxing reflexes = hypothyroid.',
      'Shins: pretibial myxoedema; legs for oedema || || ',
    ]),
    ('Finish and complete', [
      '!Complete: TFTs, thyroid antibodies, ultrasound of any nodule, and fine needle aspiration if indicated || To complete, I would request TFTs and antibodies, and an ultrasound of the neck. || ',
    ]),
  ],
  cases=[
    ('Graves\' disease', 'Tremor, sweaty, tachycardia, proptosis, lid lag, smooth goitre with a bruit.', '... **Graves\' disease**: TFTs, TSH receptor antibodies, beta-blocker for symptoms, carbimazole.'),
    ('Multinodular goitre', 'Large nodular goitre moving on swallowing, clinically euthyroid, trachea deviated to the right.', '... a **multinodular goitre**: TFTs, ultrasound; refer if compressive symptoms.'),
    ('Hypothyroidism', 'Dry coarse skin, bradycardia, puffy face, slow-relaxing reflexes.', '... **hypothyroidism**: TFTs, thyroid peroxidase antibodies; start levothyroxine.'),
    ('Solitary nodule', 'Single firm 2 cm nodule in the left lobe, clinically euthyroid, a hard node beside it.', '... a **solitary thyroid nodule with lymphadenopathy**: urgent ultrasound and fine needle aspiration on the suspected cancer pathway.'),
  ])
