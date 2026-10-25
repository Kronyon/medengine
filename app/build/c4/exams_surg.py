from .common import station

DOOR = 'You are an FY1. {who} Examine their {sys}, then present your findings to the examiner. Aim to finish examining by 7 minutes.'
MSK_HOOKS = ['**Look → Feel → Move → Special tests → Function.** Then always: "I would examine the joint above and below, check the neurovascular status and request an X-ray."',
             '**Ask about pain first and watch the face** every time you move a joint. Hurting the patient is the fastest way to fail an MSK station.',
             '**Active before passive:** the patient moves first, then you move it. Lost active but full passive = a tendon or nerve problem; both lost = the joint itself.']
PAIN = '!Expose both sides to compare; ask about pain before touching || Before we start, is there any pain? Tell me straight away if anything hurts and I\'ll stop. || Comparing with the good side is the reference for everything you find.'

station('E-ankle', 'ex', 'MSK: ankle and foot examination', 'Surgery', ffp='MSK Ankle + Foot', u=[86, 71],
  door=DOOR.format(who='A 28-year-old twisted his ankle playing football yesterday.', sys='ankle and foot'),
  hooks=MSK_HOOKS[:1] + [
    '**Ottawa ankle rules:** X-ray if there is bone tenderness at the back edge or tip of either malleolus, or they can\'t take 4 steps both straight after the injury and in the department.',
    '**Ottawa foot:** tender at the base of the 5th metatarsal or the navicular → foot X-ray.',
    '**Simmonds\' squeeze:** squeeze the calf; if the foot doesn\'t point down, the Achilles has snapped.',
    '**Tiptoe test:** the heels should swing inward. If not, think tibialis posterior dysfunction and a flat foot.',
  ],
  money='On examination of this gentleman\'s right ankle, there was swelling and bruising over the lateral malleolus. He was tender over the anterior talofibular ligament but not over the bony edges of either malleolus, the base of the 5th metatarsal or the navicular, and he could take 4 steps. Simmonds\' test was normal. These findings are consistent with a **lateral ankle sprain**, and by the **Ottawa rules he does not need an X-ray**. I would advise rest, ice, compression and elevation, with analgesia and early mobilisation.',
  traps=['Not applying the Ottawa rules out loud', 'Forgetting Simmonds\' test', 'Not looking from behind at the heels', 'Missing the foot pulses and sensation'],
  dg=['msk', 'ottawa'],
  secs=[
    ('Look', [
      PAIN,
      'Standing from the front, side and behind: arches, bunions, toe deformities, swelling, bruising, calluses || Could you stand up for me, with your feet together? || Flat or high arches, and the heel angle from behind.',
      'Tiptoe; gait; look at the shoes for wear || Could you stand on your tiptoes? Now walk to the door and back. || ',
    ]),
    ('Feel', [
      'Temperature with the back of the hand; foot pulses and capillary refill || || ',
      '!Bony landmarks for Ottawa: back edge and tip of both malleoli, base of the 5th metatarsal, navicular || I\'m going to press on some bones; tell me if it\'s sore. || These are the exact spots the rules use.',
      'Ligaments: anterior talofibular in front of the lateral malleolus; Achilles tendon for a gap; plantar fascia at the heel || || Heel pain worst with the first steps in the morning = plantar fasciitis.',
      'Squeeze across the toe joints || || Pain = synovitis, as in rheumatoid arthritis; a hot red big toe joint = gout.',
    ]),
    ('Move', [
      'Ankle: point the toes up and down, actively then passively || Point your toes to the ceiling, now push them down. || ',
      'Hindfoot: hold the heel and turn it in and out; midfoot; toes || || Inversion hurts in a lateral sprain.',
    ]),
    ('Special tests', [
      '!Simmonds\' calf squeeze, kneeling on a chair or lying face down || Could you kneel on the chair for me? I\'m going to squeeze your calf. || No movement of the foot = Achilles rupture.',
      '!State the Ottawa decision out loud || By the Ottawa rules, he does or doesn\'t need an X-ray because... || Saying the decision is the reasoning mark.',
    ]),
    ('Finish and complete', [
      '!Complete: examine the knee, neurovascular status of the foot, X-ray if Ottawa positive || To complete, I would examine the knee, check sensation in the foot, and request an X-ray if the Ottawa rules say so. || ',
    ]),
  ],
  cases=[
    ('Lateral ankle sprain', 'Swelling and tenderness in front of the lateral malleolus, no bony tenderness, can walk 4 steps.', '... a **lateral ligament sprain**; Ottawa negative, so no X-ray: RICE, analgesia, early movement.'),
    ('Ankle fracture', 'Tender at the tip of the lateral malleolus, unable to bear weight.', '... **Ottawa positive**: I would X-ray the ankle for a fracture.'),
    ('Achilles rupture', 'Sudden pain like being kicked at the back of the ankle while playing squash; palpable gap; Simmonds\' positive.', '... an **Achilles tendon rupture**: immobilise in an equinus boot and refer to orthopaedics urgently.'),
    ('Gout', 'Hot, red, exquisitely tender first metatarsophalangeal joint.', '... **acute gout of the first MTP joint**: NSAID or colchicine; urate after it settles.'),
    ('Hallux valgus', 'Big toe angled toward the others with a bony lump on the inside of the foot.', '... **hallux valgus** with a bunion: wider shoes; surgery if painful.'),
  ])

