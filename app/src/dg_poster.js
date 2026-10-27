/* medengine 🗺️ Posters: one engine for both apps.
   Every poster follows the same code, PLACE + LOCK:
   Picture with the words on it · Location never changes · Arrows carry the movement · Contrast with the lookalike ·
   Exaggerate one thing · then 🔒 LOCK hides the details so you say them before you tap.
   Zones always sit in the same place and colour: 1 🧬 cause (purple, top-left) → 2 🧍 who (amber, top-right) →
   3 🧪 prove (blue, right) → 4 💊 treat (green, bottom-right) → 5 🚩 watch (red, bottom-left) → 6 ⚖️ lookalike (slate, left),
   with 👀 spot-it in the centre and the 🪝 hook along the bottom. */
(function () {
  var P = window.PO = {};
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c]; }); };
  P.esc = esc;

  /* ---------- 🔒 what counts as a detail: numbers with units, drugs and drug classes ---------- */
  var DRUGS = ('aspirin clopidogrel ticagrelor prasugrel heparin LMWH enoxaparin dalteparin fondaparinux warfarin apixaban rivaroxaban edoxaban dabigatran DOAC alteplase tenecteplase ' +
    'atorvastatin simvastatin rosuvastatin statin ezetimibe inclisiran bisoprolol atenolol propranolol labetalol metoprolol carvedilol beta-blocker amlodipine nifedipine diltiazem verapamil CCB ' +
    'ramipril lisinopril enalapril perindopril ACE-inhibitor losartan candesartan valsartan ARB ARNI sacubitril indapamide bendroflumethiazide thiazide-like thiazide spironolactone eplerenone ' +
    'furosemide bumetanide loop-diuretic digoxin amiodarone flecainide adenosine atropine adrenaline noradrenaline GTN isosorbide nitrate ivabradine ranolazine dapagliflozin empagliflozin SGLT2 ' +
    'metformin gliclazide sulfonylurea sitagliptin DPP-4 pioglitazone semaglutide liraglutide GLP-1 insulin glucagon levothyroxine liothyronine carbimazole propylthiouracil radioiodine ' +
    'hydrocortisone prednisolone dexamethasone methylprednisolone fludrocortisone steroid steroids salbutamol terbutaline ipratropium tiotropium SABA SAMA LAMA LABA ICS MART formoterol salmeterol ' +
    'budesonide beclometasone fluticasone montelukast theophylline aminophylline magnesium amoxicillin co-amoxiclav clarithromycin erythromycin azithromycin doxycycline lymecycline flucloxacillin ' +
    'phenoxymethylpenicillin benzylpenicillin penicillin ceftriaxone cefalexin cefuroxime cefotaxime gentamicin vancomycin teicoplanin metronidazole nitrofurantoin trimethoprim ciprofloxacin ofloxacin ' +
    'levofloxacin rifampicin isoniazid pyrazinamide ethambutol pyridoxine aciclovir valaciclovir oseltamivir fidaxomicin chloramphenicol fusidic hydrogen-peroxide mupirocin terbinafine clotrimazole ' +
    'miconazole nystatin fluconazole permethrin malathion dimeticone omeprazole lansoprazole PPI loperamide macrogol senna lactulose ispaghula mesalazine 5-ASA azathioprine methotrexate ' +
    'infliximab adalimumab biologics ciclosporin tacrolimus mycophenolate hydroxychloroquine sulfasalazine colchicine allopurinol febuxostat paracetamol ibuprofen naproxen diclofenac NSAID NSAIDs ' +
    'codeine dihydrocodeine tramadol morphine oxycodone fentanyl buprenorphine diamorphine naloxone opioid opioids amitriptyline nortriptyline duloxetine gabapentin pregabalin carbamazepine ' +
    'lamotrigine levetiracetam valproate phenytoin lorazepam midazolam diazepam benzodiazepine chlordiazepoxide thiamine Pabrinex acamprosate naltrexone disulfiram methadone sertraline citalopram ' +
    'escitalopram fluoxetine paroxetine SSRI mirtazapine venlafaxine lithium olanzapine quetiapine risperidone aripiprazole haloperidol clozapine antipsychotic procyclidine dantrolene bromocriptine ' +
    'cyproheptadine lisdexamfetamine methylphenidate atomoxetine guanfacine sumatriptan triptan topiramate acetazolamide mannitol nimodipine riluzole pyridostigmine immunoglobulin IVIG tamsulosin ' +
    'alpha-blocker finasteride oxybutynin mirabegron alendronate bisphosphonate denosumab tamoxifen letrozole anastrozole trastuzumab BCG latanoprost timolol pilocarpine cyclopentolate ' +
    'acetylcysteine desferrioxamine fomepizole flumazenil protamine idarucizumab andexanet vitamin-K sodium-bicarbonate hydroxocobalamin folic-acid ferrous calcium-gluconate prochlorperazine ' +
    'betahistine cinnarizine ondansetron metoclopramide cyclizine domperidone emollient emollients adapalene benzoyl-peroxide isotretinoin tretinoin calcipotriol dithranol tacrolimus-ointment ' +
    'antihistamine omalizumab cetirizine loratadine fexofenadine chlorphenamine anti-VEGF Naseptin silver-nitrate oxygen').split(/\s+/);
  var DRUG_SRC = DRUGS.map(function (d) { return d.replace(/[.*+?^${}()|[\]\\]/g, '\\$&').replace(/-/g, '[- ]'); }).sort(function (a, b) { return b.length - a.length; }).join('|');
  var NUM_SRC = '(?:[≥≤<>]\\s?)?\\d+(?:[.,]\\d+)?(?:\\s?(?:to|–|-)\\s?\\d+(?:[.,]\\d+)?)?(?:\\s?(?:%|mg\\/kg|mg|micrograms?|kg|g|mL|ml|litres?|L|mmol\\/L|mmol|units?|hours?|h|minutes?|min|seconds?|s|days?|weeks?|months?|years?|cm²|cm|mmHg|mm|kcal|ppb|°C|°))?';
  function hits(seg) {
    var out = [], m, re;
    re = new RegExp(NUM_SRC, 'g');
    while ((m = re.exec(seg))) {
      if (!m[0]) { re.lastIndex++; continue; }
      var a = m.index, b = a + m[0].length, pc = seg.charAt(a - 1), nc = seg.charAt(b), nn = seg.charAt(b + 1);
      if (/[A-Za-z0-9]/.test(pc) || /[A-Za-z0-9]/.test(nc) || (nc === '-' && /[A-Za-z]/.test(nn))) continue;
      out.push([a, b]);
    }
    re = new RegExp('\\b(?:' + DRUG_SRC + ')\\b', 'gi');
    while ((m = re.exec(seg))) out.push([m.index, m.index + m[0].length]);
    out.sort(function (x, y) { return x[0] - y[0] || y[1] - x[1]; });
    var keep = [], end = -1;
    out.forEach(function (h) { if (h[0] >= end) { keep.push(h); end = h[1]; } });
    return keep;
  }
  function tok(seg) {
    var o = '', last = 0;
    hits(seg).forEach(function (h) { o += esc(seg.slice(last, h[0])) + '<span class="pz">' + esc(seg.slice(h[0], h[1])) + '</span>'; last = h[1]; });
    return o + esc(seg.slice(last));
  }
  function bold(t, f) { return String(t == null ? '' : t).split('**').map(function (s, i) { var h = f(s); return i % 2 ? '<b>' + h + '</b>' : h; }).join(''); }
  /* lk(t): details become pills. lk(t, 1): the whole line is the pill. plain(t): no pills. */
  function lk(t, all) { return all ? '<span class="pz">' + bold(t, esc) + '</span>' : bold(t, tok); }
  function plain(t) { return bold(t, esc); }
  function arrow(t) { var s = String(t == null ? '' : t), i = s.lastIndexOf(' → '); return i > 0 ? '<b>' + plain(s.slice(0, i)) + ' →</b> ' + lk(s.slice(i + 3), 1) : lk(s); }
  P.arrow = arrow;
  P.lk = lk; P.plain = plain; P.hits = hits;

  /* ---------- shared pictures ---------- */
  function org(o, r) { var O = window.DG && DG.ORG && (DG.ORG[o] || DG.ORG.blood); return O ? '<svg class="po-org" viewBox="0 0 160 210" aria-hidden="true">' + O.draw(r) + '</svg>' : ''; }
  function orgLabel(o, r) { var O = window.DG && DG.ORG && DG.ORG[o]; return (O && O.lab && O.lab[r]) || r || ''; }
  function pinCircle(x, y, n, cls) { return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="8" class="po-pin' + (cls ? ' ' + cls : '') + '"/><text x="' + x.toFixed(1) + '" y="' + (y + 3.4).toFixed(1) + '" text-anchor="middle" class="po-pn">' + n + '</text>'; }
  function bodySvg(items) {
    var LOC = (window.DG && DG.LOC) || {}, used = {}, s = window.DG ? DG.H.body(70, 6, 200) : '';
    items.forEach(function (it, k) {
      var p = LOC[it[1]] || LOC.all || [30, 30], rep = used[it[1]] = (used[it[1]] || 0) + 1, o = OFF[(rep - 1) % OFF.length], fx = p[0] > 0 ? -1 : 1;
      s += pinCircle(70 + p[0] + o[0] * fx, 6 + p[1] + o[1], k + 1);
    });
    return '<svg class="po-body" viewBox="0 0 140 212" aria-hidden="true">' + s + '</svg>';
  }
  var OFF = [[0, 0], [15, 0], [-15, 0], [0, 15], [0, -15], [15, 15]];
  /* a front-facing head and neck for the eye, ENT, cranial nerve and neck examinations */
  var HEAD = {top: [100, 34], forehead: [100, 52], eyes: [78, 86], reye: [78, 86], leye: [122, 86], brow: [100, 68], nose: [100, 108], mouth: [100, 134], tongue: [100, 140], cheek: [66, 118], face: [134, 120],
    rear: [40, 98], lear: [160, 98], ear: [40, 98], jaw: [100, 160], neck: [100, 200], thyroid: [100, 206], throat: [100, 180], nodes: [68, 188], shoulder: [40, 226], back: [160, 226], hands: [182, 226], all: [178, 38]};
  /* body-map places, re-homed when a condition lives in the head and neck */
  var HEADOF = {head: 'top', mind: 'forehead', eyes: 'eyes', face: 'cheek', ear: 'ear', nose: 'nose', mouth: 'mouth', neck: 'neck', throat: 'throat', chest: 'shoulder', lchest: 'shoulder', lungs: 'shoulder', heart: 'back', back: 'back', hands: 'hands', lhand: 'hands', rarm: 'shoulder', larm: 'back', legs: 'back', lleg: 'back', feet: 'back'};
  var EYES = [[78, 86], [122, 86], [78, 68], [122, 68], [100, 60], [100, 104]];
  P.HEAD = HEAD;
  P.headish = function (items) { var n = 0; (items || []).forEach(function (it) { if (/^(head|mind|eyes|face|ear|nose|mouth|neck|throat)$/.test(it[1])) n++; }); return items && items.length > 1 && n / items.length >= 0.6; };
  function headSvg(items) {
    var s = '<path class="dg-body" d="M60 214 Q60 196 78 188 L78 170 Q44 150 42 100 Q42 32 100 30 Q158 32 158 100 Q156 150 122 170 L122 188 Q140 196 140 214 Q172 216 196 236 L4 236 Q28 216 60 214 Z" style="fill:var(--surface);stroke:var(--muted);stroke-width:1.4"/>';
    s += '<ellipse cx="40" cy="100" rx="7" ry="15" style="fill:var(--surface);stroke:var(--muted)"/><ellipse cx="160" cy="100" rx="7" ry="15" style="fill:var(--surface);stroke:var(--muted)"/>';
    s += '<ellipse cx="78" cy="86" rx="12" ry="7" style="fill:none;stroke:var(--muted)"/><ellipse cx="122" cy="86" rx="12" ry="7" style="fill:none;stroke:var(--muted)"/><circle cx="78" cy="86" r="3" style="fill:var(--muted)"/><circle cx="122" cy="86" r="3" style="fill:var(--muted)"/>';
    s += '<path d="M100 92 L94 112 Q100 116 106 112" style="fill:none;stroke:var(--muted)"/><path d="M86 134 Q100 142 114 134" style="fill:none;stroke:var(--muted)"/>';
    var used = {};
    items.forEach(function (it, k) {
      var key = HEAD[it[1]] ? it[1] : (HEADOF[it[1]] || 'all'), rep = used[key] = (used[key] || 0) + 1, p;
      if (key === 'eyes') p = EYES[(rep - 1) % EYES.length];
      else { var b = HEAD[key], o = OFF[(rep - 1) % OFF.length], fx = b[0] > 100 ? -1 : 1; p = [b[0] + o[0] * fx, b[1] + o[1]]; }
      s += pinCircle(p[0], p[1], k + 1);
    });
    return '<svg class="po-body po-head" viewBox="0 0 200 238" aria-hidden="true">' + s + '</svg>';
  }
  P.bodySvg = bodySvg; P.headSvg = headSvg; P.org = org;

  /* ---------- tools bar, shared by every poster ---------- */
  function tools(o) {
    o = o || {};
    return '<div class="po-tools"><button type="button" class="po-b" data-polock aria-pressed="false" title="Hide the details: say them, then tap each pill (key L)">🔒 Lock</button><button type="button" class="po-b" data-poplay title="Walk the poster zone by zone">▶ Walk it</button>' + (o.extra || '') + '<span class="po-cnt" aria-live="polite"></span></div>';
  }
  function zone(cls, ord, col, icon, head, body, extra) {
    return '<section class="po-z ' + cls + '" data-ord="' + ord + '" style="--z:var(--po-' + col + ')"' + (extra || '') + '><h4><i>' + (typeof ord === 'number' ? ord : icon) + '</i>' + (typeof ord === 'number' ? icon + ' ' : '') + esc(head) + '</h4>' + body + '</section>';
  }
  P.zone = zone; P.tools = tools;

  /* ---------- the condition poster ---------- */
  P.cond = function (s, o) {
    o = o || {};
    var topic = s.k === 't', H = topic ? ['The idea', 'Who and when', 'What you see', 'Check', 'The steps', 'Danger'] : ['What goes wrong', 'Who gets it', 'Spot it', 'Prove it', 'Treat', 'Watch for'];
    var segs = String(s.m || '').split(/\s*→\s*/);
    var chain = '<ol class="po-chain">' + segs.map(function (g, k) { return '<li' + (k === segs.length - 1 ? ' class="end"' : '') + '>' + lk(g) + '</li>'; }).join('') + '</ol>';
    var z1 = zone('z1', 1, 'cause', '🧬', H[0], '<div class="po-cause"><figure class="po-orgf">' + org(s.o, s.r) + '<figcaption>' + esc(orgLabel(s.o, s.r)) + '</figcaption></figure>' + chain + '</div>');
    var signs = s.s || [];
    var zc = zone('zc', 'c', 'spot', '👀', H[2], '<div class="po-spot">' + (P.headish(signs) ? headSvg(signs) : bodySvg(signs)) + '<ol class="po-signs">' + signs.map(function (it) { return '<li>' + lk(it[0], 1) + '</li>'; }).join('') + '</ol></div>');
    var w = String(s.w || '').split(/\s*·\s*/);
    var z2 = zone('z2', 2, 'who', '🧍', H[1], '<div class="po-who"><b class="po-big">' + lk(w[0], 1) + '</b><div class="po-chips">' + w.slice(1).map(function (x) { return '<span>' + lk(x) + '</span>'; }).join('') + '</div></div>');
    var z3 = zone('z3', 3, 'test', '🧪', H[3], '<ul class="po-tests">' + (s.x || []).map(function (x) { return '<li' + (x[2] ? ' class="gold"' : '') + '><b>' + (x[2] ? '★ ' : '') + plain(x[0]) + '</b>' + (x[1] ? '<span>→ ' + lk(x[1], 1) + '</span>' : '') + '</li>'; }).join('') + '</ul>');
    var st = s.t || [];
    var z4 = zone('z4', 4, 'treat', '💊', H[4], '<ol class="po-ladder">' + st.map(function (x, k) { return '<li style="--k:' + k + '"' + (k === st.length - 1 ? ' class="top"' : '') + '><i>' + (k + 1) + '</i><span>' + lk(x) + '</span></li>'; }).join('') + '</ol><p class="po-note">Climb from 1: first move at the bottom, the cure at the top.</p>');
    var z5 = zone('z5', 5, 'watch', '🚩', H[5], '<ul class="po-watch">' + (s.d || []).map(function (x) { return '<li class="u-' + esc(x[1]) + '"><i></i><span>' + lk(x[0], 1) + '</span></li>'; }).join('') + '</ul><p class="po-key"><i class="u-e"></i>now <i class="u-s"></i>today <i class="u-u"></i>soon <i class="u-c"></i>cancer pathway <i class="u-r"></i>routine</p>');
    var v = s.v;
    var z6 = v ? zone('z6', 6, 'vs', '⚖️', 'Don\'t confuse with', '<div class="po-vs"><p class="po-axis">' + esc(v[1]) + '</p><div class="po-vs2"><div><b>' + esc(v[4] || s.n) + '</b>' + lk(v[2], 1) + '</div><span class="po-vsx">vs</span><div><b>' + esc(v[0]) + '</b>' + lk(v[3], 1) + '</div></div></div>') : '';
    return '<div class="po po-cond' + (o.lock ? ' lock' : '') + (v ? '' : ' nov') + '" data-po="' + esc(o.id || '') + '"><div class="po-bar"><div class="po-tt"><span class="po-badge">🗺️</span><b>' + esc(s.n) + '</b></div>' + tools(o) + '</div>'
      + '<div class="po-grid">' + z1 + zc + z2 + z3 + z4 + z5 + z6 + '</div><div class="po-hook" data-ord="7"><i>🪝</i><span>' + plain(s.h) + '</span></div>' + (o.foot || '') + '</div>';
  };

  /* ---------- master posters: split columns, a matrix, a figure, and what the AI version got wrong ---------- */
  var COL = {b: 'test', r: 'watch', g: 'treat', a: 'who', p: 'cause', t: 'spot', s: 'vs'};
  P.FIG = {};
  P.split = function (m, o) {
    o = o || {};
    var h = '<div class="po po-split' + (o.lock ? ' lock' : '') + '" data-po="' + esc(m.id) + '"><div class="po-bar"><div class="po-tt"><span class="po-badge">' + esc(m.ic || '🧭') + '</span><b>' + esc(m.t) + '</b>' + (m.sub ? '<span class="po-sub">' + plain(m.sub) + '</span>' : '') + '</div>' + tools(o) + '</div>';
    if (m.fig && P.FIG[m.fig]) h += '<figure class="po-fig" data-ord="0">' + P.FIG[m.fig](m) + '</figure>';
    if (m.cols) h += '<div class="po-cols" style="--n:' + m.cols.length + '">' + m.cols.map(function (c, k) {
      return '<section class="po-z" data-ord="' + (k + 1) + '" style="--z:var(--po-' + (COL[c.c] || 'test') + ')"><h4><i>' + (k + 1) + '</i>' + (c.i ? esc(c.i) + ' ' : '') + plain(c.h) + '</h4>' + (c.sub ? '<p class="po-sub2">' + plain(c.sub) + '</p>' : '') + '<ul class="po-items">' + c.items.map(function (it) { return '<li>' + (it[0] ? '<b>' + plain(it[0]) + '</b> ' : '') + lk(it[1], it[2] == null ? 1 : it[2]) + '</li>'; }).join('') + '</ul></section>';
    }).join('') + '</div>';
    if (m.mx) h += '<div class="po-mxw" data-ord="' + ((m.cols || []).length + 1) + '"><table class="po-mx" style="min-width:' + Math.max(520, m.mx.head.length * 118) + 'px"><thead><tr>' + m.mx.head.map(function (x) { return '<th>' + plain(x) + '</th>'; }).join('') + '</tr></thead><tbody>' + m.mx.rows.map(function (r) {
      return '<tr>' + r.map(function (x, j) { return j === 0 ? '<th>' + plain(x) + '</th>' : '<td>' + lk(x, 1) + '</td>'; }).join('') + '</tr>';
    }).join('') + '</tbody></table></div>';
    if (m.foot) h += '<div class="po-foot" data-ord="98">' + m.foot.map(function (f) { return '<div><b>' + plain(f[0]) + '</b><span>' + lk(f[1], 1) + '</span></div>'; }).join('') + '</div>';
    if (m.hook) h += '<div class="po-hook" data-ord="99"><i>🪝</i><span>' + plain(m.hook) + '</span></div>';
    if ((m.fix || []).length) h += '<details class="po-fix"><summary>🔎 What the AI-made version of this poster got wrong · ' + m.fix.length + '</summary><ul>' + m.fix.map(function (x) { return '<li>' + plain(x) + '</li>'; }).join('') + '</ul></details>';
    if (m.src) h += '<p class="po-src">Checked against: ' + plain(m.src) + '</p>';
    return h + '</div>';
  };

  /* ---------- OSCE station posters ---------- */
  /* corners: a 10-minute consultation as 4 time-stamped corners around one clock */
  P.corners = function (c, o) {
    o = o || {};
    var pos = ['tl', 'tr', 'bl', 'br'];
    var h = '<div class="po po-corners' + (o.lock ? ' lock' : '') + (o.sprint ? ' sprint' : '') + '" data-po="' + esc(c.id || '') + '"><div class="po-bar"><div class="po-tt"><span class="po-badge">🗺️</span><b>' + esc(c.t) + '</b>' + (c.sub ? '<span class="po-sub">' + plain(c.sub) + '</span>' : '') + '</div>' + tools(o) + '</div>';
    h += '<div class="po-clock" aria-hidden="true">' + c.zones.map(function (z) { return '<span style="--z:var(--po-' + z.c + ');flex:' + (z.span || 1) + '"><b>' + esc(z.time || '') + '</b>' + esc(z.i) + '</span>'; }).join('') + '</div>';
    if (c.top) h += c.top;
    h += '<div class="po-4">' + c.zones.map(function (z, k) {
      return '<section class="po-z q-' + pos[k] + '" data-ord="' + (k + 1) + '" style="--z:var(--po-' + z.c + ')"><h4><i>' + (k + 1) + '</i>' + esc(z.i) + ' ' + esc(z.h) + (z.time ? '<em>' + esc(z.time) + '</em>' : '') + '</h4>' + (z.html || '<ul class="po-items">' + z.lines.map(function (l) { return '<li>' + (typeof l === 'string' ? lk(l) : (l.h ? '<b>' + plain(l.h) + '</b> ' : '') + lk(l.t, l.all)) + '</li>'; }).join('') + '</ul>') + '</section>';
    }).join('') + '</div>';
    if (c.hook) h += '<div class="po-hook" data-ord="5"><i>🪝</i><span>' + plain(c.hook) + '</span></div>';
    if (c.foot) h += c.foot;
    return h + '</div>';
  };
  /* route: an examination as numbered pins walked around a body or a head */
  P.route = function (r, o) {
    o = o || {};
    var pins = r.pins || [], map = r.map === 'head' ? headSvg(pins) : bodySvg(pins);
    var h = '<div class="po po-route' + (o.lock ? ' lock' : '') + '" data-po="' + esc(r.id || '') + '"><div class="po-bar"><div class="po-tt"><span class="po-badge">🗺️</span><b>' + esc(r.t) + '</b></div>' + tools(o) + '</div>';
    h += '<div class="po-props" data-ord="1"><b>🎬 Before you touch</b>' + (r.props || []).map(function (p) { return '<span>' + plain(p) + '</span>'; }).join('<i>→</i>') + '</div>';
    h += '<div class="po-rt"><section class="po-z" data-ord="2" style="--z:var(--po-spot)"><h4><i>2</i>👣 The route, same order every time</h4><div class="po-spot">' + map + '<ol class="po-signs po-pins">' + pins.map(function (p) { return '<li><b>' + plain(p[0]) + '</b>' + (p[2] ? '<span>' + lk(p[2], 1) + '</span>' : '') + '</li>'; }).join('') + '</ol></div></section>';
    h += '<section class="po-z" data-ord="3" style="--z:var(--po-watch)"><h4><i>3</i>🔍 Hunt these</h4><ul class="po-items">' + (r.hunt || []).map(function (x) { return '<li>' + arrow(x) + '</li>'; }).join('') + '</ul></section></div>';
    h += '<div class="po-2"><section class="po-z" data-ord="4" style="--z:var(--po-test)"><h4><i>4</i>✅ To complete</h4><ul class="po-items po-inline">' + (r.done || []).map(function (x) { return '<li>' + lk(x, 1) + '</li>'; }).join('') + '</ul></section>';
    h += '<section class="po-z" data-ord="5" style="--z:var(--po-treat)"><h4><i>5</i>🎤 Present</h4><p class="po-say">' + lk(r.present || '', 1) + '</p></section></div>';
    return h + '</div>';
  };
  /* story: a procedure as 3 frames, set up → the move → finish and act */
  P.story = function (s, o) {
    o = o || {};
    var h = '<div class="po po-story' + (o.lock ? ' lock' : '') + '" data-po="' + esc(s.id || '') + '"><div class="po-bar"><div class="po-tt"><span class="po-badge">🎬</span><b>' + esc(s.t) + '</b></div>' + tools(o) + '</div><div class="po-frames">';
    var cols = ['spot', 'watch', 'treat'];
    h += s.frames.map(function (f, k) {
      return (k ? '<span class="po-arrow" aria-hidden="true">→</span>' : '') + '<section class="po-z po-frame" data-ord="' + (k + 1) + '" style="--z:var(--po-' + cols[k] + ')"><h4><i>' + (k + 1) + '</i>' + esc(f.i) + ' ' + esc(f.h) + '</h4><ul class="po-items">' + f.lines.map(function (l) { return '<li>' + lk(l, 1) + '</li>'; }).join('') + '</ul>' + (f.fail ? '<p class="po-fail">🚫 ' + lk(f.fail) + '</p>' : '') + '</section>';
    }).join('') + '</div>';
    if ((s.nums || []).length) h += '<div class="po-foot" data-ord="4">' + s.nums.map(function (n) { return '<div><b>' + plain(n[0]) + '</b><span>' + lk(n[1], 1) + '</span></div>'; }).join('') + '</div>';
    return h + '</div>';
  };

  /* ---------- behaviour: lock, reveal, walk ---------- */
  P.lockOn = false;
  function count(po) { var all = po.querySelectorAll('.pz'), open = po.querySelectorAll('.pz.rv'), c = po.querySelector('.po-cnt'); if (c) c.textContent = po.classList.contains('lock') && all.length ? open.length + ' of ' + all.length + ' open' : ''; }
  function setLock(po, on) {
    po.classList.toggle('lock', on);
    Array.prototype.forEach.call(po.querySelectorAll('.pz.rv'), function (x) { x.classList.remove('rv'); });
    var b = po.querySelector('[data-polock]'); if (b) { b.setAttribute('aria-pressed', on ? 'true' : 'false'); b.textContent = on ? '🔓 Unlock' : '🔒 Lock'; }
    count(po);
  }
  P.setLock = setLock;
  P.setSprint = function (po, on) { po.classList.toggle('sprint', on); var b = po.querySelector('[data-posprint]'); if (b) b.setAttribute('aria-pressed', on ? 'true' : 'false'); };
  P.refresh = function (root) { Array.prototype.forEach.call((root || document).querySelectorAll('.po'), function (po) { setLock(po, po.classList.contains('lock')); }); };
  var walkT = null;
  function stopWalk() { if (walkT) { clearInterval(walkT); walkT = null; } Array.prototype.forEach.call(document.querySelectorAll('.po.walking'), function (po) { po.classList.remove('walking'); Array.prototype.forEach.call(po.querySelectorAll('.on'), function (z) { z.classList.remove('on'); }); var b = po.querySelector('[data-poplay]'); if (b) b.textContent = '▶ Walk it'; }); }
  P.stopWalk = stopWalk;
  function walk(po) {
    stopWalk();
    var zs = Array.prototype.slice.call(po.querySelectorAll('[data-ord]')).sort(function (a, b) { var x = a.dataset.ord, y = b.dataset.ord; return (x === 'c' ? 1.5 : +x) - (y === 'c' ? 1.5 : +y); });
    if (!zs.length) return;
    var i = 0, b = po.querySelector('[data-poplay]'); if (b) b.textContent = '❚❚ Stop';
    po.classList.add('walking');
    var step = function () {
      if (!document.body.contains(po)) return stopWalk();
      zs.forEach(function (z, k) { z.classList.toggle('on', k === i); });
      try { zs[i].scrollIntoView({block: 'nearest', behavior: 'smooth'}); } catch (e) {}
      i++; if (i > zs.length) stopWalk();
    };
    step(); walkT = setInterval(step, 2600);
  }
  document.addEventListener('click', function (e) {
    var t = e.target; if (!t || !t.closest) return;
    var po = t.closest('.po'); if (!po) return;
    if (t.closest('[data-polock]')) { e.preventDefault(); var on = !po.classList.contains('lock'); setLock(po, on); P.lockOn = on; if (P.onLock) P.onLock(on); return; }
    if (t.closest('[data-poplay]')) { e.preventDefault(); if (po.classList.contains('walking')) stopWalk(); else walk(po); return; }
    var sp = t.closest('[data-posprint]'); if (sp) { e.preventDefault(); var on2 = !po.classList.contains('sprint'); P.setSprint(po, on2); if (P.onSprint) P.onSprint(on2); return; }
    var pz = t.closest('.pz');
    if (pz && po.classList.contains('lock')) { e.preventDefault(); pz.classList.toggle('rv'); count(po); return; }
    if (po.classList.contains('walking') && !t.closest('button,a,input,select')) stopWalk();
  });
  function visiblePoster() {
    var list = Array.prototype.slice.call(document.querySelectorAll('.po')), vh = window.innerHeight || 800, best = null, bs = -1;
    list.forEach(function (po) { var r = po.getBoundingClientRect(); var vis = Math.min(vh, r.bottom) - Math.max(0, r.top); if (r.width && vis > bs) { bs = vis; best = po; } });
    return bs > 40 ? best : null;
  }
  document.addEventListener('keydown', function (e) {
    var tg = e.target;
    if (e.metaKey || e.ctrlKey || e.altKey || (tg && (/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName) || tg.isContentEditable))) return;
    var k = (e.key || '').toLowerCase(); if (k !== 'l' && k !== 'n') return;
    if (document.querySelector('.overlay:not([hidden])')) return;
    var po = visiblePoster(); if (!po) return;
    if (k === 'l') { e.preventDefault(); e.stopPropagation(); var on = !po.classList.contains('lock'); setLock(po, on); P.lockOn = on; if (P.onLock) P.onLock(on); }
    else if (po.classList.contains('lock')) { var nx = po.querySelector('.pz:not(.rv)'); if (nx) { e.preventDefault(); e.stopPropagation(); nx.classList.add('rv'); try { nx.scrollIntoView({block: 'nearest'}); } catch (er) {} count(po); } }
  }, true);

  /* ---------- styles ---------- */
  var css = '.po{--po-cause:#7b5ea7;--po-who:#b26a00;--po-spot:#0f766e;--po-test:#2f6fd6;--po-treat:#16865a;--po-watch:#c93a3a;--po-vs:#5b6b7a;--po-pill:#f6e3bd;--po-pill-b:#b26a00;--po-on:#fff;container-type:inline-size;border:1px solid var(--line);border-radius:14px;background:var(--surface-2,var(--surface));padding:10px;display:flex;flex-direction:column;gap:10px;min-width:0}' +
    '@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .po{--po-cause:#b49ae0;--po-who:#f0b04a;--po-spot:#3cc7b2;--po-test:#7aa6ff;--po-treat:#3ccf8e;--po-watch:#ff7070;--po-vs:#a7b6c4;--po-pill:#3a2a10;--po-pill-b:#f0b04a;--po-on:#0d1416}}' +
    ':root[data-theme="dark"] .po{--po-cause:#b49ae0;--po-who:#f0b04a;--po-spot:#3cc7b2;--po-test:#7aa6ff;--po-treat:#3ccf8e;--po-watch:#ff7070;--po-vs:#a7b6c4;--po-pill:#3a2a10;--po-pill-b:#f0b04a;--po-on:#0d1416}' +
    '.po-bar{display:flex;flex-wrap:wrap;gap:6px 10px;align-items:center;justify-content:space-between}.po-tt{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px;min-width:0}.po-tt>b{font-family:var(--f-display);font-size:1.15rem;line-height:1.2}.po-badge{font-size:1.1rem}.po-sub{color:var(--muted);font-size:.86rem}' +
    '.po-tools{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.po-b{font:inherit;font-size:.8rem;font-weight:700;border:1px solid var(--line);background:var(--surface);color:var(--ink);border-radius:999px;padding:4px 11px;cursor:pointer;min-height:30px}.po-b[aria-pressed="true"]{background:var(--po-pill);border-color:var(--po-pill-b)}.po-cnt{font-family:var(--f-mono);font-size:.72rem;color:var(--muted)}' +
    '.po-z{background:var(--surface);border:1px solid var(--line);border-top:4px solid var(--z);border-radius:12px;padding:8px 10px 10px;min-width:0;transition:opacity .3s,box-shadow .3s}.po-z h4{margin:0 0 6px;font-size:.78rem;letter-spacing:.04em;text-transform:uppercase;color:var(--z);display:flex;align-items:center;gap:6px;font-family:var(--f-mono)}.po-z h4 i{font-style:normal;min-width:20px;height:20px;border-radius:10px;background:var(--z);color:var(--po-on);display:inline-grid;place-items:center;font-size:.72rem;padding:0 4px}.po-z h4 em{margin-left:auto;font-style:normal;color:var(--muted);font-size:.72rem}' +
    '.po-grid{display:grid;gap:10px;grid-template-columns:1fr;grid-template-areas:"z1" "zc" "z2" "z3" "z4" "z5" "z6"}.po-grid .z1{grid-area:z1}.po-grid .zc{grid-area:zc}.po-grid .z2{grid-area:z2}.po-grid .z3{grid-area:z3}.po-grid .z4{grid-area:z4}.po-grid .z5{grid-area:z5}.po-grid .z6{grid-area:z6}' +
    '@container (min-width:560px){.po-grid{grid-template-columns:1fr 1fr;grid-template-areas:"z1 zc" "z2 zc" "z3 z4" "z5 z6"}.po-cond.nov .po-grid{grid-template-areas:"z1 zc" "z2 zc" "z3 z4" "z5 z5"}}' +
    '@container (min-width:900px){.po-cond .po-body{flex-basis:132px;width:132px}.po-cond .po-head{flex-basis:150px;width:150px}.po-grid{grid-template-columns:1fr 1.2fr 1fr;grid-template-areas:"z1 zc z2" "z6 zc z3" "z5 z4 z4"}.po-cond.nov .po-grid{grid-template-areas:"z1 zc z2" "z5 zc z3" "z5 z4 z4"}}' +
    '.po-cause{display:flex;gap:8px;align-items:flex-start}.po-orgf{margin:0;flex:0 0 96px;text-align:center}.po-org{width:96px;height:auto}.po-orgf figcaption{font-size:.68rem;color:var(--po-watch);font-weight:700;line-height:1.2}' +
    '.po-chain{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:0;flex:1;min-width:0}.po-chain li{font-weight:700;line-height:1.3;font-size:.9rem}.po-chain li+li:before{content:"↓";display:block;color:var(--po-watch);font-weight:800;margin:1px 0}.po-chain li.end{color:var(--po-watch)}' +
    '.po-spot{display:flex;gap:8px;align-items:flex-start}.po-body{flex:0 0 112px;width:112px;height:auto}.po-head{flex-basis:132px;width:132px}.po-pin{fill:var(--po-watch);stroke:var(--surface);stroke-width:1.5}.po-pn{fill:var(--po-on);font:800 9px var(--f-body,sans-serif)}' +
    '.po-signs{margin:0;padding:0;list-style:none;counter-reset:s;display:flex;flex-direction:column;gap:6px;flex:1;min-width:0}.po-signs li{counter-increment:s;display:grid;grid-template-columns:20px minmax(0,1fr);gap:6px;font-weight:700;font-size:.9rem;line-height:1.3}.po-signs li:before{content:counter(s);width:18px;height:18px;border-radius:9px;background:var(--po-watch);color:var(--po-on);font-size:.7rem;display:grid;place-items:center;margin-top:1px}.po-pins li{font-weight:400}.po-pins li>b{display:block}.po-pins li>span{color:var(--muted);font-size:.86rem;grid-column:2}' +
    '.po-who .po-big{display:block;font-family:var(--f-display);font-size:1.25rem;color:var(--po-who);line-height:1.2;margin-bottom:6px}.po-chips{display:flex;flex-wrap:wrap;gap:5px}.po-chips>span{border:1px solid var(--line);border-radius:999px;padding:2px 9px;font-size:.84rem;background:var(--surface-2,var(--surface))}' +
    '.po-tests,.po-watch,.po-items{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:7px}.po-tests li{line-height:1.3;font-size:.9rem}.po-tests li>b{display:block}.po-tests li>span{display:block;color:var(--ink)}.po-tests li.gold>b{color:var(--po-test)}' +
    '.po-ladder{list-style:none;margin:0;padding:0;display:flex;flex-direction:column-reverse;gap:6px}.po-ladder li{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;align-items:start;margin-left:calc(var(--k) * 10px);border-left:3px solid var(--po-treat);background:var(--surface-2,var(--surface));border-radius:8px;padding:6px 8px;font-size:.9rem;line-height:1.3}.po-ladder li i{font-style:normal;font-weight:800;color:var(--po-treat)}.po-ladder li.top{border-left-width:5px;font-weight:700}' +
    '.po-note,.po-key{margin:6px 0 0;font-size:.74rem;color:var(--muted)}.po-key i{display:inline-block;width:9px;height:9px;border-radius:5px;margin:0 3px 0 6px;vertical-align:middle}' +
    '.po-watch li{display:grid;grid-template-columns:12px minmax(0,1fr);gap:8px;align-items:start;font-size:.9rem;line-height:1.3}.po-watch li>i{width:11px;height:11px;border-radius:6px;margin-top:4px}' +
    '.po-key i.u-e,.po-watch li.u-e>i{background:#d33}.po-key i.u-s,.po-watch li.u-s>i{background:#e8891c}.po-key i.u-u,.po-watch li.u-u>i{background:#d4b02c}.po-key i.u-c,.po-watch li.u-c>i{background:#8a5cc7}.po-key i.u-r,.po-watch li.u-r>i{background:#2e9e64}' +
    '.po-vs .po-axis{margin:0 0 6px;font-weight:700;font-size:.82rem;color:var(--po-vs)}.po-vs2{display:grid;grid-template-columns:1fr auto 1fr;gap:6px;align-items:stretch}.po-vs2>div{border:1px solid var(--line);border-radius:10px;padding:6px 8px;font-size:.88rem;line-height:1.3}.po-vs2>div>b{display:block;font-size:.8rem;color:var(--po-vs);margin-bottom:2px}.po-vsx{align-self:center;font-weight:800;color:var(--po-vs);font-size:.8rem}' +
    '.po-hook{display:flex;gap:8px;align-items:center;border-radius:12px;padding:10px 12px;background:var(--accent-soft,#d6f0eb);color:var(--ink);font-weight:700;font-size:1rem;line-height:1.35;border-left:5px solid var(--accent)}.po-hook i{font-style:normal;font-size:1.2rem}' +
    '.po.lock .pz:not(.rv){color:transparent!important;-webkit-text-fill-color:transparent;text-shadow:none;background:var(--po-pill);outline:1px dashed var(--po-pill-b);border-radius:6px;cursor:pointer;user-select:none}.po.lock .pz:not(.rv) *{color:transparent!important}.po.lock .pz.rv{background:color-mix(in srgb,var(--po-treat) 14%,transparent);border-radius:5px;cursor:pointer}.po.lock .pz{padding:0 2px;-webkit-box-decoration-break:clone;box-decoration-break:clone}' +
    '.po.walking [data-ord]:not(.on){opacity:.28}.po.walking [data-ord].on{box-shadow:0 0 0 3px var(--z,var(--accent))}' +
    '.po-cols{display:grid;gap:10px;grid-template-columns:1fr}@container (min-width:560px){.po-cols{grid-template-columns:repeat(min(var(--n),2),minmax(0,1fr))}}@container (min-width:900px){.po-cols{grid-template-columns:repeat(var(--n),minmax(0,1fr))}}' +
    '.po-items li{font-size:.9rem;line-height:1.35}.po-items li>b{color:var(--ink)}.po-inline{flex-direction:row;flex-wrap:wrap;gap:6px}.po-inline li{border:1px solid var(--line);border-radius:999px;padding:2px 10px}.po-sub2{margin:-2px 0 6px;color:var(--muted);font-size:.82rem}' +
    '.po-mxw{overflow-x:auto;border-radius:12px;border:1px solid var(--line);background:var(--surface)}.po-mx{border-collapse:collapse;width:100%;font-size:.86rem;min-width:520px}.po-mx th,.po-mx td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top;line-height:1.3}.po-mx thead th{background:var(--surface-2,var(--surface));font-size:.76rem;text-transform:uppercase;letter-spacing:.03em;color:var(--muted)}.po-mx tbody th{white-space:nowrap}' +
    '.po-foot{display:grid;gap:8px;grid-template-columns:repeat(auto-fit,minmax(200px,1fr))}.po-foot>div{background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:7px 10px;font-size:.88rem;line-height:1.35}.po-foot>div>b{display:block;font-size:.76rem;color:var(--muted);text-transform:uppercase;letter-spacing:.03em;margin-bottom:2px}' +
    '.po-fix{border:1px dashed var(--po-watch);border-radius:10px;padding:6px 10px;background:var(--surface)}.po-fix summary{cursor:pointer;font-weight:700;font-size:.88rem;color:var(--po-watch)}.po-fix ul{margin:6px 0 2px;padding-left:18px;font-size:.88rem;line-height:1.4}.po-src{margin:0;font-size:.74rem;color:var(--muted)}' +
    '.po-fig{margin:0;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:8px;text-align:center;overflow-x:auto}.po-fig svg{max-width:720px;min-width:540px;width:100%;height:auto}.po-fig text{fill:var(--ink);font:12px var(--f-body,sans-serif)}.po-fig .m{fill:var(--muted);font-size:10.5px}.po-fig .b{font-weight:700}.po-fig .w{fill:var(--po-on);font-weight:700}.po-fig .k{fill:#111}' +
    '.po-clock{display:flex;gap:3px;border-radius:999px;overflow:hidden;font-size:.72rem;font-weight:700}.po-clock span{background:var(--z);color:var(--po-on);padding:3px 8px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.po-clock b{font-family:var(--f-mono);margin-right:5px;font-weight:800}' +
    '.po-4{display:grid;gap:10px;grid-template-columns:1fr}@container (min-width:560px){.po-4{grid-template-columns:1fr 1fr}}' +
    '.po.sprint .q-tl,.po.sprint .q-tr,.po.sprint .q-bl{display:none}.po.sprint .po-4{grid-template-columns:1fr}.po .po-sprint{display:none}.po.sprint .po-sprint{display:block}.po.sprint .po-clock span:not(:last-child){opacity:.35}.po-b[data-posprint][aria-pressed="true"]{background:var(--po-pill);border-color:var(--po-pill-b)}' +
    '.po-props{display:flex;flex-wrap:wrap;gap:5px;align-items:center;background:var(--surface);border:1px solid var(--line);border-left:5px solid var(--po-who);border-radius:12px;padding:7px 10px;font-size:.86rem}.po-props>b{margin-right:4px;color:var(--po-who)}.po-props>span{border-radius:999px;padding:2px 9px;background:var(--surface-2,var(--surface));border:1px solid var(--line)}.po-props>i{font-style:normal;color:var(--muted)}' +
    '.po-rt,.po-2{display:grid;gap:10px;grid-template-columns:1fr}@container (min-width:620px){.po-rt{grid-template-columns:1.6fr 1fr}.po-2{grid-template-columns:1fr 1.4fr}}.po-say{margin:0;font-size:.92rem;line-height:1.45}' +
    '.po-frames{display:grid;gap:8px;grid-template-columns:1fr}.po-arrow{display:none}@container (min-width:700px){.po-frames{grid-template-columns:1fr auto 1fr auto 1fr;align-items:stretch}.po-arrow{display:grid;place-items:center;font-size:1.4rem;font-weight:800;color:var(--muted)}}.po-fail{margin:8px 0 0;padding:6px 8px;border-radius:8px;background:color-mix(in srgb,var(--po-watch) 12%,transparent);font-weight:700;font-size:.86rem;line-height:1.35}' +
    '.po-sprint{border:2px solid var(--po-who);border-radius:12px;padding:8px 10px;background:var(--surface)}.po-sprint b{color:var(--po-who)}.po-sprint ol{margin:6px 0 0;padding-left:20px;line-height:1.5}' +
    '.po-mxw,.po-fig{background:linear-gradient(to right,var(--surface) 30%,rgba(0,0,0,0)) left/24px 100% no-repeat local,linear-gradient(to left,var(--surface) 30%,rgba(0,0,0,0)) right/24px 100% no-repeat local,radial-gradient(farthest-side at 0 50%,rgba(0,0,0,.2),rgba(0,0,0,0)) left/10px 100% no-repeat scroll,radial-gradient(farthest-side at 100% 50%,rgba(0,0,0,.2),rgba(0,0,0,0)) right/10px 100% no-repeat scroll,var(--surface)}' +
    '@media (prefers-reduced-motion:reduce){.po-z{transition:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
})();
