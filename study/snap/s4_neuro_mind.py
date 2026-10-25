from snapdsl import N

N(89, 'Headache', 'brain', 'mening',
  'Most headaches come from muscles, nerves or vessels outside the brain → a few signal bleeding, pressure or infection inside',
  'Tension and migraine: young adults, women · cluster: men · new headache 50+: think GCA',
  'Band-like, both sides: tension>head; One-sided, throbbing, light hurts: migraine>head; Around one eye, red and watery: cluster>eyes; Worse each morning, with vomiting: raised pressure>head',
  'History: onset, pattern, triggers, red flags*; BP, fundi, neuro exam>secondary causes; ESR and CRP>50+ with a new headache; CT or MRI>red flags only',
  'Tension: paracetamol, NSAID, avoid overuse | Migraine: triptan plus NSAID; preventer: propranolol, topiramate or amitriptyline | Cluster: high-flow oxygen, subcutaneous sumatriptan; verapamil to prevent | Medication overuse: stop the painkillers',
  'Thunderclap: subarachnoid>e; Fever, neck stiffness, rash: meningitis>e; 50+ with jaw pain or visual loss: GCA, steroids today>e; New headache with neuro signs or papilloedema>s',
  'Primary headaches repeat the same story; secondary headaches tell a new one.')

N(90, 'Raised intracranial pressure', 'brain', 'whole',
  'A mass, bleed, swelling or blocked fluid → pressure rises in a closed skull → the brain is squeezed down',
  'Tumours, bleeds, abscess · hydrocephalus · IIH: young overweight women',
  'Headache worse lying down and in the morning>head; Vomiting>mouth; Papilloedema>eyes; Drowsy, confused>mind; Late: high BP, slow pulse>heart',
  'CT head>the cause*; Fundoscopy>papilloedema; Avoid LP until imaging is safe; MRI and venogram>IIH',
  'Head up 30°, ABCDE | Treat the cause; dexamethasone for tumour swelling | Mannitol or hypertonic saline if herniating | Neurosurgery; IIH: weight loss, acetazolamide',
  'Cushing\'s reflex: high BP, slow pulse, irregular breathing>e; Blown pupil: herniation>e; IIH with failing vision>s',
  'Cushing\'s triad means the brain is being pushed through the hole at the bottom.')

N(91, 'Subarachnoid haemorrhage', 'brain', 'vessel',
  'A berry aneurysm bursts → blood fills the space around the brain → sudden severe headache',
  '40 to 60 · smokers, high BP · polycystic kidneys, family history',
  'Thunderclap headache, worst ever, peaks in 1 minute>head; Neck stiffness>neck; Vomiting, collapse>mouth; Light hurts>eyes',
  'CT head within 6 h>blood around the brain*; LP at 12 h if CT normal after 6 h>xanthochromia; CT angiogram>the aneurysm',
  'ABCDE; neurosurgery referral | Nimodipine to prevent spasm | Coil or clip the aneurysm | Keep sodium and BP in range',
  'Drowsy or falling GCS>e; Vasospasm days 4 to 14: new weakness>e; Hydrocephalus>e',
  'Thunderclap = peaks in under a minute. Never send it home without imaging.')

N(92, 'Subdural haemorrhage', 'brain', 'sub',
  'A bridging vein tears → blood collects slowly between the brain and the dura → a crescent squeezing the brain',
  'Older people, alcohol · falls · anticoagulants · babies: shaken',
  'Fluctuating confusion over days to weeks>mind; Headache>head; Drowsy>head; One-sided weakness>rarm',
  'CT head>crescent that crosses suture lines*; Clotting screen>INR, platelets',
  'Reverse anticoagulation | Neurosurgery if large or symptomatic: burr holes | Small: watch and repeat CT',
  'Falling GCS, blown pupil>e; Extradural: lucid interval then collapse>e; Child with subdural: safeguarding>e',
  'Subdural is a slow crescent in the old; extradural is a fast lemon after a young person\'s skull fracture.')

