from snapdsl import N

N(86, 'Osteoarthritis', 'joint', 'cart',
  'Wear and failed repair thin the cartilage → bone rubs on bone → spurs grow and the joint stiffens',
  '45+ · obesity · old injury · women: hands and knees',
  'Pain on use, eases with rest>joints; Stiffness under 30 min in the morning>joints; Bony swelling: Heberden\'s and Bouchard\'s nodes>hands; Crepitus, reduced movement>joints',
  'Clinical diagnosis if 45+ with typical pain*; X-ray if unsure>LOSS: Loss of space, Osteophytes, Subchondral sclerosis, Subchondral cysts; Bloods>only to exclude other arthritis',
  'Exercise, weight loss: core treatment | Topical NSAID for knee or hand; paracetamol not routinely | Oral NSAID with PPI, short courses; steroid injection | Joint replacement if pain and function poor',
  'Hot, swollen single joint: septic arthritis>e; Morning stiffness over 1 hour: inflammatory>u; Night pain or weight loss: tumour>u',
  'OA is better in the morning, worse by evening. Inflammatory is worse in the morning, better with use.')

N(87, 'Joint replacements', 'joint', 'implant',
  'Worn joint surfaces are replaced with metal and plastic → pain goes and function returns → lasts 15 to 20 years',
  'End-stage OA · fractured neck of femur · RA',
  'Wound and swelling after surgery>joints; Hip: avoid deep bending early>groin; Calf swelling: DVT>legs; Pain years later: loosening>joints',
  'X-ray>position, loosening*; Bloods, CRP, aspirate>if infection is suspected',
  'Pre-op: optimise health, MRSA screen | VTE prophylaxis after surgery | Physiotherapy from day 1 | Follow up for loosening or infection',
  'Prosthetic joint infection: hot, painful, wound leaking>e; Dislocation>e; DVT or PE>e',
  'A painful replaced joint is infected until proved otherwise.')

N(122, 'Malignant melanoma', 'skin', 'mole',
  'UV damages pigment cells → they grow uncontrolled → they invade down and spread early',
  'Fair skin, sunburn · many moles · family history',
  'Asymmetric mole>skin; Irregular border>skin; Several colours>skin; Diameter over 6 mm>skin; Evolving: changing size, shape, colour>skin',
  'Weighted 7-point checklist>3 or more = suspected cancer pathway*; Dermoscopy>pattern; Excision biopsy>Breslow thickness*',
  'Suspected cancer pathway | Excision with a margin | Sentinel node biopsy by thickness | Immunotherapy or targeted drugs for spread',
  'Any suspicious pigmented lesion: suspected cancer pathway>c; Bleeding, itching mole>c',
  'ABCDE plus the ugly duckling: the mole that looks unlike the rest.')

N(123, 'Basal cell carcinoma', 'skin', 'epi',
  'UV damages basal cells → a slow tumour grows locally → it almost never spreads',
  'Older, fair skin · sun-exposed head and neck · immunosuppressed',
  'Pearly nodule with rolled edges>face; Tiny surface vessels>face; Central ulcer: rodent ulcer>nose; Slow growth over months>face',
  'Clinical and dermoscopy*; Biopsy if unsure',
  'Routine referral | Surgical excision; Mohs on the face | Cream or cryotherapy for superficial ones',
  'Near the eye or nose, or large: urgent>u; Neglected tumours destroy tissue>u',
  'Pearly, rolled, slow, rarely spreads: the cancer that destroys locally.')

N(124, 'Squamous cell carcinoma and pre-malignancy', 'skin', 'epi',
  'UV damages keratinocytes → actinic keratosis → it can become SCC, which spreads',
  'Older, outdoor workers · immunosuppressed, transplant · chronic ulcers',
  'Rough scaly patches: actinic keratosis>face; Growing crusted, tender nodule: SCC>hands; Ulcer that won\'t heal>skin; On lip or ear: higher risk>ear',
  'Clinical; biopsy>confirms SCC*; Examine nodes>spread',
  'Actinic keratosis: sun protection, 5-FU cream, cryotherapy | SCC: suspected cancer pathway | Surgical excision | Radiotherapy if not operable',
  'Suspected SCC: suspected cancer pathway>c; Transplant patient: aggressive SCC>c',
  'BCC is slow and local; SCC is faster, tender and can spread.')

