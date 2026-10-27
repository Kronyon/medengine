# Changelog

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
- 🔥 **My misses**: import a misses file made from your Passmedicine history (kept on your device only, never in the app or the repo). Each miss is your old pick vs the right answer, cued by the learning point with the answer hidden; never re-done misses first; right on two separate days and it is fixed; keyboard 1/2 and Enter.
- 🧬 New card: nerve injuries, where the bone breaks and which nerve stops (112 cards).
- Tests: `study/test_study_v12.py`; all earlier suites pass.

## 1.1.0 (2026-10-24)

- 🧬 **Why it happens** now has its own section (home screen, and "All cards" on every condition): all **111** mechanism cards grouped by system, with a search box, system chips and **📖 Read all** to open every card and read straight through.
- **Every card rewritten as movement**: one chain per line, cause → what physically happens → what you see, arrows in every line (coloured so the movement stands out), bold key words, no brackets, contrasts on one shared axis ("A vs B: X vs Y").
- **33 new cards** for the ILO conditions that had none: acid-base and respiratory failure, Covid and bronchitis, infective diarrhoea, the pain ladder, bladder and kidney cancer, epilepsy, nerve vs junction vs muscle, Bell's palsy, vertigo, the four dopamine roads, serotonin syndrome vs NMS, depression and bipolar, lithium, paracetamol overdose, panic/phobia/PTSD/OCD, delirium, catatonia and ECT, eating disorders and refeeding, perinatal mental health, ADHD, urticaria, eczema vs psoriasis, acne, skin infections, ears, sore throats and the child's airway, sinusitis, nosebleeds, sleep apnoea, the red eye, glaucoma, cataract/AMD/detachment, orbital cellulitis.
- Tests: `study/test_study_v11.py`; all earlier suites pass.

## 1.0.0 (2026-10-24)

medengine v1.0. Same app, same screens, deeper "why". Saved progress carries over.
- 🧬 **16 new mechanism cards** in the Pathoma library (78 in all), written in our own words, each in the "A vs B: X vs Y" frame with cause → what physically happens → the finding: the gallstone ladder, bowel obstruction (small vs large, ileus, volvulus), groin hernias, above vs below the dentate line, gut ischaemia, PID and ectopic, acute scrotum, thyrotoxicosis (overmaking vs leaking), thiamine and Wernicke's, the four shocks, hormone-driven hypertension, murmurs by valve and phase, nipple discharge and mastitis, familial hypercholesterolaemia, varicose veins/lymphoedema/Raynaud's, and perforation. They appear on each condition's 🧠 Think tab, in the Pathoma library and in Remix.
- 🔄 **Remix "why" lines are grounded**: the AI now gets the best-matching checked card from your library (the one naming the most of the question's options) and is told to stay consistent with it; the same card closes the lineup.
- Content audit: written with a USMLE course (Bootcamp) as a reference for which mechanisms and contrasts matter, cross-checked against standard UK teaching; no course text or images are included, and management stays UK.
- medengine-OSCE: version label only (v1.0.0); the stations are unchanged.
- Tests: `study/test_study_v10.py`; all earlier suites still pass.

## 0.10.0-beta (2026-10-24)

Remix rebuilt around one idea: **same patient, five endings**. Saved cards carry over (older AI cards switch to the new format after their next review).
- Every round is the **same case with the same five options in the same places**; one clue changes and you watch which option wins. The option you picked comes first. No more pregnancy twists or whole new cases.
- For each option, the AI gives one line on one shared axis: **option ← the clue that picks it 🔗 a picture hook**, plus a **🧬 Pathoma-style "why"** (cause → what physically happens: the finding), with the key words in bold.
- The end of each card is the **🧬 Why it happens** lineup: an "A vs B: X vs Y" title, the five rows, and the matching Pathoma card from your library (closed until you tap it).
- Offline: Passmedicine's own per-option lines are trimmed to the clue ("is for an obstructed, infected kidney" → *an obstructed, infected kidney*) and become the rounds and the lineup; your ILO clinchers are the fallback.
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
- 🧩 **All five, side by side** at the end of each card: one line per option ("it would be right if…"), from the AI or, offline, from Passmedicine's own per-option explanation.
- 🔑 **The rule** from Passmedicine's key-concept box, and 🔍 **deciding words** in yellow (chips plus the original stem, highlighted).
- 📷 **Image paste**: screenshot the ECG/X-ray/rash and ⌘V on the check screen (or before the text). Sent to the AI where it can take images (`sample: {images: true}` in the artifact; image blocks with your own key), stored on the device outside the Screenshot vault, tap to zoom.
- 🎯 Exact ILO link from Passmedicine's **Condition** tag; Weak spots shows Remix misses by condition; the vault shows **misses by system** as filters.
- 🚩 **Looks wrong** drops a variation for good; 🧠 **Careful** uses the stronger model (slower).
- Reader: warns when a question was pasted before submitting, ignores cross-out × marks unless exactly one option has one, strips "Deep dive", score and question-list lines.
- Tests: `study/test_study_v9.py` (pastes in Passmed layout written in our own words); v0.6–v0.8 suites still pass.

## 0.8.2-beta (2026-10-23)

- Remix: you're never stuck finishing a card or a replay. **📋 New question / ⏹ Stop replay** sits on every card, **Esc** goes straight back to the paste box (cursor ready), and pasting a new question mid-card or mid-replay starts it at once.

## 0.8.1-beta (2026-10-23)

- Fix "Empty answer" with your own AI key (website/download): newer models think by default and thinking counts toward `max_tokens`, so the 600-token quick budget could end with no text. Quick calls now switch thinking off (with a one-time fallback for custom models), Remix asks for 2,000 tokens, and an empty reply explains itself. Also fixes the OSCE AI patient on the website.
- Remix reader strips Passmedicine's answer percentages glued onto each option ("…area0%").
- Remix reader tuned to a real Passmedicine page copy: the case runs from "Question N of M" to the question (lab rows and short lines included), the related-video block can no longer be mistaken for the question, "<option> is correct." sets ✅, and page furniture (reference ranges, ratings, links, media, score) is stripped.

## 0.8.0-beta (2026-10-23)

medengine-STUDY only; OSCE build unchanged. Saved progress untouched.
- 🔄 **Remix**: paste a Passmedicine question you got wrong (⌘A, ⌘C, then ⌘V on the Remix page). The page clutter is stripped, you confirm ✅ the right answer and ✋ your pick, then get the case in one line plus three one-change variations (change one clue, change the patient, change the timeline), answered with 1-5. Uses AI where available (claude.ai `sample` in the artifact; the user's own key on the website/download, shared with OSCE), otherwise an offline remix that quizzes the clinchers of the matched ILO conditions. Remix vault in this browser with replay, only-misses, export and clear.
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