N(93, 'Meningitis', 'brain', 'mening',
  'Bacteria or viruses inflame the meninges → swelling and toxins → sepsis and raised pressure',
  'Babies, students, the elderly · not immunised · close contacts',
  'Fever and headache>head; Neck stiffness>neck; Light hurts>eyes; Non-blanching rash>skin; Confused, drowsy>mind',
  'Blood cultures first>before antibiotics; LP if safe>CSF: cloudy, high neutrophils, low glucose = bacterial*; Bloods>FBC, CRP, lactate, meningococcal PCR',
  'Community with rash: IM benzylpenicillin straight away | Hospital: IV ceftriaxone; add amoxicillin if 60+ or immunosuppressed | Dexamethasone before or with the first dose | Notify public health; prophylaxis for contacts',
  'Purpuric rash: meningococcal sepsis>e; Seizures, falling GCS>e; Hearing loss after: test hearing>u',
  'Never delay antibiotics for an LP.')

N(94, 'Encephalitis', 'brain', 'cortex',
  'A virus, usually herpes simplex, infects the brain tissue → temporal lobes swell → confusion and fits',
  'Any age · immunosuppressed · HSV most common in the UK',
  'Fever>head; Confusion, odd behaviour>mind; Seizures>head; Speech or memory problems>head',
  'MRI>temporal lobe changes*; LP>lymphocytes, HSV PCR*; EEG>temporal changes',
  'IV aciclovir on suspicion, before the results | Supportive care, seizure control | Treat for 14 to 21 days',
  'Status epilepticus>e; Falling GCS>e; Lasting memory and personality change>r',
  'Meningitis gives the neck; encephalitis gives the mind. Aciclovir if in doubt.')

N(95, 'Brain abscess', 'brain', 'deep',
  'Bacteria spread from ears, sinuses, teeth or the blood → pus collects in the brain → it acts as a growing mass',
  'Ear or sinus infection, dental abscess · endocarditis · immunosuppressed',
  'Headache>head; Fever, sometimes absent>head; Focal weakness>rarm; Seizures>head',
  'CT or MRI with contrast>ring-enhancing lesion*; Blood cultures>the bug; Avoid LP>risk of coning',
  'IV antibiotics for weeks | Neurosurgical drainage | Find and treat the source',
  'Raised pressure signs>e; Rupture into the ventricles>e',
  'Ring-enhancing lesion plus fever plus a source = abscess until proved otherwise.')

N(96, 'Epilepsy', 'brain', 'cortex',
  'Brain cells fire together abnormally → a seizure → the pattern depends on where it starts',
  'Any age · after stroke, head injury · family history',
  'Tonic-clonic: stiffen then jerk>head; Tongue bitten on the side>mouth; Incontinence>genit; Confused and sleepy after>mind; Focal: jerking or odd feelings in one part>rarm',
  'Witness account and video>most useful*; EEG>supports the type; MRI>structural cause; Bloods, ECG>glucose, sodium, calcium, arrhythmia',
  'First fit: specialist within 2 weeks; no driving | Generalised: sodium valproate, not in women who could get pregnant: lamotrigine or levetiracetam | Focal: lamotrigine or levetiracetam | Safety advice: baths, heights, swimming',
  'Status: over 5 minutes, buccal midazolam or IV lorazepam>e; Valproate in pregnancy: birth defects>s; Driving: tell the DVLA>r',
  'Faint: brief, quick recovery, pale. Fit: tongue bitten, long confusion after.')

N(97, 'Motor neurone disease', 'nerve', 'horn',
  'Motor nerve cells in the brain and cord die → muscles weaken and waste → sensation is untouched',
  '50 to 70 · men slightly more · family history in some',
  'Weakness, wasting, twitching muscles>rarm; Brisk reflexes alongside wasting>legs; Slurred speech, choking>mouth; No sensory loss>skin',
  'Clinical: mixed upper and lower motor neurone signs*; EMG>widespread denervation; MRI>exclude cord compression',
  'Specialist MDT | Riluzole | NIV for breathing | Feeding tube, speech help, palliative care',
  'Breathing failure>e; Aspiration pneumonia>s; Mood and end-of-life planning>u',
  'Upper and lower motor neurone signs in the same limb, no sensory loss = MND.')