N(125, 'Skin signs of systemic disease', 'skin', 'derm',
  'Internal disease leaves marks on the skin → read the skin to find the organ',
  'Diabetes, liver, IBD, thyroid, cancer, sarcoid, lupus',
  'Necrobiosis lipoidica on shins: diabetes>legs; Erythema nodosum: IBD, sarcoid, strep, TB>legs; Pyoderma gangrenosum: IBD>legs; Acanthosis nigricans: insulin resistance, cancer>neck; Butterfly rash: lupus>face',
  'Treat the skin as a clue: find the disease*; Bloods by suspicion>glucose, LFT, ANA; Biopsy if unsure',
  'Treat the underlying disease | Skin-specific care | Refer dermatology if severe',
  'Sudden acanthosis nigricans in an adult: cancer>c; Spreading pyoderma>s',
  'The skin is a window: name the rash, then hunt the organ.', k='t')

N(126, 'Urticaria', 'skin', 'derm',
  'Mast cells release histamine → fluid leaks in the dermis → itchy wheals that come and go within 24 h',
  'Any age · triggers: infection, food, drugs, NSAIDs · chronic: often no trigger',
  'Itchy raised wheals>skin; Each wheal fades within 24 h>skin; Swelling of lips or eyes: angioedema>face',
  'Clinical diagnosis*; Look for a trigger>history; Chronic over 6 weeks>FBC, CRP, TFT',
  'Avoid triggers | Non-sedating antihistamine daily | Up to 4 times the dose; short steroid course for severe | Chronic: specialist, omalizumab',
  'Tongue or throat swelling, wheeze, low BP: anaphylaxis, IM adrenaline 0.5 mg>e; ACE inhibitor angioedema>s',
  'Wheals that move and fade in hours = urticaria. One spot lasting days = something else.')

N(127, 'Leg ulcers', 'limb', 'skin',
  'Venous pressure or poor arterial flow → skin can\'t heal → an ulcer lasting over 2 weeks',
  'Venous: older, varicose veins, DVT · arterial: smokers, diabetes',
  'Venous: shallow, inner ankle, eczema, brown skin>legs; Arterial: punched out, on the foot, painful>feet; Leg pain worse raised: arterial>legs',
  'ABPI>before compression*; Duplex>veins or arteries; Biopsy if not healing>exclude SCC',
  'Venous: compression if ABPI 0.8 to 1.3 | Leg raising, walking, dressings | Arterial: vascular referral, revascularise | Treat infection only if clinically infected',
  'Spreading cellulitis>s; Critical ischaemia: rest pain, gangrene>s; Non-healing ulcer with rolled edge: SCC>c',
  'Venous weeps at the ankle; arterial hurts at the toes. ABPI before any compression.')

N(128, 'Eczema', 'skin', 'epi',
  'A leaky skin barrier plus allergic inflammation → dry, itchy, inflamed skin → scratching makes it worse',
  'Atopic: children, asthma, hay fever · contact: irritants, nickel, hairdressers',
  'Dry itchy skin>skin; Flexures: elbows, knees in older children>joints; Face and cheeks in babies>face; Contact: shaped like the culprit>hands',
  'Clinical diagnosis*; Patch testing>contact allergy; Swab if infected>Staph or herpes',
  'Emollients lots and often, soap substitute | Topical steroid for flares by severity | Tacrolimus for face or steroid-sparing | Phototherapy, systemic treatment for severe',
  'Painful punched-out blisters: eczema herpeticum, aciclovir>e; Weeping crusted: Staph infection>s',
  'Emollients are the foundation; steroids put out the flares.')

