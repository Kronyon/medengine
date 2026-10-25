from .common import station

DOOR = 'You are an FY1. {who} {task} Explain what you are doing to the patient as you go.'

station('P-bpm', 'proc', 'Blood pressure measurement', 'DOPS', ffp='BP', u=[4],
  door=DOOR.format(who='A 52-year-old man\'s home readings have been high.', task='Measure his blood pressure manually.'),
  hooks=[
    '**Rest 5 minutes, sitting, arm supported at heart level, right cuff size.**',
    '**Feel before you listen:** pump up until the radial pulse vanishes, then add 20 to 30. That stops the silent gap fooling you.',
    '**Korotkoff 1 = first tap = systolic. Korotkoff 5 = sounds disappear = diastolic.**',
    '**Let it down 2 to 3 mmHg per second.**',
    '**Postural drop:** a fall of 20 systolic or 10 diastolic on standing.',
  ],
  money='His blood pressure is 152 over 94 in the right arm, measured seated after 5 minutes\' rest with a standard adult cuff. As this is 140 over 90 or more, I would offer **ambulatory blood pressure monitoring** to confirm hypertension, and assess cardiovascular risk and end-organ damage.',
  traps=['Wrong cuff size', 'Not palpating the systolic first', 'Deflating too fast', 'Arm hanging below heart level'],
  dg=['bp'],
  secs=[
    ('Set up', [
      '!Seated for 5 minutes, no caffeine or smoking for 30 minutes, arm bare and supported at heart level || Have you had any caffeine or a cigarette in the last half hour? || ',
      '!Choose the cuff: the bladder should cover about 80% of the arm; arrow over the brachial artery, 2 to 3 cm above the elbow crease || || A small cuff reads falsely high.',
    ]),
    ('Measure', [
      '!Palpate the radial pulse and inflate until it disappears; note it and deflate || You\'ll feel the cuff squeeze tightly for a moment. || ',
      '!Stethoscope diaphragm over the brachial artery; inflate 20 to 30 above the palpated value || || ',
      '!Deflate 2 to 3 mmHg per second; first tapping sound = systolic; disappearance = diastolic || || ',
      'Record to the nearest 2 mmHg, the arm and the position; measure both arms the first time || || A difference over 15 means repeat; use the higher arm from then on.',
      'Postural BP if dizzy or falls: lying 5 minutes, then standing at 1 and 3 minutes || || ',
    ]),
    ('Act on it', [
      '!Interpret: clinic 140 over 90 or more → offer ambulatory monitoring; 180 over 120 with symptoms or signs → same-day assessment || || NICE NG136.',
    ]),
  ])

station('P-wash', 'proc', 'Hand washing', 'DOPS', ffp='Hand washing', u=[46],
  door='You are an FY1 about to examine a patient. Demonstrate a full hand wash, and tell the examiner when you would use soap and water instead of alcohol gel.',
  hooks=[
    '**6 steps, each 5 times:** palm to palm → backs of hands with fingers laced → palms with fingers laced → backs of fingers locked → thumbs rotated → fingertips in the palms.',
    '**Wash 40 to 60 seconds; rub 20 to 30 seconds.**',
    '**5 moments:** before touching a patient, before a clean procedure, after body fluid exposure, after touching a patient, after touching their surroundings.',
    '**Soap and water, not gel, for diarrhoea: C. difficile and norovirus,** because alcohol doesn\'t kill spores.',
    '**Bare below the elbows.**',
  ],
  money='I have washed my hands using the 6-step technique for about 40 seconds, dried them with a paper towel and turned the tap off with the towel. I would use **soap and water rather than alcohol gel** when my hands are visibly dirty and for patients with diarrhoea, such as **C. difficile or norovirus**.',
  traps=['Wearing a watch or rings', 'Skipping the thumbs or fingertips', 'Turning the tap off with clean hands'],
  dg=['wash', 'moments'],
  secs=[
    ('Prepare', [
      '!Bare below the elbows: no watch, rings except a plain band, sleeves rolled up; cover cuts || || ',
      'Wet hands with warm water; apply soap || || ',
    ]),
    ('The 6 steps', [
      '!Palm to palm || || ',
      '!Right palm over the back of the left hand with fingers laced, and the other way || || ',
      '!Palm to palm with fingers laced || || ',
      '!Backs of fingers to the opposite palm with fingers interlocked || || ',
      '!Rotational rubbing of each thumb in the opposite palm || || The thumbs are the most often missed area.',
      '!Rotational rubbing of the fingertips in the opposite palm || || ',
    ]),
    ('Finish', [
      'Rinse; dry thoroughly with paper towels; turn the tap off with the towel or elbow; bin it with the foot pedal || || ',
      '!Name the 5 moments and when soap is needed instead of gel || || ',
    ]),
  ])

