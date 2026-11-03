#!/usr/bin/env python3
"""v3.3.0: STUDY phone width. v3.2.0's poster tabs (Poster, Scenes, Props, Film…) ran 15 to 30 px past a 390 px screen."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
t = F.read_text(encoding='utf-8')
CSS = ('html .seg{max-width:100%;min-width:0;overflow-x:auto;scrollbar-width:none}html .seg::-webkit-scrollbar{display:none}'
       'html .seg button{white-space:nowrap;flex:0 0 auto}\n')
i = t.index('</style>')
if CSS in t:
    raise SystemExit('already applied')
F.write_text(t[:i] + CSS + t[i:], encoding='utf-8')
print('STUDY phone-width fix applied')
