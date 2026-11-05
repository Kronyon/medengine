#!/usr/bin/env python3
"""v3.6.3 engine fixes in site/study.html (also flows into STEP1 through build.py). Applied once.

Checked against the outside audit; each item here was confirmed in the code first:
  1. The AI system prompt still said "medengine-OSCE"; it now names STUDY or STEP1 from the page title.
  2. Pasted images were sent only to Anthropic keys; Gemini, OpenAI and Groq dropped them. They now go to all four,
     and Groq tries its vision models first when there is an image.
  3. The 📲 device sync button was hidden on phones; it now stays.
  4. Review screen: every wrong option gets one card holding its "why not" line and its 🔀 flip, so flips are no
     longer printed twice. Options with nothing written get a ✨ button that asks your own AI and keeps the answer
     in your progress (synced like the rest). Triggers, Pathoma, poster and comments fold into one 📚 Deep dive
     that remembers if you leave it open.
"""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
assert 'tmWhyNot' not in s, 'already applied'


def must(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:90])
    s = s.replace(a, b)


# 1. system prompt and key message
must("  var SYSTEM = 'You are the engine behind medengine-OSCE, a UK OSCE practice app for medical students. Follow the instructions in the user turn exactly.';",
     "  var SYSTEM = /STEP1/.test(document.title || '')\n"
     "    ? 'You are the engine behind medengine-STEP1, a USMLE Step 1 question bank and tutor for a UK medical student. Follow the instructions in the user turn exactly.'\n"
     "    : 'You are the engine behind medengine-STUDY, a UK finals single best answer question bank and clinical reasoning tutor (UKMLA, MS AKT, Nottingham FFP). Use UK practice, NICE guidance, UK drug names and SI units. Follow the instructions in the user turn exactly.';")
must("'Add your key to use the AI patient and examiner.'", "'Add your AI key to use the AI features.'")

# 2. images for every provider
must("    var prov = detectProvider(key);\n    if (prov && prov.id === 'gemini') {",
     "    var prov = detectProvider(key);\n"
     "    // images (a question's ECG, X-ray or screenshot) are read once and sent in each provider's own format\n"
     "    var imgs = !opts.images ? [] : (typeof Blob !== 'undefined' && opts.images instanceof Blob) ? [opts.images] : Array.prototype.slice.call(opts.images);\n"
     "    if (imgs.length > 5) throw { code: 'image_rejected', message: 'Too many images' };\n"
     "    var img64 = [];\n"
     "    for (var ii = 0; ii < imgs.length; ii++) {\n"
     "      if (IMG_TYPES.indexOf(imgs[ii].type) < 0 || imgs[ii].size > IMG_MAX) throw { code: 'image_rejected', message: 'Use a JPEG, PNG, GIF or WebP image under 5 MB' };\n"
     "      img64.push({ type: imgs[ii].type, data: await b64(imgs[ii]) });\n"
     "    }\n"
     "    if (prov && prov.id === 'gemini') {")
must("""      var gemContents = messages.map(function (m) {
        return {
          role: m.role === 'assistant' ? 'model' : 'user',
          parts: [{ text: typeof m.content === 'string' ? m.content : JSON.stringify(m.content) }]
        };
      });""",
     """      var gemContents = messages.map(function (m, mi) {
        var parts = [{ text: typeof m.content === 'string' ? m.content : JSON.stringify(m.content) }];
        if (mi === messages.length - 1 && img64.length) parts = img64.map(function (g) { return { inlineData: { mimeType: g.type, data: g.data } }; }).concat(parts);
        return { role: m.role === 'assistant' ? 'model' : 'user', parts: parts };
      });""")
must("      var candidateModels = isGroq ? await discoverGroqModels(key, opts.signal) : ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo'];",
     "      var candidateModels = isGroq ? await discoverGroqModels(key, opts.signal) : ['gpt-4o-mini', 'gpt-4o', 'gpt-3.5-turbo'];\n"
     "      if (img64.length) candidateModels = candidateModels.filter(function (m) { return /vision|llama-4|scout|maverick|gpt-4o/i.test(m); }).concat(candidateModels.filter(function (m) { return !/vision|llama-4|scout|maverick|gpt-4o/i.test(m); }));")