station('E-elbow', 'ex', 'MSK: elbow examination', 'Surgery', ffp='MSK Elbow', u=[86],
  door=DOOR.format(who='A 45-year-old decorator has pain on the outside of his right elbow.', sys='elbow'),
  hooks=MSK_HOOKS[:1] + [
    '**Tennis = lateral = extensors.** A backhand uses the muscles that bend the wrist back.',
    '**Golfer\'s = medial = flexors.**',
    '**Cozen\'s test:** resisted wrist extension with the elbow straight hurts on the outside = tennis elbow.',
    '**Pronation and supination with the elbows tucked in**, holding pens like thumbs-up, so the shoulder can\'t cheat.',
  ],
  money='On examination of this gentleman\'s right elbow, there was no swelling or deformity and a normal carrying angle. He was tender over the lateral epicondyle. He had a full range of movement, but Cozen\'s test reproduced lateral elbow pain. These findings are consistent with **lateral epicondylitis**, tennis elbow. I would advise rest from the aggravating activity, analgesia, physiotherapy and an elbow strap.',
  traps=['Not checking the carrying angle', 'Forgetting the ulnar nerve in the groove', 'Testing pronation without tucking the elbows in'],
  dg=['msk', 'elbow'],
  secs=[
    ('Look', [
      PAIN,
      'Carrying angle with the arms straight and palms forward; swelling over the olecranon; rheumatoid nodules; psoriasis plaques; scars || Could you hold your arms out with your palms facing forward? || A boggy swelling over the point = olecranon bursitis.',
    ]),
    ('Feel', [
      'Temperature; lateral epicondyle; medial epicondyle; olecranon || || ',
      'Radial head while you turn the forearm; ulnar nerve in the groove behind the medial epicondyle || || ',
    ]),
    ('Move', [
      '!Flexion and extension, actively then passively || Touch your shoulder, then straighten your arm fully. || ',
      'Pronation and supination with the elbows tucked into the sides || Tuck your elbows in, thumbs up, now turn your palms up, then down. || ',
    ]),
    ('Special tests', [
      '!Cozen\'s: elbow straight, make a fist, cock the wrist back against your resistance || Make a fist and push your hand up against mine. || Pain at the lateral epicondyle = tennis elbow.',
      'Golfer\'s test: resisted wrist flexion || Now push your hand down against mine. || Pain at the medial epicondyle = golfer\'s elbow.',
      'Function: hand to mouth, hand behind the head || || ',
    ]),
    ('Finish and complete', [
      '!Complete: shoulder and wrist, neurovascular status of the hand, X-ray if indicated || To complete, I would examine the shoulder and wrist and check the nerves and pulses in the hand. || ',
    ]),
  ],
  cases=[
    ('Tennis elbow', 'Tender lateral epicondyle, positive Cozen\'s test.', '... **lateral epicondylitis**: activity modification, analgesia, physiotherapy, strap.'),
    ('Golfer\'s elbow', 'Tender medial epicondyle, pain on resisted wrist flexion.', '... **medial epicondylitis**.'),
    ('Olecranon bursitis', 'Fluctuant swelling over the olecranon with full movement.', '... **olecranon bursitis**; if hot and red, aspirate to exclude infection or gout.'),
    ('Rheumatoid nodules', 'Firm nodules along the extensor surface of the forearm with symmetrical hand synovitis.', '... **rheumatoid nodules**: examine the hands.'),
  ])

