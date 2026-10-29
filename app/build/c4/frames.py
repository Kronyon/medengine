from .common import item

def F(t, kind, spec):
    return {'t': t, 'kind': kind, 'secs': [{'h': h, 'items': [item(x) for x in xs]} for h, xs in spec]}

FRAMES = {
  'xopen': F('Opening: WIPER', 'xopen', [('', [
    '!Wash your hands visibly as you walk in || || Examiners tick what they see.',
    '!Introduce yourself; confirm name and date of birth || Hello, I\'m Nana, a fourth-year medical student. Could you tell me your full name and date of birth? || ',
    '!Permission: explain the examination and get consent; offer a chaperone || I\'ve been asked to examine you today. It involves me looking, feeling and listening. Is that OK? Would you like a chaperone? || ',
    'Expose appropriately and Reposition; ask about pain || Is there any pain anywhere before I start? || WIPER: Wash, Introduce, Permission, Expose, Reposition.',
  ])]),
  'xclose': F('Closing', 'xclose', [('', [
    'Thank the patient, offer help to dress, wash your hands || Thank you. I\'ll let you get dressed. || ',
    '!Present: summary, key positive and negative findings, most likely diagnosis, how you would complete the examination || || ',
  ])]),
  'popen': F('Opening a procedure', 'popen', [('', [
    '!Hand hygiene, introduce, confirm identity with name, date of birth and wristband || || ',
    '!Explain the procedure, why it is needed, what it will feel like; consent || || ',
    '!Allergies: latex, chlorhexidine, plasters, lidocaine || Do you have any allergies, for example to plasters, latex or cleaning wipes? || ',
    'Check the request or prescription; gather equipment; clean the tray; gloves and apron || || ',
  ])]),
  'pclose': F('Closing a procedure', 'pclose', [('', [
    '!Sharps straight into the bin; clinical waste; hand hygiene || || ',
    '!Document: what, when, site, size or results, complications; label samples at the bedside || || ',
    'Thank the patient; check they are comfortable; safety-net about the site || If the area becomes red, swollen or painful, tell the nurse. || ',
  ])]),
  'pres': F('Present to the examiner', 'pres', [('', [
    '!Signal the switch, then summarise in one or two sentences: who, what, how long, key positives and negatives || Thank you. I\'d now like to present to the examiner. Mr Jones is a 61-year-old smoker with 45 minutes of central crushing chest pain... || Stop gathering at 8 minutes to protect this.',
    '!Most likely diagnosis and the clue that clinches it || The most likely diagnosis is ___ because ___. || ',
    '!The dangerous alternative and how you would exclude it || The important thing to exclude is ___, which I\'d do with ___. || ',
    'Investigations: bedside, bloods, imaging || I would like an ECG, troponin and a chest X-ray. || ',
    'First steps of management if asked || || ',
  ])]),
  'open': F('Opening the station', 'open', [('', [
    'Read the door twice; underline every task verb || || Every verb on the door is a marked domain. Miss a verb and you lose the whole domain.',
    'Hand hygiene as you walk in, visibly || || Examiners tick what they see.',
    'Introduce yourself: name and role || Hello, my name is Nana, I\'m a fourth-year medical student. || The actor is asked afterwards whether they would want you as their doctor.',
    '!Confirm name and date of birth || Can I check your full name and date of birth, please? || Patient identification is a safety mark.',
    '!Explain why you are here and gain consent; check comfort || I\'ve been asked to talk with you about what brought you in today. Is that OK? Are you comfortable? || No consent means no marks for what follows.',
  ])]),
  'hx': F('History: the skeleton', 'hx', [
    ('Open and listen', [
      'Open question, then the golden minute without interrupting || In your own words, what\'s been happening? || The key clue usually comes in their second sentence. Count to two after they stop.',
      'Pick up a cue and reflect it back || You mentioned your dad. Tell me more about that. || Picking up a cue is how Communication scores 3 or 4 rather than 2.',
    ]),
    ('The complaint', [
      'SOCRATES for pain; for anything else: onset, duration, pattern, getting better or worse || Where exactly is it? When did it start, and was it sudden or gradual? || A timeline sorts acute, subacute and chronic causes before you think of a diagnosis.',
      '!Discriminating questions that split your top 2 or 3 || Is there anything that makes it better or worse? || Questions that change your differential are what Information gathering really marks.',
      '!Red flags for this presentation: see the 🚩 card || Have you noticed any weight loss, night sweats, bleeding, or anything else that worried you? || Missing the red flag is the commonest reason for a borderline fail.',
      'Focused systems review || || Catches the second problem the actor only reveals if asked.',
    ]),
    ('Background', [
      'Past history: MJ THREADS, plus operations || Do you have any other medical problems, or have you had any operations? || MJ THREADS: MI, Jaundice, TB, Hypertension, Rheumatic fever, Epilepsy, Asthma and COPD, Diabetes, Stroke.',
      '!Drugs, bought medicines, herbal, adherence; allergies and what happened || What medicines do you take, including anything you buy yourself? Any allergies, and what happened when you had it? || A drug cause is a favourite twist. Rash versus anaphylaxis changes what you can prescribe.',
      'Family history || Does anything run in the family, like heart problems, cancer or sudden deaths under 40? || Family history unlocks risk: early heart disease, bowel cancer, sudden death.',
      'Social: SADDO, plus who is at home || Do you smoke? How much do you drink in a week? What do you do for work? Who is at home? || SADDO: Smoking in pack-years, Alcohol in units, Drugs, Driving, Occupation. Driving matters for fits, faints, diabetes and eyesight.',
    ]),
    ('Their view, then wrap up', [
      '!ICE, and the impact on their life || What have you been thinking it might be? Is anything worrying you in particular? How is it affecting you day to day? || The actor has a hidden worry waiting to be asked.',
      'Signpost each move; summarise back and check || Thank you. I\'d now like to ask about your general health. ... Let me check I\'ve got this right. || Signposting and summarising were both flagged in your feedback.',
      'Stop at 8 minutes and turn to the examiner || || A finished presentation scores more than a perfect social history.',
    ]),
  ]),
  'mhx': F('Psychiatric history: the skeleton', 'hx', [
    ('Rapport and their story', [
      'Warm, unhurried open question; acknowledge distress || It sounds like things have been really hard recently. Take your time. || Distressed people only disclose risk to someone who feels safe.',
      'Their story: onset, trigger, course, impact || When did you first notice things changing? Did anything set it off? || Onset and trigger separate adjustment, depression, bipolar and physical causes.',
    ]),
    ('Screen every syndrome', [
      'Mood: low mood plus SIGECAPS || How has your mood been? How are you sleeping and eating? || SIGECAPS: Sleep, Interest, Guilt, Energy, Concentration, Appetite, Psychomotor, Suicide.',
      'Mania: DIGFAST, even when it looks like depression || Have there been times you felt the opposite: full of energy, hardly needing sleep? || Missing bipolar changes the treatment: an antidepressant alone can tip someone into mania.',
      'Anxiety and psychosis, asked in a normalising way || Sometimes when people are under a lot of stress they hear or see things others don\'t. Has that happened to you? || Normalising gets honest answers about voices, compulsions or purging.',
    ]),
    ('Risk, always', [
      '!Suicide: thoughts, plans, intent, means, preparation, what keeps them going || Sometimes when people feel this low they think about ending their life. Have you had thoughts like that? || Asking directly does not put the idea into someone\'s head.',
      '!Risk to others, from others, self-neglect; who is at home || Are there any children at home, or anyone who depends on you? || Safeguarding is a named mark in every mental health station.',
    ]),
    ('Background', [
      'Past psychiatric history: episodes, admissions, Mental Health Act, what helped || Have you ever had help for your mental health before? What helped? || What helped before predicts what will help now.',
      '!Alcohol and drugs, counted || How much alcohol do you drink in a typical week? Any other drugs? || Substances cause, mimic and worsen almost every presentation.',
      'Medical, family and personal history: thyroid, head injury, medicines; family suicide; childhood, work, money, relationships, police || || Physical causes come off the list first; family history raises the risk.',
    ]),
    ('Their view, then wrap up', [
      '!Insight and ICE: what they think is going on and what they want today || What do you think is going on? What would you like to get out of today? || Insight predicts engagement and goes in every MSE presentation.',
      'Summarise, then a risk formulation: what raises and lowers the risk right now || || Formulate, don\'t score: NICE advises against using risk scales to predict suicide.',
    ]),
  ]),
  'hxclose': F('Closing a history', 'hxclose', [('', [
    'Thank them, tell them what happens next, gel your hands || Thank you, that\'s really helpful. I\'m going to talk to my colleague now. || A courteous close leaves the actor scoring you highly.',
  ])]),
}