station('P-cbg', 'proc', 'Capillary blood glucose', 'DOPS', ffp='Blood glucose', u=[67, 70],
  door=DOOR.format(who='A 70-year-old woman with type 2 diabetes on gliclazide is sweaty and confused.', task='Measure her capillary blood glucose.'),
  hooks=[
    '**Wash their hands first:** sugar on the skin gives a falsely high reading.',
    '**Side of the finger, not the pad:** fewer nerve endings, less pain. Avoid the thumb and index finger.',
    '**Check the meter and strips:** quality control done and strips in date.',
    '**Four is the floor:** under 4 mmol/L = hypoglycaemia: treat now.',
  ],
  money='Her capillary blood glucose is **2.8 mmol/L**, so she is **hypoglycaemic**. As she is confused but able to swallow, I would give **15 to 20 g of fast-acting glucose**, such as 4 to 5 glucose tablets or 150 to 200 ml of fruit juice, recheck in 10 to 15 minutes, then give a longer-acting carbohydrate. I would review her gliclazide.',
  traps=['Not washing the patient\'s hands', 'Using the pad of the finger', 'Not disposing of the lancet straight away', 'Getting a reading but not acting on it'],
  dg=['cbg'],
  secs=[
    ('Prepare', [
      '!Check the meter\'s quality control and the strip expiry date || || ',
      '!Patient washes and dries their hands; gloves on || Could you wash your hands with water for me first? || ',
    ]),
    ('Do it', [
      '!Choose the side of a fingertip on the middle or ring finger; use a single-use lancet || A small sharp scratch now. || ',
      'Squeeze gently from the base, don\'t milk the tip; apply the drop to the strip || || Hard squeezing dilutes the blood with tissue fluid.',
      '!Lancet straight into the sharps bin; pressure with gauze || || ',
    ]),
    ('Act on it', [
      '!Read, document and act: under 4 treat a hypo; over 11 in type 1 diabetes check ketones || || ',
    ]),
  ])

