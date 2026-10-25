from .common import item

def F(t, kind, spec):
    return {'t': t, 'kind': kind, 'secs': [{'h': h, 'items': [item(x) for x in xs]} for h, xs in spec]}

FRAMES = {
  'xopen': F('Opening: WIPER', 'xopen', [('', [
    '!Wash your hands visibly as you walk in || || Examiners tick what they see.',
    '!Introduce yourself; confirm name and date of birth || Hello, I\'m Nana, a third-year medical student. Could you tell me your full name and date of birth? || ',
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
}