station('E-hand', 'ex', 'MSK: hand and wrist examination', 'Surgery', ffp='MSK Hand + Wrist', u=[86, 99],
  door=DOOR.format(who='A 58-year-old woman has painful, stiff hands.', sys='hands'),
  hooks=MSK_HOOKS[:1] + [
    '**RA = soft, warm, symmetrical MCP and PIP joints, spares the DIP.** Ulnar deviation, swan neck, boutonnière, Z-thumb.',
    '**OA = hard bony nodes.** B for Bouchard\'s comes before H for Heberden\'s, just as the PIP comes before the DIP walking out to the fingertip.',
    '**Three nerves, three tests:** radial = wrist extension; ulnar = spread the fingers; median = thumb to the ceiling.',
    '**Snuffbox tenderness after a fall on the outstretched hand = scaphoid fracture until proven otherwise,** even with a normal X-ray.',
  ],
  money='On examination of this lady\'s hands, there was symmetrical swelling of the MCP and PIP joints with ulnar deviation and swan-neck deformities. The joints were warm and tender, with sparing of the DIP joints. There were nodules at the elbows. Grip strength and fine function were reduced. These findings are consistent with **rheumatoid arthritis**. I would like **X-rays of the hands, rheumatoid factor, anti-CCP, CRP and ESR**, and refer to rheumatology.',
  traps=['Forgetting to look at the elbows', 'Not testing function such as a button or a coin', 'Missing the three nerves'],
  dg=['msk', 'hand'],
  secs=[
    ('Look', [
      PAIN,
      '!Backs then palms on a pillow: swellings, deformities, nail pitting, wasting of the thenar and hypothenar eminences, scars, skin || Could you put your hands on the pillow, palms down, then turn them over? || ',
      'Elbows: rheumatoid nodules, psoriasis || || ',
    ]),
    ('Feel', [
      'Temperature over the joints; radial pulse; bulk of the thenar and hypothenar muscles || || ',
      '!Gently squeeze across the MCP joints, watching the face; feel each joint bimanually || I\'m going to squeeze gently across your knuckles. || Pain on squeeze = synovitis.',
      'Sensation: index pulp for the median, little finger pulp for the ulnar, back of the thumb web for the radial || || ',
      'Anatomical snuffbox || || ',
    ]),
    ('Move', [
      'Prayer and reverse prayer; make a fist; spread the fingers || Put your hands together like a prayer. Now back to back. Make a fist. Spread your fingers. || ',
      '!Power: wrist extension, finger abduction, thumb abduction; Froment\'s || Hold this paper between your thumb and finger while I pull. || Froment\'s: the thumb bends to grip = weak ulnar adductor.',
    ]),
    ('Special tests and function', [
      'Phalen\'s for 60 seconds and Tinel\'s over the carpal tunnel || || Tingling in the thumb, index and middle fingers = carpal tunnel.',
      'Finkelstein\'s for de Quervain\'s || || ',
      '!Function: grip, pinch, pick up a coin, undo a button, write || Could you undo this button for me? || Function is what matters to the patient.',
    ]),
    ('Finish and complete', [
      '!Complete: elbows and shoulders, X-rays, bloods || To complete, I would X-ray both hands and check rheumatoid factor and anti-CCP. || ',
    ]),
  ],
  cases=[
    ('Rheumatoid arthritis', 'Symmetrical warm MCP and PIP swelling, ulnar deviation, swan neck, Z-thumb, elbow nodules.', '... **rheumatoid arthritis**: X-rays, RF and anti-CCP, early rheumatology referral for DMARDs.'),
    ('Nodal osteoarthritis', 'Hard Heberden\'s and Bouchard\'s nodes, squaring of the thumb base, cool joints.', '... **nodal osteoarthritis**: analgesia, hand therapy, topical NSAIDs.'),
    ('Carpal tunnel syndrome', 'Thenar wasting, weak thumb abduction, positive Phalen\'s and Tinel\'s.', '... **carpal tunnel syndrome**.'),
    ('Dupuytren\'s contracture', 'Thickened cord in the palm pulling the ring finger into flexion.', '... **Dupuytren\'s contracture**; ask about alcohol, diabetes and family history.'),
    ('Psoriatic arthritis', 'Nail pitting, onycholysis, swollen DIP joints, sausage-shaped finger.', '... **psoriatic arthritis**.'),
  ])

