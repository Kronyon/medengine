/* medengine-OSCE v1.3: examination pictures. */
(function () {
  var d = DG.def, H = DG.H, S = H.svg, T = H.t, on = H.on;

  /* ---------- heart: where to listen ---------- */
  d('ausc', {t: 'Where to listen: All Physicians Take Money', caps: [
    '**A · Aortic:** 2nd space, **right** of the sternum. Aortic stenosis is loudest here.', '**P · Pulmonary:** 2nd space, **left** of the sternum.',
    '**T · Tricuspid:** 4th space at the left sternal edge.', '**M · Mitral:** 5th space in the midclavicular line, the apex.',
    '**Mitral stenosis:** roll onto the left side, breathe out, listen at the apex with the **bell**.', '**Aortic regurgitation:** sit forward, breathe out, listen at the left sternal edge with the diaphragm.',
    'Keep a finger on the **carotid** the whole time: a murmur with the pulse is systolic.'],
    draw: function (i) {
      var s = H.torso(55, 22, 210, 200), P = [[141, 66, 'A'], [179, 66, 'P'], [172, 116, 'T'], [208, 136, 'M']];
      s += H.p('M100 40 Q130 44 154 48 M166 48 Q190 44 220 40', 'dg-ln');
      s += H.r(153, 46, 14, 104, 'dg-thin', 4);
      [60, 80, 100, 120, 140].forEach(function (y) { s += H.p('M152 ' + y + ' Q125 ' + (y - 8) + ' 82 ' + (y + 8), 'dg-thin') + H.p('M168 ' + y + ' Q195 ' + (y - 8) + ' 238 ' + (y + 8), 'dg-thin'); });
      s += T(160, 14, 'patient\'s right   ·   patient\'s left', 'dg-tm', 'middle');
      P.forEach(function (p, k) { var hot = i === k || (i === 4 && k === 3) || (i === 5 && k === 2); s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="11" class="dg-pt' + (hot ? ' dg-on' : '') + '"/>' + T(p[0], p[1] + 4, p[2], hot ? 'dg-tb dg-srf' : 'dg-ta', 'middle', 12, hot ? ' style="fill:var(--on-accent)"' : ''); });
      if (i < 4) s += H.tag([126, 194, 158, 208][i], [P[0][1] - 16, P[1][1] - 16, P[2][1] + 2, P[3][1] + 26][i], ['Aortic · 2nd right', 'Pulmonary · 2nd left', 'Tricuspid · 4th left edge', 'Mitral · 5th, midclavicular'][i], '', ['end', 'start', 'end', 'middle'][i]);
      if (i === 4) s += H.tag(226, 160, '🔔 bell · left side · breath out', 'w', 'middle');
      if (i === 5) s += H.tag(172, 150, 'sit forward · breath out', 'w', 'middle');
      if (i === 6) s += H.c(146, 18, 7, 'dg-pt dg-on') + H.tag(150, 36, 'carotid: time it', 'w', 'start');
      return S(320, 230, s, 'Chest with the four listening areas');
    }});

  /* ---------- murmur shapes ---------- */
  d('murmurs', {t: 'Murmur shapes: draw them between S1 and S2', caps: [
    '**Aortic stenosis:** ejection systolic, a diamond that rises then falls. Right 2nd space → **carotids**. Slow-rising pulse, soft S2.',
    '**Mitral regurgitation:** pansystolic, a flat block from S1 right to S2. Apex → **axilla**.',
    '**Aortic regurgitation:** early diastolic, starts loud at S2 then fades. Left sternal edge, sitting forward. Collapsing pulse.',
    '**Mitral stenosis:** a low rumble in mid-diastole, loudest just before S1. Apex, bell, left side. Loud S1, malar flush, AF.'],
    draw: function (i) {
      var s = '', y = 118;
      s += T(115, 24, 'SYSTOLE', 'dg-tm', 'middle') + T(225, 24, 'DIASTOLE', 'dg-tm', 'middle');
      s += H.ln(20, y, 300, y, 'dg-thin');
      [[60, 'S1'], [170, 'S2'], [280, 'S1']].forEach(function (p) { s += H.r(p[0] - 3, 40, 6, y - 40, 'dg-acc', 2) + T(p[0], y + 18, p[1], 'dg-tb', 'middle'); });
      var shp = [
        'M68 ' + y + ' L115 52 L162 ' + y + ' Z',
        'M64 ' + y + ' L64 66 L166 66 L166 ' + y + ' Z',
        'M174 ' + y + ' L174 52 L262 ' + y + ' Z',
        'M190 ' + y + ' C200 100 208 108 216 100 C224 92 232 104 240 96 C252 84 262 74 274 62 L274 ' + y + ' Z'][i];
      s += H.p(shp, 'dg-wl');
      if (i === 3) s += H.ln(186, y, 186, 92, 'dg-ln') + T(186, 86, 'snap', 'dg-tm', 'middle');
      s += T(160, 150, ['Aortic stenosis → carotids', 'Mitral regurgitation → axilla', 'Aortic regurgitation · sit forward', 'Mitral stenosis · bell at the apex'][i], 'dg-ta', 'middle', 12);
      return S(320, 160, s, 'Murmur timing');
    }});

  /* ---------- lungs: where to percuss and listen ---------- */
  d('lungs', {t: 'Chest: compare side to side, front then back', caps: [
    '**Apices:** above the collarbones. Always compare the same spot on each side.', '**Upper zones** at the front.', '**Middle and lower** at the front.',
    '**Axillae:** the side of the chest; easy to forget.', '**Back:** ask them to cross their arms to move the shoulder blades.', '**Back, middle.**', '**Bases:** the lower lobes are mostly at the back.'],
    draw: function (i) {
      var s = H.torso(14, 30, 140, 180) + H.torso(166, 30, 140, 180);
      s += T(84, 20, 'FRONT', 'dg-tm', 'middle') + T(236, 20, 'BACK', 'dg-tm', 'middle');
      s += H.r(78, 46, 12, 90, 'dg-thin', 4) + H.ln(236, 40, 236, 200, 'dg-dash');
      s += H.p('M190 60 Q205 90 200 120 M282 60 Q267 90 272 120', 'dg-thin');
      var F = [[[54, 46], [114, 46]], [[54, 80], [114, 80]], [[56, 118], [112, 118]], [[24, 120], [144, 120]]],
          B = [[[208, 72], [264, 72]], [[206, 116], [266, 116]], [[204, 160], [268, 160]]], n = 0;
      F.concat(B).forEach(function (pr, k) { pr.forEach(function (p) { n++; s += H.c(p[0], p[1], 8, 'dg-pt' + (k === i ? ' dg-on' : '')) + T(p[0], p[1] + 3.5, String(n), k === i ? '' : 'dg-tm', 'middle', 9, k === i ? ' style="fill:var(--on-accent);font-weight:700"' : ''); }); if (k === i) s += H.p('M' + (pr[0][0] + 10) + ' ' + (pr[0][1] - 10) + ' Q' + ((pr[0][0] + pr[1][0]) / 2) + ' ' + (pr[0][1] - 26) + ' ' + (pr[1][0] - 10) + ' ' + (pr[1][1] - 10), 'dg-ar'); });
      return S(320, 215, s, 'Percussion and auscultation sites');
    }});

  /* ---------- eye movements ---------- */
  d('eyeH', {t: 'Eye movements: the H, with the nerve for each muscle', ms: 1800, caps: [
    'Start in the middle. **Head still**, follow my finger, tell me if you see double.', '**Out: lateral rectus, VI.** LR6.', '**Out and up: superior rectus, III.**',
    '**Out and down: inferior rectus, III.**', '**In: medial rectus, III.**', '**In and up: inferior oblique, III.**', '**In and down: superior oblique, IV.** SO4. The one you need to walk down stairs.'],
    draw: function (i) {
      var pos = [[0, 0], [-34, 0], [-30, -16], [-30, 16], [34, 0], [30, -16], [30, 16]][i], cx = 160 + pos[0], cy = 96 + pos[1], s = '', id = H.uid();
      s += H.p('M116 72 L116 120 M204 72 L204 120 M116 96 L204 96', 'dg-dash');
      s += '<clipPath id="' + id + '"><path d="M86 96 Q160 34 234 96 Q160 158 86 96 Z"/></clipPath>';
      s += H.p('M86 96 Q160 34 234 96 Q160 158 86 96 Z', 'dg-skin');
      s += '<g clip-path="url(#' + id + ')"><circle cx="' + cx + '" cy="' + cy + '" r="27" fill="#4f7f9c" style="transition:all .5s"/><circle cx="' + cx + '" cy="' + cy + '" r="11" fill="#0d1418" style="transition:all .5s"/><circle cx="' + (cx + 6) + '" cy="' + (cy - 7) + '" r="3.5" fill="#fff" opacity=".8"/></g>';
      s += H.p('M86 96 Q160 34 234 96 Q160 158 86 96 Z', 'dg-ln');
      s += T(70, 100, 'lateral', 'dg-tm', 'end') + T(250, 100, 'medial', 'dg-tm');
      s += T(160, 22, 'Patient\'s RIGHT eye, as you face them', 'dg-tm', 'middle');
      if (i) s += H.tag(160, 178, ['', 'Lateral rectus · VI', 'Superior rectus · III', 'Inferior rectus · III', 'Medial rectus · III', 'Inferior oblique · III', 'Superior oblique · IV'][i], i === 1 || i === 6 ? 'w' : '', 'middle');
      return S(320, 190, s, 'Eye movement directions');
    }});

  /* ---------- visual pathway and field defects ---------- */
  function field(cx, cy, r, black, spare) {
    var q = {UL: 'M' + cx + ' ' + cy + ' L' + (cx - r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 0 1 ' + cx + ' ' + (cy - r) + ' Z', UR: 'M' + cx + ' ' + cy + ' L' + cx + ' ' + (cy - r) + ' A' + r + ' ' + r + ' 0 0 1 ' + (cx + r) + ' ' + cy + ' Z',
             LR: 'M' + cx + ' ' + cy + ' L' + (cx + r) + ' ' + cy + ' A' + r + ' ' + r + ' 0 0 1 ' + cx + ' ' + (cy + r) + ' Z', LL: 'M' + cx + ' ' + cy + ' L' + cx + ' ' + (cy + r) + ' A' + r + ' ' + r + ' 0 0 1 ' + (cx - r) + ' ' + cy + ' Z'};
    var s = '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" style="stroke:var(--muted)"/>';
    black.forEach(function (k) { s += '<path d="' + q[k] + '" fill="#141414"/>'; });
    if (spare) s += '<circle cx="' + cx + '" cy="' + cy + '" r="6" fill="#fff"/>';
    return s + '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" style="stroke:var(--muted)"/>';
  }
  d('fields', {t: 'Where is the lesion? Read it from the field', caps: [
    '**Right optic nerve:** the right eye sees nothing. Think optic neuritis, CRAO, glaucoma.', '**Optic chiasm:** both outer halves lost, **bitemporal hemianopia**. Pituitary adenoma pressing from below.',
    '**Right optic tract:** the same half of space lost in both eyes, **left homonymous hemianopia**.', '**Right temporal lobe:** upper left quarter in both eyes. **Pie in the sky.**',
    '**Right parietal lobe:** lower left quarter. **Pie on the floor.**', '**Right occipital cortex:** left homonymous hemianopia **with macular sparing**. Posterior cerebral artery stroke.'],
    draw: function (i) {
      var s = '', L = [[0, ['UR', 'LR'], 'nothing'], [[], []]][0];
      s += '<circle cx="118" cy="26" r="13" class="dg-skin"/><circle cx="202" cy="26" r="13" class="dg-skin"/><circle cx="118" cy="26" r="5" class="dg-ink"/><circle cx="202" cy="26" r="5" class="dg-ink"/>';
      s += T(118, 8, 'LEFT eye', 'dg-tm', 'middle') + T(202, 8, 'RIGHT eye', 'dg-tm', 'middle');
      // nasal fibres cross, temporal fibres don't
      s += H.p('M113 38 L160 82 L198 122', 'dg-thin') + H.p('M207 38 L160 82 L122 122', 'dg-thin') + H.p('M123 38 Q140 70 124 122', 'dg-ln') + H.p('M197 38 Q180 70 196 122', 'dg-ln');
      s += H.c(124, 124, 4, 'dg-ink') + H.c(196, 124, 4, 'dg-ink');
      s += H.p('M124 126 Q92 152 140 184 M124 126 Q122 156 142 184 M196 126 Q228 152 180 184 M196 126 Q198 156 178 184', 'dg-thin');
      s += H.p('M128 188 Q160 198 192 188', 'dg-ln') + T(160, 210, 'occipital cortex', 'dg-tm', 'middle');
      var site = [[184, 56], [160, 82], [186, 104], [216, 152], [196, 152], [182, 188]][i];
      s += '<rect x="' + (site[0] - 10) + '" y="' + (site[1] - 3) + '" width="20" height="6" rx="3" class="dg-red" transform="rotate(-30 ' + site[0] + ' ' + site[1] + ')"/>';
      var Lf = [[], ['UL', 'LL'], ['UL', 'LL'], ['UL'], ['LL'], ['UL', 'LL']][i], Rf = [['UL', 'UR', 'LL', 'LR'], ['UR', 'LR'], ['UL', 'LL'], ['UL'], ['LL'], ['UL', 'LL']][i];
      s += field(250, 70, 24, Lf, i === 5) + field(250, 150, 24, Rf, i === 5);
      s += T(250, 38, 'left eye field', 'dg-tm', 'middle') + T(250, 118, 'right eye field', 'dg-tm', 'middle');
      s += T(226, 192, 'black = cannot see', 'dg-tm');
      return S(320, 220, s, 'Visual pathway');
    }});

  /* ---------- facial nerve: UMN vs LMN ---------- */
  function face(cx, cy, kind, lab) {
    var s = '<ellipse cx="' + cx + '" cy="' + cy + '" rx="52" ry="66" class="dg-skin"/>';
    var droopL = kind !== 'n';
    // forehead lines: absent on the affected side (viewer's left) in LMN
    [-46, -38].forEach(function (dy) { s += H.p('M' + (cx + 6) + ' ' + (cy + dy) + ' q14 -4 28 0', 'dg-thin'); if (kind !== 'lmn') s += H.p('M' + (cx - 34) + ' ' + (cy + dy) + ' q14 -4 28 0', 'dg-thin'); });
    s += H.p('M' + (cx - 32) + ' ' + (cy - (kind === 'lmn' ? 18 : 24)) + ' q12 -6 22 0', 'dg-ln') + H.p('M' + (cx + 10) + ' ' + (cy - 24) + ' q12 -6 22 0', 'dg-ln');
    s += '<ellipse cx="' + (cx - 21) + '" cy="' + (cy - 10) + '" rx="9" ry="' + (kind === 'lmn' ? 6 : 4) + '" class="dg-srf" style="stroke:var(--ink)"/><ellipse cx="' + (cx + 21) + '" cy="' + (cy - 10) + '" rx="9" ry="4" class="dg-srf" style="stroke:var(--ink)"/>';
    s += H.p('M' + cx + ' ' + (cy - 4) + ' l-4 18 h8', 'dg-thin');
    s += H.p(droopL ? 'M' + (cx - 22) + ' ' + (cy + 36) + ' Q' + (cx - 4) + ' ' + (cy + 34) + ' ' + (cx + 20) + ' ' + (cy + 28) : 'M' + (cx - 20) + ' ' + (cy + 30) + ' Q' + cx + ' ' + (cy + 38) + ' ' + (cx + 20) + ' ' + (cy + 30), 'dg-ln');
    if (droopL) s += H.p('M' + (cx - 34) + ' ' + (cy + 16) + ' q4 10 10 18', 'dg-thin');
    return s + T(cx, cy + 86, lab, 'dg-ta', 'middle');
  }
  d('face7', {t: 'Facial weakness: is the forehead spared?', caps: [
    '**Stroke, an upper motor neurone lesion:** the lower face droops but the **forehead still wrinkles**, because the forehead gets nerve supply from both sides of the brain.',
    '**Bell\'s palsy, a lower motor neurone lesion:** the **whole side** is weak, forehead included; the eye won\'t close. Check the ear for vesicles: Ramsay Hunt.',
    '**Forehead spared = stroke. Forehead frozen too = Bell\'s.**'],
    draw: function (i) {
      var s = '<g class="' + on(i !== 1) + '">' + face(82, 82, 'umn', 'Stroke · forehead spared') + '</g><g class="' + on(i !== 0) + '">' + face(238, 82, 'lmn', 'Bell\'s · whole side') + '</g>';
      return S(320, 180, s, 'Facial nerve palsy');
    }});

  /* ---------- dermatomes ---------- */
  d('dermUL', {t: 'Arm dermatomes: test each with a sternum reference', caps: [
    '**C5:** outer upper arm, the regimental badge patch.', '**C6:** outer forearm and **thumb**. Six-shooter: make a gun with the thumb and index.', '**C7:** the **middle finger**.',
    '**C8:** the **little finger** and the inner hand.', '**T1:** inner forearm, up towards the elbow.'],
    draw: function (i) {
      var s = '', arm = 'M118 14 L182 14 L180 108 L176 186 L130 186 L122 108 Z';
      s += H.p(arm, 'dg-skin') + H.r(128, 186, 46, 30, 'dg-skin', 6);
      var fingers = [[108, 192, 10, 30, -24], [131, 214, 9, 26], [142, 214, 9, 30], [153, 214, 9, 27], [164, 214, 8, 22]];
      fingers.forEach(function (f) { s += '<rect x="' + f[0] + '" y="' + f[1] + '" width="' + f[2] + '" height="' + f[3] + '" rx="4" class="dg-skin"' + (f[4] ? ' transform="rotate(' + f[4] + ' ' + (f[0] + 5) + ' ' + f[1] + ')"' : '') + '/>'; });
      var R = [
        '<path d="M119 18 L150 18 L148 80 L121 86 Z" class="dg-wl"/>',
        '<path d="M123 112 L150 112 L148 186 L131 186 Z" class="dg-wl"/><rect x="108" y="192" width="10" height="30" rx="4" class="dg-wl" transform="rotate(-24 113 192)"/>',
        '<rect x="142" y="214" width="9" height="30" rx="4" class="dg-wl"/><rect x="140" y="188" width="12" height="26" class="dg-wl"/>',
        '<rect x="164" y="214" width="8" height="22" rx="4" class="dg-wl"/><rect x="153" y="214" width="9" height="27" rx="4" class="dg-wl" opacity=".6"/><path d="M160 150 L177 150 L176 186 L172 214 L160 214 Z" class="dg-wl"/>',
        '<path d="M152 112 L180 112 L178 150 L152 150 Z" class="dg-wl"/>'][i];
      s += R + T(96, 60, 'outer', 'dg-tm', 'end') + T(206, 60, 'inner', 'dg-tm');
      s += H.tag(250, 30, ['C5', 'C6', 'C7', 'C8', 'T1'][i], 'w', 'middle');
      return S(320, 250, s, 'Arm dermatomes');
    }});
  d('dermLL', {t: 'Leg dermatomes', caps: [
    '**L3:** front of the lower thigh, just above the knee.', '**L4:** inside of the shin down to the inner ankle. **L4 = knee jerk and ankle dorsiflexion.**',
    '**L5:** outside of the shin, top of the foot and the **big toe**. Big toe extension is the L5 test.', '**S1:** outside edge of the foot, the little toe and the sole. **S1 = ankle jerk.**',
    '**S3 to S5: the saddle.** Numb saddle + retention + weak legs = cauda equina: emergency MRI.'],
    draw: function (i) {
      var s = H.p('M118 10 L184 10 L180 106 L172 202 L130 202 L122 106 Z', 'dg-skin') + H.p('M126 202 L176 202 Q186 224 176 236 L126 236 Q118 222 126 202 Z', 'dg-skin');
      [[128, 236, 7], [138, 238, 7], [148, 239, 8], [158, 240, 9], [170, 240, 11]].forEach(function (t) { s += '<ellipse cx="' + t[0] + '" cy="' + (t[1] + 4) + '" rx="' + (t[2] / 2) + '" ry="6" class="dg-skin"/>'; });
      s += T(100, 140, 'outer', 'dg-tm', 'end') + T(200, 140, 'inner', 'dg-tm');
      var R = [
        '<path d="M122 74 L182 80 L181 102 L122 96 Z" class="dg-wl"/>',
        '<path d="M154 110 L180 108 L174 200 L156 202 Z" class="dg-wl"/>',
        '<path d="M126 132 L150 132 L150 202 L130 202 Z" class="dg-wl"/><path d="M136 204 L166 204 L168 232 L136 232 Z" class="dg-wl"/><ellipse cx="170" cy="244" rx="6" ry="6" class="dg-wl"/>',
        '<path d="M124 204 L136 204 L136 236 L122 232 Z" class="dg-wl"/><ellipse cx="128" cy="240" rx="4" ry="6" class="dg-wl"/>',
        '<circle cx="250" cy="120" r="34" class="dg-wl"/>'][i];
      s += R + (i === 4 ? T(250, 124, 'saddle', 'dg-tb', 'middle') : '');
      s += H.tag(250, 30, ['L3', 'L4', 'L5', 'S1', 'S3 to S5'][i], 'w', 'middle');
      return S(320, 252, s, 'Leg dermatomes');
    }});

  /* ---------- abdomen: 9 regions ---------- */
  var REG = [['Right upper quadrant: right hypochondrium', 'Liver, gallbladder'], ['Epigastrium', 'Stomach, pancreas, duodenum'], ['Left hypochondrium', 'Spleen, stomach'],
    ['Right flank', 'Right kidney, ascending colon'], ['Umbilical', 'Small bowel, aorta'], ['Left flank', 'Left kidney, descending colon'],
    ['Right iliac fossa', 'Appendix, caecum, right ovary'], ['Suprapubic', 'Bladder, uterus'], ['Left iliac fossa', 'Sigmoid colon, left ovary']];
  function abdomen() { return H.p('M60 22 Q160 4 260 22 L262 206 Q160 226 58 206 Z', 'dg-skin') + H.p('M66 40 Q112 70 160 52 Q208 70 254 40', 'dg-thin') + H.c(160, 120, 3, 'dg-ink'); }
  d('abdo9', {t: 'The 9 regions and what lives in each', caps: REG.map(function (r) { return '**' + r[0] + ':** ' + r[1] + '.'; }),
    draw: function (i) {
      var xs = [58, 128, 192, 262], ys = [16, 84, 152, 214], s = abdomen();
      s += H.ln(128, 18, 128, 214, 'dg-dash') + H.ln(192, 18, 192, 214, 'dg-dash') + H.ln(60, 84, 262, 84, 'dg-dash') + H.ln(60, 152, 262, 152, 'dg-dash');
      var cx = i % 3, cy = Math.floor(i / 3);
      s += H.r(xs[cx] + 2, ys[cy] + 2, xs[cx + 1] - xs[cx] - 4, ys[cy + 1] - ys[cy] - 4, 'dg-hl', 6) + T((xs[cx] + xs[cx + 1]) / 2, (ys[cy] + ys[cy + 1]) / 2 + 4, ['Liver', 'Stomach', 'Spleen', 'R kidney', 'Bowel, aorta', 'L kidney', 'Appendix', 'Bladder', 'Sigmoid'][i], 'dg-tb', 'middle', 10);
      s += T(160, 236, 'patient\'s right on your left', 'dg-tm', 'middle');
      return S(320, 244, s, 'Abdominal regions');
    }});
  d('organs', {t: 'Palpating the organs', caps: [
    '**Liver:** start in the **right iliac fossa** and move up a hand\'s width with each breath in, so a huge liver isn\'t missed.',
    '**Spleen:** start in the right iliac fossa and go **diagonally** to the left upper quadrant. It has a notch and you can\'t get above it.',
    '**Kidneys:** one hand behind, one in front; **ballot**. You can get above a kidney.',
    '**Aorta:** two hands above the umbilicus. **Fingers pushed apart = expansile = aneurysm.**',
    '**Shifting dullness:** percuss to dull, keep your finger there, roll them towards you, wait 30 seconds, percuss again: now resonant = ascites.'],
    draw: function (i) {
      var s = abdomen();
      s += '<g class="' + on(i === 0) + '">' + H.p('M66 50 Q110 46 152 64 Q140 92 96 90 Q72 86 66 50 Z', 'dg-wl') + [196, 168, 140, 112].map(function (y, k) { return H.c(100, y, 4, 'dg-fa') + (k ? H.arrow(100, y + 24, 100, y + 6) : ''); }).join('') + '</g>';
      s += '<g class="' + on(i === 1) + '">' + H.p('M212 58 Q240 66 238 92 Q222 96 208 80 Z', 'dg-wl') + H.arrow(104, 196, 210, 88) + '</g>';
      s += '<g class="' + on(i === 2) + '"><ellipse cx="96" cy="128" rx="12" ry="20" class="dg-wl"/><ellipse cx="224" cy="128" rx="12" ry="20" class="dg-wl"/>' + H.arrow(70, 128, 84, 128) + H.arrow(250, 128, 236, 128) + '</g>';
      s += '<g class="' + on(i === 3) + '"><rect x="152" y="70" width="16" height="68" rx="8" class="dg-bl"/>' + H.arrow(156, 100, 136, 100, 'dg-arr') + H.arrow(164, 100, 184, 100, 'dg-arr') + '</g>';
      s += '<g class="' + on(i === 4) + '">' + H.p('M62 150 Q66 196 110 206 L110 150 Z M258 150 Q254 196 210 206 L210 150 Z', 'dg-hl') + T(160, 196, 'fluid sits in the flanks', 'dg-tm', 'middle') + '</g>';
      return S(320, 236, s, 'Organ palpation');
    }});

  /* ---------- thyroid ---------- */
  d('thyroid', {t: 'Thyroid: look, swallow, tongue, then feel from behind', caps: [
    'The thyroid sits **below the cricoid**, wrapped round the trachea like a bow tie.', '**Swallow:** a goitre **rises**, because the gland is attached to the larynx.',
    '**Stick the tongue out:** a **thyroglossal cyst rises**, because it is tethered to the tongue base.', '**Feel from behind** with both hands; ask them to swallow again. Check the nodes.'],
    draw: function (i) {
      var up = i === 1 ? -14 : 0, s = '';
      s += H.p('M104 10 L104 200 M216 10 L216 200', 'dg-ln') + H.p('M104 200 Q60 210 30 230 M216 200 Q260 210 290 230', 'dg-ln');
      s += '<g style="transition:transform .5s" transform="translate(0 ' + up + ')">' + H.p('M146 54 L160 74 L174 54', 'dg-ln') + H.r(144, 86, 32, 10, 'dg-thin', 5) + T(196, 62, 'thyroid cartilage', 'dg-tm') + T(196, 94, 'cricoid', 'dg-tm') + H.p('M158 112 C130 96 116 112 124 138 C130 156 150 152 158 128 Z M162 112 C190 96 204 112 196 138 C190 156 170 152 162 128 Z', 'dg-wl') + H.r(150, 112, 20, 12, 'dg-wl', 4) + '</g>';
      if (i === 1) s += H.p('M158 126 C130 110 116 126 124 152 C130 170 150 166 158 142 Z M162 126 C190 110 204 126 196 152 C190 170 170 166 162 142 Z', 'dg-dash') + H.arrow(220, 150, 220, 122);
      if (i === 2) s += H.c(160, 66, 9, 'dg-bl') + H.arrow(176, 70, 176, 50, 'dg-arr') + T(236, 40, 'cyst rises with the tongue', 'dg-tr', 'middle');
      if (i === 3) s += H.p('M80 120 Q110 112 126 126 M240 120 Q210 112 194 126', 'dg-ar') + T(160, 186, 'fingers on both lobes from behind', 'dg-ta', 'middle');
      return S(320, 236, s, 'Thyroid examination');
    }});

  /* ---------- MSK pictures ---------- */
  d('ottawa', {t: 'Ottawa rules: the 4 bony spots and 4 steps', caps: [
    '**Lateral malleolus:** tender at the **back edge or tip**, the lower 6 cm → ankle X-ray.', '**Medial malleolus:** back edge or tip, lower 6 cm → ankle X-ray.',
    '**Base of the 5th metatarsal** → foot X-ray.', '**Navicular** on the inside of the midfoot → foot X-ray.', '**Can\'t take 4 steps,** both straight after the injury and in the department → X-ray.'],
    draw: function (i) {
      var s = '';
      s += T(80, 16, 'OUTSIDE', 'dg-tm', 'middle') + T(240, 16, 'INSIDE', 'dg-tm', 'middle');
      s += H.p('M58 20 L58 100 Q56 128 34 136 L30 150 L150 150 Q150 136 128 128 L96 118 L84 104 L84 20 Z', 'dg-skin');
      s += H.p('M218 20 L218 100 Q216 128 196 136 L190 150 L310 150 Q306 132 286 128 L254 120 L244 104 L244 20 Z', 'dg-skin');
      s += '<g class="' + on(i === 0) + '">' + H.p('M82 50 L82 104', 'dg-arr') + H.c(80, 108, 7, 'dg-bl') + '</g>';
      s += '<g class="' + on(i === 1) + '">' + H.p('M242 50 L242 104', 'dg-arr') + H.c(240, 108, 7, 'dg-bl') + '</g>';
      s += '<g class="' + on(i === 2) + '">' + H.c(118, 138, 7, 'dg-bl') + '</g>';
      s += '<g class="' + on(i === 3) + '">' + H.c(266, 126, 7, 'dg-bl') + '</g>';
      s += '<g class="' + on(i === 4) + '">' + [0, 1, 2, 3].map(function (k) { return '<ellipse cx="' + (70 + k * 56) + '" cy="' + (k % 2 ? 178 : 190) + '" rx="10" ry="6" class="dg-hl"/>'; }).join('') + T(160, 206, '4 steps?', 'dg-ta', 'middle', 12) + '</g>';
      return S(320, 212, s, 'Ottawa ankle and foot rules');
    }});
  d('shoulder', {t: 'Shoulder: where in the arc does it hurt?', caps: [
    'Arm by the side. Ask them to raise it out sideways, **all the way up**, and tell you where it hurts.', '**Painful arc 60 to 120°:** the cuff tendon is pinched under the acromion. **Impingement or supraspinatus.**',
    '**Pain only at the very top, 160 to 180°:** the **ACJ**.', '**External rotation with the elbows tucked in:** lost first, **actively and passively**, in **frozen shoulder**.'],
    draw: function (i) {
      var cx = 168, cy = 84, R = 70, s = '', ang = [0, 90, 172, 0][i];
      var pt = function (a, r) { var t = a * Math.PI / 180; return [cx - r * Math.sin(t), cy + r * Math.cos(t)]; };
      var arc = function (a0, a1, st) { var d = ''; for (var a = a0; a <= a1; a += 3) { var q = pt(a, R); d += (d ? ' L' : 'M') + q[0].toFixed(1) + ' ' + q[1].toFixed(1); } return '<path d="' + d + '" style="fill:none;stroke-linecap:round;' + st + '"/>'; };
      s += '<circle cx="190" cy="40" r="15" class="dg-skin"/>' + H.p('M168 66 L212 66 L216 180 L164 180 Z', 'dg-skin');
      if (i < 3) {
        s += arc(0, 180, 'stroke:var(--line);stroke-width:8');
        s += arc(60, 120, 'stroke:var(--warn);stroke-width:8;opacity:' + (i === 1 ? 1 : 0.3));
        s += arc(160, 180, 'stroke:var(--bad);stroke-width:8;opacity:' + (i === 2 ? 1 : 0.3));
        var e = pt(ang, R - 12); s += '<line x1="' + cx + '" y1="' + cy + '" x2="' + e[0].toFixed(1) + '" y2="' + e[1].toFixed(1) + '" style="stroke:var(--muted);stroke-width:9;stroke-linecap:round"/>' + H.c(cx, cy, 5, 'dg-ink');
        s += T(cx - 6, cy + R + 14, '0°', 'dg-tm', 'middle') + T(cx - R - 14, cy + 4, '90°', 'dg-tm', 'middle') + T(cx, cy - R - 6, '180°', 'dg-tm', 'middle');
        if (i === 1) s += H.tag(60, 30, '60 to 120°: cuff', 'w', 'middle');
        if (i === 2) s += H.tag(250, 16, 'top: ACJ', 'b', 'middle');
      } else {
        s = '<circle cx="150" cy="120" r="7" class="dg-ink"/>' + H.p('M150 120 L150 60', 'dg-ln') + '<line x1="150" y1="120" x2="96" y2="96" style="stroke:var(--muted);stroke-width:8;stroke-linecap:round"/>' + H.p('M150 70 A50 50 0 0 0 104 90', 'dg-arr') + T(150, 150, 'seen from above: forearm swings outwards', 'dg-tm', 'middle') + H.tag(150, 172, 'lost actively AND passively = frozen', 'b', 'middle');
      }
      return S(320, 186, s, 'Shoulder abduction arc');
    }});
  d('hip', {t: 'Hip: Trendelenburg and Thomas\' tests', caps: [
    'Standing on both legs, the pelvis is level.', '**Normal:** standing on the right leg, the right hip abductors hold the pelvis level, or it rises on the left.',
    '**Positive Trendelenburg:** the pelvis **drops on the lifted side**, because the abductors on the standing side are weak. **The sound side sags.**',
    '**Thomas\' test:** bend the good hip fully with your hand under their back; if the other thigh lifts off the bed, there is a **fixed flexion deformity**.'],
    draw: function (i) {
      var s = '';
      if (i < 3) {
        var tilt = [0, -6, 9][i], lift = i > 0;
        s += '<g transform="rotate(' + tilt + ' 160 70)" style="transition:transform .6s">' + H.r(100, 60, 120, 20, 'dg-wl', 10) + '<circle cx="124" cy="80" r="6" class="dg-ink"/><circle cx="196" cy="80" r="6" class="dg-ink"/>' + H.c(160, 36, 14, 'dg-skin') + H.ln(160, 50, 160, 60, 'dg-ln') + '</g>';
        s += H.p('M124 82 L122 190', 'dg-ln') + (lift ? H.p('M' + (196 + (tilt > 0 ? 6 : -2)) + ' ' + (82 + tilt * 1.4) + ' L212 136 L196 172', 'dg-ln') : H.p('M196 82 L198 190', 'dg-ln'));
        s += T(124, 206, 'right', 'dg-tm', 'middle') + T(196, 206, 'left', 'dg-tm', 'middle');
        if (i === 2) s += H.tag(250, 150, 'drops on the lifted side', 'b', 'middle');
      } else {
        s += H.ln(20, 170, 300, 170, 'dg-thin') + H.c(40, 150, 12, 'dg-skin') + H.r(52, 142, 100, 20, 'dg-skin', 8) + H.p('M150 152 L196 92 L240 150', 'dg-ln') + H.p('M150 152 L230 128 L300 140', 'dg-ln');
        s += H.arrow(240, 166, 240, 138, 'dg-arr') + T(236, 116, 'thigh lifts = fixed flexion', 'dg-tr', 'middle') + T(150, 78, 'good hip bent fully', 'dg-tm', 'end') + H.p('M96 162 q6 -10 14 0', 'dg-ar') + T(74, 186, 'hand under the back', 'dg-tm');
      }
      return S(320, 214, s, 'Hip tests');
    }});

  /* ---------- breast ---------- */
  d('breast', {t: 'Breast: map it like a clock', caps: [
    'Four quadrants. **Half of breast cancers are in the upper outer quadrant.**', 'The **axillary tail** runs up into the armpit: easy to miss.',
    'Feel behind the **nipple last**; ask her to express any discharge herself.', 'Describe a lump by the **clock and the distance from the nipple**: "at 2 o\'clock, 4 cm from the nipple".',
    '**Axilla:** take the weight of her arm and feel the 5 groups: front, back, inner, outer, apex.'],
    draw: function (i) {
      var cx = 140, cy = 120, s = '';
      s += '<g class="' + on(i === 1 || i === 4) + '">' + H.p('M198 72 Q236 40 262 22 L278 40 Q250 70 214 96 Z', 'dg-hl') + T(236, 14, 'axillary tail', 'dg-tm', 'middle') + '</g>';
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="82" class="dg-skin"/>' + H.ln(cx - 82, cy, cx + 82, cy, 'dg-dash') + H.ln(cx, cy - 82, cx, cy + 82, 'dg-dash');
      if (i === 0) s += '<path d="M' + cx + ' ' + cy + ' L' + cx + ' ' + (cy - 82) + ' A82 82 0 0 1 ' + (cx + 82) + ' ' + cy + ' Z" class="dg-wl"/>' + T(cx + 40, cy - 34, 'upper outer', 'dg-tb', 'middle');
      [12, 3, 6, 9].forEach(function (h) { var a = (h * 30 - 90) * Math.PI / 180; s += T((cx + 94 * Math.cos(a)).toFixed(0), (cy + 94 * Math.sin(a) + 4).toFixed(0), String(h), 'dg-tm', 'middle'); });
      s += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (i === 2 ? 10 : 7) + '" class="' + (i === 2 ? 'dg-pt dg-on' : 'dg-pt') + '"/>';
      if (i === 3) { var a2 = (60 - 90) * Math.PI / 180, lx = cx + 50 * Math.cos(a2), ly = cy + 50 * Math.sin(a2); s += H.ln(cx, cy, lx, ly, 'dg-ar') + '<circle cx="' + lx.toFixed(1) + '" cy="' + ly.toFixed(1) + '" r="9" class="dg-bl"/>' + T(lx + 12, ly - 8, '2 o\'clock · 4 cm', 'dg-tr'); }
      if (i === 4) [[230, 92], [246, 78], [258, 104], [224, 112], [262, 56]].forEach(function (p) { s += H.c(p[0], p[1], 5, 'dg-pt dg-on'); });
      s += T(cx, 222, 'left breast, facing her', 'dg-tm', 'middle');
      return S(300, 230, s, 'Breast quadrants');
    }});

  /* ---------- scrotal lump decision tree ---------- */
  d('scrotum', {t: 'Scrotal lump: three questions', caps: [
    '**Can\'t get above it** → it has come down from the abdomen: an **inguinal hernia**.', '**Above it, separate from the testis, lights up** → **epididymal cyst**.',
    '**Separate, doesn\'t light up** → varicocele (bag of worms) or epididymitis (tender, hot).', '**Surrounds the testis and lights up** → **hydrocele**.',
    '**Part of the testis, hard, doesn\'t light up** → **testicular cancer until proven otherwise**: urgent ultrasound and tumour markers.',
    '**Sudden severe pain, high-riding testis, no cremasteric reflex** → **torsion**: theatre now.'],
    draw: function (i) {
      var B = function (x, y, w, txt, hot, leaf) { var lines = txt.split('|'); return '<g class="' + (hot ? 'dg-on' : 'dg-off') + '"><rect x="' + (x - w / 2) + '" y="' + y + '" width="' + w + '" height="' + (14 + lines.length * 12) + '" rx="8" class="' + (leaf ? 'dg-wl' : 'dg-hl') + '"/>' + lines.map(function (l, k) { return T(x, y + 15 + k * 12, l, leaf ? 'dg-tb' : '', 'middle', 10.5); }).join('') + '</g>'; };
      var E = function (x1, y1, x2, y2, lab, hot) { return '<g class="' + (hot ? 'dg-on' : 'dg-off') + '">' + H.ln(x1, y1, x2, y2, 'dg-ar') + T((x1 + x2) / 2 + (x2 < x1 ? -6 : 6), (y1 + y2) / 2, lab, 'dg-ta', x2 < x1 ? 'end' : 'start', 10) + '</g>'; };
      var p = [[1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, 1, 1, 0, 0, 0], [1, 1, 0, 1, 0, 0], [1, 1, 0, 1, 0, 0], [0, 0, 0, 0, 0, 1]][i];
      var s = '';
      if (i === 5) return S(360, 250, B(180, 90, 300, '⚠️ Sudden pain + high, horizontal testis|+ no cremasteric reflex|= TORSION: surgery within 6 hours', true, true), 'Torsion');
      s += B(180, 6, 170, 'Can I get above it?', true);
      s += E(140, 32, 70, 70, 'no', i === 0) + B(64, 72, 110, 'Inguinal hernia', i === 0, 1);
      s += E(220, 32, 260, 70, 'yes', i > 0) + B(260, 72, 150, 'Separate from the testis?', i > 0);
      s += E(222, 98, 150, 136, 'yes', i === 1 || i === 2) + B(150, 138, 96, 'Lights up?', i === 1 || i === 2);
      s += E(296, 98, 300, 136, 'no', i === 3 || i === 4) + B(300, 138, 96, 'Lights up?', i === 3 || i === 4);
      s += E(126, 164, 52, 196, 'yes', i === 1) + B(50, 198, 88, 'Epididymal|cyst', i === 1, 1);
      s += E(170, 164, 142, 196, 'no', i === 2) + B(142, 198, 92, 'Varicocele or|epididymitis', i === 2, 1);
      s += E(280, 164, 234, 196, 'yes', i === 3) + B(234, 198, 82, 'Hydrocele', i === 3, 1);
      s += E(318, 164, 316, 196, 'no', i === 4) + B(316, 198, 80, 'Testicular|tumour', i === 4, 1);
      return S(360, 250, s, 'Scrotal lump decision tree');
    }});

  /* ---------- DRE: the prostate story ---------- */
  d('dre', {t: 'DRE: the prostate story', caps: [
    '**Left side, knees up to the chest,** bottom at the edge of the bed. Chaperone and consent first.', '**Normal prostate:** walnut-sized, smooth, rubbery, with a **central groove** you can feel. At 12 o\'clock in a man.',
    '**BPH:** bigger but still **smooth and rubbery**; the groove is still there.', '**Cancer:** **hard, craggy, irregular**; the groove is lost.', '**Look at the glove:** blood, mucus, black tarry stool.'],
    draw: function (i) {
      var s = '';
      if (i === 0) {
        s += H.ln(20, 160, 300, 160, 'dg-thin') + H.c(66, 104, 18, 'dg-skin') + H.p('M84 112 Q150 92 196 116 Q222 130 212 150 L160 150 Q140 140 112 138 Z', 'dg-skin') + H.p('M196 120 L236 84 L262 120 M200 140 L244 110 L272 150', 'dg-ln') + T(160, 186, 'left lateral, knees up', 'dg-ta', 'middle');
        return S(320, 196, s, 'Left lateral position');
      }
      var big = i === 2 ? 1.35 : 1, cx = 160, cy = 96;
      if (i === 4) return S(320, 196, H.p('M100 150 L100 80 Q100 56 124 56 Q148 56 148 80 L148 150 Z', 'dg-skin') + '<ellipse cx="124" cy="66" rx="16" ry="10" class="dg-bl"/>' + T(200, 70, 'blood?', 'dg-tr') + T(200, 92, 'mucus?', 'dg-tb') + T(200, 114, 'melaena: black and tarry?', 'dg-tb'), 'Glove');
      if (i === 3) s += H.p('M' + (cx - 46) + ' ' + cy + ' l8 -22 l14 -6 l10 -16 l14 10 l12 -6 l14 14 l16 -2 l8 20 l-6 14 l8 18 l-12 14 l-16 -2 l-14 12 l-18 -4 l-16 8 l-12 -16 l-12 -4 l-4 -18 Z', 'dg-bl');
      else s += '<ellipse cx="' + (cx - 22 * big) + '" cy="' + cy + '" rx="' + (26 * big) + '" ry="' + (32 * big) + '" class="dg-hl"/><ellipse cx="' + (cx + 22 * big) + '" cy="' + cy + '" rx="' + (26 * big) + '" ry="' + (32 * big) + '" class="dg-hl"/>' + H.ln(cx, cy - 30 * big, cx, cy + 30 * big, 'dg-ln');
      s += T(cx, 176, ['', 'Normal: walnut, smooth, groove', 'BPH: big, smooth, groove kept', 'Cancer: hard, craggy, groove lost'][i], i === 3 ? 'dg-tr' : 'dg-ta', 'middle', 12);
      return S(320, 196, s, 'Prostate');
    }});

  /* ---------- skin ---------- */
  var LES = [['Macule', 'flat, under 1 cm'], ['Patch', 'flat, over 1 cm'], ['Papule', 'raised, under 1 cm'], ['Plaque', 'raised and flat-topped, over 1 cm'], ['Nodule', 'deep and round, over 1 cm'], ['Vesicle', 'fluid, under 0.5 cm'], ['Bulla', 'fluid, over 0.5 cm'], ['Pustule', 'pus-filled'], ['Wheal', 'swollen, itchy, gone within 24 hours']];
  d('lesion', {t: 'Lesion words: flat, raised, deep or fluid', caps: LES.map(function (l) { return '**' + l[0] + ':** ' + l[1] + '.'; }),
    draw: function (i) {
      var y = 100, s = '';
      s += H.r(10, y, 300, 70, 'dg-mut', 0) + H.ln(10, y, 310, y, 'dg-ln');
      s += T(20, y + 60, 'skin in cross-section', 'dg-tm');
      s += H.ln(110, 34, 210, 34, 'dg-ln') + H.ln(110, 28, 110, 40, 'dg-ln') + H.ln(210, 28, 210, 40, 'dg-ln') + T(160, 26, '1 cm', 'dg-tm', 'middle');
      var c = 160, sh = [
        '<rect x="' + (c - 36) + '" y="' + (y - 2) + '" width="72" height="5" class="dg-wl"/>',
        '<rect x="' + (c - 110) + '" y="' + (y - 2) + '" width="220" height="5" class="dg-wl"/>',
        H.p('M' + (c - 30) + ' ' + y + ' Q' + c + ' ' + (y - 40) + ' ' + (c + 30) + ' ' + y + ' Z', 'dg-wl'),
        H.p('M' + (c - 110) + ' ' + y + ' L' + (c - 100) + ' ' + (y - 20) + ' L' + (c + 100) + ' ' + (y - 20) + ' L' + (c + 110) + ' ' + y + ' Z', 'dg-wl'),
        '<ellipse cx="' + c + '" cy="' + (y + 4) + '" rx="56" ry="44" class="dg-wl"/>',
        H.p('M' + (c - 18) + ' ' + y + ' Q' + c + ' ' + (y - 30) + ' ' + (c + 18) + ' ' + y + ' Z', 'dg-hl'),
        H.p('M' + (c - 70) + ' ' + y + ' Q' + c + ' ' + (y - 70) + ' ' + (c + 70) + ' ' + y + ' Z', 'dg-hl'),
        H.p('M' + (c - 20) + ' ' + y + ' Q' + c + ' ' + (y - 34) + ' ' + (c + 20) + ' ' + y + ' Z', '') .replace('class=""', 'fill="#e8c547" stroke="#a48410"'),
        H.p('M' + (c - 80) + ' ' + y + ' Q' + (c - 40) + ' ' + (y - 26) + ' ' + c + ' ' + (y - 24) + ' Q' + (c + 40) + ' ' + (y - 26) + ' ' + (c + 80) + ' ' + y + ' Z', 'dg-bl')][i];
      s += sh + H.tag(160, 74 - (i === 6 ? 14 : 0), LES[i][0], 'w', 'middle');
      return S(320, 180, s, 'Lesion morphology');
    }});
  d('rashpat', {t: 'Where it is points to what it is', caps: [
    '**Extensors:** elbows, knees, scalp → **psoriasis**.', '**Flexures:** elbow and knee creases, neck, wrists → **eczema**.', '**One dermatome on one side** → **shingles**.',
    '**Sun-exposed:** face, the V of the neck, backs of the hands → photosensitivity, lupus, actinic damage.', '**A ring with a scaly edge** → **tinea**.', '**Non-blanching spots in an unwell person** → **meningococcal sepsis**: act now.'],
    draw: function (i) {
      var s = H.body(150, 8, 210), k = 1.05, X = function (v) { return 150 + v * k; }, Y = function (v) { return 8 + v * k; }, dot = function (x, y, r, c) { return '<circle cx="' + x.toFixed(1) + '" cy="' + y.toFixed(1) + '" r="' + r + '" class="' + (c || 'dg-bl') + '"/>'; };
      if (i === 0) s += dot(X(-38), Y(80), 8) + dot(X(38), Y(80), 8) + dot(X(-14), Y(150), 9) + dot(X(14), Y(150), 9) + dot(X(0), Y(6), 8);
      if (i === 1) s += dot(X(-36), Y(76), 7, 'dg-wl') + dot(X(36), Y(76), 7, 'dg-wl') + dot(X(0), Y(30), 7, 'dg-wl') + dot(X(-40), Y(102), 6, 'dg-wl') + dot(X(40), Y(102), 6, 'dg-wl');
      if (i === 2) s += H.p('M' + X(-30) + ' ' + Y(60) + ' Q' + X(-14) + ' ' + Y(56) + ' ' + X(-1) + ' ' + Y(66) + ' L' + X(-1) + ' ' + Y(74) + ' Q' + X(-14) + ' ' + Y(64) + ' ' + X(-30) + ' ' + Y(70) + ' Z', 'dg-bl');
      if (i === 3) s += dot(X(0), Y(16), 12, 'dg-wl') + dot(X(0), Y(40), 7, 'dg-wl') + dot(X(-40), Y(108), 6, 'dg-wl') + dot(X(40), Y(108), 6, 'dg-wl');
      if (i === 4) s += '<circle cx="' + X(10) + '" cy="' + Y(80) + '" r="12" fill="none" style="stroke:var(--bad);stroke-width:3;stroke-dasharray:2 2"/>';
      if (i === 5) [[-14, 160], [-10, 172], [-18, 180], [12, 166], [16, 178], [10, 186], [-6, 140], [8, 146]].forEach(function (p) { s += dot(X(p[0]), Y(p[1]), 2.6, 'dg-red'); });
      if (i === 5) s += T(250, 190, 'glass test: still there', 'dg-tr', 'middle');
      return S(300, 232, s, 'Rash distribution');
    }});
  d('abcde', {t: 'ABCDE: benign on the left, worrying on the right', caps: [
    '**A · Asymmetry:** one half doesn\'t match the other.', '**B · Border:** ragged, notched or blurred.', '**C · Colour:** several shades: brown, black, red, blue, white.',
    '**D · Diameter:** over 6 mm, the size of a pencil end.', '**E · Evolving:** changing in size, shape or colour. **The most important letter.**'],
    draw: function (i) {
      var s = '', B1 = '#7a4a2a', B2 = '#3b2416', R1 = '#a8443a';
      s += T(80, 20, 'reassuring', 'dg-tm', 'middle') + T(240, 20, 'worrying', 'dg-tm', 'middle') + H.ln(160, 26, 160, 150, 'dg-dash');
      var good = '<circle cx="80" cy="86" r="' + (i === 3 ? 14 : 22) + '" fill="' + B1 + '"/>';
      var bad = [
        '<path d="M222 64 Q260 58 262 84 Q266 112 236 108 Q212 104 214 88 Q206 70 222 64 Z" fill="' + B1 + '"/>',
        '<path d="M218 66 l10 -4 l6 8 l10 -6 l6 10 l10 2 l-2 12 l8 8 l-8 8 l2 12 l-12 0 l-6 10 l-10 -6 l-10 4 l-4 -12 l-10 -4 l6 -10 l-6 -10 l10 -4 Z" fill="' + B1 + '"/>',
        '<circle cx="240" cy="86" r="24" fill="' + B1 + '"/><path d="M226 70 Q246 64 252 84 Q236 96 226 70 Z" fill="' + B2 + '"/><circle cx="252" cy="98" r="7" fill="' + R1 + '"/><circle cx="230" cy="96" r="5" fill="#2a3a66"/>',
        '<circle cx="240" cy="86" r="30" fill="' + B1 + '"/>',
        '<circle cx="216" cy="88" r="10" fill="' + B1 + '"/>' + H.arrow(232, 88, 250, 88) + '<path d="M264 66 Q292 62 292 88 Q296 112 270 110 Q252 108 256 90 Q250 72 264 66 Z" fill="' + B2 + '"/>'][i];
      s += good + bad;
      if (i === 3) s += H.ln(210, 128, 270, 128, 'dg-ln') + T(240, 142, 'over 6 mm', 'dg-tr', 'middle') + H.ln(66, 128, 94, 128, 'dg-ln') + T(80, 142, 'small', 'dg-tm', 'middle');
      s += H.tag(160, 168, ['Asymmetry', 'Border', 'Colour', 'Diameter', 'Evolving'][i], 'w', 'middle');
      return S(320, 180, s, 'ABCDE of melanoma');
    }});

  /* ---------- ENT ---------- */
  d('nose', {t: 'Looking into the right nostril', caps: [
    'The **septum** is the wall on your right, towards the middle; the **turbinates** bulge in from the outside wall.', '**Little\'s area** at the front of the septum: about 90% of nosebleeds come from here.',
    '**Inferior turbinate:** pink and sensitive. **Pale, swollen and boggy = allergic rhinitis.**', '**Polyp:** grey, shiny, like a peeled grape, and you can touch it without pain. **One-sided = refer.**'],
    draw: function (i) {
      var id = H.uid(), s = '<clipPath id="' + id + '"><circle cx="150" cy="104" r="86"/></clipPath><circle cx="150" cy="104" r="88" fill="#1a1012"/><g clip-path="url(#' + id + ')">';
      s += '<path d="M200 10 Q220 104 200 200 L250 200 L250 10 Z" fill="#e8a49a"/>';
      s += '<ellipse cx="' + (i === 2 ? 98 : 88) + '" cy="136" rx="' + (i === 2 ? 56 : 44) + '" ry="' + (i === 2 ? 36 : 28) + '" fill="' + (i === 2 ? '#efd9d4' : '#d97c70') + '"/><ellipse cx="86" cy="72" rx="32" ry="17" fill="#cf766b"/>';
      if (i === 1) s += '<path d="M206 70 q8 6 2 14 q-8 6 0 14" stroke="#c22" stroke-width="2.4" fill="none"/><circle cx="210" cy="86" r="11" fill="none" stroke="var(--warn)" stroke-width="2.4"/>';
      if (i === 3) s += '<ellipse cx="150" cy="102" rx="25" ry="31" fill="#b9bfc2"/><ellipse cx="142" cy="92" rx="6" ry="9" fill="#fff" opacity=".45"/>';
      s += '</g><circle cx="150" cy="104" r="88" fill="none" style="stroke:var(--muted);stroke-width:6"/>';
      s += T(222, 30, 'septum', 'dg-tm', 'middle') + T(64, 172, 'turbinate', 'dg-tm', 'middle');
      s += H.tag(150, 214, ['septum on your right', 'Little\'s area', i === 2 ? 'pale, boggy turbinate' : 'turbinate', 'polyp: grey, insensate'][i], i === 3 ? 'w' : '', 'middle');
      return S(300, 226, s, 'Anterior rhinoscopy view');
    }});
  d('mouth', {t: 'Mouth: the order so nothing is missed', caps: [
    '**Lips** and the corners of the mouth.', '**Cheeks** both sides: the parotid duct opens opposite the upper second molar.', '**Gums and teeth.**', '**Hard and soft palate.**',
    '**Top of the tongue.**', '**Sides and underneath of the tongue:** the commonest place for oral cancer.', '**Floor of the mouth:** lift the tongue to see it.', '**Tonsils, uvula and the back wall:** say ahh.'],
    draw: function (i) {
      var s = '', hot = function (k, el) { return '<g class="' + on(i === k) + '">' + el + '</g>'; };
      s += '<ellipse cx="150" cy="112" rx="128" ry="98" class="dg-skin"/>';
      s += '<ellipse cx="150" cy="112" rx="112" ry="84" fill="#5a1f22"/>';
      s += '<ellipse cx="150" cy="74" rx="78" ry="34" fill="#c46b6f"/>' + '<path d="M144 92 Q150 112 156 92 Z" fill="#d98b8f"/>';
      s += '<ellipse cx="78" cy="112" rx="14" ry="22" fill="#d06f74"/><ellipse cx="222" cy="112" rx="14" ry="22" fill="#d06f74"/>';
      s += '<ellipse cx="150" cy="' + (i === 6 ? 150 : 160) + '" rx="70" ry="' + (i === 6 ? 32 : 42) + '" fill="#d8777b"/>';
      if (i === 6) s += '<path d="M120 182 Q150 196 180 182" stroke="#fff" stroke-opacity=".5" fill="none"/>' + '<ellipse cx="150" cy="186" rx="40" ry="10" fill="#b55a60"/>';
      for (var k = 0; k < 12; k++) { var a = Math.PI * (0.12 + 0.76 * k / 11); s += '<rect x="' + (150 - 100 * Math.cos(a) - 6).toFixed(1) + '" y="' + (112 - 70 * Math.sin(a) - 8).toFixed(1) + '" width="12" height="14" rx="3" fill="#f3efe4"/>'; }
      var hl = [
        '<ellipse cx="150" cy="112" rx="126" ry="96" fill="none" style="stroke:var(--warn);stroke-width:5"/>',
        '<ellipse cx="44" cy="112" rx="14" ry="40" class="dg-wl"/><ellipse cx="256" cy="112" rx="14" ry="40" class="dg-wl"/>',
        '<path d="M50 104 Q150 -6 250 104" fill="none" style="stroke:var(--warn);stroke-width:6"/>',
        '<ellipse cx="150" cy="70" rx="78" ry="30" class="dg-wl"/>',
        '<ellipse cx="150" cy="156" rx="50" ry="22" class="dg-wl"/>',
        '<ellipse cx="88" cy="164" rx="16" ry="26" class="dg-bl"/><ellipse cx="212" cy="164" rx="16" ry="26" class="dg-bl"/>',
        '<ellipse cx="150" cy="186" rx="42" ry="12" class="dg-wl"/>',
        '<ellipse cx="78" cy="112" rx="18" ry="26" class="dg-wl"/><ellipse cx="222" cy="112" rx="18" ry="26" class="dg-wl"/><ellipse cx="150" cy="100" rx="10" ry="14" class="dg-wl"/>'][i];
      s += hl + H.tag(150, 222, String(i + 1) + ' of 8', 'w', 'middle');
      return S(300, 232, s, 'Oral cavity');
    }});
  d('drum', {t: 'The eardrum: normal first, then the classics', caps: [
    '**Normal right drum:** pearly grey, the **handle of the malleus**, and the **cone of light at 5 o\'clock**. In the left ear it is at 7 o\'clock: it points to the nose.',
    '**Acute otitis media:** red, **bulging**, cone of light lost. Pain and fever.', '**Glue ear:** dull, **retracted**, with a **fluid level and bubbles**. Hearing reduced, no pain.',
    '**Cholesteatoma:** a crust or white mass in the **attic** at the top, with foul discharge. Refer.'],
    draw: function (i) {
      var k = ['normal', 'aom', 'ome', 'chol'][i], m = (window.MEV && MEV.drum) ? MEV.drum(k) : '';
      if (i === 0 && m) m = m.replace('</svg>', '<text x="98" y="44" font-size="8" fill="#fff">malleus</text><text x="114" y="140" font-size="8" fill="#fff">cone of light</text></svg>');
      if (i === 3 && m) m = m.replace('</svg>', '<ellipse cx="80" cy="30" rx="14" ry="8" fill="#f4f1e6"/><text x="98" y="26" font-size="8" fill="#fff">attic</text></svg>');
      return '<div style="max-width:240px;margin:0 auto">' + m + '</div>';
    }});
  d('rinne', {t: 'Rinne and Weber in one picture', caps: [
    '**Rinne:** fork on the **mastoid**, then beside the ear. "Which is louder?"', '**Rinne positive: air louder than bone.** Normal, or sensorineural loss.',
    '**Rinne negative: bone louder.** A **conductive** loss in that ear: wax, glue ear, perforation, otosclerosis.', '**Weber:** fork on the middle of the forehead. Normal: heard in the middle.',
    '**Conductive loss:** Weber goes to the **BAD** ear. Try it: block one ear with a finger and hum.', '**Sensorineural loss:** Weber goes to the **GOOD** ear. One-sided sensorineural loss needs an MRI.'],
    draw: function (i) {
      var s = '';
      var fork = function (x, y, rot) { return '<g transform="rotate(' + rot + ' ' + x + ' ' + y + ')"><path d="M' + x + ' ' + y + ' l0 -20 M' + (x - 5) + ' ' + (y - 20) + ' l0 -30 M' + (x + 5) + ' ' + (y - 20) + ' l0 -30 M' + (x - 5) + ' ' + (y - 20) + ' l10 0" class="dg-ln" style="stroke-width:2.4"/></g>'; };
      if (i < 3) {
        s += '<ellipse cx="150" cy="104" rx="70" ry="80" class="dg-skin"/>' + '<ellipse cx="196" cy="104" rx="10" ry="18" class="dg-skin"/>' + T(150, 200, 'side view, right ear', 'dg-tm', 'middle');
        s += fork(i === 0 ? 214 : 234, i === 0 ? 132 : 104, i === 0 ? -20 : 0);
        if (i === 0) s += H.tag(250, 150, 'on the mastoid', '', 'middle');
        if (i === 1) s += H.tag(250, 30, 'air > bone: positive', 'g', 'middle');
        if (i === 2) s += H.tag(250, 30, 'bone > air: negative', 'b', 'middle');
      } else {
        s += '<ellipse cx="150" cy="110" rx="66" ry="78" class="dg-skin"/><ellipse cx="82" cy="112" rx="9" ry="16" class="dg-skin"/><ellipse cx="218" cy="112" rx="9" ry="16" class="dg-skin"/>';
        s += fork(150, 46, 0) + T(150, 204, 'front view', 'dg-tm', 'middle');
        if (i === 3) s += H.arrow(140, 70, 96, 100) + H.arrow(160, 70, 204, 100);
        if (i === 4) s += H.arrow(150, 70, 92, 104, 'dg-arr') + H.r(70, 104, 12, 16, 'dg-bl', 3) + T(240, 92, 'good', 'dg-tm') + T(40, 92, 'bad, blocked', 'dg-tr');
        if (i === 5) s += H.arrow(150, 70, 208, 104, 'dg-arr') + T(36, 92, 'nerve deaf', 'dg-tr') + T(234, 92, 'good', 'dg-tm');
      }
      return S(320, 212, s, 'Rinne and Weber');
    }});
  d('nodes', {t: 'Neck nodes: one loop, from behind', ms: 1600, caps: [
    '**1 · Submental**, under the chin.', '**2 · Submandibular**, under the jaw.', '**3 · Preauricular**, in front of the ear.', '**4 · Postauricular**, behind the ear.',
    '**5 · Occipital**, the base of the skull.', '**6 · Posterior triangle**, down behind the long neck muscle.', '**7 · Supraclavicular**, above the collarbone. **Left side = Virchow\'s node.**',
    '**8 · Anterior chain**, back up the front of the long neck muscle to the jaw.'],
    draw: function (i) {
      var s = H.p('M92 26 Q150 2 208 30 Q232 60 220 96 Q212 120 206 150 Q240 176 300 196 L300 220 L30 220 L30 200 Q80 184 104 170 L108 134 Q90 126 88 116 L74 110 Q66 98 80 94 L70 82 Q62 74 74 66 Q78 42 92 26 Z', 'dg-skin');
      s += H.p('M174 92 L118 184', 'dg-dash') + H.p('M96 188 Q160 178 236 188', 'dg-thin') + '<ellipse cx="166" cy="78" rx="9" ry="15" class="dg-skin"/>';
      var P = [[100, 126], [128, 120], [152, 76], [182, 80], [212, 100], [198, 150], [160, 180], [132, 150]], path = '';
      P.forEach(function (p, k) { if (k && k <= i) path += H.arrow(P[k - 1][0], P[k - 1][1], p[0] + (P[k - 1][0] < p[0] ? -6 : 6), p[1], 'dg-ar'); });
      s += path;
      P.forEach(function (p, k) { s += '<circle cx="' + p[0] + '" cy="' + p[1] + '" r="8" class="dg-pt' + (k <= i ? ' dg-on' : '') + '"/>' + T(p[0], p[1] + 3.5, String(k + 1), k <= i ? '' : 'dg-tm', 'middle', 9, k <= i ? ' style="fill:var(--on-accent);font-weight:700"' : ''); });
      return S(320, 222, s, 'Head and neck lymph nodes');
    }});

  /* ---------- eyes ---------- */
  function eye(extra, pupil, under) {
    var id = H.uid();
    return '<clipPath id="' + id + '"><path d="M50 96 Q160 6 270 96 Q160 186 50 96 Z"/></clipPath><path d="M50 96 Q160 6 270 96 Q160 186 50 96 Z" fill="#f4f1ec"/><g clip-path="url(#' + id + ')">' + (under || '') + '<circle cx="160" cy="96" r="38" fill="#5c7d56"/><circle cx="160" cy="96" r="' + (pupil || 13) + '" fill="#0d1418"/>' + (extra || '') + '</g><path d="M50 96 Q160 6 270 96 Q160 186 50 96 Z" class="dg-ln"/>';
  }
  d('redeye', {t: 'Red eye: read the pattern', caps: [
    '**Conjunctivitis:** redness everywhere, worst away from the cornea, sticky, vision normal.', '**Ciliary flush:** a red ring hugging the cornea = something deeper: keratitis, uveitis, acute glaucoma. **Same day.**',
    '**Subconjunctival haemorrhage:** a flat bright-red patch, painless, vision normal.', '**Acute angle closure:** ring of redness, **hazy cornea**, a **fixed mid-dilated pupil**, pain and vomiting.',
    '**Anterior uveitis:** ring of redness, light sensitivity, **small irregular pupil**.', '**Herpes keratitis:** a **branching** ulcer that glows green with fluorescein. No steroid drops.'],
    draw: function (i) {
      var R = '#d64545', s = '';
      if (i === 0) s = eye('', 13, '<rect x="40" y="0" width="240" height="200" fill="' + R + '" opacity=".38"/>') + '<circle cx="76" cy="104" r="4" fill="#e3c34a"/><circle cx="248" cy="102" r="3" fill="#e3c34a"/>';
      if (i === 1) s = eye('', 13, '<circle cx="160" cy="96" r="54" fill="' + R + '" opacity=".55"/>');
      if (i === 2) s = eye('', 13, '<path d="M60 70 Q96 40 128 66 Q116 120 70 120 Z" fill="#c62828" opacity=".9"/>');
      if (i === 3) s = eye('<circle cx="160" cy="96" r="38" fill="#fff" opacity=".45"/>', 22, '<circle cx="160" cy="96" r="54" fill="' + R + '" opacity=".55"/>');
      if (i === 4) s = eye('', 0, '<circle cx="160" cy="96" r="54" fill="' + R + '" opacity=".5"/>').replace('<circle cx="160" cy="96" r="0" fill="#0d1418"/>', '<path d="M152 90 L166 88 L170 100 L158 106 L150 100 Z" fill="#0d1418"/>');
      if (i === 5) s = eye('<path d="M140 84 L156 92 L150 104 M156 92 L172 86 L180 96 M172 86 L170 74" stroke="#5cff6a" stroke-width="3" fill="none"/>', 13, '<circle cx="160" cy="96" r="50" fill="' + R + '" opacity=".25"/>');
      return S(320, 190, s, 'Red eye patterns');
    }});
  d('snellen', {t: 'Visual acuity: the fraction', caps: [
    '**6 / X:** the top number is the distance in metres; the bottom is the line they can read. A normal eye reads that line at X metres.', '**6/6** is normal. 6/5 is better than normal.',
    '**6/60:** only the top letter.', '**Pinhole improves it = a glasses problem.** No improvement = disease in the eye or nerve.', 'Can\'t read the top letter? Try **counting fingers, hand movements, then light perception**.'],
    draw: function (i) {
      var L = [['E', 60, 34], ['F P', 36, 24], ['T O Z', 24, 18], ['L P E D', 18, 14], ['P E C F D', 12, 11], ['E D F C Z P', 9, 9], ['F E L O P Z D', 6, 7.5]], s = H.r(70, 6, 180, 200, 'dg-skin', 6), y = 40;
      L.forEach(function (l, k) { var hot = (i === 1 && l[1] === 6) || (i === 2 && l[1] === 60); s += T(160, y, l[0], hot ? 'dg-ta' : 'dg-tb', 'middle', l[2] * 0.95) + T(262, y - 2, '6/' + l[1], hot ? 'dg-ta' : 'dg-tm'); y += l[2] * 0.9 + 8; });
      if (i === 3) s += '<circle cx="40" cy="110" r="22" class="dg-ink"/><circle cx="40" cy="110" r="3" class="dg-srf"/>' + T(40, 146, 'pinhole', 'dg-tm', 'middle');
      if (i === 4) s += T(40, 70, 'CF', 'dg-tb', 'middle') + T(40, 100, 'HM', 'dg-tb', 'middle') + T(40, 130, 'PL', 'dg-tb', 'middle');
      return S(320, 222, s, 'Snellen chart');
    }});
  d('fundus', {t: 'Fundoscopy: the six pictures to know', caps: [
    '**Normal:** a pink disc with sharp margins, the cup under half of the disc, 4 arcades of vessels, the macula last.', '**Background diabetic:** dots, blots and hard yellow exudates.',
    '**Proliferative diabetic:** **new fragile vessels**, often on the disc. Urgent laser.', '**Central retinal artery occlusion:** pale white retina with a **cherry-red spot**. Ask about GCA.',
    '**Central retinal vein occlusion:** **haemorrhages everywhere**, the stormy sunset.', '**Macular degeneration:** drusen and changes at the macula, central vision lost.'],
    draw: function (i) {
      var k = ['normal', 'dr', 'pdr', 'crao', 'crvo', 'mac'][i], m = (window.MEV && MEV.fundus) ? MEV.fundus(k) : '';
      if (i === 0 && m) m = m.replace('</svg>', '<text x="40" y="132" font-size="9" fill="#fff">disc</text><text x="120" y="130" font-size="9" fill="#fff">macula</text></svg>');
      return '<div style="max-width:250px;margin:0 auto">' + m + '</div>';
    }});
})();
