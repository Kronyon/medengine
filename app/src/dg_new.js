/* medengine-OSCE v1.4: more pictures. History patterns, red flags, the neuro and MSK moves, hand and eye signs,
   procedure angles, ECG maths, insulin and drinks. Same rules: drawn here, step-through, labels on the picture. */
(function () {
  var d = DG.def, H = DG.H, S = H.svg, T = H.t, on = H.on;
  var box = function (x, y, w, h, txt, cls, hot, sz) { var L = txt.split('|'); return '<g class="' + (hot == null ? '' : hot ? 'dg-on' : 'dg-off') + '"><rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="9" class="' + (cls || 'dg-hl') + '"/>' + L.map(function (l, k) { return T(x + w / 2, y + h / 2 - (L.length - 1) * 6.5 + k * 13 + 4, l, k === 0 ? 'dg-tb' : '', 'middle', sz || 10.5); }).join('') + '</g>'; };

  /* ================= history patterns ================= */
  d('socrates', {t: 'SOCRATES: any pain, any station', cards: [
    ['📍', 'Site', '"Where exactly? Can you point with one finger?"'], ['⏱️', 'Onset', '"Did it come on suddenly or build up?" Sudden = vessel or perforation.'],
    ['🔪', 'Character', 'Crushing, tearing, burning, colicky, stabbing.'], ['➡️', 'Radiation', 'To the arm or jaw = heart; to the back = aorta or pancreas; loin to groin = stone.'],
    ['➕', 'Associated', 'Sweating, vomiting, fever, breathless, faint.'], ['📈', 'Timing', 'Constant or comes in waves? How long each time?'],
    ['⚖️', 'Exacerbating and relieving', 'Breathing, moving, eating, lying flat, sitting forward.'], ['🔢', 'Severity', '"Out of 10, with 10 the worst imaginable."']]});
  d('tunafish', {t: 'Back pain red flags: TUNA FISH', cards: [
    ['T', 'Trauma', 'Even minor, if osteoporotic.'], ['U', 'Unexplained weight loss', 'Think cancer.'], ['N', 'Neurology', '**Saddle numbness, bladder or bowel change, both legs weak = cauda equina: emergency MRI.**'],
    ['A', 'Age under 20 or over 50', 'New back pain at these ages is not "just mechanical".'], ['F', 'Fever', 'Discitis, epidural abscess.'], ['I', 'IV drug use', 'Infection.'],
    ['S', 'Steroid use', 'Osteoporotic fracture.'], ['H', 'History of cancer', '**Breast, lung, prostate, kidney, thyroid spread to bone.** Back pain + cancer = cord compression until proven otherwise.']]});
  d('sepsis', {t: 'Sepsis: spot it in 1 minute', cards: [
    ['🌡️', 'Is it infection?', 'Fever or very low temperature, a source.'], ['🧠', 'New confusion', 'A single red flag on its own.'], ['🫁', 'Breathing 25 or more', 'Or SpO2 needing new oxygen.'],
    ['💓', 'Pulse over 130, systolic 90 or less', ''], ['🔴', 'Non-blanching rash, mottled or ashen', ''], ['🚽', 'No urine for 18 hours', ''],
    ['⏱️', 'Sepsis six within 1 hour', '**Give 3:** oxygen, IV fluids, antibiotics. **Take 3:** blood cultures, lactate, urine output.']]});
  d('cage', {t: 'Alcohol: CAGE, then count the units', cards: [
    ['✂️', 'Cut down', '"Have you ever felt you should cut down?"'], ['😠', 'Annoyed', '"Have people annoyed you by criticising your drinking?"'], ['😔', 'Guilty', '"Have you felt guilty about it?"'],
    ['🌅', 'Eye-opener', '"Ever had a drink first thing to steady your nerves?" **2 or more yes = likely dependence.**'], ['🔢', 'Then units', 'Over 14 a week = above the low-risk limit; spread over 3 or more days.']]});
  d('units', {t: 'What is a unit? Roughly 2, 2, 1', caps: ['**A pint of 4% beer ≈ 2.3 units.**', '**A medium 175 ml glass of 13% wine ≈ 2.3 units.** A bottle ≈ 10.', '**A single 25 ml shot of spirits = 1 unit.**', '**A 500 ml can of 9% strong cider ≈ 4.5 units.** 3 litres of 7.5% cider = 22.5 units.', '**Units = % × volume in ml ÷ 1000.** Low-risk limit: 14 a week.'],
    draw: function (i) {
      var s = '';
      var glass = function (x, hot, h, w, fill, lab, u) { return '<g class="' + on(hot) + '"><path d="M' + (x - w / 2) + ' ' + (150 - h) + ' L' + (x - w / 2 + 4) + ' 150 L' + (x + w / 2 - 4) + ' 150 L' + (x + w / 2) + ' ' + (150 - h) + ' Z" class="dg-skin"/><path d="M' + (x - w / 2 + 2) + ' ' + (150 - h * 0.8) + ' L' + (x - w / 2 + 4) + ' 148 L' + (x + w / 2 - 4) + ' 148 L' + (x + w / 2 - 2) + ' ' + (150 - h * 0.8) + ' Z" fill="' + fill + '"/>' + T(x, 170, lab, 'dg-tm', 'middle') + T(x, 188, u, 'dg-tb', 'middle', 13) + '</g>'; };
      s += glass(50, i === 0 || i === 4, 90, 44, '#e3a72f', 'pint 4%', '2.3');
      s += '<g class="' + on(i === 1 || i === 4) + '"><path d="M106 70 Q106 104 126 106 Q146 104 146 70 Z" class="dg-skin"/><path d="M108 84 Q110 102 126 103 Q142 102 144 84 Z" fill="#8c1f3a"/><path d="M126 106 L126 146 M112 150 L140 150" class="dg-ln"/>' + T(126, 170, '175 ml 13%', 'dg-tm', 'middle') + T(126, 188, '2.3', 'dg-tb', 'middle', 13) + '</g>';
      s += glass(196, i === 2 || i === 4, 40, 30, '#d9c9a3', 'shot 40%', '1');
      s += '<g class="' + on(i === 3 || i === 4) + '"><rect x="248" y="66" width="40" height="84" rx="8" class="dg-skin"/><rect x="252" y="80" width="32" height="40" rx="4" fill="#5aa04a"/>' + T(268, 170, '500 ml 9%', 'dg-tm', 'middle') + T(268, 188, '4.5', 'dg-tb', 'middle', 13) + '</g>';
      if (i === 4) s += H.tag(160, 30, '% × ml ÷ 1000', 'w', 'middle');
      return S(320, 196, s, 'Alcohol units');
    }});
  d('chestpain', {t: 'Chest pain: the character points to the cause', caps: [
    '**Central, crushing, to the arm or jaw, sweaty** = ACS.', '**Tearing, straight through to the back**, unequal arm BPs = aortic dissection.', '**Sharp, worse breathing in**, one side = PE, pneumothorax or pneumonia.',
    '**Better sitting forward, worse lying flat** = pericarditis.', '**Burning behind the sternum after food or lying down** = reflux.', '**Reproduced exactly by pressing** = musculoskeletal. Only once the dangerous ones are out.'],
    draw: function (i) {
      var s = H.torso(70, 30, 180, 170) + H.r(152, 46, 16, 90, 'dg-thin', 4);
      var spots = [[160, 92, 26, 'dg-bl'], [160, 82, 18, 'dg-bl'], [200, 100, 20, 'dg-wl'], [160, 96, 22, 'dg-wl'], [160, 110, 14, 'dg-wl'], [112, 76, 12, 'dg-hl']];
      var p = spots[i]; s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + p[2] + '" class="' + p[3] + '"/>';
      if (i === 0) s += H.arrow(180, 86, 232, 124, 'dg-arr') + H.arrow(160, 70, 160, 40, 'dg-arr') + T(244, 138, 'left arm', 'dg-tr', 'middle');
      if (i === 1) s += H.arrow(176, 82, 236, 60, 'dg-arr') + T(244, 54, 'to the back', 'dg-tr');
      if (i === 2) s += H.p('M190 90 l6 6 l-6 6 l6 6', 'dg-ar');
      if (i === 3) s += T(160, 220, 'sit forward ✓   lie flat ✗', 'dg-ta', 'middle');
      if (i === 4) s += T(160, 220, 'after food · lying down', 'dg-ta', 'middle');
      if (i === 5) s += T(110, 104, 'press =', 'dg-ta', 'middle') + T(110, 116, 'same pain', 'dg-ta', 'middle');
      s += H.tag(160, 18, ['ACS', 'Dissection', 'Pleuritic', 'Pericarditis', 'Reflux', 'MSK'][i], i < 2 ? 'b' : 'w', 'middle');
      return S(320, 228, s, 'Chest pain patterns');
    }});
  var AP = [['Right upper', 'Biliary colic, cholecystitis, cholangitis, hepatitis', 'Fever + jaundice = cholangitis'], ['Epigastric', 'Peptic ulcer, pancreatitis, gastritis, MI', 'Through to the back = pancreatitis or AAA'], ['Left upper', 'Spleen, gastritis, pancreatitis', 'Trauma + shoulder tip pain = splenic rupture'],
    ['Right flank', 'Stone, pyelonephritis', 'Loin to groin colic = stone'], ['Central', 'Early appendicitis, obstruction, AAA, mesenteric ischaemia', 'Pain out of proportion = ischaemia'], ['Left flank', 'Stone, pyelonephritis', ''],
    ['Right iliac fossa', 'Appendicitis, ectopic, ovarian torsion, Crohn\'s', 'Any woman: pregnancy test'], ['Suprapubic', 'Retention, UTI, PID', 'Palpable bladder = retention'], ['Left iliac fossa', 'Diverticulitis, ectopic, ovarian, colitis', 'Older + fever = diverticulitis']];
  d('abdopain', {t: 'Abdominal pain: where it is → what it is', caps: AP.map(function (a) { return '**' + a[0] + ':** ' + a[1] + '.' + (a[2] ? ' 🚩 ' + a[2] + '.' : ''); }),
    draw: function (i) {
      var xs = [22, 114, 206, 298], ys = [16, 84, 152, 214], s = H.p('M24 22 Q160 2 296 22 L298 206 Q160 228 22 206 Z', 'dg-skin');
      s += H.ln(114, 14, 114, 216, 'dg-dash') + H.ln(206, 14, 206, 216, 'dg-dash') + H.ln(24, 84, 296, 84, 'dg-dash') + H.ln(24, 152, 296, 152, 'dg-dash');
      var cx = i % 3, cy = Math.floor(i / 3);
      s += H.r(xs[cx] + 2, ys[cy] + 2, xs[cx + 1] - xs[cx] - 4, ys[cy + 1] - ys[cy] - 4, 'dg-wl', 6);
      var words = AP[i][1].split(', ').slice(0, 3);
      words.forEach(function (w, k) { s += T((xs[cx] + xs[cx + 1]) / 2, (ys[cy] + ys[cy + 1]) / 2 - 8 + k * 12, w.replace('Early ', '').replace(' torsion', ''), 'dg-tb', 'middle', 9); });
      return S(320, 232, s, 'Abdominal pain by region');
    }});
  d('headache', {t: 'Headache: how fast it peaks tells you the danger', caps: [
    '**Thunderclap: peaks within a minute** = subarachnoid haemorrhage until proven otherwise. CT within 6 hours.', '**Migraine: builds over an hour,** one-sided, throbbing, light hurts, lasts hours to 3 days.',
    '**Raised pressure: worse each morning,** worse lying, coughing or bending, with vomiting. Getting steadily worse over weeks.', '**Cluster: 15 to 180 minutes, same time each day,** around one eye with a red watery eye.',
    '**Over 50, new, with jaw pain on chewing** = giant cell arteritis. Steroids today to save the sight.'],
    draw: function (i) {
      var s = H.ln(30, 160, 310, 160, 'dg-thin') + H.ln(30, 20, 30, 160, 'dg-thin') + T(170, 182, 'time', 'dg-tm', 'middle') + T(12, 16, 'pain', 'dg-tm');
      var curves = ['M30 158 L40 158 L46 30 L300 40', 'M30 158 C90 150 110 50 160 46 C220 44 240 120 300 150', 'M30 150 Q60 120 80 150 Q110 112 140 150 Q170 100 200 150 Q230 86 260 150 Q280 76 300 120', 'M30 158 L60 158 L70 50 L100 50 L110 158 L180 158 L190 50 L220 50 L230 158 L300 158', 'M30 150 Q140 140 300 70'];
      s += '<path d="' + curves[i] + '" style="fill:none;stroke:' + (i === 0 || i === 4 ? 'var(--bad)' : 'var(--accent)') + ';stroke-width:3;stroke-linejoin:round"/>';
      s += H.tag(170, 14, ['Thunderclap: under 1 minute', 'Migraine: builds over an hour', 'Raised ICP: worse each morning', 'Cluster: same time daily', 'GCA: over 50, jaw pain'][i], i === 0 || i === 4 ? 'b' : 'w', 'middle');
      if (i === 2) s += T(80, 176, 'morning', 'dg-tm', 'middle') + T(140, 176, 'morning', 'dg-tm', 'middle') + T(200, 176, 'morning', 'dg-tm', 'middle');
      return S(320, 190, s, 'Headache onset patterns');
    }});
  var NG = [[30, 'Breast lump, unexplained; armpit lump'], [40, 'Jaundice → pancreas; haemoptysis → lung'], [45, 'Visible haematuria → bladder or kidney; hoarse voice or neck lump → head and neck'],
    [50, 'One-nipple discharge or retraction → breast'], [55, 'Weight loss + dyspepsia, reflux or upper abdominal pain → oesophagus and stomach'], [60, 'Non-visible haematuria + dysuria → bladder; bone pain → myeloma bloods; weight loss + new diabetes → pancreas CT']];
  d('ng12', {t: 'Suspected cancer referral: the age ladder', caps: NG.map(function (n) { return '**' + n[0] + ' and over:** ' + n[1] + '.'; }).concat(['**Any age:** dysphagia, a testicular lump, FIT 10 or more, a rectal mass, a changing mole scoring 3, a mouth ulcer over 3 weeks, an unexplained thyroid lump.']),
    draw: function (i) {
      var s = '', wrap = function (t, n) { var out = [], line = ''; t.split(' ').forEach(function (w) { if ((line + ' ' + w).trim().length > n) { out.push(line.trim()); line = w; } else line += ' ' + w; }); if (line.trim()) out.push(line.trim()); return out; };
      NG.forEach(function (n, k) { var y = 182 - k * 30, hot = k === i || i === 6; s += '<g class="' + on(hot || k < i) + '"><rect x="12" y="' + y + '" width="' + (36 + k * 16) + '" height="22" rx="5" class="' + (k === i ? 'dg-wl' : 'dg-hl') + '"/>' + T(20, y + 15, String(n[0]), 'dg-tb', '', 12) + '</g>'; });
      var txt = i < 6 ? NG[i][1].split('; ') : ['Any age:', 'dysphagia', 'a testicular lump', 'FIT 10 or more', 'a rectal mass', 'a mole scoring 3', 'mouth ulcer over 3 weeks', 'a thyroid lump'];
      var L = []; txt.forEach(function (x) { L = L.concat(wrap(x, 26)); });
      L.forEach(function (x, k) { s += T(140, 26 + k * 15, x, k === 0 && i === 6 ? 'dg-tr' : 'dg-ta', '', 11); });
      return S(330, 210, s, 'NG12 ages');
    }});

  /* ================= psychiatry mnemonics ================= */
  d('aseptic', {t: 'Mental state examination: ASEPTIC', cards: [
    ['👕', 'A · Appearance and behaviour', 'Self-care, eye contact, agitation or slowed, rapport.'], ['🗣️', 'S · Speech', 'Rate, volume, flow: pressured or poor.'],
    ['🌦️', 'E · Emotion', '**Mood = what they say** in their words. **Affect = what you see**: flat, reactive, incongruent.'], ['👂', 'P · Perception', 'Hallucinations: which sense; second or third person.'],
    ['💭', 'T · Thought', '**Form:** flight of ideas, loosening. **Content:** delusions, suicidal thoughts.'], ['🪞', 'I · Insight', '"What do you think is going on?" Do they accept help?'],
    ['🧭', 'C · Cognition', 'Orientation, attention, memory.'], ['⚠️', 'Then risk', 'To self, to others, from others.']]});
  d('sigecaps', {t: 'Depression: low mood + SIGECAPS', cards: [
    ['😴', 'S · Sleep', 'Early waking is classic.'], ['🎨', 'I · Interest', 'Anhedonia: lost enjoyment.'], ['😞', 'G · Guilt', 'Worthless, a burden.'], ['🔋', 'E · Energy', 'Exhausted.'],
    ['🎯', 'C · Concentration', ''], ['🍽️', 'A · Appetite', 'And weight.'], ['🐢', 'P · Psychomotor', 'Slowed or agitated.'], ['⚠️', 'S · Suicide', '**Always ask directly.** 2 weeks or more of symptoms.']]});
  d('digfast', {t: 'Mania: DIGFAST', cards: [
    ['🦋', 'D · Distractible', ''], ['🌙', 'I · Insomnia', 'Little need for sleep, not tired.'], ['👑', 'G · Grandiose', 'Special powers, big plans.'], ['💨', 'F · Flight of ideas', 'Racing thoughts.'],
    ['🏃', 'A · Activity up', 'Goal-directed, restless.'], ['🗯️', 'S · Speech pressured', 'Hard to interrupt.'], ['💸', 'T · Thoughtless risks', 'Spending, sex, driving. **Ask about money and debts.**']]});
  d('sadpersons', {t: 'Suicide risk factors: SAD PERSONS, as a prompt only', caps: ['Use it to remember **what to ask**, never as a score. **NICE says don\'t use risk scales** to predict suicide or decide treatment.'], cards: [
    ['S', 'Sex: male', ''], ['A', 'Age: young men, older people', ''], ['D', 'Depression', ''], ['P', 'Previous attempt', 'The strongest predictor.'], ['E', 'Ethanol and drugs', ''],
    ['R', 'Rational thinking lost', 'Psychosis.'], ['S', 'Social support lacking', 'Alone, recent loss.'], ['O', 'Organised plan', '**Plan, means, final acts: notes, wills.**'], ['N', 'No partner', ''], ['S', 'Sickness', 'Chronic illness or pain.']]});

  /* ================= examination signs ================= */
  d('swift', {t: 'Neuro inspection: SWIFT', cards: [
    ['🩹', 'S · Scars', 'Spine, carpal tunnel, previous surgery.'], ['📉', 'W · Wasting', 'Small hand muscles, thighs. Wasting = lower motor neurone.'], ['🌀', 'I · Involuntary movements', 'Chorea, dystonia, myoclonus.'],
    ['〰️', 'F · Fasciculations', 'Watch the muscle for 20 seconds. **Motor neurone disease** until proven otherwise.'], ['🤚', 'T · Tremor', 'Rest = Parkinson\'s; outstretched = essential or thyroid; on reaching = cerebellar.']]});
  d('danish', {t: 'Cerebellar signs: DANISH', cards: [
    ['🔄', 'D · Dysdiadochokinesia', 'Clumsy fast alternating hand movements.'], ['🚶', 'A · Ataxia', 'Wide-based gait; can\'t heel-toe walk.'], ['👀', 'N · Nystagmus', 'Fast beat towards the side of the lesion.'],
    ['☝️', 'I · Intention tremor', 'Worse as the finger nears its target.'], ['🗣️', 'S · Slurred speech', 'Scanning, staccato.'], ['🦵', 'H · Heel-shin', 'And hypotonia. **Cerebellar signs are on the same side as the lesion.**']]});
  d('seads', {t: 'MSK look: SEADS', cards: [
    ['🎈', 'S · Swelling', 'Effusion, bony swelling, soft tissue.'], ['🔴', 'E · Erythema', 'Red and hot = infection or crystals.'], ['📉', 'A · Atrophy', 'Muscle wasting, quadriceps, deltoid, thenar.'],
    ['📐', 'D · Deformity', 'Varus, valgus, fixed flexion, shortening, rotation.'], ['🩹', 'S · Skin and scars', 'Midline knee scar = replacement; psoriasis plaques; nodules.']]});
  d('lump', {t: 'Any lump: S S S C T F', cards: [
    ['📍', 'Site', 'Clock face, or distance from a landmark.'], ['📏', 'Size', 'In cm, measured.'], ['⚪', 'Shape', 'Round, irregular; smooth or craggy edge.'], ['🪨', 'Consistency', 'Soft, rubbery, hard.'],
    ['😣', 'Tenderness', 'And temperature: hot + tender = inflammation.'], ['📌', 'Fixation', 'To skin or deeper. **Hard + irregular + fixed = cancer pattern.**'], ['🔦', 'Plus', 'Transilluminates? Pulsatile? Cough impulse? Can you get above it?']]});
  var MUL = [['Shoulder abduction', 'C5', -70], ['Elbow flexion', 'C5, C6', 0], ['Elbow extension', 'C7', 1], ['Wrist extension', 'C6, C7', 2], ['Finger flexion', 'C8', 3], ['Finger abduction', 'T1', 4]];
  d('myoUL', {t: 'Arm power: one movement, one root', caps: MUL.map(function (m) { return '**' + m[0] + ' = ' + m[1] + '.**'; }).concat(['Grade each **out of 5**: 0 nothing, 1 flicker, 2 gravity removed, 3 against gravity, 4 some resistance, 5 normal.']),
    draw: function (i) {
      var s = '<circle cx="80" cy="40" r="14" class="dg-skin"/>' + H.p('M66 58 L94 58 L98 150 L62 150 Z', 'dg-skin');
      var P = [[[146, 64], [194, 64]], [[100, 116], [128, 74]], [[100, 116], [138, 150]], [[100, 118], [152, 118]], [[100, 118], [152, 118]], [[100, 118], [152, 118]], [[100, 118], [152, 118]]][i];
      var el = P[0], wr = P[1], L = function (a, b, w) { return '<line x1="' + a[0] + '" y1="' + a[1] + '" x2="' + b[0] + '" y2="' + b[1] + '" style="stroke:var(--muted);stroke-width:' + w + ';stroke-linecap:round"/>'; };
      s += L([94, 64], el, 12) + L(el, wr, 10);
      if (i === 3) s += L(wr, [160, 102], 8);
      else if (i === 4) s += '<circle cx="' + (wr[0] + 6) + '" cy="' + wr[1] + '" r="8" class="dg-skin"/>';
      else if (i === 5) s += L(wr, [170, 106], 4) + L(wr, [172, 118], 4) + L(wr, [170, 130], 4);
      else s += '<circle cx="' + wr[0] + '" cy="' + wr[1] + '" r="8" class="dg-skin"/>';
      var arr = [[170, 92, 170, 52], [140, 100, 130, 66], [120, 128, 146, 160], [168, 118, 166, 92], [174, 108, 160, 128], [176, 112, 190, 96], null][i];
      if (arr) s += H.arrow(arr[0], arr[1], arr[2], arr[3], 'dg-arr');
      if (i < 6) s += H.tag(256, 40, MUL[i][1], 'w', 'middle') + T(256, 70, MUL[i][0], 'dg-tb', 'middle', 11);
      else s += box(176, 40, 136, 120, 'MRC power|5 normal|4 some resistance|3 against gravity|2 gravity removed|1 flicker · 0 none', 'dg-hl', null, 10);
      return S(320, 190, s, 'Upper limb myotomes');
    }});
  var MLL = [['Hip flexion', 'L1, L2'], ['Knee extension', 'L3, L4'], ['Ankle dorsiflexion', 'L4'], ['Big toe extension', 'L5'], ['Ankle plantarflexion', 'S1'], ['Knee flexion and hip extension', 'L5, S1']];
  d('myoLL', {t: 'Leg power: count down the leg', caps: MLL.map(function (m) { return '**' + m[0] + ' = ' + m[1] + '.**'; }),
    draw: function (i) {
      var s = H.ln(20, 170, 300, 170, 'dg-thin') + H.r(30, 150, 90, 18, 'dg-skin', 8) + H.c(36, 140, 12, 'dg-skin');
      var hip = [120, 158], th = [[60, 200], [200, 160], [200, 160], [200, 160], [200, 160], [200, 160]][i];
      var knee = i === 0 ? [176, 110] : i === 1 ? [180, 124] : [200, 160];
      var ankle = i === 0 ? [236, 140] : i === 1 ? [232, 166] : i === 5 ? [240, 120] : [270, 160];
      s += '<line x1="' + hip[0] + '" y1="' + hip[1] + '" x2="' + knee[0] + '" y2="' + knee[1] + '" style="stroke:var(--muted);stroke-width:14;stroke-linecap:round"/><line x1="' + knee[0] + '" y1="' + knee[1] + '" x2="' + ankle[0] + '" y2="' + ankle[1] + '" style="stroke:var(--muted);stroke-width:11;stroke-linecap:round"/>';
      var toe = i === 2 ? [ankle[0] + 6, ankle[1] - 26] : i === 4 ? [ankle[0] + 26, ankle[1] + 6] : [ankle[0] + 4, ankle[1] - 22];
      s += '<line x1="' + ankle[0] + '" y1="' + ankle[1] + '" x2="' + toe[0] + '" y2="' + toe[1] + '" style="stroke:var(--muted);stroke-width:9;stroke-linecap:round"/>';
      var arr = [[176, 128, 176, 92], [244, 150, 272, 120], [ankle[0] + 22, ankle[1] - 6, ankle[0] + 18, ankle[1] - 30], [toe[0] + 12, toe[1] + 6, toe[0] + 12, toe[1] - 14], [ankle[0] + 34, ankle[1] - 10, ankle[0] + 40, ankle[1] + 14], [250, 104, 216, 130]][i];
      s += H.arrow(arr[0], arr[1], arr[2], arr[3], 'dg-arr');
      s += H.tag(90, 40, MLL[i][1], 'w', 'middle') + T(90, 68, MLL[i][0], 'dg-tb', 'middle', 11);
      return S(320, 190, s, 'Lower limb myotomes');
    }});
  d('plantar', {t: 'Plantar response: which way does the big toe go?', caps: ['Run a blunt object up the **outside of the sole** and across the ball of the foot.', '**Normal: the toe curls down.** Flexor plantar.', '**Upper motor neurone: the big toe goes up and the others fan out.** Babinski positive. "Up = UMN."', '**Clonus:** flick the foot up quickly; more than 3 beats = upper motor neurone.'],
    draw: function (i) {
      var s = H.p('M70 60 Q60 140 90 170 Q140 190 220 176 Q262 168 270 140 Q272 110 240 104 L120 70 Q96 50 70 60 Z', 'dg-skin');
      if (i === 0) s += H.p('M100 160 Q170 168 230 150 Q250 136 248 118', 'dg-arr') + T(150, 196, 'outside edge of the sole', 'dg-tm', 'middle');
      var toeUp = i === 2, tx = 262, ty = 120;
      if (i >= 1 && i <= 2) s += '<line x1="248" y1="112" x2="' + (toeUp ? 268 : 280) + '" y2="' + (toeUp ? 72 : 132) + '" style="stroke:var(--muted);stroke-width:12;stroke-linecap:round"/>' + H.tag(160, 26, toeUp ? 'Toe up = UMN' : 'Toe down = normal', toeUp ? 'b' : 'g', 'middle');
      if (i === 2) [[250, 140], [240, 150], [228, 158]].forEach(function (p, k) { s += H.arrow(p[0], p[1], p[0] + 10 + k * 3, p[1] + 14, 'dg-arr'); });
      if (i === 3) s += H.p('M260 100 q10 -14 0 -28 M270 104 q12 -18 0 -36', 'dg-arr') + H.tag(160, 26, 'over 3 beats = UMN', 'b', 'middle');
      return S(320, 204, s, 'Plantar response');
    }});
  d('jvp', {t: 'JVP vs carotid: 5 ways to tell them apart', caps: [
    'Patient at **45°**, head turned slightly left. Look between the two heads of sternocleidomastoid, up to the earlobe.', '**JVP: two flickers per beat;** the carotid is one sharp thrust.',
    '**You can\'t feel the JVP;** you can feel the carotid.', '**Press over the liver: the JVP rises.** Hepatojugular reflux.', '**Measure the height above the sternal angle:** over 3 cm = raised. Fluid overload or right heart failure.'],
    draw: function (i) {
      var s = H.p('M90 20 Q140 10 190 30 L196 200 L60 200 L70 120 Q66 70 90 20 Z', 'dg-skin') + H.p('M120 40 L150 190 M170 40 L160 190', 'dg-thin');
      s += H.p('M144 70 Q140 110 146 150', 'dg-thin');
      var wave = function (x, y, two) { return '<path d="M' + x + ' ' + y + (two ? ' q6 -14 12 0 q6 -10 12 0' : ' l6 -20 l6 20') + '" class="dg-ar"/>'; };
      if (i === 0) s += H.ln(40, 200, 240, 104, 'dg-dash') + T(250, 100, '45°', 'dg-ta');
      if (i === 1) s += wave(220, 70, true) + T(244, 66, 'JVP: 2', 'dg-ta') + wave(220, 120, false) + T(244, 116, 'carotid: 1', 'dg-ta');
      if (i === 2) s += T(230, 80, 'JVP: can\'t feel ✋', 'dg-ta', 'middle') + T(230, 110, 'carotid: can feel ✋', 'dg-ta', 'middle');
      if (i === 3) s += H.arrow(146, 160, 146, 96, 'dg-arr') + T(230, 120, 'press the liver →', 'dg-tm', 'middle') + T(230, 136, 'JVP rises', 'dg-tr', 'middle');
      if (i === 4) s += H.ln(146, 96, 146, 172, 'dg-ln') + H.ln(130, 172, 200, 172, 'dg-dash') + T(206, 176, 'sternal angle', 'dg-tm') + T(160, 134, '> 3 cm', 'dg-tr');
      return S(320, 210, s, 'JVP');
    }});
  d('clubbing', {t: 'Clubbing: the diamond window', caps: ['Put the backs of the two index fingers together, nail to nail.', '**Normal: a diamond-shaped window** between the nails.', '**Clubbed: the window is gone.** Schamroth\'s sign.', '**Chest causes:** lung cancer, fibrosis, bronchiectasis, empyema. **Heart:** endocarditis, cyanotic heart disease. **Gut:** IBD, cirrhosis. **Never COPD alone.**'],
    draw: function (i) {
      if (i === 3) return S(320, 190, box(20, 30, 280, 130, 'Clubbing causes|Chest: cancer, fibrosis, bronchiectasis, empyema|Heart: endocarditis, cyanotic disease|Gut: IBD, cirrhosis|Never COPD alone', 'dg-hl', null, 11), 'Clubbing causes');
      var club = i === 2;
      var L = 'M84 196 L84 70 Q84 34 124 34 L158 40 ' + (club ? 'Q166 76 160 112' : 'L144 78 L160 112') + ' L160 196 Z';
      var R = 'M236 196 L236 70 Q236 34 196 34 L162 40 ' + (club ? 'Q154 76 160 112' : 'L176 78 L160 112') + ' L160 196 Z';
      var s = '<path d="' + L + '" class="dg-skin"/><path d="' + R + '" class="dg-skin"/>';
      s += '<path d="M124 36 L158 40 ' + (club ? 'Q166 76 160 112' : 'L144 78') + '" style="fill:none;stroke:var(--accent);stroke-width:4;stroke-linecap:round"/><path d="M196 36 L162 40 ' + (club ? 'Q154 76 160 112' : 'L176 78') + '" style="fill:none;stroke:var(--accent);stroke-width:4;stroke-linecap:round"/>';
      s += T(104, 24, 'nail', 'dg-tm', 'middle') + T(216, 24, 'nail', 'dg-tm', 'middle');
      if (i === 1) s += '<path d="M160 44 L146 78 L160 110 L174 78 Z" class="dg-wl"/>' + T(160, 150, 'window ✓', 'dg-ta', 'middle');
      if (i === 2) s += T(160, 150, 'no window', 'dg-tr', 'middle');
      if (i === 0) s += T(160, 150, 'back to back', 'dg-tm', 'middle');
      return S(320, 200, s, 'Schamroth window');
    }});
  d('cvshands', {t: 'Hands in a CVS exam: endocarditis and more', caps: ['**Splinter haemorrhages:** thin red-brown lines under the nail.', '**Osler nodes: painful** pea-like lumps on the finger pads. Osler = Ouch.', '**Janeway lesions: painless** flat red spots on the palm.', '**Clubbing**, and **tendon xanthomata** for high cholesterol.'],
    draw: function (i) {
      var s = '<path d="M110 200 L110 120 Q110 100 126 100 L210 100 Q226 100 226 120 L226 200 Z" class="dg-skin"/>';
      [116, 144, 172, 200].forEach(function (x, k) { var h = [70, 84, 80, 64][k]; s += '<rect x="' + x + '" y="' + (100 - h) + '" width="22" height="' + (h + 10) + '" rx="10" class="dg-skin"/><rect x="' + (x + 4) + '" y="' + (100 - h + 4) + '" width="14" height="16" rx="5" fill="var(--surface-2)" stroke="var(--muted)"/>'; });
      s += '<rect x="84" y="120" width="22" height="56" rx="10" class="dg-skin" transform="rotate(-25 95 148)"/>';
      if (i === 0) [152, 155, 158].forEach(function (x) { s += '<line x1="' + x + '" y1="22" x2="' + x + '" y2="32" style="stroke:#7a2a1a;stroke-width:1.5"/>'; });
      if (i === 1) s += '<circle cx="155" cy="30" r="5" fill="#c0506a"/><circle cx="183" cy="34" r="5" fill="#c0506a"/>';
      if (i === 2) s += '<circle cx="150" cy="150" r="5" fill="#e07a7a"/><circle cx="190" cy="165" r="4" fill="#e07a7a"/><circle cx="170" cy="140" r="3.5" fill="#e07a7a"/>';
      if (i === 3) s += '<rect x="144" y="16" width="22" height="18" rx="9" class="dg-wl"/>';
      s += H.tag(260, 40, ['Splinters', 'Osler: ouch', 'Janeway: painless', 'Clubbing'][i], i === 1 ? 'b' : 'w', 'middle');
      return S(320, 208, s, 'Hand signs');
    }});
  var LS = [['Asterixis: the flap', -40, 104], ['Leuconychia, clubbing, palmar erythema, Dupuytren\'s', 40, 106], ['Yellow sclera: jaundice', 4, 14], ['Spider naevi: more than 5', -10, 56], ['Gynaecomastia', 12, 60], ['Ascites, caput medusae', 0, 94], ['Big spleen', 14, 84], ['Bruising, ankle swelling', -14, 170]];
  d('liversigns', {t: 'Chronic liver disease: read the body from hands to feet', caps: LS.map(function (l) { return '**' + l[0] + '.**'; }),
    draw: function (i) {
      var s = H.body(150, 8, 214), k = 1.07;
      LS.forEach(function (l, n) { s += '<circle cx="' + (150 + l[1] * k).toFixed(1) + '" cy="' + (8 + l[2] * k).toFixed(1) + '" r="' + (n === i ? 9 : 4) + '" class="' + (n === i ? 'dg-wl' : 'dg-pt') + '"/>'; });
      s += H.tag(250, 30, LS[i][0].split(':')[0].split(',')[0], 'w', 'middle');
      return S(300, 236, s, 'Liver signs');
    }});
  d('kneetests', {t: 'Knee tests in pictures', caps: ['**Patellar tap:** squeeze fluid down from above, then press the kneecap; a tap = large effusion.', '**Anterior drawer:** knee at 90°, sit gently on the foot, pull the shin forward. Moves = **ACL**.', '**Posterior sag:** look from the side at 90°. Shin sinks back = **PCL**.', '**Valgus stress:** push the knee inwards at 20°. Opens on the inside = **MCL**.'],
    draw: function (i) {
      var s = H.ln(10, 180, 310, 180, 'dg-thin');
      if (i === 0) { s += '<line x1="40" y1="120" x2="280" y2="120" style="stroke:var(--muted);stroke-width:30;stroke-linecap:round"/><ellipse cx="170" cy="104" rx="16" ry="10" class="dg-skin"/>' + H.arrow(100, 80, 150, 98, 'dg-arr') + H.arrow(170, 70, 170, 94, 'dg-arr') + T(170, 60, 'press', 'dg-ta', 'middle') + T(96, 70, 'squeeze down', 'dg-ta', 'middle'); }
      else if (i === 3) { s += '<line x1="60" y1="60" x2="160" y2="110" style="stroke:var(--muted);stroke-width:26;stroke-linecap:round"/><line x1="160" y1="110" x2="270" y2="130" style="stroke:var(--muted);stroke-width:22;stroke-linecap:round"/>' + H.arrow(160, 60, 160, 96, 'dg-arr') + H.arrow(290, 160, 270, 140, 'dg-arr') + T(170, 52, 'push in', 'dg-ta', 'middle') + T(160, 150, 'opens inside = MCL', 'dg-tr', 'middle'); }
      else { var sag = i === 2 ? 10 : 0; s += '<line x1="40" y1="170" x2="160" y2="80" style="stroke:var(--muted);stroke-width:26;stroke-linecap:round"/><line x1="' + (160) + '" y1="' + (80 + sag) + '" x2="' + (180) + '" y2="176" style="stroke:var(--muted);stroke-width:22;stroke-linecap:round"/><ellipse cx="190" cy="178" rx="24" ry="8" class="dg-skin"/>';
        if (i === 1) s += H.arrow(176, 120, 216, 120, 'dg-arr') + T(230, 112, 'pull forward', 'dg-ta') + T(230, 128, 'moves = ACL', 'dg-tr');
        if (i === 2) s += T(220, 90, 'sags back', 'dg-tr') + T(220, 106, '= PCL', 'dg-tr') + H.ln(150, 72, 196, 72, 'dg-dash'); }
      return S(320, 196, s, 'Knee special tests');
    }});
  d('handjoints', {t: 'Hand joints: which ones swell tells you which arthritis', caps: ['**Rheumatoid: MCPs and PIPs**, both hands, soft and warm. DIPs spared.', '**Osteoarthritis: DIPs and PIPs**, hard bony nodes, and the thumb base.', '**Psoriatic: DIPs**, with nail pitting and a sausage finger.', '**Nerves: median** = thumb, index, middle, half ring on the palm side; **ulnar** = little and half ring.'],
    draw: function (i) {
      var s = '<path d="M110 210 L106 130 Q106 112 124 110 L216 110 Q232 112 232 130 L230 210 Z" class="dg-skin"/>';
      var F = [[120, 70], [148, 84], [176, 80], [204, 64]], j = [];
      F.forEach(function (f, k) { var x = f[0]; s += '<rect x="' + x + '" y="' + (110 - f[1]) + '" width="22" height="' + (f[1] + 8) + '" rx="10" class="dg-skin"/>'; j.push([x + 11, 114, 'mcp'], [x + 11, 110 - f[1] * 0.45, 'pip'], [x + 11, 110 - f[1] * 0.78, 'dip']); });
      s += '<rect x="80" y="122" width="24" height="60" rx="10" class="dg-skin" transform="rotate(-28 92 152)"/>';
      if (i < 3) { var hot = [['mcp', 'pip'], ['pip', 'dip'], ['dip']][i]; j.forEach(function (p) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="' + (hot.indexOf(p[2]) >= 0 ? 7 : 3) + '" class="' + (hot.indexOf(p[2]) >= 0 ? (i === 0 ? 'dg-bl' : 'dg-wl') : 'dg-pt') + '"/>'; }); if (i === 1) s += '<circle cx="104" cy="168" r="8" class="dg-wl"/>'; if (i === 2) s += '<rect x="148" y="26" width="22" height="84" rx="10" class="dg-bl"/>'; }
      else { s += '<path d="M106 130 L106 210 L194 210 L192 110 L120 110 Z" fill="var(--accent)" fill-opacity=".22"/><path d="M194 110 L232 112 L230 210 L194 210 Z" fill="var(--warn)" fill-opacity=".3"/>' + T(150, 196, 'median', 'dg-ta', 'middle') + T(212, 196, 'ulnar', 'dg-tb', 'middle'); }
      s += H.tag(270, 30, ['RA', 'OA', 'Psoriatic', 'Nerves'][i], 'w', 'middle');
      return S(320, 220, s, 'Hand joints');
    }});
  d('leglength', {t: 'Leg length: true vs apparent', caps: ['**True length:** ASIS to the medial malleolus. Short = the problem is in the hip or leg itself.', '**Apparent length:** umbilicus to the medial malleolus. Different only when the pelvis is tilted.', '**Short + externally rotated after a fall = fractured neck of femur.**'],
    draw: function (i) {
      var s = '<ellipse cx="160" cy="40" rx="70" ry="22" class="dg-skin"/>' + H.c(160, 46, 3, 'dg-ink') + H.c(110, 40, 4, 'dg-ink') + H.c(210, 40, 4, 'dg-ink');
      s += '<line x1="130" y1="56" x2="126" y2="200" style="stroke:var(--muted);stroke-width:22;stroke-linecap:round"/><line x1="190" y1="56" x2="' + (i === 2 ? 200 : 194) + '" y2="' + (i === 2 ? 186 : 200) + '" style="stroke:var(--muted);stroke-width:22;stroke-linecap:round"/>';
      s += H.c(136, 200, 4, 'dg-ink') + H.c(i === 2 ? 190 : 184, i === 2 ? 186 : 200, 4, 'dg-ink');
      if (i === 0) s += H.ln(110, 40, 136, 200, 'dg-arr') + T(70, 120, 'ASIS → malleolus', 'dg-ta', 'middle');
      if (i === 1) s += H.ln(160, 46, 136, 200, 'dg-arr') + T(70, 120, 'navel → malleolus', 'dg-ta', 'middle');
      if (i === 2) s += '<ellipse cx="210" cy="192" rx="18" ry="7" class="dg-bl" transform="rotate(40 210 192)"/>' + T(250, 140, 'short and', 'dg-tr', 'middle') + T(250, 156, 'turned out', 'dg-tr', 'middle');
      return S(320, 214, s, 'Leg length');
    }});
  d('simmonds', {t: 'Simmonds\' squeeze test', caps: ['Kneeling on a chair, feet hanging free.', '**Squeeze the calf: the foot points down.** Achilles intact.', '**Squeeze the calf: the foot doesn\'t move.** Achilles ruptured. Usually a pop, like being kicked, in someone doing sport.'],
    draw: function (i) {
      var s = H.r(30, 60, 140, 16, 'dg-mut', 4) + T(100, 54, 'chair', 'dg-tm', 'middle') + '<line x1="60" y1="70" x2="200" y2="70" style="stroke:var(--muted);stroke-width:24;stroke-linecap:round"/>';
      var foot = i === 1 ? 'M200 70 L232 108' : 'M200 70 L204 112';
      s += '<path d="' + foot + '" style="stroke:var(--muted);stroke-width:14;stroke-linecap:round;fill:none"/>';
      if (i > 0) s += H.arrow(150, 30, 150, 54, 'dg-arr') + H.arrow(150, 112, 150, 88, 'dg-arr') + T(150, 22, 'squeeze', 'dg-ta', 'middle');
      if (i === 1) s += H.tag(250, 150, 'foot points: intact', 'g', 'middle');
      if (i === 2) s += H.tag(250, 150, 'no movement: ruptured', 'b', 'middle') + '<line x1="190" y1="58" x2="190" y2="82" style="stroke:var(--bad);stroke-width:3;stroke-dasharray:3 2"/>';
      return S(320, 170, s, 'Simmonds test');
    }});
  d('otoscope', {t: 'Otoscope: hold, pull, brace', caps: ['**Hold it like a pen**, not like a hammer.', '**Adults: pull the pinna up and back** to straighten the canal. Children: back; infants: back and down.', '**Brace your little finger on their cheek** so if they move, the otoscope moves with them.', '**Good ear first; largest speculum that fits; change it between ears.**'],
    draw: function (i) {
      var s = '<ellipse cx="120" cy="110" rx="48" ry="70" class="dg-skin"/><path d="M110 90 Q96 110 112 130" class="dg-ln"/><circle cx="120" cy="110" r="6" class="dg-ink"/>';
      if (i === 1) s += H.arrow(150, 60, 176, 30, 'dg-arr') + T(190, 26, 'up and back', 'dg-ta');
      var scope = '<g transform="rotate(-10 200 120)"><rect x="140" y="104" width="90" height="12" rx="6" class="dg-skin"/><rect x="228" y="96" width="24" height="70" rx="8" class="dg-skin"/><path d="M140 104 L126 110 L140 116 Z" class="dg-ink"/></g>';
      if (i !== 1) s += scope;
      if (i === 0) s += T(240, 190, 'pen grip', 'dg-ta', 'middle');
      if (i === 2) s += '<circle cx="168" cy="150" r="9" class="dg-wl"/>' + T(220, 196, 'little finger on the cheek', 'dg-ta', 'middle');
      if (i === 3) s += H.tag(220, 30, 'good ear first', 'w', 'middle');
      return S(320, 206, s, 'Otoscopy technique');
    }});
  d('confront', {t: 'Visual fields by confrontation', caps: ['**Sit 1 metre apart, eyes level.**', '**Mirror each other:** they cover their left eye with their left hand; you close your right. You are the normal control.', '**Wiggle a finger halfway between you,** coming in from outside each of the 4 quadrants. "Say now when you see it move."', '**Central field and blind spot with a red pin.** Then swap eyes.'],
    draw: function (i) {
      var s = '<circle cx="60" cy="100" r="34" class="dg-skin"/><circle cx="260" cy="100" r="34" class="dg-skin"/>' + T(60, 156, 'patient', 'dg-tm', 'middle') + T(260, 156, 'you', 'dg-tm', 'middle');
      s += '<circle cx="72" cy="92" r="4" class="dg-ink"/><circle cx="248" cy="92" r="4" class="dg-ink"/>';
      if (i === 0) s += H.arrow(100, 60, 220, 60) + H.arrow(220, 60, 100, 60) + T(160, 52, '1 metre', 'dg-ta', 'middle');
      if (i >= 1) s += '<rect x="44" y="96" width="18" height="10" rx="4" class="dg-wl"/>' + H.p('M268 92 l10 0', 'dg-ln');
      if (i === 2) s += '<circle cx="160" cy="40" r="6" class="dg-bl"/>' + H.arrow(160, 14, 160, 32, 'dg-arr') + H.ln(160, 40, 160, 170, 'dg-dash') + T(170, 186, 'halfway', 'dg-tm');
      if (i === 3) s += '<circle cx="160" cy="96" r="6" fill="#d33"/>' + T(160, 120, 'red pin', 'dg-tr', 'middle');
      return S(320, 196, s, 'Confrontation');
    }});
  d('rapd', {t: 'Swinging torch: finding a bad optic nerve', caps: ['Shine in the **good eye: both pupils constrict.**', '**Swing quickly to the bad eye: both pupils dilate.** Less light gets reported by the damaged nerve.', 'That is a **relative afferent pupillary defect**: think optic neuritis, a big retinal detachment, CRAO or glaucoma.'],
    draw: function (i) {
      var small = i === 0, s = '';
      [100, 220].forEach(function (x) { s += '<path d="M' + (x - 50) + ' 100 Q' + x + ' 50 ' + (x + 50) + ' 100 Q' + x + ' 150 ' + (x - 50) + ' 100 Z" fill="#f4f1ec" stroke="var(--muted)"/><circle cx="' + x + '" cy="100" r="22" fill="#5c7d56"/><circle cx="' + x + '" cy="100" r="' + (small ? 6 : 13) + '" fill="#0d1418" style="transition:r .4s"/>'; });
      s += T(100, 170, 'right · good', 'dg-tm', 'middle') + T(220, 170, 'left · bad nerve', 'dg-tm', 'middle');
      var tx = small ? 100 : 220; s += '<path d="M' + tx + ' 20 L' + (tx - 10) + ' 46 L' + (tx + 10) + ' 46 Z" fill="#f0c040"/>' + H.ln(tx, 46, tx, 74, 'dg-dash');
      if (i === 2) s += H.tag(160, 190, 'RAPD on the left', 'b', 'middle');
      return S(320, 200, s, 'RAPD');
    }});
  d('lidlag', {t: 'Thyroid eyes: lid retraction, lid lag, proptosis', caps: ['**Normal:** the upper lid covers the top of the iris.', '**Lid retraction:** white sclera visible above the iris at rest. Any overactive thyroid.', '**Lid lag:** as the eye follows your finger down, the lid lags behind and white shows above.', '**Proptosis:** look from above and behind: the eye bulges forward. **Graves\' only.**'],
    draw: function (i) {
      var s = '', top = [70, 58, 58, 52][i], iris = i === 2 ? 112 : 100;
      s += '<path d="M60 100 Q160 ' + (top - 40) + ' 260 100 Q160 150 60 100 Z" fill="#f4f1ec" stroke="var(--muted)"/>';
      s += '<circle cx="160" cy="' + iris + '" r="34" fill="#5c7d56"/><circle cx="160" cy="' + iris + '" r="12" fill="#0d1418"/>';
      if (i === 0) s += '<path d="M60 100 Q160 30 260 100 L260 70 L60 70 Z" fill="var(--surface-2)"/><path d="M60 100 Q160 52 260 100" fill="none" stroke="var(--ink)" stroke-width="2"/>';
      if (i === 1 || i === 2) s += T(160, 40, 'white above the iris', 'dg-tr', 'middle');
      if (i === 2) s += H.arrow(290, 60, 290, 130, 'dg-arr') + T(290, 150, 'looking down', 'dg-tm', 'middle');
      if (i === 3) s += '<path d="M60 170 Q160 140 260 170" class="dg-thin"/><ellipse cx="160" cy="178" rx="30" ry="14" class="dg-wl"/>' + T(160, 200, 'from above: bulges forward', 'dg-tr', 'middle');
      return S(320, 210, s, 'Thyroid eye signs');
    }});

  /* ================= procedures ================= */
  d('prepdone', {t: 'Every procedure: PREP, do it, DONE', cards: [
    ['🪪', 'P · Patient ID', 'Name, date of birth, wristband.'], ['🗣️', 'R · Reason and consent', 'What, why, what it feels like.'], ['🧰', 'E · Equipment', 'Clean tray, in date, sharps bin within reach.'],
    ['🧤', 'P · Protect', 'Hand hygiene, gloves, apron; allergies: latex, chlorhexidine, plasters.'], ['🗑️', 'D · Dispose', 'Sharps straight in the bin.'], ['👀', 'O · Observe', 'Is the patient OK? Bleeding, pain?'],
    ['📝', 'N · Note', 'Document and label at the bedside.'], ['💬', 'E · Explain', 'The result and what happens next.']]});
  d('cannangle', {t: 'Cannula: the angle, then 2 mm more', caps: ['**Anchor the skin** below the site with your thumb.', '**Bevel up at 10 to 30°** along the line of the vein.', '**Flashback in the chamber:** blood means the needle tip is in.', '**Drop the angle and advance 2 mm more,** so the plastic tip is in the vein too.', '**Slide the plastic off the needle** into the vein. Tourniquet off, press beyond the tip, needle out, cap, flush.'],
    draw: function (i) {
      var s = H.r(10, 110, 300, 60, 'dg-mut', 6) + H.ln(10, 110, 310, 110, 'dg-ln') + '<rect x="20" y="132" width="280" height="14" rx="7" fill="#7a8fc6" opacity=".7"/>' + T(30, 160, 'vein', 'dg-tm');
      var ang = [20, 20, 20, 8, 6][i], tipX = [120, 150, 176, 196, 230][i], tipY = [104, 120, 136, 138, 138][i];
      var L = 120, bx = tipX - L * Math.cos(ang * Math.PI / 180), by = tipY - L * Math.sin(ang * Math.PI / 180);
      if (i === 0) s += '<ellipse cx="250" cy="104" rx="20" ry="9" class="dg-wl"/>' + T(250, 92, 'anchor', 'dg-ta', 'middle');
      s += '<line x1="' + bx.toFixed(1) + '" y1="' + by.toFixed(1) + '" x2="' + tipX + '" y2="' + tipY + '" style="stroke:#8a8f96;stroke-width:3"/>';
      s += '<line x1="' + bx.toFixed(1) + '" y1="' + by.toFixed(1) + '" x2="' + (tipX - (i === 4 ? 0 : 8)) + '" y2="' + (tipY - (i === 4 ? 0 : 2)) + '" style="stroke:#2e9e44;stroke-width:6;opacity:.6"/>';
      s += '<rect x="' + (bx - 22).toFixed(1) + '" y="' + (by - 8).toFixed(1) + '" width="22" height="16" rx="4" fill="#2e9e44"/>';
      if (i >= 2) s += '<rect x="' + (bx - 18).toFixed(1) + '" y="' + (by - 4).toFixed(1) + '" width="10" height="8" fill="#c22"/>' + T(bx - 10, by - 14, 'flashback', 'dg-tr', 'middle');
      s += H.tag(160, 28, ['anchor the skin', '10 to 30°, bevel up', 'flashback', 'flatten, +2 mm', 'slide the plastic in'][i], 'w', 'middle');
      return S(320, 180, s, 'Cannulation angle');
    }});
  d('cuff', {t: 'BP cuff: size and position', caps: ['**The bladder should wrap about 80% of the arm.** Too small reads falsely high.', '**Arrow over the brachial artery**, 2 to 3 cm above the elbow crease.', '**Arm supported at heart level**, sitting, rested for 5 minutes, legs uncrossed.'],
    draw: function (i) {
      var s = '<line x1="40" y1="100" x2="280" y2="100" style="stroke:var(--muted);stroke-width:44;stroke-linecap:round"/>' + H.c(230, 100, 5, 'dg-ink') + T(230, 140, 'elbow crease', 'dg-tm', 'middle');
      s += '<rect x="120" y="72" width="90" height="56" rx="6" fill="#2f6fd6" opacity=".75"/>';
      if (i === 0) s += '<rect x="126" y="76" width="78" height="40" rx="4" fill="#fff" opacity=".35"/>' + T(165, 62, '80% of the arm', 'dg-ta', 'middle');
      if (i === 1) s += '<path d="M190 120 L196 110 L202 120 Z" fill="#fff"/>' + H.ln(196, 110, 196, 128, 'dg-ln') + T(200, 170, '2 to 3 cm above', 'dg-ta', 'middle');
      if (i === 2) s += H.ln(20, 100, 300, 100, 'dg-dash') + T(160, 30, 'at heart level · 5 minutes rest', 'dg-ta', 'middle');
      return S(320, 180, s, 'BP cuff');
    }});
  d('cathM', {t: 'Male catheter: why 90° and to the hilt', caps: ['The male urethra has **two bends**.', '**Lift the penis up to 90°** with your non-dominant hand: one bend straightens.', '**Advance all the way to the Y junction,** the hilt. The balloon sits past the prostate.', '**Urine first, then inflate 10 ml.** Inflating in the urethra tears it.', '**Replace the foreskin.**'],
    draw: function (i) {
      var s = '<path d="M40 40 Q120 30 150 80 Q170 120 150 150 L120 150 Q140 120 120 90 Q100 60 40 64 Z" class="dg-skin"/>' + T(70, 30, 'bladder', 'dg-tm', 'middle');
      s += '<ellipse cx="80" cy="52" rx="44" ry="24" class="dg-hl"/><circle cx="150" cy="112" r="14" class="dg-wl"/>' + T(178, 116, 'prostate', 'dg-tm');
      var shaft = i >= 1 ? 'M150 130 L150 60 L170 60 L170 130' : 'M146 150 Q170 190 230 196 L236 176 Q190 172 166 142';
      s += '<path d="' + shaft + '" class="dg-skin"/>';
      var path = i >= 1 ? 'M160 64 L160 112 Q150 96 120 70 Q100 52 70 52' : 'M232 186 Q186 182 160 142 L150 120 Q140 96 110 70';
      s += '<path d="' + path + '" style="fill:none;stroke:var(--accent);stroke-width:' + (i >= 2 ? 4 : 1.5) + ';stroke-dasharray:' + (i >= 2 ? 'none' : '3 3') + '"/>';
      if (i >= 3) s += '<circle cx="74" cy="52" r="10" fill="none" stroke="var(--accent)" stroke-width="3"/>' + T(74, 84, '10 ml', 'dg-ta', 'middle');
      if (i === 1) s += T(200, 50, 'up to 90°', 'dg-ta');
      if (i === 2) s += T(200, 50, 'to the hilt', 'dg-ta');
      if (i === 3) s += T(200, 50, 'urine, then inflate', 'dg-ta');
      if (i === 4) s += H.tag(220, 180, 'replace the foreskin', 'b', 'middle');
      return S(320, 210, s, 'Male catheter');
    }});
  d('cathF', {t: 'Female catheter: find the meatus', caps: ['**Knees bent and apart, heels together.** Good light.', '**Separate the labia** with the non-dominant hand and keep them apart.', '**The urethral meatus sits above the vaginal opening,** below the clitoris.', '**Clean front to back, one swab per stroke.** Wrong hole? Leave that catheter in as a signpost.'],
    draw: function (i) {
      var s = '<ellipse cx="160" cy="110" rx="70" ry="90" class="dg-skin"/><ellipse cx="160" cy="112" rx="36" ry="74" fill="#e8a8a0" opacity=".6"/>';
      s += '<circle cx="160" cy="50" r="6" fill="#c97a74"/><circle cx="160" cy="86" r="4" fill="#7a2a2a"/><ellipse cx="160" cy="130" rx="12" ry="22" fill="#7a2a2a" opacity=".8"/>';
      s += T(250, 54, 'clitoris', 'dg-tm') + T(250, 90, 'meatus', i === 2 ? 'dg-ta' : 'dg-tm') + T(250, 134, 'vagina', 'dg-tm');
      s += H.ln(168, 50, 244, 50, 'dg-thin') + H.ln(166, 86, 244, 86, 'dg-thin') + H.ln(174, 130, 244, 130, 'dg-thin');
      if (i === 1) s += H.arrow(130, 112, 92, 112, 'dg-ar') + H.arrow(190, 112, 228, 112, 'dg-ar');
      if (i === 2) s += '<circle cx="160" cy="86" r="10" fill="none" stroke="var(--warn)" stroke-width="3"/>';
      if (i === 3) s += H.arrow(140, 40, 140, 180, 'dg-arr') + T(110, 110, 'front to back', 'dg-tr', 'end');
      return S(320, 210, s, 'Female catheter');
    }});

  /* ================= ECG and imaging ================= */
  d('ecgrate', {t: 'ECG rate in 5 seconds: 300, 150, 100, 75, 60, 50', caps: ['Find an R wave on a thick line.', '**Count the big squares to the next R: 300, 150, 100, 75, 60, 50.**', 'Here it lands on the 4th line: **75 a minute**.', 'Irregular? **Count the QRS complexes on the 10-second strip and multiply by 6.**'],
    draw: function (i) {
      var s = '';
      for (var x = 20; x <= 320; x += 8) s += '<line x1="' + x + '" y1="30" x2="' + x + '" y2="150" style="stroke:var(--bad);stroke-opacity:' + ((x - 20) % 40 ? 0.12 : 0.35) + '"/>';
      for (var y = 30; y <= 150; y += 8) s += '<line x1="20" y1="' + y + '" x2="320" y2="' + y + '" style="stroke:var(--bad);stroke-opacity:' + ((y - 30) % 40 ? 0.12 : 0.35) + '"/>';
      var beat = function (x) { return 'L' + (x - 6) + ' 110 L' + x + ' 50 L' + (x + 6) + ' 120 L' + (x + 10) + ' 110'; };
      s += '<path d="M20 110 ' + beat(60) + ' L' + 200 + ' 110 ' + beat(220) + ' L320 110" class="dg-ln" style="stroke-width:2"/>';
      if (i >= 1) ['300', '150', '100', '75'].forEach(function (n, k) { var xx = 100 + k * 40; s += T(xx, 24, n, xx === 220 && i >= 2 ? 'dg-tr' : 'dg-ta', 'middle', 11); });
      if (i === 2) s += H.tag(220, 172, '75 a minute', 'b', 'middle');
      if (i === 3) s += H.tag(170, 172, 'irregular: QRS in 10 s × 6', 'w', 'middle');
      return S(330, 184, s, 'ECG rate');
    }});
  d('axis', {t: 'Axis: look at lead I and aVF', caps: ['**Both up = normal axis.** Thumbs up, thumbs up.', '**I up, aVF down = left axis deviation:** they are Leaving each other. Then check lead II.', '**I down, aVF up = right axis deviation:** they are Reaching for each other.', 'Left: LBBB, inferior MI, LVH. Right: RVH, PE, lateral MI, tall thin people.'],
    draw: function (i) {
      var mini = function (x, up, lab) { var y = 100; return T(x, 50, lab, 'dg-tb', 'middle', 12) + '<path d="M' + (x - 30) + ' ' + y + ' L' + (x - 6) + ' ' + y + ' L' + x + ' ' + (up ? y - 36 : y + 6) + ' L' + (x + 6) + ' ' + (up ? y + 6 : y + 36) + ' L' + (x + 12) + ' ' + y + ' L' + (x + 30) + ' ' + y + '" class="dg-ln" style="stroke-width:2.4"/>'; };
      var st = [[1, 1], [1, 0], [0, 1], [1, 1]][i];
      var s = mini(90, st[0], 'I') + mini(230, st[1], 'aVF');
      s += H.tag(160, 170, ['Normal', 'Left: leaving', 'Right: reaching', 'Causes'][i], i ? 'w' : 'g', 'middle');
      if (i === 1) s += H.arrow(140, 100, 110, 100, 'dg-arr') + H.arrow(180, 100, 210, 100, 'dg-arr');
      if (i === 2) s += H.arrow(120, 100, 150, 100, 'dg-arr') + H.arrow(200, 100, 170, 100, 'dg-arr');
      return S(320, 186, s, 'ECG axis');
    }});
  d('ecgblocks', {t: 'Heart block in 4 strips', caps: ['**First degree:** PR over 0.2 s, every P conducted. Usually harmless.', '**Mobitz I, Wenckebach:** PR gets longer and longer, then a beat drops.', '**Mobitz II:** PR fixed, then suddenly a P with no QRS. Risk of complete block: pace.', '**Complete block:** P waves and QRS march to their own beat. Slow wide escape; pace.'],
    draw: function (i) {
      var M = window.MEV && MEV.ECG ? MEV.ECG : {}, k = ['hb1', 'mob1', 'mob2', 'chb'][i];
      var h = M[k] ? M[k]() : '';
      return '<div class="dg-img dg-img-ecg">' + h + '</div>';
    }});
  d('hfcxr', {t: 'Heart failure on a chest X-ray: ABCDE', cards: [
    ['🦇', 'A · Alveolar oedema', 'Bat\'s-wing shadowing around the hila.'], ['➖', 'B · Kerley B lines', 'Short horizontal lines at the edges of the lower zones.'],
    ['❤️', 'C · Cardiomegaly', 'Heart over half the chest width on a PA film.'], ['⬆️', 'D · Diversion', 'Upper lobe vessels as big as the lower ones.'], ['💧', 'E · Effusions', 'Blunted costophrenic angles.']]});
  d('ctwin', {t: 'CT windows: the same slice, two ways', caps: ['**Soft tissue window:** organs, vessels and contrast show; the lungs are just black.', '**Lung window:** the lungs show their vessels and any nodule; everything else looks washed out.', 'Always say which window. A **PE needs the soft tissue window**; a **lung nodule needs the lung window**.'],
    draw: function (i) {
      var k = i === 1 ? 'mass' : 'pe';
      return '<div class="dg-img" style="max-width:300px;margin:0 auto">' + DG.ct(k) + '</div>';
    }});
  d('insulin', {t: 'Insulin: background vs mealtime', caps: ['**Basal, long-acting:** a flat line all day and night. **Never stop it, even when ill or not eating.**', '**Bolus, rapid-acting:** a peak with each meal, gone in a few hours.', '**Together = basal-bolus:** copies a working pancreas.', '**Hypo risk is highest** a couple of hours after a bolus, and overnight after alcohol or exercise.'],
    draw: function (i) {
      var s = H.ln(30, 160, 310, 160, 'dg-thin') + H.ln(30, 20, 30, 160, 'dg-thin');
      [['08', 60], ['13', 140], ['19', 230]].forEach(function (m) { s += T(m[1], 176, m[0] + ':00 🍽️', 'dg-tm', 'middle'); });
      if (i === 0 || i >= 2) s += '<path d="M30 120 L310 120" style="stroke:var(--accent);stroke-width:4"/>' + T(300, 112, 'basal', 'dg-ta', 'end');
      if (i >= 1) [60, 140, 230].forEach(function (x) { s += '<path d="M' + x + ' ' + (i >= 2 ? 120 : 160) + ' Q' + (x + 16) + ' ' + (i >= 2 ? 40 : 80) + ' ' + (x + 50) + ' ' + (i >= 2 ? 120 : 160) + '" style="stroke:var(--warn);stroke-width:3;fill:none"/>'; });
      if (i === 3) s += '<circle cx="96" cy="140" r="8" class="dg-bl"/><circle cx="290" cy="140" r="8" class="dg-bl"/>' + T(160, 30, 'hypo danger points', 'dg-tr', 'middle');
      return S(320, 186, s, 'Insulin profiles');
    }});
  d('doac', {t: 'DOAC vs warfarin', head: ['', 'DOAC: apixaban, rivaroxaban', 'Warfarin'], keep: true, rows: [
    ['Blood tests', 'No INR; **kidneys at least yearly**', '**INR** regularly, target usually 2 to 3'], ['Food', 'No diet rules', '**Keep vitamin K steady**: green veg; no cranberry juice'],
    ['Interactions', 'Fewer', '**Many**: antibiotics, alcohol, St John\'s wort'], ['Used for', 'Most AF, DVT and PE', '**Metal valves**, severe kidney disease, antiphospholipid'],
    ['Reversal', 'Specific antidotes', 'Vitamin K and clotting factors'], ['Both', '**Black, Blood, Brain → A&E**', 'Avoid NSAIDs; carry the card']],
    caps: ['DOACs need no INR but **do** need kidney checks.', 'Warfarin is the one with the **diet rules**.', 'Warfarin interacts with almost everything.', '**Metal valve = warfarin.** DOACs are not for mechanical valves.', 'Both can be reversed.', 'The counselling that matters for both: **bleeding red flags**.']});

  /* ================= more history patterns ================= */
  d('palpit', {t: 'Palpitations: tap it out, then how it starts', caps: ['**"Can you tap out how it felt?"** Regular or irregular in 5 seconds.', '**Fast, regular, switches on and off like a light** = SVT. Vagal manoeuvres stop it.', '**Irregularly irregular** = AF. Ask stroke risk factors for CHA2DS2-VASc.', '**Builds up and settles gradually,** with a trigger = sinus tachycardia: anxiety, fever, anaemia, thyroid, caffeine.', '🚩 **With a blackout, chest pain or breathlessness, or on exertion** = same-day ECG and cardiology.'],
    draw: function (i) {
      var s = H.ln(20, 170, 310, 170, 'dg-thin');
      var reg = function (y, gap, x0, x1) { var p = 'M' + x0 + ' ' + y; for (var x = x0; x < x1; x += gap) p += ' L' + (x + gap * 0.4) + ' ' + y + ' l3 -26 l3 34 l3 -8 L' + (x + gap) + ' ' + y; return p; };
      if (i === 0) s += T(160, 90, '👆 tap · tap · tap', 'dg-tb', 'middle', 18);
      if (i === 1) s += '<path d="M20 120 L90 120 ' + reg(120, 16, 90, 240).slice(10) + ' L310 120" class="dg-ln" style="stroke-width:2"/>' + T(90, 150, 'on', 'dg-tr', 'middle') + T(240, 150, 'off', 'dg-tr', 'middle');
      if (i === 2) { var p = 'M20 120', x = 20, g = [14, 30, 18, 40, 12, 26, 34, 16, 22, 38, 14]; g.forEach(function (gg) { p += ' L' + (x + gg * 0.5) + ' 120 l3 -26 l3 34 l3 -8 L' + (x + gg) + ' 120'; x += gg; }); s += '<path d="' + p + '" class="dg-ln" style="stroke-width:2"/>' + T(160, 150, 'no pattern at all', 'dg-tr', 'middle'); }
      if (i === 3) { var q = 'M20 120', xx = 20; [34, 30, 26, 22, 20, 20, 22, 26, 30, 34].forEach(function (gg) { q += ' L' + (xx + gg * 0.5) + ' 120 l3 -26 l3 34 l3 -8 L' + (xx + gg) + ' 120'; xx += gg; }); s += '<path d="' + q + '" class="dg-ln" style="stroke-width:2"/>' + T(160, 150, 'speeds up slowly, slows down slowly', 'dg-tr', 'middle'); }
      if (i === 4) s += box(30, 50, 260, 90, '🚩 Blackout · chest pain|breathless · on exercise|sudden death in the family under 40', 'dg-bl', null, 11);
      return S(320, 180, s, 'Palpitations');
    }});
  d('sobtime', {t: 'Breathlessness: how fast it came on', caps: ['**Seconds to minutes:** PE, pneumothorax, anaphylaxis, an inhaled object.', '**Hours to days:** pneumonia, an asthma or COPD flare, heart failure, an effusion.', '**Weeks to months:** COPD, fibrosis, anaemia, lung cancer, a slowly failing heart.', 'Then **what makes it worse:** lying flat or waking at night = heart failure; exercise, cold, night-time cough = asthma.'],
    draw: function (i) {
      var s = H.ln(20, 150, 310, 150, 'dg-thin');
      var lab = [['seconds', 40], ['hours to days', 150], ['weeks to months', 260]];
      lab.forEach(function (l, k) { s += '<g class="' + on(k === i || i === 3) + '"><rect x="' + (l[1] - 50) + '" y="60" width="100" height="70" rx="10" class="' + (k === 0 ? 'dg-bl' : k === 1 ? 'dg-wl' : 'dg-hl') + '"/>' + T(l[1], 100, ['⚡', '🌤️', '🐢'][k], '', 'middle', 26) + T(l[1], 172, l[0], 'dg-tb', 'middle') + '</g>'; });
      if (i < 3) s += T(160, 30, [['PE · pneumothorax · anaphylaxis'], ['pneumonia · asthma · HF · effusion'], ['COPD · fibrosis · anaemia · cancer']][i][0], 'dg-ta', 'middle', 11);
      else s += T(160, 30, 'lying flat → heart · cold and exercise → asthma', 'dg-ta', 'middle', 11);
      return S(320, 186, s, 'Breathlessness timing');
    }});
  d('legswell', {t: 'Swollen legs: one or both?', caps: ['**One leg, hot, tender, calf bigger by 3 cm** = DVT until proven otherwise. Wells score, D-dimer or scan.', '**One leg, red, hot, spreading, feverish** = cellulitis. Mark the edge.', '**Both legs, pitting** = something general: heart failure, low albumin from the liver or kidney, or a drug such as amlodipine.', '**Both legs, plus breathless lying flat** = heart failure: NT-proBNP.'],
    draw: function (i) {
      var leg = function (x, fat, cls) { var w = fat ? 30 : 22; return '<path d="M' + (x - w / 2) + ' 30 L' + (x - w / 2 + 2) + ' 160 Q' + x + ' 176 ' + (x + w / 2 + 14) + ' 172 L' + (x + w / 2) + ' 156 L' + (x + w / 2) + ' 30 Z" class="' + (cls || 'dg-skin') + '"/>'; };
      var both = i >= 2, s = leg(120, both, both ? 'dg-wl' : '') + leg(200, true, i === 1 ? 'dg-bl' : 'dg-wl');
      if (i === 0) s += H.ln(176, 110, 226, 110, 'dg-dash') + T(250, 114, '+3 cm', 'dg-tr');
      if (i === 1) s += H.p('M184 70 Q206 60 220 80 Q226 110 210 130 Q188 136 182 112', 'dg-ar') + T(256, 70, 'mark the edge', 'dg-ta', 'middle');
      if (i >= 2) s += '<circle cx="120" cy="130" r="5" class="dg-ink"/>' + T(70, 134, 'pits', 'dg-ta', 'end');
      if (i === 3) s += H.tag(160, 16, 'breathless lying flat → HF', 'b', 'middle');
      s += T(120, 192, 'right', 'dg-tm', 'middle') + T(200, 192, 'left', 'dg-tm', 'middle');
      return S(320, 200, s, 'Leg swelling');
    }});
})();
