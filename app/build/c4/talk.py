from .common import station, V

# ---------------- Communication ----------------
station('C-bbn', 'comm', 'Breaking bad news: SPIKES', 'Communication', ffp='Breaking Bad News (SPIKES)', u=[21, 77, 57],
  door='You are an FY1. The patient is here for the result of a recent scan. Your consultant has asked you to break the news and explain the next steps. A specialist nurse is available.',
  hooks=[
    '**SPIKES:** Setting → Perception → Invitation → Knowledge → Emotions → Strategy and Summary.',
    '**Warning shot, then the word, then silence.** "I\'m afraid the scan shows something serious." Pause. "It shows a cancer." Pause.',
    '**Say the word cancer.** Euphemisms like "a growth" leave people unsure.',
    '**Let the silence do the work.** Count to 10 before you speak again.',
    '**Name the emotion:** "I can see this is a huge shock."',
  ],
  money='I\'m afraid the scan has shown something serious. There\'s a **mass in your lung, and it looks like a cancer**. *Pause.* I\'m so sorry; I can see this is a shock. *Pause.* We don\'t yet know what type it is or whether it has spread, so the next step is a **biopsy and more scans**. Your case will be discussed by a team of specialists to plan the best treatment, and a **specialist nurse** will be your point of contact. You won\'t be on your own with this.',
  traps=['Jumping straight to the result without checking what they know', 'Using euphemisms or jargon', 'Talking through the silence', 'Leaving without a clear next step and contact'],
  dg=['spikes'],
  vars=[
    V('A', 'Peter, 66, retired lorry driver', 'Lung cancer on CT chest',
      ['You had a cough for 3 months and coughed up some blood. You had a CT scan last week.', 'You have come alone; your wife is at work.', 'ONLY IF ASKED: you think it might be "just an infection".', 'When you hear the news, go quiet, then ask "Am I going to die?"', 'ONLY IF ASKED: your brother died of lung cancer within 3 months, so you are terrified.'],
      'CT chest: a 4 cm spiculated mass in the right upper lobe with enlarged mediastinal nodes, suspicious of lung cancer. No biopsy yet.',
      'Sets up: private, sits, phone away, asks if he wants someone with him; checks what he knows; warning shot; says the word cancer; silence; responds to emotion; honest that the type and spread are unknown; next steps: biopsy, PET-CT, MDT, lung cancer nurse; answers "am I going to die" honestly without false hope or a timescale; written information; follow-up date; who to contact.'),
    V('B', 'Anne, 58', 'Bladder cancer on cystoscopy',
      ['You had blood in your urine and a camera test.', 'You brought your husband.', 'ONLY IF ASKED: you are a carer for your mother and worry who will look after her.'],
      'Flexible cystoscopy: a papillary tumour in the bladder; biopsy confirmed urothelial cancer.',
      'SPIKES; plain words; next steps: TURBT and staging; specialist nurse; explores the caring worry and offers social support.'),
  ],
  ask=['Am I going to die?', 'How long have I got?', 'Is it my fault for smoking?'],
  secs=[
    ('S: Setting', [
      '!Private room, sitting, phone or bleep silenced, tissues; offer someone to be with them || Before we start, would you like anyone with you? || ',
    ]),
    ('P: Perception', [
      '!Find out what they know and expect || Can you tell me what you understand about why you had the scan? || You pitch the news from their starting point.',
    ]),
    ('I: Invitation', [
      'Ask how much detail they want || I have the results here. Would it be OK if I went through them with you? || ',
    ]),
    ('K: Knowledge', [
      '!Warning shot, then the news in plain words, including the word cancer || I\'m afraid the results are not what we hoped. ... It shows a cancer. || ',
      '!Pause and allow silence || || ',
    ]),
    ('E: Emotions', [
      '!Recognise and name the emotion; empathic response; allow tears || I can see this is a terrible shock. || ',
      'Answer difficult questions honestly; don\'t give a timescale you don\'t know || I wish I could tell you more right now. Once we have the biopsy results, the specialists can give you a much clearer picture. || ',
    ]),
    ('S: Strategy and summary', [
      '!Next steps: tests, MDT, specialist nurse, follow-up date || || ',
      '!Summarise, check understanding, written information, who to contact, safety-net || || ',
    ]),
  ])