station('P-inhaler', 'proc', 'Inhaler technique', 'DOPS', ffp='Inhaler technique', u=[15, 16],
  door=DOOR.format(who='A 23-year-old with asthma keeps needing his blue inhaler.', task='Check and teach his inhaler technique with a metered-dose inhaler and a spacer.'),
  hooks=[
    '**Metered-dose inhaler: slow and steady,** a 3 to 5 second breath in. **Dry powder: quick and deep.**',
    '**Shake, breathe out, seal, press as you start breathing in, hold for 10.**',
    '**Wait 30 to 60 seconds between puffs.**',
    '**Rinse and spit after a steroid inhaler** to prevent thrush and a hoarse voice.',
    '**Watch them do it.** Then ask them to show you again: teach-back.',
  ],
  money='His technique has improved after demonstration. He now shakes the inhaler, breathes out fully, presses at the start of a **slow 3 to 5 second breath**, holds it for 10 seconds and waits before the second puff. I have given him a spacer, explained cleaning it monthly, and reminded him to **rinse his mouth after his preventer**. I would review him in 4 to 6 weeks.',
  traps=['Not asking the patient to show you first', 'Not checking the dose counter or expiry', 'Teaching a fast breath for a metered-dose inhaler', 'No teach-back'],
  dg=['inhaler'],
  secs=[
    ('Assess first', [
      '!Ask them to show you how they normally use it, and watch || Could you show me how you usually take your inhaler? || You can\'t correct what you haven\'t seen.',
    ]),
    ('Metered-dose inhaler', [
      'Check the dose counter and expiry; remove the cap; shake || || ',
      '!Sit or stand upright; breathe out fully, away from the inhaler || Breathe all the way out first. || ',
      '!Seal the lips; press once as you start a slow, deep breath over 3 to 5 seconds || Start breathing in slowly, and press now. || Pressing too early or late puts the drug on the back of the throat.',
      '!Hold the breath for 10 seconds, or as long as comfortable || || ',
      'Wait 30 to 60 seconds before a second puff || || ',
    ]),
    ('Spacer', [
      'Shake the inhaler and fit it into the spacer; one puff into the spacer, then 5 normal breaths or one slow deep breath and hold || || A spacer delivers more drug to the lungs, especially in an attack.',
      'Clean the spacer monthly with warm soapy water and let it air dry; replace yearly || || Drying with a cloth makes it static, so drug sticks to it.',
    ]),
    ('Finish', [
      '!Rinse and spit after a steroid inhaler || || ',
      '!Teach-back: watch them do it again || Could you show me once more so I know I explained it clearly? || ',
    ]),
  ])

station('P-pefr', 'proc', 'Peak flow measurement', 'DOPS', ffp='Peak flow', u=[15, 16],
  door=DOOR.format(who='A 30-year-old woman has a wheeze that is worse in the mornings.', task='Measure her peak expiratory flow and interpret it.'),
  hooks=[
    '**Huff, don\'t puff:** short, sharp and hard, like blowing out candles. Not long.',
    '**Best of 3,** each within about 20 L/min of each other.',
    '**Compare with her predicted and her own best.**',
    '**Variation over 20% between morning and evening suggests asthma.**',
  ],
  money='Her best of 3 readings is **320 L/min**, against a predicted 450, which is about **70% of predicted**. I would ask her to keep a **peak flow diary** twice a day for 2 to 4 weeks, as **variability of over 20%** supports asthma, alongside spirometry with reversibility and FeNO.',
  traps=['Not resetting the pointer', 'Fingers over the scale', 'Recording the average instead of the best', 'Not comparing with predicted'],
  dg=['pefr'],
  secs=[
    ('Prepare', [
      'New disposable mouthpiece; pointer to zero; fingers clear of the scale || || ',
      '!Stand or sit upright || Could you sit up straight, or stand if you can? || ',
    ]),
    ('Do it', [
      '!Big breath in, seal the lips around the mouthpiece, blow out as hard and fast as possible || Take the biggest breath you can, seal your lips, and blast it out as hard and fast as you can, like blowing out candles. || ',
      '!Record; reset; repeat 3 times; take the best || || ',
    ]),
    ('Interpret', [
      '!Compare with predicted for age, height and sex, and with their personal best; document || || In an attack: under 50% of best = acute severe; under 33% = life-threatening.',
    ]),
  ])

