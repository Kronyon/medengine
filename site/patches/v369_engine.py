#!/usr/bin/env python3
"""v3.6.9 engine: with the 🎓 Mock-like chip on, a shuffled run is weighted by week to match your mock
(acute abdomen and mental health about 15% each), using the per-question weight q.mw set by v364_ml.py.
Efraimidis-Spirakis weighted shuffle: key = r^(1/w), sort descending. Without the chip nothing changes."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
OLD = "      list = shuffle(list, rng(Date.now() & 0xffffffff));\n"
NEW = ("      const r = rng(Date.now() & 0xffffffff);\n"
       "      /* v3.6.9: Mock-like runs follow the mock's week weighting */\n"
       "      if ((hqCfg.src || []).includes('ml') && list.some(it => it.mw)) list = list.map(it => [Math.pow(r(), 1 / (it.mw || 1)), it]).sort((a, b) => b[0] - a[0]).map(x => x[1]);\n"
       "      else list = shuffle(list, r);\n")
assert s.count(OLD) == 1, 'shuffle line not found'
s = s.replace(OLD, NEW)
F.write_text(s, encoding='utf-8')
print('v369 engine ok')
