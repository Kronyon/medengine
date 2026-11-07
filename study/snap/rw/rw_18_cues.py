"""v3.6.19 (part 3): remove give-away wording from distractors, and add close options in 6 more questions.
Official options are short and neutral. A distractor that carries its own reason to be wrong ("monotherapy", "as the
level is low", "blind", "strict lifelong", "completely", "every time") can be ruled out without knowing the medicine.
These are trimmed so every option reads like the answer; the meaning is unchanged, so the why lines stay. Applied by
site/patches/v364_rw.py as data version 20."""
K = 'keep'
def trim(*pairs): return {'o': [(a, b, K) for a, b in pairs]}
R = {
 # "monotherapy"
 'h0018': trim(('Goserelin implant monotherapy', 'Goserelin implant')),
 'h0129': trim(('Goserelin monotherapy', 'Goserelin injections')),
 'h0273': trim(('Long-term oral antibiotic monotherapy', 'Long-term oral antibiotics')),
 'h0334': trim(('Digoxin monotherapy', 'Digoxin')),
 'h0373': trim(('Oral amoxicillin monotherapy for 5 days', 'Oral amoxicillin for 5 days')),
 'h0414': trim(('Give intravenous vitamin K monotherapy', 'Give intravenous vitamin K')),
 'h0416': trim(('Vancomycin monotherapy', 'Vancomycin')),
 'h0505': trim(('Oral co-amoxiclav monotherapy and discharge', 'Oral co-amoxiclav and discharge')),
 'h0584': trim(('Intravenous co-trimoxazole monotherapy', 'Intravenous co-trimoxazole')),
 'h0648': trim(('Intravenous glyceryl trinitrate monotherapy', 'Intravenous glyceryl trinitrate infusion')),
 'h0661': trim(('As-needed salbutamol reliever monotherapy', 'As-needed salbutamol reliever'),
               ('Regular oral montelukast monotherapy', 'Regular oral montelukast'),
               ('Regular salmeterol inhaler monotherapy', 'Regular salmeterol inhaler')),
 'h0708': trim(('Furosemide monotherapy', 'Furosemide')),
 'h0717': trim(('Switch atorvastatin to ezetimibe monotherapy', 'Switch atorvastatin to ezetimibe')),
 'h1109': trim(('Oral loperamide monotherapy', 'Oral loperamide')),
 'h1111': trim(('Serum IgG endomysial antibody monotherapy', 'Serum IgG endomysial antibody')),
 'h1123': trim(('Full-dose proton pump inhibitor monotherapy for 8 weeks', 'Full-dose proton pump inhibitor for 8 weeks')),
 'h1263': trim(('Fresh frozen plasma monotherapy', 'Fresh frozen plasma'), ('Tranexamic acid monotherapy', 'IV tranexamic acid')),
 'h1264': trim(('IM dexamethasone monotherapy', 'IM dexamethasone')),
 'h1506': trim(('Oral co-amoxiclav monotherapy for 14 days', 'Oral co-amoxiclav for 14 days'),
               ('Single-dose oral azithromycin 1 g monotherapy', 'Single-dose oral azithromycin 1 g')),
 'h1542': trim(('Oral amoxicillin monotherapy', 'Oral amoxicillin')),
 # a reason built into the option
 'h0380': trim(('No antibiotic as it is viral', 'No antibiotic')),
 'h0633': trim(('Reassure as there is no lump', 'Reassure')),
 'h0681': trim(('Reassure and discharge as the chest X-ray is normal', 'Reassure and discharge')),
 'h0849': trim(('No action as she is seizure-free', 'No change to her current treatment')),
 'h1086': trim(('Reassure as it has gone', 'Reassure')),
 'h1129': trim(('Reassure him as the serum PSA is normal', 'Reassure him')),
 'h1133': trim(('Reassure her and discharge without follow-up', 'Reassure and discharge')),
 'h1286': trim(('No referral is required as the level is below the diagnostic threshold', 'No referral needed')),
 'h1395': trim(('No action needed as he feels well', 'No action is needed today')),
 'h1455': trim(('Transfuse as it is life-saving', 'Transfuse')),
 'h1663': trim(('Discharge as the level is low', 'Discharge')),
 # loaded adjectives
 'h0258': trim(('Lifelong strict gluten-free exclusion diet', 'Gluten-free exclusion diet')),
 'h0365': trim(('Switch apixaban to lifelong low-dose aspirin 75 mg daily', 'Switch apixaban to aspirin 75 mg daily'), ('Continue apixaban 2.5 mg twice daily indefinitely', 'Continue apixaban 2.5 mg twice daily long term')),
 'h1182': trim(('Lifelong daily oral furosemide 40 mg', 'Oral furosemide 40 mg daily')),
 'h1656': trim(('Advise strict lifelong avoidance of dietary fat', 'Advise a low-fat diet')),
 'h1437': trim(('Craniotomy every time', 'Craniotomy')),
  'h0628': trim(('Rest the right breast completely for 48 hours', 'Rest the right breast for 48 hours')),
 'h0671': trim(('Withhold antibiotics completely without a back-up script', 'No antibiotic prescription')),
 'h0699': trim(('Stop statin therapy completely', 'Stop the simvastatin')),
 'h1538': trim(('Completely normal CSF profile', 'Normal CSF')),
 'h0920': {'o': [('Lifelong', '9 months', 'Courses beyond 6 months add resistance without extra benefit; review at 3 months and stop by 6.')]},
 # unstable lower GI bleed: CT angiography; upper GI endoscopy if the urea suggests an upper source
 'h0518': {'o': [('Immediate blind exploratory laparotomy', 'Exploratory laparotomy', K),
                 ('Immediate unprepped bedside colonoscopy', 'Urgent colonoscopy', K),
                 ('Erect anteroposterior chest radiograph', 'Urgent upper GI endoscopy', 'An upper source is checked first when the urea is raised or there is melaena; his urea is normal and the blood is maroon, so CT angiography.')],
           'f': {'Urgent upper GI endoscopy': 'melaena with a urea of 18 mmol/L'}},
 # first imaging for a breast lump at 23
 'h0003': {'o': [('Computed tomography of the thorax', 'Ultrasound-guided core biopsy', 'Core biopsy follows the scan and depends on what it shows; the first test is the ultrasound.')],
           'f': {'Ultrasound-guided core biopsy': 'a U3 lesion already seen on ultrasound'}},
 # relapse prevention: acamprosate or naltrexone first; disulfiram second
 'h0468': {'o': [('Methadone', 'Disulfiram', 'Disulfiram is second line, for when acamprosate and naltrexone are unsuitable or the person prefers it, with supervision.')],
           'f': {'Disulfiram': 'acamprosate and naltrexone both unsuitable and he wants an aversive drug'},
           'x': {'Chlordiazepoxide': 'Chlordiazepoxide treats withdrawal, which he has completed; it does not keep him abstinent.'}},
 # disabling post-dural puncture headache despite conservative care
 'h0564': {'o': [('Triptan', 'Wait 7 days for it to settle', 'Most settle within a week, but hers is disabling and conservative care has failed after 3 days, so a blood patch now.')],
           'f': {'Wait 7 days for it to settle': 'a mild headache on day 1 that she is managing at home'}},
 # hospital-acquired pneumonia, non-severe, no allergy
 'h0382': {'o': [('Oral vancomycin', 'Oral doxycycline', 'Doxycycline is an alternative for penicillin allergy; with no allergy, co-amoxiclav is first choice.')],
           'f': {'Oral doxycycline': 'the same pneumonia with a penicillin allergy'}},
 # very high prolactin with headaches: pituitary MRI
 'h0011': {'o': [('Pattern-reversal visual evoked potentials', 'Macroprolactin screen', 'A macroprolactin screen is for a mildly raised prolactin without symptoms; 4,200 with galactorrhoea, amenorrhoea and headaches needs pituitary imaging.')],
           'f': {'Macroprolactin screen': 'prolactin 900 mU/L found on a routine test with no symptoms'}},
}

