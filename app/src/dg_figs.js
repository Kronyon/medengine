/* medengine 🧭 master poster figures. Each is drawn as SVG so it works offline and in both themes.
   The figure is the anchor picture; the words and the 🔒 pills sit in the columns underneath. Needs dg_core.js and dg_poster.js. */
(function () {
  var P = window.PO; if (!P) return;
  var e = P.esc, F = P.FIG, uid = 0;
  function T(x, y, s, c, a, st) { return '<text x="' + (+x).toFixed(1) + '" y="' + (+y).toFixed(1) + '"' + (c ? ' class="' + c + '"' : '') + (a ? ' text-anchor="' + a + '"' : '') + (st ? ' style="' + st + '"' : '') + '>' + e(s) + '</text>'; }
  function L(x1, y1, x2, y2, st) { return '<line x1="' + (+x1).toFixed(1) + '" y1="' + (+y1).toFixed(1) + '" x2="' + (+x2).toFixed(1) + '" y2="' + (+y2).toFixed(1) + '" style="' + (st || 'stroke:var(--muted);stroke-width:1.2') + '"/>'; }
  function svg(w, h, body, label) { return '<svg viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="' + e(label) + '">' + body + '</svg>'; }
  function dot(x, y, r, fill) { return '<circle cx="' + (+x).toFixed(1) + '" cy="' + (+y).toFixed(1) + '" r="' + r + '" style="fill:' + fill + '"/>'; }
  function num(x, y, n, col) { return dot(x, y, 9, col || 'var(--po-watch)') + T(x, y + 4, String(n), 'w', 'middle', 'font-size:10px'); }
  function zig(x1, x2, base, a1, a2, step) { var p = [], up = true; for (var x = x1; x <= x2; x += step) { var a = a1 + (a2 - a1) * (x - x1) / Math.max(1, x2 - x1); p.push(x.toFixed(1) + ',' + (base - (up ? a : -a * 0.35)).toFixed(1)); up = !up; } return p.join(' '); }
  /* two-line label: bold name, muted detail */
  function lab(x, y, h, d, a, col) { return T(x, y, h, 'b', a, col ? 'fill:' + col : '') + (d ? T(x, y + 15, d, 'm', a) : ''); }

  /* 🫁 spirometry: volume-time and flow-volume, drawn from real ratios */
  F.spiro = function () {
    var s = '', C = [['Normal', 4.5, 0.621, 'var(--muted)', 'big and fast · ratio 0.8'], ['Obstructive', 4.0, 1.443, 'var(--po-test)', 'slow climb, scooped loop · ratio under 0.7'], ['Restrictive', 2.4, 0.396, 'var(--po-who)', 'small but fast · ratio normal or high']];
    var x0 = 64, y0 = 214, sx = 40, sy = 34, X = function (t) { return x0 + t * sx; }, Y = function (v) { return y0 - v * sy; };
    s += T(x0 + 120, 22, 'Volume against time', 'b', 'middle') + L(x0, y0, X(6) + 8, y0) + L(x0, y0, x0, Y(5) - 8);
    for (var t = 0; t <= 6; t++) s += T(X(t), y0 + 15, t + ' s', 'm', 'middle');
    for (var v = 1; v <= 5; v++) s += T(x0 - 6, Y(v) + 4, v + ' L', 'm', 'end');
    s += L(X(1), y0, X(1), Y(5) - 4, 'stroke:var(--muted);stroke-dasharray:3 3') + T(X(1) + 4, Y(5) + 6, 'FEV1 is read at 1 second', 'm');
    C.forEach(function (c) {
      var pts = []; for (var i = 0; i <= 60; i++) { var tt = i / 10; pts.push(X(tt).toFixed(1) + ',' + Y(c[1] * (1 - Math.exp(-tt / c[2]))).toFixed(1)); }
      s += '<polyline points="' + pts.join(' ') + '" style="fill:none;stroke:' + c[3] + ';stroke-width:3;stroke-linejoin:round"/>' + dot(X(1), Y(c[1] * (1 - Math.exp(-1 / c[2]))), 4.5, c[3]);
    });
    var a0 = 430, b0 = 214, ax = 54, ay = 16, A = function (v) { return a0 + v * ax; }, B = function (f) { return b0 - f * ay; };
    s += T(a0 + 140, 22, 'Flow against volume, breathing out', 'b', 'middle') + L(a0, b0, A(5) + 8, b0) + L(a0, b0, a0, B(10) - 6);
    for (var w = 1; w <= 5; w++) s += T(A(w), b0 + 15, w + ' L', 'm', 'middle');
    [2, 4, 6, 8, 10].forEach(function (f) { s += T(a0 - 6, B(f) + 4, String(f), 'm', 'end'); });
    s += T(a0 - 30, B(10) - 12, 'L/s', 'm');
    var path = function (d, c) { return '<path d="' + d + '" style="fill:none;stroke:' + c + ';stroke-width:3;stroke-linejoin:round"/>'; };
    s += path('M' + A(0) + ' ' + B(0) + ' Q' + A(0.12) + ' ' + B(9.2) + ' ' + A(0.6) + ' ' + B(8.2) + ' L' + A(4.5) + ' ' + B(0), C[0][3]);
    s += path('M' + A(0) + ' ' + B(0) + ' Q' + A(0.08) + ' ' + B(5.6) + ' ' + A(0.4) + ' ' + B(5.0) + ' Q' + A(1.1) + ' ' + B(0.6) + ' ' + A(4.0) + ' ' + B(0), C[1][3]);
    s += path('M' + A(0) + ' ' + B(0) + ' Q' + A(0.08) + ' ' + B(6.8) + ' ' + A(0.35) + ' ' + B(6.2) + ' L' + A(2.4) + ' ' + B(0), C[2][3]);
    C.forEach(function (c, k) { var x = 40 + k * 232; s += L(x, 252, x + 22, 252, 'stroke:' + c[3] + ';stroke-width:4') + lab(x + 28, 256, c[0], c[4]); });
    return svg(720, 290, s, 'Spirometry: normal, obstructive and restrictive curves');
  };

  /* 🫀 mitral stenosis: the heart sounds on a timeline */
  F.ms = function () {
    var s = '', b = 128;
    s += T(360, 22, 'At the apex, with the bell, patient rolled onto the left side', 'b', 'middle');
    s += L(70, 40, 250, 40, 'stroke:var(--po-test);stroke-width:2') + T(160, 36, 'Systole', 'm', 'middle') + L(254, 40, 640, 40, 'stroke:var(--po-cause);stroke-width:2') + T(447, 36, 'Diastole', 'm', 'middle');
    s += L(40, b, 680, b, 'stroke:var(--line);stroke-width:1.5');
    s += L(70, b, 70, b - 62, 'stroke:var(--ink);stroke-width:6') + T(70, b - 70, 'Loud S1', 'b', 'middle');
    s += L(250, b, 250, b - 36, 'stroke:var(--ink);stroke-width:4') + T(250, b - 44, 'S2', 'b', 'middle');
    s += L(298, b, 298, b - 30, 'stroke:var(--po-watch);stroke-width:2.5') + T(304, b - 38, 'Opening snap', 'b', 'start', 'fill:var(--po-watch)');
    s += '<polyline points="' + zig(310, 560, b, 13, 5, 6) + ' ' + zig(564, 632, b, 6, 22, 4) + '" style="fill:none;stroke:var(--po-test);stroke-width:2"/>';
    s += T(430, b + 32, 'Low rumble: blood squeezing through the slit', 'm', 'middle') + T(626, b - 50, 'Presystolic surge,', 'm', 'end') + T(626, b - 38, 'gone in AF', 'm', 'end');
    s += L(640, b, 640, b - 62, 'stroke:var(--ink);stroke-width:6') + T(664, b - 70, 'S1', 'b', 'middle');
    s += L(252, b + 52, 296, b + 52, 'stroke:var(--po-watch);stroke-width:2') + L(252, b + 46, 252, b + 58, 'stroke:var(--po-watch);stroke-width:2') + L(296, b + 46, 296, b + 58, 'stroke:var(--po-watch);stroke-width:2');
    s += T(306, b + 56, 'The shorter this gap from S2 to the snap, the tighter the valve', 'm');
    return svg(720, 200, s, 'Mitral stenosis heart sounds: loud S1, opening snap, mid-diastolic rumble');
  };

  /* 👁️ anterior uveitis: the front of the eye */
  F.eye = function () {
    var id = 'poeye' + (++uid), cx = 190, cy = 122, s = '';
    var lid = 'M50 122 Q190 12 330 122 Q190 232 50 122 Z';
    s += '<defs><clipPath id="' + id + '"><path d="' + lid + '"/></clipPath></defs><path d="' + lid + '" style="fill:#f7f1e8;stroke:var(--muted);stroke-width:2"/>';
    s += '<g clip-path="url(#' + id + ')">';
    for (var a = 0; a < 360; a += 15) { var r = a * Math.PI / 180; s += L(cx + 62 * Math.cos(r), cy + 62 * Math.sin(r), cx + (88 + (a % 30 ? 0 : 14)) * Math.cos(r), cy + (88 + (a % 30 ? 0 : 14)) * Math.sin(r), 'stroke:#d24a4a;stroke-width:1.6;opacity:.75'); }
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="60" style="fill:none;stroke:#cf3535;stroke-width:13;opacity:.55"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="53" style="fill:#7a5536"/>';
    for (var b = 0; b < 360; b += 12) { var q = b * Math.PI / 180; s += L(cx + 14 * Math.cos(q), cy + 14 * Math.sin(q), cx + 50 * Math.cos(q), cy + 50 * Math.sin(q), 'stroke:#5c3e26;stroke-width:1.2'); }
    var pts = []; for (var c = 0; c < 360; c += 20) { var rr = (c >= 100 && c <= 160) ? 6.5 : 11, z = c * Math.PI / 180; pts.push((cx + rr * Math.cos(z)).toFixed(1) + ',' + (cy + rr * Math.sin(z)).toFixed(1)); }
    s += '<polygon points="' + pts.join(' ') + '" style="fill:#0c0c0c"/>';
    s += '<path d="M' + (cx - 32.4) + ' ' + (cy + 42) + ' A53 53 0 0 0 ' + (cx + 32.4) + ' ' + (cy + 42) + ' Z" style="fill:#f4f0e2"/>';
    s += '<circle cx="' + cx + '" cy="' + cy + '" r="53" style="fill:#fff;opacity:.13"/>';
    [[176, 150], [188, 156], [201, 153], [212, 147], [168, 143]].forEach(function (k) { s += dot(k[0], k[1], 2.3, '#efe6d6'); });
    s += '</g>';
    var call = [[236, 76, 46, 'Ring of red hugging the cornea', 'ciliary flush'], [201, 115, 92, 'Small pupil', 'the iris muscle is in spasm'], [186, 128, 138, 'Irregular edge', 'the iris sticks to the lens'], [214, 168, 184, 'White fluid level', 'hypopyon, when severe'], [212, 147, 230, 'Hazy front chamber', 'cells and flare on the slit lamp']];
    call.forEach(function (k, i) { s += L(k[0], k[1], 382, k[2] - 4, 'stroke:var(--muted);stroke-width:1') + dot(k[0], k[1], 2.6, 'var(--ink)') + num(394, k[2] - 4, i + 1, 'var(--po-spot)') + lab(410, k[2], k[3], k[4]); });
    return svg(720, 252, s, 'Anterior uveitis: ciliary flush, small irregular pupil, hypopyon');
  };

  /* 👅 sore throat: the score bands and what each one means */
  F.throat = function () {
    var s = '', col = function (k, ok, mid) { return k <= ok ? 'var(--po-treat)' : (mid != null && k <= mid ? 'var(--po-who)' : 'var(--po-watch)'); };
    s += T(118, 64, 'FeverPAIN', 'b', 'end');
    for (var k = 0; k <= 5; k++) s += '<rect x="' + (130 + k * 95) + '" y="44" width="91" height="30" rx="6" style="fill:' + col(k, 1, 3) + '"/>' + T(175.5 + k * 95, 64, String(k), 'w', 'middle');
    s += T(225, 34, 'No antibiotic', 'b', 'middle', 'fill:var(--po-treat)') + T(415, 34, 'None, or back-up', 'b', 'middle', 'fill:var(--po-who)') + T(605, 34, 'Immediate or back-up', 'b', 'middle', 'fill:var(--po-watch)');
    s += T(118, 120, 'Centor', 'b', 'end');
    for (var j = 0; j <= 4; j++) s += '<rect x="' + (130 + j * 114) + '" y="100" width="110" height="30" rx="6" style="fill:' + col(j, 2) + '"/>' + T(185 + j * 114, 120, String(j), 'w', 'middle');
    s += T(301, 150, 'No antibiotic', 'b', 'middle', 'fill:var(--po-treat)') + T(586, 150, 'Immediate or back-up', 'b', 'middle', 'fill:var(--po-watch)');
    return svg(720, 162, s, 'FeverPAIN and Centor score bands with the NICE action for each');
  };

  /* 🩻 CT: the same head, plain and with dye */
  F.ct = function () {
    var s = '', head = function (cx, cy) { return '<circle cx="' + cx + '" cy="' + cy + '" r="92" style="fill:#14171b"/><circle cx="' + cx + '" cy="' + cy + '" r="78" style="fill:#62666b;stroke:#ececec;stroke-width:9"/>' +
      '<ellipse cx="' + (cx - 13) + '" cy="' + (cy - 4) + '" rx="7" ry="22" transform="rotate(-12 ' + (cx - 13) + ' ' + (cy - 4) + ')" style="fill:#25292e"/><ellipse cx="' + (cx + 13) + '" cy="' + (cy - 4) + '" rx="7" ry="22" transform="rotate(12 ' + (cx + 13) + ' ' + (cy - 4) + ')" style="fill:#25292e"/>'; };
    s += head(180, 112) + '<path d="M113 58 Q138 112 113 166 Q100 112 113 58 Z" style="fill:#fafafa"/>' + dot(214, 142, 12, '#f4f4f4');
    s += L(116, 70, 66, 44, 'stroke:var(--po-test);stroke-width:1.5') + T(8, 40, 'fresh blood', 'b', 'start', 'fill:var(--po-test)') + L(222, 150, 300, 186, 'stroke:var(--po-test);stroke-width:1.5') + T(304, 190, 'a bleed', 'b', 'start', 'fill:var(--po-test)');
    s += head(540, 112) + '<circle cx="568" cy="92" r="17" style="fill:#3a3e43;stroke:#f5f5f5;stroke-width:4"/><path d="M522 160 L540 150 L558 160 L556 176 L524 176 Z" style="fill:none;stroke:#f5f5f5;stroke-width:2.6"/>' + L(540, 150, 540, 120, 'stroke:#f5f5f5;stroke-width:2');
    s += L(584, 82, 650, 46, 'stroke:var(--po-who);stroke-width:1.5') + T(654, 44, 'bright rim', 'b', 'start', 'fill:var(--po-who)') + L(522, 170, 444, 196, 'stroke:var(--po-who);stroke-width:1.5') + T(440, 200, 'vessels', 'b', 'end', 'fill:var(--po-who)');
    s += lab(180, 226, 'Without contrast', 'fresh blood, bone and stones are bright on their own', 'middle', 'var(--po-test)');
    s += lab(540, 226, 'With contrast', 'vessels and the rim of an abscess or tumour light up', 'middle', 'var(--po-who)');
    return svg(720, 252, s, 'CT head without contrast showing fresh blood, and with contrast showing a ring-enhancing lesion and vessels');
  };

  /* ⚡ the fork: stable or not */
  F.fork = function () {
    var s = '';
    s += '<rect x="230" y="10" width="260" height="40" rx="20" style="fill:var(--surface);stroke:var(--ink);stroke-width:2"/>' + T(360, 35, 'Is the patient stable?', 'b', 'middle');
    s += L(300, 50, 190, 92, 'stroke:var(--po-watch);stroke-width:3') + L(420, 50, 530, 92, 'stroke:var(--po-treat);stroke-width:3');
    s += T(232, 76, 'No', 'b', 'end', 'fill:var(--po-watch)') + T(488, 76, 'Yes', 'b', 'start', 'fill:var(--po-treat)');
    s += '<rect x="24" y="94" width="330" height="86" rx="12" style="fill:none;stroke:var(--po-watch);stroke-width:2"/><rect x="366" y="94" width="330" height="86" rx="12" style="fill:none;stroke:var(--po-treat);stroke-width:2"/>';
    s += lab(40, 118, 'The first move, now', 'shock, decompress, fluids, adrenaline, calcium', 'start', 'var(--po-watch)') + T(40, 160, 'Name the disease once the physiology is safe', 'm');
    s += lab(382, 118, 'Name it, prove it, then the cure', 'history, examination, the gold test', 'start', 'var(--po-treat)') + T(382, 160, 'Treat the cause and plan ahead', 'm');
    return svg(720, 190, s, 'Is the patient stable? No: the first move. Yes: diagnose and treat the cause.');
  };

  /* 💊 the WHO ladder */
  F.ladder = function () {
    var s = '', st = [[30, 150, '1 · Non-opioid', 'paracetamol, an NSAID if safe', '.12'], [250, 108, '2 · Weak opioid', 'codeine or tramadol, plus step 1', '.2'], [470, 66, '3 · Strong opioid', 'morphine or oxycodone, plus step 1', '.3']];
    st.forEach(function (k) { s += '<rect x="' + k[0] + '" y="' + k[1] + '" width="220" height="' + (196 - k[1]) + '" rx="6" style="fill:rgba(22,134,90,' + k[4] + ');stroke:var(--po-treat);stroke-width:1.5"/>' + lab(k[0] + 12, k[1] + 22, k[2], k[3]); });
    s += L(30, 30, 690, 30, 'stroke:var(--po-cause);stroke-width:2;stroke-dasharray:6 4') + T(360, 22, 'Adjuvants at any step: amitriptyline, duloxetine, gabapentinoids, steroids', 'm', 'middle');
    s += T(30, 214, 'Pain rising →', 'b') + T(690, 214, 'A laxative with every opioid', 'b', 'end', 'fill:var(--po-watch)');
    return svg(720, 222, s, 'The WHO analgesic ladder with adjuvants at every step');
  };

  /* ⚡ nerves: where each one breaks */
  F.nerves = function () {
    var s = '', cx = 360, y0 = 12, k = 1.6, X = function (v) { return cx + v * k; }, Y = function (v) { return y0 + v * k; };
    s += (window.DG && DG.H ? DG.H.body(cx, y0, 200 * k) : '');
    var Lf = [['Axillary', 'Shoulder dislocation → numb badge', -31, 46], ['Long thoracic', 'Axillary surgery → winged scapula', -20, 60], ['Radial', 'Humerus shaft → wrist drop', -38, 72], ['Sciatic', 'Back of the hip → foot drop', -12, 114], ['Common peroneal', 'Fibula neck → foot drop', -24, 150]];
    var Rt = [['Brachial plexus', 'Erb\'s: waiter\'s tip · Klumpke: claw', 12, 34], ['Ulnar', 'Elbow → claw ring and little', 28, 79], ['Median', 'Carpal tunnel → numb thumb side', 39, 100], ['Femoral', 'Groin → weak knee straightening', 12, 110], ['Superior gluteal', 'Hip surgery → Trendelenburg gait', 22, 122], ['Tibial', 'Behind the knee → can\'t tiptoe', 15, 156]];
    Lf.forEach(function (n, i) { var ly = 40 + i * 64; s += L(X(n[2]), Y(n[3]), 252, ly - 4, 'stroke:var(--muted);stroke-width:1') + lab(246, ly, n[0], n[1], 'end'); s += num(X(n[2]), Y(n[3]), i + 1); });
    Rt.forEach(function (n, i) { var ly = 30 + i * 56; s += L(X(n[2]), Y(n[3]), 466, ly - 4, 'stroke:var(--muted);stroke-width:1') + lab(472, ly, n[0], n[1]); s += num(X(n[2]), Y(n[3]), Lf.length + i + 1, 'var(--po-test)'); });
    return svg(720, 350, s, 'Body map of nerve injuries and what each causes');
  };

  /* 🧩 the colon, coloured by operation */
  F.colon = function () {
    var s = '', seg = function (d, c, dash) { return '<path d="' + d + '" style="fill:none;stroke:' + c + ';stroke-width:24;stroke-linecap:round;stroke-linejoin:round' + (dash ? ';opacity:.55' : '') + '"/>'; };
    s += seg('M210 262 L210 110 Q210 80 240 80 L320 80', 'var(--po-test)') + seg('M320 80 L420 80', 'var(--po-test)', 1) + seg('M420 80 L480 80 Q510 80 510 110 L510 220', 'var(--po-who)');
    s += seg('M510 220 C510 276 430 214 392 250', 'var(--po-cause)') + seg('M392 250 Q362 262 360 286', 'var(--po-treat)') + seg('M360 286 L360 314', 'var(--po-watch)');
    s += '<path d="M206 276 q-6 14 4 22" style="fill:none;stroke:var(--muted);stroke-width:6;stroke-linecap:round"/>';
    s += lab(190, 160, 'Right hemicolectomy', 'caecum, ascending, hepatic flexure', 'end', 'var(--po-test)');
    s += lab(370, 44, 'Extended right hemicolectomy', 'the transverse colon', 'middle', 'var(--po-test)');
    s += lab(612, 150, 'Left hemicolectomy', 'splenic flexure, descending', 'middle', 'var(--po-who)');
    s += lab(612, 238, 'Sigmoid colectomy', 'the sigmoid loop', 'middle', 'var(--po-cause)');
    s += lab(338, 262, 'Anterior resection', 'upper and mid rectum', 'end', 'var(--po-treat)');
    s += lab(376, 318, 'APR', 'low rectum and anus → permanent colostomy', 'start', 'var(--po-watch)');
    s += '<circle cx="40" cy="300" r="13" style="fill:var(--surface);stroke:var(--po-watch);stroke-width:3"/><circle cx="40" cy="300" r="5" style="fill:var(--po-watch)"/>' + lab(60, 296, 'Ileostomy', 'right, spouted, liquid', 'start');
    s += '<circle cx="572" cy="300" r="13" style="fill:var(--po-watch);opacity:.85"/>' + lab(592, 296, 'Colostomy', 'left, flush, formed', 'start');
    return svg(720, 342, s, 'The colon coloured by the operation that removes each part, with stomas');
  };

  /* 🧷 antibodies pinned to their organs */
  F.abmap = function () {
    var s = '', cx = 360, y0 = 12, k = 1.7, X = function (v) { return cx + v * k; }, Y = function (v) { return y0 + v * k; };
    s += (window.DG && DG.H ? DG.H.body(cx, y0, 200 * k) : '');
    var Lf = [['Anti-NMDA receptor', 'Autoimmune encephalitis', 0, 6], ['Anti-TPO · TSH receptor', 'Hashimoto\'s · Graves\'', 0, 32], ['Anti-GBM · c-ANCA · p-ANCA', 'Lungs and kidneys: Goodpasture\'s, GPA, MPA', -12, 56], ['Anti-mitochondrial · smooth muscle', 'PBC · autoimmune hepatitis', -12, 76], ['Anti-tTG · endomysial', 'Coeliac disease', -4, 90], ['Anti-Jo-1', 'Myositis with lung fibrosis', -15, 132]];
    var Rt = [['Anti-AChR · anti-VGCC', 'Myasthenia · Lambert-Eaton', 5, 13], ['Anti-Ro · anti-La', 'Sjögren\'s; heart block in the baby', 3, 23], ['ANA · anti-dsDNA · anti-Smith', 'SLE: dsDNA tracks the kidneys', 10, 50], ['Anti-intrinsic factor', 'Pernicious anaemia', 10, 70], ['Anti-GAD', 'Type 1 diabetes', 6, 80], ['Anti-centromere · Scl-70', 'Limited · diffuse systemic sclerosis', 32, 86], ['Anti-CCP · rheumatoid factor', 'Rheumatoid arthritis', 40, 101], ['Anticardiolipin', 'Antiphospholipid: clots, miscarriage', 6, 110]];
    Lf.forEach(function (n, i) { var ly = 28 + i * 58; s += L(X(n[2]), Y(n[3]), 262, ly - 4, 'stroke:var(--muted);stroke-width:1') + lab(256, ly, n[0], n[1], 'end'); s += dot(X(n[2]), Y(n[3]), 5, 'var(--po-cause)'); });
    Rt.forEach(function (n, i) { var ly = 22 + i * 44; s += L(X(n[2]), Y(n[3]), 458, ly - 4, 'stroke:var(--muted);stroke-width:1') + lab(464, ly, n[0], n[1]); s += dot(X(n[2]), Y(n[3]), 5, 'var(--po-test)'); });
    return svg(720, 372, s, 'Body map: each autoantibody pinned to the organ it attacks');
  };

  /* 🎧 four murmurs on one time axis */
  F.murmur = function () {
    var s = '', S1 = 170, S2 = 400, S3 = 650, rows = [['Aortic stenosis', 'ejection, to the neck', 'var(--po-test)'], ['Mitral regurgitation', 'pansystolic, to the armpit', 'var(--po-who)'], ['Aortic regurgitation', 'early diastolic, sit forward', 'var(--po-cause)'], ['Mitral stenosis', 'snap, then a rumble', 'var(--po-watch)']];
    s += T(S1, 20, 'S1', 'b', 'middle') + T(S2, 20, 'S2', 'b', 'middle') + T(S3, 20, 'S1', 'b', 'middle');
    s += L(S1 + 6, 30, S2 - 6, 30, 'stroke:var(--po-test);stroke-width:2') + T((S1 + S2) / 2, 44, 'Systole', 'm', 'middle') + L(S2 + 6, 30, S3 - 6, 30, 'stroke:var(--po-cause);stroke-width:2') + T((S2 + S3) / 2, 44, 'Diastole', 'm', 'middle');
    rows.forEach(function (r, i) {
      var yb = 96 + i * 58;
      s += lab(10, yb - 18, r[0], r[1]) + L(S1 - 8, yb, S3 + 8, yb, 'stroke:var(--line);stroke-width:1.5');
      [S1, S2, S3].forEach(function (x, j) { s += L(x, yb, x, yb - (j === 1 ? 26 : 32), 'stroke:var(--ink);stroke-width:' + (i === 3 && j !== 1 ? 5 : 3)); });
      if (i === 0) s += '<path d="M' + (S1 + 14) + ' ' + yb + ' L' + ((S1 + S2) / 2 + 6) + ' ' + (yb - 34) + ' L' + (S2 - 12) + ' ' + yb + ' Z" style="fill:' + r[2] + ';opacity:.45;stroke:' + r[2] + ';stroke-width:2"/>';
      if (i === 1) s += '<rect x="' + (S1 + 8) + '" y="' + (yb - 22) + '" width="' + (S2 - S1 - 16) + '" height="22" style="fill:' + r[2] + ';opacity:.45;stroke:' + r[2] + ';stroke-width:2"/>';
      if (i === 2) s += '<path d="M' + (S2 + 8) + ' ' + (yb - 32) + ' L' + (S2 + 180) + ' ' + yb + ' L' + (S2 + 8) + ' ' + yb + ' Z" style="fill:' + r[2] + ';opacity:.45;stroke:' + r[2] + ';stroke-width:2"/>';
      if (i === 3) s += L(S2 + 32, yb, S2 + 32, yb - 24, 'stroke:' + r[2] + ';stroke-width:2.5') + '<polyline points="' + zig(S2 + 42, S2 + 190, yb, 12, 5, 6) + ' ' + zig(S2 + 194, S3 - 6, yb, 6, 20, 4) + '" style="fill:none;stroke:' + r[2] + ';stroke-width:2"/>';
    });
    return svg(720, 290, s, 'Aortic stenosis, mitral regurgitation, aortic regurgitation and mitral stenosis drawn on one heart-sound timeline');
  };
})();
