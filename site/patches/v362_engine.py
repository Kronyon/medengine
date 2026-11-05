#!/usr/bin/env python3
"""v3.6.2: a "🆕 Set E" source chip in the Hammer view, so the 87 new paper-style SBAs can be drilled on their own.
The chip hides itself when a build has no set E questions (STEP1). Applied once."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
def must(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)
must("['b', '🧭', 'Off the map'], ['m', '🎓', 'My mock'], ['o', '🏛️', 'Official papers']];",
     "['b', '🧭', 'Off the map'], ['m', '🎓', 'My mock'], ['o', '🏛️', 'Official papers'], ['e', '🆕', 'Set E: FFP topics']];")
must("HQ_SRC.map(([k, ic, l]) => { const sub = k === 'all' ? all : all.filter(it => it.t === k), st = hqPctStats(sub); return chip(",
     "HQ_SRC.map(([k, ic, l]) => { const sub = k === 'all' ? all : all.filter(it => k === 'e' ? it.set === 'E' : it.t === k), st = hqPctStats(sub); if (k === 'e' && !sub.length) return ''; return chip(")
must("    if (!hqHas(c.src, it.t)) return false;",
     "    if (!hqHas(c.src, it.t) && !(it.set === 'E' && c.src.includes('e'))) return false;")
F.write_text(s, encoding='utf-8')
print('ok')