station('P-obs', 'proc', 'Basic physiological observations', 'DOPS', ffp='Basic physiological obs', u=[46, 12],
  door=DOOR.format(who='A 76-year-old man on the ward has become drowsy.', task='Take a full set of observations, calculate his NEWS2 and say what you would do.'),
  hooks=[
    '**Breathing rate first and quietly,** while you pretend to take the pulse. It changes first and is the one most often guessed.',
    '**NEWS2 bands:** 0 to 4 low; a single red 3 or a total of 5 to 6 = urgent review; 7 or more = emergency team.',
    '**New confusion = C in ACVPU,** scored as 3 on its own.',
    '**Scale 2 for oxygen saturations only if the target is 88 to 92%,** such as in a carbon dioxide retainer.',
  ],
  money='His observations are: respiratory rate 24, saturations 93% on air, blood pressure 98 over 60, pulse 112, new confusion, and temperature 38.6. That gives a **NEWS2 of 12**, an **emergency response**. I would escalate to the registrar immediately using SBAR, start an A to E assessment, and suspect **sepsis**: sepsis six within the hour.',
  traps=['Telling the patient you are counting breaths', 'Forgetting to note the oxygen device and flow', 'Calculating the score but not escalating'],
  dg=['news2'],
  secs=[
    ('Observations', [
      '!Respiratory rate for 30 to 60 seconds without telling them || || ',
      '!Oxygen saturations with a warm finger; note the device and flow; correct scale || || ',
      'Blood pressure with the right cuff || || ',
      'Pulse rate, rhythm and volume for 30 to 60 seconds, a full minute if irregular || || ',
      '!Level of consciousness: ACVPU || Can you tell me where you are today? || ',
      'Temperature; capillary refill; capillary glucose if unwell || || ',
    ]),
    ('Score and act', [
      '!Plot each and total the NEWS2 || || ',
      '!Act on the score and escalate with SBAR || I\'m calling because Mr Smith has a NEWS2 of 12 and I am worried he is septic. || The score is useless unless you escalate.',
    ]),
  ])

station('P-ecg12', 'proc', '12-lead ECG recording', 'DOPS', ffp='12-lead ECG', u=[0, 3],
  door=DOOR.format(who='A 64-year-old man has chest pain.', task='Record a 12-lead ECG.'),
  hooks=[
    '**Find the sternal angle:** the 2nd rib is beside it, so the gap below is the 2nd space. Count down to the 4th.',
    '**V1 and V2 in the 4th space either side of the sternum. V4 in the 5th space, midclavicular. V3 halfway between. V5 and V6 level with V4 in the anterior and mid axillary lines.**',
    '**Limb leads, clockwise from the right arm: Ride Your Green Bike:** Red right arm, Yellow left arm, Green left leg, Black right leg.',
    '**Check 25 mm per second and 10 mm per mV,** then label and show it straight away if there is chest pain.',
  ],
  money='I have recorded a 12-lead ECG with the patient lying at 45 degrees, at **25 mm per second and 10 mm per millivolt**. It is labelled with his name, date of birth, date, time and "chest pain". Because he has chest pain, I would **show it to a senior immediately**, within 10 minutes of arrival.',
  traps=['Placing V1 and V2 too high', 'Swapping the arm leads', 'Not labelling it', 'Not showing it to a doctor when there is chest pain'],
  dg=['ecg12'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; offer a chaperone; expose the chest || I\'m going to put some stickers on your chest, wrists and ankles to record the electrical activity of your heart. It doesn\'t hurt. || ',
      'Lie at 45 degrees; skin clean and dry; shave if needed || || ',
    ]),
    ('Electrodes', [
      '!Limb leads on the wrists and ankles: red right arm, yellow left arm, green left leg, black right leg || || ',
      '!V1 4th space right sternal edge; V2 4th space left sternal edge || || ',
      '!V4 5th space midclavicular; V3 between V2 and V4; V5 anterior axillary line; V6 mid-axillary line, both level with V4 || || ',
    ]),
    ('Record', [
      'Ask them to lie still, relax and breathe normally; check speed 25 mm/s and gain 10 mm/mV; record || Try to stay as still as you can for a few seconds. || ',
      '!Label: name, date of birth, date, time, symptoms; show to a doctor immediately if chest pain || || ',
      'Remove the electrodes, help them dress, wash hands || || ',
    ]),
  ])