station('C-expl', 'comm', 'Explaining a diagnosis', 'Communication', ffp='Explaining a diagnosis', u=[67, 15, 41, 29],
  door='You are an FY1 in general practice. The patient has come back for the result of their tests. Explain the diagnosis and the plan.',
  hooks=[
    '**Ask, Tell, Ask:** find out what they know, tell one chunk, check they\'ve got it.',
    '**Chunk and check:** 2 or 3 facts at a time, then "Does that make sense so far?"',
    '**What it is → why it happens → what it means for you → what happens next → what you can do → when to worry.**',
    '**Draw it.** A quick sketch beats a paragraph.',
    '**Teach-back at the end:** "Could you tell me in your own words what you\'ll tell your family?"',
  ],
  money='Your blood test shows you have **type 2 diabetes**. *Pause.* That means your body isn\'t using its **insulin** properly, so sugar builds up in your blood instead of going into your muscles for energy. *Check.* Over years, high sugar can damage the **eyes, kidneys, nerves and heart**, which is why getting it under control now matters. The good news is there\'s a lot you can do: **diet, activity and weight**, and a tablet called **metformin**. Could you tell me in your own words what diabetes is, so I know I\'ve explained it clearly?',
  traps=['Launching into an explanation without asking what they know', 'Jargon', 'Lecturing without checking', 'No teach-back or safety-net'],
  dg=['chunk'],
  vars=[
    V('A', 'Priya, 52', 'New type 2 diabetes: HbA1c 58',
      ['You had a blood test at a health check.', 'ONLY IF ASKED: your mum had diabetes and lost a leg; you are frightened.', 'You think diabetes is caused by eating too much sugar.'],
      'HbA1c 58 mmol/mol on two occasions.',
      'Checks knowledge; explains diabetes simply, with insulin as a key; addresses the leg amputation fear: good control prevents it, annual foot checks; why it matters; lifestyle; metformin; structured education such as DESMOND; eye screening; teach-back.'),
    V('B', 'Tom, 19', 'Asthma diagnosed on spirometry and FeNO',
      ['You have had a cough at night and wheeze with exercise.', 'ONLY IF ASKED: you want to join the army and worry asthma will stop you.'],
      'Spirometry with 15% reversibility; FeNO 55 ppb.',
      'Explains asthma as sensitive, swollen airways; triggers; preventer and reliever; action plan; honest that armed forces entry rules vary and to check; teach-back.'),
    V('C', 'Linda, 45', 'Gallstones causing biliary colic',
      ['You get pain under your right ribs after fatty food that lasts an hour or two.', 'ONLY IF ASKED: you are worried it is cancer like your sister had.'],
      'Ultrasound: multiple gallstones, no gallbladder wall thickening, normal bile duct.',
      'Explains gallstones with a drawing; why fatty food triggers pain; not cancer; options: laparoscopic removal of the gallbladder; red flags: fever, jaundice, pain over 6 hours → urgent.'),
    V('D', 'Jake, 28', 'Irritable bowel syndrome',
      ['You have bloating, cramps and alternating bowel habit for a year; tests are normal.', 'ONLY IF ASKED: you feel nobody believes you and think it might be in your head.'],
      'FBC, CRP, coeliac serology and faecal calprotectin all normal.',
      'Validates that it is real; explains a sensitive gut and gut-brain link; normal tests reassure; diet: regular meals, fibre, low FODMAP with a dietitian; stress; medicines for symptoms; red flags: blood, weight loss, over 60 change → return.'),
  ],
  ask=['Is it my fault?', 'Will it go away?', 'Do I need to tell work?'],
  secs=[
    ('Start', [
      '!Find out what they know and what they are worried about || Before I explain, what have you been thinking might be going on? || ',
      'Signpost || I\'d like to explain what the test shows, then we can talk about what happens next. Is that OK? || ',
    ]),
    ('Explain in chunks', [
      '!Name the diagnosis in plain words || || ',
      '!What it is and why it happens, with an analogy or a drawing || || ',
      '!Check after each chunk || Does that make sense so far? || ',
      'What it means for them: work, family, driving, future || || ',
    ]),
    ('Plan', [
      '!What happens next: tests, treatment, referrals || || ',
      'What they can do themselves || || ',
    ]),
    ('Close', [
      '!Address their specific worry || || The hidden worry is usually a scored item.',
      '!Teach-back, leaflet, follow-up, safety-net || Could you tell me in your own words what you\'ll tell your family? || ',
    ]),
  ])

