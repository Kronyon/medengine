# Where v3.6.13 is (2026-11-05, night)

Done and published:
- Detector (study/snap/rw/detect.py) over all 1,811 Hammer questions: triage.json flags len, mix, abs, clone, neg, frame.
- rw_01 acute abdomen, rw_02 mental health (incl. 24 clones rebuilt), rw_03 251 card-matched why-nots in priority weeks,
  rw_04 every length give-away in the whole bank (now 25.0% longest-correct, 0 stand-outs) + 3 imports restyled.
- Mock-like chip (495), run migration (q.pmv + hqMig), version 3.6.4.
- rw_05 eyes and ENT: 29 clones rebuilt, 3 negative lead-ins, 16 distractor sets (v3.6.5, data version 7, chip 501).
  A qid may now appear in several rw files (applied in order). Bump study/snap/rw/VERSION per release.
- rw_06 b targets: 17 questions (v3.6.6, data version 8, chip 503). Set E untouched.
- rw_07 skin, neuro, renal: 29 clones and negative lead-ins (v3.6.7, data version 9, chip 509).
- rw_08 rest of the bank: 21 clones rebuilt + 18 negative lead-ins (v3.6.8, data version 10). Longest-correct 20.8%.
- rw_09 precision give-aways + last weak distractors; Mock-like rebalanced to the mock lead-in mix (802) with week weights q.mw
  (v364_ml.py) and a weighted shuffle (v369_engine.py); v369_polish.py cleans official explanations. v3.6.9, data version 11.
  The 'mix' flag is mostly noise: a hand read of all 247 untouched non-priority flags found about 5 truly weak.
- rw_10: my own collision clones re-rebuilt, last true clones, classroom framing, tranexamic negative lead-in (v3.6.10, data version 12).
  RULE: before writing a 'new' rebuild, check its answer against every answer in the bank (no new clone).
  Left on purpose: 5 'which patient' list questions (d/x cards), patient 'asks' stems (normal MSCAA style), set E.
- v3.6.13: the v3.6.12 Antigravity bank is IMPORTED after rw_01..10 (site/patches/v3613_import.py, data in
  study/snap/rw/import_v3612.json). Correct run migration at data version 13 (v3.6.12 shipped ov 14, kept so its runs stay).
  Fixes on top go in rw_13+ (data version 2+NN, so rw_13 = 15). rebuild.sh runs RW_MAX=10, import, RW_MIN=13.
  NEVER edit site/study.html by hand or ship a build that changes options without a pmv entry: saved runs break.
  study/snap/rw/focus.py WEEK prints only the clone and negative questions of a week with the question each copies.

Rules: rebuild with `sh study/snap/rw/rebuild.sh` then `python3 site/build.py`. Each rw_NN file is one published
batch with its own data version; never change option order in a published file, add rw_05, rw_06... instead.

Next (in order):
1. Weak distractors (mix flags, about 650, many benign) week by week, outside the priority weeks.
   Remaining clone flags are mostly set E or false positives (same answer, different topic).
2. The 495 remaining card-matched why-nots outside the priority weeks.
