# medengine-STEP1

USMLE Step 1 on the medengine-STUDY engine. claude.ai artifact: https://claude.ai/artifact/GVUEwVwVsrm1akHoL9jJYX (publish `step1/medengine-step1.html` there with capabilities db, user, sample with images, downloads). `site/build.py` (`make_step1`) takes `site/study.html`, swaps in the Step 1 content pack, adds the Step 1 add-on and renames every storage key, so STEP1 and STUDY never share progress.

## Files

| File | What it is |
| --- | --- |
| `src/topics_*.txt` | First Aid chapters (`@`), topics (`#`) and red-flag trigger rows (`!` scene with **flip words** `\|` lock-in) |
| `src/notes_*.txt` | High-yield cloze notes: `## Topic`, `> block opener`, `- line` with `{{answer\|wrong\|wrong\|wrong}}` |
| `src/sba_*.txt` | Questions: stem, results table, options, why, red flags, money line, inflow → outflow, a flip and a why-not for every wrong option |
| `src/arrows_*.txt` | Domino arrows with roles (`p` primary, `k` knock-on, `c` compensation) and `>>` change-the-film flips |
| `src/path_*.txt` | Inflow → outflow mechanism chains |
| `src/eponyms.txt`, `src/gloss_us.txt` | Eponym decoder; US abbreviations and drug names with the UK term |
| `build_pack.py` | Validates everything above and writes the original 3.4.0 pack (any content error stops the build) |
| `pack_base.json` | The 3.6.0 pack with the UWorld, High-Yield and notes imports: the source of truth for data since 3.6.1. Never edited by hand by the build |
| `improve_pack.py` | Reads `pack_base.json` and writes `pack.json`: OCR and chrome clean-up, lead-ins restored, topics re-filed by what the question says, a real 4-box on every question, cards and note blanks rebuilt. Prints what it changed |
| `ext_step1.js`, `ext_step1.css` | UWorld Deconstruct, timed block, acid-base compass, nephron map, lab values |
| `test_step1.js` | Unit tests for the compass maths and lab conversions (`node step1/test_step1.js`) |
| `test_step1_page.js` | Browser test, including the storage isolation check (`node step1/test_step1_page.js http://localhost:PORT/step1.html`) |
| `supabase_step1.sql` | The private backup table for the website copy; run once in Supabase |
| `medengine-step1.html` | The claude.ai artifact build (derived; do not edit) |

## Adding a system in depth

1. Add `notes_<system>.txt`, `sba_<system>.txt`, `arrows_<system>.txt` and `path_<system>.txt`, using topic names exactly as they appear in the topics files.
2. Add the chapter id to `PILOT` in `build_pack.py`.
3. `python3 step1/build_pack.py && python3 site/build.py`, then run both tests.

## Since 3.6.1: the pipeline

`pack_base.json` → `python3 step1/improve_pack.py` → `pack.json` → `python3 site/build.py`. To bring in a new import, replace `pack_base.json` with it and rerun; your content is kept and only repaired. The add-on's Bank chips (UWorld, High-Yield, Mine), the 📊 per-system bars on home and the ✨ Sharpen / 🔁 Twin buttons in the review read the `src` field on each question.

Everything in `src/` is written in our own words. The UWorld and High-Yield imports in `pack_base.json` (tagged `src`) are used with permission and are kept whole.