s_old = "      var oaiMsgs = [{ role: 'system', content: SYSTEM + (opts._json ? ' Reply with ONLY one valid JSON value, no prose and no code fences.' : '') }].concat(messages.map(function (m) { return { role: m.role, content: typ"
i = s.index(s_old)
j = s.index('\n', i)
line = s[i:j]
must(line, line + "\n      if (img64.length) { var oLast = oaiMsgs[oaiMsgs.length - 1]; oLast.content = [{ type: 'text', text: String(oLast.content) }].concat(img64.map(function (g) { return { type: 'image_url', image_url: { url: 'data:' + g.type + ';base64,' + g.data } }; })); }")
must("""    var imgs = !opts.images ? [] : (typeof Blob !== 'undefined' && opts.images instanceof Blob) ? [opts.images] : Array.prototype.slice.call(opts.images);
    if (imgs.length) {
      if (imgs.length > 5) throw { code: 'image_rejected', message: 'Too many images' };
      var blocks = [];
      for (var ii = 0; ii < imgs.length; ii++) {
        var im = imgs[ii];
        if (IMG_TYPES.indexOf(im.type) < 0 || im.size > IMG_MAX) throw { code: 'image_rejected', message: 'Use a JPEG, PNG, GIF or WebP image under 5 MB' };
        blocks.push({ type: 'image', source: { type: 'base64', media_type: im.type, data: await b64(im) } });
      }""",
     """    if (img64.length) {
      var blocks = img64.map(function (g) { return { type: 'image', source: { type: 'base64', media_type: g.type, data: g.data } }; });""")

# 3. keep device sync on phones
must(".stats .pill.days,.brand small,.search-wrap .kbd,#aiKeyBtn,#devBtn,#helpBtn,#bountyBtn{display:none!important}",
     ".stats .pill.days,.brand small,.search-wrap .kbd,#aiKeyBtn,#helpBtn,#bountyBtn{display:none!important}")

# 4a. one card per wrong option: why-not + flips, with an AI fill for the gaps
i = s.index("  let fl = '';\n  if (tm.f && tm.f.length) {")
j = s.index("  return '<div class=\"tm\" role=\"group\"", i)
s = s[:i] + s[j:]
must("+ '</div>' + fl + ((tm.x || []).length ? '<div class=\"tm-x\"><span class=\"tm-fk\">❌ Why not the others</span>' + tm.x.map(([i, s]) => '<div class=\"tm-xr\"><b>' + L[i] + '. ' + esc(it.o[i]) + '</b><span>' + esc(s) + '</span></div>').join('') + '</div>' : '') + (EXT.tmExtra",
     "+ '</div>' + tmWhyNot(it) + (EXT.tmExtra")
must("function tmRe(c){",
     r"""const TM_LAZY = /instead specifically indicated|clinical findings instead/i;
function tmWhyNot(it){
  const tm = it.tm || {}, L = 'ABCDE', ai = (S.tmai || {})[it.id] || {}, xs = {}, fs = {};
  (tm.x || []).forEach(([i, t]) => { if (t && !TM_LAZY.test(t)) xs[i] = t; });
  (tm.f || []).forEach(([c, i]) => { const t = String(c || '').trim(); if (t && !/^[✗❌]/.test(t) && i !== it.a) (fs[i] = fs[i] || []).push(t); });
  let miss = 0; const empty = [];
  const rows = it.o.map((o, i) => {
    if (i === it.a) return '';
    const parts = [];
    if (xs[i]) parts.push('<span>' + esc(xs[i]) + '</span>');
    else if (ai[i]) parts.push('<span>' + esc(ai[i]) + ' <span class="tm-aitag" title="Written by your AI">✨ AI</span></span>');
    (fs[i] || []).forEach(t => parts.push('<span class="tm-xf">🔀 Right instead if ' + esc(t.replace(/^if\s+/i, '')) + '</span>'));
    if (!xs[i] && !ai[i]) miss++;
    if (!parts.length) { empty.push(L[i]); return ''; }
    return '<div class="tm-xr"><b>' + L[i] + '. ' + esc(o) + '</b>' + parts.join('') + '</div>';
  }).join('');
  const head = it.f && (!(tm.f || []).length || !hqFlipDup(it)) ? '<div class="tm-fhead">🔄 <b>Flip it:</b> ' + esc(it.f) + '</div>' : '';
  const btn = miss ? '<div class="tm-xe">' + (empty.length ? '<span class="hint">Not explained yet: ' + empty.join(', ') + '</span> ' : '') + '<button class="btn ghost sm tm-aib" data-tmai="' + esc(it.id) + '">✨ Write the ' + miss + ' missing why-not' + (miss > 1 ? 's' : '') + ' with my AI</button></div>' : '';
  return '<div class="tm-x"><span class="tm-fk">❌ Why not the others · 🔀 what would make each one right</span>' + head + rows + btn + '</div>';
}
async function tmAiFill(id, b){
  const it = hqItem(id); if (!it) return;
  const sample = window.claude && window.claude.use ? await window.claude.use('sample') : null;
  if (!sample) { if (window.medengineAccount) window.medengineAccount.open(); else toast('Add your AI key first'); return; }
  const tm = it.tm || {}, L = 'ABCDE', have = {};
  (tm.x || []).forEach(([i, t]) => { if (t && !TM_LAZY.test(t)) have[i] = 1; });
  S.tmai = S.tmai || {}; const mine = S.tmai[id] || {};
  const need = it.o.map((o, i) => i).filter(i => i !== it.a && !have[i] && !mine[i]);
  if (!need.length) return;
  const us = /STEP1/.test(document.title || '');
  b.disabled = true; b.textContent = '✨ Writing…';
  const lab = (it.lab || []).map(r => r.filter(Boolean).join(' ')).join('; ');
  const prompt = 'You write the "why not" line for each wrong option in a ' + (us ? 'USMLE Step 1 question' : 'UK finals single best answer question (UKMLA and MS AKT style: NICE guidance, UK drug names, SI units)') + '.\n\n'
    + 'Stem: ' + it.s.replace(/\n/g, ' ') + (lab ? '\nResults: ' + lab : '') + '\nQuestion: ' + (it.ql || '') + '\nOptions: ' + it.o.map((o, i) => L[i] + '. ' + o).join(' | ')
    + '\nCorrect answer: ' + L[it.a] + '. ' + it.o[it.a] + (it.w ? '\nWhy it is right: ' + it.w : '') + (tm.g ? '\nDeciding clue: ' + tm.g : '')
    + '\n\nFor each wrong option ' + need.map(i => L[i]).join(', ') + ', write one sentence of 12 to 25 words. Name the specific detail in this stem that rules it out, or the feature that option would need and that is missing here, and give the real fact (its typical presentation, the test result it would give, or where it sits in the guideline). Do not say "the findings indicate" or "rather than". No brackets.'
    + '\nReply with JSON only: {"' + L[need[0]] + '": "sentence"' + (need.length > 1 ? ', ...' : '') + '} with exactly the letters ' + need.map(i => L[i]).join(', ') + '.';
  try {
    const r = await sample.json(prompt, {modelTier: 'quick', maxTokens: 900});
    let n = 0;
    need.forEach(i => { const t = r && (r[L[i]] || r[L[i].toLowerCase()]); if (typeof t === 'string' && t.trim().length > 15) { mine[i] = t.trim(); n++; } });
    if (!n) throw {message: 'The AI reply was empty'};
    S.tmai[id] = mine; save();
    toast('✨ ' + n + ' why-not line' + (n > 1 ? 's' : '') + ' saved to your progress');
  } catch (e) { toast('AI could not write them: ' + ((e && e.message) || 'try again')); }
  if (typeof hqDraw === 'function' && hqSess && !hqSess.done) hqDraw(); else { b.disabled = false; b.textContent = '✨ Try again'; }
}
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-tmai]'); if (!b) return; e.preventDefault(); e.stopPropagation(); tmAiFill(b.dataset.tmai, b); }, true);
document.addEventListener('toggle', e => { if (e.target.classList && e.target.classList.contains('hq-deep')) { S.set.hqDeepOpen = e.target.open; save(); } }, true);
function tmRe(c){""")

