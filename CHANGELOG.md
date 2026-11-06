# Changelog

## 3.6.13 (2026-11-06)

🔍 **Audit of the v3.6.12 Hammer rewrite (Antigravity), saves repaired, style fixes on top.**
- **Imported:** the v3.6.12 bank (all 1,811 questions rewritten in a blend of MSCAA and Nottingham style: stems with observations and labelled results, "x-week history of" in 22% of stems like the mock's 21%, a why-not line for every wrong option). It is kept as `study/snap/rw/import_v3612.json` and applied by `site/patches/v3613_import.py`, so the build stays reproducible.
- **Saves repaired (the important one).** v3.6.12 changed the options of 754 questions but wrote run-migration entries for only 105, and 56 of those pointed picks at the wrong option. A run saved on v3.6.10 would have shown your old picks against different answers in about 650 questions. Every changed question now has one correct entry: picks follow their option text (629 questions, including light rewording such as "Lipoma" to "Breast lipoma"), and picks on the 125 questions whose answer changed are cleared rather than misread. Runs saved on v3.6.12 itself are left alone. Tested on real v3.6.10 and v3.6.12 option lists, and the runs survive a reload.
- **Mock-like chip fixed.** v3.6.12 had put 1,796 of 1,811 questions in it, which made the filter do nothing. It is back to **809**, with the mock's mix (54% diagnosis, 25% management, 6% investigation, 13% other) and the mock week weighting.
- **24 answers that gave themselves away by length** trimmed (for example "Obtain three sets of peripheral blood cultures from separate venepuncture sites spaced over 6 to 24 hours" against short distractors).
- **71 test-wise cues removed:** "alone", "only" and "all" appeared only in wrong options ("Aspirin 300 mg immediately alone").
- **Lead-ins in MSCAA form:** guideline names taken out of 28 lead-ins ("Under British Thoracic Society guidelines, which..."), 44 "What is..." lead-ins rewritten as "Which...", 2 negative lead-ins made positive, the longest lead-ins shortened.
- **Six new clones** the rewrite had created (BCG, testicular lymphoma, perforated ulcer, Crohn's, fat necrosis, prostate MRI) rebuilt as new angles: systemic BCG infection, Leydig cell tumour, colonic interposition (Chilaiditi), faecal calprotectin, Mondor's disease, transperineal biopsy.
- **Text polish:** >= <= -> ug cm2 to proper symbols, LaTeX removed, spaced dashes replaced, "you" removed from 5 stems, US spellings (-ize) changed.
- **STEP1:** the 139 question images that v3.6.12 linked (UWorld figures already in the pack) are kept, through `step1/img_links_v3612.json`. Its other STEP1 changes are not carried over: about 420 machine-written why-not lines that read as fragments ("Vs Protein carrier (13, s0197): Oil/water partition co..."), lead-in sentences added as clues, invented sequential UWorld numbers (UW-10001 onwards) and templated "twin" questions the app never shows (2.5 MB). STEP1 options did not change, so STEP1 saves were never at risk.
- Answer-length spread now matches the papers (answer is the longest option in 15% of Hammer questions vs 19% of the mock and 23% of the official papers; shortest 22% vs 18%).

## 3.6.10 (2026-11-05)

🧹 **Last sweep: clones, classroom framing, last negative lead-in** (31 questions).
- **Clones I had created myself, fixed.** Seven rebuilds in 3.6.5 to 3.6.8 had landed on an angle the bank already asked (SCC in a transplant patient, ACE inhibitor angioedema, riluzole, Boerhaave, popliteal aneurysm with aortic scan, phyllodes excision, torsion of the appendix testis). Each was rebuilt again, after checking its answer against every answer in the bank: Bowen's disease, hereditary angioedema (C1 inhibitor), gastrostomy in MND, Mallory-Weiss tear, elective popliteal aneurysm repair, duct ectasia, and renal ultrasound for a new varicocele in an older man.
- **Remaining true clones rebuilt:** acamprosate (now its mechanism), endophthalmitis (now its treatment), DVT (interim anticoagulation when the scan is delayed), troponin (chronic myocardial injury in CKD), ischaemic colitis (supportive care), urinary retention (post-obstructive diuresis), spirometry (fixed obstruction).
- **Last negative lead-in gone:** "in which situation does tranexamic acid not help?" is now a heavy-periods vignette where a past DVT rules out tranexamic acid.
- **Classroom framing removed** from 14 stems ("the examiner asks you", "a medical student asks", "the registrar asks you to work out"), and two "which patient" lists became single vignettes (urgent endoscopy at 58 with weight loss; tonsillectomy criteria).
- **Bank now:** longest option is the answer in 20.4% of questions; 0 length stand-outs; 0 true negative lead-ins; clone flags left are set E or different topics that share an answer.

## 3.6.9 (2026-11-05)

🎓 **Mock-like now matches the mock's shape**, plus the good parts of an outside (Gemini) audit, checked against the data first.
- **Lead-in mix fixed.** The chip was 84% "most likely diagnosis" questions; your mock is 53%. It now holds **802** questions: 54% diagnosis, 29% management, 6% investigation, 9% other (mock 53 / 24 / 8 / 13). The added management and investigation questions are ones with no length, framing, clone or negative flags, reviewed ones first.
- **Mock week weighting.** With the chip on, a shuffled run is weighted by week to match the mock (acute abdomen and mental health about 15% each, instead of every week equal). Without the chip nothing changes.
- **Precision give-aways fixed (20 questions).** The answer was the only option with a dose, a strength or "urgent" (for example "IM glucagon 1 mg" against four bare options). The answer is trimmed, or a lookalike gets the same precision ("Urgent scrotal ultrasound first").
- **Last throwaway distractors replaced** in the untouched weeks after a hand read of all 247 flagged questions there: chemotherapy for a BCC, vasectomy for fertility before orchidectomy, isotretinoin for recurrent boils.
- **Official paper explanations:** 23 chatbot openers ("Based on the information given, ...") removed and 2 bare-letter answers ("the most likely diagnosis is E.") replaced with the option itself.

## 3.6.8 (2026-11-05)

🩺 **The rest of the bank: clones and negative lead-ins** (21 questions rebuilt, 18 lead-ins rewritten; set E left as written).
- **Breast:** periductal mastitis prevention (stop smoking), inflammatory cancer referral, Paget's biopsy, phyllodes excision.
- **Leg:** diabetic foot ulcer (foot care team within 1 working day), Marjolin biopsy, varicose veins with skin changes (refer), popliteal aneurysm (scan the aorta), lymphoedema (compression and skin care).
- **Abdomen and GI:** fistula-in-ano (MRI pelvis), chronic fissure (GTN), unstable diverticular bleed (CT angiography), Boerhaave, day 3 rescue therapy in acute severe colitis.
- **Chest, cough and blood:** Pancoast (chest X-ray first), dissection (CT aortic angiogram), torsades (stop QT drugs), endocarditis with heart failure (urgent valve surgery), TTP rewritten in paper style (plasma exchange, platelets avoided).
- **Endocrine and joints:** TSH over 10 twice (levothyroxine), RA X-ray (periarticular erosions) replacing "which is not a sign of OA".
- **Drug and test cards:** "which should be avoided" now reads positively, for example "which antibiotic is most likely to worsen her myasthenia?" and "which patient has a contraindication to sumatriptan?".
- **Whole bank now:** the longest option is the answer in **20.8%** of questions (papers: 19 to 25%), with **0** stand-outs. 466 questions have been rewritten since 3.6.3.

## 3.6.7 (2026-11-05)

🧴🧠 **Skin, neurology and renal weeks: clones rebuilt** (29 questions; set E left as written).
- **Skin (15):** the same diagnosis asked twice is now a second angle: SCC in a transplant patient, malignant acanthosis (gastric cancer), pretibial myxoedema, ACE inhibitor angioedema, eczema herpeticum management (aciclovir and same-day referral), facial eczema steroid strength, pseudofolliculitis advice, Fournier's debridement, plantar wart treatment, crusted scabies (ivermectin with permethrin), the guttate psoriasis trigger (ASO titre), Löfgren chest X-ray, necrotising fasciitis vs cellulitis (disproportionate pain), tinea cruris treatment and TEN management.
- **Neurology (9):** riluzole in MND, cerebral toxoplasmosis in HIV, brain abscess antibiotics, bacterial meningitis treatment (ceftriaxone with dexamethasone; amoxicillin only over 60), TB meningitis (four drugs for 12 months plus steroids). "Which should be avoided" lead-ins now read positively (UKMEC 4, which drug worsens myoclonus, which test carries the greatest risk).
- **Renal and urology (5):** retrograde urethrogram for stricture, phaeochromocytoma before VHL surgery, pyelonephritis antibiotic as a positive question (cefalexin, with lower-UTI-only drugs as distractors), torsion of the appendix testis (blue dot sign), and the pregnancy UTI lead-in turned positive.
- 🎓 Mock-like chip: **509**.

## 3.6.6 (2026-11-05)

🎯 **b targets read through one by one** (17 questions; set E left as written).
- **Missing result restored:** the Addison's question asked "what does this result mean?" without showing the 9 am cortisol. It now shows 520 nmol/L and asks for the interpretation (over about 500: Addison's very unlikely; 100 to 500: synacthen).
- **Clones and recall-only items rebuilt:** otosclerosis now asks the tympanometry result (shallow peak, no stapedial reflex) instead of repeating the set E diagnosis question; "name the cluster C disorders" is now a vignette of avoidant personality disorder; pityriasis versicolor asks the organism (Malassezia); Kawasaki is in paper style with short options (IVIG and aspirin), not sentence-long ones with "alone" and "only" in the wrong answers.
- **Weak distractors replaced:** cochlear implant and tympanoplasty for otosclerosis, a cholinesterase inhibitor for late-onset hallucinations, the right colic artery for the caecum (lead-in now "mainly supplies the caecum", which removes an argument about the ascending colon), port-site and positioning pain for shoulder-tip pain, intranasal antihistamine and montelukast for hay fever.
- **Lead-ins in paper style:** "What does this suggest?" and "What is this called?" now read "Which is the most likely diagnosis?" or "Which term best describes this?".
- 🎓 Mock-like chip: **503**.

## 3.6.5 (2026-11-05)

👁️👂 **Eyes and ENT rebuilt by hand** (53 questions), so your Saturday revision is drilling different facts, not the same fact three times.
- **29 clones rebuilt as new angles.** Contact lens keratitis was asked three times as "same-day referral"; now one asks the organism (Pseudomonas), one the prevention advice (Acanthamoeba and tap water) and one is a simple corneal abrasion. Uveitis diagnosis three times is now sarcoidosis, HLA-B27 and a steroid pressure rise. Orbital cellulitis CT three times is now orbital vs periorbital, abscess drainage and the abducens nerve in cavernous sinus thrombosis. Also new: amaurosis fugax carotid imaging, warfarin and INR, tractional detachment, chalazion first steps, neonatal chlamydia, OCT for wet AMD, injection endophthalmitis, chemical burn severity, white-eyed blow-out, cataract complications and the DVLA standard; in ENT Ramsay Hunt treatment, vestibular migraine, buccal prochlorperazine, home sleep study, hardwood adenocarcinoma, quinsy drainage, sternomastoid tumour, unresponsive choking, bacterial tracheitis, dermoid cyst, the Sistrunk hyoid and rigid bronchoscopy.
- **Negative lead-ins gone** ("which drops should be avoided", "which should be avoided"): the herpes ulcer now asks which drop made it worse, the metal-hammering eye asks for the investigation (CT, not MRI) and the swimmer's perforated drum asks which drops to use.
- **Weak distractors replaced with real lookalikes** in 16 more questions, for example ocular massage beside steroids for GCA, NSAID eye drops and oral prednisolone beside oral NSAID for scleritis, mupirocin beside Naseptin, routine vs suspected cancer ENT referral.
- 🎓 Mock-like chip now holds **501** questions (rebuilt clones join it).
- **Your runs are safe** across both releases: a run saved on 3.6.3 or 3.6.4 moves its picks to the new letters (tested on a question changed in both), and a pick on a rebuilt question is cleared.
- Engine: a question can now be rewritten again in a later batch (`v364_rw.py` applies each batch in order with its own data version). Release number lives in `study/snap/rw/VERSION`.

## 3.6.4 (2026-11-05)

🔨 **Hammer rebuilt towards your mock.** An audit against your 91-question mock and the 599 MSCAA and MS AKT questions found Hammer about 80% like the real papers. The gaps were weak distractors, a length give-away, clones and too few diagnosis questions. This release fixes those, priority weeks first.
- **Length give-away gone:** in 3.6.3 the longest option was the answer 31.9% of the time (the papers: 19 to 25%). Every Hammer question where the answer stood out by length (more than 15% and 3 characters longer than every other option) was evened out, by trimming the answer or giving a distractor real detail. Now **25.0%**, and **0** questions where the answer stands out.
- **Priority weeks rewritten by hand: acute abdomen and jaundice, mental health, eyes, ENT and the b targets.** Weak option sets now hold real lookalikes, for example the Crohn's drug question now offers adalimumab, budesonide, infliximab and methotrexate, not ferrous sulfate and vitamin D. Negative lead-ins ("which should be avoided") are now positive, as the MSCAA style guide requires.
- **Clones rebuilt as new questions:** 30 questions that repeated an earlier answer and angle (catatonia three times, adjustment disorder four times, cholangitis three times) now test something new in the same unit: delusional perception, waxy flexibility, the lorazepam challenge, prolonged grief, multisystemic therapy, Prader-Willi, schizotypal disorder, partner treatment in PID, PTC drainage after a failed ERCP and more.
- **All 251 card-matched why-not lines in the priority weeks rewritten from their own stems.** The 3.6.3 card match had put wrong lines on some options (labetalol explained by raised intracranial pressure, "no treatment" by Wenckebach).
- **3.6.0 imports restyled** to paper format (h1743, h1744, h1746, h1749, h1750, h1751), with short options instead of sentence-long ones. The DKA potassium question now follows the JBDS rule (below 3.5: senior review for extra potassium).
- 🎓 **Mock-like chip** in the Hammer view: 495 questions made of the b targets, set E and condition questions that ask for the diagnosis or cause (55% of your mock does), with clones left out.
- **Your runs are safe.** When options are re-sorted, a half-finished run moves your pick and crossed-out options to the new letters; a pick on a rebuilt question is cleared. Tested in the browser.
- Source: `study/snap/rw/rw_NN_*.py` (one file per batch), applied by `site/patches/v364_rw.py` with `v364_engine.py` and `v364_ml.py`; `study/snap/rw/rebuild.sh` rebuilds STUDY from the 3.6.3 page. `study/snap/rw/detect.py` is the weak-question detector.

## 3.6.3 (2026-11-05)

✍️ **"Why not" lines rewritten by hand, and STUDY cleaned up.** You found the old explanations lazy (the pilocarpine and sigmoid volvulus cards); every wrong option across all three banks now has a line written from its own stem.
- **Removed:** 1,483 template lines ("the clinical findings instead specifically indicated X rather than Y") and 542 copy-paste "Ruled out by ..." lines that pasted the gate under every wrong option.
- **Filled from your own cards:** 785 lines taken from your triggers, drug, test and procedure cards where they already had the right fact.
- **Hand-written:** 2,683 lines: 549 for your mock, the official papers, h0227 and h0313, and 2,134 for 1,211 Hammer questions. Each says what that option would need, or what it actually treats, in one short British English sentence. Coverage check: 0 wrong options without a line or a flip in Hammer, mock or the official papers.
- Source: `study/snap/wn_hand.py` and `wn_hand2.py`, applied by `site/patches/v363_hand.py` (safe to re-run; it never overwrites a line except the ids listed in `wn_hand2.REWRITE`).
- **Review cards:** one card per option, with ❌ why not and 🔀 change the film side by side. 🔬 Deep dive opens the gate, the cues and every flip. ✨ AI fill writes a line for any option that is still empty and saves it with your progress (`S.tmai`), so it syncs and survives a reload.
- **USMLE questions moved out of STUDY.** 54 of the 66 questions added in 3.6.0 were USMLE basic science filed under FFP units, and each showed a UWorld screenshot whose notes gave the answer away. They now live only in STEP1 (49 were already there; 5 move across through `step1/from_study.json`). The 12 clinical ones stay: 11 re-filed to their units, and 3 outside your ILOs (pre-eclampsia, ectopic, Kawasaki) sit under their own clearly labelled heading.
- **Calcium gluconate:** the hyperkalaemia card and trigger line now note that older papers write "10 mL of 10%" (30 mL is current UK guidance), so both wordings are recognised.
- **AI:** the system prompt names STUDY or STEP1 by page; images are now sent to Gemini, OpenAI and Groq. The 📲 sync button now shows on phones.

**STEP1:**
- **Confirm answer is off by default.** Tapping an option answers it; existing saves are moved over once, and the setting can still be switched back on.
- 🇬🇧 **FFP overlap chip** to drill only questions that overlap your FFP ILOs.
- **UK names and units strip** beside US drug names and lab values.
- UWorld screenshot notes now appear only **after** you answer, so they can't give the answer away.

## 3.6.2 (2026-11-05)

🔨 **Hammer set E: 87 new paper-style SBAs (h1779 to h1865)** in STUDY, written fresh around core FFP AKT topics and modelled on the MS AKT, MSCAA and Nottingham mock papers: stems of about 60 words with observations in a second paragraph, results tables in 38 of them, 5 alphabetical options and the papers' lead-ins.
- Topics: thyroid surgery and nodules, anal fissure, volvulus, diverticulitis, large bowel obstruction, rectal and bladder cancer, visible haematuria, renal colic, ADPKD, post-streptococcal GN, NSTEMI antiplatelets, vasospastic angina, stable chest pain, heart failure, dissection imaging, asthma, pneumoconiosis, bronchiectasis (3 angles), TB (2), sarcoidosis, pneumonia severity, pulmonary oedema, respiratory acidosis, hepatitis E, Gilbert syndrome, cholangitis, pancreatitis, coeliac, UC, C. difficile, Shigella, dysphagia and pharyngeal pouch, B12, hypercalcaemia, hyperkalaemia, hypoglycaemia, SSRI hyponatraemia, thyrotoxicosis, Paget's, RA, psoriatic arthritis (3 angles), anti-Jo-1, ACJ arthritis, GCA, embolus, psoriasis triggers, scabies, plantar wart, BCC, acne, onychomycosis, orbital cellulitis, uveitis, wet AMD, steroid cataract, hypertensive retinopathy, amaurosis fugax, otosclerosis, epiglottitis, HSV encephalitis, SAH, lumbar puncture safety, schizoid personality, BPD and DBT, bipolar, anorexia, conduct disorder, ADHD, aripiprazole, best interests, autonomy, hepatitis B precautions.
- Every question has a thought map with cues taken word for word from the stem, up to 3 change-the-film flips, and a "why not" line for all 4 wrong options. All pass the Hammer linter (no give-away lengths, no absolute words in distractors, British spelling).
- New Hammer targets: Viral hepatitis, Infection control and bloodborne viruses, Ethics: the four principles, Jaundice and LFT patterns, Paget's disease and metabolic bone, Rheumatoid and psoriatic arthritis, Dysphagia and pharyngeal pouch.
- 🆕 **Set E chip** in the Hammer view to drill the 87 on their own (`site/patches/v362_engine.py`; hidden in STEP1).
- Source: `study/snap/hq6_a.py`, `hq6_b.py`, `hq6_c.py`, applied by `site/patches/v362_sba.py` (`--check` lints without writing).

## 3.6.1 (2026-11-05)

🔍 **Audit of 3.6.0 (the Antigravity update): everything kept, the weak parts rewritten, new depth on top.** 3.5.0 and 3.6.0 were built outside this repo; 3.6.1 brings both in and repairs them.

**STEP1 data** (`step1/pack_base.json` is the 3.6.0 data untouched; `step1/improve_pack.py` writes `pack.json` from it, so a future import is repaired the same way):
- 1,649 questions kept. Every templated "twin" (the same stem with a new age) retired; 1,426 UWorld and 165 High-Yield 4-box explanations rebuilt from each question's own explanation: red flags that are really in the stem, the money line, the inflow → outflow chain and a why-not for each wrong option. High-Yield arrow questions now say exactly which arrow each wrong option gets wrong (660 lines).
- Your 58 hand-written renal SBAs had been given made-up UWorld ids in 3.6.0; they are recognised again (matched to `src/sba_*.txt`), keep every hand-written flip and are labelled 🎯 medengine originals.
- 645 questions re-filed to the topic they actually test (a renal question was sitting under Cardiology), by matching the question's words against each topic.
- OCR repair: 392 broken words, 298 garbled runs, 111 lead-ins that were cut off restored, 1,203 lines of website chrome ("Previous", "Next", "Correct answer", peer statistics) and 47 duplicated passages removed. The original explanation is kept in `eo`.
- Your notes: 1,126 "High-Yield / NBME rule" and "Pathophysiology / First Aid pearl" lines had their blank on the wrong answer (aminocaproic acid → Psoriasis). Each line is now filed under the topic it describes; 60 keep a blank on the right answer, the rest read as plain facts. 48 bare outline headings and image file names dropped.
- 60 UWorld images now shipped in `img/`; 52 US terms merged into the glossary; 14 posters moved to the right topic.

**STUDY**: the 66 new Hammer SBAs (h1713 on) and their images kept. 308 stems had one of 11 stock sentences glued on; they come off. Every hand-written flip that 3.6.0 overwrote with generated padding is back; padding that taught something moved to "Why not". Header link to STEP1.

**New in STEP1:**
- 🏦 **Bank chips** on the block setup: UWorld, High-Yield, Mine, or any mix.
- 📊 **Per-system bars** on home from your last answers, with one tap to drill your weakest system.
- ✨ **Sharpen** and 🔁 **Twin** in the review: your AI rewrites a weak 4-box or writes a real twin (new patient, same concept, different answer), saved on your device. 📋 Copy the question as text for Anki.
- Engine: `EXT.tmExtra` hook in the review (`site/patches/v361_engine.py`); no change when no pack declares it.

## 3.4.0 (2026-11-04)

🎯 **medengine-STEP1: a USMLE Step 1 app on the STUDY engine** (`step1.html`, third card on the launcher, key 3).
- **Its own saves.** Every storage key, both IndexedDB names, the save file format, the cloud backup table (`med_backups_step1`, run `step1/supabase_step1.sql` once) and the topic discussion threads (`s1u:`) are separate, and STEP1 never publishes a leaderboard profile. A browser test seeds STUDY and OSCE progress, uses STEP1 hard, and checks nothing of theirs changed.
- **Breadth from day one:** all 16 First Aid chapters as 237 topics with 855 red-flag trigger lines in the one-line High-Yield format (scene, flip word, answer), every line a drop-down blank whose wrong options are the neighbouring answers, each labelled with its own scene. Browse by the 2026 USMLE content outline systems with their exam weights.
- **Deep pilot: renal, acid-base and electrolytes.** 22 topics of high-yield cloze notes (227 drop-down blanks, each with 3 written distractors), 58 NBME-style questions with US units and drug names (results tables, alphabetical options, British English explanations), 21 domino arrows with 26 change-the-film flips, 9 inflow to outflow mechanism chains.
- **The 4-box explanation** on every question: 🎯 Red flags, 💰 Money line, 🌊 Inflow → outflow, and 🔀 Change the film for every wrong option, plus a why-not line for each.
- **Domino arrows** now colour each value as 🔴 primary insult, 🟡 knock-on or 🟢 compensation once answered, and offer 🔀 flips that change one feature of the case (Conn → renal artery stenosis → Liddle).
- **⚡ UWorld Deconstruct:** paste a missed question and its explanation, or drop a screenshot. Your AI (Claude in the artifact, your own key on the website) returns the 4 boxes, an arrows drill, a twin question with a new patient, and Anki cards, all in fresh words; the paste itself is never stored. ✍️ By hand works without AI. Copy every card as tab-separated text for Anki.
- **⏱️ Timed block:** 20 questions in 30 minutes, as in the 2026 exam, with marking, strike-out, a navigator, keyboard answers and lab values beside the question; no feedback until the end, then review every answer in the Hammer view.
- **🧭 Acid-base compass:** pH, primary process, Winter and the other compensation rules, albumin-corrected anion gap, delta ratio and osmolar gap, drawn on a bicarbonate against CO₂ map with every compensation band (47 unit tests).
- **🫘 Nephron map:** tap a segment for its transporters, hormones, drugs and diseases; pick a diuretic to light up where it acts.
- **🧪 US lab values with the UK bridge** (60 tests with SI equivalents and a converter); the Hammer reference ranges switch to US units in STEP1.
- **🔺 Eponym decoder** (52) and **US abbreviations and drug names with the UK term** (57).
- Content is written fresh in our own words; nothing is copied from First Aid, High-Yield, UWorld, Boards and Beyond or Bootcamp.
- Engine: STUDY gains small pack hooks (`site/patches/v340_pack_hooks.py` and `v340_pack_hooks2.py`); with no pack declared it behaves exactly as before (checked view by view against 3.3.5).

## 3.3.5 (2026-11-04)

🔨 **SBA audit: Hammer questions checked against the real papers.**
- Benchmarked all 1,632 Hammer SBAs against the 91 Nottingham mock questions and the 599 MSC and MSCAA paper questions: stem length, question types, option style, answer position and how often the answer is the longest option all sit close to the real papers. The big difference was data: 3% of Hammer questions had a results table, against 23 to 36% of the papers.
- Read every drug, test and procedure question (408) and a random 150 condition questions. Fixed: stable lithium is checked every 6 months, not 3 (h0446); hyperthermia is one of the 4 Hs, so h1469 had two right answers; h0794 offered carbimazole options to a patient on mesalazine; h1458 mixed products with ratios; h0738 asked for the "usual" maximum but meant the short-term one; h0659 gave LDL a total cholesterol range; h1305 anion gap wording; missing ranges in h0533 and h0843.
- Two near-copies rewritten as new angles on the same topic: h1504 is now Fitz-Hugh-Curtis syndrome, h1626 posterior capsule opacification.
- 69 stems that listed 2 or more results in prose now show them in an Investigations table, with any later text under it, as on the papers.
- 🆕 **80 new Hammer SBAs (h1633 to h1712)**: 51 with full results tables and normal decoy rows (fluids and electrolytes, AKI, anaemia, DKA and HHS, thyroid, LFTs, Glasgow score, blood gases, pleural fluid, CSF, lithium, staggered paracetamol, coeliac with IgA deficiency, CK, FH, CPPD, ACR, PE, GI bleed, SIADH, PTHrP) and 29 on ILO topics no question asked (RV infarct, Dressler's, LV aneurysm, torsades, hypertensive emergency, Cushing's triad, false localising VI, CIDP, CMT, mononeuritis multiplex, Argyll Robertson, carotid dissection, hydroxychloroquine screening, uric acid, struvite and enteric oxalate stones, Heberden's nodes, von Willebrand, angiofibroma, Bacillus cereus, Yersinia, acanthosis nigricans, convulsive syncope, dissociative seizures, laryngomalacia, choanal atresia, DT timing, FMD, Trousseau's, antiphospholipid, gastric outlet obstruction, carbon monoxide). Every one has a thought map and a "why not" line for all 4 wrong options.
- Source: `study/snap/hq5_data.py`, applied by `site/patches/v335_sba.py` (linted for give-away option lengths and absolute words; every cue checked against the stem or results). Saved progress keeps its ids; 69 converted stems may shift a saved highlight by one paragraph.

## 3.3.4 (2026-11-03)

🎯 **Voice stations are marked from Whisper too.** With a Groq or OpenAI key, a 🎙 Voice station quietly records your own turns (paused while the patient or examiner speaks). ⚡ End & Mark sends that recording to Whisper, primed with the station's words, and marks the accurate transcript instead of the browser's guesses. Without a key, or if Whisper fails, it marks the browser text as before. The Voice card says when this is on.

## 3.3.3 (2026-11-03)

🎯 **Accurate dictation in 📋 Grade (Whisper).** With a Groq (gsk_…) or OpenAI (sk-…) key, 🎯 Accurate dictate records the station and sends the audio to Whisper (Groq: whisper-large-v3-turbo) with a vocabulary hint built from the station's own clinical words plus common OSCE words, then fills the box and marks it. Website copy only; the audio goes to your key's provider.

## 3.3.2 (2026-11-03)

📋 **Grade marks what you actually said.**
- Found with a real abdominal transcript: every domain scored 4/4 although consent, the chaperone and the board-like rigidity were never mentioned. The general matcher accepted any 2 words of a bullet from anywhere in the transcript, and "a look, feel and listen to your abdomen" was quoted as proof for 9 bullets.
- Now only discriminating words count (words shared by many of a station's bullets are ignored), they must occur together within about 25 words, longer bullets need 3, with light stemming. A vague opening now scores 3% instead of most of the domains.
- More voice slips fixed: "date to Beth", "purchase/podcast for" (percuss), "puppet" (palpate), "light partitions", "iliac fossil", "pygastric", "sifting bonus" (shifting dullness), "rossing", "bow the kidneys", "use une's".
- Mannequin stations: the AI speaks only as the examiner.

## 3.3.1 (2026-11-03)

🎙️ **TalkType (or any dictation app) straight into 📋 Grade.**
- `osce.html#talk=<text>` catches a transcript from an iPhone or Mac Shortcut (share sheet or clipboard). It is a #fragment, so the text never reaches the web server, and it is cleared from the address bar at once.
- The transcript goes to the station you last used and is marked automatically. With no station yet, it waits for the next one you open; for a 🔒 My circuit station, it waits until you unlock.
- 📋 Paste & mark: one tap reads the clipboard into 📋 Grade and marks it (website copy; the claude.ai viewer blocks clipboard reads).

## 3.3.0 (2026-11-03)

The three files in `site/` are now the source of truth (Antigravity and Claude both edit them). `python3 site/build.py` makes the website zip, the offline zip and the two claude.ai artifacts. Every change is a patch script in `site/patches/`.

🔐 **Cloud security (STUDY).**
- v3.2.0's Supabase tables let anyone with the public key read, edit and delete every row, and the page kept every password and PIN in plain text. Now: Supabase Auth (email and password, reset by email), per-user row-level security, a private backup table, one vote per person, and pings only the recipient can read. Run `site/data/medengine-v3.3.0-supabase.sql` once.
- The old password registry is wiped on load; anything from the network is cleaned and escaped before it reaches the page.
- Progress Shield snapshots moved to IndexedDB (they were filling localStorage and silently stopping saves). Saves that fail now say so.
- Tested against a mock Supabase: no requests while signed out, every request carries the user's token, a 401 refreshes and retries, hostile names do not run.

⏳ **Voice stations wait for you.** 2.5 s after your last word by default (1.5, 3.5, 5 s or tap to send), plus 1.5 s if you trail off on "and…" or "um…", with a countdown bar, ➤ Send (Enter) and ✋ Hold (Esc).

🧬 **Mnemonics on every frame, examination and procedure (OSCE).** 84 aids, each tagged by kind (letters, route, rule, numbers, groups, picture, or ⛔ none) with why it fits and when it would hurt; TAGBS-P is marked as yours. A card on every station, a hub with search and filters, a letter quiz, and your own mnemonics per station.

🔒 **My circuit (OSCE).** Import a private station pack, seal it with your own password (AES-GCM, PBKDF2 with 600,000 rounds) and unlock it to practise. No station content ships in this repository or the zips.

🛡️ **📋 Grade: safety and order checks.** Tourniquet off before the needle, no resheathing, label at the bedside, urine before the balloon, positive ID for blood, pH not "whoosh", direct suicide questions, apology for the error itself. Negation-aware ("I won't re-palpate"). A missed safety step caps the station at 54%, as an examiner would. Voice fixes are now scoped to the right station ("thorough examination" only becomes thyroid in a thyroid station; "deflated" is no longer turned into "lethargic"). ✨ Fix words in the box. 📚 A link from the grade to that condition's SBAs in STUDY (`study.html#hq-u<n>`). The offline examiner no longer invents non-negotiables or a timeline.

⚡ **Thought maps (STUDY).** v3.2.0 padded every map to 4 flips; about 1 in 10 added flips was wrong, and 1,383 were reasons rather than flips. The 2,122 hand-written maps are restored and re-validated; the 1,383 reasons now sit in their own ❌ "Why not the others" list. The 200 MS AKT 2026 maps were cleaned (plain words, no dashes or brackets; no flips on "which feature" questions).

🧹 **Fixes.** AI defaults back to Haiku 5.5 and Sonnet 5.5 (v3.2.0 silently downgraded them). Every OSCE page fits a 390 px phone (40 overflowed). STUDY poster tabs no longer overflow. "Sketchy" labels renamed "Scenes" (trademark). Education-only line on the launcher. The public web build drops the character skins and cursors.

## 2.7.3 (2026-10-30)

⚡ **STUDY: an arrow thought map on every explanation.**
- After you answer, the explanation opens with 🎯 Trigger cues ➔ ⚙️ Mechanism ➔ ⚖️ Decisive gate ➔ ✅ Answer.
- Under the gate, "↳ 🔀 If instead…" lines show the one change to the stem that would make a distractor right, for up to 3 distractors.
- It runs left to right on a laptop and stacks top to bottom on a phone.
- All 2,122 questions have one: 399 MSC paper questions, 91 Nottingham mock questions and all 1,632 Hammer questions. The maps were written by hand in `study/snap/maps/m000.txt` to `m106.txt`. The build checks that every cue is verbatim in the stem or results, and that every flip names a real wrong option.

🖍️ **STUDY: a cue check on your highlights.**
- After you answer, your yellow highlights stay. The real trigger cues are underlined in green in the stem and the Investigations table.
- The score line says how many cues your highlights caught.
- On a phone, a floating 🖍️ Highlight ON/OFF pill sits above the answers. Scrolling never highlights.

☁️ **STUDY: 🔥 My misses now sync between devices.**
- Misses are merged item by item: both devices' misses are kept, the higher seen count wins, and a miss marked fixed stays fixed.
- They go only to your private per-user database. Vault images still stay on the device.

🧹 **Data fixes**
- BP values such as 232/134 no longer render as "232/13 mmHg4".
- Sweat chloride, vaginal pH, NG aspirate pH and conjunctival pH no longer get serum reference ranges added.

📦 **Build:** `offline/dist/medengine-code-audit.zip` is the website zip without `img/`. It stays under 20 MB for audit tools with an upload cap.
- Test: `study/test_study_v273.py` checks 100% map coverage, map placement, flips, the green cue underline, the phone pill and layout at 390 px, and a laptop and phone merging misses.

## 2.7.2 (2026-10-29)

🖍️ **STUDY: highlighter on every question, like SBA Bank.**
- Drag across words, or tap a word, and it turns yellow. Tap more words next to it to build a phrase.
- Tap a highlight to remove it, or use 🧽 to clear the whole question.
- 🖍️ or <kbd>H</kbd> switches the pen on and off.
- Highlights work on the stem, the Investigations table and the lead-in. They stay through answering and review, and they are kept per question.

📲 **STUDY: carry on from your laptop to your phone.**
- **☁️ Automatic sync is fixed.** Progress used to go to the database as one document, and documents are capped at 256 KiB. Once a progress record grew past that, sync switched itself off without saying so.
- Progress is now split into parts and chunks, and each part is merged record by record:
  - each saved run is matched by its ID and the newer one wins; ended runs stay deleted;
  - question stats keep the higher attempt count;
  - streak days and highlights are merged.
- So two devices never wipe each other's work. Sync pulls when you return to the tab and every minute, and pushes when you leave.
- The run header now shows ☁️ synced or 💾 saved. Tap it, or 📲 in the top bar, for the devices panel.
- **💾 Save file and 📋 save code** move everything between devices, including the offline and website copies that cannot sync: progress, runs, highlights, 🔥 My misses and remix cards. Loading merges rather than replaces. The API key is never included.
- Test: `study/test_study_v271.py` plays a laptop and a phone against a mock database with the real size limit, plus a no-Claude copy loading a save code.

## 2.7.1 (2026-10-29)

📝 **STUDY 2.7.1: every Hammer question is now a full MSCAA-length vignette.** All 1,632 stems were rewritten by hand, so none read like "A woman with DKA has…" any more.
- Each stem follows the paper order: who the patient is, with an age and the story; then observations and examination; then results; then the lead-in on its own line.
- The median stem is now 49 words. The official MSC papers' median is 57.
- The keyed answer, the options, the explanation and the facts that tell the options apart are unchanged. Where a stem needed a detail to keep the answer right, it was added: for example, a CURB-65 of 4, apixaban dose-reduction criteria, and a frame-only walker for hemiarthroplasty.
- Set C chains keep the same patient across all three steps.
- Results are written in as text, so the range filter adds MSCAA reference ranges and builds an Investigations table when there are three or more results.
- Source files are `study/snap/vignettes/v00.txt` to `v32.txt`, read by `mscaa.vignettes()`. `test_study_v27.py` now checks that every Hammer item has a vignette, that the median length is at least 45 words, and that stems contain no dashes or non-range brackets.

🎓 **OSCE:** the introduction lines and AI prompts now say "fourth-year medical student".

## 2.7.0 (2026-10-29)

🎭 **A full case for every OSCE station.** All 444 history, psychiatry and examination cases now have a proper patient script, not a few sparse lines. This covers the 141 past-paper variants, every bank history and psychiatry station, the core Y stations, and 2 to 3 cases for each of the 24 examination stations.
- **🎭 Patient sheet (Friends → Patient):** how to play the part, a verbatim opening line, the story if given space, an answer for each history question, yes and no symptoms, background, ideas, concerns and expectations, a hidden cue, and a question to ask the candidate. Exam cases list the findings to mime or read out.
- **📋 Examiner sheet:** the verbatim presentation, three-tier differentials (most likely, common alternative, must-not-miss, each with a because), investigations in order, management, and what to tell the patient.
- **📝 Script and ✅ mark scheme:** each case adds "This case: what to ask" (or "what the examiner looks for") with the reason for each question, red flags, and a "Present, differentials and next steps" section.
- Exam cases can carry their own door brief, so choosing case B of the cardiovascular station gives the 71-year-old woman with mitral regurgitation. Bank stations whose door text lost a sentence to the results filter now read in full.
- Build: `content/cases/*.txt`, `build/build_cases.py --strict` (fails if any station lacks a case). Test: `app/build/test_v27.py`.

📝 **STUDY 2.7.0: MSCAA layout.** All 1,632 Hammer questions and 91 mock questions are laid out the way the MSCAA and MS AKT papers are:
- ages written "54 year old";
- history, then a new paragraph for observations and examination;
- observations written "pulse rate 104 bpm", "BP 88/50 mmHg";
- the lead-in on its own line, worded "Which is the most…";
- options in alphabetical order (numbers in ascending order), with saved runs remapped.
🧪 Results carry the reference ranges printed in the papers, and three or more results become an Investigations table. Fluid results (pleural, CSF, urine) are left without serum ranges. Code: `study/snap/mscaa.py`.

🟦 **Fixed:** blocker and question words such as "initial", "safest" and "takes warfarin" were drawn as full-width rounded cards, because the highlighter's class name clashed with an existing card style. They're plain text again, highlighted only in 🦅 Scan mode.

🔒 **Examiner patterns no longer give the answers away:**
- the set chips show only ○ (not done), ✅ or ❌;
- the pattern rule stays folded behind "🔓 Show the pattern" until the whole set is done;
- finishing a 🧬 set shows the pattern at the end.

🗺️ **Snapshot under every answer:** the condition's poster and up to 6 🔑 clinchers from the notes. It can be collapsed and remembers that choice.

🧹 Removed the "© Medical Schools Council… Page n of N" footers that had leaked into 224 official justifications. Test: `study/test_study_v27.py`.

## STUDY 2.6.1 (2026-10-29)

🔀 **Multi-select Hammer filters.** Every chip row now takes several picks: inside a row they add together (official papers plus my mock; 🔨 plus 🔨🔨; in my ILOs plus ILO edge; not done plus missed), and across rows they narrow each other. The paper and ILO rows narrow official questions only, so mixing sources still works. The examiner-pattern row has an "In any of these / In all of these" switch, and a ✕ Clear filters button resets everything.

## 2.6.0 (2026-10-29)

🔒 **No spoilers in Hammer SBAs.** Before you answer, the tag row shows only where the question comes from (🔨 Hammer SBA, 🎓 Mock Qn or 🏛️ paper Qn), its hammer rating and reference, and "🔒 Topic after you answer". The topic, the pattern, the ILO verdict and the 🔥 double-tested badge appear once you answer. Run labels that name a topic in the header wait too; examiner-pattern runs show "🧬 Examiner pattern set".

💾 **Every run is saved.** Up to 12 unfinished runs are kept on this device, newest first, each with its place, answers, cross-outs, score so far and age, and a ▶ Resume and 🗑 button in the hub. Starting a new run no longer wipes the last one; reopening the same set resumes it; 🏁 End closes it. A "💾 saved" note sits in the header. The old single saved run is migrated.

🎤 **OSCE: three new frameworks** (12 tiles), built from the Gemini advice where it added to what the app had:
- **🎤 Present to the examiner and give differentials:** headline, key positives, important negatives, to complete, three-tier differentials (likely, common alternative, must-not-miss, each with a "because"), investigations in order, first management. Variations after a history, an abnormal or a normal examination, a data station, and the examiner's "Differentials?", "Investigate?" and "Manage?" questions.
- **🔀 What to say next:** a timed junction line for every change of section in a 10-minute station, plus rescues for a blank mind, a cue or tears, an interruption, not knowing, forgetting something, running out of time, being challenged and an angry patient.
- **🗺 Management plan:** urgency, bedside, bloods, imaging, conservative, named first-line drug, specialist with urgency, safety-net; filled in for all 16 ILO weeks with UK guidance.
- History, examination, data and psychiatry stations show a 🎤 Present, differentials and plan card (outside poster view) for their type and ILO week. Test: `app/build/test_v26.py`.

## 2.5.1 (2026-10-29)

🎯 **ILO audit of all 399 official questions**, one by one, against the 168 FFP ILO conditions.
- **Verdicts:** 🎯 218 in my ILOs (the condition or decision tested is an ILO condition or its listed content), 🟡 69 on the edge (inside one of the 16 ILO weeks as a differential, complication or principle), 🌍 112 outside (obstetrics and gynaecology, paediatrics, statistics and ethics, rheumatology and orthopaedics, renal and endocrine, trauma and anaesthetics, other neurology, haematology, infection and genetics). This corrects 2.5.0, which counted 73% as inside by pinning edge questions to the nearest unit.
- **Every question carries its verdict:** a badge before you answer and a one-line 🎯 ILO check after it; outside questions say which specialty they belong to. The ILO filter now has the three levels, and condition pages count only in-ILO and edge questions.
- **🎯 ILO audit panel** in the Hammer hub: verdict totals, a per-week breakdown, the outside questions by specialty, and all 399 rows with the reason, each one tap to practise.
- Long URLs in the examiners' justifications now wrap on phones. Content in `study/snap/off_ilo.py`; tests check every verdict and the full audit list.

## 2.5.0 (2026-10-29)

🏛️ **The official practice papers inside medengine-STUDY, decoded.**
- **399 official questions** with their answers, images and the examiners' justifications: MS AKT practice papers 1 and 2 (Medical Schools Council, 2023) and the MSCAA practice papers of December 2017, November 2018, December 2019 and December 2020. Parsed from the answer-key PDFs; lab results become real Investigations tables with reference ranges; the 21 images (ECGs, X-rays, CT, fundus and skin photos) are embedded.
- **Tagged like the mock:** each question has an ILO unit (73% sit inside the FFP ILOs; the rest are marked 🌍 beyond them), a hammer rating, a pattern and a 🔄 flip. Filter by paper, by inside or beyond the ILOs, and by examiner pattern. Each condition page's 🔨 button now includes its official questions.
- **🦅 Scan mode (S):** the question line moves to the top, out-of-range lab rows and vitals light up with ↑ or ↓, normal rows fade, and blocker words (CKD, Parkinson's, pregnant, a job, a valve, warfarin) get the highlighter. Works on every question.
- **🧬 Examiner patterns:** 45 hand-checked groups that link questions across the papers and the mock: 🔥 double-tested (near word for word, or the same X-ray reused for a different answer), ⛓️ same patient at the next step, 🚫 a comorbidity that blocks first line, ⚠️ lab decoys just over the line, 🧮 one decision grid tested from every angle, 🔗 the same trap in a new patient. After each answer the pattern box shows the rule and runs the whole set in order.
- **🏛️ The official papers, decoded:** a blueprint computed from the papers: question types against the mock, story length, lab tables and how many lab rows are normal decoys.
- **Set C: 162 new MSCAA-style hammers.** For each of the 54 ILO units the official papers never asked about, one patient across three questions (diagnosis, test or number, treatment with a blocker), with vitals blocks and Investigations tables. `hammer.py` gains `$` lab rows and `!` patient rules; question ids for sets A and B are unchanged, so saved progress carries over.
- Content in `study/snap/official/` (papers and images), `off_meta_*.py` (my tags), `off_links.py` (the groups) and `hq3_*.py` (set C). Tests: `study/test_study_v22.py` checks the official data, filters, scan mode, pattern runs, images and lab tables.

## 2.4.0 (2026-10-28)

🔨 **Hammer SBAs, SBA Bank-style, and 501 new mock-style questions.**
- **Move back and forth:** a numbered palette (green right, red wrong) jumps to any question; ← Prev and Next →, or the arrow keys, move without losing answers. 🏁 End finishes early; ✕ Leave keeps your place.
- **Save and come back:** every pick, cross-out and your place are saved with your progress. The Hammer hub shows ⏸ Unfinished run with ▶ Resume, after a reload too.
- **Cross out options** before you answer: tap ✕, right-click the option or press Shift and the letter. Tap again to undo.
- **🧲 Triggers under the answer:** after each answer, the matching ⭐ signature line and up to 4 trigger lines (condition clues, bugs, drugs, investigations, management), with a jump to that unit's triggers.
- **No give-away options:** every option set was rebalanced so the answer is not the longest or most detailed one (it had been the longest in 47% of questions; now about 28%, close to the 20% of chance, with tiny margins), and distractors no longer carry absolute words such as only, never or always. `hammer.py` now fails any question whose answer is much longer than every distractor or whose distractors carry an absolute word the answer lacks.
- **Set B: 501 new questions written to the mock's style:** 3 more for every ILO condition (unit 57 gets 6), with realistic vignettes, numbers to interpret, short sibling options and the same pattern mix. Total 1,470 hammers plus the 91 mock questions.
- Content in `study/snap/hq2_*.py`. Tests: `study/test_study_v22.py` now checks the palette, Prev and ArrowLeft, cross-outs, resume after reload, triggers under the answer and the option-length audit; the oldest STUDY tests accept 2.x versions.

## 2.3.0 (2026-10-28)

🔨 **Hammer SBAs** in medengine-STUDY, built from the formative mock: what it tests, and three graded questions for everything in the ILOs.
- **969 new single-best-answer questions, written in our own words for UK practice:** 3 for each of the 166 ILO conditions (61 and 88 share the pages they repeat), 83 drug groups, 53 tests and procedures, and 21 off-map topics the mock tested from just outside the ILO titles (otosclerosis, CSF leak, Budd-Chiari, misidentification delusions, grief, vasculitis, colonic blood supply, node drainage, adrenal tests and more).
- **The hammer scale:** 🔨 the classic picture, 🔨🔨 two steps, a lookalike or a number that overrides the story, 🔨🔨🔨 the curveball. Each question is tagged with the pattern it tests: 👯 lookalike, 🔢 number, 📍 place, time or anatomy, 💊 drug, 🪜 right rung (the first step versus the definitive one).
- **🔄 The flip** after every answer: the one change to the stem that would make another option right.
- **🎓 My mock:** the paper's 91 unique questions (Q84 repeats Q83) with their answers and explanations, each tagged with its hammer, pattern, ILO and flip, and a 📊 blueprint of what the paper asked by system, question type, source and pattern.
- **Use it:** filter by source, hammer, pattern, system, not done or missed last time; A to E or 1 to 5 to answer, Enter for next, Esc to leave; results are saved with your progress; the end screen ranks your patterns and redoes the misses. Every condition page has its own 🔨 button, and search offers matching questions.
- Content in `study/snap/hq_*.py`, linted by `hammer.py` (one question at each level per target, 5 options, one answer, no brackets, dashes or US spellings); mock in `study/snap/mock92.json` with `mock_meta.py`. Tests: `study/test_study_v22.py`.

## 2.2.0 (2026-10-28)

🧲 Triggers: every one of the 1,975 word-hunt clues gone through by hand, system by system.
- **The flipping word is highlighted on every clue**: the phrase the exam hides the answer behind, in highlighter, in Triggers and on each condition's word-hunt panel.
- **Stacks, High-Yield's left column:** clues that share a scene now sit together under one label (After an MI: the timeline; Reading the ECG; Which bug; Small cells; Big cells; Broken cells; The withdrawal clock; and 430 more), so the scene stays still and only the highlighted word changes. On a phone the label sits on top.
- **Answers brought up to date where they were wrong:** open-angle glaucoma now starts with selective laser trabeculoplasty (NICE NG81); suspected wet AMD goes to a macula service within 1 working day (NICE NG82).
- Content in `study/snap/hl_*.py` (one file per ILO system), checked by `hlmark.py`: every clue covered once, every phrase found, no stack split in two.
- Tests: `test_trg.py` now fails if any condition clue has no highlighted word.

## 2.1.0 (2026-10-28)

🧲 **Triggers** in both apps: the High-Yield HY pattern for everything in the ILOs.
- **One line = the scene + the word that flips it → the answer.** The flipping words are in highlighter; lines that share a scene stack together so only that word changes. 3,410 lines on one scroll, each with a small picture: the organ, the kind of clue (ECG, scan, bloods, child, pregnancy, travel, drug, fever), a bug's real Gram-stain look (purple positive, pink negative, rods, cocci, spirals, yeast, mould), a drug's route, or the kind of procedure.
- **5 parts:** 🩺 **Conditions** (a ⭐ signature trigger for all 168 ILO conditions plus the 1,975 word-hunt clues), 🦠 **Bugs** (76 organisms filed under the scene the exam sets, with a picture key), 💊 **Drugs** (every ILO drug: the scene that calls for it, then the catches), 🔬 **Investigations** (scores such as Wells, CURB-65, CHA2DS2-VASc and GRACE; bloods; X-ray, CT, CT angiography, MRI, MRCP, ultrasound; OGD, colonoscopy, flexible sigmoidoscopy, cystoscopy, ERCP and other scopes; bedside tests) and 🛠️ **Management** (cardioversion, pacing, valve replacement and TAVI, needle decompression, chest drains, VATS, coiling, thrombectomy, hemiarthroplasty, DHS and nails, EVAR, TURP, TURBT, stomas and bowel operations, ENT and eye surgery, therapies and the Mental Health Act).
- **Use it:** ⌘F or Ctrl+F filters it, press again for the browser's own find; a jump list for every section; 🔒 Lock or L blurs the answers, tap or N reveals; each condition's word hunt and ILO page link to its own triggers; search shows a Triggers result.
- Written in our own words for UK practice (NICE, BTS, BNF, MHRA, RC UK, the Mental Health Act). One shared engine, `app/src/trg.js`; content in `study/snap/t_cond.py`, `t_bugs.py`, `t_drugs.py`, `t_ix.py`, `t_mx.py`, linted by `triggers.py`.
- Tests: `app/build/test_trg.py` for both apps.

## 2.0.0 (2026-10-27)

Both apps rebuilt around one picture code: 🗺️ **posters**.
- **The code, PLACE + LOCK.** Every poster puts the same zone in the same place and colour: 🧬 what goes wrong top-left, 🧍 who top-right, 🧪 prove it on the right, 💊 treat bottom-right, 🚩 watch for bottom-left, ⚖️ the lookalike on the left, 👀 spot it in the middle on a body or head map, 🪝 the hook along the bottom. Words sit inside the picture, arrows carry the mechanism, one hook per poster. 🔒 **Lock** or the L key turns drugs, doses, numbers, signs and findings into amber pills: say them, then tap or press N, with a counter. ▶ **Walk it** lights the zones in reading order.
- **medengine-STUDY:** every condition page opens on its poster, unlocked when reading and locked in Fill, SBA and Recall so it scaffolds without spoiling. The 🎞️ film and 🖼️ pictures sit in tabs beside it. ⚖️ **Don't confuse with** on all 165 conditions: each next to its classic lookalike, compared on one shared axis.
- 🧭 **14 master posters** with drawn figures: spirometry, mitral stenosis, anterior uveitis, sore throat and CT contrast rebuilt from the AI-made infographics with every error fixed and listed under 🔎; plus the red eye, dizziness and hearing, stable or unstable first moves, antidotes, the pain ladder and opioid maths, nerve injuries on a body map, bowel operations and stomas, antibodies pinned to their organs, and four murmurs on one time axis.
- 🖼️ **My infographics** in STUDY: paste, drop or choose a picture, drag boxes over the details, then study by tapping each box. Kept only in this browser on this device.
- **medengine-OSCE:** 🗺️ Poster is the first mode on every station. History, psychiatry, drug, communication and imaging stations become a 10-minute clock with 4 timed corners built from each station's own data, with the plan forked by case; ⚡ **Last 2 min**, automatic at the 8:00 gong, collapses it to the plan. The 24 examinations become a route round a body or a head: props before you touch, numbered pins, what to hunt for, how to complete. The 15 procedures become a 3-frame storyboard with the move that fails each frame and the numbers to know, including the proteinuria plan on the urine dip. ILO pages open on the condition poster; a 🗺️ Posters hub holds them all.
- **Hand and wrist, and shoulder, examinations removed:** not in the FFP CPSA. The FFP checklist is now 63 items.
- **⌘F / Ctrl+F** jumps to the search bar in both apps; press it again there for the browser's own find. Search finds the master posters.
- **Accuracy pass:** type 2 diabetes to NICE NG28 2026, modified-release metformin with an SGLT2 inhibitor from diagnosis and semaglutide for artery disease; lipid targets from NG238; FeverPAIN and Centor bands from NG84; IBS as a positive diagnosis; thunderclap headache peaking within 1 to 5 minutes; wet AMD to a macula clinic within 1 working day; the uveitis HLA-B27 list and treatment order; asthma control wording; goal-directed fluids in pancreatitis; brackets removed from station posters.
- 🙈 Test me is now 🔒 Lock everywhere.
- Tests: `app/build/test_v9.py`, `study/test_study_v20.py`; all earlier suites pass.

## 1.5.0 (2026-10-25)

medengine-STUDY: a picture snapshot for every condition.
- 🎞️ **Snapshot at the top of all 168 ILO conditions:** the same 7-frame picture film every time, so only the content changes. 1 🧬 **What goes wrong:** the organ is drawn with the broken part glowing, and the chain runs down in arrows. 2 🧍 **Who gets it.** 3 👀 **Spot it:** numbered dots on a body map. 4 🧪 **Prove it:** the tests, with ★ on the one that proves it. 5 💊 **Treat:** a ladder from first move to cure. 6 🚩 **Watch for:** each danger colour-coded by how fast to act. 7 🪝 **The hook.** UK guidance, written in our own words.
- 17 drawn organ pictures carry them: heart, lungs, limb vessels, gut, liver and pancreas, urinary tract, scrotum, breast, thyroid, diabetes, brain, nerve and muscle, joint, skin, eye, ear nose and throat, the mind and the blood.
- ▶ plays a snapshot like a GIF, swiping steps it, and 🙈 **Test me** hides the words so you say each frame before you tap. **More pictures** under each snapshot opens the matching medengine-OSCE drawings.
- 🎞️ **Snapshots** section on the home screen: all of them by ILO week, with a filter.
- Tests: `study/test_study_v15.py`; all earlier STUDY suites pass.

## 1.4.0 (2026-10-25)

medengine-OSCE: learn the skeleton once, then only remember what is special to each station.
- 🚩 **Red flags → where to send** on every history and psychiatry station, matched to its conditions: the flag, what it means, what you do and how fast (🔴 999 or A&E · 🟠 same-day specialist · 🟣 suspected cancer pathway · 🟡 urgent · 🟢 routine). 21 sheets cover all 168 ILO conditions, written from current UK guidance including the NG12 suspected cancer changes (oesophago-gastric to the suspected cancer pathway, FIT 10 or more). A 🚩 browser with a filter sits on the History and Psychiatry pages and the home screen.
- 🧱 **Skeleton card** on every station: the moves that never change for that kind of station, as a chip row, with the mnemonics that carry them: SOCRATES, ICE, MJ THREADS, SADDO, Present in 4, WIPER, IPPA, Look Feel Move, SEADS, SWIFT, Tell People Really Calm Stories, UMN goes up, DANISH, LR6 SO4, S S S C T F, DCM, PREP and DONE, SPIKES, Ask Tell Ask, ASEPTIC, SIGECAPS, DIGFAST.
- 🎯 **Only remember for this one:** the hooks card now holds just the station's own specifics. Generic lines the skeleton covers are gone; new hooks include AS = SAD, the 3 Cs of a big liver, the unhappy triad and CAGE.
- 🖼️ **47 new step-through pictures (128 in all):** SOCRATES, chest pain patterns, abdominal pain by region, headache onset curves, palpitations, breathlessness timing, leg swelling, TUNA FISH, sepsis, CAGE and units, the NG12 age ladder, ASEPTIC, SIGECAPS, DIGFAST, SAD PERSONS as a prompt only, SWIFT, DANISH, SEADS, the lump checklist, arm and leg myotomes with MRC grades, the plantar response, JVP vs carotid, Schamroth's window, endocarditis hands, liver signs, knee tests, RA vs OA hands and the hand nerves, true vs apparent leg length, Simmonds', otoscope grip, confrontation, the swinging torch, thyroid eye signs, PREP and DONE, cannula angle, BP cuff, male and female catheter, ECG rate, axis, heart block strips, heart failure on a CXR, CT windows, insulin profiles and DOAC vs warfarin. History and psychiatry stations now get up to 4 pictures for their presentation.
- 🙈 **Test me** on pictures: hides the labels and captions so you say them first, then tap the picture to check. Resets on every step.
- ✅ **Leaner checklists:** the history skeleton is 13 items with the mnemonics built in, and histories now close with a thank-you instead of a plan and safety-net. ⓘ words and the why now appear on 745 of 1,045 past-paper mark-scheme items.
- Tests: `app/build/test_v8.py`.

## 1.3.0 (2026-10-25)

medengine-OSCE rebuilt around how FFP stations actually run: **one station, one 10-minute task**.
- 🏠 **New home and navigation by station type:** 🗣️ History · 🩺 Examination · 🖼️ Imaging and ECG · 💊 Drug counselling · 💬 Communication · 🧪 Procedures · 🧠 Psychiatry. Each type opens with how that station runs in 5 steps, a filter box and a 🎲 random button.
- ✅ **Your FFP checklist** on the home screen: all 65 items from the paper list, each linked to its station, ticked with your best score once practised.
- ✂️ **No more packed stations.** The past papers that crammed a history, an examination, results and counselling into 10 minutes are split: the history becomes a history station that ends by presenting to the examiner, the explanation becomes its own talking station, and the examination findings become practice cases on the matching examination. A–E, prescribing-chart and data stations that aren't FFP types are no longer listed.
- 🩺 **Every FFP examination and procedure rewritten from scratch** with what to do, the exact words to say and why each step scores: 26 examinations including new ankle and foot, elbow, external genitalia, rash, lesions, nose, mouth, otoscopy and hearing, anterior eye, acuity and fields, and fundoscopy; 15 procedures including hand washing and male and female catheterisation. Each has hooks, the traps, a model presentation and "present these findings" cases with a tap-to-reveal model answer.
- 💊 **15 drug counselling stations** on the FFP list (inhalers, steroids, hypertension, heart failure, antipsychotics, antidepressants, insulin, tablets for diabetes, thyroid, alcohol, NSAIDs and PPIs, anticoagulation, home oxygen, QRISK and CHA2DS2-VASc, ORBIT and falls), each with 2 to 3 actor cases. 💬 SPIKES, explaining a diagnosis and antibiotic stewardship. 🧠 Mental health history and risk assessment, with the past-paper MSE and suicide risk stations. 🖼️ Chest X-ray, abdominal X-ray, CT and ECG with drawn case pictures.
- 🖼️ **81 step-through pictures** that play like a GIF (tap ▶, or swipe): where to listen and murmur shapes, chest signs, eye movements, visual field lesions, facial palsy, dermatomes, abdominal regions, thyroid, Ottawa rules, the painful arc, Trendelenburg, breast clock, the scrotal lump tree, the prostate, lesion words, ABCDE, the nose, the mouth, the eardrum, Rinne and Weber, the neck node loop, red eye, Snellen, fundi, Korotkoff, the 5 moments, ECG leads, the dipstick, cannula sizes, order of draw, Allen's test, inhalers, steroid tapering, the hypertension steps, heart failure pillars, the 4 Ms, hypo 15 and 15, the withdrawal clock, AF and stroke, 100-person risk pictures, CHA2DS2-VASc and ORBIT, SPIKES, chunk and check, and the imaging approaches. All drawn in the app, so they work offline and in dark mode.
- 🤖 AI patient and voice stay on the talking stations; on imaging stations the AI plays the examiner. Examination and procedure stations keep Script, Tick and Friends.
- Old links still work: STUDY's ILO links, and the old exam and procedure links now open the new stations. Saved attempts carry over.
- Tests: `app/build/test_v7.py`.

## 1.2.1 (2026-10-25)

- ⚡ **First move vs cure now covers every ILO condition** (168 of 168) in 84 cards: related conditions share a card so it stays lean. New: aortic dissection, lipids, endocarditis, effusion, bronchitis/Covid/bronchiectasis, lung cancer and fibrosis, malnutrition and refeeding, IBS and constipation, perianal abscess, lower GI bleed, appendicitis, PID, the acute abdomen, mastitis, veins and Raynaud's, the diabetes annual review, thyroid cancer, BPH and stricture, prostate cancer and cord compression, penis and scrotum, OA and joint replacement, raised ICP and brain infections, GBS/myasthenia/MND, first-episode psychosis, depression, anxiety/PTSD/OCD, eating disorders and perinatal, neurodevelopment and catatonia, alcohol and drugs, delirium, the derm step-up, skin infections and infestations, skin failure, children's ENT and airway, vertigo and Bell's, and the eye.
- Tests: a coverage check fails if any ILO condition has no ⚡ card, or if the deck grows past 120 cards.

## 1.2.0 (2026-10-25)

- ⚡ **First move vs cure**: 48 decision cards in the same arrow style as 🧬 Why it happens, for the acute and high-yield ILO conditions. 🔴 unstable vs 🟢 stable splits and 1️⃣ → 2️⃣ → 🎯 ladders: tachy and brady arrhythmias, ACS, heart failure, the NICE hypertension ladder, PE, DVT, acute asthma, COPD oxygen, pneumothorax, CURB-65, sepsis, upper GI bleed, perforation, UC flares, gallstones, coeliac, reflux, fissure, diverticulitis, hernias, bowel cancer surgery by site, obstruction, breast referral and hormone drugs, DKA vs HHS, hypoglycaemia, thyroid, adrenal crisis, hyperkalaemia, AKI, renal colic, UTI, the acute scrotum and urology 2-week waits, status epilepticus, SAH, meningitis, C. diff and food poisoning, TB, skin, eye and ENT emergencies, psychiatric drug emergencies, antidotes, anaemia, opioid maths. UK guidance only. Own section (search, system chips, 📖 Read all, a "read it like a playmaker" cue), plus a ⚡ strip on each condition's Think tab.
- 🔄 Remix grounds next-step answers with the matching ⚡ card as well as the 🧬 card.
- 🔥 **My misses**: import a misses file made from your SBA Bank history (kept on your device only, never in the app or the repo). Each miss is your old pick vs the right answer, cued by the learning point with the answer hidden; never re-done misses first; right on two separate days and it is fixed; keyboard 1/2 and Enter.
- 🧬 New card: nerve injuries, where the bone breaks and which nerve stops (112 cards).
- Tests: `study/test_study_v12.py`; all earlier suites pass.

## 1.1.0 (2026-10-24)

- 🧬 **Why it happens** now has its own section (home screen, and "All cards" on every condition): all **111** mechanism cards grouped by system, with a search box, system chips and **📖 Read all** to open every card and read straight through.
- **Every card rewritten as movement**: one chain per line, cause → what physically happens → what you see, arrows in every line (coloured so the movement stands out), bold key words, no brackets, contrasts on one shared axis ("A vs B: X vs Y").
- **33 new cards** for the ILO conditions that had none: acid-base and respiratory failure, Covid and bronchitis, infective diarrhoea, the pain ladder, bladder and kidney cancer, epilepsy, nerve vs junction vs muscle, Bell's palsy, vertigo, the four dopamine roads, serotonin syndrome vs NMS, depression and bipolar, lithium, paracetamol overdose, panic/phobia/PTSD/OCD, delirium, catatonia and ECT, eating disorders and refeeding, perinatal mental health, ADHD, urticaria, eczema vs psoriasis, acne, skin infections, ears, sore throats and the child's airway, sinusitis, nosebleeds, sleep apnoea, the red eye, glaucoma, cataract/AMD/detachment, orbital cellulitis.
- Tests: `study/test_study_v11.py`; all earlier suites pass.

## 1.0.0 (2026-10-24)

medengine v1.0. Same app, same screens, deeper "why". Saved progress carries over.
- 🧬 **16 new mechanism cards** in the Pathophysiology library (78 in all), written in our own words, each in the "A vs B: X vs Y" frame with cause → what physically happens → the finding: the gallstone ladder, bowel obstruction (small vs large, ileus, volvulus), groin hernias, above vs below the dentate line, gut ischaemia, PID and ectopic, acute scrotum, thyrotoxicosis (overmaking vs leaking), thiamine and Wernicke's, the four shocks, hormone-driven hypertension, murmurs by valve and phase, nipple discharge and mastitis, familial hypercholesterolaemia, varicose veins/lymphoedema/Raynaud's, and perforation. They appear on each condition's 🧠 Think tab, in the Pathophysiology library and in Remix.
- 🔄 **Remix "why" lines are grounded**: the AI now gets the best-matching checked card from your library (the one naming the most of the question's options) and is told to stay consistent with it; the same card closes the lineup.
- Content audit: written with a USMLE course (Bootcamp) as a reference for which mechanisms and contrasts matter, cross-checked against standard UK teaching; no course text or images are included, and management stays UK.
- medengine-OSCE: version label only (v1.0.0); the stations are unchanged.
- Tests: `study/test_study_v10.py`; all earlier suites still pass.

## 0.10.0-beta (2026-10-24)

Remix rebuilt around one idea: **same patient, five endings**. Saved cards carry over (older AI cards switch to the new format after their next review).
- Every round is the **same case with the same five options in the same places**; one clue changes and you watch which option wins. The option you picked comes first. No more pregnancy twists or whole new cases.
- For each option, the AI gives one line on one shared axis: **option ← the clue that picks it 🔗 a picture hook**, plus a **🧬 Pathophysiology-style "why"** (cause → what physically happens: the finding), with the key words in bold.
- The end of each card is the **🧬 Why it happens** lineup: an "A vs B: X vs Y" title, the five rows, and the matching Pathophysiology card from your library (closed until you tap it).
- Offline: SBA Bank's own per-option lines are trimmed to the clue ("is for an obstructed, infected kidney" → *an obstructed, infected kidney*) and become the rounds and the lineup; your ILO clinchers are the fallback.
- Only a whole option name is hidden in a clue, so clues stay readable.

## 0.9.1-beta (2026-10-24)

Remix made simple again: v0.8's calm card with v0.9's useful parts kept underneath. Saved cards carry over.
- One card shape: 🎬 the case (deciding words in yellow), ✅ why right, ❌ why yours was wrong, then each variation as **one amber "If instead…" line** and the options. Removed: the struck-out/underlined animation, the answer-flip line, the rule box, the deciding-word chips, the "Original question" dropdown.
- **Replays start instantly.** The next round's new variations are made quietly after you finish a card and are ready next time; no "Fresh variations on the way…" wait and no "Use last time's" button. Smaller AI replies, so the first remix is quicker too.
- 🧩 **Compare all five + the rule** is tucked into one closed line at the end; open it only if you want it.
- 📷 is a single button on the check screen; 🚩 is a small icon.
- Kept: spaced ▶ Due today, exact ILO link, image paste, 🧠 Careful, misses by system, Weak spots.

## 0.9.0-beta (2026-10-24)

Remix v0.9 (medengine-STUDY; OSCE unchanged). Saved progress and v0.8 remix cards carry over.
- 🔁 **Fresh variations on every replay** (the AI is told which changes it has already used), on a spaced schedule: tomorrow → 3 days → a week → 3 weeks → 2 months, back to tomorrow after a miss. **▶ Due today** in the vault, on the paste screen and in Weak spots. The next card's variations are made while you answer the current one; "Use last time's" if the AI is slow.
- 🎬 **Spot the change**: the case line shows the old words struck out and the new words underlined (0.4 s, then still; off with reduced motion), and the answer flips (old → new) once you answer.
- 🧩 **All five, side by side** at the end of each card: one line per option ("it would be right if…"), from the AI or, offline, from SBA Bank's own per-option explanation.
- 🔑 **The rule** from SBA Bank's key-concept box, and 🔍 **deciding words** in yellow (chips plus the original stem, highlighted).
- 📷 **Image paste**: screenshot the ECG/X-ray/rash and ⌘V on the check screen (or before the text). Sent to the AI where it can take images (`sample: {images: true}` in the artifact; image blocks with your own key), stored on the device outside the Screenshot vault, tap to zoom.
- 🎯 Exact ILO link from SBA Bank's **Condition** tag; Weak spots shows Remix misses by condition; the vault shows **misses by system** as filters.
- 🚩 **Looks wrong** drops a variation for good; 🧠 **Careful** uses the stronger model (slower).
- Reader: warns when a question was pasted before submitting, ignores cross-out × marks unless exactly one option has one, strips "Deep dive", score and question-list lines.
- Tests: `study/test_study_v9.py` (pastes in Passmed layout written in our own words); v0.6–v0.8 suites still pass.

## 0.8.2-beta (2026-10-23)

- Remix: you're never stuck finishing a card or a replay. **📋 New question / ⏹ Stop replay** sits on every card, **Esc** goes straight back to the paste box (cursor ready), and pasting a new question mid-card or mid-replay starts it at once.

## 0.8.1-beta (2026-10-23)

- Fix "Empty answer" with your own AI key (website/download): newer models think by default and thinking counts toward `max_tokens`, so the 600-token quick budget could end with no text. Quick calls now switch thinking off (with a one-time fallback for custom models), Remix asks for 2,000 tokens, and an empty reply explains itself. Also fixes the OSCE AI patient on the website.
- Remix reader strips SBA Bank's answer percentages glued onto each option ("…area0%").
- Remix reader tuned to a real SBA Bank page copy: the case runs from "Question N of M" to the question (lab rows and short lines included), the related-video block can no longer be mistaken for the question, "<option> is correct." sets ✅, and page furniture (reference ranges, ratings, links, media, score) is stripped.

## 0.8.0-beta (2026-10-23)

medengine-STUDY only; OSCE build unchanged. Saved progress untouched.
- 🔄 **Remix**: paste a SBA Bank question you got wrong (⌘A, ⌘C, then ⌘V on the Remix page). The page clutter is stripped, you confirm ✅ the right answer and ✋ your pick, then get the case in one line plus three one-change variations (change one clue, change the patient, change the timeline), answered with 1-5. Uses AI where available (claude.ai `sample` in the artifact; the user's own key on the website/download, shared with OSCE), otherwise an offline remix that quizzes the clinchers of the matched ILO conditions. Remix vault in this browser with replay, only-misses, export and clear.
- ⏱ **Speed tags** on 63 conditions with one clear time course (⚡ sudden, 〰️ comes and goes, 🌊 fluctuates, 📈 gradual) with a filter under Browse.
- Plain-word labels in the decoder and sniper (what you see, memory hook, what do you do).
- Website/download STUDY now carries the AI key layer. Tests: `study/test_study_v8.py`.

## 0.7.0-beta (2026-10-23)

- 🎬🟰🏷️ Dual-code clinchers (29 rewritten, 18 added): what you see 🟰 the exam name with a memory hook → the diagnosis.
- 🔺 Jargon decoder: 40 exam names that don't describe what they are, each with what you see, hook, trap and what to do.
- Sniper modes: picture → name, name → picture, what do you do, or all three on one term.
- 🥊 WPW vs LBBB showdown with drawn strips (shared visual layer, `app/src/mev.js`; OSCE dist not rebuilt yet). Tests: `study/test_study_v7.py`.

## 0.6.0-beta (2026-10-20)

Visual layer, exam-proofing and sniper training. Both apps, nothing removed, saved progress untouched.

**Both apps**
- 👁️ **Clinical Atlas Lookup** on every station, framework, exam, ILO pack and STUDY condition: a 3-button row picked for the system (DermNet NZ for skin, LITFL ECGs for cardio, Radiopaedia / Radiology Masterclass for X-rays and CT, Google Images for fundoscopy and otoscopy) plus a lookup panel with all five atlases and an editable search. Opens in a new tab; nothing is downloaded.
- 🥊 **Visual showdowns, the Dirty Dozen (+1)**: BCC vs SCC, melanoma vs seborrhoeic keratosis, psoriasis vs discoid eczema, eczema herpeticum vs impetigo, diabetic retinopathy vs CRVO, CRVO vs CRAO, maculopathy vs proliferative, AOM vs glue ear, glue ear vs cholesteatoma, Mobitz I vs II vs complete block, hyper- vs hypokalaemia, effusion vs pneumothorax vs perforation, and STEMI territories. Each has drawn schematics (ECG strips, CXRs, fundi, eardrums, a tappable 12-lead map), a 🎬 mental film per side, ✂️ the one feature that splits them, the trap, and "Quiz me" with the name hidden.
- 🗂 **Systems and presentations** drop-downs (13 systems; presentation frameworks such as chest pain, SOB, abdo pain, jaundice).
- 🆕 **Guideline nuances** (one shared source, `app/content/updates_2026.json`): NICE NG28 Feb 2026 (MR metformin + SGLT2i dual first line; old QRISK rule flagged for older banks), Listeria cover age (≥60 vs >50 by source; NICE NG240 says "risk factors"), s5(2) only for inpatients and never in ED.

**medengine-OSCE**
- ⏱ The last 2 minutes turn the timer track amber, and a soft **8:00 chime** (Web Audio) plays so your ears cue the switch to reasoning, plan and safety-net. 🔔/🔕 toggle on the timer.
- 🎙 Voice marking: phonetic speech-to-text errors in drug and anatomy names are not penalised ("am load a pin" = amlodipine).
- T2DM station (PP49) updated to the 2026 NICE pathway.

**medengine-STUDY**
- 🎯 **Blind clincher sniper**: a clincher with the disease blacked out → name it, pick the first-line action or investigation (from the OSCE packs), call the lookalike trap; 🧬 Mutate keeps the presentation and changes one feature; misses recycle.
- 📋 **Paste exam image**: Ctrl+V / ⌘V (or long-press → Paste, or 📷 Choose image) on any condition saves a compressed screenshot under it (IndexedDB, localStorage fallback); 📋 Screenshot vault with a review mode that hides your note.
- 🆕 notes beside the older NICE lines in the original notes.

## 0.5.0-beta (2026-10-20)
First named release: **medengine.exe**.
- 107 past-paper OSCE stations (222 cases) with scripts (what to say and why), hooks, money lines, friend sheets (candidate, patient, examiner) and Nottingham-style domain marking.
- 🧭 Frameworks: 9 skeletons (history, psychiatric history, examination, procedure, A to E, explaining, prescribing, data interpretation, professional) and 108 variations showing what changes, a differential tree, and non-negotiables.
- ⛔ 18 universal non-negotiables on every station.
- 🤖 AI text stations and 🎙 voice stations: the AI plays patient and examiner, 10-minute timer with 5:00 and 9:00 signals, reading time, hands-free or push-to-talk.
- 🧑‍⚕️ AI examiner marking: domain scores with reasons, quoted fixes with exact words, non-negotiables, timeline, speech analytics, ideal last 90 seconds, viva questions, progress versus last attempt.
- 🪝 All hooks in one view (354 cards) plus flashcard drill.
- Website build: Appwrite accounts, AI via an Appwrite Function (Anthropic API), Stripe subscriptions (Pro) with webhook-managed access.

### 0.5.0-beta (rename)
- The OSCE app is now **medengine-OSCE** and the notes/SBA app is **medengine-STUDY** (both part of medengine.exe). Cross-links, page titles, website footer and legal pages updated. Saved progress is untouched (storage keys unchanged).
- Added the downloadable app (`offline/`): one launcher (`medengine.html`) for medengine-OSCE and medengine-STUDY, no sign-in, works offline; AI uses your own Anthropic key.
- Added a backup of the medengine-STUDY page under `study/`.
- One-file build `medengine.html` (both apps + images, instant switching, deep links between apps) and `medengine-website.zip` for iPhone/iPad via any static host. Cross-app links now open in the same tab.
