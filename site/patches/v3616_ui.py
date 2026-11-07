#!/usr/bin/env python3
"""v3.6.16: the comments box sits right above Deep dive (as on Passmedicine), not hidden inside it."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
old = """    const deep = hqTriggers(it) + hqPathophysiologyBox(it) + hqPosterBox(it) + (typeof discBoxHtml === 'function' ? discBoxHtml('q:' + it.id, hqTitle(it), ui != null ? ui : hqGuessUnit(it), it) : '');
    if (deep) h += '<details class="panel hq-deep"' + (S.set.hqDeepOpen ? ' open' : '') + '><summary><b>📚 Deep dive</b> <span class="hint">triggers, Pathophysiology, poster, comments</span></summary>' + deep + '</details>';"""
new = """    const disc = typeof discBoxHtml === 'function' ? discBoxHtml('q:' + it.id, hqTitle(it), ui != null ? ui : hqGuessUnit(it), it) : '';
    const deep = hqTriggers(it) + hqPathophysiologyBox(it) + hqPosterBox(it);
    if (disc) h += '<div class="hq-disc">' + disc + '</div>';
    if (deep) h += '<details class="panel hq-deep"' + (S.set.hqDeepOpen ? ' open' : '') + '><summary><b>📚 Deep dive</b> <span class="hint">triggers, pathophysiology, poster</span></summary>' + deep + '</details>';"""
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace(".tm-score{margin:8px 0 0;font-size:.9rem}\n", ".tm-score{margin:8px 0 0;font-size:.9rem}\n.hq-disc .disc-box{margin-top:12px}\n", 1)
F.write_text(s, encoding='utf-8'); print('v3616 ui ok')
