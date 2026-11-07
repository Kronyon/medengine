"""v3.6.19 (part 2): stem-anchored near-misses.
Where the closest real alternative is also a guideline first choice (trimethoprim beside nitrofurantoin, cryotherapy
beside salicylic acid, ciprofloxacin beside cefalexin), official papers add one stem detail that rules it out, then
put it in the options. That is done here: the stem gains the detail, the near-miss joins the options, and its why line
names the detail. Applied by site/patches/v364_rw.py as data version 19."""
R = {
 # high local trimethoprim resistance, so nitrofurantoin (a UTI in the last 6 months would make this recurrent and need a culture)
 'h1141': {'s': [('and she is not pregnant.', 'and she is not pregnant. This is her first urine infection. Local data show high E. coli resistance to trimethoprim.')],
           'o': [('Cefalexin for 7 days', 'Trimethoprim 3 days, no urine culture', 'Trimethoprim is a first choice when resistance is unlikely; local resistance is high, so nitrofurantoin.')],
           'f': {'Trimethoprim 3 days, no urine culture': 'low local resistance and no trimethoprim in the past 3 months'}},
 # pyelonephritis: ciprofloxacin is also first choice, so the stem rules it out
 'h1143': {'s': [('She has no drug allergies.', 'She has no drug allergies, but she ruptured an Achilles tendon while taking ciprofloxacin last year.')],
           'o': [('Pivmecillinam', 'Ciprofloxacin', 'Ciprofloxacin treats pyelonephritis, but a tendon rupture on a fluoroquinolone rules it out for good.')],
           'f': {'Ciprofloxacin': 'the same infection with no previous fluoroquinolone harm'},
           'w': 'For acute pyelonephritis in a non-pregnant adult who can go home, NICE first choices are oral cefalexin, co-amoxiclav or trimethoprim (if the organism is sensitive) or ciprofloxacin. Her tendon rupture on ciprofloxacin removes the fluoroquinolone, and drugs that work only in the bladder (nitrofurantoin, fosfomycin) will fail, so cefalexin.'},
 # warts: cryotherapy is an equal first choice, so the stem asks for a home treatment
 'h0080': {'s': [('and he would like treatment.', 'and he would like a treatment he can use at home.')],
           'o': [('Oral antibiotics', 'Cryotherapy in clinic', 'Cryotherapy works as well, but it needs repeated clinic visits and he wants a treatment he can use at home.')],
           'f': {'Cryotherapy in clinic': 'he would rather have it done in clinic every few weeks'},
           'x': {'Oral prednisolone': 'Systemic steroids suppress immunity and do not clear warts.',
                 'Surgical excision': 'Excision scars, and warts often come back in the scar; it is not used for common warts.'},
           'w': 'Salicylic acid daily for up to 3 months, or cryotherapy. He wants a home treatment, so salicylic acid. Many warts clear by themselves within 2 years.'},
 'h0971': {'s': [('He wants treatment.', 'He wants a treatment he can use at home.')],
           'o': [('Oral terbinafine', 'Cryotherapy in clinic', 'Cryotherapy is the alternative, but it needs repeated clinic visits and he wants a treatment he can use at home.')],
           'f': {'Cryotherapy in clinic': 'salicylic acid used daily for 12 weeks without success'}},
 # GAD: pregabalin follows SSRI and SNRI intolerance; another SSRI follows lack of effect
 'h0450': {'s': [('and then venlafaxine, without improvement.', 'and then venlafaxine, but stopped both because of severe nausea and sexual side effects.')],
           'o': [('Haloperidol', 'Escitalopram', 'Another SSRI is offered when one did not work; she could not tolerate an SSRI or an SNRI, so pregabalin.')],
           'f': {'Escitalopram': 'sertraline tolerated well but no benefit after 12 weeks'}},
 # OA: weight loss is core only if overweight
 'h0398': {'s': [('BMI 31 kg/m².', 'BMI 23 kg/m².')],
           'o': [('Transcutaneous electrical nerve stimulation', 'Weight loss programme', 'Weight loss is core when someone is overweight; with a BMI of 23 the core treatment is strengthening exercise.')],
           'f': {'Weight loss programme': 'the same knees with a BMI of 31'}},
 # heavy periods without pain, no hormones wanted
 'h0935': {'o': [('Danazol', 'Mefenamic acid', 'An NSAID is preferred when heavy bleeding comes with painful periods; she has no pain, so tranexamic acid.'),
                 ('Ulipristal acetate', 'Levonorgestrel IUS', 'The hormonal coil is first line for heavy bleeding, but it is hormonal and she has declined hormones.')],
           'f': {'Mefenamic acid': 'heavy and painful periods',
                 'Levonorgestrel IUS': 'happy to use a hormonal coil and wants contraception'}},
 # actinic keratoses: eight patches across the vertex is field change
 'h0053': {'o': [('Oral aciclovir', 'Cryotherapy to each patch', 'Cryotherapy suits one or a few keratoses; eight patches across the vertex is field change, treated with a field cream.'),
                 ('Oral doxycycline', 'Excision biopsy', 'Biopsy is for a lesion that is raised, indurated, tender or ulcerated, which suggests SCC; none of these is.')],
           'f': {'Cryotherapy to each patch': 'two isolated keratoses on the back of the hand',
                 'Excision biopsy': 'one patch has become a tender, fast-growing nodule'}},
 # fibroadenoma confirmed on core biopsy
 'h0002': {'o': [('Simple mastectomy', 'Vacuum-assisted excision', 'Excision is for a fibroadenoma over 3 cm, one that is growing, or at the woman\'s request; hers is 1.5 cm and stable.')],
           'f': {'Vacuum-assisted excision': 'a 4 cm fibroadenoma that is still growing'}},
 # Malassezia folliculitis: topical first
 'h1584': {'o': [('Oral flucloxacillin', 'Oral itraconazole', 'An oral antifungal is for widespread or resistant folliculitis after topical treatment has failed; start with the wash.')],
           'f': {'Oral itraconazole': 'still widespread after 4 weeks of ketoconazole wash'}},
 # NICE NG120: doxycycline is first choice; amoxicillin and clarithromycin are alternatives
 'h0672': {'o': [('Oral nitrofurantoin', 'Oral amoxicillin', 'Amoxicillin is an alternative; NICE names doxycycline as the first choice for adults with acute cough.'),
                 ('Oral flucloxacillin', 'Oral clarithromycin', 'Clarithromycin is an alternative when doxycycline is unsuitable; he has no allergy or contraindication.')],
           'f': {'Oral amoxicillin': 'pregnant, so doxycycline is unsuitable',
                 'Oral clarithromycin': 'doxycycline unsuitable and a penicillin allergy'}},
 # first mania: antipsychotic first; lithium if that fails
 'h1196': {'o': [('Lamotrigine', 'Lithium', 'Lithium is added if an antipsychotic does not work and is the long-term mainstay; acute mania starts with an antipsychotic.')],
           'f': {'Lithium': 'no response to haloperidol and then olanzapine'}},
 # influenza in pregnancy: oseltamivir first
 'h0779': {'o': [('Prednisolone', 'Inhaled zanamivir', 'Zanamivir is used when the circulating strain is resistant to oseltamivir; otherwise oseltamivir is first line in pregnancy.')],
           'f': {'Inhaled zanamivir': 'an outbreak strain known to be resistant to oseltamivir'}},
 # lymphoedema cellulitis after urticaria to amoxicillin: clarithromycin
 'h1524': {'o': [('Oral furosemide', 'Cefalexin', 'Cephalosporins are avoided after an urticarial reaction to amoxicillin; clarithromycin is used.')],
           'f': {'Cefalexin': 'a mild delayed rash to amoxicillin, with no urticaria or swelling'}},
 'h0455': {'x': {'Clomipramine': 'Clomipramine is used after an SSRI has failed or is not tolerated; start with an SSRI.'}},
}
