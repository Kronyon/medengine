#!/usr/bin/env python3
"""v3.6.14 UI:
1. The why-not list goes back to the slim v3.6.2 look: one "↳" line per wrong option on a thin left rule, no boxes.
   An option with only a flip reads like the old gate line: "↳ 🔀 If … ➔ D. Anxiolytic".
2. Hover (or tap) tooltips: once a question is answered, conditions, drugs, organisms, tests, procedures, eponyms and
   abbreviations in the stem, the explanation and the why-not lines get a dotted underline; hovering shows a one-line
   trigger or summary built from the app's own data (D.trg, D.jg, D.gloss). Never before answering, so they cannot
   give the answer away."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')


def must(old, new, n=1):
    global s
    assert s.count(old) == n, ('not found x%d' % s.count(old), old[:90])
    s = s.replace(old, new)


# ------------------------------------------------------------------ 1. slim why-not rows
must("""    if (xs[i]) parts.push('<span>' + esc(xs[i]) + '</span>');
    else if (ai[i]) parts.push('<span>' + esc(ai[i]) + ' <span class="tm-aitag" title="Written by your AI">✨ AI</span></span>');
    (fs[i] || []).forEach(t => parts.push('<span class="tm-xf">🔀 Right instead if ' + esc(t.replace(/^if\\s+/i, '')) + '</span>'));
    if (!xs[i] && !ai[i] && !(fs[i] && fs[i].length)) miss++;
    if (!parts.length) { empty.push(L[i]); return ''; }
    return '<div class="tm-xr"><b>' + L[i] + '. ' + esc(o) + '</b>' + parts.join('') + '</div>';""",
     """    const why = xs[i] ? esc(xs[i]) : ai[i] ? esc(ai[i]) + ' <span class="tm-aitag" title="Written by your AI">✨ AI</span>' : '';
    const flips = (fs[i] || []).map(t => { t = t.replace(/^right instead\\s+/i, ''); return /^if\\s/i.test(t) ? 'If ' + esc(t.replace(/^if\\s+/i, '')) : esc(t.charAt(0).toUpperCase() + t.slice(1)); });
    if (!xs[i] && !ai[i] && !flips.length) miss++;
    if (!why && !flips.length) { empty.push(L[i]); return ''; }
    const opt = '<b>' + L[i] + '. ' + esc(o) + '</b>';
    if (!why) return flips.map(f => '<div class="tm-xr"><span class="tm-fa" aria-hidden="true">↳ 🔀</span><span>' + f + ' <span class="tm-fx">➔</span> ' + opt + '</span></div>').join('');
    return '<div class="tm-xr"><span class="tm-fa" aria-hidden="true">↳</span><span>' + opt + '<span class="tm-xc">:</span> ' + why
      + flips.map(f => '<span class="tm-xf">🔀 ' + f + ' <span class="tm-fx">➔</span> <b>' + L[i] + '</b></span>').join('') + '</span></div>';""")
must("""'<div class="tm-x"><span class="tm-fk">❌ Why not the others · 🔀 what would make each one right</span>'""",
     """'<div class="tm-x"><span class="tm-fk">❌ Why not the others · 🔀 change one thing and…</span>'""")

must(""".tm-x{margin-top:10px;display:flex;flex-direction:column;gap:5px}
.tm-xr{display:flex;flex-direction:column;gap:1px;padding:6px 9px;border-radius:8px;border-left:3px solid #ef4444;background:rgba(239,68,68,.09);line-height:1.4}
.tm-xr b{font-size:.9rem}
.tm-xr span{font-size:.88rem}
""", """.tm-x{margin:10px 0 0;padding:2px 0 2px 12px;border-left:3px solid #f08a3c;display:flex;flex-direction:column;gap:5px}
.tm-xr{display:flex;gap:6px;font-size:.9rem;line-height:1.45}
.tm-xr>.tm-fa{flex:0 0 auto;opacity:.7}
.tm-xr b{font-weight:650}
.tm-xc{opacity:.6}
""")
must(".tm-xr .tm-xf{display:block;margin-top:3px;color:var(--muted);font-size:.92em}",
     ".tm-xr .tm-xf{display:block;margin-top:1px;color:var(--muted);font-size:.95em}")
must(".tm-fhead{margin:4px 0 8px;padding:6px 10px;border:1px dashed var(--line);border-radius:10px}",
     ".tm-fhead{margin:0 0 2px;font-size:.9rem;line-height:1.45}")

# ------------------------------------------------------------------ 2. hover / tap tooltips
must("  m.innerHTML = h; hlApply(m, it.id); if (ans) tmCues(m, it); hlPill(m);\n",
     "  m.innerHTML = h; hlApply(m, it.id); if (ans) tmCues(m, it); hlPill(m);\n  if (ans) ttWrap(m);\n")

JS = r"""/* v3.6.14: hover or tap a condition, drug, organism, test, procedure, sign or abbreviation for a one-line summary.
   Built once from the app's own data (D.trg, D.jg, D.gloss); used only after a question is answered. */
let TT = null, ttCur = null;
const TT_KIND = {c: '🩺 Condition', bug: '🦠 Organism', dr: '💊 Drug', ix: '🧪 Test', mx: '🛠️ Procedure', jg: '🔎 Sign', ab: '🔤 Abbreviation'};
const TT_GRAM = {gpc_cl: 'Gram-positive cocci in clusters', gpc_ch: 'Gram-positive cocci in chains', gpc_pr: 'Gram-positive diplococci with a capsule',
  gnc: 'Gram-negative diplococci', gncb: 'Gram-negative coccobacilli', gnr: 'Gram-negative rods', gncv: 'Gram-negative curved rods',
  gpr: 'Gram-positive rods', gprs: 'Gram-positive spore-forming rods', gpbr: 'Gram-positive branching rods', afb: 'Acid-fast bacillus',
  spiro: 'Spirochaete', nowall: 'Bacterium with no cell wall', intra: 'Obligate intracellular bacterium', venv: 'Enveloped virus',
  vnak: 'Non-enveloped virus', yeast: 'Yeast', yeastc: 'Encapsulated yeast', mould: 'Mould', proto: 'Protozoan', mite: 'Mite', louse: 'Louse', worm: 'Helminth'};
const TT_SKIP = new Set(['US', 'PA', 'PD', 'IVF', 'OD', 'ON', 'OM', 'MS', 'HA', 'LL', 'UL', 'NC', 'CR', 'CP', 'PR', 'PT', 'SE', 'AP', 'HD', 'IO', 'RR', 'CN',
  'LN', 'NV', 'PV', 'RA', 'SQ', 'FU', 'HO', 'UO', 'CI', 'BM', 'NAD', 'MET', 'NET', 'MEN', 'MAP', 'LAD', 'CAD', 'ART', 'LCA', 'MOF', 'RSO', 'RMO', 'SHO',
  'DSN', 'EBM', 'IV', 'BMI', 'ECG', 'CRP', 'GI', 'PO', 'PCR', 'FBC', 'U&E', 'LFT', 'ESR', 'ALT', 'AST', 'ALP', 'TFT', 'BP', 'SOB', 'DM', 'Mx', 'Ix', 'Dx', 'Rx', 'Tx', 'FHx', 'DDx', 'PRN', 'QDS', 'TDS', 'stat', 'CCOT', 'BIBA', 'OOH', 'NVD', 'LCir', 'ABC', 'ABCDE', 'CBT', 'TTO', 'PET', 'CF', 'AMS', 'ANP', 'MDD', 'SCZ', 'PERT', 'PEP', 'MSE', 'CTB', 'CTH', 'MT']);
function ttMd(t){ return esc(String(t || '')).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); }
function ttBuild(){
  if (TT) return TT;
  const T = D.trg || {}, map = new Map(), list = [];
  const add = (k, e, pri) => {
    k = String(k || '').replace(/\s*\([^)]*\)/g, '').replace(/\s+/g, ' ').trim();
    if (k.length < 3 && !/^[A-Z]{2}$/.test(k)) return;
    if (TT_SKIP.has(k)) return;
    const key = k.toLowerCase(), old = map.get(key);
    if (old && old.p <= pri) return;
    if (e.id == null) { e.id = list.length; list.push(e); }
    map.set(key, {p: pri, k, cs: /^[A-Z0-9][A-Za-z0-9&/-]{1,7}$/.test(k) && (k.match(/[A-Z]/g) || []).length >= 2, e});
  };
  (D.jg || []).forEach(j => {
    const e = {t: 'jg', h: j.t, l: j.f, a: j.h ? '💡 ' + j.h : ''};
    String(j.t).split(/\s+vs\.?\s+/).forEach(n => add(n, e, 0));
    (j.al || []).forEach(a => add(a, e, 0));
  });
  Object.values(T.c || {}).forEach(([trig, dx]) => {
    const [n0, ...r] = String(dx || '').split(':');
    const n = n0.split(',')[0].replace(/^Likely\s+/, '').trim();
    if (n.split(' ').length > 5 || /\b(first|ladder|irrigate|threatening|maintenance|high risk|then|grade|blocking|from an|with bone)\b/i.test(n)) return;
    add(n, {t: 'c', h: n, l: trig, a: r.join(':').trim() ? '➔ ' + r.join(':').trim() : ''}, 1);
  });
  Object.entries(D.snap || {}).forEach(([k, v]) => {
    const n = String(v.n || '');
    if (!n || /\band\b|[,:&/]|^(Headache|Arrhythmias|Hernias|Aneurysms|Constipation|Sepsis)$/.test(n)) return;
    const c = (T.c || {})[k], e = {t: 'c', h: n, l: v.m, a: c ? '🎯 ' + c[0] : v.w ? '👤 ' + v.w : ''};
    add(n, e, 2);
  });
  const DX = /(itis|osis|oma|aemia|pathy|syndrome|disease|palsy|cancer|carcinoma|tumour|ulcer|infarct|stenosis|regurgitation|failure|fibrosis|ectasis|hernia|cyst|gravis|abscess|fever|dyskinesia|tachycardia|flutter|fibrillation|pregnancy|haemorrhage|haematoma|embolism|thrombosis|aneurysm|dementia|keratosis|pemphigoid|megacolon|demyelination|polydipsia|sprue|spasm|lymphoma|leukaemia|disorder|phenomenon|mellitus|insipidus|neuroma|schwannoma|plasia|ischaemia|dissection|torsion|volvulus|obstruction|perforation|psychosis|mania|delirium|neuritis|vera|angina|ileus|colic|toxicity|anaphylaxis|shock)$/i;
  (D.hunt || []).forEach(h => {
    const a = String(h[2] || '').replace(/\*\*/g, ''), n = a.split(/\s*(?:→|:|;|,| — | - |\(| = | vs |\+)\s*/)[0].trim();
    if (n.split(' ').length > 4 || n.length < 5 || /\d|until|proven|[/>"]|^(Acute|Chronic|Other|Viral|Primary|Secondary) \w+$|^(Exclude|Favours|Causes|Not|Usually|Slit-lamp|Ipsilateral|Obstructing|Abscess or)\b/.test(n) || !/^[A-Z]/.test(n)) return;
    if (/^(Abscess|Acidosis|Adenocarcinoma|Cancer|Fever|Fibrosis|Haematoma|Perforation|Thrombosis|Torsion|Lymphoma|Myopathy|Polyposis|Vasospasm|Pneumonitis|Calcinosis|Parakeratosis|Steatosis|Ototoxicity)$/.test(n)) return;
    if (!DX.test(n) && !/^[A-Z][a-z]+'s?( (disease|syndrome|sign|triad))?$/.test(n)) return;
    add(n, {t: 'c', h: n, l: '🎯 ' + h[1], a: '➔ ' + a}, 2.5);
  });
  const scen = {};
  (T.sc || []).forEach(g => (g[2] || []).forEach(([id, tr, ans]) => { if (!scen[id]) scen[id] = [tr, ans]; }));
  Object.entries(T.bug || {}).forEach(([id, [n, al, cl]]) => {
    const sc = scen[id], e = {t: 'bug', h: n, l: TT_GRAM[cl] || '', a: sc ? '🎯 ' + sc[0] + ' ➔ ' + sc[1] : ''};
    add(n, e, 3);
    if (/^Staph /.test(n)) add(n.replace(/^Staph /, 'Staphylococcus '), e, 3);
    if (/^Strep /.test(n)) add(n.replace(/^Strep /, 'Streptococcus '), e, 3);
    if (/^H\. /.test(n)) add(n.replace(/^H\. /, 'Helicobacter ').replace('Helicobacter influenzae', 'Haemophilus influenzae'), e, 3);
    if (al && al.split(' ').length <= 2 && !/\b(rice|virus|mite|atypical)\b/.test(al)) add(al, e, 3);
  });
  const grp = (G, t, pri) => (G || []).forEach(g => (g[2] || []).forEach(([n, ic, use, pit]) => {
    if (/\bvs\b|timing|aftercare|position check/.test(n)) return;
    const p = (pit || [])[0], e = {t, h: n.split(' · ')[0], l: use, w: p ? p[0] + ' ➔ ' + p[1] : ''};
    n.split(' · ').forEach((x, j) => { if (!j || t === 'dr' || /[A-Z]|\s/.test(x)) add(x, e, pri); });
  }));
  grp(T.dr, 'dr', 4); grp(T.ix, 'ix', 5); grp(T.mx, 'mx', 5);
  (D.gloss || []).forEach(([k, v]) => {
    if (!/^[A-Za-z][A-Za-z0-9&/-]{1,7}$/.test(k) || (k.match(/[A-Z]/g) || []).length < 2) return;
    add(k, {t: 'ab', h: k, l: v}, 6);
  });
  const keys = [...map.values()].map(v => v.k).sort((a, b) => b.length - a.length);
  let re = null;
  try { re = new RegExp('(?<![\\p{L}\\p{N}])(' + keys.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('|') + ')(s?)(?![\\p{L}\\p{N}])', 'giu'); } catch (e) { re = null; }
  TT = {map, list, re};
  return TT;
}
function ttWrap(m){
  if (S.set.ttOff) return;
  const tt = ttBuild(); if (!tt.re) return;
  const seen = new Set(); let n = 0;
  m.querySelectorAll('.hq-stem, .hq-why, .tm-x, .hq-flip').forEach(root => {
    const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {acceptNode: x => x.parentNode.closest('button,a,input,textarea,select,code,.tt,.tm-aitag,.tm-fk,.hq-labw') ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT});
    const nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
    nodes.forEach(node => {
      const s = node.data; let mt, last = 0, frag = null;
      tt.re.lastIndex = 0;
      while (n < 40 && (mt = tt.re.exec(s))) {
        const v = tt.map.get(mt[1].toLowerCase());
        if (!v || (v.cs && mt[1] !== v.k) || seen.has(v.e.id)) continue;
        seen.add(v.e.id); n++;
        frag = frag || document.createDocumentFragment();
        frag.append(s.slice(last, mt.index));
        const sp = document.createElement('span'); sp.className = 'tt tt-' + v.e.t; sp.dataset.tt = v.e.id; sp.textContent = mt[0];
        frag.append(sp); last = mt.index + mt[0].length;
      }
      if (frag) { frag.append(s.slice(last)); node.replaceWith(frag); }
    });
  });
}
function ttShow(el, pin){
  const e = ttBuild().list[+el.dataset.tt]; if (!e) return;
  let p = document.getElementById('ttpop');
  if (!p) { p = document.createElement('div'); p.id = 'ttpop'; p.setAttribute('role', 'tooltip'); document.body.appendChild(p); }
  p.innerHTML = '<div class="tt-h"><span class="tt-k">' + TT_KIND[e.t] + '</span><b>' + esc(e.h) + '</b></div>' + (e.l ? '<div class="tt-l">' + ttMd(e.l) + '</div>' : '')
    + (e.a ? '<div class="tt-a">' + ttMd(e.a) + '</div>' : '') + (e.w ? '<div class="tt-w' + (e.t === 'dr' ? '">⚠️ ' : ' tt-n">↪ ') + ttMd(e.w) + '</div>' : '');
  p.className = 'on' + (pin ? ' pin' : '');
  const r = el.getBoundingClientRect(), W = Math.min(330, window.innerWidth - 24);
  p.style.width = W + 'px';
  const x = Math.max(12, Math.min(r.left + r.width / 2 - W / 2, window.innerWidth - W - 12));
  let y = r.top - p.offsetHeight - 8; if (y < 8) y = r.bottom + 8;
  p.style.left = (x + window.scrollX) + 'px'; p.style.top = (y + window.scrollY) + 'px';
  ttCur = el;
}
function ttHide(){ const p = document.getElementById('ttpop'); if (p) p.className = ''; ttCur = null; }
function ttPinned(){ const p = document.getElementById('ttpop'); return !!(p && p.classList.contains('pin')); }
document.addEventListener('mouseover', ev => {
  const t = ev.target.closest && ev.target.closest('.tt');
  if (t && t !== ttCur && !ttPinned()) ttShow(t);
  else if (!t && ttCur && !ttPinned()) ttHide();
});
document.addEventListener('click', ev => {
  const t = ev.target.closest && ev.target.closest('.tt');
  if (t && !t.closest('.hq-stem.hl-on')) { if (t === ttCur && ttPinned()) ttHide(); else ttShow(t, true); return; }
  if (!(ev.target.closest && ev.target.closest('#ttpop'))) ttHide();
});
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && ttCur) ttHide(); });
window.addEventListener('scroll', () => { if (ttCur && !ttPinned()) ttHide(); }, {passive: true});
window.addEventListener('hashchange', ttHide);
window.MEtt = {build: ttBuild, wrap: ttWrap};
"""
must("function tmWhyNot(it){\n", JS + "function tmWhyNot(it){\n")

CSS = """.tt{text-decoration:underline dotted;text-decoration-thickness:1.5px;text-underline-offset:3px;cursor:help;text-decoration-color:var(--muted)}
.tt:hover{background:rgba(127,127,127,.14);border-radius:3px}
.tt-c{text-decoration-color:#f59e0b}.tt-dr{text-decoration-color:#38bdf8}.tt-bug{text-decoration-color:#a78bfa}
.tt-ix,.tt-mx{text-decoration-color:#2dd4bf}.tt-jg{text-decoration-color:#f472b6}
#ttpop{position:absolute;z-index:9999;display:none;padding:9px 11px;border-radius:10px;background:#111827;color:#f3f4f6;font-size:.82rem;line-height:1.45;box-shadow:0 10px 28px rgba(0,0,0,.4);border:1px solid rgba(255,255,255,.12);pointer-events:none}
#ttpop.on{display:block}#ttpop.pin{pointer-events:auto}
#ttpop .tt-h{display:flex;flex-wrap:wrap;gap:6px;align-items:center;margin-bottom:4px}
#ttpop .tt-k{font-size:.68rem;padding:1px 7px;border-radius:999px;background:rgba(255,255,255,.12);white-space:nowrap}
#ttpop .tt-a{margin-top:4px;color:#a7f3d0}#ttpop .tt-w{margin-top:4px;color:#fcd34d}#ttpop .tt-n{color:#bae6fd}
"""
must(".tm-score{margin:8px 0 0;font-size:.9rem}\n", ".tm-score{margin:8px 0 0;font-size:.9rem}\n" + CSS)

F.write_text(s, encoding='utf-8')
print('v3614 ui ok')
