"""v3.6.2 Hammer set E, part 3 of 3 (format in hq6_a.py)."""

Q = r"""
@u 70 1D
s: A 72 year old man with type 2 diabetes who takes gliclazide is brought in by ambulance after his wife found him sweaty and confused. He cannot follow instructions or swallow safely. A cannula is already in place. // GCS 11, pulse rate 104 bpm, BP 146/84 mmHg.
$ Capillary blood glucose ; 1.8 mmol/L ; 4.0–7.8
$ Sodium ; 139 mmol/L ; 135–146
? Which is the most appropriate immediate treatment?
> Buccal glucose gel ; IM glucagon ; *IV 10% glucose ; IV 50% glucose ; Oral sugary drink
= A hypoglycaemic patient who cannot swallow safely but has IV access needs IV glucose: about 150 ml of 10% glucose or 75 ml of 20% over 10 to 15 minutes. Recheck the glucose after 10 minutes. Sulfonylurea hypoglycaemia can recur for many hours, so he needs admission and a glucose infusion if it returns.
~ Unconscious with no IV access → IM glucagon 1 mg.
c: gliclazide | cannot follow instructions or swallow safely | cannula is already in place | Capillary blood glucose 1.8
m: Glucose given into a vein restores fuel to the brain within minutes without relying on the gut or liver glycogen
g: Hypoglycaemia, unable to swallow, IV access → IV 10% or 20% glucose
f: the same picture with no IV access possible => IM glucagon
f: alert and able to swallow with a glucose of 3.1 => Oral sugary drink
x: Buccal glucose gel => Risks aspiration when he cannot swallow safely and is not advised if consciousness is reduced
x: IM glucagon => Used when IV access is not possible; it needs liver glycogen and acts more slowly
x: IV 50% glucose => Highly irritant to veins and damages tissue if it leaks, so 10% or 20% is preferred
x: Oral sugary drink => Unsafe when he cannot swallow

@k x:therapies 2R
s: A 23 year old woman has a 5 year history of cutting herself when distressed, intense relationships that end abruptly, and anger she struggles to control. She describes feeling empty and fears that people will leave her. Her mood shifts within hours. She has no psychotic symptoms and no sustained period of low or elevated mood.
? Which is the most appropriate long-term treatment?
> Cognitive behavioural therapy for depression ; *Dialectical behaviour therapy ; Eye movement desensitisation and reprocessing ; Fluoxetine ; Olanzapine
= Self-harm, unstable intense relationships, fear of abandonment, emptiness, anger and mood that shifts within hours are emotionally unstable, or borderline, personality disorder. Psychological therapy is the main treatment, and NICE recommends considering dialectical behaviour therapy for women with this diagnosis when reducing recurrent self-harm is the priority. Medicines are not used to treat the disorder itself.
~ Flashbacks, nightmares and hypervigilance after an assault → trauma-focused CBT or EMDR for PTSD.
c: cutting herself when distressed | intense relationships that end abruptly | feeling empty | Her mood shifts within hours | no sustained period of low or elevated mood
m: DBT teaches emotion regulation and distress tolerance while validating the person, so self-harm is no longer needed to cope
g: Borderline personality disorder with repeated self-harm → dialectical behaviour therapy
f: flashbacks, nightmares and hypervigilance since an assault 6 months ago => Eye movement desensitisation and reprocessing
f: 2 months of low mood, loss of interest and early waking with no long-standing relationship difficulties => Cognitive behavioural therapy for depression
x: Cognitive behavioural therapy for depression => She has no sustained low mood, and standard CBT does not target her emotional instability
x: Eye movement desensitisation and reprocessing => A treatment for PTSD, which is not described
x: Fluoxetine => Drugs do not treat the disorder and are used for coexisting conditions such as depression
x: Olanzapine => Sometimes used short term in a crisis, but not as treatment for the disorder

@u 120 1L
s: A 13 year old boy is referred by his school. Over the past 18 months he has stolen from shops, set fire to a bin, been cruel to the family cat and regularly stays out all night without permission. He has hit other pupils and threatened a teacher with a compass. // He is not low in mood, has no psychotic symptoms and does not use drugs.
? Which is the most likely diagnosis?
> Antisocial personality disorder ; Attention deficit hyperactivity disorder ; Autism spectrum disorder ; *Conduct disorder ; Oppositional defiant disorder
= A repeated pattern of serious violations of other people's rights and of age-appropriate rules, including theft, fire setting, cruelty to animals, aggression and staying out at night, is conduct disorder. Oppositional defiant disorder is defiance and temper without these serious violations. Antisocial personality disorder cannot be diagnosed before 18.
~ Angry, argumentative and defiant towards adults but no theft, aggression or cruelty → oppositional defiant disorder.
c: stolen from shops | set fire to a bin | cruel to the family cat | stays out all night | threatened a teacher
m: Persistent antisocial behaviour that breaks major rules and harms others, usually from a mix of temperament and environment
g: Theft, fire setting, cruelty and aggression in a child → conduct disorder
f: a 7 year old who argues, loses his temper and refuses rules at home but harms no one => Oppositional defiant disorder
f: the same behaviour continuing in a 22 year old who shows no remorse => Antisocial personality disorder
f: fidgety, impulsive and inattentive in every setting since age 5, without cruelty or theft => Attention deficit hyperactivity disorder
x: Antisocial personality disorder => Cannot be diagnosed before 18, though conduct disorder often comes before it
x: Attention deficit hyperactivity disorder => Can coexist, but impulsivity and inattention do not explain cruelty and theft
x: Autism spectrum disorder => Involves social communication difficulty and rigid routines, not deliberate harm to others
x: Oppositional defiant disorder => Defiance and temper without serious violations such as theft, cruelty or fire setting

@u 119 1L
s: An 8 year old boy is brought to his GP because his teacher says he cannot sit still, interrupts constantly and rarely finishes his work. His parents say he is the same at home, loses things every day and runs into the road without looking. This has been the case since he started school 3 years ago. // His hearing test is normal. He makes good eye contact, plays imaginatively and has friends. No staring spells have been seen.
? Which is the most likely diagnosis?
> *Attention deficit hyperactivity disorder ; Autism spectrum disorder ; Childhood absence epilepsy ; Hearing impairment ; Oppositional defiant disorder
= Hyperactivity, impulsivity and inattention at home and at school for more than 6 months, starting before age 12, are attention deficit hyperactivity disorder. His normal hearing, good social skills and lack of staring spells argue against the alternatives. He should be referred for specialist assessment; drug treatment is not started in primary care.
~ Many brief staring spells a day with eyelid flickering and 3 Hz spike and wave on EEG → childhood absence epilepsy.
c: cannot sit still | interrupts constantly | the same at home | since he started school 3 years ago | hearing test is normal
m: Differences in frontostriatal dopamine and noradrenaline signalling weaken inhibition and sustained attention
g: Inattention, hyperactivity and impulsivity in 2 settings for over 6 months → ADHD
f: many brief staring spells a day with eyelid flickering and 3 Hz spike and wave on EEG => Childhood absence epilepsy
f: poor eye contact, a need for fixed routines and difficulty making friends => Autism spectrum disorder
f: defiance and temper outbursts at home only, with good concentration at school => Oppositional defiant disorder
x: Autism spectrum disorder => He has good eye contact, imaginative play and friends
x: Childhood absence epilepsy => Causes brief staring spells, and none have been seen
x: Hearing impairment => His hearing test is normal
x: Oppositional defiant disorder => Describes defiance and temper rather than restlessness and inattention in every setting

@u 51 1D
s: A 68 year old man with chronic kidney disease has felt weak for 2 days. He recently started spironolactone for heart failure and also takes ramipril. // Pulse rate 52 bpm, BP 118/70 mmHg. His ECG shows tall peaked T waves, flattened P waves and a QRS duration of 140 ms.
$ Potassium ; 7.4 mmol/L ; 3.5–5.3
$ Creatinine ; 286 µmol/L ; 60–120
$ Bicarbonate ; 19 mmol/L ; 22–30
$ Glucose ; 6.1 mmol/L ; 4.0–7.8
? Which is the most appropriate first treatment?
> Calcium resonium ; *IV calcium gluconate ; IV insulin with glucose ; Nebulised salbutamol ; Sodium bicarbonate
= Severe hyperkalaemia with ECG changes needs IV calcium gluconate first, 30 ml of 10% over 5 to 10 minutes. It protects the heart within minutes but does not lower the potassium. Insulin with glucose and nebulised salbutamol then shift potassium into cells, and the spironolactone and ramipril are stopped.
~ Potassium of 6.6 with a normal ECG → insulin with glucose to shift potassium; calcium is for ECG changes.
c: spironolactone | ramipril | tall peaked T waves | QRS duration of 140 ms | Potassium 7.4
m: Calcium restores the gap between resting and threshold potential in cardiac cells, protecting against arrhythmia while potassium is lowered
g: Hyperkalaemia with ECG changes → IV calcium gluconate first
f: a potassium of 6.6 with a normal ECG => IV insulin with glucose
x: Calcium resonium => Removes potassium through the gut over hours to days, far too slowly
x: IV insulin with glucose => Lowers potassium within 15 to 30 minutes and comes next, once the heart is protected
x: Nebulised salbutamol => An add-on to insulin that shifts potassium into cells, not the first treatment
x: Sodium bicarbonate => Considered with severe acidosis and does not protect the heart

@k b:inflamarthritis 2L
s: A 39 year old man has had a painful swollen left knee for 3 weeks, and the whole of the second toe on his right foot is swollen like a sausage. His heels hurt when he first gets up. He has had flaky patches in his scalp for years, which he thought were dandruff. He has had no diarrhoea, urinary symptoms or new sexual partner. // There is a small effusion in the left knee and tenderness where both Achilles tendons insert.
$ CRP ; 22 mg/L ; <5
$ Rheumatoid factor ; negative ;
$ Uric acid ; 0.32 mmol/L ; 0.20–0.42
? Which is the most likely diagnosis?
> Gout ; *Psoriatic arthritis ; Reactive arthritis ; Rheumatoid arthritis ; Septic arthritis
= An asymmetrical oligoarthritis with dactylitis of a whole toe, heel enthesitis, a negative rheumatoid factor and unrecognised scalp psoriasis is psoriatic arthritis. Look for psoriasis in hidden places such as the scalp, natal cleft and umbilicus, and for nail pitting. With no infection beforehand, reactive arthritis is unlikely.
~ The same joints 2 weeks after chlamydia or a diarrhoeal illness, with conjunctivitis → reactive arthritis.
c: sausage | heels hurt | flaky patches in his scalp | no diarrhoea, urinary symptoms or new sexual partner | Rheumatoid factor negative
m: Inflammation starts at entheses, where tendons and ligaments insert into bone, and spreads to joints and whole digits
g: Dactylitis plus enthesitis plus psoriasis anywhere → psoriatic arthritis
f: the same joints 2 weeks after a chlamydia infection, with conjunctivitis and dysuria => Reactive arthritis
f: a hot red first toe joint overnight with a uric acid of 0.56 => Gout
f: symmetrical swelling of the knuckles and wrists with positive anti-CCP => Rheumatoid arthritis
x: Gout => Gives sudden severe attacks, usually of the first toe joint, and his urate is normal
x: Reactive arthritis => Follows a gut or genital infection, and he has had none
x: Rheumatoid arthritis => Symmetrical small joint disease, usually seropositive, without dactylitis
x: Septic arthritis => A hot, very painful single joint with fever, not dactylitis and enthesitis over weeks

@k b:inflamarthritis 3T
s: A 52 year old woman with plaque psoriasis for 20 years has had pain and stiffness in several fingers for 2 years. Her fingernails are pitted and lifting from the nail bed. Several distal interphalangeal joints are swollen, and her left index finger is shortened and unusually floppy. // An X-ray of both hands is requested.
? Which X-ray finding is most likely?
> Chondrocalcinosis of the wrist ; Joint space narrowing with osteophytes ; Periarticular osteopenia with marginal erosions ; *Pencil-in-cup deformity ; Punched-out erosions with overhanging edges
= Distal interphalangeal joint disease with nail pitting and onycholysis in long-standing psoriasis is psoriatic arthritis. Its X-ray signature is the end of one bone eroded into a pencil shape sitting in a cupped base, with new bone formation nearby. Severe destruction shortens the digit, which can telescope: arthritis mutilans.
~ Symmetrical knuckle and wrist disease with periarticular osteopenia and marginal erosions → rheumatoid arthritis.
c: plaque psoriasis for 20 years | pitted and lifting | distal interphalangeal | shortened and unusually floppy
m: Erosion eats away the end of one phalanx while bone proliferates at the base of the next, so the joint becomes a pencil sitting in a cup
g: Psoriatic DIP disease with nail changes → pencil-in-cup on X-ray
f: symmetrical swelling of the knuckles and wrists in a woman positive for rheumatoid factor => Periarticular osteopenia with marginal erosions
f: hard bony swellings at the DIP joints in a 70 year old with no psoriasis => Joint space narrowing with osteophytes
f: recurrent hot joints with tophi on the ears => Punched-out erosions with overhanging edges
x: Chondrocalcinosis of the wrist => The calcified cartilage of calcium pyrophosphate disease
x: Joint space narrowing with osteophytes => Osteoarthritis, which forms bony Heberden's nodes without nail disease
x: Periarticular osteopenia with marginal erosions => The pattern of rheumatoid arthritis, which spares the DIP joints
x: Punched-out erosions with overhanging edges => The pattern of chronic tophaceous gout

@k x:mca 2R
s: A 19 year old man with a severe learning disability needs several dental extractions under general anaesthetic for painful abscesses. He cannot understand or retain information about the procedure, even with pictures and support. His mother, who cares for him, offers to sign the consent form. He has no lasting power of attorney or deputy. The dentist, anaesthetist and family agree the treatment is needed.
? Which is the most appropriate way to proceed?
> Apply to the Court of Protection for a decision ; Ask his mother to sign the consent form ; *Make a best interests decision with his mother and the team ; Treat him under the Mental Health Act ; Wait until he can consent for himself
= He lacks capacity for this decision, and at 19 his mother cannot consent for him unless she holds a relevant lasting power of attorney or is a court-appointed deputy. Under the Mental Capacity Act the treating clinicians decide in his best interests, consulting his mother and others who know him, and record it, often at a best interests meeting.
~ No family or friends to consult about serious medical treatment → instruct an Independent Mental Capacity Advocate.
c: 19 year old | cannot understand or retain | offers to sign the consent form | no lasting power of attorney | agree the treatment is needed
m: For an adult who lacks capacity, consent passes to no one; the decision-maker acts in his best interests after consulting others
g: Adult lacking capacity with no LPA or deputy → best interests decision by the clinicians with the family
f: his mother and the team strongly disagree about whether major surgery is in his best interests => Apply to the Court of Protection for a decision
f: he is 15 and lacks Gillick competence => Ask his mother to sign the consent form
x: Apply to the Court of Protection for a decision => Kept for serious disputes or decisions such as withdrawing life-sustaining treatment
x: Ask his mother to sign the consent form => A parent cannot consent for an adult who lacks capacity
x: Treat him under the Mental Health Act => Covers treatment of mental disorder, not dental surgery
x: Wait until he can consent for himself => His incapacity is lifelong and he is in pain from abscesses now

@u 39 1R
s: A 26 year old woman has had hard, infrequent stools every 3 to 4 days for 2 months since starting a desk job. She strains and sometimes sees a little bright red blood on the paper. She eats mainly white bread, crisps and ready meals and drinks about 1 litre of fluid a day. She has not tried any changes or remedies. She has no weight loss and no family history of bowel cancer. // Abdominal examination is normal.
? Which is the most appropriate first step?
> Bisacodyl tablets ; *Increase dietary fibre and fluid intake ; Lactulose ; Macrogol sachets ; Refer for flexible sigmoidoscopy
= Recent constipation with a low-fibre diet, low fluid intake and inactivity, and no red flags, is managed first with lifestyle advice: more fibre from wholegrains, fruit and vegetables, more fluid and more activity. If that fails, a bulk-forming laxative such as ispaghula is added, then an osmotic laxative.
~ New constipation at 64 with weight loss and iron deficiency → urgent investigation for colorectal cancer.
c: since starting a desk job | white bread, crisps and ready meals | about 1 litre of fluid | not tried any changes | no weight loss
m: Fibre holds water in the stool and adds bulk, which speeds transit and softens the stool
g: Simple constipation with a poor diet and no red flags → fibre, fluid and activity first
f: stools still hard after 6 weeks of dietary change and a bulk-forming laxative => Macrogol sachets
x: Bisacodyl tablets => A stimulant laxative for when diet and softer laxatives are not enough
x: Lactulose => An osmotic laxative that causes bloating, used after diet and a bulk-forming laxative
x: Macrogol sachets => The usual next step if diet and a bulk-forming laxative fail
x: Refer for flexible sigmoidoscopy => She is young with no red flags, and small streaks of bright red blood with hard stools fit a fissure or haemorrhoids

@u 98 2L
s: A 48 year old woman has found it hard to climb stairs and to lift her arms to brush her hair for 3 months. She has become breathless on exertion and has a dry cough. The skin on the sides of her fingers is thickened and cracked. She has no rash on her face or knuckles. // Her shoulder and hip girdle muscles are weak. There are fine crackles at both lung bases.
$ Creatine kinase ; 4800 IU/L ; 25–200
$ ESR ; 38 mm/h ; <20
$ TSH ; 1.9 mU/L ; 0.3–4.2
? Which antibody is most likely to be positive?
> Anti-centromere ; Anti-cyclic citrullinated peptide ; Anti-double-stranded DNA ; *Anti-Jo-1 ; Anti-Scl-70
= Proximal weakness with a very high creatine kinase is an inflammatory myopathy, and with interstitial lung disease and thickened, cracked skin on the fingers, called mechanic's hands, it is the antisynthetase syndrome. Anti-Jo-1 is the classic antibody. Anti-Scl-70 also goes with lung fibrosis, but in systemic sclerosis, which does not raise the CK like this.
~ Skin tightening from the fingers up the arms, Raynaud's and lung fibrosis with a normal CK → anti-Scl-70 in diffuse systemic sclerosis.
c: climb stairs | lift her arms | dry cough | thickened and cracked | Creatine kinase 4800
m: Antibodies against histidyl-tRNA synthetase go with inflammation in muscle, lung and joints
g: Myositis plus interstitial lung disease plus mechanic's hands → anti-Jo-1
f: skin tightening from the fingers up the arms, Raynaud's and lung fibrosis with a normal CK => Anti-Scl-70
f: tight skin limited to the fingers and face with calcinosis and Raynaud's => Anti-centromere
f: a malar rash, mouth ulcers, arthritis and proteinuria => Anti-double-stranded DNA
x: Anti-centromere => Marks limited cutaneous systemic sclerosis, with Raynaud's and calcinosis, not myositis
x: Anti-cyclic citrullinated peptide => Specific for rheumatoid arthritis
x: Anti-double-stranded DNA => Specific for SLE, which causes a rash, arthritis and nephritis
x: Anti-Scl-70 => Linked to lung fibrosis in diffuse systemic sclerosis, which does not raise the CK like this

@u 20 2R
s: A 41 year old man who arrived from Pakistan 18 months ago has had a productive cough for 10 weeks, evening fevers, night sweats and 6 kg weight loss. // Temperature 37.8°C. There are crackles at the left apex. Chest X-ray shows left upper lobe consolidation with a small cavity. An HIV test is negative.
? Which investigation is most likely to confirm the diagnosis?
> Bronchoscopy with lavage ; CT chest ; Interferon gamma release assay ; Mantoux test ; *Sputum smear microscopy and culture
= Suspected active pulmonary TB is confirmed by sending at least 3 sputum samples, including an early morning one, for microscopy for acid-fast bacilli and mycobacterial culture, with rapid molecular testing for rifampicin resistance. Culture also gives drug sensitivities. IGRA and Mantoux tests show exposure, not active disease.
~ Cannot produce sputum even after induction → bronchoscopy with lavage.
c: Pakistan | 10 weeks | night sweats | 6 kg weight loss | small cavity
m: Acid-fast bacilli from the cavity are coughed up in sputum, seen with Ziehl-Neelsen or auramine stains and grown in culture
g: Suspected active pulmonary TB → 3 sputum samples for microscopy and culture
f: he cannot produce sputum even after nebulised hypertonic saline => Bronchoscopy with lavage
f: a healthcare worker with no symptoms and a normal chest X-ray after an exposure => Interferon gamma release assay
x: Bronchoscopy with lavage => Invasive and used when sputum cannot be obtained
x: CT chest => Shows the extent of disease but cannot identify the organism
x: Interferon gamma release assay => Detects infection but cannot tell latent from active disease
x: Mantoux test => Detects past exposure or BCG and cannot confirm active TB

@u 86 2L
s: A 58 year old retired builder has had pain on the top of his right shoulder for 6 months. It is worst when he reaches across his body to fasten a seatbelt and when he lifts his arm fully above his head. // There is a bony swelling and point tenderness over the acromioclavicular joint. Pain is reproduced by bringing the arm across the chest. Movement is painful in the last 20 degrees of abduction. External rotation is full.
? Which is the most likely diagnosis?
> *Acromioclavicular joint osteoarthritis ; Adhesive capsulitis ; Cervical radiculopathy ; Glenohumeral osteoarthritis ; Rotator cuff tendinopathy
= Pain on top of the shoulder with local tenderness and swelling of the acromioclavicular joint, pain on bringing the arm across the body and a painful arc at the top of abduction are acromioclavicular joint osteoarthritis. Rotator cuff tendinopathy gives a painful arc in the middle of abduction, and adhesive capsulitis loses external rotation.
~ A painful arc between 60 and 120 degrees with pain on resisted abduction → rotator cuff tendinopathy.
c: top of his right shoulder | reaches across his body | point tenderness over the acromioclavicular joint | last 20 degrees of abduction | External rotation is full
m: The worn joint is squeezed when the arm crosses the body or reaches the top of elevation
g: ACJ tenderness, pain across the body and a high painful arc → ACJ osteoarthritis
f: a painful arc between 60 and 120 degrees with pain on resisted abduction => Rotator cuff tendinopathy
f: global stiffness with loss of external rotation in a woman with diabetes => Adhesive capsulitis
f: neck pain with tingling down the arm into the thumb => Cervical radiculopathy
x: Adhesive capsulitis => Causes global stiffness, with external rotation lost first, and his is full
x: Cervical radiculopathy => Causes neck pain and symptoms down the arm in a dermatome
x: Glenohumeral osteoarthritis => Causes deep pain and loss of movement in every direction, especially rotation
x: Rotator cuff tendinopathy => Gives a painful arc in the middle of abduction, not tenderness over the ACJ

@k b:inflamarthritis 1L
s: A 45 year old woman has had pain and swelling in both hands for 4 months, with morning stiffness lasting 2 hours. Her knuckles and the middle joints of her fingers are affected on both sides, and her wrists ache. She has no rash or skin disease. // Both wrists and several metacarpophalangeal and proximal interphalangeal joints are swollen and tender. The distal interphalangeal joints are normal and there is no nail pitting.
$ CRP ; 34 mg/L ; <5
$ Rheumatoid factor ; positive ;
$ Anti-CCP antibodies ; strongly positive ;
? Which is the most likely diagnosis?
> Osteoarthritis ; Polymyalgia rheumatica ; Psoriatic arthritis ; *Rheumatoid arthritis ; Systemic lupus erythematosus
= A symmetrical inflammatory arthritis of the small joints of the hands and wrists, sparing the distal interphalangeal joints, with morning stiffness over an hour and positive rheumatoid factor and anti-CCP is rheumatoid arthritis. Anti-CCP is highly specific. She should be referred urgently to rheumatology to start a DMARD such as methotrexate.
~ Heberden's nodes at the DIP joints with brief morning stiffness and a normal CRP → osteoarthritis.
c: both hands | morning stiffness lasting 2 hours | knuckles and the middle joints | distal interphalangeal joints are normal | Anti-CCP antibodies strongly positive
m: Autoimmune synovitis thickens the joint lining, which erodes cartilage and bone at the joint margins
g: Symmetrical small joint synovitis with long morning stiffness and anti-CCP → RA
f: hard bony swellings at the DIP joints with 10 minutes of morning stiffness and a normal CRP => Osteoarthritis
f: DIP joint swelling with nail pitting and plaques on the elbows => Psoriatic arthritis
f: a 72 year old with shoulder and hip girdle stiffness and an ESR of 60 but no joint swelling => Polymyalgia rheumatica
x: Osteoarthritis => Affects the DIP joints and thumb base with short stiffness and no raised inflammatory markers
x: Polymyalgia rheumatica => Causes girdle stiffness in older people without small joint swelling
x: Psoriatic arthritis => Usually asymmetrical with DIP and nail involvement and a negative rheumatoid factor
x: Systemic lupus erythematosus => Causes a non-erosive arthritis with a rash, mouth ulcers and other organ involvement

@u 103 1L
s: A 29 year old man is brought in by his partner. For 10 days he has slept 2 hours a night, talked rapidly and spent £8,000 on cars he cannot afford. He says he is about to become a billionaire. Two years ago he had 4 months of low mood and could not work. He does not use drugs, and a urine drug screen is negative. // He is overactive, distractible and difficult to interrupt.
? Which is the most likely diagnosis?
> *Bipolar affective disorder ; Cyclothymia ; Emotionally unstable personality disorder ; Recurrent depressive disorder ; Schizophrenia
= An episode of elevated mood with little sleep, pressured speech, reckless spending and grandiosity lasting more than a week is mania, and with a previous depressive episode this is bipolar affective disorder. A negative drug screen makes a substance cause less likely. He needs urgent specialist assessment.
~ Several years of mild ups and downs that never reach mania or major depression → cyclothymia.
c: 10 days | slept 2 hours a night | spent £8,000 | billionaire | 4 months of low mood
m: Manic and depressive episodes recur in the same person, and disturbed sleep is often the first sign of a relapse
g: Mania for over a week plus past depression → bipolar affective disorder
f: several years of mild mood swings that never reach mania or major depression => Cyclothymia
f: mood that changes within hours, with self-harm and fear of abandonment => Emotionally unstable personality disorder
f: 6 months of hearing voices discussing him and believing his thoughts are broadcast, with normal mood => Schizophrenia
x: Cyclothymia => Mild persistent mood instability that never reaches full mania
x: Emotionally unstable personality disorder => Mood shifts within hours in reaction to events, not sustained mania for days
x: Recurrent depressive disorder => Cannot explain a manic episode
x: Schizophrenia => Grandiose ideas can occur, but the core here is a sustained mood episode with no first-rank symptoms

@u 23 2L
s: A 28 year old woman has had painful red lumps on both shins and painful swollen ankles for 2 weeks, with a dry cough and mild fever. She has not travelled and has no TB contacts. // Temperature 37.8°C. There are tender red nodules on both shins. Both ankles are swollen. Chest X-ray shows bilateral hilar lymphadenopathy with clear lung fields.
$ Adjusted calcium ; 2.68 mmol/L ; 2.20–2.60
$ Serum ACE ; 94 U/L ; 8–52
$ CRP ; 42 mg/L ; <5
? Which is the most likely diagnosis?
> Hodgkin lymphoma ; Hypersensitivity pneumonitis ; *Sarcoidosis ; Systemic lupus erythematosus ; Tuberculosis
= Erythema nodosum, bilateral hilar lymphadenopathy, ankle arthritis and fever are Löfgren's syndrome, an acute presentation of sarcoidosis. A raised ACE and mild hypercalcaemia support it. Löfgren's syndrome has an excellent prognosis and often settles with NSAIDs.
~ Night sweats, weight loss, itch and a mediastinal mass → Hodgkin lymphoma.
c: painful red lumps on both shins | swollen ankles | not travelled and has no TB contacts | bilateral hilar lymphadenopathy | Serum ACE 94
m: Non-caseating granulomas form in lymph nodes and lungs, and activated macrophages make ACE and active vitamin D
g: Erythema nodosum, bilateral hilar nodes and ankle arthritis → Löfgren's sarcoidosis
f: night sweats, weight loss, itching and a mediastinal mass with node pain after alcohol => Hodgkin lymphoma
f: cough, weight loss and a cavity after living with someone with smear-positive TB => Tuberculosis
f: breathlessness and fevers a few hours after cleaning out a pigeon loft => Hypersensitivity pneumonitis
x: Hodgkin lymphoma => Causes asymmetrical nodes with B symptoms, not erythema nodosum and ankle arthritis
x: Hypersensitivity pneumonitis => Follows antigen exposure and does not cause hilar lymphadenopathy
x: Systemic lupus erythematosus => Causes a rash, arthritis and serositis, not hilar lymphadenopathy
x: Tuberculosis => Can cause erythema nodosum but rarely symmetrical hilar nodes with ankle arthritis, and she has no exposure

@u 6 2L
s: A 66 year old man has had increasing breathlessness on exertion and swollen ankles for 3 months. He smokes and has type 2 diabetes. He drinks 6 units of alcohol a week. // BP 128/80 mmHg. There is no murmur. ECG shows Q waves in leads V1 to V4. Echocardiography shows a left ventricular ejection fraction of 32% with the anterior wall and apex not contracting, and normal valves.
$ NT-proBNP ; 2450 ng/L ; <400
? Which is the most likely underlying cause of his heart failure?
> Alcoholic cardiomyopathy ; Aortic stenosis ; Hypertensive heart disease ; *Ischaemic heart disease ; Viral myocarditis
= Heart failure with a reduced ejection fraction in a smoker with diabetes, with Q waves in the anterior leads and an anterior wall and apex that do not contract, points to a previous silent infarct: ischaemic heart disease. It is the commonest cause of heart failure in the UK. Loss of movement in one region separates it from the global weakness of a cardiomyopathy.
~ Globally poor contraction with dilated chambers in a man drinking 80 units a week → alcoholic cardiomyopathy.
c: smokes | type 2 diabetes | 6 units | Q waves in leads V1 to V4 | anterior wall and apex not contracting
m: Infarcted muscle in the territory of the left anterior descending artery is replaced by scar that cannot contract
g: Regional wall motion loss with Q waves → ischaemic cardiomyopathy
f: globally poor contraction with dilated chambers in a man drinking 80 units a week => Alcoholic cardiomyopathy
f: an ejection systolic murmur radiating to the carotids and a valve area of 0.7 square centimetres => Aortic stenosis
f: a 25 year old breathless 2 weeks after a flu-like illness, with a raised troponin and global hypokinesia => Viral myocarditis
x: Alcoholic cardiomyopathy => He drinks little, and it causes global rather than regional weakness
x: Aortic stenosis => There is no murmur and the valves are normal
x: Hypertensive heart disease => His blood pressure is normal, and it usually thickens the ventricle evenly
x: Viral myocarditis => Follows a viral illness in younger people and causes global dysfunction

@u 76 1L
s: A 74 year old man has had worsening back pain for 2 months that wakes him at night. He has had a weak urinary stream and nocturia for a year. He has lost 5 kg. // Rectal examination shows a hard, irregular prostate with no midline sulcus. There is tenderness over the lumbar spine. Urine dipstick is normal.
$ PSA ; 186 µg/L ; <6.5
$ ALP ; 486 IU/L ; 25–115
$ Adjusted calcium ; 2.52 mmol/L ; 2.20–2.60
$ Haemoglobin ; 112 g/L ; 130–175
? Which is the most likely diagnosis?
> Benign prostatic hyperplasia ; Bladder cancer ; Multiple myeloma ; *Prostate cancer with bone metastases ; Spinal tuberculosis
= A hard irregular prostate, a very high PSA, back pain at night, weight loss and a raised ALP are prostate cancer with sclerotic bone metastases. Bladder cancer presents with painless haematuria. He needs urgent assessment, including the risk of spinal cord compression, and androgen deprivation therapy.
~ Painless visible haematuria with a normal prostate and PSA → bladder cancer.
c: wakes him at night | weak urinary stream | lost 5 kg | hard, irregular prostate | PSA 186
m: Prostate cancer spreads through the vertebral venous plexus to the spine, where it stimulates osteoblasts and raises the ALP
g: Hard irregular prostate, very high PSA, bone pain and a high ALP → metastatic prostate cancer
f: painless visible haematuria with a normal feeling prostate and a PSA of 2 => Bladder cancer
f: a smooth enlarged prostate, a PSA of 4.8 and no back pain or weight loss => Benign prostatic hyperplasia
f: back pain with a calcium of 3.1, a normal ALP and a paraprotein on electrophoresis => Multiple myeloma
x: Benign prostatic hyperplasia => Causes a smooth enlarged prostate with a modest PSA rise, not bone pain and weight loss
x: Bladder cancer => Presents with painless haematuria, and his urine is clear
x: Multiple myeloma => Causes lytic lesions with a normal ALP and often a high calcium
x: Spinal tuberculosis => Causes back pain with fever and sweats, not an irregular prostate and a high PSA

@u 60 1L
s: A 78 year old woman with atrial fibrillation stopped her apixaban a month ago because of nosebleeds. Two hours ago she had sudden severe pain in her right leg, which became cold and numb. She has never had leg pain on walking. // Pulse irregularly irregular, 104 bpm. The right leg is pale and cold below the knee with no pulses below the femoral. The left leg has normal pulses. Sensation is reduced in the right foot.
? Which is the most likely cause?
> *Acute arterial embolus ; Acute thrombosis on existing atherosclerosis ; Compartment syndrome ; Deep vein thrombosis ; Popliteal aneurysm thrombosis
= Sudden onset over minutes in a patient with atrial fibrillation off anticoagulation, no history of claudication and normal pulses in the other leg is an embolus lodging where the artery divides. Reduced sensation means the limb is threatened: give IV heparin and arrange urgent embolectomy.
~ Worsening over days in a smoker with years of claudication and weak pulses in both legs → thrombosis on existing atherosclerosis.
c: atrial fibrillation | stopped her apixaban | sudden severe pain | never had leg pain on walking | left leg has normal pulses
m: Clot forms in the left atrium during AF, breaks off and lodges where the artery divides, cutting off flow before collaterals can develop
g: Sudden ischaemia, AF and normal pulses in the other leg → embolus
f: worsening over days in a smoker with years of claudication and weak pulses in both legs => Acute thrombosis on existing atherosclerosis
f: a pulsatile swelling behind the other knee as well => Popliteal aneurysm thrombosis
f: a swollen, warm, red calf with the foot pulses present => Deep vein thrombosis
x: Acute thrombosis on existing atherosclerosis => Usually follows claudication, and the other leg would have weak pulses
x: Compartment syndrome => Follows trauma or reperfusion, with a tense swollen compartment and pain on stretching
x: Deep vein thrombosis => Makes the leg swollen and warm, not pale, cold and pulseless
x: Popliteal aneurysm thrombosis => Possible, but there is no pulsatile swelling, and AF off anticoagulation makes an embolus far likelier

@k b:inflamarthritis 2L
s: A 47 year old man shows his hands to his GP. The end joints of 3 fingers on his left hand are swollen and red, and his whole right middle finger is swollen like a sausage. Several nails have small pits, and 2 are lifting from the nail bed. There are well-defined red plaques with silvery scale on both elbows. He has no hard bony swellings and no tophi. // His hand X-ray shows erosions with fluffy new bone at the end joints.
? Which is the most likely diagnosis?
> Gout ; Heberden's nodes of osteoarthritis ; *Psoriatic arthritis ; Rheumatoid arthritis ; Systemic lupus erythematosus
= Distal interphalangeal joint arthritis, dactylitis, nail pitting and onycholysis with plaque psoriasis are psoriatic arthritis. Nail disease is the strongest clinical marker of who with psoriasis will develop arthritis. Erosions with fluffy new bone distinguish it from rheumatoid arthritis and osteoarthritis.
~ Hard, non-inflamed bony swellings at the DIP joints in an older woman without psoriasis → Heberden's nodes of osteoarthritis.
c: end joints of 3 fingers | swollen like a sausage | small pits | lifting from the nail bed | silvery scale
m: Inflammation at the entheses and nail beds spreads into the DIP joints, with both erosion and new bone
g: DIP arthritis with nail pitting, dactylitis and plaques → psoriatic arthritis
f: hard, non-inflamed bony swellings at the DIP joints in a 70 year old woman with no psoriasis => Heberden's nodes of osteoarthritis
f: chalky nodules over the knuckles and ears with a uric acid of 0.62 => Gout
f: symmetrical swelling of the knuckles and wrists with ulnar deviation => Rheumatoid arthritis
x: Gout => Can affect the fingers but causes tophi and acute attacks, not nail pitting and dactylitis
x: Heberden's nodes of osteoarthritis => Hard bony swellings without redness, nail pitting or dactylitis
x: Rheumatoid arthritis => Spares the DIP joints and affects the knuckles and wrists symmetrically
x: Systemic lupus erythematosus => Causes a non-erosive arthritis with a rash, not DIP erosions and nail pitting

@k b:otosclerosis 2L
s: A 32 year old woman has had gradually worsening hearing in both ears for 3 years, worse since the birth of her daughter. She hears better in noisy places. Her father wore hearing aids from his 40s. // Both eardrums look normal and move normally. Rinne's test is negative on both sides and Weber's test is central. Audiometry shows a conductive hearing loss in both ears with a dip in bone conduction at 2 kHz.
? Which is the most likely diagnosis?
> Cholesteatoma ; Noise-induced hearing loss ; Otitis media with effusion ; *Otosclerosis ; Vestibular schwannoma
= Progressive conductive hearing loss with normal eardrums in a young woman, worse after pregnancy and with a family history, is otosclerosis: new bone fixes the stapes footplate. Hearing better in background noise and a dip in bone conduction at 2 kHz, the Carhart notch, are classic. Hearing aids or stapes surgery help.
~ A dull, retracted eardrum with a flat tympanogram after a cold → otitis media with effusion.
c: both ears for 3 years | since the birth of her daughter | hears better in noisy places | father | eardrums look normal
m: Abnormal bone remodelling around the oval window fixes the stapes, so sound is not passed to the cochlea
g: Conductive loss with normal eardrums, a family history and worsening in pregnancy → otosclerosis
f: a dull, retracted eardrum with a flat tympanogram after a cold => Otitis media with effusion
f: a foul-smelling discharge with white debris in a pocket of the eardrum => Cholesteatoma
f: sensorineural loss in one ear with tinnitus and imbalance => Vestibular schwannoma
x: Cholesteatoma => Causes a smelly discharge with an abnormal eardrum
x: Noise-induced hearing loss => Sensorineural, with a notch at 4 kHz
x: Otitis media with effusion => The eardrums would be dull and would not move normally
x: Vestibular schwannoma => Causes sensorineural loss in one ear

@k b:vasculitis 2L
s: A 74 year old woman has had a new headache over her right temple for 2 weeks and pain in her jaw when chewing that makes her stop eating. Her scalp hurts when she brushes her hair. Her shoulders have been stiff in the mornings. She has no nasal symptoms, cough or blood in her urine. // The right temporal artery is thickened and tender with a reduced pulse. Visual acuity is normal.
$ ESR ; 92 mm/h ; <30
$ CRP ; 68 mg/L ; <5
$ Platelets ; 486 × 10⁹/L ; 150–400
? Which is the most likely diagnosis?
> Cluster headache ; *Giant cell arteritis ; Granulomatosis with polyangiitis ; Polymyalgia rheumatica ; Trigeminal neuralgia
= A new temporal headache over the age of 50 with jaw claudication, scalp tenderness, a thickened tender temporal artery and a very high ESR is giant cell arteritis. The shoulder stiffness is associated polymyalgia. Start high-dose prednisolone immediately to protect her sight, and arrange temporal artery ultrasound or biopsy.
~ Bloody nasal crusting, haemoptysis, haematuria and a positive c-ANCA → granulomatosis with polyangiitis.
c: over her right temple | pain in her jaw when chewing | scalp hurts | no nasal symptoms, cough or blood in her urine | ESR 92
m: Granulomatous inflammation of branches of the external carotid narrows the lumen, so the chewing muscles and optic nerve are starved of blood
g: Over 50 with a new headache, jaw claudication and a high ESR → GCA: steroids now
f: bloody nasal crusting, haemoptysis and haematuria with a positive c-ANCA => Granulomatosis with polyangiitis
f: shoulder and hip girdle stiffness with a raised ESR but no headache or jaw pain => Polymyalgia rheumatica
f: electric shocks of pain in the cheek triggered by brushing her teeth => Trigeminal neuralgia
x: Cluster headache => Causes severe attacks around one eye with a watering eye, usually in younger men
x: Granulomatosis with polyangiitis => Involves the nose, lungs and kidneys, which are clear here
x: Polymyalgia rheumatica => Explains the shoulder stiffness but not the headache, jaw claudication and abnormal artery
x: Trigeminal neuralgia => Brief electric shock pains without jaw claudication or a raised ESR

@u 57 2L
s: A 61 year old woman with breast cancer known to have spread to her spine has become confused and drowsy over 4 days. She has been very thirsty, passing large volumes of urine and is constipated. Her morphine dose has not changed. // She is dehydrated and drowsy but has no focal neurological signs.
$ Adjusted calcium ; 3.46 mmol/L ; 2.20–2.60
$ Sodium ; 141 mmol/L ; 135–146
$ Glucose ; 6.2 mmol/L ; 4.0–7.8
$ Creatinine ; 128 µmol/L ; 45–90
$ PTH ; 0.6 pmol/L ; 1.6–8.5
? Which is the most likely cause of her confusion?
> Brain metastases ; *Hypercalcaemia ; Hypoglycaemia ; Hyponatraemia ; Opioid toxicity
= Confusion, thirst, polyuria, constipation and dehydration with an adjusted calcium of 3.46 and a suppressed PTH are hypercalcaemia of malignancy, from bone metastases and PTH-related peptide. It is an oncological emergency: give IV 0.9% saline, then an IV bisphosphonate such as zoledronic acid.
~ Confusion with headache, vomiting and new focal weakness in metastatic breast cancer → brain metastases.
c: spread to her spine | very thirsty, passing large volumes | constipated | morphine dose has not changed | Adjusted calcium 3.46
m: Bone metastases and tumour PTH-related peptide release calcium from bone, which slows nerve conduction and stops the kidney concentrating urine
g: Confusion, thirst, polyuria and constipation in cancer with a high calcium → hypercalcaemia: fluids then a bisphosphonate
f: headache, vomiting and new weakness of the left arm => Brain metastases
f: a sodium of 118 with euvolaemia and concentrated urine => Hyponatraemia
f: pinpoint pupils and a respiratory rate of 8 after her morphine dose was doubled => Opioid toxicity
x: Brain metastases => Usually cause headache, vomiting or focal signs, and she has none
x: Hypoglycaemia => Her glucose is normal
x: Hyponatraemia => Her sodium is normal
x: Opioid toxicity => Her dose is unchanged, and opioids do not cause thirst and polyuria

@u 17 3R
s: A 61 year old woman with bronchiectasis has had more sputum than usual for 5 days, now dark green, with increased breathlessness. She has been started on oral ciprofloxacin, based on previous sputum cultures growing Pseudomonas aeruginosa. She is not currently doing any regular airway clearance. // Temperature 37.6°C, oxygen saturation 95% breathing air. There are coarse crackles at both bases with scattered wheeze.
? Which is the most appropriate treatment to add to her antibiotic?
> *Airway clearance physiotherapy ; Inhaled corticosteroid ; Long-term oral prednisolone ; Montelukast ; Oral theophylline
= Airway clearance techniques, such as the active cycle of breathing, taught by a respiratory physiotherapist are a cornerstone of bronchiectasis care, during an exacerbation and long term. British Thoracic Society guidance is that everyone with bronchiectasis is taught airway clearance. Inhaled steroids are not used routinely unless there is coexisting asthma or COPD.
~ Wheeze with variable airflow obstruction and raised eosinophils alongside bronchiectasis → an inhaled corticosteroid for coexisting asthma.
c: bronchiectasis | more sputum than usual | Pseudomonas aeruginosa | not currently doing any regular airway clearance
m: Mucus pooling in dilated airways keeps bacteria multiplying, and clearing it breaks the cycle of infection and inflammation
g: Bronchiectasis exacerbation → antibiotic plus airway clearance physiotherapy
f: wheeze with variable airflow obstruction and blood eosinophils of 0.8 alongside her bronchiectasis => Inhaled corticosteroid
x: Inhaled corticosteroid => Not recommended in bronchiectasis unless there is coexisting asthma or COPD
x: Long-term oral prednisolone => Raises the risk of infection and has no role in routine bronchiectasis care
x: Montelukast => An asthma drug with no role in bronchiectasis
x: Oral theophylline => A weak bronchodilator with a narrow therapeutic range that does not clear sputum, and ciprofloxacin raises its level

@k b:dysphagia 2L
s: A 76 year old man has had difficulty swallowing for 6 months. Food sticks high in his throat, he regurgitates undigested food hours after meals and his neck gurgles when he drinks. His wife has noticed bad breath, and he has had a chest infection. He has lost 2 kg. // There is a soft swelling on the left side of the neck that gurgles on pressure.
? Which is the most likely diagnosis?
> Achalasia ; Oesophageal carcinoma ; Oesophageal web ; *Pharyngeal pouch ; Thyroid goitre
= Difficulty swallowing high in the throat, regurgitation of undigested food long after meals, gurgling, bad breath, aspiration and a neck swelling in an older man are a pharyngeal pouch, or Zenker's diverticulum, bulging through Killian's dehiscence. A barium swallow confirms it, because blind endoscopy risks perforating the pouch.
~ Difficulty with both solids and liquids from the start and a bird's beak on barium swallow → achalasia.
c: high in his throat | undigested food hours after meals | gurgles | bad breath | left side of the neck
m: Weak muscle between thyropharyngeus and cricopharyngeus lets the lining bulge out and trap food above a tight upper sphincter
g: High dysphagia, undigested regurgitation, gurgling and bad breath in an older man → pharyngeal pouch
f: difficulty with solids and liquids from the start and a bird's beak on barium swallow => Achalasia
f: dysphagia for solids then liquids over 2 months with 9 kg weight loss => Oesophageal carcinoma
f: dysphagia with iron deficiency anaemia and glossitis in a middle-aged woman => Oesophageal web
x: Achalasia => Affects the lower oesophagus with dysphagia for liquids and solids, without a neck swelling
x: Oesophageal carcinoma => Gives rapidly progressive dysphagia with marked weight loss rather than gurgling and undigested regurgitation
x: Oesophageal web => The upper oesophageal web of Plummer-Vinson syndrome comes with iron deficiency
x: Thyroid goitre => Moves on swallowing and does not gurgle or fill with food

@k x:upperscope 2R
s: A 66 year old man has had difficulty swallowing for 6 weeks. Solid food such as meat and bread sticks behind his breastbone, but he can drink liquids without difficulty. It is getting worse. He has had heartburn for years and has lost 5 kg. // Abdominal examination is normal.
? Which is the most appropriate investigation?
> Barium swallow ; CT chest and abdomen ; Oesophageal manometry ; Trial of a proton pump inhibitor ; *Urgent upper GI endoscopy
= Progressive dysphagia for solids with liquids still passing points to a mechanical narrowing, such as a carcinoma or a peptic stricture. NICE recommends an urgent direct access upper GI endoscopy for anyone with dysphagia, and he also has weight loss and long-standing reflux. Endoscopy allows a biopsy.
~ Difficulty with solids and liquids from the start → a motility disorder such as achalasia, investigated with manometry after endoscopy.
c: Solid food such as meat and bread sticks | drink liquids without difficulty | getting worse | heartburn for years | lost 5 kg
m: A fixed narrowing lets fluids pass but blocks a solid bolus, and it worsens as a tumour grows
g: Dysphagia, especially with weight loss → urgent upper GI endoscopy
f: high dysphagia, gurgling and regurgitation of food eaten the day before in a 78 year old => Barium swallow
f: dysphagia for solids and liquids from the start with a normal endoscopy => Oesophageal manometry
x: Barium swallow => Used first when a pharyngeal pouch is suspected, but it cannot take a biopsy
x: CT chest and abdomen => Stages a cancer once found but is not the diagnostic test
x: Oesophageal manometry => Assesses motility disorders after endoscopy has excluded a structural cause
x: Trial of a proton pump inhibitor => Dysphagia with weight loss needs endoscopy, not a trial of treatment

@k d:cdiff 1D
s: A 79 year old woman developed watery diarrhoea 6 times a day, 5 days after starting co-amoxiclav for a chest infection. She has mild lower abdominal cramps. This is her first episode. // Temperature 37.6°C, pulse rate 92 bpm, BP 124/78 mmHg. The abdomen is soft and mildly tender.
$ Clostridioides difficile toxin ; positive ;
$ White cell count ; 12.8 × 10⁹/L ; 4.0–11.0
$ Creatinine ; 82 µmol/L ; 45–90
? In addition to stopping co-amoxiclav, which is the most appropriate treatment?
> Fidaxomicin ; IV vancomycin ; Loperamide ; Oral metronidazole ; *Oral vancomycin
= A first episode of C. difficile infection that is not life-threatening is treated with oral vancomycin 125 mg 4 times a day for 10 days, after stopping the causative antibiotic where possible. Fidaxomicin is second line, or used for a recurrence within 12 weeks. Metronidazole is no longer recommended first line, and IV vancomycin does not reach the bowel.
~ A recurrence within 12 weeks of the first episode settling → fidaxomicin.
c: co-amoxiclav | first episode | Temperature 37.6 | Clostridioides difficile toxin positive
m: Antibiotics wipe out the normal colonic flora, so C. difficile spores germinate and release toxins that damage the colonic lining
g: First non-severe C. difficile → oral vancomycin for 10 days
f: a recurrence 6 weeks after the first episode settled => Fidaxomicin
x: Fidaxomicin => Second line, or the choice for a recurrence within 12 weeks
x: IV vancomycin => Is not excreted into the bowel, so it does not reach the infection
x: Loperamide => Antimotility drugs risk toxic megacolon and should be avoided
x: Oral metronidazole => No longer recommended first line because it is less effective

@u 134 1L
s: A 61 year old man with type 2 diabetes has a thickened, yellow, crumbly big toenail on his right foot that has slowly worsened over 2 years. White debris builds up under the nail. The skin between his 4th and 5th toes is itchy and peeling. // His other nails are normal. There are no skin plaques, nail pits or redness around the nail fold.
? Which is the most likely diagnosis?
> Chronic paronychia ; Nail psoriasis ; *Onychomycosis ; Subungual haematoma ; Subungual melanoma
= A slowly thickening, yellow, crumbly toenail with debris underneath, together with athlete's foot between the toes, is onychomycosis, usually from Trichophyton rubrum. Nail clippings should be sent for microscopy and culture before treatment. Oral terbinafine for 3 months is first line for toenails if treatment is wanted.
~ Pitting and lifting of several nails with plaques on the elbows → nail psoriasis.
c: thickened, yellow, crumbly | slowly worsened over 2 years | White debris | between his 4th and 5th toes is itchy and peeling | no skin plaques, nail pits
m: Dermatophytes spread from the skin of the foot into the nail bed and digest keratin, so the nail thickens and crumbles
g: Thick yellow crumbly nail with debris and athlete's foot → onychomycosis: clippings before terbinafine
f: pitting and lifting of several fingernails with plaques on the elbows => Nail psoriasis
f: a dark brown streak in the nail that has widened and spread onto the nail fold => Subungual melanoma
f: a swollen, red, tender nail fold in a cleaner whose hands are often wet => Chronic paronychia
x: Chronic paronychia => Inflames the nail fold, which is normal here
x: Nail psoriasis => Causes pitting and lifting, usually with skin plaques elsewhere
x: Subungual haematoma => Follows an injury, with a dark red-purple area that grows out with the nail
x: Subungual melanoma => Gives a pigmented streak that can spread onto the nail fold
"""