station('E-knee', 'ex', 'MSK: knee examination', 'Surgery', ffp='MSK Knee', u=[86, 87],
  door=DOOR.format(who='A 66-year-old woman has had a painful right knee for 2 years.', sys='knee'),
  hooks=MSK_HOOKS[:1] + [
    '**Small effusion = sweep test; big effusion = patellar tap.**',
    '**ACL = anterior drawer and Lachman\'s,** Lachman\'s is the more sensitive. A pop, then swelling within hours = blood in the joint.',
    '**Valgus stress = MCL; varus stress = LCL,** at 20 to 30 degrees of bend.',
    '**Joint line tenderness + locking = meniscus.**',
    '**Knee pain in a child: examine the hip.**',
  ],
  money='On examination of this lady\'s right knee, she walked with an antalgic gait. There was a varus deformity and quadriceps wasting. There was a small effusion on the sweep test and medial joint line tenderness. Flexion was reduced to 90 degrees with crepitus. The ligaments were stable. These findings are consistent with **osteoarthritis of the right knee**. I would like to examine the hip and request a **weight-bearing X-ray**.',
  traps=['Not checking for an effusion', 'Sitting on the foot for the drawer test without asking', 'Not offering to examine the hip'],
  dg=['msk', 'knee'],
  secs=[
    ('Look', [
      PAIN,
      'Standing: varus or valgus, quadriceps wasting, swelling, scars, a Baker\'s cyst behind; gait || Could you walk to the door and back? || A midline scar = replacement.',
      'Lying: compare both sides || || ',
    ]),
    ('Feel', [
      'Temperature compared with the other knee || || ',
      '!Effusion: sweep test, then patellar tap || || ',
      'Knee bent to 90 degrees: joint lines, patella borders, tibial tuberosity, popliteal fossa || || Tibial tuberosity pain in a teenager = Osgood-Schlatter.',
    ]),
    ('Move', [
      '!Active flexion and extension; passive with a hand on the patella for crepitus; check for a fixed flexion deformity || Slide your heel up to your bottom, then straighten it. || ',
    ]),
    ('Special tests', [
      'Collateral ligaments: valgus and varus stress at 20 to 30 degrees || || ',
      '!Posterior sag first, then anterior and posterior drawer at 90 degrees; Lachman\'s at 20 to 30 degrees || Is it OK if I sit gently on your foot to keep it still? || Look for the sag first or a PCL tear fakes a positive anterior drawer.',
      'Say McMurray\'s for the meniscus, done gently if indicated || || ',
    ]),
    ('Finish and complete', [
      '!Complete: hip examination, neurovascular status, X-ray || To complete my examination I would examine the hip, check the foot pulses and sensation, and request a weight-bearing X-ray. || ',
    ]),
  ],
  cases=[
    ('Knee osteoarthritis', 'Varus deformity, crepitus, medial joint line tenderness, reduced flexion, bony swelling.', '... **knee osteoarthritis**: weight loss, quadriceps strengthening, analgesia; joint replacement if severe.'),
    ('ACL rupture', 'Twisting injury with a pop, rapid swelling, positive Lachman\'s and anterior drawer.', '... an **ACL rupture**: MRI and orthopaedic referral; physiotherapy or reconstruction.'),
    ('Meniscal tear', 'Medial joint line tenderness, locking episodes, small effusion.', '... a **medial meniscal tear**: MRI; arthroscopy if it locks.'),
    ('Septic arthritis', 'Hot, red, swollen knee, fever, unable to bend it at all.', '... **septic arthritis until proven otherwise**: aspirate before antibiotics, blood cultures, urgent orthopaedics.'),
  ])

station('E-shoulder', 'ex', 'MSK: shoulder examination', 'Surgery', ffp='MSK Shoulder', u=[86],
  door=DOOR.format(who='A 52-year-old woman with diabetes cannot reach up to brush her hair.', sys='shoulder'),
  hooks=MSK_HOOKS[:1] + [
    '**Frozen shoulder freezes external rotation first, actively AND passively.** A cuff tear loses active movement but passive is full.',
    '**Painful arc 60 to 120 degrees = impingement of the cuff.** Painful only at the very top = ACJ.',
    '**Cuff tests:** empty can = supraspinatus; resisted external rotation = infraspinatus; lift-off = subscapularis.',
    '**Shoulder pain can come from the neck,** so always examine the cervical spine.',
  ],
  money='On examination of this lady\'s right shoulder, there was no wasting or deformity. There was no tenderness. Active and passive movements were globally restricted, most markedly external rotation. These findings are consistent with **adhesive capsulitis**, frozen shoulder, which is more common with diabetes. I would examine the neck, request an X-ray to exclude arthritis, and offer analgesia, physiotherapy and possibly a steroid injection.',
  traps=['Not comparing active with passive movement', 'Forgetting the cervical spine', 'Not looking from behind for wasting and winging'],
  dg=['msk', 'shoulder'],
  secs=[
    ('Look', [
      PAIN,
      'Front, side and behind: asymmetry, wasting above and below the scapular spine, scars, a step at the ACJ, winging || Could you push against the wall for me? || Wasting above the spine of the scapula = supraspinatus.',
    ]),
    ('Feel', [
      'From the middle out: sternoclavicular joint, clavicle, ACJ, acromion, coracoid, spine of the scapula; temperature || || ',
    ]),
    ('Move', [
      '!Active then passive: flexion, extension, abduction watching for a painful arc, adduction || Raise your arms out to the side and over your head. Tell me where it hurts. || ',
      '!External rotation with the elbows tucked in at 90 degrees; internal rotation, hand up the back || Elbows in at your sides, and turn your hands outwards. || External rotation is the movement that tells you frozen shoulder.',
    ]),
    ('Special tests', [
      'Rotator cuff: empty can, resisted external rotation, lift-off || Arms out, thumbs down, push up against me. || ',
      'Impingement: Hawkins-Kennedy || || Pain when the flexed arm is turned in = impingement.',
      'Function: hands behind the head, hands behind the back || || ',
    ]),
    ('Finish and complete', [
      '!Complete: cervical spine and elbow, neurovascular check including the regimental badge area, X-ray || To complete, I would examine the neck and elbow, check the axillary nerve, and request an X-ray. || ',
    ]),
  ],
  cases=[
    ('Frozen shoulder', 'Global restriction of active and passive movement, external rotation worst, in a diabetic.', '... **adhesive capsulitis**: analgesia, physiotherapy, steroid injection; resolves over 1 to 3 years.'),
    ('Supraspinatus impingement', 'Painful arc 60 to 120 degrees, pain on empty can, positive Hawkins-Kennedy.', '... **subacromial impingement with supraspinatus tendinopathy**: physiotherapy, injection.'),
    ('Rotator cuff tear', 'Can\'t lift the arm actively but full passive range, weak empty can, wasting.', '... a **rotator cuff tear**: ultrasound or MRI and orthopaedic referral.'),
    ('ACJ arthritis', 'Tender ACJ with a bony bump, pain at the top of abduction, positive scarf test.', '... **ACJ osteoarthritis**.'),
  ])

