#!/usr/bin/env python3
"""v3.3.0 small fixes (applied once; kept as a record).

  - AI defaults back to the current models (v3.2.0 pinned the 4.5 models and silently
    downgraded anyone who had chosen 5.5)
  - STUDY: #hq-u<n> opens that condition's hammer SBAs (the bridge from OSCE 📋 Grade)
  - STUDY: "Sketchy" is a trademark; the visible labels now say "Scenes"
  - launcher: education-only line
"""
import pathlib

SITE = pathlib.Path(__file__).resolve().parents[1]


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


def models(t):
    t = one(t, "var DEFAULT_MODELS = { quick: 'claude-haiku-4-5', smart: 'claude-sonnet-4-5' };",
            "var DEFAULT_MODELS = { quick: 'claude-haiku-5-5', smart: 'claude-sonnet-5-5' };")
    t = one(t, "    if (q === 'claude-haiku-5-5') q = DEFAULT_MODELS.quick;\n", '')
    t = one(t, "    if (s === 'claude-sonnet-5-5') s = DEFAULT_MODELS.smart;\n", '')
    return t


# OSCE
p = SITE / 'osce.html'
t = models(p.read_text(encoding='utf-8'))
p.write_text(t, encoding='utf-8')

# STUDY
p = SITE / 'study.html'
t = models(p.read_text(encoding='utf-8'))
t = one(t, "  const h = (location.hash || '').slice(1);\n  const m = h.match(/^u(\\d+)-(read|fill|mcq|recall|think)$/);",
        "  const h = (location.hash || '').slice(1);\n  const mq = h.match(/^hq-u(\\d+)$/); if (mq && UNITS[+mq[1]]) return {view: 'hqu', u: +mq[1]};\n  const m = h.match(/^u(\\d+)-(read|fill|mcq|recall|think)$/);")
t = one(t, "function go(r, push = true){\n  route = r;",
        "function go(r, push = true){\n"
        "  if (r.view === 'hqu') {\n"
        "    /* from OSCE 📋 Grade: straight into this condition's hammer SBAs */\n"
        "    const k = String(HQ.al && HQ.al[r.u] != null ? HQ.al[r.u] : r.u);\n"
        "    if (!HQ.q.some(q => q.t === 'u' && q.k === k)) r = {view: 'unit', u: r.u, mode: 'read'};\n"
        "    else { route = {view: 'hammer'}; try { history.replaceState(null, '', '#hammer'); } catch(e) {} renderSide(); hqCfg.tgt = 'u:' + k; hqSess = null; return hqStart(0); }\n"
        "  }\n"
        "  route = r;")
for a, b in [('🎬 Sketchy', '🎬 Scenes'), ('Sketchy scenes', 'Visual scenes'),
             ('Sketchy visual mnemonic scene for ', 'Visual mnemonic scene for '),
             ('4-Layer Sketchy Mnemonic Stage', '4-layer visual mnemonic scene'),
             ('24 recurring Sketchy props', '24 recurring scene props'),
             ('Preview Sketchy stage right here', 'Preview the scene right here'),
             ('Custom Sketchy mnemonic hook', 'Your own scene hook'),
             ('Pinned custom Sketchy hook!', 'Pinned your own scene hook!')]:
    if a not in t:
        print('note: not found', a)
    t = t.replace(a, b)
p.write_text(t, encoding='utf-8')

# launcher
p = SITE / 'index.html'
t = p.read_text(encoding='utf-8')
t = one(t, '  </div>\n</main>', '  </div>\n  <p class="edu">For education only, not medical advice. Check anything you act on against current UK guidance.</p>\n</main>')
t = one(t, '</style>', '.edu{margin:18px 2px 0;font-size:.8rem;color:var(--muted, #6b6b6b);text-align:center}\n</style>')
p.write_text(t, encoding='utf-8')
print('small fixes applied')
