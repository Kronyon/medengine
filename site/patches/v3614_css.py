#!/usr/bin/env python3
"""v3.6.14: thought-map cue chips no longer overflow their column. The role tag sat beside the text in a flex row, so a
long word ("hallucinations", "postoperative") could not wrap and spilled over the arrow. The tag is now inline and the
text flows after it and wraps beneath; any single word wider than the column breaks."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
def must(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)
must(".tm-cue{display:flex;align-items:baseline;gap:5px;padding:2px 6px;border-radius:5px}",
     ".tm-cue{display:block;padding:3px 6px;border-radius:5px;line-height:1.4;overflow-wrap:anywhere;min-width:0}")
must(".tm-cue-role{font:700 .64rem var(--f-mono,monospace);text-transform:uppercase;letter-spacing:.02em;padding:1px 5px;border-radius:4px;background:rgba(0,0,0,.15);flex:none;opacity:.92}",
     ".tm-cue-role{display:inline-block;margin:0 5px 1px 0;vertical-align:1px;font:700 .64rem var(--f-mono,monospace);text-transform:uppercase;letter-spacing:.02em;padding:1px 5px;border-radius:4px;background:rgba(0,0,0,.15);opacity:.92;white-space:nowrap}")
must(".tm-n{flex:1 1 0;min-width:0;", ".tm-n{flex:1 1 0;min-width:0;overflow-wrap:anywhere;")

# phone overflow sweep (iPhone 13 width): lab ranges, poster pin cards, "don't confuse" columns
must(".hq-ref-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));",
     ".hq-ref-list{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(310px,100%),1fr));")
must(".hq-ref-vs{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0}",
     ".hq-ref-vs{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:1;min-width:0;max-width:64%}")
must("font-variant-numeric:tabular-nums;white-space:nowrap}", "font-variant-numeric:tabular-nums;white-space:normal;text-align:right;max-width:100%;overflow-wrap:anywhere}")
must(".sk-zones{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));",
     ".sk-zones{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(220px,100%),1fr));")
must(".sk-pin-card{border:1.5px solid var(--line);", ".sk-pin-card{min-width:0;overflow-wrap:anywhere;border:1.5px solid var(--line);")
must(".sk-pin-top{display:flex;align-items:center;gap:6px;", ".sk-pin-top{display:flex;flex-wrap:wrap;align-items:center;gap:4px 6px;")
must(".po-vs2{display:grid;grid-template-columns:1fr auto 1fr;", ".po-vs2{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);")

# the top bar overflowed between about 900 and 1240 px wide (the ? button was cut off): the STEP1/OSCE links go to their round badges early
must(".stats{display:flex;gap:8px;align-items:center}",
     ".stats{display:flex;gap:8px;align-items:center}\n@media (max-width:1240px){.top .oscelink{font-size:0;gap:0;padding:4px;flex:none}.top .oscelink .od{font-size:.65rem}.top{gap:8px}.stats{gap:6px}}")
must(".sk-prop-chip{display:inline-flex;align-items:center;gap:5px;", ".sk-prop-chip{display:inline-flex;align-items:center;gap:5px;max-width:100%;overflow-wrap:anywhere;")
must(".po-vs2>div{border:1px solid var(--line);", ".po-vs2>div{min-width:0;overflow-wrap:anywhere;hyphens:auto;border:1px solid var(--line);")
F.write_text(s, encoding='utf-8'); print('v3614 css ok')