station('E-hip', 'ex', 'MSK: hip examination', 'Surgery', ffp='MSK Hip', u=[86, 87],
  door=DOOR.format(who='A 71-year-old man has a painful right hip and struggles to put his socks on.', sys='hip'),
  hooks=MSK_HOOKS[:1] + [
    '**Internal rotation goes first in hip OA.** Check it with the hip and knee at 90 degrees.',
    '**Trendelenburg:** stand on one leg; if the pelvis drops on the opposite side, the abductors on the standing side are weak. **The sound side sags.**',
    '**Thomas\' test:** bend the good hip fully with your hand under the back; if the other thigh lifts, there is a fixed flexion deformity.',
    '**Short, externally rotated leg after a fall = fractured neck of femur.**',
  ],
  money='On examination of this gentleman\'s right hip, he walked with an antalgic gait and had a positive Trendelenburg test on the right. There was apparent shortening of the right leg. Internal rotation was markedly reduced and painful, and Thomas\' test showed a fixed flexion deformity of 15 degrees. These findings are consistent with **osteoarthritis of the right hip**. I would examine the knee and lumbar spine and request an **AP pelvis and lateral hip X-ray**.',
  traps=['Not fixing the pelvis with a hand on the opposite ASIS during abduction', 'Forgetting leg length', 'Not examining the knee and back'],
  dg=['msk', 'hip'],
  secs=[
    ('Look', [
      PAIN,
      'Standing: scars, wasting of the buttock and thigh, posture || || ',
      '!Gait, then Trendelenburg test each side || Could you walk for me? Now stand on your right leg, holding my hands for balance. || ',
      'Lying: position of the leg; measure true and apparent leg length || || True: ASIS to medial malleolus. Apparent: umbilicus to medial malleolus.',
    ]),
    ('Feel', [
      'Greater trochanter tenderness; temperature || || Tender trochanter = trochanteric bursitis, not hip OA.',
    ]),
    ('Move', [
      'Flexion: knee to chest || Bring your knee up to your chest. || ',
      '!Internal and external rotation with hip and knee at 90 degrees || I\'m going to turn your leg in and out. || ',
      'Abduction and adduction with a hand fixing the opposite ASIS || || ',
      'Extension lying on the side or front || || ',
    ]),
    ('Special tests', [
      '!Thomas\' test for fixed flexion deformity || I\'m going to bend your left knee up to your chest. || ',
    ]),
    ('Finish and complete', [
      '!Complete: knee and lumbar spine, neurovascular status, X-ray || To complete, I would examine the knee and lower back and request an X-ray of the pelvis and hip. || ',
    ]),
  ],
  cases=[
    ('Hip osteoarthritis', 'Antalgic gait, positive Trendelenburg, reduced internal rotation, fixed flexion deformity.', '... **hip osteoarthritis**: analgesia, physiotherapy, weight loss; total hip replacement if severe.'),
    ('Total hip replacement', 'Healed posterior scar over the hip, good range of movement.', '... a **previous total hip replacement**; warn against deep bending early on to avoid dislocation.'),
    ('Fractured neck of femur', 'Fall onto the hip, leg shortened and externally rotated, can\'t lift it.', '... a **fractured neck of femur**: analgesia including a fascia iliaca block, X-ray, orthopaedic surgery within 36 hours.'),
    ('Trochanteric bursitis', 'Tender over the greater trochanter, pain lying on that side, full hip movement.', '... **greater trochanteric pain syndrome**.'),
  ])