N(129, 'Folliculitis', 'skin', 'foll',
  'Hair follicles get infected or irritated → small pus spots around hairs',
  'Shaving · hot tubs: Pseudomonas · diabetes',
  'Small itchy pustules around hairs>skin; Beard, legs, buttocks>face; Boils if deeper>skin',
  'Clinical*; Swab if not settling>culture',
  'Stop shaving the area, antiseptic washes | Topical antibiotic | Oral flucloxacillin if widespread or boils',
  'Recurrent boils: check glucose, PVL Staph>u; Spreading cellulitis>s',
  'A spot centred on a hair is folliculitis.')

N(130, 'Impetigo', 'skin', 'epi',
  'Staph or strep infect the top layer → honey-coloured crusts → very contagious',
  'Children · eczema · close contact',
  'Golden honey crusts>face; Around mouth and nose>mouth; Blistering type: bullous>skin',
  'Clinical diagnosis*; Swab if recurrent or not responding',
  'Hydrogen peroxide cream if localised | Topical fusidic acid if that is unsuitable | Oral flucloxacillin if widespread | Off school until crusted or 48 h after antibiotics',
  'Widespread or unwell>s; Post-strep kidney disease: dark urine later>u',
  'Golden crust on a child\'s face = impetigo.')

N(131, 'Cellulitis', 'skin', 'derm',
  'Bacteria enter through broken skin → infection spreads in the dermis and fat → red, hot, swollen',
  'Older adults · leg swelling, eczema, athlete\'s foot · diabetes',
  'Red, hot, swollen, tender area>legs; Usually one leg>legs; Fever>head; Spreading edge>legs',
  'Clinical diagnosis*; Mark the edge>track spread; Bloods if unwell>FBC, CRP, cultures',
  'Oral flucloxacillin; clarithromycin if allergic | Raise the leg, analgesia | IV antibiotics if severe or not improving | Treat the entry point: athlete\'s foot',
  'Pain out of proportion: necrotising fasciitis>e; Around the eye: orbital cellulitis>e; Sepsis>e',
  'Both legs red and warm is rarely cellulitis: think venous eczema.')

N(132, 'Necrotising fasciitis', 'skin', 'fascia',
  'Toxin-producing bacteria spread along the fascia → tissue dies fast → sepsis within hours',
  'Diabetes, IV drug use · after surgery or minor wounds · immunosuppressed',
  'Severe pain out of proportion>legs; Rapidly spreading redness>legs; Skin purple, blistering, crackles under the skin>skin; Very unwell, septic>heart',
  'Clinical suspicion: don\'t wait*; Bloods>very high CRP, CK, lactate; Imaging must not delay theatre',
  'Sepsis six | IV broad-spectrum antibiotics | Emergency surgical debridement',
  'Septic shock>e; Fournier\'s gangrene in the perineum>e',
  'Pain beyond the redness = theatre, not the ward.')

N(133, 'Cutaneous warts', 'skin', 'epi',
  'Human papilloma virus infects the skin → keratinocytes overgrow → rough lumps',
  'Children and teens · swimmers: verrucas · immunosuppressed',
  'Rough raised lumps on hands>hands; Verrucas on soles with black dots>feet; Flat warts on face>face',
  'Clinical diagnosis*; Biopsy if atypical or in immunosuppressed',
  'Leave: most go within 2 years | Salicylic acid daily | Cryotherapy',
  'Atypical, bleeding or changing: refer>u; Immunosuppressed with many warts>u',
  'Black dots in a verruca are clotted capillaries.')

N(134, 'Cutaneous fungal infections', 'skin', 'epi',
  'Dermatophytes or yeasts live on keratin → spread in warm, moist skin → itchy scaly rashes',
  'Athletes, damp feet · diabetes · steroids, antibiotics: candida',
  'Ring with scaly edge, clearing centre: tinea corporis>skin; Itchy cracked toe webs: athlete\'s foot>feet; Thick yellow nails>feet; Red, moist folds with satellite spots: candida>groin',
  'Clinical*; Skin scrapings or nail clippings>microscopy and culture, before oral treatment',
  'Keep dry | Topical terbinafine or imidazole | Oral terbinafine for nails or scalp | Avoid steroid creams on fungal rashes',
  'Tinea incognito from steroid cream>r; Scalp ringworm in children with kerion>u',
  'A ring with a scaly edge and a clear centre: think fungus before eczema.')