N(98, 'Myopathies', 'nerve', 'muscle',
  'The muscle fibres themselves are damaged → weakness close to the trunk → nerves and sensation normal',
  'Statins, steroids · thyroid · polymyositis, inherited',
  'Struggles to climb stairs or rise from a chair>legs; Can\'t lift arms above the head>rarm; Muscle pain in some>larm; Normal sensation>skin',
  'CK>raised*; TFT>thyroid causes; EMG and muscle biopsy>type',
  'Stop the culprit drug | Treat the cause; steroids for inflammatory myositis | Physiotherapy',
  'Dark urine with very high CK: rhabdomyolysis>e; Breathing or swallowing weakness>e',
  'Proximal weakness, normal sensation, high CK = the muscle, not the nerve.')

N(99, 'Neuropathies and palsies', 'nerve', 'nerve',
  'Nerves are squashed, starved or poisoned → numbness, tingling and weakness in their territory',
  'Diabetes, alcohol, B12 · carpal tunnel: women, pregnancy · GBS after an infection',
  'Tingling in a glove and stocking pattern>feet; Carpal tunnel: numb thumb to ring finger at night>hands; Foot drop: common peroneal>legs; Ascending weakness after illness: GBS>legs',
  'Bloods>glucose, B12, TFT, U&E, LFT, folate*; Nerve conduction studies>type and site; LP>GBS: high protein, normal cells',
  'Treat the cause | Neuropathic pain: amitriptyline, duloxetine, gabapentin, pregabalin | Carpal tunnel: splint, steroid injection, surgery | GBS: IV immunoglobulin, monitor breathing',
  'GBS: falling FVC, needs ICU>e; Sudden foot drop with back pain: cauda equina>e; Diabetic foot ulcers>s',
  'Glove and stocking = many nerves. One territory = one nerve squashed.')

N(100, 'Schizophrenia and psychosis', 'mind', 'thought',
  'Too much dopamine signalling in some pathways → the brain mislabels thoughts and noises → voices and fixed false beliefs',
  'Late teens to 30s · family history · cannabis, migrants, urban upbringing',
  'Hearing voices in the third person>ear; Delusions: fixed false beliefs>mind; Thought broadcast or insertion>mind; Negative: flat, withdrawn, no motivation>face',
  'Clinical: first-rank symptoms over 1 month*; Exclude organic causes>drugs, thyroid, MRI if atypical; Baseline before antipsychotics>weight, glucose, lipids, ECG, prolactin',
  'Early intervention in psychosis team | Antipsychotic plus CBT and family work | Clozapine after 2 failed antipsychotics | Physical health checks yearly',
  'Command voices to harm self or others>e; Self-neglect, suicide risk>s; NMS on antipsychotics>e',
  'Positive symptoms are added: voices, delusions. Negative are taken away: drive, emotion, speech.')

N(101, 'Antipsychotics, NMS and acute dystonia', 'mind', 'drug',
  'Antipsychotics block dopamine → psychosis eases → but block too much elsewhere and you get movement and hormone side effects',
  'Anyone on antipsychotics · first doses: dystonia · young men: high-potency drugs',
  'Acute dystonia: neck twists, eyes roll up>neck; Akathisia: can\'t sit still>legs; Parkinsonism, tremor>hands; Weight gain, diabetes: atypicals>abdo; NMS: fever, rigid, confused>mind',
  'Baseline and yearly>weight, glucose, lipids, ECG, prolactin*; NMS: CK>very high; Clozapine: FBC>neutrophils weekly at first',
  'Dystonia: procyclidine | Akathisia: lower dose, propranolol | NMS: stop the drug, cool, fluids; dantrolene or bromocriptine | Clozapine: monitored, highest efficacy',
  'NMS: fever, rigidity, high CK>e; Clozapine with sore throat or fever: neutropenia>e; QT prolongation>s',
  'Typicals move you: stiff and shaky. Atypicals feed you: weight, sugar, lipids.', k='t')

N(102, 'Depression and suicide risk', 'mind', 'mood',
  'Stress, genes and thinking patterns shift brain chemistry → low mood and lost pleasure → everything slows',
  'Women 2 times more · after loss, chronic illness · postnatal · alcohol',
  'Low mood most of the day for 2 weeks>mind; Lost interest or pleasure>face; Poor sleep, early waking>head; Tired, low appetite>abdo; Thoughts of death or suicide>mind',
  'Clinical: SIGECAPS, PHQ-9>severity*; Risk assessment>thoughts, plans, intent, protective factors; Bloods>TFT, FBC to exclude physical causes',
  'Less severe: guided self-help, CBT, exercise | More severe: CBT plus an SSRI: sertraline | Not responding: switch or add; psychiatry | Severe or life-threatening: ECT',
  'Active plan with intent>e; Psychotic depression>s; SSRI in under 25s: watch for agitation and suicidal thoughts early>s',
  'Ask about suicide directly: asking does not plant the idea.')