station('E-breast', 'ex', 'Breast examination', 'Surgery', ffp='Breast', u=[52, 53, 57, 54, 56],
  door=DOOR.format(who='A 42-year-old woman has found a lump in her left breast.', sys='breasts'),
  hooks=[
    '**Chaperone first, then the good side first.**',
    '**Look in 3 positions:** relaxed, hands pressed on the hips, hands behind the head. Each one shows tethering in a new way.',
    '**Every quadrant + the axillary tail + the nipple.** Map lumps like a clock with the distance from the nipple.',
    '**Triple assessment:** examine, image, biopsy. Every new lump gets all three.',
    '**Breast mouse = fibroadenoma:** small, smooth, rubbery and slips away under your fingers in a young woman.',
  ],
  money='On examination of this lady\'s breasts, with a chaperone present, there was asymmetry with skin dimpling over the upper outer quadrant of the left breast on raising the arms. There was a 3 cm hard, irregular, non-tender lump at 2 o\'clock, 4 cm from the nipple, fixed to the skin. There was a hard node in the left axilla. These findings are **highly suspicious of breast cancer**. I would refer her on the **suspected cancer pathway for triple assessment**: clinical examination, mammogram and ultrasound, and core biopsy.',
  traps=['Not offering a chaperone', 'Forgetting the axillary tail', 'Not describing the lump fully: site, size, shape, consistency, fixation', 'Forgetting the nodes'],
  dg=['breast'],
  secs=[
    ('Prepare', [
      '!Introduce, consent, chaperone; expose to the waist; ask about pain and the side of the lump || This examination involves looking at and feeling both breasts. Would you be happy for me to go ahead with a chaperone in the room? || A chaperone is a critical item.',
    ]),
    ('Look', [
      '!Sitting on the edge of the bed: arms relaxed, then pressing on the hips, then hands behind the head || Could you press your hands on your hips for me? Now put your hands behind your head. || Tethering and dimpling show up when the muscles tense.',
      'Asymmetry, skin dimpling, peau d\'orange, redness, nipple inversion, discharge, Paget\'s eczema of the nipple, scars || || ',
    ]),
    ('Feel', [
      '!Lying at 45 degrees, hand behind the head on the side being examined; the normal side first || || ',
      '!Flat of the fingers, all 4 quadrants and the axillary tail, then behind the nipple || || A system, such as clock face or vertical strips, means nothing is missed.',
      '!Describe any lump: site by the clock, distance from the nipple, size, shape, consistency, mobility, fixation to skin or muscle, tenderness || Press your hands into your hips again for me. || Fixed when the muscle is tensed = attached to the chest wall.',
      'Ask the patient to express any nipple discharge herself || || ',
    ]),
    ('Nodes', [
      '!Axilla: take the weight of her arm, feel the 5 groups; then supraclavicular and cervical nodes || Let me hold the weight of your arm. || ',
    ]),
    ('Finish and complete', [
      '!Complete: triple assessment, referral on the suspected cancer pathway for any concerning lump || To complete, I would arrange triple assessment: imaging and a core biopsy. || NICE: unexplained lump in a woman aged 30 or over = suspected cancer pathway.',
    ]),
  ],
  cases=[
    ('Breast cancer', 'Hard irregular fixed lump, skin tethering, axillary node.', '... **suspicious of breast cancer**: suspected cancer pathway for triple assessment.'),
    ('Fibroadenoma', 'Smooth, mobile, rubbery 2 cm lump in a 22-year-old.', '... most likely a **fibroadenoma**: triple assessment with ultrasound; reassure.'),
    ('Breast cyst', 'Smooth, fluctuant, well-defined lump in a 45-year-old.', '... likely a **breast cyst**: ultrasound and aspiration.'),
    ('Breast abscess', 'Hot, red, tender fluctuant swelling in a breastfeeding mother with fever.', '... a **breast abscess**: antibiotics, ultrasound-guided aspiration; keep breastfeeding or expressing.'),
  ])

