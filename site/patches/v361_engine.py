#!/usr/bin/env python3
"""v3.6.1: one more pack hook in the STUDY engine (applied once). EXT.tmExtra(it) adds a pack's own panel under the
4-box explanation (STEP1 uses it for the UWorld ID, Anki cards from the question and the AI rebuild and twin buttons).
Nothing changes for STUDY, which sets no EXT.tmExtra."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
assert 'EXT.tmExtra' not in s, 'already applied'
a = "'</div>' : '') + '<div class=\"tm-score\" data-tmscore></div></div>';"
assert s.count(a) == 1
s = s.replace(a, "'</div>' : '') + (EXT.tmExtra ? EXT.tmExtra(it) : '') + '<div class=\"tm-score\" data-tmscore></div></div>';")
F.write_text(s, encoding='utf-8')
print('v3.6.1 tmExtra hook applied')