# the hedged answer: the only option with "or" covers two choices and gives itself away; each now names one
def ans(a, b): return {'o': [(a, b, None)]}
R.update({
 'h0044': ans('Digital tip ulceration or pitting scars', 'Digital pitting scars'),
 'h0072': ans('Crusted, or after 48 hours of antibiotics', '48 hours after starting antibiotics'),
 'h0285': ans('Withhold apixaban and give andexanet alfa or PCC', 'Withhold apixaban and give andexanet alfa'),
 'h0356': {'o': [('Decreased or undetectable serum haptoglobin', 'Low serum haptoglobin', None), ('Markedly Reduced serum ferritin', 'Markedly reduced serum ferritin', K)]},
 'h0363': {'o': [('Step down immediately to a controlled 24% or 28% Venturi mask titrated to target SpO2 88% to 92%', 'Step down to a 28% Venturi mask titrated to a target SpO2 of 88% to 92%', None), ('Remove the oxygen mask completely so he breathes room air and repeat the blood gas in 1 hour', 'Stop the oxygen and repeat the blood gas in 1 hour', K)]},
 'h0366': ans('No further tests unless symptoms or signs develop', 'No further tests unless symptoms develop'),
 'h0368': ans('Attend the Emergency Department or call 999 immediately for urgent hospital assessment', 'Attend the Emergency Department now for urgent assessment'),
 'h0500': ans('Pain or physical illness', 'Physical illness'),
 'h0561': ans('Hearing aid or stapedotomy', 'Hearing aid'),
 'h0776': ans('Stop or review both if possible', 'Stop both if possible'),
 'h0807': ans('Propranolol or carvedilol', 'Propranolol'),
 'h0828': ans('Amiloride or a thiazide', 'Amiloride'),
 'h0928': ans('Once daily or alternate days', 'Once daily'),
 'h1157': ans('Flush or replace it', 'Flush the catheter'),
 'h1300': ans('Perform immediate needle decompression or finger thoracostomy on the right side', 'Perform immediate right-sided needle decompression'),
 'h1311': ans('Intravenous sotrovimab (or remdesivir) avoiding ritonavir', 'Intravenous sotrovimab'),
 'h1312': ans('No further D-dimer or imaging tests', 'No further tests'),
 'h1314': ans('Start LMWH and arrange V/Q or CTPA', 'Start LMWH, then lung imaging'),
 'h1355': ans('CT colonography or contrast CT abdomen', 'Minimal-preparation CT colonography'),
 'h1431': ans('Ureteroscopy or lithotripsy', 'Ureteroscopy'),
 'h1450': ans('CBT or behavioural activation', 'Cognitive behavioural therapy'),
 'h1462': ans('Morphine or midazolam', 'Morphine'),
 'h1500': ans('Intravenous andexanet alfa or 4-factor PCC', 'Intravenous andexanet alfa'),
 'h1515': ans('Watchful waiting or repair', 'Watchful waiting'),
 'h1563': ans('Look for pain or physical illness', 'Look for a physical cause'),
 'h1578': ans('Steroid, topical or oral', 'Oral prednisolone'),
 'h1599': ans('Burns or intensive care unit', 'Transfer to a burns unit'),
 'h1668': ans('Request IgG-based coeliac serology (IgG tTG or IgG DGP)', 'Request IgG-based coeliac serology'),
 'h1669': ans('Add IV infliximab or ciclosporin', 'Add IV infliximab'),
 'h1745': ans('Diffusely decreased (absent) uptake; start propranolol and an NSAID (or prednisolone if severe)', 'Diffusely decreased (absent) uptake; start propranolol and an NSAID'),
 # absolute words left in a distractor
 'h0155': trim(('Remove the catheter permanently', 'Remove the catheter')),
 'h0207': trim(('When the conjunctivae are completely white', 'When the eyes are no longer red and sticky')),
 'h0386': trim(('Stop rifampicin alone and continue the remaining three drugs', 'Stop rifampicin and continue the other three drugs')),
 'h0689': trim(('Lifelong daily therapy', 'Long-term daily therapy')),
 'h0728': trim(('Withhold thrombolysis permanently and give aspirin 300 mg', 'Withhold thrombolysis and give aspirin 300 mg')),
 'h0874': trim(('Every 2 weeks indefinitely', 'Every 2 weeks long term')),
})