station('C-abx', 'comm', 'Antibiotic stewardship', 'Communication', ffp='Antibiotic Stewardship', u=[151, 18, 149, 150],
  door='You are an FY1 in general practice. The patient has a respiratory tract infection and is asking for antibiotics. You have examined them; the findings are on the card. Discuss the management.',
  hooks=[
    '**It\'s real, it\'s a virus, here\'s how to feel better, here\'s when to come back.**',
    '**Ask why they want antibiotics first:** a work deadline, a past experience, a fear of pneumonia.',
    '**How long it lasts:** ear infection about 3 days to a week; sore throat about a week; sinusitis 2 to 3 weeks; cough up to 3 weeks; cold about 10 days.',
    '**Antibiotics:** don\'t work on viruses; cause diarrhoea, thrush and rashes; make bacteria in your body resistant for months.',
    '**Back-up prescription:** collect it if not better by a set day or if worse.',
  ],
  money='From what you\'ve told me and from examining you, this looks like a **viral sore throat**. Antibiotics only work on bacteria, so they **wouldn\'t make you better faster**, but they can cause **diarrhoea, thrush or a rash**, and they make the bugs in your body more resistant. A sore throat like this usually lasts **about a week**. **Paracetamol or ibuprofen, fluids and rest** will help most. If you\'re **not improving in 3 days**, or get worse, or have trouble swallowing or breathing, come back or call 111.',
  traps=['Refusing without exploring why they want antibiotics', 'Not giving the expected duration', 'No self-care plan', 'No safety-net or back-up option'],
  dg=['abxdays'],
  vars=[
    V('A', 'Chris, 28, sales manager', 'Viral sore throat, FeverPAIN 1',
      ['Sore throat for 2 days, runny nose and cough.', 'You have a big presentation in 3 days and want antibiotics to be well for it.', 'ONLY IF ASKED: last time you had a sore throat, antibiotics "cleared it up in a day".', 'You are not allergic to anything.'],
      'Temperature 37.6. Tonsils mildly red, no exudate, no tender nodes. Cough and coryza present. FeverPAIN score 1.',
      'Explores ICE including the presentation; explains FeverPAIN 1 means a virus is most likely; no antibiotics; why: side effects and resistance; expected duration about a week; self-care: paracetamol, ibuprofen, salt water gargles, lozenges; safety-net: drooling, can\'t swallow, breathing difficulty, one-sided severe pain or not improving in 3 to 5 days; TARGET leaflet.'),
    V('B', 'Megan, 34, mother of Ruby, 3', 'Child with acute otitis media',
      ['Ruby has had ear pain and a temperature for a day. She is eating and drinking.', 'ONLY IF ASKED: you are worried she will go deaf.'],
      'Ruby: temperature 38.1, red bulging right drum, no discharge, alert and playful.',
      'Explains most ear infections clear in 3 days; antibiotics make little difference; paracetamol or ibuprofen; back-up prescription to collect if not better in 3 days or worse; hearing returns; red flags: very unwell, discharge, swelling behind the ear, drowsy.'),
    V('C', 'Graham, 45', 'Acute cough for 10 days',
      ['You have a cough for 10 days with green phlegm. You feel tired but OK.', 'ONLY IF ASKED: you think green phlegm means you need antibiotics.'],
      'Temperature 37.2, sats 98%, respiratory rate 16, chest clear.',
      'Explains green phlegm doesn\'t mean bacteria; cough lasts up to 3 weeks; honey and lemon; no antibiotics; safety-net: breathlessness, chest pain, coughing blood, fever, over 3 weeks → return.'),
  ],
  ask=['But I always get antibiotics.', 'What if it turns into something worse?', 'Can I have them just in case?'],
  secs=[
    ('Explore', [
      '!Ideas, concerns and expectations: why they want antibiotics || What were you hoping we could do today? Is there something in particular that\'s worrying you? || ',
    ]),
    ('Explain', [
      '!The likely cause and the score || This is most likely a virus, which is what causes most sore throats. || ',
      '!Why antibiotics wouldn\'t help: viruses, side effects, resistance || || ',
      '!How long it usually lasts || || Telling them the expected duration reduces reconsultation.',
    ]),
    ('Plan', [
      '!Self-care: paracetamol or ibuprofen, fluids, rest, gargles, honey || || ',
      'Back-up prescription when appropriate || || ',
      'Address their specific worry, such as work || || ',
    ]),
    ('Safety-net', [
      '!Specific red flags, when to return, and a leaflet || If you can\'t swallow your saliva, struggle to breathe, or it isn\'t improving in 3 days, come back or call 111. || ',
    ]),
  ])

