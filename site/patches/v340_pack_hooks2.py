#!/usr/bin/env python3
"""v3.4.0, part 2: a few more pack hooks in the STUDY engine (applied once; kept as a record). Nothing changes for STUDY.

  - a pack view survives a reload (#deconstruct, #block...)
  - window.ME also exposes the question stem renderer, saved runs and the reference-range table, so a pack can run
    its own timed block and then open the engine's review on the same answers
  - a pack with no reasoning trees opens the arrows tab of the library instead of an empty page
  - a pack without scanned pages hides the "Original pages" buttons
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
assert 'window.MEDENGINE_PACK' in s, 'apply v340_pack_hooks.py first'
assert 'hqResume: rid =>' not in s, 'already applied'


def must(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:90])
    s = s.replace(old, new)


must("'triggers','hammer','leaderboard'].includes(h)) return {view: h};",
     "'triggers','hammer','leaderboard'].includes(h) || EXT_VIEWS[h]) return {view: h};")
must("route.id === 'cases' ? 'cases' : 'trees';", "route.id === 'cases' ? 'cases' : FW.length ? 'trees' : 'arrows';")
must("  if (qq.length || os.length) h += '<div class=\"srcs\"><span class=\"hint\">Original pages:</span>'",
     "  if (!PACK.noFig && (qq.length || os.length)) h += '<div class=\"srcs\"><span class=\"hint\">Original pages:</span>'")
must("  view: (name, fn) => { EXT_VIEWS[name] = fn; },",
     "  hqStem: it => hqStem(it), hqResume: rid => hqResume(rid), hqRuns: () => hqRuns(), tmHtml: it => tmHtml(it), refRanges: HQ_REF_RANGES,\n"
     "  view: (name, fn) => { EXT_VIEWS[name] = fn; },")

F.write_text(s, encoding='utf-8')
print('v3.4.0 pack hooks part 2 applied')
