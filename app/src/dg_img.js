/* medengine-OSCE v1.3: case pictures for the imaging stations: chest X-ray, abdominal X-ray, CT and ECG schematics. */
(function () {
  var H = DG.H, S = H.svg, T = H.t;
  var M = function () { return window.MEV || {}; };

  /* ---------- chest X-ray: MEV schematics plus new kinds drawn on top of the normal film ---------- */
  var RL = 'M42 40 C 30 72, 28 112, 34 136 Q 60 110 88 128 L 90 46 C 76 30, 56 30, 42 40 Z';
  var LL = 'M158 40 C 170 72, 172 112, 166 139 Q 140 112 112 129 L 110 46 C 124 30, 144 30, 158 40 Z';
  DG.cxr = function (kind) {
    var base = M().cxr ? M().cxr(['eff', 'ptx', 'perf'].indexOf(kind) >= 0 ? kind : 'normal') : '';
    if (!base) return '';
    var id = H.uid(), o = '';
    if (kind === 'cons') {
      o += '<clipPath id="' + id + '"><path d="' + RL + '"/></clipPath><g clip-path="url(#' + id + ')"><path d="M30 96 Q50 84 86 96 L90 130 Q60 112 30 140 Z" fill="#cfcfcf" opacity=".75"/>';
      for (var k = 0; k < 9; k++) o += '<circle cx="' + (40 + (k * 37) % 44) + '" cy="' + (98 + (k * 13) % 26) + '" r="' + (4 + k % 3) + '" fill="#e8e8e8" opacity=".5"/>';
      o += '<path d="M84 98 L66 108 L54 118 M66 108 L62 122 M74 104 L70 96" stroke="#141414" stroke-width="2.2" fill="none"/></g>';
      o += '<path d="M14 150 L46 118" stroke="#f0b04a" stroke-width="1.5"/><text x="2" y="162" fill="#f0b04a" font-size="10" font-weight="700">air bronchograms</text>';
    }
    if (kind === 'hf') {
      o += '<path d="M80 72 C 70 92, 70 118, 82 132 C 100 144, 146 146, 164 128 C 172 108, 160 86, 128 76 C 116 70, 96 68, 80 72 Z" fill="#d8d8d8" opacity=".95"/>';
      o += '<defs><radialGradient id="' + id + '"><stop offset="0" stop-color="#ddd" stop-opacity=".8"/><stop offset="1" stop-color="#ddd" stop-opacity="0"/></radialGradient></defs><ellipse cx="66" cy="84" rx="30" ry="26" fill="url(#' + id + ')"/><ellipse cx="136" cy="84" rx="30" ry="26" fill="url(#' + id + ')"/>';
      [118, 122, 126].forEach(function (y) { o += '<path d="M33 ' + y + ' l9 0 M167 ' + (y + 2) + ' l-9 0" stroke="#e6e6e6" stroke-width="1.2"/>'; });
      o += '<path d="M34 136 Q 44 128 50 134 L50 140 Z M166 139 Q 156 130 150 136 L150 142 Z" fill="#cfcfcf"/>';
      o += '<text x="122" y="168" fill="#f0b04a" font-size="10" font-weight="700">big heart, bat wings</text>';
    }
    if (kind === 'mass') {
      o += '<circle cx="62" cy="62" r="11" fill="#d6d6d6"/>' + [0, 45, 90, 135, 180, 225, 270, 315].map(function (a) { var r = a * Math.PI / 180; return '<path d="M' + (62 + 11 * Math.cos(r)).toFixed(1) + ' ' + (62 + 11 * Math.sin(r)).toFixed(1) + ' l' + (6 * Math.cos(r)).toFixed(1) + ' ' + (6 * Math.sin(r)).toFixed(1) + '" stroke="#d6d6d6" stroke-width="1.4"/>'; }).join('');
      o += '<ellipse cx="80" cy="84" rx="9" ry="12" fill="#cfcfcf"/><path d="M8 30 L50 56" stroke="#f0b04a" stroke-width="1.5"/><text x="2" y="24" fill="#f0b04a" font-size="10" font-weight="700">spiculated mass</text>';
    }
    return base.replace('</svg>', o + '<text class="keep" x="8" y="14" fill="#9a9a9a" font-size="9" font-weight="700">R</text></svg>');
  };

  /* ---------- abdominal X-ray ---------- */
  DG.axr = function (kind) {
    var id = H.uid(), s = '<rect width="220" height="240" fill="#050505"/><path d="M14 8 L206 8 L214 236 L6 236 Z" fill="#4c4c4c"/>';
    s += '<path d="M14 40 Q60 30 92 60 L92 90 Q50 96 16 80 Z" fill="#5d5d5d"/>';
    for (var v = 0; v < 7; v++) s += '<rect x="98" y="' + (14 + v * 26) + '" width="24" height="20" rx="4" fill="#b8b8b8"/>';
    s += '<path d="M40 196 Q60 168 104 192 L110 236 L30 236 Z M180 196 Q160 168 116 192 L110 236 L190 236 Z" fill="#a9a9a9" opacity=".9"/><circle cx="60" cy="218" r="12" fill="#c6c6c6"/><circle cx="160" cy="218" r="12" fill="#c6c6c6"/>';
    var gas = '#0b0b0b', wall = '#8a8a8a';
    var loop = function (x, y, w, h) { var g = '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (h / 2) + '" fill="' + gas + '" stroke="' + wall + '"/>'; for (var k = x + 6; k < x + w - 4; k += 6) g += '<line x1="' + k + '" y1="' + (y + 2) + '" x2="' + k + '" y2="' + (y + h - 2) + '" stroke="#9a9a9a" stroke-width="1"/>'; return g; };
    var colon = function (wd, haustra) {
      var g = '<path d="M40 190 L40 70 Q40 52 60 52 L160 52 Q180 52 180 70 L180 180 Q170 196 140 190" fill="none" stroke="' + wall + '" stroke-width="' + (wd + 2) + '" stroke-linejoin="round"/><path d="M40 190 L40 70 Q40 52 60 52 L160 52 Q180 52 180 70 L180 180 Q170 196 140 190" fill="none" stroke="' + gas + '" stroke-width="' + wd + '" stroke-linejoin="round"/>';
      if (haustra) [[40, 80], [40, 110], [40, 140], [40, 170], [80, 52], [110, 52], [140, 52], [180, 80], [180, 110], [180, 140]].forEach(function (p) { var vert = p[0] === 40 || p[0] === 180; g += vert ? '<path d="M' + (p[0] - wd / 2) + ' ' + p[1] + ' q' + (wd / 3) + ' 3 0 6 M' + (p[0] + wd / 2) + ' ' + p[1] + ' q' + (-wd / 3) + ' 3 0 6" stroke="#9a9a9a" fill="none"/>' : '<path d="M' + p[0] + ' ' + (52 - wd / 2) + ' q3 ' + (wd / 3) + ' 6 0 M' + p[0] + ' ' + (52 + wd / 2) + ' q3 ' + (-wd / 3) + ' 6 0" stroke="#9a9a9a" fill="none"/>'; });
      return g;
    };
    if (kind === 'normal') s += colon(8, true);
    if (kind === 'sbo') { [[70, 80, 80, 16], [62, 102, 96, 16], [70, 124, 84, 16], [64, 146, 92, 16], [74, 168, 72, 16]].forEach(function (l) { s += loop(l[0], l[1], l[2], l[3]); }); s += '<text x="4" y="232" fill="#f0b04a" font-size="10" font-weight="700">central loops, lines all the way across</text>'; }
    if (kind === 'lbo' || kind === 'rigler') { s += colon(22, kind === 'lbo'); if (kind === 'lbo') s += '<text x="4" y="232" fill="#f0b04a" font-size="10" font-weight="700">peripheral, haustra part-way across</text>'; }
    if (kind === 'rigler') { s = s.replace(/fill="#4c4c4c"/, 'fill="#262626"'); s += '<path d="M40 190 L40 70 Q40 52 60 52 L160 52 Q180 52 180 70 L180 180" fill="none" stroke="#e0e0e0" stroke-width="1.6" transform="translate(-12 0)"/><text x="4" y="232" fill="#f0b04a" font-size="10" font-weight="700">both sides of the wall visible: Rigler\'s</text>'; }
    if (kind === 'volv') { s += '<path d="M166 196 C 214 120, 150 20, 70 40 C 20 52, 30 120, 120 150 C 150 160, 160 180, 150 200" fill="' + gas + '" stroke="' + wall + '" stroke-width="3"/><path d="M155 194 C 150 140, 110 90, 70 64" stroke="#8a8a8a" stroke-width="5" fill="none"/><text x="4" y="232" fill="#f0b04a" font-size="10" font-weight="700">coffee bean from the left lower quadrant</text>'; }
    if (kind === 'mega') { s += colon(10, false) + '<rect x="46" y="38" width="128" height="32" rx="16" fill="' + gas + '" stroke="#9a9a9a" stroke-width="4"/>' + [70, 100, 130, 150].map(function (x) { return '<ellipse cx="' + x + '" cy="40" rx="5" ry="4" fill="#7a7a7a"/>'; }).join('') + '<text x="4" y="232" fill="#f0b04a" font-size="10" font-weight="700">transverse colon over 6 cm, no haustra</text>'; }
    s += '<text class="keep" x="8" y="22" fill="#9a9a9a" font-size="9" font-weight="700">R</text>';
    return '<svg viewBox="0 0 220 240" role="img" aria-label="Abdominal X-ray schematic: ' + kind + '">' + s + '</svg>';
  };

  /* ---------- CT axial slice ---------- */
  DG.ct = function (kind) {
    var s = '<rect width="240" height="200" fill="#000"/>', lungW = kind === 'mass';
    if (kind === 'pe' || kind === 'mass') {
      s += '<ellipse cx="120" cy="104" rx="108" ry="80" fill="' + (lungW ? '#9a9a9a' : '#6f6f6f') + '"/>';
      s += '<path d="M28 104 Q30 50 84 40 Q108 50 104 104 Q106 156 80 168 Q32 160 28 104 Z" fill="' + (lungW ? '#1d1d1d' : '#050505') + '"/><path d="M212 104 Q210 50 156 40 Q132 50 136 104 Q134 156 160 168 Q208 160 212 104 Z" fill="' + (lungW ? '#1d1d1d' : '#050505') + '"/>';
      if (lungW) for (var k = 0; k < 18; k++) s += '<circle cx="' + (44 + (k * 53) % 50) + '" cy="' + (60 + (k * 31) % 96) + '" r="1.4" fill="#777"/><circle cx="' + (150 + (k * 47) % 52) + '" cy="' + (62 + (k * 29) % 94) + '" r="1.4" fill="#777"/>';
      s += '<ellipse cx="124" cy="120" rx="24" ry="26" fill="' + (lungW ? '#bbb' : '#8b8b8b') + '"/><circle cx="140" cy="72" r="11" fill="' + (lungW ? '#bbb' : '#f2f2f2') + '"/>';
      s += '<path d="M106 76 Q88 78 70 86" stroke="' + (lungW ? '#bbb' : '#f2f2f2') + '" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M120 66 Q130 62 140 62" stroke="#f2f2f2" stroke-width="8" fill="none"/>';
      s += '<rect x="110" y="160" width="20" height="18" rx="4" fill="#eee"/>';
      if (kind === 'pe') s += '<ellipse cx="86" cy="80" rx="8" ry="4" fill="#3a3a3a"/><path d="M60 40 L84 76" stroke="#f0b04a" stroke-width="1.5"/><text x="20" y="34" fill="#f0b04a" font-size="10" font-weight="700">dark filling defect</text>';
      if (kind === 'mass') s += '<circle cx="66" cy="96" r="14" fill="#c8c8c8"/>' + [0, 60, 120, 180, 240, 300].map(function (a) { var r = a * Math.PI / 180; return '<path d="M' + (66 + 14 * Math.cos(r)).toFixed(1) + ' ' + (96 + 14 * Math.sin(r)).toFixed(1) + ' l' + (7 * Math.cos(r)).toFixed(1) + ' ' + (7 * Math.sin(r)).toFixed(1) + '" stroke="#c8c8c8" stroke-width="1.6"/>'; }).join('') + '<text x="16" y="186" fill="#f0b04a" font-size="10" font-weight="700">lung window: spiculated mass</text>';
    } else {
      s += '<ellipse cx="120" cy="104" rx="108" ry="82" fill="#6a6a6a"/><ellipse cx="120" cy="104" rx="100" ry="74" fill="#585858"/>';
      s += '<path d="M24 90 Q34 40 96 34 Q112 70 92 110 Q60 130 26 120 Z" fill="#7d7d7d"/><path d="M216 92 Q206 54 168 44 Q160 70 176 96 Q196 104 216 92 Z" fill="#787878"/>';
      s += '<ellipse cx="80" cy="134" rx="14" ry="18" fill="#8e8e8e"/><ellipse cx="160" cy="134" rx="14" ry="18" fill="#8e8e8e"/><ellipse cx="80" cy="134" rx="5" ry="6" fill="#d8d8d8"/><ellipse cx="160" cy="134" rx="5" ry="6" fill="#d8d8d8"/>';
      s += '<rect x="108" y="150" width="24" height="22" rx="5" fill="#eee"/>';
      if (kind === 'aaa') s += '<circle cx="124" cy="122" r="28" fill="#4a4a4a" stroke="#9a9a9a" stroke-width="3"/><circle cx="128" cy="118" r="13" fill="#f2f2f2"/><path d="M190 30 L150 104" stroke="#f0b04a" stroke-width="1.5"/><text x="150" y="24" fill="#f0b04a" font-size="10" font-weight="700">7 cm aorta</text>';
      else s += '<circle cx="124" cy="132" r="8" fill="#f2f2f2"/>';
      if (kind === 'air') s += '<path d="M40 52 Q80 26 132 30 Q100 40 70 58 Q52 64 40 52 Z" fill="#000"/><path d="M150 14 L100 38" stroke="#f0b04a" stroke-width="1.5"/><text x="150" y="12" fill="#f0b04a" font-size="10" font-weight="700">free air, front</text>';
    }
    s += '<text class="keep" x="8" y="104" fill="#9a9a9a" font-size="10" font-weight="700">R</text><text class="keep" x="224" y="104" fill="#9a9a9a" font-size="10" font-weight="700">L</text>';
    return '<svg viewBox="0 0 240 200" role="img" aria-label="CT schematic: ' + kind + '">' + s + '</svg>';
  };

  /* ---------- ECG rhythm strips (extra to the MEV set) ---------- */
  var g = function (t, c, w) { var x = (t - c) / w; return Math.exp(-0.5 * x * x); };
  function strip(o) {
    var W = o.ms * 0.1, Ht = 100, base = 62, k = 40, h = '<svg class="mev-ecg" viewBox="0 0 ' + W + ' ' + Ht + '" role="img" aria-label="' + H.esc(o.label) + '"><rect class="bg" width="' + W + '" height="' + Ht + '"/>';
    for (var x = 0; x <= W; x += 4) h += '<line class="' + (x % 20 ? 'g1' : 'g2') + '" x1="' + x + '" y1="0" x2="' + x + '" y2="' + Ht + '"/>';
    for (var y = 2; y <= Ht; y += 4) h += '<line class="' + ((y - 2) % 20 ? 'g1' : 'g2') + '" x1="0" y1="' + y + '" x2="' + W + '" y2="' + y + '"/>';
    var pts = [];
    for (var t = 0; t <= o.ms; t += 4) {
      var v = 0;
      o.q.forEach(function (q) {
        if (o.p) v += 0.15 * g(t, q - 120, 16);
        v += -0.08 * g(t, q + 8, 6) + 1.1 * g(t, q + 30, 8) - 0.28 * g(t, q + 52, 8);
        if (o.ste) { var a = 1 / (1 + Math.exp(-(t - q - 60) / 6)), z = 1 / (1 + Math.exp((t - q - 230) / 18)); v += o.ste * a * z; }
        v += (o.ste ? 0.18 : 0.28) * g(t, q + (o.fast ? 200 : 300), o.fast ? 30 : 42);
      });
      if (o.fib) v += 0.05 * Math.sin(t / 19) + 0.035 * Math.sin(t / 7.3 + 1) + 0.025 * Math.sin(t / 31 + 2);
      pts.push((t * 0.1).toFixed(1) + ',' + (base - v * k).toFixed(1));
    }
    h += '<polyline class="tr" points="' + pts.join(' ') + '"/>';
    (o.ann || []).forEach(function (a) { h += '<text x="' + (a[0] * 0.1).toFixed(1) + '" y="' + (a[2] || 12) + '" text-anchor="middle" class="' + (a[3] || 'pm') + '">' + H.esc(a[1]) + '</text>'; });
    return h + '</svg>';
  }
  DG.ECG = {
    af: function () { return strip({ms: 5600, q: [300, 820, 1240, 1920, 2380, 2760, 3420, 3900, 4600, 5050], fib: true, label: 'Atrial fibrillation: irregularly irregular, no P waves', ann: [[2600, 'no P waves · irregular', 94]]}); },
    stemi: function () { return strip({ms: 5600, q: [300, 1100, 1900, 2700, 3500, 4300, 5100], p: true, ste: 0.42, label: 'ST elevation, as seen in II, III and aVF in an inferior STEMI', ann: [[2900, 'ST elevation', 12]]}); },
    svt: function () { var q = []; for (var t = 200; t < 5500; t += 333) q.push(t); return strip({ms: 5600, q: q, fast: true, label: 'SVT: regular narrow complexes at 180, no visible P waves', ann: [[2800, 'regular · 180 · narrow', 94]]}); },
    norm: function () { return strip({ms: 5600, q: [300, 1100, 1900, 2700, 3500, 4300, 5100], p: true, label: 'Normal sinus rhythm'}); }
  };
  ['chb', 'hiK', 'wpw', 'lbbb', 'mob1', 'mob2', 'loK'].forEach(function (k) { DG.ECG[k] = function () { return M().ECG && M().ECG[k] ? M().ECG[k]() : ''; }; });
})();