# ---------------- Psychiatry ----------------
station('Y-mhx', 'psych', 'Mental health history', 'Psychiatry', ffp='Mental Health History', u=[102, 104, 100, 103, 110],
  door='You are an FY1 in general practice. Take a psychiatric history from this patient, then present your summary, likely diagnosis and risk to the examiner.',
  hooks=[
    '**Their story → mood → anxiety → psychosis → substances → risk → their life story.**',
    '**Depression core 3:** low mood, loss of interest, low energy, for 2 weeks or more. Then the biology: sleep, appetite, weight, concentration, libido.',
    '**Ask about suicide directly.** Asking does not put the idea into someone\'s head.',
    '**Screen for mania and psychosis even when it looks like depression:** it changes the treatment.',
    '**Life story:** childhood, school, work, relationships, housing, money, forensic history, and who supports them.',
  ],
  money='Ms Patel is a 32-year-old teacher with **6 weeks of low mood, loss of interest and poor energy**, with early waking, poor appetite and weight loss, following her divorce. She has **passive thoughts of death but no plans or intent**, and her children are protective. There are no psychotic or manic features. She drinks 2 glasses of wine nightly. The most likely diagnosis is a **moderate depressive episode**. Her risk is currently **low to moderate**. I would offer **talking therapy and an SSRI**, a safety plan and review in 2 weeks.',
  traps=['Not asking about suicide directly', 'Forgetting to screen for mania and psychosis', 'Not asking about alcohol and drugs', 'No risk summary at the end'],
  dg=['mhx'],
  vars=[
    V('A', 'Ms Patel, 32, teacher', 'Moderate depressive episode',
      ['Low mood for 6 weeks since your divorce; you have stopped enjoying painting.', 'You wake at 4am and can\'t get back to sleep; poor appetite; lost half a stone.', 'ONLY IF ASKED: you sometimes think you would be better off not waking up, but you would never do anything because of your children.', 'You drink 2 glasses of wine every night to sleep.', 'No voices; no periods of very high mood.'],
      '', 'Systematic history; core and biological symptoms; duration; trigger; screens anxiety, psychosis, mania; alcohol; direct suicide questions; protective factors; PMH, drug history, family history, personal and social history; presents: moderate depression, risk low to moderate, management: NHS Talking Therapies, SSRI, safety plan, review.'),
    V('B', 'Dan, 23, student', 'Generalised anxiety disorder',
      ['You worry constantly about everything: exams, money, your health; it is hard to switch off.', 'You get headaches, tense shoulders, poor sleep, and feel on edge.', 'ONLY IF ASKED: you have panic attacks before exams.', 'You drink 6 energy drinks a day.'],
      '', 'Anxiety symptoms for over 6 months; panic; caffeine; screens depression and risk; presents GAD; management: self-help, CBT, SSRI.'),
    V('C', 'Kayleigh, 26', 'Bipolar disorder: a manic episode',
      ['You have barely slept for a week but feel full of energy and brilliant ideas.', 'You have spent £3,000 on a business plan.', 'Talk fast and jump between topics.', 'ONLY IF ASKED: you had a very low period last year.'],
      '', 'Picks up pressured speech; screens mania: sleep, energy, spending, grandiosity, risk-taking; past depression; presents probable bipolar affective disorder, manic episode; urgent psychiatry referral; avoid antidepressants alone.'),
  ],
  ask=['Do you think I\'m going mad?', 'Will I have to take tablets?', 'Will this affect my job?'],
  secs=[
    ('Open', [
      '!Open question and listen; acknowledge it can be hard to talk about || What\'s been happening? Take your time. || ',
    ]),
    ('Presenting complaint', [
      '!Mood, interest, energy, and how long || How has your mood been? Are you still enjoying things you used to? || ',
      '!Biological symptoms: sleep, appetite, weight, concentration, libido || How are you sleeping? || ',
      'Triggers and what has been happening in their life || || ',
    ]),
    ('Screen the rest', [
      '!Anxiety and panic || || ',
      '!Psychosis: voices, unusual beliefs, feeling watched || Sometimes when people are stressed they hear things others can\'t. Has anything like that happened to you? || ',
      '!Mania: periods of very high mood or energy, little sleep, overspending || || ',
      'OCD and trauma symptoms || || ',
    ]),
    ('Substances', ['!Alcohol in units, drugs, smoking || || ']),
    ('Risk', [
      '!Suicide: thoughts, plans, intent, preparations, protective factors || Have things ever got so bad that you\'ve thought about ending your life? || ',
      'Risk to others; risk from others; self-neglect || || ',
    ]),
    ('Background', [
      'Past psychiatric history, medications, allergies, medical history || || ',
      'Family history of mental illness and suicide || || ',
      'Personal and social history: childhood, work, relationships, housing, money, forensic, support || || ',
    ]),
    ('Present to the examiner', [
      '!Summary, likely diagnosis, risk level, and plan || || ',
    ]),
  ])