# 4b. review screen: no second flip box; deep-dive drawer
must("    if (it.f && !hqFlipDup(it)) h += '<div class=\"hq-flip\"><span class=\"hq-fl\">🔄 Flip it</span>' + esc(it.f).replace('→', '<b class=\"hq-arr\">→</b>') + '</div>';\n",
     "    if (it.f && !it.tm) h += '<div class=\"hq-flip\"><span class=\"hq-fl\">🔄 Flip it</span>' + esc(it.f).replace('→', '<b class=\"hq-arr\">→</b>') + '</div>';\n")
must("""    h += hqTriggers(it) + hqPathomaBox(it) + hqPosterBox(it);
    const ui = hqUnitOf(it);
    if (typeof discBoxHtml === 'function') h += discBoxHtml('q:' + it.id, hqTitle(it), ui != null ? ui : hqGuessUnit(it), it);""",
     """    const ui = hqUnitOf(it);
    const deep = hqTriggers(it) + hqPathomaBox(it) + hqPosterBox(it) + (typeof discBoxHtml === 'function' ? discBoxHtml('q:' + it.id, hqTitle(it), ui != null ? ui : hqGuessUnit(it), it) : '');
    if (deep) h += '<details class="panel hq-deep"' + (S.set.hqDeepOpen ? ' open' : '') + '><summary><b>📚 Deep dive</b> <span class="hint">triggers, Pathoma, poster, comments</span></summary>' + deep + '</details>';""")
must(".oscelink{display:inline-flex;",
     ".tm-xr .tm-xf{display:block;margin-top:3px;color:var(--muted);font-size:.92em}.tm-xr .tm-xm{display:block;color:var(--muted);font-style:italic}.tm-aitag{font-size:.75em;border:1px solid var(--line);border-radius:999px;padding:0 6px;color:var(--muted)}.tm-fhead{margin:4px 0 8px;padding:6px 10px;border:1px dashed var(--line);border-radius:10px}.tm-aib{margin-top:6px}.hq-deep>summary{cursor:pointer;padding:4px 0}\n.oscelink{display:inline-flex;")
F.write_text(s, encoding='utf-8')
print('ok')
