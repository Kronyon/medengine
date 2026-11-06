#!/usr/bin/env python3
"""v3.6.13 engine: from v3.6.12 (Antigravity) - a wrong option that has a "right instead if" flip counts as explained,
so the "Not explained yet" AI button only shows when an option has neither a why-not line nor a flip."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
OLD = "    if (!xs[i] && !ai[i]) miss++;\n"
NEW = "    if (!xs[i] && !ai[i] && !(fs[i] && fs[i].length)) miss++;\n"
assert s.count(OLD) == 1, 'tmWhyNot line not found'
F.write_text(s.replace(OLD, NEW), encoding='utf-8'); print('v3613 engine ok')