N(135, 'Scabies', 'skin', 'epi',
  'Mites burrow into the skin → the immune system reacts weeks later → intense itch, worse at night',
  'Close contact · care homes · households, schools',
  'Intense itch, worse at night>skin; Burrows in finger webs and wrists>hands; Rash on waist, genitals>genit; Others at home itching too>all',
  'Clinical; dermoscopy>burrows with the mite*',
  'Permethrin cream to the whole body, repeat in 7 days | Treat everyone in the house at the same time | Wash bedding and clothes hot | Itch can last weeks after cure',
  'Crusted scabies in immunosuppressed: very contagious>u; Secondary infection>s',
  'Treat the whole household on the same day, or it comes back.')

N(136, 'Head lice', 'skin', 'foll',
  'Lice live on the scalp and lay eggs on hairs → bites itch → spread by head-to-head contact',
  'School-age children · close contact',
  'Itchy scalp>head; Live lice or eggs near the scalp>head; Behind ears, nape of neck>neck',
  'Detection combing>live lice confirm it*',
  'Wet combing every 4 days for 2 weeks | Dimeticone lotion, repeat in 7 days | Treat only those with live lice | No need to exclude from school',
  'Secondary infection>r; Treatment failure: recheck technique>r',
  'Only treat live lice, not nits.')

N(137, 'Psoriasis', 'skin', 'epi',
  'The immune system speeds up skin turnover → cells pile up in thick plaques',
  'Any age · family history · triggers: stress, strep throat, beta-blockers, lithium',
  'Red plaques with silvery scale>skin; Elbows, knees, scalp>joints; Nail pitting, lifting>hands; Joint pain: psoriatic arthritis>joints',
  'Clinical diagnosis*; Screen for psoriatic arthritis, CV risk, depression',
  'Emollients | Potent steroid plus vitamin D ointment | Phototherapy | Methotrexate, ciclosporin, then biologics',
  'Erythrodermic or pustular psoriasis: skin failure>e; Joint pain: rheumatology>u',
  'Silvery scale on extensors = psoriasis; ill-defined itchy flexures = eczema.')

N(138, 'Acne vulgaris', 'skin', 'foll',
  'Hormones increase oil, follicles block, bacteria grow → comedones, then inflamed spots',
  'Teenagers · PCOS · steroids',
  'Blackheads and whiteheads>face; Red papules and pustules>face; Nodules and cysts: severe>face; Back and chest>back',
  'Clinical diagnosis*; PCOS screen>irregular periods, hair growth',
  'Mild: topical benzoyl peroxide plus adapalene | Moderate: add topical antibiotic, or oral doxycycline | Combined pill for women | Severe or scarring: isotretinoin via dermatology',
  'Scarring or severe distress: refer>u; Isotretinoin: pregnancy prevention, mood>s',
  'Never use an antibiotic alone in acne: always pair it with benzoyl peroxide.')

N(139, 'Describing skin lesions and skin failure', 'skin', 'epi',
  'Describe like a phone call to a dermatologist → where, what, colour, edge, surface → widespread skin loss is an emergency',
  'Anyone with a rash · skin failure: drugs, erythroderma, TEN',
  'Macule: flat under 1 cm; patch over>skin; Papule: raised under 1 cm; plaque over>skin; Vesicle under 0.5 cm; bulla over>skin; Non-blanching: purpura>legs',
  'Glass test>purpura doesn\'t blanch*; Skin failure: U&E, albumin, temperature>fluid and heat loss',
  'Describe: site, distribution, morphology, colour, edge, surface | Skin failure: warm, fluids, emollients | Stop the culprit drug | Dermatology or burns unit',
  'Non-blanching rash with fever: meningococcal>e; Skin peeling with mucosa: SJS or TEN>e; Erythroderma over 90%>e',
  'Flat, raised, deep, fluid: sort every lesion into one of four.', k='t')