station('Y-risk', 'psych', 'Risk assessment', 'Psychiatry', ffp='Risk Assessment', u=[100, 102, 109, 116],
  door='You are an FY1 in A&E. The patient has been brought in by the police after an argument with a neighbour. Assess the patient\'s risk, then present your risk assessment and plan to the examiner.',
  hooks=[
    '**Three directions of risk:** to self, to others, from others. Then self-neglect.',
    '**Static vs dynamic:** past history doesn\'t change; current symptoms, drugs and stress do. You treat the dynamic ones.',
    '**Command voices + a named target + access to weapons = high risk to others.**',
    '**Children and dependants:** always ask who is at home. Safeguarding comes first.',
    '**Formulate, don\'t just score:** what, to whom, how likely, how soon, what makes it better or worse.',
  ],
  money='Mr Hughes is a 34-year-old man with **paranoid beliefs that his neighbour is poisoning him** and **second-person command voices** telling him to "sort him out". He has a **history of violence** and keeps a hammer by his door. He has stopped his medication and is using cannabis. He denies thoughts of self-harm. He lives alone with no children. I would assess his risk to **others as high and imminent**. He needs **urgent psychiatric assessment** today; I would inform my senior, ensure staff safety, and consider the Mental Health Act. **Confidentiality may be broken** to protect the neighbour.',
  traps=['Only asking about suicide', 'Missing children or dependants', 'Not asking about weapons and access', 'Not stating a clear risk level and plan'],
  dg=['risk3'],
  vars=[
    V('A', 'Mr Hughes, 34', 'Psychosis with high risk to others',
      ['You believe your neighbour is putting poison through your letterbox. You are angry.', 'You hear a voice telling you to "sort him out".', 'ONLY IF ASKED: you have a hammer by the door "for protection". You hit someone in a fight 5 years ago.', 'You stopped your olanzapine 2 months ago and smoke cannabis daily.', 'You have no thoughts of harming yourself.'],
      '', 'Risk to self, others and from others; command hallucinations; specific target; weapon access; history of violence; non-adherence and cannabis; protective factors; formulates high imminent risk to others; urgent psychiatry, senior, safety, Mental Health Act consideration, confidentiality may be breached.'),
    V('B', 'Jade, 29', 'Depression with domestic abuse and young children',
      ['You feel low and hopeless. You have two children, aged 2 and 5.', 'ONLY IF ASKED: your partner hits you when he drinks and you are scared.', 'ONLY IF ASKED: sometimes you feel you can\'t cope with the children.'],
      '', 'Asks about risk from others: domestic abuse, sensitively and alone; children\'s safety: safeguarding referral; risk to self; formulates; offers domestic abuse support, safety plan, refuge information, safeguarding.'),
  ],
  ask=['Are you going to section me?', 'Will you tell the police?', 'Will social services take my kids?'],
  secs=[
    ('Open and rapport', ['!Explain your role and the limits of confidentiality || What you tell me is confidential, unless I\'m worried about your safety or someone else\'s. || ']),
    ('Current mental state', ['!Mood, psychotic symptoms, command hallucinations, anger || || ']),
    ('Risk to self', ['!Self-harm and suicidal thoughts, plans, intent; self-neglect || || ']),
    ('Risk to others', [
      '!Thoughts of harming anyone, a named person, plans, weapons, past violence || Have you had any thoughts of hurting anyone? || ',
      '!Children and dependants at home || || ',
    ]),
    ('Risk from others', ['!Abuse, exploitation, domestic violence || Is anyone hurting you or making you feel unsafe? || ']),
    ('Context', ['Drugs, alcohol, medication adherence, recent losses, support, protective factors || || ']),
    ('Formulate and plan', [
      '!State the risk: what, to whom, likelihood, how soon || || ',
      '!Plan: senior, psychiatry, safeguarding, Mental Health Act, confidentiality decisions || || ',
    ]),
  ])

# ---------------- Imaging and ECG ----------------
IMG_DOOR = 'You are an FY1. You will be shown {what}. Present it to the examiner systematically, give your diagnosis and the next step.'

