#!/usr/bin/env python3
"""v3.6.4 engine (applied once):
1. 🎓 Mock-like chip in the Hammer view: questions flagged ml (b targets, set E, diagnosis lead-ins, clones left out).
2. Saved runs survive option rewrites. When a question's options are rewritten and re-sorted, the data patch records the
   new order in q.pmv = [[version, map]]; every saved run (and the run being saved) is moved to the new letters, so a
   half-finished block never shows your old pick on a different option. AI why-not lines saved for a rewritten question
   are dropped, because hand-written lines now cover every option."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
def must(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)
must("['o', '🏛️', 'Official papers'], ['e', '🆕', 'Set E: FFP topics']];",
     "['o', '🏛️', 'Official papers'], ['e', '🆕', 'Set E: FFP topics'], ['ml', '🎓', 'Mock-like']];")
must("all.filter(it => k === 'e' ? it.set === 'E' : it.t === k), st = hqPctStats(sub); if (k === 'e' && !sub.length) return '';",
     "all.filter(it => k === 'e' ? it.set === 'E' : k === 'ml' ? !!it.ml : it.t === k), st = hqPctStats(sub); if ((k === 'e' || k === 'ml') && !sub.length) return '';")
must("    if (!hqHas(c.src, it.t) && !(it.set === 'E' && c.src.includes('e'))) return false;",
     "    if (!hqHas(c.src, it.t) && !(it.set === 'E' && c.src.includes('e')) && !(it.ml && c.src.includes('ml'))) return false;")
# run migration: one function used everywhere a run is read or saved
must("function hqRuns(){\n",
     "/* v3.6.4: move a saved run's picks and crossed-out options to the new letters after an option rewrite */\n"
     "function hqMig(r){\n"
     "  let ch = 0;\n"
     "  if (!r.ov) { Object.keys(r.pk || {}).forEach(id => { const q = hqItem(id); if (q && q.pm) r.pk[id] = q.pm[r.pk[id]]; }); Object.keys(r.x || {}).forEach(id => { const q = hqItem(id); if (q && q.pm) r.x[id] = r.x[id].map(v => q.pm[v]); }); r.ov = 2; ch = 1; }\n"
     "  const tgt = HQ.ov || 2;\n"
     "  if (r.ov < tgt) {\n"
     "    const mv = (q, v) => { (q.pmv || []).forEach(([ver, pm]) => { if (ver > r.ov && v != null) v = pm[v]; }); return v; };\n"
     "    Object.keys(r.pk || {}).forEach(id => { const q = hqItem(id); if (q && q.pmv) { const v = mv(q, r.pk[id]); if (v == null) delete r.pk[id]; else r.pk[id] = v; } });\n"
     "    Object.keys(r.x || {}).forEach(id => { const q = hqItem(id); if (q && q.pmv) r.x[id] = (r.x[id] || []).map(v => mv(q, v)).filter(v => v != null); });\n"
     "    r.ov = tgt; ch = 1;\n"
     "  }\n"
     "  return ch;\n"
     "}\n"
     "function hqTmaiMig(){\n"
     "  const tgt = HQ.ov || 2; if (!S.tmai || (S.tmov || 2) >= tgt) return;\n"
     "  Object.keys(S.tmai).forEach(id => { const q = hqItem(id); if (q && (q.pmv || []).some(([v]) => v > (S.tmov || 2))) delete S.tmai[id]; });\n"
     "  S.tmov = tgt; save();\n"
     "}\n"
     "function hqRuns(){\n")
must("  return S.hqRuns || (S.hqRuns = []);\n}",
     "  const R = S.hqRuns || (S.hqRuns = []);\n  if (R.reduce((n, r) => n + hqMig(r), 0)) save();\n  hqTmaiMig();\n  return R;\n}")
must("  if (!r.ov) { Object.keys(r.pk || {}).forEach(id => { const q = hqItem(id); if (q && q.pm) r.pk[id] = q.pm[r.pk[id]]; }); Object.keys(r.x || {}).forEach(id => { const q = hqItem(id); if (q && q.pm) r.x[id] = r.x[id].map(v => q.pm[v]); }); r.ov = 2; }\n",
     "  hqMig(r);\n")
must("done: sc.done, right: sc.right, pct: sc.pct, ts: Date.now(), ov: 2};",
     "done: sc.done, right: sc.right, pct: sc.pct, ts: Date.now(), ov: HQ.ov || 2};")
must("Object.assign(window.__mev, {tmBt, tmHtml, msMerge, hqItem, hqAll, check: mevCheck,",
     "Object.assign(window.__mev, {tmBt, tmHtml, msMerge, hqItem, hqAll, hqRuns, hqRunScore, state: () => S, check: mevCheck,")
must('<span class="word">medengine-STUDY</span><small>v3.6.3</small>', '<span class="word">medengine-STUDY</span><small>v3.6.4</small>')
F.write_text(s, encoding='utf-8')
print('v364 engine ok')
