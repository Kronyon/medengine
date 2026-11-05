# Where v3.6.4 is (2026-11-05, evening)

Done and published:
- Detector (study/snap/rw/detect.py) over all 1,811 Hammer questions: triage.json flags len, mix, abs, clone, neg, frame.
- rw_01 acute abdomen, rw_02 mental health (incl. 24 clones rebuilt), rw_03 251 card-matched why-nots in priority weeks,
  rw_04 every length give-away in the whole bank (now 25.0% longest-correct, 0 stand-outs) + 3 imports restyled.
- Mock-like chip (495), run migration (q.pmv + hqMig), version 3.6.4.

Rules: rebuild with `sh study/snap/rw/rebuild.sh` then `python3 site/build.py`. Each rw_NN file is one published
batch with its own data version; never change option order in a published file, add rw_05, rw_06... instead.

Next (in order):
1. Eyes and ENT weak distractors and clones (rw_05).
2. b targets read-through (rw_06).
3. Other weeks: derm, neuro, haem, giupset, sob, cough, dm, abdopr, breast, leg, chest, joint, then d and x.
4. The 495 remaining card-matched why-nots outside the priority weeks.