station('I-cxr', 'img', 'Chest X-ray interpretation', 'Imaging', ffp='Respiratory CXR', u=[19, 9, 11, 6, 21, 45],
  door=IMG_DOOR.format(what='a chest X-ray'),
  hooks=[
    '**Details → RIPE → ABCDE.**',
    '**Details:** name, date of birth, date, PA or AP, erect or supine.',
    '**RIPE quality:** Rotation, Inspiration of 5 to 6 front ribs, the Picture includes the whole chest, Exposure.',
    '**ABCDE:** Airway, Breathing, Cardiac, Diaphragm, Everything else including bones and lines.',
    '**Heart size is only valid on a PA film:** over half the chest width = cardiomegaly.',
    '**Lose a heart border = the lobe next to it:** right heart border = middle lobe; left heart border = lingula.',
  ],
  money='This is a **PA erect chest X-ray** of John Smith, taken today. It is adequately inspired, not rotated and well exposed. The trachea is central. There is **an area of increased opacification in the right lower zone with air bronchograms**; the right heart border is preserved and the costophrenic angle is clear. The heart is not enlarged. The diaphragm and bones are normal. These findings are consistent with **right lower lobe consolidation**, most likely **pneumonia**. I would calculate **CURB-65** and start antibiotics per local guidance.',
  traps=['Skipping the patient details and film type', 'Jumping to the obvious abnormality before the quality checks', 'Forgetting the review areas: apices, behind the heart, below the diaphragm', 'Not giving a next step'],
  dg=['cxrsys'],
  vars=[
    V('A', 'John Smith, 68', 'Right lower lobe consolidation', [], 'Patchy opacity in the right lower zone with air bronchograms; right heart border preserved.', 'Right lower lobe pneumonia: CURB-65, antibiotics, repeat X-ray in 6 weeks if a smoker over 50.', img={'k': 'cxr', 'a': 'cons'}),
    V('B', 'Mary Jones, 74', 'Left pleural effusion', [], 'Homogeneous opacity at the left base with a meniscus; costophrenic angle lost.', 'Left pleural effusion: ultrasound-guided pleural tap; Light\'s criteria.', img={'k': 'cxr', 'a': 'eff'}),
    V('C', 'Tom Green, 22', 'Right pneumothorax', [], 'Visible lung edge on the right with no lung markings beyond it.', 'Right pneumothorax: if primary, under 2 cm and not breathless, consider conservative management; otherwise aspiration or drain per BTS.', img={'k': 'cxr', 'a': 'ptx'}),
    V('D', 'Ali Khan, 70', 'Pneumoperitoneum', [], 'Crescent of free air under the right hemidiaphragm on an erect film.', 'Free air under the diaphragm = perforated viscus: nil by mouth, IV fluids, antibiotics, urgent surgical review, CT.', img={'k': 'cxr', 'a': 'perf'}),
    V('E', 'Betty White, 81', 'Heart failure', [], 'Cardiomegaly, upper lobe diversion, Kerley B lines, bat-wing shadowing, small effusions.', 'Pulmonary oedema from heart failure: ABCDE of heart failure; sit up, oxygen, IV furosemide, echo.', img={'k': 'cxr', 'a': 'hf'}),
    V('F', 'Ron Black, 66, smoker', 'Lung mass', [], 'A rounded spiculated opacity in the right upper zone with a bulky right hilum.', 'Suspicious of lung cancer: urgent CT chest on the suspected cancer pathway.', img={'k': 'cxr', 'a': 'mass'}),
  ],
  ask=['What would you do next?', 'What are the review areas?', 'How do you know the film is adequate?'],
  secs=[
    ('Details', ['!Name, date of birth, date and time, PA or AP, erect or supine || This is a PA erect chest X-ray of... taken on... || ']),
    ('Quality: RIPE', [
      '!Rotation: spinous processes midway between the clavicle heads || || ',
      '!Inspiration: 5 to 6 anterior ribs above the diaphragm || || ',
      'Picture: whole chest included; Exposure: vertebrae just visible behind the heart || || ',
    ]),
    ('ABCDE', [
      '!Airway: trachea central, carina || || ',
      '!Breathing: lungs zone by zone comparing sides, pleura, costophrenic angles || || ',
      '!Cardiac: size, borders || || ',
      'Diaphragm: shape, free air under it || || ',
      'Everything else: bones, soft tissue, lines and tubes, review areas || || ',
    ]),
    ('Conclude', ['!Diagnosis, differential, next step || These findings are consistent with... I would... || ']),
  ])

