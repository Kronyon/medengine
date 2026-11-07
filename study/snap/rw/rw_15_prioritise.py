"""v3.6.18 (part 3): from recall to prioritisation.
A question where the classic pair (amitriptyline -> bicarbonate) is the only option from the right world tests a
reflex, not a decision. Official papers keep the classic answer but add other things you might really do in that
scenario, so you must rank them: here fluids for the hypotension and charcoal for the ingestion sit beside
bicarbonate, and the stem detail (QRS 140 ms, 3 hours, drowsy) decides. Applied by site/patches/v364_rw.py as data
version 17."""
R = {
 'h0471': {'o': [('Sodium bicarbonate', 'IV 8.4% sodium bicarbonate', None),
                 ('Intravenous amiodarone', 'IV amiodarone', 'keep'),
                 ('Intravenous flumazenil', 'IV flumazenil', 'keep'),
                 ('Intravenous magnesium sulfate', 'Activated charcoal', 'Charcoal is for a tricyclic taken within 1 hour with a protected airway; she is 3 hours out and drowsy, so it risks aspiration.'),
                 ('Intravenous naloxone', 'IV 0.9% sodium chloride bolus', 'Fluids help the blood pressure, but a QRS of 140 ms needs sodium bicarbonate, which treats the sodium channel block and the hypotension.')],
           'f': {'Activated charcoal': 'within 1 hour of the overdose, alert, with a normal QRS',
                 'IV 0.9% sodium chloride bolus': 'hypotension with a normal QRS and no arrhythmia'}},
 'h1221': {'o': [('Intravenous naloxone bolus', 'Activated charcoal 50 g', 'Charcoal is given within 1 hour and only with a protected airway; at 2 hours with a GCS of 10 it risks aspiration and does not treat the QRS.')],
           'f': {'Activated charcoal 50 g': 'within 1 hour of the overdose, alert, with a normal ECG'}},
 'h0851': {'o': [('Supportive care without flumazenil', 'Supportive care and observation', None),
                 ('Physostigmine', 'Intubation and ventilation', 'He is rousable, breathing 14 times a minute and protecting his airway; intubation is for a falling GCS or failing breathing.')],
           'f': {'Intubation and ventilation': 'GCS 8 with snoring respirations and a rising carbon dioxide'}},
 'h0444': {'o': [('Self-help leaflet and helpline', 'Urgent referral within a week', 'A plan with a date, possessions given away and goodbye letters mean imminent risk; a week is too long, so he needs crisis assessment today.')],
           'f': {'Urgent referral within a week': 'passive thoughts of death with no plan or intent and good support at home'}},
 'h0441': {'o': [('Liver function', 'Clozapine level', 'A level checks toxicity or adherence; fever and a sore throat on clozapine mean agranulocytosis until the neutrophil count is known.')],
           'f': {'Clozapine level': 'drowsiness and drooling after she stopped smoking'}},
 'h1086': {'o': [('Triptan if it recurs', 'Same-day emergency eye referral', 'Vision has fully recovered and the eye is normal; brief curtain-like loss is a retinal TIA, managed through the TIA pathway with aspirin.')],
           'f': {'Same-day emergency eye referral': 'vision still lost with a pale retina and a cherry-red spot'}},
 'h0990': {'o': [('Oral antihistamine', 'Same-day dermatology clinic review', 'Low temperature, a fast pulse and oedema mean erythrodermic skin failure, which needs admission for fluids, warmth and monitoring, not a clinic visit.')],
           'f': {'Same-day dermatology clinic review': 'widespread psoriasis with normal observations and no systemic upset'}},
}