N(103, 'Bipolar disorder', 'mind', 'swing',
  'Mood regulation breaks down → episodes swing from depression to mania → normal in between',
  'Late teens to 20s · strong family history · triggered by sleep loss, drugs, antidepressants',
  'Mania: little sleep, not tired>head; Grandiose, racing thoughts>mind; Pressured speech>mouth; Spending, risky sex or driving>all; Depression episodes>face',
  'Clinical: mania for 7 days or hypomania 4 days*; Exclude drugs, thyroid>bloods; Before lithium>U&E, TFT, ECG, calcium, weight',
  'Mania: stop antidepressants; antipsychotic | Long term: lithium first-line | Valproate only if no pregnancy possible | Psychoeducation, sleep routine, relapse plan',
  'Mania with risk to self or others: admission, MHA>e; Lithium toxicity: tremor, vomiting, confusion>e; Depressive phase suicide>s',
  'Never give an antidepressant alone in bipolar: it can flip someone into mania.')

N(104, 'Generalised anxiety and panic', 'mind', 'fear',
  'The threat system stays switched on → worry or surges of fear → the body fires adrenaline',
  'Women · 20s to 50s · stress, family history',
  'Worry about many things on most days: GAD>mind; Sudden surges of fear, peaking in 10 min: panic>heart; Palpitations, sweating, shaking>hands; Breathless, tingling>lungs',
  'Clinical: GAD-7>severity*; Exclude thyroid, caffeine, alcohol, drugs>bloods if needed; ECG>if palpitations',
  'Psychoeducation, self-help | CBT or applied relaxation | SSRI: sertraline | Avoid benzodiazepines except in crisis',
  'Suicidal thoughts>s; Alcohol or benzodiazepine dependence>u; Chest pain: rule out cardiac first>e',
  'Anxiety is a smoke alarm that rings for toast. CBT recalibrates the alarm.')

N(105, 'Acute stress reaction and PTSD', 'mind', 'stress',
  'A terrifying event overwhelms coping → memories stay raw and replay → the body stays on alert',
  'After assault, combat, accidents, disasters · earlier trauma',
  'Flashbacks and nightmares>mind; Avoiding reminders>face; Always on edge, startles easily>heart; Numb, detached>face',
  'Clinical: acute stress under 1 month; PTSD over 1 month*; Screen for depression, substance use, risk',
  'Watchful waiting for the first month | Trauma-focused CBT | EMDR | Drugs: venlafaxine or SSRI if therapy not enough',
  'Suicidal thoughts>s; Alcohol or drug use to cope>u; Ongoing danger: safeguarding>e',
  'PTSD: the past keeps happening in the present.')

N(106, 'OCD', 'mind', 'loop',
  'Intrusive thoughts cause anxiety → rituals relieve it briefly → the relief reinforces the loop',
  'Teens to 20s · family history · after strep in children: PANDAS',
  'Intrusive unwanted thoughts>mind; Compulsions: washing, checking, counting>hands; Knows they are excessive>mind; Hours lost each day>all',
  'Clinical: Y-BOCS severity*; Screen for depression and tics',
  'CBT with exposure and response prevention | SSRI, higher doses, or clomipramine | Specialist service if severe',
  'Severe self-neglect or skin damage from washing>u; Suicidal thoughts>s',
  'Exposure and response prevention: face the fear, skip the ritual, let the anxiety fall on its own.')

N(107, 'Somatisation and medically unexplained symptoms', 'mind', 'body',
  'Distress is felt as body symptoms → real suffering → tests keep coming back normal',
  'Women more · anxiety, depression · past trauma',
  'Many symptoms across systems>all; Pain, tiredness, bowel symptoms>abdo; Repeated normal tests>mind; Frequent attenders>face',
  'Rule out organic disease once, thoroughly*; Avoid repeated tests>they reinforce worry; Screen for depression and anxiety',
  'One named clinician; regular scheduled reviews | Explain: real symptoms, no damage | CBT; treat depression or anxiety | Antidepressant for pain-predominant',
  'New physical red flag: still investigate it>s; Suicidal thoughts>s',
  'Acknowledge the symptoms are real; explain the mechanism; stop chasing tests.')