station('I-axr', 'img', 'Abdominal X-ray interpretation', 'Imaging', ffp='Abdominal X-ray', u=[48, 45, 25, 79],
  door=IMG_DOOR.format(what='an abdominal X-ray'),
  hooks=[
    '**3-6-9:** small bowel over 3 cm, colon over 6 cm, caecum over 9 cm = dilated.',
    '**Small bowel is central with lines all the way across:** valvulae conniventes. **Colon is around the edge with lines part-way across:** haustra.',
    '**Coffee bean from the left lower abdomen to the right upper = sigmoid volvulus.**',
    '**Both sides of the bowel wall visible = Rigler\'s sign = free air.** An erect CXR is better for perforation; CT is best.',
    '**Bowel gas, then outside the bowel, then bones, soft tissue, stones and artefacts.**',
  ],
  money='This is a **supine abdominal X-ray** of Mrs Brown, taken today. There are **multiple dilated loops of central bowel up to 4.5 cm with valvulae conniventes** crossing the full width. There is no gas in the large bowel. There is no free air. The bones and soft tissues are normal. These findings are consistent with **small bowel obstruction**. I would make her nil by mouth, insert a **nasogastric tube**, start **IV fluids**, check for hernias and request a **CT abdomen**.',
  traps=['Mixing up valvulae conniventes and haustra', 'Not measuring', 'Forgetting to look for free air', 'Saying an AXR excludes perforation'],
  dg=['axr', 'axrsys'],
  vars=[
    V('A', 'Mrs Brown, 72, previous hysterectomy', 'Small bowel obstruction', [], 'Central dilated loops up to 4.5 cm with valvulae conniventes; no colonic gas.', 'SBO, likely adhesions: drip and suck, CT, surgical review.', img={'k': 'axr', 'a': 'sbo'}),
    V('B', 'Mr Grey, 78', 'Large bowel obstruction', [], 'Peripheral dilated colon up to 8 cm with haustra; caecum 9 cm.', 'LBO: CT to find the cause, often cancer; risk of caecal perforation over 12 cm.', img={'k': 'axr', 'a': 'lbo'}),
    V('C', 'Mr Field, 82, care home resident', 'Sigmoid volvulus', [], 'A huge coffee-bean loop arising from the left lower abdomen pointing to the right upper.', 'Sigmoid volvulus: flexible sigmoidoscopy to decompress, flatus tube.', img={'k': 'axr', 'a': 'volv'}),
    V('D', 'Ms Lee, 31, ulcerative colitis', 'Toxic megacolon', [], 'Transverse colon over 6 cm with loss of haustra and mucosal thickening.', 'Toxic megacolon: IV steroids, surgical review, risk of perforation.', img={'k': 'axr', 'a': 'mega'}),
  ],
  ask=['What size is too big?', 'How would you confirm a perforation?', 'What is the next step?'],
  secs=[
    ('Details', ['!Name, date, supine or erect || || ']),
    ('Bowel gas', [
      '!Small bowel: central, valvulae conniventes, over 3 cm is dilated || || ',
      '!Large bowel: peripheral, haustra, over 6 cm, caecum over 9 cm || || ',
    ]),
    ('Outside the bowel', ['!Free air: Rigler\'s sign; gas in the biliary tree || || ']),
    ('Everything else', ['Bones, soft tissues, organ outlines, calcification such as stones, artefacts and lines || || ']),
    ('Conclude', ['!Diagnosis and next step || || ']),
  ])

station('I-ct', 'img', 'Chest and abdominal CT', 'Imaging', ffp='Chest + Abdominal CT', u=[13, 44, 40, 43, 21],
  door=IMG_DOOR.format(what='a CT image'),
  hooks=[
    '**You are looking up from the patient\'s feet:** their right is on your left.',
    '**Name it first:** CT of what, with or without contrast, which phase, which window.',
    '**Windows:** lung window to see lungs; soft tissue window to see organs; bone window for bones.',
    '**Black to white: air, fat, water, soft tissue, blood, contrast and bone.**',
    '**Scroll top to bottom, one organ at a time.**',
  ],
  money='This is an **axial CT pulmonary angiogram** of Mr Taylor, in the soft tissue window, viewed from the feet. There is a **filling defect in the right main pulmonary artery**, a dark area within the bright contrast. The lungs, heart and bones are otherwise normal. These findings are consistent with a **pulmonary embolism**. I would start **anticoagulation with a DOAC** such as apixaban, assess the heart strain, and look for a cause.',
  traps=['Getting left and right the wrong way round', 'Not saying the window and phase', 'Describing only the obvious finding'],
  dg=['ctorient', 'hu'],
  vars=[
    V('A', 'Mr Taylor, 54', 'Pulmonary embolism on CTPA', [], 'Dark filling defect in the right main pulmonary artery within bright contrast.', 'PE: anticoagulate; thrombolysis if haemodynamically unstable; look for the cause.', img={'k': 'ct', 'a': 'pe'}),
    V('B', 'Mr Wood, 76', 'Abdominal aortic aneurysm', [], 'Aorta 7 cm across with a rim of thrombus and surrounding fat stranding.', 'AAA, possibly leaking: vascular surgeons now, permissive hypotension.', img={'k': 'ct', 'a': 'aaa'}),
    V('C', 'Ms Hall, 66', 'Lung tumour', [], 'Spiculated mass in the right lung in the lung window.', 'Suspected lung cancer: biopsy, PET-CT, lung MDT.', img={'k': 'ct', 'a': 'mass'}),
    V('D', 'Mr King, 45', 'Pneumoperitoneum on CT', [], 'Black free air anterior to the liver under the abdominal wall.', 'Perforated viscus: resuscitate, antibiotics, surgery.', img={'k': 'ct', 'a': 'air'}),
  ],
  ask=['How do you know which side is which?', 'What does the contrast phase tell you?', 'What would you do now?'],
  secs=[
    ('Details', ['!Name, date, type of scan, contrast and phase, window || This is an axial CT... with contrast, in the soft tissue window. || ']),
    ('Orientation', ['!Viewed from the feet: patient\'s right on the left of the screen || || ']),
    ('Systematic review', [
      '!Chest: lungs, airways, pulmonary arteries, heart, mediastinum, pleura || || ',
      '!Abdomen: liver, gallbladder, pancreas, spleen, kidneys, adrenals, bowel, aorta, free fluid or air || || ',
      'Bones and soft tissues || || ',
    ]),
    ('Conclude', ['!Diagnosis and next step || || ']),
  ])