station('P-ecg3', 'proc', '3-lead ECG monitoring', 'DOPS', ffp='3-lead ECG', u=[3],
  door=DOOR.format(who='A 70-year-old with palpitations needs cardiac monitoring.', task='Attach a 3-lead cardiac monitor.'),
  hooks=[
    '**Ride Your Green:** Red under the right collarbone, Yellow under the left collarbone, Green on the lower left chest.',
    '**Put them on bone, not muscle,** to reduce movement interference.',
    '**Lead II shows the rhythm best.**',
    '**A monitor is for rhythm only:** it can\'t diagnose ischaemia. That needs a 12-lead.',
  ],
  money='I have attached a 3-lead monitor: **red below the right clavicle, yellow below the left clavicle, green on the lower left chest**. I have selected **lead II**, set heart rate alarms, and the trace shows sinus rhythm at 88. For any chest pain I would record a **12-lead ECG**.',
  traps=['Swapping red and yellow', 'Placing electrodes over muscle', 'Not setting the alarms'],
  dg=['ecg3'],
  secs=[
    ('Do it', [
      '!ID, explain, consent; expose the chest; clean dry skin || || ',
      '!Red below the right clavicle, yellow below the left clavicle, green on the lower left chest wall || || ',
      '!Select lead II; check the trace; set alarm limits || || ',
      'Document and explain the alarms to the patient || The monitor may beep if a wire comes loose; just let the nurse know. || ',
    ]),
  ])

station('P-dip', 'proc', 'Urine dipstick', 'DOPS', ffp='Urine dipstick', u=[80, 67, 77],
  door=DOOR.format(who='A 28-year-old woman has burning when passing urine.', task='Test her urine sample with a dipstick and interpret it.'),
  hooks=[
    '**Nitrites are specific, leucocytes are sensitive.** Both positive with symptoms = UTI.',
    '**Read each pad at its own time** using the chart on the bottle; a timer matters.',
    '**Blood and protein = think kidney.** Glucose = diabetes. Ketones = DKA or not eating.',
    '**Do a pregnancy test in any woman who could be pregnant.**',
    '**Over 65s: don\'t dip for a UTI.** Bacteria in the urine are common and harmless.',
  ],
  money='The dipstick shows **leucocytes 2+ and nitrites positive**, with a trace of blood and no glucose or protein. The pregnancy test is negative. With her symptoms, this is consistent with an **uncomplicated lower UTI**. I would send the sample for culture and offer **nitrofurantoin 100 mg modified-release twice daily for 3 days**.',
  traps=['Not checking the expiry date', 'Reading all the pads at once', 'Forgetting a pregnancy test', 'Not sending for culture when indicated'],
  dg=['dip'],
  secs=[
    ('Prepare', [
      '!Gloves; fresh midstream sample; check the expiry date on the pot; don\'t touch the pads || || ',
    ]),
    ('Do it', [
      '!Dip all pads briefly; tap off the excess; hold horizontal || || ',
      '!Read each pad against the bottle chart at the stated time || || ',
    ]),
    ('Interpret', [
      '!Report and interpret: leucocytes, nitrites, blood, protein, glucose, ketones, pH, specific gravity; pregnancy test || || ',
      'Send for culture: pregnancy, men, children, treatment failure, recurrent infection || || ',
    ]),
  ])

