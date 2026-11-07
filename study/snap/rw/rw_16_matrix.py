"""v3.6.19: the "same drug, one variable changed" pass.
Official papers often keep the right drug in most options and change one thing: duration, dose, route, timing, or
whether a test is sent (nitrofurantoin 3 or 7 days, with or without an MSU). Knowing the drug then earns nothing; the
stem detail decides. Each new option is a real, guideline-based choice for a slightly different patient, written with
the flip that would make it right. Applied by site/patches/v364_rw.py as data version 18."""
R = {
 # NICE NG109: non-pregnant woman under 65, typical symptoms: nitrofurantoin 3 days, no culture needed
 'h1141': {'o': [('Nitrofurantoin for 3 days', 'Nitrofurantoin 3 days, no urine culture', None),
                 ('Amoxicillin for 3 days', 'Nitrofurantoin 3 days with urine culture', 'She is under 65, not pregnant, with typical symptoms and a positive dipstick, so a culture adds nothing before treating.'),
                 ('Ciprofloxacin course for 3 days', 'Nitrofurantoin 7 days, no urine culture', 'Seven days is the course for men and pregnant women; a non-pregnant woman needs 3 days.'),
                 ('Co-amoxiclav for 5 days', 'Nitrofurantoin 7 days with urine culture', 'Seven days with a culture is the plan in pregnancy; she is not pregnant, so 3 days without a culture.')],
           'f': {'Nitrofurantoin 3 days with urine culture': 'aged 70, or symptoms still present after a first course',
                 'Nitrofurantoin 7 days, no urine culture': 'a 40 year old man with the same symptoms',
                 'Nitrofurantoin 7 days with urine culture': 'pregnant at 20 weeks with the same symptoms'}},
 # pregnancy: nitrofurantoin 7 days; trimethoprim avoided in the first trimester
 'h1142': {'o': [('Doxycycline for 7 days', 'Nitrofurantoin for 3 days', 'Three days is for non-pregnant women; pregnancy needs a 7-day course because untreated bacteriuria leads to pyelonephritis.'),
                 ('Ciprofloxacin for 7 days', 'Trimethoprim for 7 days', 'Seven days is right for pregnancy, but trimethoprim is a folate antagonist avoided in the first trimester; at 12 weeks use nitrofurantoin.')],
           'f': {'Nitrofurantoin for 3 days': 'a non-pregnant 30 year old woman',
                 'Trimethoprim for 7 days': 'a man with lower UTI and a low risk of resistance'}},
 # NICE NG110: acute prostatitis: ciprofloxacin 14 days; trimethoprim 14 days if a fluoroquinolone is unsuitable
 'h0765': {'o': [('Amoxicillin for 5 days', 'Ciprofloxacin for 7 days', 'Seven days treats pyelonephritis; prostatitis needs 14 days so it does not become chronic.'),
                 ('Doxycycline for 3 days', 'Trimethoprim for 14 days', 'Fourteen days is right, but trimethoprim is the second choice when a fluoroquinolone is unsuitable; he has no reason to avoid ciprofloxacin.')],
           'f': {'Ciprofloxacin for 7 days': 'fever and loin pain with a non-tender prostate (pyelonephritis)',
                 'Trimethoprim for 14 days': 'tendon rupture on a previous fluoroquinolone'},
           'x': {'Nitrofurantoin for 7 days': 'Nitrofurantoin reaches the bladder, not prostate tissue; 7 days treats lower UTI in men.'}},
 # NICE NG95: erythema migrans is diagnosed clinically: doxycycline 21 days
 'h0759': {'o': [('No treatment', 'Doxycycline for 28 days', 'Twenty-eight days is for Lyme arthritis or acrodermatitis; isolated erythema migrans needs 21 days.'),
                 ('Amoxicillin for 5 days', 'Amoxicillin for 21 days', 'Amoxicillin for 21 days is the alternative when doxycycline is unsuitable; he can take doxycycline.'),
                 ('Clarithromycin for 3 days', 'Lyme serology before treating', 'Erythema migrans is diagnosed on sight; early serology is often negative, so treat now without testing.')],
           'f': {'Doxycycline for 28 days': 'a swollen knee months after a tick bite',
                 'Amoxicillin for 21 days': 'pregnant with the same expanding ring',
                 'Lyme serology before treating': 'no rash, but fatigue and joint pain after a tick bite'}},
 # CKS: dermatophyte toenails: terbinafine 3 to 6 months; 6 weeks is the fingernail course
 'h0083': {'o': [('Oral terbinafine', 'Oral terbinafine for 3 months', None),
                 ('Clotrimazole cream', 'Oral terbinafine for 6 weeks', 'Six weeks is the fingernail course; toenails grow slowly and need 3 to 6 months.'),
                 ('Topical steroid', 'Oral itraconazole pulses', 'Itraconazole is used for Candida or when terbinafine is unsuitable; a dermatophyte with normal liver tests needs terbinafine.')],
           'f': {'Oral terbinafine for 6 weeks': 'the same dermatophyte in two fingernails',
                 'Oral itraconazole pulses': 'Candida grown from the nail clippings'},
           'x': {'Oral griseofulvin': 'Griseofulvin is less effective than terbinafine for nails and is no longer used first line.'}},
 # thyroid nodule, euthyroid: ultrasound grades the nodule; FNA follows the U grade
 'h0123': {'o': [('Calcitonin', 'Fine needle aspiration', 'FNA is decided by the ultrasound U grade, so the ultrasound comes first.')],
           'f': {'Fine needle aspiration': 'a U4 nodule on ultrasound'},
           'x': {'CT neck': 'CT is for retrosternal extension or airway compression; a euthyroid nodule is graded on ultrasound first.',
                 'Radioisotope uptake scan': 'An uptake scan looks for a hot nodule when the TSH is low; her TSH is normal.'}},
 # hydrocele hiding the testis: ultrasound first; markers follow a solid mass
 'h0144': {'o': [('Blood cultures', 'Serum AFP and beta-hCG', 'Tumour markers follow an ultrasound that shows a solid mass; image the testis first.')],
           'f': {'Serum AFP and beta-hCG': 'a solid mass in the testis on ultrasound'},
           'x': {'Urine culture and sensitivity': 'Urine culture is for epididymo-orchitis with dysuria and a tender epididymis; this swelling is painless.',
                 'Watch and wait': 'The testis cannot be felt, so a tumour behind the hydrocele must be excluded with ultrasound.'}},
 # NICE NG202: moderate OSA with sleepiness: CPAP; mandibular device for mild OSA or CPAP intolerance
 'h0180': {'o': [('Tonsillectomy', 'Mandibular advancement device', 'A mandibular device is for mild OSA or when CPAP is not tolerated; moderate OSA with an Epworth of 15 needs CPAP.')],
           'f': {'Mandibular advancement device': 'mild OSA (AHI 9) with snoring, or CPAP tried and not tolerated'}},
 # mastitis with urticaria and angioedema to amoxicillin: erythromycin
 'h0009': {'o': [('Trimethoprim', 'Cefalexin', 'Cephalosporins are avoided after urticaria and angioedema to a penicillin; erythromycin is used.')],
           'f': {'Cefalexin': 'a mild delayed rash to amoxicillin years ago, with no swelling'}},
 # pertussis: macrolide within 21 days; notify on clinical suspicion
 'h0380': {'o': [('Oral prednisolone for 5 days', 'Clarithromycin; notify if PCR confirms', 'Pertussis is notified on clinical suspicion; waiting for PCR delays protecting her nursery contacts.')]},
 # GCA without visual symptoms: oral prednisolone 40 to 60 mg today
 'h0405': {'o': [('Perform a diagnostic lumbar puncture', 'Start IV methylprednisolone today', 'IV methylprednisolone is for visual loss or amaurosis; her vision is normal, so oral prednisolone 40 to 60 mg.'),
                 ('Trial of oral sumatriptan 50 mg stat', 'Start oral prednisolone 15 mg today', 'Fifteen milligrams is the polymyalgia dose; giant cell arteritis needs 40 to 60 mg to protect the eyes.')],
           'f': {'Start IV methylprednisolone today': 'transient loss of vision in one eye this morning',
                 'Start oral prednisolone 15 mg today': 'shoulder and hip girdle stiffness with no headache or jaw pain'}},
 # subdural with midline shift on apixaban: stop and reverse (andexanet alfa or PCC)
 'h0414': {'o': [('Transfuse two pools of platelets', 'Stop apixaban and observe', 'An expanding subdural with midline shift needs active reversal with andexanet alfa or PCC; waiting for apixaban to clear is too slow.')],
           'f': {'Stop apixaban and observe': 'a minor nosebleed that has already stopped'}},
 # alcohol withdrawal, no liver disease: chlordiazepoxide; lorazepam if decompensated liver disease
 'h0467': {'o': [('Disulfiram', 'Lorazepam', 'Lorazepam is chosen in decompensated liver disease; with a normal liver, long-acting chlordiazepoxide gives a smoother withdrawal.')],
           'f': {'Lorazepam': 'jaundice, ascites and an INR of 2.1'},
           'x': {'Acamprosate': 'Acamprosate prevents relapse after withdrawal; it does not treat withdrawal itself.'}},
 # dental-source cerebral abscess: ceftriaxone plus metronidazole for anaerobes
 'h1541': {'o': [('IV aciclovir', 'Ceftriaxone and aciclovir', 'Aciclovir covers herpes encephalitis; a dental-source abscess needs metronidazole for the anaerobes.'),
                 ('Oral amoxicillin', 'Ceftriaxone and vancomycin', 'Vancomycin is added for resistant pneumococcal meningitis; a dental-source abscess needs anaerobic cover with metronidazole.')],
           'f': {'Ceftriaxone and aciclovir': 'fever, confusion and temporal lobe seizures with a normal CT',
                 'Ceftriaxone and vancomycin': 'meningitis after travel to an area with penicillin-resistant pneumococcus'}},
 # NICE NG153: widespread impetigo in an unwell child: oral flucloxacillin
 'h0071': {'o': [('Trimethoprim', 'Hydrogen peroxide 1% cream', 'Hydrogen peroxide is for localised impetigo in a well child; widespread lesions with fever need oral flucloxacillin.'),
                 ('Metronidazole', 'Clarithromycin', 'Clarithromycin is the choice in penicillin allergy; he has none, so flucloxacillin.')],
           'f': {'Hydrogen peroxide 1% cream': 'two small crusted patches near the mouth in a well child',
                 'Clarithromycin': 'the same child with penicillin anaphylaxis'},
           'x': {'Fusidic acid cream': 'Topical fusidic acid is for localised impetigo; widespread lesions with fever need oral treatment.'}},
 # cellulitis with penicillin anaphylaxis: clarithromycin
 'h0074': {'o': [('Nitrofurantoin', 'Co-amoxiclav', 'Co-amoxiclav contains a penicillin; it is for cellulitis near the eyes or nose in someone without allergy.')],
           'f': {'Co-amoxiclav': 'cellulitis beside the nose with no penicillin allergy'},
           'x': {'Flucloxacillin': 'Flucloxacillin is first line for cellulitis, but it is a penicillin and he had anaphylaxis.'}},
 # epididymo-orchitis from a urinary source in an older man: ofloxacin
 'h0146': {'o': [('Azithromycin', 'IM ceftriaxone and oral doxycycline', 'This covers gonorrhoea and chlamydia in sexually acquired cases; a 70 year old with BPH and a positive dipstick has an enteric organism.')],
           'f': {'IM ceftriaxone and oral doxycycline': 'a 24 year old with a new partner and urethral discharge'}},
 # Budd-Chiari: anticoagulate first; TIPSS if that fails
 'h0567': {'o': [('Steroids', 'TIPSS', 'TIPSS is for ascites or worsening liver function despite anticoagulation; the first treatment is anticoagulation.')],
           'f': {'TIPSS': 'refractory ascites despite 3 months of anticoagulation'},
           'x': {'Liver transplant': 'Transplant is for fulminant liver failure or failure of TIPSS; her liver function is only mildly impaired.'}},
 # venous ulcer, ABPI 0.9: full compression is safe
 'h1175': {'o': [('Multilayer compression', 'Full multilayer compression', None),
                 ('Topical steroid', 'Reduced compression bandaging', 'Reduced compression is for an ABPI of 0.5 to 0.8; at 0.9 full compression is safe and heals faster.'),
                 ('Oral antibiotics', 'Vascular referral before compression', 'Referral before compression is for an ABPI under 0.5 or over 1.3; hers is 0.9.')],
           'f': {'Reduced compression bandaging': 'the same ulcer with an ABPI of 0.7',
                 'Vascular referral before compression': 'an ABPI of 1.4 in a man with diabetes'}},
 # second pneumothorax in a fit young man: surgery
 'h1413': {'o': [('Antibiotics', 'Talc pleurodesis via the drain', 'Medical pleurodesis is for patients unfit for surgery; a fit 24 year old has VATS, which has a lower recurrence rate.')],
           'f': {'Talc pleurodesis via the drain': 'frail with severe COPD and unfit for surgery'}},
}