N(108, 'Eating disorders', 'mind', 'food',
  'Control and body image become fixed on food → restriction, bingeing or purging → the body starves or is thrown off balance',
  'Young women · teens · athletes, dancers · perfectionism, anxiety',
  'Anorexia: low weight, fear of gaining>abdo; Bulimia: binge and purge, normal weight>mouth; Russell\'s sign: calloused knuckles>hands; Amenorrhoea>genit; Cold, fine downy hair>skin',
  'BMI and weight trend*; Bloods>U&E, potassium, phosphate, magnesium, glucose; ECG>slow pulse, long QT; Risk assessment using MEED>sit-up-squat-stand test',
  'Eating disorder team | Anorexia: specialist family therapy for young people, CBT-ED for adults | Bulimia: guided self-help, CBT-ED | Medical admission if high risk',
  'BMI under 13, pulse under 40, low potassium, long QT>e; Refeeding syndrome>e; Suicide risk>s',
  'Anorexia is low weight; bulimia is normal weight with purging. Both can stop a heart.')

N(109, 'Personality disorders', 'mind', 'self',
  'Patterns of thinking, feeling and relating set early → rigid and long-lasting → cause distress in many settings',
  'Start in adolescence · childhood trauma · emotionally unstable: women more · antisocial: men more',
  'Emotionally unstable: intense, unstable relationships>mind; Fear of abandonment>face; Self-harm, impulsivity>larm; Antisocial: disregard for others>hands',
  'Clinical: lifelong pattern across settings*; Screen for depression, substance use, risk',
  'Validate, consistent boundaries | Dialectical behaviour therapy, mentalisation-based therapy | Crisis plan | Drugs only for comorbid illness or short crises',
  'Self-harm or suicidal crisis>e; Risk to others>s; Substance misuse>u',
  'Not an illness that comes and goes, but a long-standing way of being.')

N(110, 'Alcohol and substance misuse', 'mind', 'habit',
  'Repeated use hijacks the reward system → tolerance, then withdrawal → use continues despite harm',
  'Men more · young adults for drugs · stress, family history',
  'Craving, can\'t cut down>mind; Withdrawal: tremor, sweats from 6 to 12 h>hands; Fits at 24 to 48 h>head; DTs at 48 to 72 h>mind; Wernicke\'s: confusion, wobbly, eye movements>eyes',
  'AUDIT-C, then AUDIT>screen*; Bloods>LFT, GGT, MCV, FBC; Urine drug screen',
  'Brief intervention, motivational interviewing | Assisted withdrawal: chlordiazepoxide reducing course | Thiamine for all, IV Pabrinex if Wernicke\'s | Relapse prevention: acamprosate or naltrexone; opioids: methadone or buprenorphine',
  'DTs: hallucinations, fever, confusion>e; Wernicke\'s: IV thiamine before glucose>e; Opioid overdose: naloxone>e',
  'Withdrawal clock: 6 shakes, 12 sees, 24 fits, 48 DTs.')

N(111, 'Overdose, self-harm and lithium toxicity', 'mind', 'crisis',
  'A person in distress harms themselves or takes too much → treat the body, then the mind → assess risk every time',
  'Young women for self-harm · men more for completed suicide · lithium users',
  'Paracetamol: often no symptoms early>abdo; Opioids: pinpoint pupils, slow breathing>eyes; Lithium toxicity: coarse tremor, vomiting, confusion>hands; Cuts or burns>larm',
  'Paracetamol level at 4 h or later>nomogram*; Bloods>U&E, LFT, INR, glucose, lithium level; ECG>tricyclics, QT; Psychosocial assessment>every self-harm presentation',
  'ABCDE; TOXBASE | Paracetamol: acetylcysteine if over the line or staggered | Opioids: naloxone; tricyclics: sodium bicarbonate | Lithium: stop, fluids, haemodialysis if severe',
  'Staggered paracetamol overdose: treat regardless of level>e; Lithium over 2 or neuro signs>e; High suicide intent>e',
  'Every self-harm needs a psychosocial assessment, even if the overdose was small.')