station('P-cann', 'proc', 'IV cannulation', 'DOPS', ffp='IV cannulation', u=[51],
  door=DOOR.format(who='A 54-year-old man needs IV fluids.', task='Insert an IV cannula on the model.'),
  hooks=[
    '**Gauge colours, biggest to smallest:** orange 14, grey 16, green 18, pink 20, blue 22. A green 18 is the usual adult choice; grey or orange for resuscitation.',
    '**Clean 30 seconds, dry 30 seconds, and don\'t touch it again.**',
    '**Flashback, then drop the angle and go 2 mm further,** so the plastic is in the vein before you slide it off the needle.',
    '**Release the tourniquet before you take the needle out.**',
    '**Needle straight in the sharps bin. Never re-sheath.**',
  ],
  money='I inserted an **18 gauge green cannula** into the right forearm vein at the first attempt using aseptic non-touch technique. It flushed easily with 5 ml of saline without pain or swelling. It is secured with a sterile dressing, dated, and documented with a **VIP score of 0**.',
  traps=['Re-palpating the cleaned skin', 'Removing the needle before releasing the tourniquet', 'Not flushing', 'Not documenting'],
  dg=['cann'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; allergies to chlorhexidine, plasters or latex || I need to put a small plastic tube in your vein for fluids. It\'s a sharp scratch, then the needle comes out and only the plastic stays. || ',
      'Clean the tray; gather the cannula, tourniquet, 2% chlorhexidine in 70% alcohol wipe, dressing, saline flush, sharps bin, gloves || || ',
    ]),
    ('Insert', [
      '!Tourniquet; choose a straight vein away from a joint; clean for 30 seconds and let it dry || || ',
      '!Anchor the skin; bevel up at 10 to 30 degrees; watch for flashback || Sharp scratch now. || ',
      '!Drop the angle, advance 2 mm, slide the cannula off the needle into the vein || || ',
      '!Release the tourniquet; press over the vein beyond the tip; remove the needle into the sharps bin; cap || || ',
    ]),
    ('Finish', [
      '!Flush with saline: no pain or swelling; secure with a dressing; date it || || ',
      'Document: site, size, date, time, attempts, VIP score || || ',
    ]),
  ])

station('P-venep', 'proc', 'Venepuncture', 'DOPS', ffp='Venepuncture', u=[51, 10],
  door=DOOR.format(who='A 45-year-old woman needs blood tests: blood cultures, clotting, U&E, FBC and glucose.', task='Take the blood on the model.'),
  hooks=[
    '**Order of draw: Cultures → Clotting → Chemistry → Counts → Crossmatch → Glucose.**',
    'Colours: culture bottles → light blue → gold → purple → pink → grey. Green heparin comes after gold if used.',
    '**Tourniquet off within a minute, and before the needle comes out.**',
    '**Label at the bedside, in front of the patient.** Crossmatch is handwritten.',
    '**Invert gently, don\'t shake.**',
  ],
  money='I have taken blood from the left antecubital fossa at the first attempt. I filled the bottles in order: **blood cultures, then light blue for clotting, gold for U&E, purple for FBC and grey for glucose**. I labelled them at the bedside, checked the patient\'s details, and sent them with a completed request form.',
  traps=['Wrong order of draw', 'Leaving the tourniquet on for over a minute', 'Labelling away from the patient', 'Not checking for a needle-stick risk or allergy'],
  dg=['draw'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; check allergies and any arm to avoid such as a fistula or mastectomy side || Is there an arm we should avoid? || ',
      'Gather the vacutainer, needle, tubes, tourniquet, chlorhexidine wipe, cotton wool, plaster, sharps bin, gloves || || ',
    ]),
    ('Take blood', [
      '!Tourniquet; find a vein; clean for 30 seconds and let it dry || || ',
      '!Anchor; needle bevel up at about 30 degrees; attach the bottles in order || Sharp scratch. || ',
      '!Release the tourniquet before removing the needle; press with cotton wool || || ',
      '!Needle straight in the sharps bin || || ',
    ]),
    ('Finish', [
      'Invert the tubes gently; label at the bedside; request form; plaster || || ',
    ]),
  ])

