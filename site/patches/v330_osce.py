#!/usr/bin/env python3
"""v3.3.0 OSCE patch for site/osce.html (applied once; kept as a record).

  - 🧬 Mnemonics: every frame, examination and procedure (site/data/mnemonics.json), each with
    why it works and when a mnemonic would hurt; a card on every station, a hub, a letter quiz,
    and your own mnemonics per station
  - 🔒 My circuit: import a private pack, seal it with your password (AES-GCM, PBKDF2 600k),
    unlock to practise; nothing exam-specific ships in this file
  - 📋 Grade: 🛡️ safety and order checks (negation-aware, critical steps cap at 54%),
    station-scoped voice fixes, "✨ Fix words in the box", and a bridge to STUDY's SBAs
  - honest offline examiner (no invented non-negotiables or timeline)
"""
import json, pathlib

HERE = pathlib.Path(__file__).resolve().parent
F = HERE.parent / 'osce.html'
t = F.read_text(encoding='utf-8')
BLOCK = (HERE / 'v330_osce_block.js').read_text(encoding='utf-8')
MN = json.loads((HERE.parent / 'data' / 'mnemonics.json').read_text(encoding='utf-8'))


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


if 'const MN = ' in t:
    raise SystemExit('already applied')

# 1. mnemonic data straight after the station data
i = t.index('const D = ')
j = t.index('\n', i)
mn_js = json.dumps(MN, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
t = t[:j + 1] + 'const MN = ' + mn_js + ';\n' + t[j + 1:]

# 2. the v3.3.0 block, once every view and helper it needs exists
views = "const VIEWS = ['home', 'sniper', 'stations', 'fw', 'hooks', 'exams', 'dops', 'ilos', 'skills', 'visual', 'ffp', 'rf', 'posters', 'triggers'];\n"
t = one(t, views, views + BLOCK + '\n')

# 3. voice fixes know which station they are in
a = t.index('function normalizeTalkType(rawText){')
b = t.index('return {raw, norm, clauses, windows, rescued};', a)
body = t[a:b].replace('function normalizeTalkType(rawText){', 'function normalizeTalkType(rawText, st){\n  const MAP = ttMapFor(st);', 1)
if body.count('TALKTYPE_MAP.forEach(') != 3:
    raise SystemExit('normalizeTalkType shape changed')
t = t[:a] + body.replace('TALKTYPE_MAP.forEach(', 'MAP.forEach(') + t[b:]

# 4. grade: safety and order checks, the cap, and what to change first
t = one(t, '  const parsed = normalizeTalkType(rawText);', '  const parsed = normalizeTalkType(rawText, st);')
t = one(t, '  // Sync official 0-4 domain scores into 👥 Friends -> 📋 Examiner sheet',
        '  // v3.3.0: safety and order checks; a missed safety step caps the station at 54%\n'
        '  const chk = chkRun(st, parsed.norm, prevResult), chkCrit = chk.filter(x => !x.ok && x.c), capPct = chkCrit.length ? 54 : 100;\n\n'
        '  // Sync official 0-4 domain scores into 👥 Friends -> 📋 Examiner sheet')
t = one(t, '    const pctTmp = maxPts > 0 ? Math.round((earnedPts / maxPts) * 100) : 0;',
        '    const pctTmp = Math.min(capPct, maxPts > 0 ? Math.round((earnedPts / maxPts) * 100) : 0);')
t = one(t, '  const pct = maxPts > 0 ? Math.round((earnedPts / maxPts) * 100) : 0;',
        '  const rawPct = maxPts > 0 ? Math.round((earnedPts / maxPts) * 100) : 0, pct = Math.min(capPct, rawPct);')
t = one(t, '  const changeText = worstDom && worstDom.score < 4\n',
        "  const changeText = chkCrit.length ? '🚨 Safety: ' + chkCrit[0].t + (chkCrit[0].why ? '. ' + chkCrit[0].why : '') : worstDom && worstDom.score < 4\n")
t = one(t, '    retryBaseHits: hits.map(h => h.id),\n    quoteById\n  };',
        '    retryBaseHits: hits.map(h => h.id),\n    quoteById,\n    chk,\n    chkOk: chk.filter(x => x.ok).map(x => x.t),\n    rawPct\n  };')

# 5. grade drawer: the checks panel, the fix button, the STUDY bridge
t = one(t, "    h += '<div class=\"change\"><b>🔧 One Thing to Change</b><div>' + esc(r.changeText) + '</div></div>';\n    h += '</div>';\n",
        "    h += '<div class=\"change\"><b>🔧 One Thing to Change</b><div>' + esc(r.changeText) + '</div></div>';\n    h += '</div>';\n    h += chkHtml(r);\n")
dict_btn = "  h += '<button type=\"button\" class=\"btn sm tt-dict' + (ttDictState.on ? ' on' : '') + '\" data-ttdictate>' + (ttDictState.on ? '⏹ Stop Mic (' + mmss(ttDictState.sec) + ')' : '🎙️ Dictate') + '</button>';\n"
t = one(t, dict_btn, dict_btn + "  if (r && r.rescued && r.rescued.length) h += '<button type=\"button\" class=\"btn sm\" data-ttfix title=\"Swap misheard words in the box for the right ones\">✨ Fix words in the box</button>';\n")
t = one(t, "  h += '</div></details>';\n  return h;\n}\n\nfunction redrawSniperStationWrap(){",
        "  if (r) h += ttBridgeHtml(st);\n  h += '</div></details>';\n  return h;\n}\n\nfunction redrawSniperStationWrap(){")

# 6. station page: the mnemonic card
t = one(t, '<div id="dgWrap"></div><div id="hookWrap"></div>', '<div id="dgWrap"></div><div id="mnWrap"></div><div id="hookWrap"></div>')
hook_line = "  $('#hookWrap').innerHTML = skelCardHtml(st) + rfCardHtml(st) + nextCardHtml(st) + hookHtml(Object.assign(hooksFor(st, cur.vk), cur.hidden ? {money: '', all: []} : {}), cur.mode === 'script');\n"
t = one(t, hook_line, hook_line + "  const mnw = $('#mnWrap'); if (mnw) mnw.innerHTML = mnCardHtml(st);\n")
t = one(t, "  $('#hookWrap').hidden = cand || md === 'poster';\n",
        "  $('#hookWrap').hidden = cand || md === 'poster';\n  const mnw = $('#mnWrap'); if (mnw) mnw.hidden = cand || ((md === 'ai' || md === 'voice') && !cur.fb);\n")

# 7. routes, nav highlight and nav buttons
t = one(t, "sniper: vSniper}[route.v] || vHome)(m);", "sniper: vSniper, mn: vMn, my: vMy}[route.v] || vHome)(m);")
t = one(t, "route.v === 'sniper' ? 'sniper' : '';", "route.v === 'sniper' ? 'sniper' : route.v === 'mn' || route.v === 'my' ? route.v : '';")
t = one(t, "st0 ? 'ty:' + typeOf(st0) :", "st0 ? (st0.my ? 'my' : 'ty:' + typeOf(st0)) :")
t = one(t, '    <button data-v="posters">🗺️ Posters</button>\n', '    <button data-v="posters">🗺️ Posters</button>\n    <button data-v="mn">🧬 Mnemonics</button>\n')
t = one(t, '    <button data-ty="psych">🧠 Psych</button>\n', '    <button data-ty="psych">🧠 Psych</button>\n    <button data-v="my">🔒 My circuit</button>\n')

# 8. offline examiner: only report what was actually measured
t = one(t, "const parsedTurns = normalizeTalkType(meTurns || 'Hello my name is Nana');", "const parsedTurns = normalizeTalkType(meTurns || 'Hello my name is Nana', st);")
t = one(t, "non_negotiables: UNI.map((n, idx) => ({ i: idx, done: idx < 3, note: idx < 3 ? 'Completed in station' : 'Ensure explicit check before 8:00' })),", 'non_negotiables: [],')
t = one(t, "timeline: (cur && cur.chat ? cur.chat.filter(x => x.role === 'user').slice(0, 6) : []).map(x => ({ t: mmss(x.t || 0), event: cutT(x.content, 70), good: true })),", 'timeline: [],')
t = one(t, 'reasoning_sentence: { said: gRes.pct >= 65,', 'reasoning_sentence: { said: /\\b(because|which (suggests|points|fits)|most likely|in keeping with|consistent with)\\b/i.test(meTurns),')
t = one(t, "safety: slips.length ? slips[0].fix : '',", "safety: (gRes.chk || []).filter(x => !x.ok && x.c).map(x => x.t + (x.why ? ': ' + x.why : '')).join(' · ') || (slips.length ? slips[0].fix : ''),")
t = one(t, "const normObj = typeof normalizeTalkType === 'function' ? normalizeTalkType(raw) : { norm: raw.toLowerCase() };",
        "const normObj = typeof normalizeTalkType === 'function' ? normalizeTalkType(raw, st) : { norm: raw.toLowerCase() };")

# 9. voice: say how long it waits, and keep the hint in step with the setting
t = one(t, 'The patient answers out loud. Start a sentence with', "The patient answers out loud, <span id=\"vWaitHint\">' + vWaitHint() + '</span>. Start a sentence with")
t = one(t, "if (t.id === 'vPauseSel') { S.set.vWait = t.value; save(); return vArm(); }",
        "if (t.id === 'vPauseSel') { S.set.vWait = t.value; save(); const wh = $('#vWaitHint'); if (wh) wh.innerHTML = vWaitHint(); return vArm(); }")

# 10. home eyebrow showed a stale version
t = one(t, "APP_NAME + ' v2.0 · FFP CPSA", "APP_NAME + ' v' + APP_VERSION + ' · FFP CPSA")

# 11. styles
CSS = """
/* v3.3.0: mnemonics, my circuit, safety checks */
.mn-card{border-left-color:var(--accent)}
.mn-tools{gap:6px;flex-wrap:wrap;align-items:center}
.mn-item{border:1px solid var(--line);border-radius:10px;padding:9px 11px;background:var(--surface);display:flex;flex-direction:column;gap:6px;min-width:0}
.mn-none{border-style:dashed;background:var(--surface-2)}
.mn-hd{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px;min-width:0}
.mn-k{font-family:var(--f-mono);font-size:.68rem;font-weight:700;color:var(--muted);border:1px solid var(--line);border-radius:5px;padding:1px 6px;white-space:nowrap}
.mn-code{font-family:var(--f-display);font-size:1.05rem;color:var(--accent-ink);overflow-wrap:anywhere}
.mn-t{color:var(--muted);font-size:.85rem}
.mn-tag{font-size:.68rem;font-weight:700;border-radius:5px;padding:1px 6px;background:var(--good-soft);color:var(--ink);border:1px solid var(--good)}
.mn-letters{display:flex;flex-direction:column;gap:4px}
.mn-l{display:grid;grid-template-columns:minmax(40px,auto) minmax(0,1fr);gap:8px;align-items:baseline;text-align:left;border:1px solid var(--line);border-radius:8px;background:var(--surface-2);padding:5px 9px;font:inherit;color:var(--ink);cursor:pointer;width:100%}
.mn-l b{font-family:var(--f-display);color:var(--accent-ink);font-size:1rem;overflow-wrap:anywhere}
.mn-l.hid span{color:var(--muted);font-style:italic}
.mn-l:focus-visible{outline:2px solid var(--focus);outline-offset:2px}
.mn-lineq{display:block}
.mn-line{background:var(--accent-soft);border-left:4px solid var(--accent);border-radius:8px;padding:7px 10px;line-height:1.45}
.mn-why summary{cursor:pointer;font-weight:700;font-size:.85rem;color:var(--muted)}
.mn-why div{margin-top:4px;line-height:1.45;font-size:.9rem}
.mn-pr{line-height:1.45;margin:2px 0}
.mn-form{display:flex;flex-direction:column;gap:6px;border:1px dashed var(--line);border-radius:10px;padding:9px}
.mn-form input,.mn-form textarea,.my-form input{font:inherit;color:var(--ink);background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:8px 10px;width:100%;box-sizing:border-box}
.my-form{display:flex;flex-direction:column;gap:8px;margin-top:10px;max-width:420px}
.tt-sec.chk{border-left:4px solid var(--good)}
/* v3.3.0: phone-width fixes for v3.2.0 cards (mode bar, body map, doorway HUD) */
html .seg{max-width:100%;min-width:0;overflow-x:auto;scrollbar-width:none}html .seg::-webkit-scrollbar{display:none}html .seg button{white-space:nowrap;flex:0 0 auto}
html .bmap-list,html .bmap-row,html .bmap-hd,html .bmap-bd{min-width:0}html .bmap-hd>*{min-width:0;overflow-wrap:anywhere}html .bmap-hd .code{white-space:normal}
@media (max-width:560px){html .bmap-wrap{grid-template-columns:minmax(0,1fr)}html .sh-row{grid-template-columns:minmax(0,1fr)}}
html .sh-row>*{min-width:0;overflow-wrap:anywhere}html .sh-row .code{white-space:normal}
"""
t = one(t, '.vwait{margin:6px 0 2px}', CSS.strip() + '\n.vwait{margin:6px 0 2px}')

F.write_text(t, encoding='utf-8')
print('OSCE v3.3.0 patch applied')
