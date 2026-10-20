# Changelog

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
