"""v3.6.9: precision give-aways and the last weak distractors.
A precision give-away is an answer that alone carries a dose, a strength or an "urgent" while the four wrong options
are bare (Gemini's point: equal length is not equal specificity). Fixed by trimming the answer or giving a lookalike
the same precision. Applied by site/patches/v364_rw.py."""
R = {
 # ---------------------------------------------------------------- the answer alone carried a dose or strength
 'h0110': {'o': [('IM glucagon 1 mg', 'IM glucagon', None)]},
 'h0307': {'o': [('IV fluid bolus of 500 ml', 'IV fluid bolus', None)]},
 'h0512': {'o': [('Topical glyceryl trinitrate 0.4%', 'Topical glyceryl trinitrate', None)]},
 'h0513': {'o': [('Topical diltiazem 2%', 'Topical diltiazem', None)]},
 'h0551': {'o': [('12-lead ECG', 'ECG', None)]},
 'h0751': {'o': [('Ceftriaxone 1 g IM', 'IM ceftriaxone', None)]},
 'h0912': {'o': [('IV lipid emulsion 20%', 'IV lipid emulsion', None)]},
 'h1275': {'o': [('IV lorazepam 4 mg', 'IV lorazepam', None)]},
 'h1475': {'o': [('Dexamethasone 6 mg daily', 'Oral dexamethasone', None)]},
 'h1495': {'o': [('GTN 0.4% ointment', 'GTN ointment', None)]},
 'h1533': {'o': [('Dexamethasone 16 mg', 'Dexamethasone', None)]},
 'h1637': {'o': [('Generous IV 0.9% saline', 'IV 0.9% saline', None)]},
 'h0198': {'o': [('5 back blows', 'Back blows', None)]},
 'h1747': {'o': [('Urgent plasma exchange', 'Plasma exchange', None)]},
 # ---------------------------------------------------------------- the answer alone carried a time frame or "urgent": give a lookalike the same
 'h0184': {'o': [('Ciprofloxacin ear drops', 'Ciprofloxacin ear drops for 7 days', 'keep')]},
 'h1149': {'o': [('Scrotal ultrasound first', 'Urgent scrotal ultrasound first', 'keep')]},
 'h1150': {'o': [('Doppler ultrasound first', 'Urgent Doppler ultrasound first', 'keep')]},
 'h1210': {'o': [('Refer to a dietitian', 'Urgent dietitian referral', 'keep')]},
 'h1863': {'o': [('CT chest and abdomen', 'Urgent CT chest and abdomen', 'keep')]},
 'h1368': {'o': [('Ambulatory BP', 'Routine cardiology clinic',
                  'A routine wait is unsafe: exertional syncope with a murmur and a family history of sudden death suggests HCM, which needs urgent assessment.')]},

 # ---------------------------------------------------------------- the last throwaway distractors found by hand in the untouched weeks
 'h0049': {'o': [('Chemotherapy', 'Mohs micrographic surgery',
                  'Mohs surgery is kept for high-risk BCCs on the central face or recurrent tumours; a nodular BCC on the back is excised with a standard margin.')]},
 'h0152': {'o': [('Vasectomy', 'GnRH analogue to protect the testis',
                  'GnRH analogues are tried to protect the ovaries during chemotherapy; there is no evidence they protect sperm production.'),
                 ('Testosterone injections', 'Biopsy of the other testis',
                  'A biopsy of the other testis looks for germ cell neoplasia in situ in high-risk men; it does not preserve fertility.')]},
 'h0960': {'o': [('Isotretinoin', 'Decolonisation before swabbing',
                  'Decolonisation (chlorhexidine wash and nasal mupirocin) is offered once PVL-positive Staphylococcus aureus is confirmed, not before.'),
                 ('Topical steroid', 'Seven days of flucloxacillin for her',
                  'A short course may treat this boil, but recurrent boils across the family suggest PVL carriage, which needs a swab first.')]},
}
