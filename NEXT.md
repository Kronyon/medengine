# Where v3.6.8 is (2026-11-05, night)

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
  study/snap/rw/focus.py WEEK prints only the clone and negative questions of a week with the question each copies.

Rules: rebuild with `sh study/snap/rw/rebuild.sh` then `python3 site/build.py`. Each rw_NN file is one published
batch with its own data version; never change option order in a published file, add rw_05, rw_06... instead.

Next (in order):
1. Weak distractors (mix flags, about 650, many benign) week by week, outside the priority weeks.
   Remaining clone flags are mostly set E or false positives (same answer, different topic).
2. The 495 remaining card-matched why-nots outside the priority weeks.
