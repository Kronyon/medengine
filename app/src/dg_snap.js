/* medengine 🎞️ Snapshot: the same 7-frame film for every condition, so only the content changes.
   1 What goes wrong (the organ, the broken part, the chain) · 2 Who · 3 Spot it (body map) · 4 Prove it ·
   5 Treat (a ladder) · 6 Watch for · 7 Hook. DG.snapDef(id, s) registers one; DG.html(id) draws it. */
(function () {
  var H = DG.H, S = H.svg, esc = H.esc, T = function (x, y, s, c, a, sz) { return H.t(x, y, s, c, a, null, sz ? ' style="font-size:' + sz + 'px"' : ''); };
  var HOT = 'snap-hot', OK = 'snap-org';
  function wrap(t, n) { var out = [], line = ''; String(t).split(' ').forEach(function (w) { if ((line + ' ' + w).trim().length > n && line) { out.push(line.trim()); line = w; } else line += ' ' + w; }); if (line.trim()) out.push(line.trim()); return out; }
  function lines(x, y, t, n, cls, lh, a) { return wrap(t, n).map(function (l, k) { return T(x, y + k * (lh || 13), l, cls || '', a || '', null); }).join(''); }
  function c(r, key, hot) { return key === hot ? HOT : OK; }

  /* ---------- organ pictograms: each draws in a 160 x 210 box; the broken part glows ---------- */
  var ORG = {
    heart: {lab: {cor: 'coronary artery', aov: 'aortic valve', mv: 'mitral valve', lv: 'left ventricle', atria: 'atria and conduction', peri: 'pericardium', aorta: 'aorta', whole: 'the heart muscle'},
      draw: function (h) {
        var s = '<path class="' + c(0, 'aorta', h) + '" d="M86 74 L86 34 Q86 18 104 18 Q124 18 126 38 L126 62 L116 62 L116 40 Q114 30 104 30 Q98 30 98 40 L98 74 Z"/>';
        s += '<path class="' + c(0, 'peri', h) + '" style="fill:none;stroke-width:' + (h === 'peri' ? 6 : 1.4) + '" d="M80 64 C58 34 10 50 22 100 C32 136 66 160 80 190 C94 160 128 136 138 100 C150 50 102 34 80 64 Z"/>';
        s += '<path class="' + (h === 'whole' ? HOT : OK) + '" d="M80 72 C60 44 20 58 30 100 C38 130 68 152 80 178 C92 152 122 130 130 100 C140 58 100 44 80 72 Z"/>';
        s += '<ellipse class="' + c(0, 'atria', h) + '" cx="58" cy="86" rx="20" ry="15"/><ellipse class="' + c(0, 'atria', h) + '" cx="104" cy="84" rx="20" ry="15"/>';
        s += '<path class="' + c(0, 'lv', h) + '" d="M84 104 L124 100 C120 128 100 148 84 166 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'cor' ? 4 : 2) + ';stroke:' + (h === 'cor' ? 'var(--bad)' : 'var(--muted)') + '" d="M84 78 Q78 110 82 160 M84 92 Q104 102 118 120"/>';
        s += '<circle class="' + c(0, 'aov', h) + '" cx="92" cy="74" r="7"/><circle class="' + c(0, 'mv', h) + '" cx="100" cy="100" r="7"/>';
        if (h === 'atria') s += '<path d="M54 70 l6 10 l-5 2 l7 12" style="fill:none;stroke:var(--bad);stroke-width:2"/>';
        return s;
      }},
    lungs: {lab: {airway: 'airways', alv: 'air sacs', pleura: 'pleural space', apex: 'upper lobe', vessel: 'lung arteries', lung: 'one lung', both: 'both lungs', base: 'lower zones', air: 'air outside the lung'},
      draw: function (h) {
        var s = '<path class="' + c(0, 'airway', h) + '" d="M76 14 L84 14 L84 58 L104 76 L100 82 L80 64 L60 82 L56 76 L76 58 Z"/>';
        var L = 'M70 70 Q44 54 26 80 Q12 120 18 178 Q44 190 72 176 Z', R = 'M90 70 Q116 54 134 80 Q148 120 142 178 Q116 190 88 176 Z';
        if (h === 'air') return s + '<path d="M70 70 Q44 54 26 80 Q12 120 18 178 Q44 190 72 176 Z" style="fill:none;stroke:var(--muted);stroke-dasharray:4 3"/><path class="' + OK + '" d="M70 84 Q54 80 48 100 Q44 130 50 160 Q62 168 72 160 Z"/><path class="' + HOT + '" style="fill-opacity:.12" d="M70 70 Q44 54 26 80 Q12 120 18 178 Q44 190 72 176 L72 160 Q62 168 50 160 Q44 130 48 100 Q54 80 70 84 Z"/><path class="' + OK + '" d="' + R + '"/>';
        s += '<path class="' + (h === 'lung' || h === 'both' ? HOT : OK) + '" d="' + L + '"/><path class="' + (h === 'both' ? HOT : OK) + '" d="' + R + '"/>';
        if (h === 'apex') s += '<path class="' + HOT + '" d="M70 70 Q44 54 26 80 Q22 92 21 104 L70 104 Z"/>';
        if (h === 'base') s += '<path class="' + HOT + '" d="M19 146 Q18 160 18 178 Q44 190 72 176 L72 146 Z M141 146 Q142 160 142 178 Q116 190 88 176 L88 146 Z"/>';
        if (h === 'alv') { s += '<path class="' + HOT + '" d="M19 130 Q18 160 18 178 Q44 190 72 176 L72 130 Z"/>'; for (var i = 0; i < 9; i++) s += '<circle cx="' + (28 + (i % 3) * 16) + '" cy="' + (142 + Math.floor(i / 3) * 12) + '" r="4" style="fill:var(--bad);opacity:.5"/>'; }
        if (h === 'pleura') s += '<path class="' + HOT + '" d="M19 140 Q18 160 18 178 Q44 190 72 176 L72 140 Q46 148 19 140 Z"/><path d="M70 70 Q44 54 26 80 Q12 120 18 178 Q44 190 72 176" style="fill:none;stroke:var(--bad);stroke-width:3"/>';
        if (h === 'vessel') s += '<path d="M80 60 L80 90 M80 90 Q60 100 44 120 M80 90 Q100 100 116 120 M44 120 l-8 14 M44 120 l6 16 M116 120 l8 14 M116 120 l-6 16" style="fill:none;stroke:var(--bad);stroke-width:3"/><circle cx="44" cy="120" r="5" style="fill:var(--bad)"/>';
        else s += '<path d="M80 64 L80 90 M80 90 Q60 100 44 120 M80 90 Q100 100 116 120" style="fill:none;stroke:var(--muted);stroke-width:1.2;opacity:.6"/>';
        return s;
      }},
    limb: {lab: {aorta: 'abdominal aorta', artery: 'leg artery', vein: 'deep leg vein', skin: 'lower-leg skin', lymph: 'lymph drainage', fingers: 'finger arteries', super: 'surface veins'},
      draw: function (h) {
        var s = '<path class="' + OK + '" d="M40 60 L74 60 L72 200 L52 200 Z"/><path class="' + OK + '" d="M86 60 L120 60 L108 200 L88 200 Z"/>';
        if (h === 'lymph') s += '<path class="' + HOT + '" d="M38 120 Q30 160 46 202 L78 202 Q82 160 74 120 Z"/>';
        s += '<path class="' + (h === 'aorta' ? HOT : OK) + '" d="M76 10 L84 10 L84 ' + (h === 'aorta' ? '30 Q100 44 84 60' : '60') + ' L84 70 L66 90 L62 86 L76 70 L76 ' + (h === 'aorta' ? '60 Q60 44 76 30' : '60') + ' Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'artery' ? 4 : 2) + ';stroke:' + (h === 'artery' ? 'var(--bad)' : '#c55') + '" d="M64 88 L60 196"/><path style="fill:none;stroke-width:' + (h === 'vein' ? 5 : 2) + ';stroke:' + (h === 'vein' ? 'var(--bad)' : '#4a6fc6') + '" d="M66 196 L68 92"/>';
        if (h === 'vein') s += '<ellipse cx="67" cy="160" rx="7" ry="14" style="fill:var(--bad)"/>';
        if (h === 'super') s += '<path d="M100 80 Q94 110 104 130 Q96 150 102 196" style="fill:none;stroke:var(--bad);stroke-width:4"/><circle cx="104" cy="130" r="5" style="fill:var(--bad)"/>';
        if (h === 'skin') s += '<ellipse class="' + HOT + '" cx="60" cy="182" rx="10" ry="7"/>';
        s += '<g transform="translate(118 20)"><rect class="' + OK + '" x="0" y="30" width="32" height="26" rx="6"/>' + [0, 8, 16, 24].map(function (x) { return '<rect class="' + (h === 'fingers' ? HOT : OK) + '" x="' + (x + 1) + '" y="4" width="6" height="28" rx="3"/>'; }).join('') + '</g>';
        return s;
      }},
    gut: {lab: {oes: 'oesophagus', stom: 'stomach', duod: 'duodenum', small: 'small bowel', colon: 'colon', sig: 'sigmoid colon', rect: 'rectum', anus: 'anus', app: 'appendix', perit: 'the peritoneum', wall: 'the diaphragm gap'},
      draw: function (h) {
        var s = '';
        if (h === 'perit') s += '<rect class="' + HOT + '" x="8" y="40" width="144" height="160" rx="30" style="fill-opacity:.12"/>';
        s += '<path class="' + c(0, 'oes', h) + '" d="M76 6 L84 6 L86 52 L78 54 Z"/>';
        if (h === 'wall') s += '<path d="M40 50 L150 50" style="stroke:var(--bad);stroke-width:4;stroke-dasharray:30 10"/>';
        else s += '<path d="M30 52 Q80 40 150 52" style="fill:none;stroke:var(--muted);stroke-dasharray:3 3"/>';
        s += '<path class="' + c(0, 'stom', h) + '" d="M80 50 Q116 34 124 60 Q128 90 100 96 Q86 98 82 86 Q96 84 102 74 Q104 60 82 62 Z"/>';
        s += '<path class="' + c(0, 'duod', h) + '" d="M82 86 Q66 92 64 104 Q66 116 82 112 L84 106 Q72 108 72 102 Q74 96 86 94 Z"/>';
        s += '<path class="' + c(0, 'colon', h) + '" style="fill:none;stroke-width:12;stroke:' + (h === 'colon' ? 'var(--bad)' : 'var(--line)') + ';opacity:' + (h === 'colon' ? 0.6 : 1) + '" d="M34 176 L34 108 Q34 98 46 98 L120 98 Q132 98 132 110 L132 160"/>';
        s += '<path style="fill:none;stroke-width:12;stroke:' + (h === 'sig' ? 'var(--bad)' : 'var(--line)') + ';opacity:' + (h === 'sig' ? 0.6 : 1) + '" d="M132 160 Q132 180 110 176 Q92 172 90 184"/>';
        s += '<path class="' + c(0, 'small', h) + '" d="M48 116 Q66 108 84 118 Q104 110 118 120 Q118 134 100 136 Q84 130 66 140 Q50 138 48 128 Q62 130 70 126 Z M50 146 Q70 138 92 150 Q110 142 120 150 Q118 162 98 164 Q78 158 58 164 Q46 160 50 146 Z"/>';
        s += '<path class="' + c(0, 'app', h) + '" d="M30 176 Q26 190 34 194 Q38 186 38 178 Z"/>';
        s += '<rect class="' + c(0, 'rect', h) + '" x="84" y="182" width="14" height="16" rx="4"/><rect class="' + c(0, 'anus', h) + '" x="86" y="198" width="10" height="9" rx="3"/>';
        return s;
      }},
    hepat: {lab: {liver: 'liver', gb: 'gallbladder', duct: 'bile duct', panc: 'pancreas'},
      draw: function (h) {
        var s = '<path class="' + c(0, 'liver', h) + '" d="M10 50 Q70 20 140 44 Q130 80 92 92 Q54 100 22 90 Q6 76 10 50 Z"/>';
        s += '<path class="' + c(0, 'gb', h) + '" d="M58 92 Q52 116 64 120 Q76 116 72 92 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'duct' ? 5 : 2.5) + ';stroke:' + (h === 'duct' ? 'var(--bad)' : 'var(--muted)') + '" d="M80 90 L82 134 Q84 146 92 150 M66 106 L80 112"/>';
        s += '<path class="' + c(0, 'panc', h) + '" d="M84 146 Q78 162 96 164 Q120 154 150 140 Q152 130 140 130 Q116 140 96 142 Z"/>';
        s += '<path class="' + OK + '" style="fill:none;stroke-width:10" d="M84 138 Q66 150 76 172 Q90 180 98 168"/>';
        return s;
      }},
    uro: {lab: {kid: 'kidney', ureter: 'ureter', bladder: 'bladder', prostate: 'prostate', urethra: 'urethra'},
      draw: function (h) {
        var bean = function (x, hot) { return '<path class="' + (hot ? HOT : OK) + '" d="M' + x + ' 30 Q' + (x + 30) + ' 24 ' + (x + 30) + ' 60 Q' + (x + 30) + ' 96 ' + x + ' 90 Q' + (x + 12) + ' 74 ' + (x + 10) + ' 60 Q' + (x + 12) + ' 44 ' + x + ' 30 Z"/>'; };
        var s = bean(22, h === 'kid') + '<g transform="translate(160 0) scale(-1 1)">' + bean(22, false) + '</g>';
        s += '<path style="fill:none;stroke-width:' + (h === 'ureter' ? 5 : 2.5) + ';stroke:' + (h === 'ureter' ? 'var(--bad)' : 'var(--muted)') + '" d="M50 64 Q60 110 70 140 M110 64 Q100 110 90 140"/>';
        if (h === 'ureter') s += '<circle cx="62" cy="112" r="5" style="fill:var(--bad)"/>';
        s += '<path class="' + c(0, 'bladder', h) + '" d="M56 138 Q80 124 104 138 Q110 166 80 172 Q50 166 56 138 Z"/>';
        s += '<ellipse class="' + c(0, 'prostate', h) + '" cx="80" cy="180" rx="14" ry="9"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'urethra' ? 5 : 2.5) + ';stroke:' + (h === 'urethra' ? 'var(--bad)' : 'var(--muted)') + '" d="M80 172 L80 206"/>';
        return s;
      }},
    scrot: {lab: {testis: 'testis', epi: 'epididymis', cord: 'spermatic cord', penis: 'penis and foreskin', sac: 'fluid around the testis', canal: 'inguinal canal'},
      draw: function (h) {
        var s = '<path style="fill:none;stroke-width:' + (h === 'canal' ? 6 : 2) + ';stroke:' + (h === 'canal' ? 'var(--bad)' : 'var(--line)') + '" d="M20 30 L70 60"/>';
        if (h === 'canal') s += '<ellipse cx="44" cy="46" rx="16" ry="10" style="fill:var(--bad);opacity:.35"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'cord' ? 6 : 3) + ';stroke:' + (h === 'cord' ? 'var(--bad)' : 'var(--muted)') + '" d="M70 60 Q78 80 74 110 M96 60 Q92 80 98 110"/>';
        if (h === 'cord') s += '<path d="M66 84 q8 -6 16 0 q8 6 16 0" style="fill:none;stroke:var(--bad);stroke-width:3"/>';
        s += '<path class="' + c(0, 'penis', h) + '" d="M76 40 L94 40 L94 104 Q85 112 76 104 Z"/>';
        s += '<path class="' + (h === 'sac' ? HOT : OK) + '" d="M40 110 Q80 96 126 110 Q138 170 84 200 Q30 170 40 110 Z"/>';
        s += '<ellipse class="' + c(0, 'testis', h) + '" cx="66" cy="150" rx="15" ry="22"/><ellipse class="' + OK + '" cx="104" cy="150" rx="15" ry="22"/>';
        s += '<path class="' + c(0, 'epi', h) + '" d="M80 132 Q90 150 80 172 Q76 170 78 150 Q76 136 80 132 Z"/>';
        return s;
      }},
    breast: {lab: {lump: 'a lump in the breast tissue', duct: 'the ducts behind the nipple', nipple: 'the nipple', axilla: 'armpit nodes', whole: 'the whole breast', skin: 'a segment of breast'},
      draw: function (h) {
        var s = '<path class="' + (h === 'whole' ? HOT : OK) + '" d="M20 60 Q20 180 90 180 Q150 180 150 110 Q150 60 110 50 Z"/>';
        if (h === 'skin') s += '<path class="' + HOT + '" d="M96 120 L126 60 Q150 76 150 110 Z"/>';
        [[96, 120, 40, 70], [96, 120, 60, 150], [96, 120, 130, 150], [96, 120, 140, 96]].forEach(function (d) { s += '<path d="M' + d[0] + ' ' + d[1] + ' L' + d[2] + ' ' + d[3] + '" style="stroke:' + (h === 'duct' ? 'var(--bad)' : 'var(--line)') + ';stroke-width:' + (h === 'duct' ? 3 : 1.5) + '"/>'; });
        s += '<circle class="' + c(0, 'nipple', h) + '" cx="96" cy="120" r="8"/>';
        if (h === 'lump') s += '<circle class="' + HOT + '" cx="122" cy="80" r="12"/>';
        s += [[34, 30], [48, 22], [26, 44]].map(function (p) { return '<circle class="' + (h === 'axilla' ? HOT : OK) + '" cx="' + p[0] + '" cy="' + p[1] + '" r="6"/>'; }).join('');
        return s;
      }},
    neck: {lab: {thyroid: 'thyroid gland', nodule: 'a thyroid nodule'},
      draw: function (h) {
        var s = '<path class="' + OK + '" d="M40 10 Q80 0 120 10 L118 120 Q150 140 156 200 L4 200 Q10 140 42 120 Z"/>';
        s += '<rect x="72" y="40" width="16" height="140" rx="6" style="fill:var(--surface-2);stroke:var(--line)"/>';
        s += '<path class="' + (h === 'thyroid' ? HOT : OK) + '" d="M80 104 Q60 70 52 96 Q46 124 64 128 Q76 128 80 116 Q84 128 96 128 Q114 124 108 96 Q100 70 80 104 Z"/>';
        if (h === 'nodule') s += '<circle class="' + HOT + '" cx="96" cy="108" r="9"/>';
        return s;
      }},
    sugar: {lab: {islet: 'insulin cells in the pancreas', blood: 'sugar in the blood', cell: 'cells that need insulin', vessel: 'small and large vessels', nerve: 'nerves of the feet'},
      draw: function (h) {
        var s = '<path class="' + OK + '" d="M10 30 Q60 10 120 26 Q140 40 120 50 Q70 42 20 54 Q4 46 10 30 Z"/>';
        [[40, 36], [70, 32], [100, 36]].forEach(function (p) { s += '<circle class="' + (h === 'islet' ? HOT : OK) + '" cx="' + p[0] + '" cy="' + p[1] + '" r="6"/>'; });
        s += '<rect x="6" y="80" width="148" height="34" rx="17" class="' + (h === 'blood' || h === 'vessel' ? HOT : OK) + '" style="fill-opacity:.15"/>';
        for (var i = 0; i < 10; i++) s += '<rect x="' + (16 + i * 13) + '" y="' + (90 + (i % 2) * 8) + '" width="6" height="6" style="fill:' + (h === 'blood' ? 'var(--bad)' : 'var(--warn)') + '"/>';
        s += '<circle class="' + (h === 'cell' ? HOT : OK) + '" cx="44" cy="160" r="26"/><path d="M60 146 l10 -6 l2 12 Z" style="fill:var(--muted)"/>';
        s += '<path class="' + (h === 'nerve' ? HOT : OK) + '" d="M100 140 L140 140 L144 196 L106 196 Q96 190 100 140 Z"/>';
        s += '<path d="M120 140 Q116 170 126 194" style="fill:none;stroke:' + (h === 'nerve' ? 'var(--bad)' : 'var(--line)') + ';stroke-width:2"/>';
        return s;
      }},
    brain: {lab: {cortex: 'the cortex', vessel: 'a brain artery', mening: 'the meninges', sub: 'between the brain and the skull', whole: 'the whole brain, swelling', cbm: 'the cerebellum', nerve: 'a cranial nerve', deep: 'deep inside the brain'},
      draw: function (h) {
        var s = '<path style="fill:none;stroke:var(--muted);stroke-width:5" d="M20 120 Q12 30 90 22 Q156 24 150 110 Q146 140 128 150"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'mening' ? 6 : 2) + ';stroke:' + (h === 'mening' ? 'var(--bad)' : 'var(--line)') + '" d="M28 120 Q22 40 90 32 Q146 34 142 108"/>';
        if (h === 'sub') s += '<path class="' + HOT + '" d="M40 70 Q60 38 100 38 Q70 46 52 76 Z"/>';
        s += '<path class="' + (h === 'whole' ? HOT : OK) + '" d="M34 118 Q28 50 90 42 Q138 44 136 104 Q134 128 112 128 L70 132 Q40 134 34 118 Z"/>';
        s += '<path style="fill:none;stroke:var(--line)" d="M60 60 Q70 80 60 100 M90 50 Q96 76 86 96 M112 60 Q118 80 110 104"/>';
        if (h === 'cortex') s += '<path class="' + HOT + '" d="M90 44 Q130 46 134 90 L92 92 Z"/>';
        if (h === 'deep') s += '<circle class="' + HOT + '" cx="84" cy="96" r="14"/>';
        s += '<path class="' + c(0, 'cbm', h) + '" d="M100 130 Q128 126 132 146 Q120 160 100 152 Z"/>';
        s += '<path class="' + OK + '" d="M84 128 L98 128 L96 196 L86 196 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'vessel' ? 4 : 2) + ';stroke:' + (h === 'vessel' ? 'var(--bad)' : '#c55') + '" d="M90 150 L90 118 Q70 112 52 116 M90 118 Q112 112 126 116"/>';
        if (h === 'vessel') s += '<circle cx="62" cy="114" r="7" style="fill:var(--bad)"/>';
        if (h === 'nerve') s += '<path d="M86 140 Q60 150 40 160" style="fill:none;stroke:var(--bad);stroke-width:4"/>';
        if (h === 'whole') s += '<path d="M84 38 L84 18 M40 60 L26 50 M134 60 L148 50" style="stroke:var(--bad);stroke-width:2.5"/>';
        return s;
      }},
    nerve: {lab: {horn: 'motor nerve cells in the cord', root: 'a nerve root', nerve: 'a peripheral nerve', nmj: 'the nerve to muscle junction', muscle: 'the muscle itself'},
      draw: function (h) {
        var s = '<rect class="' + OK + '" x="14" y="10" width="34" height="190" rx="16"/>';
        s += '<path class="' + c(0, 'horn', h) + '" d="M24 90 Q31 70 38 90 Q31 110 24 90 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'root' ? 6 : 3) + ';stroke:' + (h === 'root' ? 'var(--bad)' : 'var(--muted)') + '" d="M38 90 L64 96"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'nerve' ? 5 : 3) + ';stroke:' + (h === 'nerve' ? 'var(--bad)' : 'var(--muted)') + (h === 'nerve' ? ';stroke-dasharray:8 4' : '') + '" d="M64 96 Q96 104 112 120"/>';
        s += '<circle class="' + c(0, 'nmj', h) + '" cx="116" cy="124" r="7"/>';
        s += '<path class="' + c(0, 'muscle', h) + '" d="M110 130 Q150 130 152 160 Q150 196 120 198 Q96 186 104 150 Z"/>';
        return s;
      }},
    joint: {lab: {cart: 'joint cartilage', bone: 'bone', syn: 'joint lining', implant: 'the new joint', whole: 'the whole joint'},
      draw: function (h) {
        var s = '<path class="' + c(0, 'bone', h) + '" d="M50 6 L110 6 L112 70 Q130 84 120 100 L40 100 Q30 84 48 70 Z"/>';
        s += '<path class="' + c(0, 'bone', h) + '" d="M38 120 L122 120 Q130 130 114 140 L110 206 L50 206 L46 140 Q30 130 38 120 Z"/>';
        if (h === 'implant') s += '<path d="M42 96 L118 96 L118 104 L42 104 Z M42 116 L118 116 L118 124 L42 124 Z M76 40 L84 40 L84 96 M76 124 L84 124 L84 170" style="fill:#9aa3ad;stroke:#6b737c;stroke-width:2"/>';
        else s += '<path d="M40 100 L120 100 M40 120 L120 120" style="stroke:' + (h === 'cart' ? 'var(--bad)' : 'var(--accent)') + ';stroke-width:' + (h === 'cart' ? 2 : 6) + (h === 'cart' ? ';stroke-dasharray:6 6' : '') + '"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'syn' || h === 'whole' ? 5 : 1.5) + ';stroke:' + (h === 'syn' || h === 'whole' ? 'var(--bad)' : 'var(--line)') + '" d="M30 80 Q16 110 30 140 M130 80 Q144 110 130 140"/>';
        if (h === 'cart') s += '<path d="M60 108 l4 6 M90 106 l-3 7" style="stroke:var(--bad);stroke-width:2"/>';
        return s;
      }},
    skin: {lab: {epi: 'the top layer of skin', derm: 'the dermis', fat: 'fat under the skin', foll: 'hair follicles', fascia: 'the fascia below the fat', nail: 'nails and hair', mole: 'pigment cells'},
      draw: function (h) {
        var s = '<rect class="' + c(0, 'epi', h) + '" x="6" y="30" width="148" height="22"/>';
        s += '<rect class="' + c(0, 'derm', h) + '" x="6" y="52" width="148" height="62"/>';
        s += '<rect class="' + c(0, 'fat', h) + '" x="6" y="114" width="148" height="50"/>';
        s += '<rect class="' + c(0, 'fascia', h) + '" x="6" y="164" width="148" height="12"/><rect x="6" y="176" width="148" height="30" style="fill:#c98b8b;opacity:.5"/>';
        for (var i = 0; i < 7; i++) s += '<circle cx="' + (18 + i * 20) + '" cy="140" r="7" style="fill:none;stroke:var(--line)"/>';
        s += '<path class="' + c(0, 'foll', h) + '" d="M50 30 L46 92 Q50 100 56 92 L54 30 Z"/><path d="M52 30 L58 8" style="stroke:var(--ink);stroke-width:1.5"/>';
        if (h === 'mole') s += '<ellipse cx="110" cy="40" rx="18" ry="8" style="fill:#4a3426"/><path d="M100 48 L96 80 M118 48 L124 86" style="stroke:#4a3426;stroke-width:3"/>';
        if (h === 'nail') s += '<path class="' + HOT + '" d="M96 10 L140 10 Q146 30 140 30 L96 30 Q90 30 96 10 Z"/>';
        return s;
      }},
    eye: {lab: {lid: 'eyelid margins', conj: 'conjunctiva', cornea: 'cornea', chamber: 'drainage angle', iris: 'iris', lens: 'lens', retina: 'retina', macula: 'macula', nerve: 'optic nerve', sclera: 'sclera', orbit: 'tissue around the eye', artery: 'retinal artery'},
      draw: function (h) {
        var s = '';
        if (h === 'orbit') s += '<circle class="' + HOT + '" cx="80" cy="104" r="76" style="fill-opacity:.15"/>';
        s += '<circle class="' + (h === 'sclera' ? HOT : OK) + '" cx="84" cy="104" r="60"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'retina' || h === 'artery' ? 5 : 2) + ';stroke:' + (h === 'retina' ? 'var(--bad)' : '#d79a7a') + '" d="M60 50 A58 58 0 1 1 60 158"/>';
        if (h === 'retina') s += '<path d="M120 60 Q128 80 120 100" style="fill:none;stroke:var(--bad);stroke-width:4"/>';
        if (h === 'artery') s += '<path d="M144 104 L120 90 M144 104 L118 116" style="stroke:var(--bad);stroke-width:3"/>';
        s += '<circle class="' + c(0, 'macula', h) + '" cx="142" cy="96" r="6"/>';
        s += '<path class="' + c(0, 'nerve', h) + '" d="M142 104 L160 98 L160 112 Z"/>';
        s += '<path class="' + c(0, 'cornea', h) + '" d="M34 72 Q14 104 34 136 L38 134 Q22 104 38 74 Z"/>';
        s += '<path class="' + c(0, 'chamber', h) + '" d="M38 74 Q22 104 38 134 L46 120 L46 88 Z"/>';
        s += '<path style="stroke-width:5;stroke:' + (h === 'iris' ? 'var(--bad)' : '#5c7d56') + '" d="M46 80 L46 92 M46 116 L46 128"/>';
        s += '<ellipse class="' + c(0, 'lens', h) + '" cx="56" cy="104" rx="10" ry="18"' + (h === 'lens' ? ' style="fill:#cfcab8;fill-opacity:1"' : '') + '/>';
        s += '<path class="' + c(0, 'lid', h) + '" d="M20 64 Q34 56 46 66 L40 72 Q32 66 24 70 Z M20 144 Q34 152 46 142 L40 136 Q32 142 24 138 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'conj' ? 5 : 1) + ';stroke:' + (h === 'conj' ? 'var(--bad)' : 'var(--line)') + '" d="M40 72 Q50 58 70 52 M40 136 Q50 150 70 156"/>';
        return s;
      }},
    ent: {lab: {canal: 'ear canal', middle: 'middle ear', inner: 'inner ear', nerve: 'the hearing and balance nerve', nose: 'inside the nose', sinus: 'sinuses', tonsil: 'tonsils', epi: 'epiglottis', airway: 'upper airway', face: 'facial nerve'},
      draw: function (h) {
        var s = '<path class="' + OK + '" d="M50 10 Q130 0 140 70 L154 96 L142 100 Q144 120 138 126 L144 134 Q132 160 110 160 L104 206 L40 206 L44 150 Q10 120 20 60 Q28 18 50 10 Z"/>';
        s += '<path class="' + c(0, 'sinus', h) + '" d="M110 44 L128 44 L126 60 L110 60 Z M108 70 L130 70 L132 90 L110 92 Z"/>';
        s += '<path class="' + c(0, 'nose', h) + '" d="M126 66 L148 98 L134 102 Q130 84 120 74 Z"/>';
        s += '<path class="' + c(0, 'airway', h) + '" d="M112 104 L128 104 L120 206 L106 206 Z" style="' + (h === 'airway' ? '' : 'fill:var(--surface-2)') + '"/>';
        s += '<circle class="' + c(0, 'tonsil', h) + '" cx="116" cy="124" r="7"/><path class="' + c(0, 'epi', h) + '" d="M114 146 Q124 140 128 150 L120 154 Z"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'canal' ? 6 : 3) + ';stroke:' + (h === 'canal' ? 'var(--bad)' : 'var(--muted)') + '" d="M30 84 L56 86"/>';
        s += '<rect class="' + c(0, 'middle', h) + '" x="56" y="78" width="12" height="16" rx="3"/>';
        s += '<circle class="' + c(0, 'inner', h) + '" cx="76" cy="86" r="7"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'nerve' ? 5 : 2) + ';stroke:' + (h === 'nerve' ? 'var(--bad)' : 'var(--line)') + '" d="M83 86 L98 84"/>';
        s += '<path style="fill:none;stroke-width:' + (h === 'face' ? 5 : 1.5) + ';stroke:' + (h === 'face' ? 'var(--bad)' : 'var(--line)') + '" d="M72 96 Q76 120 70 130 M70 130 L98 112 M70 130 L100 130 M70 130 L94 150"/>';
        s += '<path class="' + OK + '" d="M18 66 Q6 86 18 106 Q30 96 28 86 Q30 74 18 66 Z"/>';
        return s;
      }},
    mind: {lab: {mood: 'mood', swing: 'mood swings', thought: 'reality testing', fear: 'the alarm system', loop: 'intrusive loops', body: 'symptoms without damage', food: 'eating and body image', self: 'patterns of relating', habit: 'reward and habit', drug: 'brain chemistry from a drug', fog: 'attention and awareness', dev: 'brain development', stress: 'a reaction to an event', crisis: 'safety and risk'},
      draw: function (h) {
        var s = '<path class="' + OK + '" d="M40 200 L40 160 Q8 140 14 90 Q22 20 90 16 Q150 20 148 86 L160 112 L148 118 Q150 140 140 150 Q120 160 110 158 L110 200 Z"/>';
        var g = '<g style="fill:none;stroke:var(--bad);stroke-width:3.5">', e = '</g>';
        var icon = {
          mood: '<path d="M54 82 Q60 62 80 66 Q90 52 106 62 Q122 62 120 80 Q118 92 104 92 L62 92 Q50 92 54 82 Z"/><path d="M66 100 l-4 12 M82 100 l-4 12 M98 100 l-4 12"/>',
          swing: '<path d="M44 90 Q58 50 72 90 Q86 130 100 90 Q114 50 128 90"/>',
          thought: '<path d="M88 86 m-4 0 a4 4 0 1 1 8 0 a10 10 0 1 1 -20 0 a16 16 0 1 1 32 0 a22 22 0 1 1 -44 0"/>',
          fear: '<path d="M92 50 L72 92 L90 92 L78 128 L112 80 L94 80 L104 50 Z"/>',
          loop: '<path d="M64 92 a24 24 0 1 1 48 0 a24 24 0 1 1 -48 0"/><path d="M108 74 l6 10 l-12 2"/>',
          body: '<path d="M70 64 Q88 52 100 66 Q104 80 88 86 L88 98 M88 110 L88 112"/>',
          food: '<circle cx="88" cy="88" r="26"/><path d="M76 70 L76 106 M100 70 L100 106"/>',
          self: '<circle cx="70" cy="86" r="12"/><circle cx="108" cy="86" r="12"/><path d="M82 86 L96 86" style="stroke-dasharray:3 3"/>',
          habit: '<path d="M80 54 L96 54 L96 66 Q108 74 108 90 L108 124 L68 124 L68 90 Q68 74 80 66 Z"/>',
          drug: '<rect x="62" y="74" width="52" height="24" rx="12"/><path d="M88 74 L88 98"/>',
          fog: '<path d="M50 70 L126 70 M58 86 L118 86 M50 102 L126 102 M60 118 L110 118" style="stroke-dasharray:10 6"/>',
          dev: '<path d="M64 64 L88 64 Q88 56 96 56 Q104 56 104 64 L112 64 L112 88 Q120 88 120 96 Q120 104 112 104 L112 120 L64 120 Z"/>',
          stress: '<path d="M60 112 L80 70 L96 96 L112 60"/><path d="M106 60 L112 60 L112 68"/>',
          crisis: '<path d="M88 52 L124 116 L52 116 Z"/><path d="M88 74 L88 98 M88 106 L88 108"/>'
        };
        s += g + (icon[h] || icon.mood) + e;
        return s;
      }},
    blood: {lab: {rbc: 'red cells', wbc: 'white cells', flow: 'germs in the bloodstream', fluid: 'water and salts', drug: 'pain signals and painkillers'},
      draw: function (h) {
        var s = '<rect class="' + OK + '" x="4" y="50" width="152" height="110" rx="55"/>';
        var rbc = [[30, 80], [60, 100], [100, 82], [128, 110], [46, 128], [86, 132], [118, 140], [72, 70]];
        rbc.forEach(function (p, k) { if (h === 'rbc' && k % 2) return; s += '<ellipse cx="' + p[0] + '" cy="' + p[1] + '" rx="11" ry="7" style="fill:' + (h === 'rbc' ? '#e8a0a0' : '#d55') + ';opacity:.85"/>'; });
        s += '<circle cx="96" cy="108" r="12" style="fill:#9b7ad1;opacity:' + (h === 'wbc' ? 1 : 0.5) + '"/>' + (h === 'wbc' ? '<circle cx="56" cy="88" r="10" style="fill:#9b7ad1"/><circle cx="120" cy="80" r="9" style="fill:#9b7ad1"/>' : '');
        if (h === 'flow') [[40, 104], [70, 120], [110, 96], [134, 124], [90, 76]].forEach(function (p) { s += '<rect x="' + p[0] + '" y="' + p[1] + '" width="12" height="5" rx="2.5" style="fill:var(--bad)" transform="rotate(30 ' + p[0] + ' ' + p[1] + ')"/>'; });
        if (h === 'fluid') s += '<path d="M66 6 L94 6 L94 34 L80 46 L66 34 Z" class="' + HOT + '"/><path d="M80 46 L80 56" style="stroke:var(--bad);stroke-width:2"/>';
        if (h === 'drug') s += '<path d="M20 186 L60 186 L60 176 L100 176 L100 166 L140 166" style="fill:none;stroke:var(--bad);stroke-width:4"/>';
        if (h === 'rbc' || h === 'wbc' || h === 'flow') s += '<rect class="' + HOT + '" x="4" y="50" width="152" height="110" rx="55" style="fill-opacity:.08"/>';
        return s;
      }}
  };

  /* ---------- the body map for "spot it" ---------- */
  var LOC = {head: [0, 4], mind: [0, 8], eyes: [5, 13], face: [-6, 20], ear: [-14, 16], nose: [0, 18], mouth: [0, 24], neck: [0, 33], chest: [-10, 52], lchest: [10, 52], heart: [7, 56], lungs: [-12, 60], breast: [11, 56],
    back: [0, 64], epi: [0, 72], ruq: [-12, 76], luq: [12, 78], abdo: [0, 88], loin: [-19, 84], rif: [-12, 100], lif: [12, 100], supra: [0, 108], groin: [-14, 112], genit: [0, 118],
    rarm: [-36, 80], larm: [36, 80], hands: [-40, 102], lhand: [40, 102], joints: [-15, 148], legs: [-15, 162], lleg: [15, 162], feet: [-16, 192], skin: [18, 134], all: [30, 30]};

  function icon(test, x, y) {
    var t = test.toLowerCase(), s = '';
    if (/ecg|tape|holter/.test(t)) s = '<path d="M' + x + ' ' + (y + 6) + ' l5 0 l3 -9 l3 15 l3 -6 l6 0" style="fill:none;stroke:var(--bad);stroke-width:1.8"/>';
    else if (/x-ray|ct|mri|ultrasound|scan|echo|angio|dexa|dopp|pet|ogd|endoscop|colonoscop|cystoscop|laryngoscop|nasendoscop|fundoscop|slit|oct|tonometr|perimetr|audiogra|eeg|emg|nerve conduction|spirometr|peak flow/.test(t)) s = '<rect x="' + x + '" y="' + (y - 4) + '" width="18" height="14" rx="2" style="fill:#2b3138"/><circle cx="' + (x + 9) + '" cy="' + (y + 3) + '" r="4" style="fill:#c9ced4"/>';
    else if (/urine|dipstick|msu/.test(t)) s = '<path d="M' + (x + 2) + ' ' + (y - 4) + ' L' + (x + 16) + ' ' + (y - 4) + ' L' + (x + 14) + ' ' + (y + 10) + ' L' + (x + 4) + ' ' + (y + 10) + ' Z" style="fill:#f0d36a;stroke:var(--muted)"/>';
    else if (/biops|histol|smear|scrap|swab|microscop|culture|stain|aspirat|lumbar|csf|tap|fna/.test(t)) s = '<circle cx="' + (x + 9) + '" cy="' + (y + 3) + '" r="7" style="fill:none;stroke:var(--accent);stroke-width:2"/><circle cx="' + (x + 7) + '" cy="' + (y + 1) + '" r="1.6" style="fill:var(--accent)"/><circle cx="' + (x + 11) + '" cy="' + (y + 5) + '" r="1.6" style="fill:var(--accent)"/>';
    else if (/blood|fbc|crp|esr|troponin|u&e|lft|glucose|hba1c|tft|tsh|d-dimer|level|gas|bnp|ferritin|b12|folate|serolog|antibod|ttg|psa|calcium|lipid|amylase|lipase|lactate|cortisol|prolactin|ck|inr|clotting|monospot|hiv|igE|ige/.test(t)) s = '<rect x="' + (x + 5) + '" y="' + (y - 6) + '" width="8" height="18" rx="4" style="fill:var(--surface);stroke:var(--muted)"/><rect x="' + (x + 5) + '" y="' + (y + 3) + '" width="8" height="9" rx="3" style="fill:#c22"/>';
    else s = '<circle cx="' + (x + 7) + '" cy="' + (y + 1) + '" r="6" style="fill:none;stroke:var(--muted);stroke-width:2"/><path d="M' + (x + 11) + ' ' + (y + 5) + ' l6 6" style="stroke:var(--muted);stroke-width:2.5"/>';
    return s;
  }
  function person(who) {
    var w = who.toLowerCase(), kid = /child|baby|infant|toddler|teen|young people|school/.test(w), fem = /women|woman|female|pregnan|mother|girls/.test(w) && !/\bmen\b|\bman\b|male\b/.test(w), male = /\bmen\b|\bman\b|\bmale|boys/.test(w) && !fem;
    var k = kid ? 0.68 : 1, x = 70, top = kid ? 70 : 24;
    var s = '<g transform="translate(' + x + ' ' + top + ') scale(' + k + ')">' + '<circle class="snap-org" cx="0" cy="18" r="16"/>';
    s += fem ? '<path class="snap-org" d="M-14 40 L14 40 L30 150 L-30 150 Z"/><path d="M-16 10 Q0 -6 16 10 L18 30 Q10 22 8 12 Q0 18 -8 12 Q-10 22 -18 30 Z" style="fill:var(--muted)"/>' : '<path class="snap-org" d="M-18 40 L18 40 L22 100 L12 100 L10 176 L-10 176 L-12 100 L-22 100 Z"/>';
    if (male) s += '<path d="M-14 8 Q0 -2 14 8" style="fill:none;stroke:var(--muted);stroke-width:4"/>';
    return s + '</g>';
  }
  var UC = {e: 'var(--bad)', s: 'var(--warn)', u: '#d4a72c', c: '#8a5cc7', r: 'var(--good)'};

  DG.snapDef = function (id, s) {
    var O = ORG[s.o] || ORG.blood, lab = (O.lab && O.lab[s.r]) || s.r || '', topic = s.k === 't';
    var titles = topic ? ['🧬 The idea', '🧍 Who and when', '👀 What you see', '🧪 Check', '💊 The steps', '🚩 Danger', '🪝 The hook'] : ['🧬 What goes wrong', '🧍 Who gets it', '👀 Spot it', '🧪 Prove it', '💊 Treat', '🚩 Watch for', '🪝 The hook'];
    var caps = [
      '**' + titles[0].slice(3) + ':** ' + s.m,
      '**' + titles[1].slice(3) + ':** ' + s.w,
      '**Point to each one and say why it happens.**',
      '**Say the first test, then the one that proves it.**',
      '**Climb it out loud:** first move at the bottom, the cure at the top.',
      '**For each one, say what you would do and how fast.**',
      '**Replay the film in your head:** what breaks → who → spot it → prove it → treat → watch for.'
    ];
    DG.def(id, {t: '🎞️ ' + s.n, caps: caps, ms: 3200, snap: 1,
      draw: function (i) {
        var b = H.tag(250, 14, titles[i].slice(3), i === 5 ? 'b' : 'w', 'middle'), x0 = 172;
        if (i === 0) {
          var segs = s.m.split(/\s*→\s*/), y = 40, out = '';
          segs.forEach(function (g, k) { var L = wrap(g, 22); L.forEach(function (l, j) { out += T(x0, y + j * 15, l, k === segs.length - 1 ? 'dg-tr' : 'dg-tb', '', 12.5); }); y += (L.length - 1) * 15; if (k < segs.length - 1) { out += '<path d="M' + (x0 + 6) + ' ' + (y + 6) + ' l0 11 m-4 -4 l4 4 l4 -4" style="fill:none;stroke:var(--bad);stroke-width:1.8"/>'; y += 34; } });
          return S(340, Math.max(214, y + 16), '<g>' + O.draw(s.r) + '</g>' + H.tag(80, 206, lab, 'b', 'middle') + b + out, s.n);
        }
        if (i === 1) {
          var parts = s.w.split(/\s*·\s*/), out2 = '';
          var big = wrap(parts[0], 13), y2 = 46; big.forEach(function (l) { out2 += T(x0, y2, l, 'dg-tr', '', 18); y2 += 21; }); y2 += 8;
          parts.slice(1).forEach(function (p) { var L = wrap('• ' + p, 22); L.forEach(function (l, j) { out2 += T(x0, y2 + j * 15, l, 'dg-tb', '', 12.5); }); y2 += L.length * 15 + 8; });
          return S(340, Math.max(214, y2), person(s.w) + b + out2, s.n);
        }
        if (i === 2) {
          var out3 = H.body(70, 6, 200), y3 = 46, used = {};
          (s.s || []).forEach(function (it, k) {
            var p = LOC[it[1]] || LOC.all, rep = used[it[1]] = (used[it[1]] || 0) + 1, cx = 70 + p[0] + (rep - 1) * (p[0] > 0 ? -15 : 15), cy = 6 + p[1] + (rep > 2 ? 14 : 0);
            out3 += '<circle cx="' + cx + '" cy="' + cy + '" r="8" style="fill:var(--bad);opacity:.9"/>' + T(cx, cy + 3.5, String(k + 1), 'keep snap-n', 'middle', 9);
            out3 += '<circle cx="' + x0 + '" cy="' + (y3 - 4) + '" r="8" style="fill:var(--bad)"/>' + T(x0, y3 - 0.5, String(k + 1), 'keep snap-n', 'middle', 9); var L3 = wrap(it[0], 20); L3.forEach(function (l, j) { out3 += T(x0 + 14, y3 + j * 15, l, 'dg-tb', '', 12.5); }); y3 += L3.length * 15 + 12;
          });
          return S(340, Math.max(214, y3), out3 + b, s.n);
        }
        if (i === 3) {
          var out4 = '', y4 = 40;
          (s.x || []).forEach(function (it) {
            var N4 = wrap((it[2] ? '★ ' : '') + it[0] + (it[2] ? ': proves it' : ''), 38);
            out4 += icon(it[0], 10, y4); N4.forEach(function (l, j) { out4 += T(36, y4 + 6 + j * 15, l, it[2] ? 'dg-ta' : 'dg-tb', '', 12.5); });
            var L = it[1] ? wrap('→ ' + it[1], 40) : []; L.forEach(function (l, j) { out4 += T(36, y4 + 8 + N4.length * 15 + j * 15, l, it[2] ? 'dg-ta' : '', '', 12); });
            y4 += 16 + N4.length * 15 + L.length * 15;
          });
          return S(340, Math.max(214, y4 + 6), b + out4, s.n);
        }
        if (i === 4) {
          var st = s.t || [], n = st.length, out5 = '', top = 40, row = 50;
          st.forEach(function (it, k) {
            var y = top + (n - 1 - k) * row, w = 26 + k * 18;
            out5 += '<rect x="10" y="' + y + '" width="' + w + '" height="' + (row - 6) + '" rx="5" class="' + (k === n - 1 ? 'dg-hl' : 'dg-wl') + '"/>' + T(18, y + row / 2 + 1, String(k + 1), 'keep dg-tb', '', 12);
            var L5 = wrap(it, Math.floor((330 - w - 20) / 6.6)), y5 = y + (row - 6) / 2 - (L5.length - 1) * 7.5 + 4; L5.forEach(function (l, j) { out5 += T(w + 20, y5 + j * 15, l, k === n - 1 ? 'dg-ta' : 'dg-tb', '', 12.5); });
          });
          return S(340, Math.max(214, top + n * row + 6), b + out5, s.n);
        }
        if (i === 5) {
          var out6 = '<path d="M60 40 L110 130 L10 130 Z" style="fill:var(--bad);opacity:.15;stroke:var(--bad);stroke-width:2"/><path d="M60 70 L60 104 M60 114 L60 117" style="stroke:var(--bad);stroke-width:5;stroke-linecap:round"/>', y6 = 40;
          (s.d || []).forEach(function (it) { out6 += '<circle cx="134" cy="' + (y6 - 4) + '" r="6" style="fill:' + (UC[it[1]] || UC.u) + '"/>'; var L = wrap(it[0], 25); L.forEach(function (l, j) { out6 += T(146, y6 + j * 15, l, 'dg-tb', '', 12.5); }); y6 += L.length * 15 + 12; });
          out6 += T(14, 160, '🔴 now  🟠 today', 'dg-tm', '', 9) + T(14, 174, '🟡 soon  🟣 cancer pathway', 'dg-tm', '', 9);
          return S(340, Math.max(214, y6), b + out6, s.n);
        }
        var L7 = wrap(s.h, 24), out7 = '<circle cx="60" cy="80" r="34" style="fill:var(--warn);opacity:.3;stroke:var(--warn);stroke-width:2"/><path d="M48 112 L72 112 M50 122 L70 122" style="stroke:var(--muted);stroke-width:4;stroke-linecap:round"/><path d="M52 92 Q60 64 68 92" style="fill:none;stroke:var(--warn);stroke-width:3"/>';
        L7.forEach(function (l, j) { out7 += T(116, 50 + j * 19, l, 'dg-ta', '', 15); });
        return S(340, Math.max(214, 60 + L7.length * 19), b + out7, s.n);
      }});
  };
  DG.ORG = ORG; DG.LOC = LOC;
  var css = '.snap-org{fill:var(--surface);stroke:var(--muted);stroke-width:1.4}.snap-hot{fill:var(--bad);fill-opacity:.32;stroke:var(--bad);stroke-width:2.2;animation:snapP 1.6s ease-in-out infinite}' +
    '@keyframes snapP{50%{fill-opacity:.55}}.dg-svg .snap-n{fill:#fff;font-weight:800}@media (prefers-reduced-motion:reduce){.snap-hot{animation:none}}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
})();