station('P-abg', 'proc', 'Arterial blood gas sampling', 'DOPS', ffp='ABG', u=[12],
  door=DOOR.format(who='A 68-year-old with COPD is drowsy on oxygen.', task='Take an arterial blood gas on the model, and say how you would interpret it.'),
  hooks=[
    '**Allen\'s test first:** press on both arteries, they clench, release the ulnar side: colour back within 10 seconds = safe to use the radial.',
    '**Wrist bent back over a rolled towel,** 2 cm above the crease, at 30 to 45 degrees toward the pulse.',
    '**Press for 5 minutes,** longer on anticoagulants.',
    '**Expel the air, cap it, and run it within 10 minutes.** Write down the oxygen they are on.',
    '**Interpret: pH → CO2 → bicarbonate → oxygen.** Expected oxygen is roughly the inspired percentage minus 10 kPa.',
  ],
  money='I took a sample from the right radial artery after a normal modified Allen\'s test, pressed for 5 minutes and ran it within 10 minutes, noting he is on **28% oxygen**. The gas shows **pH 7.29, pCO2 8.9, bicarbonate 32, pO2 7.8**: an **acute on chronic type 2 respiratory failure with acidosis**. I would titrate oxygen to 88 to 92% and discuss **NIV** with my senior.',
  traps=['Skipping Allen\'s test', 'Not checking anticoagulation and clotting', 'Not expelling air bubbles', 'Not recording the inspired oxygen'],
  dg=['abg'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; check for anticoagulants and a low platelet count || This blood comes from an artery at your wrist, so it can be sharper than a normal blood test. || ',
      '!Modified Allen\'s test || Make a tight fist for me... now open your hand. || ',
      'Pre-heparinised syringe, gauze, local anaesthetic if used, sharps bin || || ',
    ]),
    ('Take it', [
      '!Wrist extended over a rolled towel; palpate the radial pulse; clean || || ',
      '!Needle at 30 to 45 degrees toward the pulse, bevel up; let arterial pressure fill 1 to 2 ml || Sharp scratch now. || ',
      '!Withdraw and press firmly for 5 minutes or more || || ',
    ]),
    ('Process', [
      '!Expel air, cap, label, record the inspired oxygen; analyse within 10 minutes || || ',
      'Interpret: pH, pCO2, bicarbonate, base excess, pO2 against the inspired oxygen; lactate || || ',
    ]),
  ])

station('P-swab', 'proc', 'Taking swabs: viral and bacterial', 'DOPS', ffp='Swabs (viral & bacterial)', u=[151, 14, 131],
  door=DOOR.format(who='A 30-year-old has a sore throat and fever, and an infected cut on her leg.', task='Take a viral nose and throat swab and a bacterial wound swab.'),
  hooks=[
    '**Bacteria go into gel; viruses go into liquid.** Bacterial swab in charcoal or Amies gel; viral swab in viral transport medium.',
    '**Throat: tonsils and back wall, not the tongue or cheeks.** Nose: along the floor of the nose, parallel to the roof of the mouth.',
    '**Wound: clean off the pus with saline first,** then zig-zag and rotate over viable tissue.',
    '**Label, request form with clinical details and any antibiotics, bag it, send promptly.**',
  ],
  money='I took a combined **viral nose and throat swab into viral transport medium** and a **bacterial wound swab into Amies medium** after cleaning the wound with saline. Both are labelled, with request forms noting the clinical details and that she has **not yet had antibiotics**, and sent to the lab.',
  traps=['Touching the tongue or cheeks', 'Putting a viral swab into a bacterial gel tube', 'Not cleaning the wound surface', 'Missing clinical details and antibiotics on the form'],
  dg=['swab'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; PPE including mask and eye protection for viral swabs || This might make you gag or your eyes water for a moment. || ',
    ]),
    ('Viral nose and throat', [
      '!Throat: depress the tongue, rub both tonsils and the back of the throat || Say ahh for me. || ',
      '!Nose: same swab, along the floor of the nostril about 2 cm, rotate for a few seconds || Tip your head back slightly. || ',
      'Into viral transport medium; snap at the line; close the lid || || ',
    ]),
    ('Bacterial wound', [
      '!Clean the surface with saline; zig-zag across the wound while rotating the swab; into Amies or charcoal gel || || ',
    ]),
    ('Send', [
      '!Label at the bedside; request form with site, clinical details and antibiotics; bag; send promptly || || ',
    ]),
  ])