station('E-scrotal', 'ex', 'Testicular examination', 'Surgery', ffp='Testicular', u=[84, 81, 82, 83, 58],
  door=DOOR.format(who='A 28-year-old man has noticed a lump in his scrotum.', sys='testes'),
  hooks=[
    '**Three questions decide every scrotal lump:** Can I get above it? Is it separate from the testis? Does it light up?',
    '**Can\'t get above = inguinal hernia.** **In the testis, hard, doesn\'t light up = cancer until proven otherwise.**',
    '**Lights up and separate = epididymal cyst. Lights up and surrounds the testis = hydrocele.**',
    '**Bag of worms, left side, disappears lying down = varicocele.**',
    '**Sudden pain + high-riding testis + no cremasteric reflex = torsion:** theatre now, within 6 hours.',
  ],
  money='On examination of this gentleman\'s scrotum, with a chaperone, the left testis had a 1 cm hard, irregular, non-tender lump arising from the testis. I could get above it and it did not transilluminate. The epididymis and cord were normal and there were no inguinal nodes. These findings are **suspicious of a testicular tumour**. I would arrange an **urgent scrotal ultrasound and tumour markers: AFP, beta-hCG and LDH**, and refer on the suspected cancer pathway.',
  traps=['No chaperone', 'Not asking whether you can get above the lump', 'Forgetting to transilluminate', 'Saying the testis drains to the inguinal nodes: it drains to the para-aortic nodes'],
  dg=['scrotum'],
  secs=[
    ('Prepare', [
      '!Consent and chaperone; expose from the umbilicus to the knees; examine standing, then lying || This involves looking at and feeling your testicles. Is that OK, with a chaperone present? || ',
    ]),
    ('Look', [
      'Skin, swelling, symmetry, the lie of each testis, scars || || A high, horizontal lie suggests torsion.',
    ]),
    ('Feel', [
      '!Normal side first; each testis between thumb and two fingers: size, consistency, lumps || Tell me if anything is tender. || ',
      'Epididymis behind the testis; spermatic cord with the vas like a piece of string || || ',
      '!Any swelling: can you get above it, is it separate from the testis, is it tender || || ',
      '!Transilluminate with a pen torch in a dim room || || Fluid lights up; solid tissue doesn\'t.',
      'Cough impulse; varicocele standing and with straining || Could you turn your head and cough? || ',
    ]),
    ('Finish and complete', [
      '!Complete: abdominal examination for para-aortic nodes, urgent ultrasound, tumour markers || To complete, I would examine the abdomen and arrange an urgent ultrasound and tumour markers. || ',
    ]),
  ],
  cases=[
    ('Testicular cancer', 'Hard, irregular, painless lump in the testis, not transilluminating.', '... **testicular tumour until proven otherwise**: urgent ultrasound, AFP, beta-hCG, LDH.'),
    ('Hydrocele', 'Smooth swelling around the testis that transilluminates; the testis can\'t be felt separately.', '... a **hydrocele**: ultrasound to check the testis beneath.'),
    ('Epididymal cyst', 'Smooth lump above and behind the testis, separate from it, transilluminates.', '... an **epididymal cyst**: reassure.'),
    ('Varicocele', 'Left-sided bag of worms when standing that empties lying down.', '... a **varicocele**; a new right-sided or non-emptying one needs a renal ultrasound.'),
    ('Testicular torsion', 'Sudden severe pain, high-riding horizontal testis, absent cremasteric reflex.', '... **testicular torsion**: emergency surgical exploration, don\'t wait for imaging.'),
    ('Inguinal hernia', 'Can\'t get above the swelling, cough impulse present.', '... an **inguinoscrotal hernia**.'),
  ])

station('E-dre', 'ex', 'Digital rectal examination', 'Surgery', ffp='DRE', u=[75, 76, 35, 33, 38],
  door='You are an FY1. A 72-year-old man has a weak stream and gets up 3 times a night to pass urine. Perform a digital rectal examination on the model, then present your findings to the examiner.',
  hooks=[
    '**Consent, chaperone, left lateral with the knees up to the chest.**',
    '**Look, lubricate, warn, then slowly in.** Sweep 360 degrees; the prostate is at 12 o\'clock in a man.',
    '**The prostate story:** normal is walnut-sized, smooth and rubbery with a central groove. **BPH = big and smooth. Cancer = hard, craggy, groove lost.**',
    '**Always look at the glove:** blood, mucus, melaena, stool colour.',
  ],
  money='On digital rectal examination, with a chaperone, the perianal skin was normal. Anal tone was normal. The prostate was enlarged, about 3 finger breadths, smooth and rubbery, with a preserved median sulcus and no nodules. There was no blood or mucus on the glove. These findings are consistent with **benign prostatic hyperplasia**. I would request a **PSA after counselling**, a urine dip, U&Es and a bladder scan.',
  traps=['No chaperone or consent', 'Forgetting to inspect before inserting the finger', 'Not looking at the glove', 'Forgetting to offer tissues and privacy afterwards'],
  dg=['dre'],
  secs=[
    ('Prepare', [
      '!Explain, consent, chaperone || I would like to examine your back passage by inserting a gloved, lubricated finger. It may be uncomfortable but it shouldn\'t hurt. Is that OK? We will have a chaperone. || ',
      'Lie on the left side, knees drawn up, bottom at the edge of the bed || Could you lie on your left side and bring your knees up towards your chest? || ',
    ]),
    ('Look', [
      'Part the buttocks: skin tags, haemorrhoids, fissure, fistula, warts, blood, rashes || || ',
      'Ask him to bear down || || Prolapsing piles or rectum show on straining.',
    ]),
    ('Feel', [
      '!Lubricate, warn, insert the finger slowly with the pad facing back || You\'ll feel me touch now. || ',
      'Tone: ask him to squeeze your finger; sensation || Squeeze my finger. || Reduced tone with saddle numbness = cauda equina.',
      '!Sweep 360 degrees for masses; feel the prostate at 12 o\'clock: size, consistency, surface, sulcus, tenderness || || ',
      '!Withdraw and inspect the glove || || ',
    ]),
    ('Finish', [
      'Wipe, offer tissues, give privacy to dress; document with the chaperone\'s name || Here are some tissues. I\'ll give you some privacy to get dressed. || ',
      '!Complete: abdominal examination, urine dip, PSA with counselling, bladder scan || || ',
    ]),
  ],
  cases=[
    ('Benign prostatic hyperplasia', 'Smooth, enlarged, rubbery prostate with a central groove.', '... **BPH**: PSA with counselling, urine dip, U&Es, bladder scan; tamsulosin, finasteride if large.'),
    ('Prostate cancer', 'Hard, irregular, craggy prostate with the median groove lost.', '... **suspicious of prostate cancer**: PSA, suspected cancer pathway, MRI prostate.'),
    ('Rectal cancer', 'Hard irregular mass on the rectal wall with blood on the glove.', '... a **rectal mass**: suspected cancer pathway for colonoscopy.'),
    ('Cauda equina', 'Reduced anal tone and perianal numbness.', '... findings of **cauda equina syndrome**: emergency MRI.'),
  ])

