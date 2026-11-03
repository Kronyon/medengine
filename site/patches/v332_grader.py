#!/usr/bin/env python3
"""v3.3.2: 📋 Grade stops handing out marks for words that appear anywhere.

Found with a real transcript (abdominal examination, mannequin, case B): every domain scored 4/4
(28/28) while the safety checks correctly found no consent, no chaperone and no comment on the
board-like rigidity. Cause: the general matcher needed any 2 words from a bullet, anywhere in the
whole transcript, and bullets with long model lines offered 20+ words, including "abdomen",
"look", "feel" and "listen". "This involves having a look, feel and listen to your abdomen" was
quoted as proof for 9 different bullets.

Now:
  - only discriminating words count: words shared by a quarter or more of the station's
    bullets (and everyday clinical words) are dropped
  - the words must turn up together, within about 25 words of speech
  - longer bullets need 3 of their words, not 2
  - a light stem ("percuss" = "percussion", "rigid" = "rigidity")
  - more voice slips fixed: "date to Beth", "purchase/podcast for" (percuss), "pop it/puppet"
    (palpate), "light partitions", "iliac fossil", "pygastric", "sifting bonus" and "shifting down"
    (shifting dullness), "rossing", "bow the kidneys", "use une's" (U&Es)
  - mannequin stations: the AI plays the examiner only, not a talking patient
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'osce.html'
t = F.read_text(encoding='utf-8')


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


if 'function anchorSet(' in t:
    raise SystemExit('already applied')

a = t.index('  // 3. General Keyword Anchor Matcher')
b = t.index('\n}\n', a)
NEW = r"""  // 3. General matcher (v3.3.2): discriminating words only, and they must turn up together
  const anchors = anchorSet(it, st);
  if (!anchors.length) {
    const fallbackRx = /\b(examine|inspect|palpat|auscultat|assess|ask|explain)\b/i;
    const ok = fallbackRx.test(norm);
    return {score: ok ? 0.5 : 0, quote: ok ? findTranscriptQuote(parsed, fallbackRx) : '', say: sayHint};
  }
  const req = anchors.length >= 8 ? 3 : anchors.length >= 3 ? 2 : 1;
  const rxs = anchors.map(w => new RegExp('\\b' + w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'i'));
  let best = {n: 0, w: ''};
  proxWindows(parsed).forEach(w => { const n = rxs.filter(rx => rx.test(w)).length; if (n > best.n) best = {n, w}; });
  if (best.n >= req) return {score: 1, quote: best.w.split(' ').slice(0, 14).join(' '), say: sayHint};
  if (best.n && best.n === req - 1) return {score: 0.5, quote: best.w.split(' ').slice(0, 14).join(' '), say: sayHint};
  return {score: 0, quote: '', say: sayHint};"""
t = t[:a] + NEW + t[b:]

HELPERS = r"""
/* v3.3.2: which words in a bullet actually discriminate it, and where they turn up together */
const ANCHOR_COMMON = new Set(['abdomen','abdominal','tummy','patient','examination','examine','examining','going','just','okay','would','like','also','then','here','there','about','some','more','them','they','their','what','when','have','been','want','need','make','sure','thank','thanks','please','today','right','left','side','sides','your','yours','with','from','into','that','this','these','those','will','well','very','much','look','looking','feel','feeling','listen','listening','pain','painful','sore','tell','know','normal','signs','sign','check','checking','station','doctor','student','examiner']);
const anchorDF = {};
function anchorSet(it, st){
  const key = st && st.id;
  if (key && !anchorDF[key]) {
    const df = {}, secs = buildChecklist(st, (cur && cur.st === st && cur.vk) || null) || [];
    let n = 0;
    secs.forEach(sc => sc.items.forEach(x => { n++; new Set(extractAnchorTokens(String(x.t || '') + ' ' + (x.say || '')).map(anchorStem)).forEach(w => { df[w] = (df[w] || 0) + 1; }); }));
    anchorDF[key] = {df, n};
  }
  const D = key ? anchorDF[key] : {df: {}, n: 0}, cap = Math.max(3, Math.ceil(D.n * 0.25));
  const out = [];
  extractAnchorTokens(String(it.t || '').replace(/<[^>]+>/g, ' ') + ' ' + (it.say || '')).forEach(w => {
    if (ANCHOR_COMMON.has(w) || /^\d+$/.test(w)) return;
    const s = anchorStem(w);
    if ((D.df[s] || 0) >= cap) return;
    if (!out.includes(s)) out.push(s);
  });
  return out.slice(0, 14);
}
function anchorStem(w){ const s = w.replace(/(ations?|ings?|ness|ities|ity|ies|ions?|es|ed|al|s)$/, ''); return (s.length >= 4 ? s : w).slice(0, 6); }
function proxWindows(parsed){
  if (parsed._prox) return parsed._prox;
  const words = String(parsed.norm || '').split(/\s+/).filter(Boolean), out = [];
  for (let i = 0; i < words.length; i += 8) { out.push(words.slice(i, i + 25).join(' ')); if (i + 25 >= words.length) break; }
  if (!out.length) out.push('');
  return parsed._prox = out;
}
"""
anchor = 'function scoreSubBullet(it, domH, st, parsed){'
t = one(t, anchor, HELPERS.lstrip('\n') + anchor)

# more voice slips, through the same scoped map
SLIPS = r"""
  TALKTYPE_MAP.push(
    [/\bdate (?:to|of|a|for|the) (?:beth|bath|berth|birds?)\b/gi, 'date of birth', 'date to Beth -> date of birth'],
    [/\b(?:purchase|podcast|because|per cuss|pecas) for\b/gi, 'percuss for', 'purchase for -> percuss for', exam],
    [/\b(?:pop it|puppet|pop pate|pal pate|palpitate)\b/gi, 'palpate', 'puppet -> palpate', exam],
    [/\blight (?:partitions|palpitations|petitions|patients)\b/gi, 'light palpation', 'light partitions -> light palpation', exam],
    [/\biliac fossils?\b/gi, 'iliac fossa', 'iliac fossil -> iliac fossa'],
    [/\b(?:a pygastric|pygastric|epic gastric|epi gastric)\b/gi, 'epigastric', 'pygastric -> epigastric'],
    [/\b(?:shifting down(?:ness)?|sifting (?:bonus|dullness|dull|down)|shifting bonus|shifting doneness|shifting dullest)\b/gi, 'shifting dullness', 'sifting bonus -> shifting dullness', exam],
    [/\b(?:rossing|rosting|row sing|rossings)\b/gi, 'rovsing', 'rossing -> rovsing', exam],
    [/\b(?:bow|bowl|ballad|ballet) the kidneys\b/gi, 'ballot the kidneys', 'bow the kidneys -> ballot the kidneys', exam],
    [/\b(?:use une'?s|you and ease?|u and e'?s|you and ees)\b/gi, 'u&es', "use une's -> U&Es"]
  );
"""
t = one(t, "function ttMapFor(st){ return TALKTYPE_MAP.filter(e => !e[3] || (st && e[3](st))); }",
        "(function moreSlips(){\n  const exam = st => typeOf(st) === 'ex' || typeOf(st) === 'proc';" + SLIPS + "})();\nfunction ttMapFor(st){ return TALKTYPE_MAP.filter(e => !e[3] || (st && e[3](st))); }")

# mannequin stations: no talking patient
t = one(t, "  return 'You are role-playing in a UK medical school OSCE (University of Nottingham, Foundations for Practice CPSA, fourth-year medical student). You play the SIMULATED PATIENT",
        "  if (/mannequin/i.test(st.info || '')) secret += '\\nMANNEQUIN STATION: there is no talking patient. Never speak as the patient and never invent a name, age or reply for her. Speak only as the examiner: start every reply with [Examiner], give each finding briefly only when the candidate says that step, and otherwise stay silent or say \"Carry on.\"\\n';\n"
        "  return 'You are role-playing in a UK medical school OSCE (University of Nottingham, Foundations for Practice CPSA, fourth-year medical student). You play the SIMULATED PATIENT")

F.write_text(t, encoding='utf-8')
print('v3.3.2 grader patch applied')