N(112, 'Psychiatric drugs, serotonin syndrome and the MHA', 'mind', 'drug',
  'Drugs change brain chemistry → too much serotonin or wrong combinations cause toxicity → the law covers treatment without consent',
  'Anyone on SSRIs, MAOIs, tramadol, triptans · people lacking insight into a mental disorder',
  'Serotonin syndrome: agitated, sweaty, fever>mind; Clonus, brisk reflexes, tremor>legs; Dilated pupils, diarrhoea>eyes; Starts within hours of a new drug>all',
  'Clinical: Hunter criteria>clonus is key*; CK, U&E>muscle breakdown; MHA assessment>AMHP plus 2 doctors',
  'Serotonin syndrome: stop the drugs, benzodiazepines, cooling | Severe: cyproheptadine, ICU | MHA section 2: 28 days assessment; section 3: 6 months treatment | Doctor\'s holding power on a ward, section 5 part 2: 72 h',
  'Temperature over 41: serotonin syndrome or NMS>e; Risk to self or others with no insight: MHA>e',
  'Serotonin syndrome is fast and twitchy; NMS is slow and rigid.', k='t')

N(113, 'ECT and catatonia', 'mind', 'fog',
  'Catatonia: the brain freezes movement and speech. ECT: a controlled seizure resets mood circuits → fast relief when life is at risk',
  'Severe depression, catatonia, mania · not eating or drinking · failed other treatment',
  'Catatonia: mute, still, staring>face; Holding odd postures>rarm; Not eating or drinking>mouth; Echoing words or actions>mouth',
  'Clinical: Bush-Francis scale*; Lorazepam challenge>improves = catatonia; Exclude NMS, encephalitis>bloods, CK',
  'Catatonia: lorazepam | ECT if lorazepam fails or life-threatening | ECT course: twice weekly under anaesthetic | Consent or legal safeguards',
  'Malignant catatonia: fever, autonomic swings>e; Not drinking: dehydration, clots>e; ECT side effects: short-term memory loss>r',
  'Lorazepam unlocks catatonia; ECT is for when life is at stake.')

N(114, 'Autism spectrum disorder', 'mind', 'dev',
  'The brain develops differently → social communication and sensory processing differ → strong routines and interests',
  'Diagnosed in childhood · boys more often diagnosed · girls often missed',
  'Social communication differences>face; Restricted, repetitive interests>mind; Need for routine>all; Sensory sensitivity: noise, light, touch>ear',
  'Specialist multidisciplinary assessment*; Screen for ADHD, anxiety, learning disability',
  'Adjustments: clear communication, predictable routine | Support at school and work | Treat anxiety, sleep and ADHD | Antipsychotic only for severe aggression',
  'Distress or meltdown from change>u; Mental health crisis or self-injury>s',
  'A different operating system, not a broken one: adjust the environment first.')

N(115, 'Perinatal mental health', 'mind', 'mood',
  'Huge hormone shifts and sleep loss after birth → mood drops or psychosis erupts → mother and baby both at risk',
  'Blues: most mothers, day 3 to 5 · depression: 1 in 10 · psychosis: bipolar history',
  'Baby blues: tearful, days 3 to 5, settles in 2 weeks>face; Postnatal depression: low mood, not bonding>mind; Psychosis: confused, delusions, first 2 weeks>mind',
  'Edinburgh Postnatal Depression Scale>screen*; Risk to mother and baby>every contact',
  'Blues: reassure | Depression: CBT, SSRI: sertraline is fine when breastfeeding | Psychosis: emergency mother and baby unit | Plan ahead for women with bipolar',
  'Postpartum psychosis: emergency admission>e; Thoughts of harming the baby>e; Suicide: a leading cause of maternal death>e',
  'Blues pass in days; depression lasts weeks; psychosis is an emergency.')