station('P-catm', 'proc', 'Male catheterisation', 'DOPS', ffp='Male & Female Catheterisation', u=[85, 75],
  door=DOOR.format(who='A 78-year-old man is in painful urinary retention.', task='Insert a urethral catheter on the model.'),
  hooks=[
    '**Two hands, two jobs:** the non-dominant hand holds the penis and becomes dirty; the dominant hand stays sterile for the catheter.',
    '**Penis up at 90 degrees** to straighten the urethra.',
    '**To the hilt, see urine, then inflate.** Never inflate before urine: a balloon in the urethra tears it.',
    '**10 ml of sterile water in the balloon.** Stop if it hurts.',
    '**Always replace the foreskin.**',
  ],
  money='I inserted a **12 Ch Foley catheter** using aseptic technique with lidocaine gel. **Urine drained before I inflated the balloon** with 10 ml sterile water, without pain. The **foreskin was replaced**. The residual volume was **900 ml**. I documented the size, batch number, residual volume and that the foreskin was replaced, and would monitor his U&Es.',
  traps=['Inflating before urine flows', 'Not waiting for the lidocaine gel to work', 'Contaminating the sterile hand', 'Forgetting to replace the foreskin'],
  dg=['cath'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent; chaperone; check allergies, especially to lidocaine or chlorhexidine || I need to put a soft tube into your bladder through your penis to drain the urine. I\'ll use a numbing gel first. || ',
      'Catheter 12 to 14 Ch; lidocaine gel; sterile pack; 2 pairs of sterile gloves; 10 ml sterile water; bag || || ',
    ]),
    ('Clean and numb', [
      '!Lying flat; sterile field; with the non-dominant hand, retract the foreskin and clean the glans away from the meatus || || ',
      '!Insert the lidocaine gel slowly; wait 3 to 5 minutes || You\'ll feel a cold, stinging feeling for a moment. || ',
    ]),
    ('Insert', [
      '!Hold the penis upright; advance the catheter with the sterile hand using the sleeve, to the hilt || || ',
      '!Wait for urine, then inflate the balloon with 10 ml sterile water, watching for pain || || ',
      'Withdraw gently until resistance; attach the bag below bladder level || || ',
      '!Replace the foreskin || || ',
    ]),
    ('Finish', [
      '!Document: indication, size, batch, residual volume, foreskin replaced; send a urine sample if needed || || ',
    ]),
  ])

station('P-catf', 'proc', 'Female catheterisation', 'DOPS', ffp='Male & Female Catheterisation', u=[85],
  door=DOOR.format(who='A 70-year-old woman needs her urine output monitored after surgery.', task='Insert a urethral catheter on the model.'),
  hooks=[
    '**Knees bent and apart, heels together.**',
    '**Separate the labia with the non-dominant hand; clean front to back, one swab per stroke.**',
    '**The meatus is above the vaginal opening.** Wrong hole? Leave that catheter in as a signpost and use a new one.',
    '**Advance until urine, then 2 cm more, then inflate.**',
  ],
  money='I inserted a **12 Ch Foley catheter** using aseptic technique with lidocaine gel. Urine drained, and I inflated the balloon with 10 ml sterile water without pain. The residual volume was 150 ml. I documented the size, batch number and residual volume.',
  traps=['Cleaning back to front', 'Losing the meatus by letting go of the labia', 'Not using a new catheter after entering the vagina'],
  dg=['cath'],
  secs=[
    ('Prepare', [
      '!ID, explain, consent, chaperone, allergies || || ',
      'Position: lying flat, knees bent and apart, heels together || || ',
    ]),
    ('Clean and insert', [
      '!Separate the labia with the non-dominant hand and keep them apart; clean front to back, one swab per stroke || || ',
      '!Lidocaine gel into the meatus; wait 3 to 5 minutes || || ',
      '!Insert the catheter until urine flows, then 2 cm further; inflate with 10 ml sterile water || || ',
      'Attach the bag below the bladder || || ',
    ]),
    ('Finish', [
      '!Document: indication, size, batch, residual volume || || ',
    ]),
  ])