station('E-genit', 'ex', 'External genitalia examination', 'Surgery', ffp='External Genitalia', u=[81, 84, 82, 58],
  door='You are an FY1. A 35-year-old man has a sore area on his penis. Examine the external genitalia on the model, then present your findings to the examiner.',
  hooks=[
    '**Retract AND replace:** pull the foreskin back to see the glans, then always put it back. Forgetting causes paraphimosis.',
    '**Systematic sweep:** groin → penis → glans and meatus → scrotum → testes → perineum.',
    '**Painless ulcer = syphilis until proven otherwise. Painful ulcers = herpes.**',
    '**The scrotal skin drains to the inguinal nodes; the testis drains to the para-aortic nodes.**',
  ],
  money='On examination of this gentleman\'s external genitalia, with a chaperone present, there was no inguinal lymphadenopathy or hernia. There were multiple small painful ulcers on the glans with surrounding redness. The foreskin retracted and was replaced. There was no discharge. Both testes were normal. These findings are consistent with **genital herpes**. I would take a **viral swab**, offer a full sexual health screen, and start aciclovir.',
  traps=['Not replacing the foreskin', 'No chaperone', 'Forgetting the inguinal nodes and hernial orifices', 'Not offering a full sexual health screen'],
  dg=['genit'],
  secs=[
    ('Prepare', [
      '!Consent, chaperone, gloves; expose from the umbilicus to the knees || I need to look at and feel your genital area. Is that OK, with a chaperone present? || ',
    ]),
    ('Groin', [
      'Inspect and feel the inguinal region for lumps and nodes; cough impulse || || ',
    ]),
    ('Penis', [
      'Inspect the shaft: ulcers, warts, rashes, lumps || || ',
      '!Retract the foreskin, or ask the patient to; inspect the glans and the meatus for discharge and hypospadias || Could you pull back your foreskin for me? || ',
      '!Replace the foreskin || And could you put it back for me now? || A critical safety item.',
    ]),
    ('Scrotum and testes', [
      'Inspect the scrotum, then feel each testis, epididymis and cord || || ',
    ]),
    ('If the model is female', [
      'Inspect the vulva, labia, clitoris and introitus with good light: ulcers, warts, discharge, swelling; ask her to cough for prolapse; Bartholin\'s glands || || A speculum examination would follow if indicated.',
    ]),
    ('Finish and complete', [
      '!Complete: swabs, urine, sexual health screen including HIV and syphilis serology || To complete, I would take swabs and offer a full sexual health screen. || ',
    ]),
  ],
  cases=[
    ('Genital herpes', 'Multiple painful shallow ulcers with tender inguinal nodes.', '... **genital herpes**: viral swab, aciclovir, sexual health screen.'),
    ('Primary syphilis', 'Single painless, clean, firm ulcer with rubbery inguinal nodes.', '... a **chancre**: syphilis serology, refer to sexual health, benzathine penicillin.'),
    ('Genital warts', 'Small soft cauliflower-like lumps on the shaft.', '... **anogenital warts**: topical treatment or cryotherapy; screen for other infections.'),
    ('Phimosis or paraphimosis', 'Tight foreskin that can\'t retract, or a retracted foreskin stuck behind a swollen glans.', '... **paraphimosis is an emergency**: reduce it with analgesia and compression.'),
  ])