station('I-ecg', 'img', '12-lead ECG interpretation', 'Imaging', ffp='12-lead ECG interpretation', u=[0, 3, 6, 68],
  door=IMG_DOOR.format(what='an ECG'),
  hooks=[
    '**Rate → Rhythm → Axis → P → PR → QRS → ST → T → QT.** The same order every time.',
    '**Rate:** 300 divided by the big squares between beats; if irregular, count beats on the strip and multiply by 6.',
    '**Axis: Leaving = Left, Reaching = Right.** Leads I and aVF pointing away from each other = left axis; towards each other = right axis.',
    '**PR over 200 ms = first-degree block. QRS over 120 ms = bundle branch block or ventricular.**',
    '**Leads tell the wall, the wall tells the artery:** II, III, aVF = inferior = right coronary; V1 to V4 = anterior = LAD; I, aVL, V5, V6 = lateral = circumflex.',
  ],
  money='This is a **12-lead ECG** of Mr Evans, taken today at 09:00, at standard speed and gain. The rate is about **80**, the rhythm is **sinus**, and the axis is normal. The PR interval and QRS are normal. There is **ST elevation in leads II, III and aVF** with reciprocal ST depression in I and aVL. These findings are consistent with an **acute inferior STEMI**. This is an emergency: I would give **aspirin 300 mg**, and call the cardiology team for **primary PCI**.',
  traps=['Not stating the patient details and the calibration', 'Skipping the axis', 'Missing the reciprocal changes', 'Not giving an immediate action for a STEMI'],
  dg=['ecgwave', 'ecgterr'],
  vars=[
    V('A', 'Mr Evans, 62', 'Inferior STEMI', [], 'Sinus rhythm 80; ST elevation in II, III, aVF; reciprocal depression in I and aVL.', 'Inferior STEMI: aspirin, primary PCI within 120 minutes; check right-sided leads for RV infarct.', img={'k': 'ecg', 'a': 'stemi'}),
    V('B', 'Mrs Clarke, 78', 'Atrial fibrillation', [], 'Irregularly irregular narrow-complex rhythm at about 110, no P waves.', 'AF with fast response: rate control with a beta-blocker, CHA2DS2-VASc and ORBIT, anticoagulation.', img={'k': 'ecg', 'a': 'af'}),
    V('C', 'Mr Patel, 81', 'Complete heart block', [], 'P waves and broad QRS complexes march independently; ventricular rate about 35.', 'Complete heart block: atropine, then pacing; admit to cardiology.', img={'k': 'ecg', 'a': 'chb'}),
    V('D', 'Mrs Okafor, 66, CKD', 'Hyperkalaemia', [], 'Tall tented T waves, flat P waves, widening QRS.', 'Hyperkalaemia: IV calcium gluconate to protect the heart, insulin with glucose, salbutamol; find the cause.', img={'k': 'ecg', 'a': 'hiK'}),
    V('E', 'Leah, 22', 'Wolff-Parkinson-White', [], 'Short PR interval with a slurred delta wave at the start of the QRS.', 'WPW: avoid AV node blockers in AF; refer for ablation.', img={'k': 'ecg', 'a': 'wpw'}),
    V('F', 'Mr Ford, 70', 'Left bundle branch block', [], 'Broad QRS with an M shape in V6 and W in V1.', 'LBBB: new LBBB with chest pain is treated like a STEMI equivalent; otherwise look for a cause.', img={'k': 'ecg', 'a': 'lbbb'}),
    V('G', 'Ben, 25', 'SVT', [], 'Regular narrow-complex tachycardia at 180 with no visible P waves.', 'SVT: vagal manoeuvres, then adenosine 6, 12, 18 mg; DC cardioversion if unstable.', img={'k': 'ecg', 'a': 'svt'}),
  ],
  ask=['How did you work out the rate?', 'Which artery is involved?', 'What would you do now?'],
  secs=[
    ('Details', ['!Name, date of birth, date and time, calibration 25 mm/s and 10 mm/mV || || ']),
    ('Rate and rhythm', [
      '!Rate: 300 over big squares, or beats on the strip times 6 || || ',
      '!Rhythm: regular or irregular, P before every QRS || || ',
    ]),
    ('Axis', ['!Leads I and aVF || || ']),
    ('Intervals and waves', [
      '!P waves, PR interval 120 to 200 ms || || ',
      '!QRS width under 120 ms; shape || || ',
      '!ST segments: elevation or depression and which leads || || ',
      'T waves; QTc || || ',
    ]),
    ('Conclude', ['!Diagnosis, territory, immediate action || || ']),
  ])
