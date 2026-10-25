/* medengine-OSCE v1.3: procedure, counselling, communication and imaging pictures. */
(function () {
  var d = DG.def, H = DG.H, S = H.svg, T = H.t, on = H.on;
  var box = function (x, y, w, h, txt, cls, hot, sz) { var lines = txt.split('|'); return '<g class="' + (hot == null ? '' : hot ? 'dg-on' : 'dg-off') + '"><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="9" class="' + (cls || 'dg-hl') + '"/>' + lines.map(function (l, k) { return T(x + w / 2, y + h / 2 - (lines.length - 1) * 6.5 + k * 13 + 4, l, k === 0 ? 'dg-tb' : '', 'middle', sz || 10.5); }).join('') + '</g>'; };

  /* ---------- procedures ---------- */
  d('bp', {t: 'Korotkoff: what you hear as the cuff comes down', caps: [
    '**Palpate first:** pump up until the radial pulse vanishes, about 150 here. That is your estimate.', '**Inflate 20 to 30 above it**, to 170 to 180, so a silent gap can\'t fool you.',
    '**Let it down 2 to 3 mmHg per second.**', '**First tapping sound = systolic**, Korotkoff 1: 140.', '**Sounds disappear = diastolic**, Korotkoff 5: 86.', 'Record to the nearest 2 mmHg: **140 over 86**, which arm, sitting.'],
    draw: function (i) {
      var X0 = 40, Y = function (p) { return 190 - p * 0.85; }, s = '';
      [0, 50, 100, 150, 200].forEach(function (p) { s += H.ln(X0, Y(p), 320, Y(p), 'dg-dash') + T(X0 - 6, Y(p) + 4, String(p), 'dg-tm', 'end'); });
      s += T(14, 18, 'mmHg', 'dg-tm');
      var wave = ''; for (var x = 60; x <= 316; x += 2) { var ph = (x % 26) / 26, v = 85 + 55 * Math.max(0, Math.sin(Math.PI * Math.min(1, ph * 2.4))) * (ph < 0.42 ? 1 : 0) + (ph >= 0.42 ? 10 * (1 - ph) : 0); wave += (x === 60 ? 'M' : 'L') + x + ' ' + Y(v).toFixed(1); }
      s += '<path d="' + wave + '" style="stroke:var(--bad);stroke-width:1.2;fill:none;opacity:.55"/>';
      var peak = i === 0 ? 150 : 176, tUp = 90, tEnd = [100, 110, 220, 250, 300, 316][i];
      var cuff = 'M60 ' + Y(0) + ' L' + tUp + ' ' + Y(peak);
      if (i >= 2) { var slope = (peak - 60) / (316 - tUp); cuff += ' L' + tEnd + ' ' + Y(peak - (tEnd - tUp) * slope).toFixed(1); }
      s += '<path d="' + cuff + '" class="dg-ar" style="stroke-width:3"/>';
      if (i === 0) s += H.tag(tUp + 6, Y(150) - 6, 'radial pulse gone ~150', 'w', 'start');
      var sys = tUp + (176 - 140) / ((176 - 60) / (316 - tUp)), dia = tUp + (176 - 86) / ((176 - 60) / (316 - tUp));
      if (i >= 3) { s += H.ln(sys, Y(140), sys, 196, 'dg-arr') + H.tag(sys, Y(140) - 10, 'K1: systolic 140', 'b', 'middle'); for (var k = sys; k < Math.min(dia, tEnd); k += 12) s += H.ln(k, 198, k, 206, 'dg-ln'); }
      if (i >= 4) s += H.ln(dia, Y(86), dia, 196, 'dg-arr') + H.tag(dia, Y(86) - 10, 'K5: gone, diastolic 86', 'b', 'middle');
      s += T(180, 220, 'taps you hear', 'dg-tm', 'middle');
      return S(330, 226, s, 'Korotkoff sounds');
    }});
  d('moments', {t: 'The 5 moments for hand hygiene', caps: [
    '**1 · Before touching a patient.**', '**2 · Before a clean or aseptic procedure.**', '**3 · After body fluid exposure risk.**', '**4 · After touching a patient.**', '**5 · After touching the patient\'s surroundings.**'],
    draw: function (i) {
      var s = '<circle cx="150" cy="112" r="96" class="dg-dash"/>' + H.r(110, 92, 80, 46, 'dg-skin', 10) + H.c(126, 106, 10, 'dg-skin') + T(150, 160, 'patient zone', 'dg-tm', 'middle');
      var P = [[48, 112, 'Before|touching'], [150, 20, 'Before|clean task'], [250, 60, 'After|body fluid'], [252, 164, 'After|touching'], [150, 204, 'After|surroundings']];
      P.forEach(function (p, k) { s += '<g class="' + on(k === i) + '"><circle cx="' + p[0] + '" cy="' + p[1] + '" r="22" class="dg-pt dg-on"/>' + T(p[0], p[1] + 5, String(k + 1), '', 'middle', 15, ' style="fill:var(--on-accent);font-weight:700"') + '</g>'; });
      return S(300, 228, s, 'Five moments');
    }});
  d('ecg12', {t: '12-lead ECG: where each sticker goes', caps: [
    'Find the **sternal angle**: the bump where the 2nd rib joins. The space below it is the 2nd space; count down to the 4th.', '**V1 and V2:** 4th space, either side of the sternum.',
    '**V4:** 5th space, **midclavicular line**. Place it before V3.', '**V3:** halfway between V2 and V4.', '**V5 and V6:** level with V4, in the anterior and mid-axillary lines.',
    '**Limbs, clockwise from the right arm: Ride Your Green Bike.** Red right arm, Yellow left arm, Green left leg, Black right leg. On wrists and ankles.'],
    draw: function (i) {
      var s = H.torso(40, 20, 240, 200) + H.r(153, 32, 14, 104, 'dg-thin', 4);
      [52, 66, 80, 94, 108].forEach(function (y, k) { s += H.p('M152 ' + y + ' Q120 ' + (y - 6) + ' 74 ' + (y + 8), 'dg-thin') + H.p('M168 ' + y + ' Q200 ' + (y - 6) + ' 246 ' + (y + 8), 'dg-thin'); });
      s += H.ln(204, 60, 204, 180, 'dg-dash') + T(206, 190, 'midclavicular', 'dg-tm', 'middle');
      if (i === 0) s += H.arrow(196, 26, 168, 42, 'dg-arr') + H.tag(198, 22, 'sternal angle → 2nd rib', 'b', 'start');
      var V = [[148, 87, 'V1', 1], [172, 87, 'V2', 1], [204, 102, 'V4', 2], [188, 96, 'V3', 3], [230, 104, 'V5', 4], [252, 106, 'V6', 4]];
      V.forEach(function (v) { if (i >= v[3]) s += '<g class="' + (i === v[3] ? 'dg-on' : '') + '"><circle cx="' + v[0] + '" cy="' + v[1] + '" r="7" class="dg-pt dg-on"/>' + T(v[0], v[1] - 10, v[2], 'dg-ta', 'middle', 10) + '</g>'; });
      if (i === 5) [[70, 40, '#d33', 'R'], [250, 40, '#e6c229', 'Y'], [230, 214, '#2e9e44', 'G'], [90, 214, '#222', 'B']].forEach(function (l) { s += '<circle cx="' + l[0] + '" cy="' + l[1] + '" r="10" fill="' + l[2] + '" stroke="#fff"/>' + T(l[0], l[1] + 4, l[3], '', 'middle', 10, ' style="fill:#fff;font-weight:700"'); });
      return S(320, 228, s, 'ECG electrode placement');
    }});
  d('ecg3', {t: '3-lead monitor: Ride Your Green', caps: ['**Red** below the **right** collarbone.', '**Yellow** below the **left** collarbone.', '**Green** on the lower left chest.', 'Choose **lead II** to see the rhythm; set the alarms.'],
    draw: function (i) {
      var s = H.torso(40, 20, 220, 196) + H.p('M80 36 Q115 42 144 46 M156 46 Q185 42 220 36', 'dg-ln');
      [[100, 54, '#d33', 'R'], [200, 54, '#e6c229', 'Y'], [206, 170, '#2e9e44', 'G']].forEach(function (l, k) { s += '<g class="' + on(i >= k) + '"><circle cx="' + l[0] + '" cy="' + l[1] + '" r="11" fill="' + l[2] + '" stroke="#fff"/>' + T(l[0], l[1] + 4, l[3], '', 'middle', 11, ' style="fill:#fff;font-weight:700"') + '</g>'; });
      if (i === 3) s += H.arrow(108, 60, 198, 162) + H.tag(150, 128, 'lead II', '', 'middle');
      return S(300, 222, s, '3-lead placement');
    }});
  var PADS = [['Leucocytes', '2 min'], ['Nitrite', '60 s'], ['Urobilinogen', '60 s'], ['Protein', '60 s'], ['pH', '60 s'], ['Blood', '60 s'], ['Specific gravity', '45 s'], ['Ketones', '40 s'], ['Bilirubin', '30 s'], ['Glucose', '30 s']];
  d('dip', {t: 'Urine dipstick: patterns, not single pads', caps: [
    'Read **each pad at its own time** against the chart on the bottle: glucose first at 30 seconds, leucocytes last at 2 minutes.',
    '**Leucocytes + nitrites** with symptoms = **UTI**. Nitrites are the specific one.', '**Blood + protein** = think **kidney**: send an ACR, U&E, and look for hypertension.', '**Glucose + ketones** = **DKA** until proven otherwise: check capillary ketones now.'],
    draw: function (i) {
      var s = H.r(10, 110, 310, 22, 'dg-skin', 4) + H.r(10, 110, 26, 22, 'dg-mut', 4), x0 = 44;
      var pos = [[], [0, 1], [3, 5], [7, 9]][i];
      PADS.forEach(function (p, k) { var x = x0 + k * 27, hot = pos.indexOf(k) >= 0; s += '<rect x="' + x + '" y="114" width="20" height="14" rx="2" fill="' + (hot ? '#7d3cff' : '#f1e8b8') + '" stroke="#999"/>'; s += '<text x="' + (x + 12) + '" y="104" font-size="9" text-anchor="start" transform="rotate(-60 ' + (x + 12) + ' 104)" class="' + (hot ? 'dg-ta' : 'dg-tm') + '">' + H.esc(p[0]) + '</text>'; if (i === 0) s += T(x + 10, 148, p[1], 'dg-tm', 'middle', 8.5); });
      s += H.tag(165, 172, ['read times', 'UTI', 'kidney', 'DKA'][i], i ? 'w' : '', 'middle');
      return S(330, 184, s, 'Urine dipstick');
    }});
  var GAU = [['14', '#f28c28', 300, 'Orange · major bleeding, resuscitation'], ['16', '#9aa0a6', 200, 'Grey · resuscitation, trauma'], ['18', '#2e9e44', 100, 'Green · the standard adult cannula: blood, CT contrast'], ['20', '#e86aa6', 60, 'Pink · routine fluids and drugs'], ['22', '#2f6fd6', 35, 'Blue · small or fragile veins']];
  d('cann', {t: 'Cannula sizes: smaller number, faster flow', caps: GAU.map(function (g) { return '**' + g[0] + ' G · ' + g[3] + '.** About ' + g[2] + ' ml a minute.'; }),
    draw: function (i) {
      var s = '';
      GAU.forEach(function (g, k) { var y = 18 + k * 36; s += '<g class="' + (k === i ? 'dg-on' : 'dg-off') + '"><rect x="10" y="' + y + '" width="30" height="24" rx="5" fill="' + g[1] + '"/>' + T(25, y + 16, g[0], '', 'middle', 11, ' style="fill:#fff;font-weight:700"') + '<rect x="50" y="' + (y + 6) + '" width="' + (g[2] * 0.7).toFixed(0) + '" height="12" rx="6" fill="' + g[1] + '" opacity=".75"/>' + T(56 + g[2] * 0.7, y + 16, '~' + g[2] + ' ml/min', 'dg-tm') + '</g>'; });
      return S(330, 196, s, 'Cannula gauges');
    }});
  var TUBES = [['Cultures', '#b9c2c9', 'Blood cultures: aerobic then anaerobic'], ['Light blue', '#7fc6ee', 'Citrate: clotting, D-dimer'], ['Gold', '#e2b13c', 'Serum: U&E, LFT, CRP, TFT'], ['Green', '#2e9e44', 'Heparin: some chemistry'], ['Purple', '#8a4fc0', 'EDTA: FBC, HbA1c'], ['Pink', '#ef86b5', 'EDTA: group and save, crossmatch'], ['Grey', '#8c9196', 'Fluoride: glucose, lactate']];
  d('draw', {t: 'Order of draw', caps: TUBES.map(function (t, k) { return '**' + (k + 1) + ' · ' + t[0] + ':** ' + t[2] + '.'; }),
    draw: function (i) {
      var s = '';
      TUBES.forEach(function (t, k) { var x = 14 + k * 44; s += '<g class="' + on(k <= i) + '">' + (k === 0 ? '<path d="M' + (x + 4) + ' 40 L' + (x + 4) + ' 30 L' + (x + 26) + ' 30 L' + (x + 26) + ' 40 L' + (x + 32) + ' 60 L' + (x + 32) + ' 130 Q' + (x + 32) + ' 140 ' + (x + 22) + ' 140 L' + (x + 8) + ' 140 Q' + (x - 2) + ' 140 ' + (x - 2) + ' 130 L' + (x - 2) + ' 60 Z" class="dg-skin"/>' : '<rect x="' + (x + 2) + '" y="40" width="26" height="100" rx="12" class="dg-skin"/>') + '<rect x="' + x + '" y="24" width="30" height="20" rx="4" fill="' + t[1] + '"/>' + T(x + 15, 160, String(k + 1), k === i ? 'dg-ta' : 'dg-tm', 'middle', 12) + '</g>'; });
      return S(330, 172, s, 'Order of draw');
    }});
  d('abg', {t: 'ABG: Allen\'s test, then the angle', caps: [
    '**Press on both** the radial and the ulnar artery.', 'Ask them to **clench the fist** a few times: the hand goes pale.', '**Release the ulnar side:** colour back within **10 seconds** = the hand has a backup supply. Safe.',
    'Wrist bent back over a rolled towel. Needle at **30 to 45 degrees**, about 2 cm above the crease, **pointing towards the pulse**.', '**Press for 5 minutes**, longer on anticoagulants. Expel air, run within 10 minutes.'],
    draw: function (i) {
      var pale = i === 1, s = '';
      s += '<path d="M10 80 L190 70 Q230 66 252 74 L300 78 Q312 92 300 108 L252 112 Q230 120 190 116 L10 126 Z" ' + (pale ? 'fill="#f3efe9" stroke="var(--muted)"' : 'class="dg-skin"') + '/>';
      if (i >= 2) s += '<path d="M190 70 Q230 66 252 74 L300 78 Q312 92 300 108 L252 112 Q230 120 190 116 Z" fill="#f0a6a0" opacity=".45"/>';
      s += H.p('M10 86 Q110 82 200 78', '').replace('class=""', 'style="stroke:var(--bad);stroke-width:2;fill:none"') + H.p('M10 118 Q110 116 200 110', '').replace('class=""', 'style="stroke:var(--bad);stroke-width:2;fill:none;opacity:.6"');
      s += T(14, 72, 'radial · thumb side', 'dg-tm') + T(14, 142, 'ulnar · little finger side', 'dg-tm') + H.ln(196, 66, 196, 122, 'dg-dash') + T(196, 60, 'wrist crease', 'dg-tm', 'middle');
      if (i <= 1) s += H.c(176, 80, 9, 'dg-wl') + H.c(176, 114, 9, 'dg-wl');
      if (i === 2) s += H.c(176, 80, 9, 'dg-wl') + H.tag(250, 150, 'pink in under 10 s', 'g', 'middle');
      if (i === 3) s += H.ln(110, 30, 168, 82, 'dg-ln') + H.ln(108, 28, 96, 18, 'dg-ln') + T(132, 24, '30 to 45°', 'dg-ta') + H.r(60, 128, 140, 14, 'dg-mut', 7) + T(130, 160, 'rolled towel', 'dg-tm', 'middle');
      if (i === 4) s += H.c(168, 82, 10, 'dg-bl') + H.tag(168, 40, 'press 5 minutes', 'b', 'middle');
      return S(320, 170, s, 'Arterial blood gas');
    }});

  /* ---------- counselling ---------- */
  var inh = function (x, col, lab) { return '<g><rect x="' + x + '" y="30" width="34" height="74" rx="8" fill="' + col + '"/><path d="M' + x + ' 92 L' + (x - 40) + ' 92 Q' + (x - 48) + ' 92 ' + (x - 48) + ' 104 L' + (x - 48) + ' 120 L' + (x + 34) + ' 120 L' + (x + 34) + ' 100" fill="' + col + '" opacity=".85"/><rect x="' + (x + 6) + '" y="18" width="22" height="16" rx="4" fill="#ddd"/>' + T(x + 4, 140, lab, 'dg-tb', 'middle', 11) + '</g>'; };
  d('inhcol', {t: 'Brown builds, blue rescues', caps: [
    '**Brown, the preventer:** a low-dose inhaled steroid. **Every day, even when well;** works over weeks. **Rinse and spit after.**',
    '**Blue, the reliever:** salbutamol opens the airways in minutes. **Using it more than 3 times a week = not controlled.**',
    '**MART:** one combination inhaler of steroid and formoterol used **both** as the daily preventer and for relief.', '**Call 999** if the blue isn\'t helping, they can\'t finish a sentence, or their lips turn blue.'],
    draw: function (i) {
      var s = '<g class="' + on(i === 0) + '">' + inh(80, '#8a5a2b', 'preventer') + '</g><g class="' + on(i === 1) + '">' + inh(180, '#2f6fd6', 'reliever') + '</g><g class="' + on(i === 2) + '">' + inh(280, '#7b4fb3', 'MART') + '</g>';
      if (i === 3) s += H.tag(170, 166, '999: blue not helping · can\'t speak · blue lips', 'b', 'middle');
      return S(330, 178, s, 'Inhaler colours');
    }});
  d('steroid', {t: 'Why steroids are never stopped suddenly', caps: [
    '**Take it in the morning with food:** it copies your body\'s own morning cortisol peak and protects the stomach.', 'After about 3 weeks, **your own cortisol switches off**, because the tablets are doing the job.',
    '**Stop suddenly = no steroid at all.** That can cause an **adrenal crisis**: collapse, vomiting, low blood pressure.', '**So we taper slowly** while your own cortisol comes back.', '**Carry the steroid card;** if you\'re ill with a fever, you may need a higher dose.'],
    draw: function (i) {
      var X = function (w) { return 40 + w * 26; }, Y = function (m) { return 170 - m * 7; }, s = '';
      s += H.ln(40, 170, 316, 170, 'dg-thin') + H.ln(40, 20, 40, 170, 'dg-thin') + T(178, 190, 'weeks', 'dg-tm', 'middle') + T(10, 18, 'dose', 'dg-tm');
      var drug = 'M' + X(0) + ' ' + Y(15) + ' L' + X(4) + ' ' + Y(15);
      if (i === 2) drug += ' L' + X(4) + ' ' + Y(0);
      if (i >= 3) drug += ' L' + X(4) + ' ' + Y(12.5) + ' L' + X(5) + ' ' + Y(12.5) + ' L' + X(5) + ' ' + Y(10) + ' L' + X(6) + ' ' + Y(10) + ' L' + X(6) + ' ' + Y(7.5) + ' L' + X(7) + ' ' + Y(7.5) + ' L' + X(7) + ' ' + Y(5) + ' L' + X(8) + ' ' + Y(5) + ' L' + X(8) + ' ' + Y(2.5) + ' L' + X(9) + ' ' + Y(2.5) + ' L' + X(9) + ' ' + Y(0);
      s += '<path d="' + drug + '" class="dg-ar" style="stroke-width:3"/>';
      if (i >= 1) s += '<path d="M' + X(0) + ' ' + Y(8) + ' Q' + X(2) + ' ' + Y(8) + ' ' + X(3) + ' ' + Y(1) + ' L' + X(i >= 3 ? 6 : 4) + ' ' + Y(1) + (i >= 3 ? ' Q' + X(8) + ' ' + Y(2) + ' ' + X(10) + ' ' + Y(8) : '') + '" class="dg-dash" style="stroke:var(--warn);stroke-width:2"/>' + T(X(1), Y(9) - 4, 'your own cortisol', 'dg-tm');
      if (i === 2) s += H.tag(X(4) + 6, Y(4), 'adrenal crisis', 'b', 'start');
      if (i === 0) s += T(X(2), Y(16) - 6, '☀️ morning, with food', 'dg-ta', 'middle');
      if (i === 4) s += H.tag(X(7), 40, '🪪 steroid card · sick-day rule', 'w', 'middle');
      return S(330, 198, s, 'Steroid taper');
    }});
  d('htnsteps', {t: 'Hypertension drugs: NICE steps', caps: [
    '**Step 1, A:** an ACE inhibitor or ARB if **under 55 and not of Black African or African-Caribbean origin**, or **any age with type 2 diabetes**.',
    '**Step 1, C:** a calcium channel blocker if **55 or over**, or of **Black African or African-Caribbean origin** without diabetes.',
    '**Step 2:** add the other, or a thiazide-like diuretic such as indapamide. In Black adults add an ARB rather than an ACE inhibitor.',
    '**Step 3: A + C + D.**', '**Step 4:** check adherence and postural BP. **Potassium 4.5 or less → spironolactone; over 4.5 → alpha or beta blocker.** Seek advice.'],
    draw: function (i) {
      var s = '';
      s += box(6, 8, 170, 58, 'A: ACE inhibitor or ARB|under 55, or type 2 diabetes', 'dg-hl', i === 0, 9.5);
      s += box(184, 8, 170, 58, 'C: calcium channel blocker|55+, or Black African or Caribbean', 'dg-hl', i === 1, 9.5);
      s += H.arrow(91, 68, 160, 90) + H.arrow(269, 68, 200, 90);
      s += box(80, 92, 200, 40, 'Step 2|A + C, or add D', 'dg-hl', i === 2, 9.5);
      s += H.arrow(180, 134, 180, 146) + box(80, 148, 200, 34, 'Step 3: A + C + D', 'dg-hl', i === 3, 9.5);
      s += H.arrow(180, 184, 180, 196) + box(6, 198, 348, 44, 'Step 4: check adherence|K 4.5 or less: spironolactone · over 4.5: alpha or beta blocker', 'dg-wl', i === 4, 9.5);
      return S(360, 248, s, 'Hypertension steps');
    }});
  d('hfpillars', {t: 'Heart failure: 4 pillars to live longer, 1 drug for the fluid', caps: [
    '**A · ACE inhibitor**, or sacubitril-valsartan: watch kidneys, potassium, cough.', '**B · Beta-blocker** such as bisoprolol: start low, go slow; tired at first.', '**M · MRA** such as spironolactone: potassium checks.',
    '**S · SGLT2 inhibitor** such as dapagliflozin: more urine, thrush, sick-day rule.', '**Furosemide** is for the **fluid** and the breathlessness, not for survival. Take it in the morning.', '**Weigh every morning:** up **2 kg in 3 days** = call.'],
    draw: function (i) {
      var s = '<path d="M40 50 L170 14 L300 50 Z" class="dg-hl"/>' + T(170, 42, 'live longer', 'dg-tb', 'middle', 12);
      ['A', 'B', 'M', 'S'].forEach(function (l, k) { var x = 54 + k * 62; s += '<g class="' + on(i === k || i > 5) + '"><rect x="' + x + '" y="54" width="44" height="100" rx="6" class="dg-wl"/>' + T(x + 22, 110, l, 'dg-tb', 'middle', 22) + '</g>'; });
      s += H.r(40, 156, 260, 10, 'dg-mut', 4);
      s += '<g class="' + on(i === 4) + '"><path d="M318 96 Q306 116 306 128 Q306 144 318 144 Q330 144 330 128 Q330 116 318 96 Z" fill="#3b8fd8"/>' + T(318, 166, 'fluid', 'dg-tm', 'middle') + '</g>';
      if (i === 5) s += H.tag(170, 186, '⚖️ +2 kg in 3 days → call', 'w', 'middle');
      return S(340, 196, s, 'Heart failure pillars');
    }});
  d('apsy', {t: 'Antipsychotic side effects: the 4 Ms', caps: [
    '**Metabolic:** weight, sugar, cholesterol. Check weight, glucose and lipids at the start, 12 weeks, then yearly.', '**Movement:** stiffness, tremor, restlessness, abnormal mouth movements later on.',
    '**Milk:** high prolactin: breast changes, periods stop, sexual problems.', '**Mortal: NMS.** Fever, rigid muscles, confusion → emergency.', '**Clozapine: sore throat or fever → blood count today.** Constipation must be reported.'],
    draw: function (i) {
      var s = H.body(150, 8, 214), k = 1.07, X = function (v) { return 150 + v * k; }, Y = function (v) { return 8 + v * k; };
      var spot = [[0, 98, 22, 'belly'], [-38, 104, 10, 'hands'], [0, 60, 14, 'chest'], [0, 16, 14, 'brain'], [0, 34, 9, 'throat']][i];
      s += '<circle cx="' + X(spot[0]) + '" cy="' + Y(spot[1]) + '" r="' + spot[2] + '" class="' + (i === 3 || i === 4 ? 'dg-bl' : 'dg-wl') + '"/>';
      s += H.tag(250, 40, ['Metabolic', 'Movement', 'Milk', 'Mortal: NMS', 'Clozapine'][i], i >= 3 ? 'b' : 'w', 'middle');
      return S(300, 236, s, 'Antipsychotic side effects');
    }});
  d('ssri', {t: 'Antidepressants: 2 weeks, 6 months, 4 weeks', caps: [
    '**Weeks 0 to 2:** side effects come first: sickness, upset stomach, feeling more anxious. They usually settle.', '**Weeks 2 to 4:** the benefit starts. Review at 2 weeks, or 1 week if under 25.',
    '**Keep going for at least 6 months after you feel well,** to stop it coming back.', '**Stop slowly over at least 4 weeks:** not addictive, but stopping suddenly causes dizziness and electric-shock feelings.'],
    draw: function (i) {
      var s = H.ln(20, 120, 320, 120, 'dg-thin') + T(30, 140, '0', 'dg-tm', 'middle') + T(80, 140, '2 wk', 'dg-tm', 'middle') + T(130, 140, '4 wk', 'dg-tm', 'middle') + T(250, 140, 'well + 6 months', 'dg-tm', 'middle');
      s += '<g class="' + on(i === 0) + '">' + H.r(30, 60, 50, 24, 'dg-wl', 6) + T(55, 76, 'side effects', 'dg-tm', 'middle', 9) + '</g>';
      s += '<g class="' + on(i === 1) + '"><path d="M80 116 L130 70 L130 116 Z" class="dg-hl"/>' + T(120, 60, 'benefit', 'dg-ta', 'middle') + '</g>';
      s += '<g class="' + on(i === 2) + '">' + H.r(130, 70, 140, 46, 'dg-hl', 4) + T(200, 98, 'keep taking it', 'dg-tb', 'middle') + '</g>';
      s += '<g class="' + on(i === 3) + '"><path d="M270 70 L270 82 L282 82 L282 94 L294 94 L294 106 L306 106 L306 116" class="dg-ar" style="stroke-width:3"/>' + T(290, 60, 'taper', 'dg-ta', 'middle') + '</g>';
      return S(330, 150, s, 'Antidepressant timeline');
    }});
  d('hypo', {t: 'Hypo: 15 and 15', caps: ['**Under 4 = hypo.** Shaky, sweaty, hungry, confused.', '**15 to 20 g of fast sugar:** 4 to 5 glucose tablets or 150 to 200 ml of fruit juice.', '**Wait 15 minutes.**', '**Recheck.** Still under 4? Repeat, up to 3 times.', '**Over 4:** a starchy snack or the next meal. If unconscious: recovery position, **glucagon**, 999. Nothing by mouth.'],
    draw: function (i) {
      var P = [[160, 28, 'Under 4'], [264, 110, '15 to 20 g|fast sugar'], [160, 192, 'Wait|15 min'], [56, 110, 'Recheck']], s = '';
      for (var k = 0; k < 4; k++) { var a = P[k], b = P[(k + 1) % 4]; s += '<path d="M' + a[0] + ' ' + a[1] + ' Q' + (k === 0 ? '250 30' : k === 1 ? '250 190' : k === 2 ? '70 190' : '70 30') + ' ' + b[0] + ' ' + b[1] + '" class="dg-dash"/>'; }
      P.forEach(function (p, k) { s += box(p[0] - 50, p[1] - 20, 100, 40, p[2], k === i ? 'dg-wl' : 'dg-hl', k === i || i === 4); });
      if (i === 4) s += H.tag(160, 112, 'over 4 → starchy snack', 'g', 'middle');
      return S(320, 220, s, 'Hypo treatment cycle');
    }});
  d('levo', {t: 'Levothyroxine: empty, early, alone', caps: ['**On waking:** levothyroxine with water, on an empty stomach.', '**Wait 30 to 60 minutes** before breakfast, tea or coffee.', '**Breakfast.**', '**4 hours later:** iron, calcium, antacids. They block absorption.', '**Thyroid blood test 6 to 8 weeks** after starting or changing the dose.'],
    draw: function (i) {
      var s = H.ln(20, 100, 320, 100, 'dg-thin'), P = [[40, '06:30', '💊 + 💧'], [120, '', '⏳ 30 to 60 min'], [190, '07:30', '🍳 ☕'], [272, '11:30', 'iron, calcium']];
      P.forEach(function (p, k) { s += '<g class="' + on(k === i || i === 4) + '"><circle cx="' + p[0] + '" cy="100" r="8" class="dg-pt dg-on"/>' + T(p[0], 128, p[1], 'dg-tm', 'middle') + T(p[0], 78, p[2], 'dg-tb', 'middle', 11) + '</g>'; });
      if (i === 4) s += H.tag(170, 150, '🧪 TFTs at 6 to 8 weeks', 'w', 'middle');
      return S(330, 162, s, 'Levothyroxine timing');
    }});
  d('etoh', {t: 'Alcohol withdrawal clock: 6, 12, 24, 48', caps: ['**6 to 12 hours: shakes,** sweats, anxiety, nausea, fast pulse.', '**12 to 24 hours: sees things:** alcoholic hallucinosis.', '**24 to 48 hours: fits.**', '**48 to 72 hours: delirium tremens:** confused, terrified, fever, racing heart. An emergency.', '**A reducing course of chlordiazepoxide with thiamine** stops the climb.'],
    draw: function (i) {
      var s = H.ln(20, 140, 320, 140, 'dg-thin'), P = [[60, '6 h', '🫨', 'shakes'], [120, '12 h', '👁️', 'sees things'], [200, '24 h', '⚡', 'fits'], [280, '48 h', '🌀', 'DTs']];
      P.forEach(function (p, k) { var hot = k <= i && i < 4; s += '<g class="' + on(hot || i === 4) + '"><rect x="' + (p[0] - 6) + '" y="' + (140 - (k + 1) * 26) + '" width="12" height="' + ((k + 1) * 26) + '" rx="4" class="' + (k === 3 ? 'dg-bl' : 'dg-wl') + '"/>' + T(p[0], 160, p[1], 'dg-tm', 'middle') + T(p[0], 140 - (k + 1) * 26 - 22, p[2], '', 'middle', 18) + T(p[0], 140 - (k + 1) * 26 - 6, p[3], 'dg-tb', 'middle', 10) + '</g>'; });
      if (i === 4) s += H.p('M30 130 Q170 60 310 130', 'dg-ar') + H.tag(170, 182, 'chlordiazepoxide + thiamine', 'g', 'middle');
      return S(330, 192, s, 'Alcohol withdrawal');
    }});
  d('nsaid', {t: 'NSAIDs hit 3 organs: gut, kidney, heart', caps: ['**Gut:** indigestion, ulcers, bleeding. **Black stools or vomiting blood = urgent.**', '**Kidney:** injury, especially when dehydrated.', '**Heart:** heart attack and stroke risk, fluid and blood pressure.', '**Triple whammy: ACE inhibitor + diuretic + NSAID = kidney injury.**', '**A PPI before breakfast** protects the stomach. Lowest dose, shortest time, with food.'],
    draw: function (i) {
      var s = H.body(150, 8, 214), k = 1.07, X = function (v) { return 150 + v * k; }, Y = function (v) { return 8 + v * k; };
      s += '<g class="' + on(i === 0 || i === 4) + '"><ellipse cx="' + X(6) + '" cy="' + Y(82) + '" rx="13" ry="9" class="dg-bl"/></g>';
      s += '<g class="' + on(i === 1 || i === 3) + '"><ellipse cx="' + X(-12) + '" cy="' + Y(92) + '" rx="5" ry="8" class="dg-wl"/><ellipse cx="' + X(12) + '" cy="' + Y(92) + '" rx="5" ry="8" class="dg-wl"/></g>';
      s += '<g class="' + on(i === 2) + '"><circle cx="' + X(6) + '" cy="' + Y(60) + '" r="9" class="dg-bl"/></g>';
      if (i === 3) s += H.tag(150, 226, 'ACEi + diuretic + NSAID', 'b', 'middle');
      if (i === 4) s += H.tag(150, 226, 'PPI: 30 to 60 min before breakfast', 'g', 'middle');
      return S(300, 236, s, 'NSAID risks');
    }});
  d('afclot', {t: 'Why AF causes strokes', caps: ['In AF the top chambers **quiver instead of squeezing**.', 'Blood **pools** in a little pouch of the left atrium, the appendage.', 'Still blood **clots**.', 'A piece flicks out, up the arteries to the **brain: a stroke**.', 'An **anticoagulant** stops the clot forming: about **two thirds fewer strokes**.'],
    draw: function (i) {
      var s = '<path d="M100 70 Q90 40 130 40 Q150 40 160 56 Q172 38 196 40 Q236 44 226 90 Q216 150 160 186 Q104 150 96 100 Z" class="dg-skin"/>' + H.ln(160, 60, 160, 170, 'dg-thin') + H.ln(100, 96, 222, 96, 'dg-thin');
      s += T(126, 84, 'RA', 'dg-tm', 'middle') + T(196, 84, 'LA', 'dg-tm', 'middle') + T(130, 130, 'RV', 'dg-tm', 'middle') + T(190, 130, 'LV', 'dg-tm', 'middle');
      s += '<path d="M222 60 Q246 52 244 72 Q240 82 226 80" class="dg-skin"/>';
      if (i === 0) s += H.p('M110 70 q4 -6 8 0 q4 6 8 0 q4 -6 8 0 M176 70 q4 -6 8 0 q4 6 8 0 q4 -6 8 0', 'dg-ar');
      if (i === 1) s += '<path d="M226 64 Q240 60 238 72 Q234 78 228 76" class="dg-wl"/>';
      if (i >= 2 && i < 4) s += '<circle cx="234" cy="70" r="7" class="dg-red"/>';
      if (i === 3) s += H.p('M200 50 Q200 20 240 14', 'dg-arr') + '<ellipse cx="270" cy="22" rx="26" ry="18" class="dg-skin"/><circle cx="262" cy="20" r="6" class="dg-red"/>' + T(270, 50, 'brain', 'dg-tm', 'middle');
      if (i === 4) s += H.tag(250, 160, '2/3 fewer strokes', 'g', 'middle');
      return S(320, 196, s, 'AF and stroke');
    }});
  d('ltot', {t: 'Home oxygen: 15 hours, zero cigarettes, 3 metres', caps: ['**At least 15 hours a day, including overnight.** Fewer hours = no survival benefit.', '**No smoking or vaping**, by anyone nearby: oxygen makes things burn fiercely.', '**3 metres from naked flames:** gas hobs, candles, fires, birthday cakes.', '**No Vaseline or oil-based creams** on the face; use water-based gel. Free **fire service** home check.'],
    draw: function (i) {
      var s = '';
      var a = 15 / 24 * 2 * Math.PI, x = 70 + 46 * Math.sin(a), y = 90 - 46 * Math.cos(a);
      s += '<g class="' + on(i === 0) + '"><circle cx="70" cy="90" r="46" class="dg-skin"/><path d="M70 90 L70 44 A46 46 0 1 1 ' + x.toFixed(1) + ' ' + y.toFixed(1) + ' Z" class="dg-hl"/>' + T(70, 152, '15+ hours', 'dg-tb', 'middle') + '</g>';
      s += '<g class="' + on(i === 1) + '">' + T(170, 100, '🚭', '', 'middle', 40) + '</g>';
      s += '<g class="' + on(i === 2) + '">' + T(260, 70, '🔥', '', 'middle', 34) + H.arrow(200, 120, 300, 120) + H.arrow(300, 120, 200, 120) + T(250, 140, '3 m', 'dg-tb', 'middle') + '</g>';
      if (i === 3) s += H.tag(170, 172, 'water-based gel · fire service check', 'w', 'middle');
      return S(330, 184, s, 'Oxygen safety');
    }});
  d('people', {t: 'Risk in people, not percentages', caps: ['Imagine **100 people exactly like you**.', 'Over 10 years, about **14 of them** will have a heart attack or stroke. That is a QRISK of 14%.', 'If all 100 took a statin, about **4 or 5 of those 14 would be spared**.', 'So **86 were never going to**, 4 or 5 are helped, and about 9 still have one. **It\'s your choice.**'],
    draw: function (i) {
      var s = '';
      for (var n = 0; n < 100; n++) {
        var r = Math.floor(n / 10), c = n % 10, x = 20 + c * 27, y = 14 + r * 23, ev = n < 14, saved = n < 4 || n === 10;
        var col = i === 0 ? 'dg-mut' : !ev ? 'dg-mut' : i >= 2 && saved ? 'dg-grn' : 'dg-red';
        s += '<circle cx="' + x + '" cy="' + y + '" r="4.5" class="' + col + '"/><rect x="' + (x - 6) + '" y="' + (y + 5) + '" width="12" height="10" rx="4" class="' + col + '"/>';
      }
      return S(290, 248, s, '100 people');
    }});
  d('chunk', {t: 'Ask, Tell, Ask: chunk and check', caps: ['**Ask:** "What do you know so far? What are you worried about?"', '**Tell:** one chunk, 2 or 3 facts, in plain words. Draw it.', '**Ask:** "Does that make sense? What questions do you have?" Then loop.', '**Teach-back at the end:** "Could you tell me in your own words what you\'ll tell your family?"'],
    draw: function (i) {
      var s = '<circle cx="160" cy="108" r="70" class="dg-dash"/>' + T(160, 112, 'chunk and check', 'dg-tm', 'middle');
      [[160, 34, 'ASK'], [228, 150, 'TELL'], [92, 150, 'ASK']].forEach(function (p, k) { s += box(p[0] - 36, p[1] - 18, 72, 36, p[2], k === i ? 'dg-wl' : 'dg-hl', i === 3 || k === i); });
      s += H.arrow(200, 50, 222, 120) + H.arrow(190, 162, 132, 162) + H.arrow(90, 126, 124, 48);
      if (i === 3) s += H.tag(160, 206, 'teach-back', 'g', 'middle');
      return S(320, 214, s, 'Ask tell ask');
    }});
  var DUR = [['Middle ear infection', 7, 'About 3 days, up to a week'], ['Sore throat', 7, 'About a week'], ['Common cold', 10, 'About 10 days'], ['Sinusitis', 21, '2 to 3 weeks'], ['Cough or bronchitis', 21, 'Up to 3 weeks']];
  d('abxdays', {t: 'How long it usually lasts, with or without antibiotics', caps: DUR.map(function (x) { return '**' + x[0] + ':** ' + x[2] + '. Telling them this stops the "it\'s not going away" return visit.'; }),
    draw: function (i) {
      var s = '';
      DUR.forEach(function (x, k) { var y = 16 + k * 38; s += '<g class="' + (k === i ? 'dg-on' : 'dg-off') + '">' + T(10, y + 12, x[0], 'dg-tb', '', 11) + '<rect x="10" y="' + (y + 18) + '" width="' + (x[1] * 13) + '" height="12" rx="6" class="dg-hl"/>' + T(16 + x[1] * 13, y + 28, x[1] + ' days', 'dg-tm') + '</g>'; });
      return S(330, 210, s, 'Illness durations');
    }});
  d('risk3', {t: 'Risk has three directions', caps: ['**To self:** suicide, self-harm, self-neglect, vulnerability.', '**To others:** thoughts of harm, a named person, weapons, past violence, **children at home**, driving.', '**From others:** abuse, domestic violence, exploitation.', '**Static vs dynamic:** history can\'t change; symptoms, drugs, stress and access to means can. Treat the dynamic ones.', '**Formulate:** what could happen, to whom, how likely, how soon, and what makes it better or worse.'],
    draw: function (i) {
      var s = H.body(160, 60, 120);
      s += '<g class="' + on(i === 0) + '">' + H.p('M160 50 Q160 20 130 18 Q104 18 110 40', 'dg-arr') + T(80, 20, 'to self', 'dg-tr', 'end') + '</g>';
      s += '<g class="' + on(i === 1) + '">' + H.arrow(196, 110, 270, 80, 'dg-arr') + T(280, 72, 'to others', 'dg-tr') + '</g>';
      s += '<g class="' + on(i === 2) + '">' + H.arrow(60, 110, 128, 120, 'dg-arr') + T(14, 100, 'from others', 'dg-tr') + '</g>';
      if (i === 3) s += H.tag(160, 196, 'treat the dynamic factors', 'w', 'middle');
      if (i === 4) s += H.tag(160, 196, 'what · to whom · how likely · how soon', 'w', 'middle');
      return S(330, 206, s, 'Three directions of risk');
    }});

  /* ---------- imaging approaches ---------- */
  d('cxrsys', {t: 'Chest X-ray: Details, RIPE, ABCDE', caps: [
    '**Details:** name, date of birth, date, **PA or AP, erect or supine**. Heart size only counts on a PA film.', '**Rotation:** the spinous process sits halfway between the two clavicle heads.',
    '**Inspiration:** count **5 to 6 front ribs** above the diaphragm in the midclavicular line.', '**Airway:** trachea central; the carina below.', '**Breathing:** upper, middle and lower zones, **comparing sides**; pleura and costophrenic angles.',
    '**Cardiac:** heart width under half the chest width on a PA film. Borders: right atrium, left ventricle.', '**Diaphragm:** the right is usually higher; look **under** it for free air.', '**Everything else and review areas:** apices, hila, behind the heart, below the diaphragm; bones, lines and tubes.'],
    draw: function (i) {
      var base = DG.cxr ? DG.cxr('normal') : ''; if (!base) return '';
      var o = '', Y = '#f0b04a';
      if (i === 0) o += '<rect x="120" y="150" width="76" height="24" rx="4" fill="#222" stroke="' + Y + '"/><text x="158" y="166" fill="' + Y + '" font-size="9" text-anchor="middle">PA · erect · date</text>';
      if (i === 1) o += '<path d="M100 40 L72 34 M100 40 L128 34" stroke="' + Y + '" stroke-width="1.6"/><circle cx="100" cy="40" r="3" fill="' + Y + '"/>';
      if (i === 2) [44, 57, 70, 83, 96, 109].forEach(function (y, k) { o += '<text x="176" y="' + (y + 3) + '" fill="' + Y + '" font-size="9" font-weight="700">' + (k + 1) + '</text>'; });
      if (i === 3) o += '<rect x="90" y="18" width="20" height="62" fill="none" stroke="' + Y + '" stroke-width="2"/>';
      if (i === 4) o += '<path d="M30 70 L90 70 M110 70 L170 70 M30 100 L90 100 M110 100 L170 100" stroke="' + Y + '" stroke-dasharray="3 3"/><text x="4" y="58" fill="' + Y + '" font-size="8">upper</text><text x="4" y="88" fill="' + Y + '" font-size="8">middle</text><text x="4" y="118" fill="' + Y + '" font-size="8">lower</text>';
      if (i === 5) o += '<path d="M84 142 L157 142 M84 138 L84 146 M157 138 L157 146" stroke="' + Y + '" stroke-width="2"/><path d="M30 156 L172 156 M30 152 L30 160 M172 152 L172 160" stroke="' + Y + '" stroke-width="1.2"/><text x="100" y="172" fill="' + Y + '" font-size="9" text-anchor="middle">heart under half the chest</text>';
      if (i === 6) o += '<path d="M34 136 Q 60 110 88 128 M166 139 Q 140 112 112 129" stroke="' + Y + '" stroke-width="2.4" fill="none"/>';
      if (i === 7) [[44, 36], [154, 36], [80, 74], [120, 74], [120, 112], [60, 146], [140, 146]].forEach(function (p) { o += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="9" fill="none" stroke="' + Y + '" stroke-width="1.6"/>'; });
      return '<div class="dg-img" style="margin:0 auto">' + base.replace('</svg>', o + '</svg>') + '</div>';
    }});
  d('axr', {t: 'Small bowel vs large bowel: 3-6-9', caps: [
    '**Small bowel:** **central**, with lines **all the way across**: the valvulae conniventes. Dilated over **3 cm**.', '**Large bowel:** **around the edge**, with haustra **part-way across**. Dilated over **6 cm**, the caecum over **9 cm**.',
    '**Sigmoid volvulus:** a huge **coffee bean** arising from the left lower abdomen, pointing to the right upper.', '**Toxic megacolon:** transverse colon over 6 cm, haustra lost, thick wall, in colitis.', '**Rigler\'s sign:** both sides of the bowel wall visible = **free air**. Confirm with an erect chest film or CT.'],
    draw: function (i) { return '<div class="dg-img" style="max-width:260px;margin:0 auto">' + DG.axr(['sbo', 'lbo', 'volv', 'mega', 'rigler'][i]) + '</div>'; }});
  d('ctorient', {t: 'CT: you are standing at the feet, looking up', caps: ['The patient lies on their back; **you look up at them from their feet**.', 'So **their right is on your left**, and the front of the body is at the top of the image.', 'The liver, on their right, appears on **your left**; the spleen on your right.'],
    draw: function (i) {
      var s = '';
      if (i === 0) { s += H.r(20, 70, 190, 46, 'dg-skin', 22) + H.c(36, 93, 15, 'dg-skin') + T(110, 98, 'lying on their back', 'dg-tm', 'middle') + T(250, 100, '👁️', '', 'middle', 28) + H.arrow(236, 94, 214, 94) + T(250, 130, 'you, at the feet', 'dg-tm', 'middle'); return S(320, 180, s, 'CT orientation'); }
      s += '<ellipse cx="160" cy="96" rx="110" ry="74" class="dg-skin"/>' + T(46, 100, 'R', 'dg-tb', 'middle', 16) + T(274, 100, 'L', 'dg-tb', 'middle', 16) + T(160, 16, 'front', 'dg-tm', 'middle') + T(160, 186, 'back', 'dg-tm', 'middle');
      s += H.r(146, 140, 28, 24, 'dg-mut', 6);
      if (i === 2) s += '<path d="M64 76 Q80 40 136 42 Q150 74 130 110 Q96 120 66 110 Z" class="dg-wl"/>' + T(100, 86, 'liver', 'dg-tb', 'middle') + '<path d="M256 80 Q248 56 216 50 Q206 72 222 94 Q240 98 256 80 Z" class="dg-hl"/>' + T(234, 78, 'spleen', 'dg-tm', 'middle');
      return S(320, 194, s, 'Axial slice orientation');
    }});
  var HU = [['Air', '−1000', 0.04], ['Fat', '−100', 0.32], ['Water', '0', 0.44], ['Soft tissue', '+40', 0.54], ['Fresh blood', '+60', 0.62], ['Contrast', '+200', 0.78], ['Bone', '+1000', 0.96]];
  d('hu', {t: 'Black to white: what each shade is', caps: HU.map(function (h) { return '**' + h[0] + ':** about ' + h[1] + ' Hounsfield units.'; }),
    draw: function (i) {
      var id = H.uid(), s = '<defs><linearGradient id="' + id + '"><stop offset="0" stop-color="#000"/><stop offset="1" stop-color="#fff"/></linearGradient></defs><rect x="14" y="40" width="300" height="30" rx="6" fill="url(#' + id + ')" stroke="var(--muted)"/>';
      HU.forEach(function (h, k) { var x = 14 + h[2] * 300; s += H.ln(x, 72, x, k === i ? 86 : 78, k === i ? 'dg-ln' : 'dg-thin') + (k === i ? T(Math.min(290, Math.max(40, x)), 102, h[0], 'dg-tb', 'middle', 12) + T(Math.min(290, Math.max(40, x)), 118, h[1] + ' HU', 'dg-tm', 'middle', 10) : ''); });
      return S(330, 124, s, 'Hounsfield scale');
    }});
  d('ecgwave', {t: 'One heartbeat on the ECG', caps: [
    '**P wave:** the atria contracting. No P waves + irregular = AF.', '**PR interval: 120 to 200 ms,** 3 to 5 small squares. Longer = first-degree block; short with a slur = WPW.',
    '**QRS: under 120 ms,** 3 small squares. Wider = bundle branch block or ventricular origin.', '**ST segment:** should be flat. **Raised = injury, a STEMI.** Depressed = ischaemia.',
    '**T wave:** recovery. Tall tented = high potassium; inverted = ischaemia or strain.', '**QT:** start of QRS to the end of T. Corrected, under about 440 ms in men and 460 in women.'],
    draw: function (i) {
      var s = '', sq = 6, x0 = 20, y0 = 110;
      for (var x = 0; x <= 300; x += sq) s += '<line x1="' + (x0 + x) + '" y1="20" x2="' + (x0 + x) + '" y2="160" style="stroke:var(--bad);stroke-opacity:' + (x % 30 ? 0.12 : 0.3) + '"/>';
      for (var y = 20; y <= 160; y += sq) s += '<line x1="20" y1="' + y + '" x2="320" y2="' + y + '" style="stroke:var(--bad);stroke-opacity:' + ((y - 20) % 30 ? 0.12 : 0.3) + '"/>';
      var P = 'M20 110 L50 110 Q62 96 74 110 L96 110 L102 118 L112 40 L122 128 L128 110 L152 110 Q176 82 200 110 L320 110';
      s += '<path d="' + P + '" class="dg-ln" style="stroke-width:2.2"/>';
      var hl = [[50, 74, 'P'], [50, 102, 'PR'], [96, 128, 'QRS'], [128, 152, 'ST'], [152, 200, 'T'], [96, 200, 'QT']][i];
      s += '<rect x="' + hl[0] + '" y="24" width="' + (hl[1] - hl[0]) + '" height="132" class="dg-hl" style="stroke:none"/>' + H.tag((hl[0] + hl[1]) / 2, 172, hl[2], 'w', 'middle');
      return S(330, 186, s, 'PQRST');
    }});
  var LEADS = [['I', 'L'], ['aVR', 'R'], ['V1', 'S'], ['V4', 'A'], ['II', 'I'], ['aVL', 'L'], ['V2', 'S'], ['V5', 'L'], ['III', 'I'], ['aVF', 'I'], ['V3', 'A'], ['V6', 'L']];
  d('ecgterr', {t: 'The leads tell you the wall, the wall tells you the artery', caps: ['**Inferior: II, III, aVF → right coronary artery.** Watch for slow rhythms and right ventricular infarct.', '**Septal and anterior: V1 to V4 → LAD.** The big one.', '**Lateral: I, aVL, V5, V6 → circumflex.**', '**Posterior:** ST **depression** with tall R waves in V1 to V3 → record V7 to V9.', '**Axis:** look at I and aVF. Both up = normal. Leaving each other = left axis; reaching for each other = right axis.'],
    draw: function (i) {
      var hot = [['I'], ['S', 'A'], ['L'], ['S'], ['ax']][i], s = '';
      LEADS.forEach(function (l, k) { var x = 10 + (k % 4) * 78, y = 10 + Math.floor(k / 4) * 50, h = hot.indexOf(l[1]) >= 0 || (i === 4 && (l[0] === 'I' || l[0] === 'aVF')); s += '<rect x="' + x + '" y="' + y + '" width="70" height="42" rx="8" class="' + (h ? (i === 3 ? 'dg-bl' : 'dg-wl') : 'dg-skin') + '"/>' + T(x + 35, y + 26, l[0], h ? 'dg-tb' : 'dg-tm', 'middle', 13); });
      return S(330, 166, s, 'ECG territories');
    }});
})();
