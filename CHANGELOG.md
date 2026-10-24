# Changelog

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
