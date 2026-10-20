# Changelog

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