N(116, 'Delirium', 'mind', 'fog',
  'An acute illness or drug disturbs the brain → attention fails and fluctuates → confusion over hours to days',
  'Older people, dementia · after surgery · infection, drugs, retention, constipation',
  'Sudden confusion that fluctuates>mind; Can\'t focus attention>eyes; Hyperactive: agitated; hypoactive: sleepy>face; Worse at night>head',
  '4AT>screen*; Find the cause>bloods, urine, CXR, drug review, bladder scan; Collateral history>baseline',
  'Treat the cause | Reorientate: glasses, hearing aids, clock, family | Avoid sedation; low-dose haloperidol only if risk | Sleep, fluids, mobilise',
  'Hypoactive delirium is easily missed>s; Falls, aspiration>s; Underlying sepsis>e',
  'PINCH ME: Pain, Infection, Nutrition, Constipation, Hydration, Medication, Environment.')

N(117, 'Adjustment disorder', 'mind', 'stress',
  'A stressful life change → coping is overwhelmed → symptoms within 3 months that settle within 6',
  'Anyone · divorce, job loss, illness, migration',
  'Low mood, worry, tearful>mind; Trouble sleeping>head; Struggling at work>all; Started within 3 months of the stressor>face',
  'Clinical: clear stressor, symptoms out of proportion*; Exclude depression and PTSD>assessment',
  'Support, problem solving | Brief talking therapy | Review: if lasting over 6 months, reassess',
  'Suicidal thoughts>s; Alcohol use to cope>u',
  'Adjustment is a reaction that fades as the stress fades.')

N(118, 'Phobias', 'mind', 'fear',
  'A specific object or situation triggers intense fear → avoidance brings relief → the fear grows',
  'Childhood onset · women more · social phobia: teens',
  'Intense fear of a specific thing: spiders, heights, needles>mind; Avoidance>face; Social phobia: fear of being judged>face; Panic symptoms on exposure>heart',
  'Clinical assessment*; Screen for depression and other anxiety',
  'Graded exposure: build a fear ladder | CBT | SSRI for social anxiety',
  'Agoraphobia housebound>u; Needle phobia blocking care>u',
  'Avoidance feeds the phobia; exposure starves it.')

N(119, 'ADHD', 'mind', 'dev',
  'Brain networks for attention and self-control develop differently → inattention, hyperactivity, impulsivity → across settings',
  'Diagnosed in childhood, persists into adults · boys diagnosed more · family history',
  'Inattention: loses things, distracted>mind; Hyperactive: fidgety, can\'t sit still>legs; Impulsive: interrupts, acts first>mouth; In 2 or more settings>all',
  'Specialist assessment, symptoms before 12*; Reports from school or work>settings; Before stimulants>height, weight, BP, pulse, cardiac history',
  'Psychoeducation, environmental changes | Children: parent training first if under 5 | Lisdexamfetamine or methylphenidate; atomoxetine if stimulants unsuitable | Monitor growth, BP, pulse',
  'Stimulants: palpitations, high BP>u; Poor appetite, weight loss>r; Misuse or diversion>u',
  'An engine with weak brakes: medication strengthens the brakes.')

N(120, 'Conduct disorder and ODD', 'mind', 'self',
  'Temperament plus harsh or inconsistent parenting → defiant, then rule-breaking behaviour → risk of antisocial adulthood',
  'Boys · ADHD · family conflict, deprivation, abuse',
  'ODD: angry, argumentative, defiant: younger>mouth; Conduct disorder: aggression, theft, cruelty>hands; Truancy>all',
  'Clinical: pattern over 6 months*; Screen for ADHD, learning difficulty, abuse',
  'Parent training programmes | Child-focused social skills | Multi-agency: school, social care | Treat ADHD if present',
  'Abuse or neglect: safeguarding>e; Violence, weapons>e',
  'Fix the environment and parenting first; most behaviour is a response.')

N(121, 'Intellectual disability', 'mind', 'dev',
  'Brain development is limited from early life → IQ under 70 with difficulty in daily living → lifelong support needs',
  'Genetic: Down\'s, fragile X · birth injury, infection · foetal alcohol',
  'Delayed milestones>head; Needs support with daily living>all; Communication difficulty>mouth; Pain shown as behaviour change>face',
  'Clinical and psychometric assessment*; Genetic testing>cause; Annual health check>from age 14',
  'Reasonable adjustments, easy-read information | Involve carers; capacity assessment for each decision | Annual health checks | Treat physical illness: diagnostic overshadowing',
  'Behaviour change may be pain or illness>s; Epilepsy, constipation, reflux are common>u; Abuse: safeguarding>e',
  'Diagnostic overshadowing: don\'t blame the disability for a new symptom.')
