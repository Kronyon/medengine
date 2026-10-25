/* medengine shared visual layer: Clinical Atlas Lookup, Visual Showdowns ("the Dirty Dozen") and
   drawn schematics (ECG strips, CXR, fundus, eardrum, STEMI lead map). Zero bloat: no photos are
   bundled; the atlases open in a new tab and the schematics are drawn in code. Used by medengine-OSCE
   and medengine-STUDY. Exposes window.MEV. */
(function () {
  'use strict';
  var MEV = window.MEV = window.MEV || {};
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); };
  var rich = function (s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); };
  var enc = encodeURIComponent;

  /* ---------------- systems ---------------- */
  MEV.SYS = [
    ['cardio', '❤️ Cardio & vascular'], ['resp', '🫁 Respiratory'], ['gi', '🍽️ GI & surgical abdomen'], ['neuro', '🧠 Neuro'],
    ['endo', '🧪 Endocrine & diabetes'], ['renal', '🫘 Renal & urology'], ['msk', '🦴 MSK'], ['psych', '🧘 Psych'],
    ['derm', '🧴 Derm'], ['ent', '👂 ENT'], ['eye', '👁️ Eye'], ['breast', '🎗️ Breast & hernia'], ['haemid', '🩸 Haem, ID & other']
  ];
  var WEEK_SYS = {chest: 'cardio', sob: 'resp', cough: 'resp', giupset: 'gi', abdopr: 'gi', acuteabdo: 'gi', breast: 'breast', leg: 'cardio', dm: 'endo', haem: 'renal', joint: 'msk', neuro: 'neuro', mh: 'psych', derm: 'derm', ent: 'ent', eye: 'eye'};
  var UNIT_SYS = {6: 'cardio', 7: 'cardio', 8: 'cardio', 10: 'haemid', 44: 'cardio', 46: 'haemid', 47: 'haemid', 50: 'haemid', 51: 'renal'};
  MEV.unitSys = function (i, w) { return UNIT_SYS[i] || WEEK_SYS[w] || 'haemid'; };
  MEV.sysLabel = function (id) { for (var k = 0; k < MEV.SYS.length; k++) if (MEV.SYS[k][0] === id) return MEV.SYS[k][1]; return ''; };
  MEV.sysOptions = function (sel) { return MEV.SYS.map(function (s) { return '<option value="' + s[0] + '"' + (sel === s[0] ? ' selected' : '') + '>' + esc(s[1]) + '</option>'; }).join(''); };

  /* ---------------- atlas ---------------- */
  var G = function (q) { return 'https://www.google.com/search?q=' + enc(q); };
  var GI = function (q) { return 'https://www.google.com/search?tbm=isch&q=' + enc(q); };
  var ATLAS = {
    dermnet: {n: 'DermNet NZ', ico: '🧴', s: '25,000+ peer-reviewed clinical skin images', site: function (q) { return 'https://dermnetnz.org/search?q=' + enc(q); }, img: function (q) { return GI('site:dermnetnz.org ' + q); }},
    litfl: {n: 'LITFL · Life in the Fast Lane', ico: '❤️', s: 'ECG library, CXRs and critical-care cases (opened via Google, because LITFL\'s own search misses pages)', site: function (q) { return G('site:litfl.com ' + q); }, img: function (q) { return GI('site:litfl.com ' + q); }},
    radiopaedia: {n: 'Radiopaedia', ico: '🩻', s: 'X-ray, CT and MRI cases with the signs labelled', site: function (q) { return 'https://radiopaedia.org/search?lang=gb&q=' + enc(q) + '&scope=all'; }, img: function (q) { return GI('site:radiopaedia.org ' + q); }},
    rmc: {n: 'Radiology Masterclass', ico: '🎓', s: 'Step-by-step chest and abdominal X-ray tutorials', site: function (q) { return G('site:radiologymasterclass.co.uk ' + q); }, img: function (q) { return GI('site:radiologymasterclass.co.uk ' + q); }},
    google: {n: 'Google Images', ico: '🖼️', s: 'Any clinical photo: fundoscopy, otoscopy, rashes, signs', site: function (q) { return GI(q + ' clinical'); }, img: function (q) { return GI(q); }}
  };
  var PRI = {
    derm: [['dermnet', 'site', 'DermNet', ''], ['dermnet', 'img', 'DermNet images', ''], ['google', 'img', 'Clinical photos', ' skin clinical']],
    cardio: [['litfl', 'site', 'LITFL ECG', ' ECG'], ['litfl', 'img', 'ECG images', ' ECG'], ['radiopaedia', 'site', 'Radiopaedia', '']],
    resp: [['radiopaedia', 'site', 'Radiopaedia', ''], ['rmc', 'site', 'Radiology Masterclass', ' chest x-ray'], ['litfl', 'site', 'LITFL', '']],
    gi: [['radiopaedia', 'site', 'Radiopaedia', ''], ['rmc', 'site', 'Radiology Masterclass', ' abdominal x-ray'], ['google', 'img', 'Clinical images', '']],
    eye: [['google', 'img', 'Fundoscopy', ' fundoscopy'], ['google', 'img', 'Eye photos', ' eye clinical photo'], ['dermnet', 'site', 'DermNet', '']],
    ent: [['google', 'img', 'Otoscopy', ' otoscopy'], ['google', 'img', 'ENT photos', ' ENT clinical'], ['radiopaedia', 'site', 'Radiopaedia', '']],
    neuro: [['radiopaedia', 'site', 'Radiopaedia', ''], ['rmc', 'site', 'CT head', ' CT head'], ['google', 'img', 'Clinical signs', ' clinical sign']],
    renal: [['radiopaedia', 'site', 'Radiopaedia', ''], ['litfl', 'site', 'LITFL', ''], ['google', 'img', 'Images', '']],
    endo: [['google', 'img', 'Clinical signs', ' clinical sign'], ['litfl', 'site', 'LITFL', ''], ['radiopaedia', 'site', 'Radiopaedia', '']],
    msk: [['radiopaedia', 'site', 'Radiopaedia', ' x-ray'], ['google', 'img', 'Clinical photos', ' clinical'], ['rmc', 'site', 'Radiology Masterclass', '']],
    psych: [['litfl', 'site', 'LITFL tox', ''], ['google', 'img', 'Images', ''], ['radiopaedia', 'site', 'Radiopaedia', '']],
    breast: [['radiopaedia', 'site', 'Radiopaedia', ''], ['google', 'img', 'Clinical photos', ' clinical'], ['dermnet', 'site', 'DermNet', '']],
    haemid: [['google', 'img', 'Blood film & signs', ' blood film'], ['litfl', 'site', 'LITFL', ''], ['dermnet', 'site', 'DermNet', '']]
  };
  MEV.cleanQ = function (q) {
    var s = String(q || '').replace(/\*\*/g, '').replace(/\([^)]*\)/g, ' ').split(/\s+\/\s+|:\s+|\s+→\s+/)[0];
    return s.replace(/&/g, 'and').replace(/\s+/g, ' ').trim();
  };
  function linkHtml(key, kind, label, q, cls) {
    var a = ATLAS[key], href = a[kind](q);
    return '<a class="' + (cls || 'mev-a') + '" href="' + esc(href) + '" target="_blank" rel="noopener noreferrer" title="' + esc(a.n + (kind === 'img' ? ' · images' : '') + ': ' + q) + '">' + (kind === 'img' && key !== 'google' ? '🖼️' : a.ico) + ' ' + esc(label) + ' ↗</a>';
  }
  MEV.atlasRowHtml = function (q, sys, extra) {
    var c = MEV.cleanQ(q), pri = PRI[sys] || PRI.haemid;
    var h = '<div class="mev-row mev-atlasrow"><button type="button" class="mev-btn main" data-mev-atlas="' + esc(c) + '" data-mev-sys="' + esc(sys || '') + '">👁️ Clinical Atlas Lookup</button>';
    pri.forEach(function (p) { h += linkHtml(p[0], p[1], p[2], c + p[3]); });
    var ids = MEV.sdFor((extra || '') + ' ' + q);
    if (ids.length) h += ids.map(function (id) { var s = SDBY[id]; return '<button type="button" class="mev-sdchip" data-mev-sd="' + id + '">🥊 ' + esc(s.t) + '</button>'; }).join('');
    return h + '</div>';
  };

  /* ---------------- dialog ---------------- */
  var dlg = null;
  function dialog(html) {
    if (!dlg) {
      dlg = document.createElement('dialog');
      dlg.className = 'mev-dlg';
      dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
      dlg.addEventListener('close', function () { dlg.innerHTML = ''; });
      document.body.appendChild(dlg);
    }
    dlg.innerHTML = '<div class="mev-dlgb">' + html + '</div>';
    try { if (!dlg.open) dlg.showModal(); } catch (e) { dlg.setAttribute('open', ''); }
    return dlg;
  }
  MEV.closeDialog = function () { if (dlg) { try { dlg.close(); } catch (e) { dlg.removeAttribute('open'); } } };
  function atlasBody(q, sys) {
    var pri = PRI[sys] || PRI.haemid, h = '';
    h += '<p class="mev-h">Best for this ' + (sys ? esc(MEV.sysLabel(sys).replace(/^\S+\s/, '')) : 'topic') + '</p><div class="mev-row">' + pri.map(function (p) { return linkHtml(p[0], p[1], p[2], q + p[3]); }).join('') + '</div>';
    h += '<p class="mev-h">All atlases</p><div class="mev-atl">' + Object.keys(ATLAS).map(function (k) {
      var a = ATLAS[k];
      return '<div class="mev-at"><b>' + a.ico + ' ' + esc(a.n) + '</b><span class="s">' + esc(a.s) + '</span><div class="r">' + linkHtml(k, 'site', k === 'google' ? 'Clinical photos' : 'Search', q) + (k === 'google' ? '' : linkHtml(k, 'img', 'Images', q)) + '</div></div>';
    }).join('') + '</div>';
    var ids = MEV.sdFor(q);
    if (ids.length) h += '<p class="mev-h">🥊 Visual showdowns for this</p><div class="mev-row">' + ids.map(function (id) { return '<button type="button" class="mev-sdchip" data-mev-sd="' + id + '">🥊 ' + esc(SDBY[id].t) + '</button>'; }).join('') + '</div>';
    return h;
  }
  MEV.openAtlas = function (q, sys) {
    var c = MEV.cleanQ(q);
    dialog('<div class="mev-dlgh"><h2>👁️ Clinical Atlas Lookup</h2><button type="button" class="mev-x" data-mev-close aria-label="Close">✕</button></div>'
      + '<input class="mev-q" id="mevQ" type="search" value="' + esc(c) + '" aria-label="What to look up" placeholder="e.g. hyperkalaemia ECG">'
      + '<div id="mevAt" data-sys="' + esc(sys || '') + '">' + atlasBody(c, sys) + '</div>'
      + '<div class="mev-row"><button type="button" class="mev-btn" data-mev-lib>🥊 All visual showdowns</button></div>'
      + '<p class="mev-note">Opens the atlas in a new tab. Nothing is downloaded into the app, so it stays light and works offline for everything else.</p>');
    var inp = document.getElementById('mevQ');
    if (inp) {
      inp.addEventListener('input', function () { var box = document.getElementById('mevAt'); if (box) box.innerHTML = atlasBody(inp.value.trim() || c, box.dataset.sys); });
      if (!c) setTimeout(function () { try { inp.focus(); } catch (e) {} }, 30);
    }
  };

  /* ---------------- schematics ---------------- */
  var gauss = function (t, c, s) { var x = (t - c) / s; return Math.exp(-0.5 * x * x); };
  function ecgStrip(o) {
    // o: {ms, beats:[{p, q}], pAmp, wide, t:'n'|'tall'|'flat', u, std, ann:[[ms, text, cls, y]]}
    var W = o.ms * 0.1, H = 100, base = 62, k = 40, h = '';
    h += '<svg class="mev-ecg" viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + esc(o.label || 'ECG strip') + '"><rect class="bg" width="' + W + '" height="' + H + '"/>';
    var g = '';
    for (var x = 0; x <= W; x += 4) g += '<line class="' + (x % 20 ? 'g1' : 'g2') + '" x1="' + x + '" y1="0" x2="' + x + '" y2="' + H + '"/>';
    for (var y = 2; y <= H; y += 4) g += '<line class="' + ((y - 2) % 20 ? 'g1' : 'g2') + '" x1="0" y1="' + y + '" x2="' + W + '" y2="' + y + '"/>';
    h += g;
    var pts = [];
    function val(t) {
      var v = 0;
      o.beats.forEach(function (b) {
        if (b.p != null) v += (o.pAmp == null ? 0.15 : o.pAmp) * gauss(t, b.p + 40, 16);
        if (b.q != null) {
          var q = b.q;
          // wpw: slow slurred delta ramp, then the spike; lbbb (V6): sharp onset, broad notched "M"
          if (o.qrs === 'wpw') v += 0.4 * gauss(t, q + 52, 24) + 0.9 * gauss(t, q + 80, 9) - 0.22 * gauss(t, q + 100, 9);
          else if (o.qrs === 'lbbb') v += 0.72 * gauss(t, q + 38, 13) + 0.78 * gauss(t, q + 92, 16);
          else if (o.wide) v += -0.05 * gauss(t, q + 10, 10) + 0.85 * gauss(t, q + 50, 20) - 0.35 * gauss(t, q + 105, 22);
          else v += -0.08 * gauss(t, q + 8, 6) + 1.1 * gauss(t, q + 30, 8) - 0.28 * gauss(t, q + 52, 8);
          var tc = q + (o.wide || o.qrs ? 330 : 300);
          if (o.t === 'tall') v += 0.95 * gauss(t, q + (o.wide ? 300 : 270), 20);
          else if (o.t === 'flat') v += 0.05 * gauss(t, tc, 45);
          else if (o.t === 'inv') v -= 0.26 * gauss(t, tc, 44);
          else v += 0.28 * gauss(t, tc, 42);
          if (o.u) v += 0.17 * gauss(t, q + 480, 32);
          if (o.std) { var a = 1 / (1 + Math.exp(-(t - q - 85) / 8)), z = 1 / (1 + Math.exp((t - q - 250) / 14)); v += o.std * a * z; }
        }
      });
      return v;
    }
    // capital delta: shade the slurred ramp under the curve (wpw only)
    if (o.qrs === 'wpw') o.beats.forEach(function (b) {
      if (b.q == null) return;
      var dp = [];
      for (var t2 = b.q + 4; t2 <= b.q + 62; t2 += 4) dp.push((t2 * 0.1).toFixed(1) + ',' + (base - val(t2) * k).toFixed(1));
      h += '<polygon class="dl" points="' + ((b.q + 4) * 0.1).toFixed(1) + ',' + base + ' ' + dp.join(' ') + ' ' + ((b.q + 62) * 0.1).toFixed(1) + ',' + base + '"/>';
    });
    for (var t = 0; t <= o.ms; t += 4) pts.push((t * 0.1).toFixed(1) + ',' + (base - val(t) * k).toFixed(1));
    h += '<polyline class="tr" points="' + pts.join(' ') + '"/>';
    (o.ann || []).forEach(function (a) { h += '<text x="' + (a[0] * 0.1).toFixed(1) + '" y="' + (a[3] || 12) + '" text-anchor="middle" class="' + (a[2] || '') + '">' + esc(a[1]) + '</text>'; });
    return h + '</svg>';
  }
  function beatsFrom(pTimes, prs) {
    return pTimes.map(function (p, i) { var pr = prs[i % prs.length]; return {p: p, q: pr == null ? null : p + pr}; });
  }
  var ECG = {
    norm: function () { var ps = [150, 950, 1750, 2550, 3350, 4150, 4950]; return ecgStrip({ms: 5600, beats: beatsFrom(ps, [160]), label: 'Normal sinus rhythm'}); },
    hb1: function () { var ps = [150, 950, 1750, 2550, 3350, 4150, 4950]; return ecgStrip({ms: 5600, beats: beatsFrom(ps, [270]), ann: ps.map(function (p) { return [p + 155, '0.27s', '', 12]; }), label: 'First-degree block: long fixed PR, every P conducted'}); },
    mob1: function () {
      var ps = [120, 940, 1760, 2580, 3400, 4220, 5040], prs = [160, 250, 330, null];
      var ann = []; ps.forEach(function (p, i) { var pr = prs[i % 4]; if (pr == null) { ann.push([p + 40, '✕ no QRS', 'drop', 94]); } else ann.push([p + pr / 2 + 20, (pr / 1000).toFixed(2) + 's', '', 12]); });
      return ecgStrip({ms: 5700, beats: beatsFrom(ps, prs), ann: ann, label: 'Mobitz I: PR lengthens then a dropped beat'});
    },
    mob2: function () {
      var ps = [120, 940, 1760, 2580, 3400, 4220, 5040], prs = [180, 180, null];
      var ann = []; ps.forEach(function (p, i) { var pr = prs[i % 3]; if (pr == null) ann.push([p + 40, '✕ no QRS', 'drop', 94]); else ann.push([p + 110, '0.18s', '', 12]); });
      return ecgStrip({ms: 5700, beats: beatsFrom(ps, prs), ann: ann, label: 'Mobitz II: fixed PR then a dropped beat'});
    },
    chb: function () {
      var ps = [], qs = [500, 2150, 3800, 5450], beats = [], ann = [];
      for (var p = 150; p < 5900; p += 680) { ps.push(p); beats.push({p: p, q: null}); ann.push([p + 40, 'P', 'pm', 12]); }
      qs.forEach(function (q) { beats.push({p: null, q: q}); });
      return ecgStrip({ms: 6000, beats: beats, wide: true, ann: ann, label: 'Complete heart block: P waves and QRS independent'});
    },
    hiK: function () { var ps = [150, 950, 1750, 2550, 3350, 4150, 4950]; return ecgStrip({ms: 5600, beats: beatsFrom(ps, [210]), pAmp: 0.04, wide: true, t: 'tall', label: 'Hyperkalaemia: tented T, flat P, wide QRS'}); },
    loK: function () { var ps = [150, 950, 1750, 2550, 3350, 4150, 4950]; return ecgStrip({ms: 5600, beats: beatsFrom(ps, [190]), t: 'flat', u: true, std: -0.06, label: 'Hypokalaemia: flat T, U waves'}); },
    wpw: function () {
      var ps = [150, 1050, 1950, 2850], ann = [];
      ps.forEach(function (p, i) { if (i === 1) ann.push([p + 50, 'PR 0.10 s', 'pm', 94]); if (i === 1 || i === 3) ann.push([p + 128, 'Δ', 'dlt', 40]); });
      return ecgStrip({ms: 3600, beats: beatsFrom(ps, [100]), qrs: 'wpw', t: 'inv', ann: ann, label: 'WPW: short PR, delta wave slurring the start of a wide QRS, discordant T'});
    },
    lbbb: function () {
      var ps = [150, 1050, 1950, 2850], ann = [];
      ps.forEach(function (p, i) { if (i === 1) ann.push([p + 80, 'PR 0.16 s', 'pm', 94]); if (i === 1 || i === 3) ann.push([p + 225, 'M', 'mm', 14]); });
      return ecgStrip({ms: 3600, beats: beatsFrom(ps, [160]), qrs: 'lbbb', t: 'inv', ann: ann, label: 'LBBB in V6: normal PR, broad notched M-shaped QRS, discordant T'});
    }
  };

  // seeded random for stable lesion layouts
  function rnd(seed) { var a = seed >>> 0; return function () { a = (a + 0x6D2B79F5) | 0; var t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
  var uid = 0;
  function fundus(kind) {
    var id = 'mf' + (++uid), r = rnd(kind.length * 97 + 11), h = '';
    var pale = kind === 'crao', dark = kind === 'crvo';
    var c1 = pale ? '#f2d3c4' : dark ? '#cf6236' : '#e8844b', c2 = pale ? '#d7a08e' : dark ? '#7e2616' : '#a4351e';
    h += '<svg viewBox="0 0 200 200" role="img" aria-label="Fundus schematic: ' + kind + '"><defs><radialGradient id="' + id + 'g" cx="55%" cy="50%" r="60%"><stop offset="0" stop-color="' + c1 + '"/><stop offset="1" stop-color="' + c2 + '"/></radialGradient><clipPath id="' + id + 'c"><circle cx="100" cy="100" r="92"/></clipPath><filter id="' + id + 'b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.6"/></filter><filter id="' + id + 'd" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter></defs>';
    h += '<circle cx="100" cy="100" r="96" fill="#1b0e0b"/><g clip-path="url(#' + id + 'c)"><rect width="200" height="200" fill="url(#' + id + 'g)"/>';
    // macula
    h += '<circle cx="132" cy="100" r="15" fill="#7a2312" opacity="' + (pale ? 0 : 0.35) + '"/>';
    // vessels: [path, isVein]
    var V = [
      ['M66 92 C 92 58, 140 52, 196 66', 1], ['M66 108 C 92 142, 140 148, 196 134', 1], ['M58 92 C 48 68, 36 50, 18 36', 1], ['M58 108 C 48 132, 36 150, 18 164', 1],
      ['M68 95 C 96 66, 142 62, 196 76', 0], ['M68 105 C 96 134, 142 138, 196 124', 0], ['M60 95 C 52 72, 42 56, 24 44', 0], ['M60 105 C 52 128, 42 144, 24 156', 0]
    ];
    V.forEach(function (v) {
      var vein = v[1], w = vein ? (dark ? 4.2 : 3) : (pale ? 1 : 1.9), col = vein ? (dark ? '#5a0d08' : '#7d1a12') : (pale ? '#d9705d' : '#c8402b');
      if (dark && vein) h += '<path d="' + v[0] + '" fill="none" stroke="' + col + '" stroke-width="' + w + '" stroke-linecap="round" stroke-dasharray="14 2"/>';
      else h += '<path d="' + v[0] + '" fill="none" stroke="' + col + '" stroke-width="' + w + '" stroke-linecap="round"' + (pale && !vein ? ' stroke-dasharray="6 3"' : '') + '/>';
    });
    // disc
    if (dark) h += '<circle cx="62" cy="100" r="17" fill="#f2c27a" filter="url(#' + id + 'd)"/>';
    h += '<circle cx="62" cy="100" r="13" fill="' + (pale ? '#f6ecd6' : '#f6d68c') + '"' + (dark ? ' filter="url(#' + id + 'b)"' : '') + '/><circle cx="64" cy="100" r="5.5" fill="' + (pale ? '#fbf5e8' : '#fbe9b9') + '"/>';
    function dots(n, col, rmin, rmax, area) {
      var s = '';
      for (var i = 0; i < n; i++) { var a = area(), rr = rmin + r() * (rmax - rmin); s += '<circle cx="' + a[0].toFixed(1) + '" cy="' + a[1].toFixed(1) + '" r="' + rr.toFixed(1) + '" fill="' + col + '"/>'; }
      return s;
    }
    var anywhere = function () { var ang = r() * Math.PI * 2, d = 22 + r() * 62; return [100 + Math.cos(ang) * d, 100 + Math.sin(ang) * d]; };
    if (kind === 'dr' || kind === 'pdr' || kind === 'mac') {
      h += dots(kind === 'dr' ? 26 : kind === 'pdr' ? 7 : 12, '#6e0b08', 1.2, 2.6, kind === 'pdr' ? function () { var a = r() * 6.283, d = 30 + r() * 30; return [62 + Math.cos(a) * d, 100 + Math.sin(a) * d * 0.7]; } : anywhere);
      h += dots(kind === 'dr' ? 14 : 6, '#ffe07a', 0.9, 1.6, function () { var a = r() * 6.28, d = 30 + r() * 25; return [128 + Math.cos(a) * d, 100 + Math.sin(a) * d * 0.8]; });
    }
    if (kind === 'mac') { for (var i = 0; i < 26; i++) { var a = i / 26 * 6.283, d = 17 + r() * 4; h += '<circle cx="' + (132 + Math.cos(a) * d).toFixed(1) + '" cy="' + (100 + Math.sin(a) * d).toFixed(1) + '" r="' + (1.2 + r()).toFixed(1) + '" fill="#ffe27a"/>'; } }
    if (kind === 'dr' || kind === 'pdr' || dark) h += dots(dark ? 5 : 3, '#fff7ea', 3.5, 5, anywhere).replace(/\/>/g, ' filter="url(#' + id + 'b)" opacity=".9"/>');
    if (kind === 'pdr') {
      for (var j = 0; j < 9; j++) { var a2 = j / 9 * 6.283; h += '<path d="M' + (62 + Math.cos(a2) * 12).toFixed(1) + ' ' + (100 + Math.sin(a2) * 12).toFixed(1) + ' q ' + (Math.cos(a2 + 1) * 9).toFixed(1) + ' ' + (Math.sin(a2 + 1) * 9).toFixed(1) + ' ' + (Math.cos(a2) * 14).toFixed(1) + ' ' + (Math.sin(a2) * 14).toFixed(1) + '" fill="none" stroke="#e8312a" stroke-width=".9"/>'; }
      h += '<path d="M128 156 l 26 -3 q 2 12 -12 14 q -12 1 -14 -11 z" fill="#5a0606" opacity=".85"/>';
    }
    if (dark) {
      for (var f = 0; f < 70; f++) { var p = anywhere(), ang = Math.atan2(p[1] - 100, p[0] - 62) * 180 / Math.PI; h += '<ellipse cx="' + p[0].toFixed(1) + '" cy="' + p[1].toFixed(1) + '" rx="' + (3.5 + r() * 4).toFixed(1) + '" ry="' + (1 + r() * 0.8).toFixed(1) + '" fill="#6a0805" opacity=".9" transform="rotate(' + ang.toFixed(0) + ' ' + p[0].toFixed(1) + ' ' + p[1].toFixed(1) + ')"/>'; }
    }
    if (pale) h += '<circle cx="132" cy="100" r="10" fill="#fbe6dc"/><circle cx="132" cy="100" r="5" fill="#c4141c"/>';
    return h + '</g></svg>';
  }
  function drum(kind) {
    var id = 'md' + (++uid), h = '';
    var c = {normal: ['#ddd6cb', '#a8a197'], aom: ['#f07a5c', '#b22a1e'], ome: ['#d2ad6e', '#8c6e40'], chol: ['#d9d2c6', '#a29b90']}[kind];
    h += '<svg viewBox="0 0 160 160" role="img" aria-label="Eardrum schematic: ' + kind + '"><defs><radialGradient id="' + id + '" cx="48%" cy="52%" r="60%"><stop offset="0" stop-color="' + c[0] + '"/><stop offset="1" stop-color="' + c[1] + '"/></radialGradient></defs>';
    h += '<circle cx="80" cy="80" r="76" fill="#4a2c20"/><circle cx="80" cy="80" r="62" fill="url(#' + id + ')"/>';
    if (kind === 'aom') h += '<ellipse cx="74" cy="74" rx="26" ry="20" fill="#ffd2b8" opacity=".35"/><circle cx="96" cy="98" r="9" fill="#f3d36b" opacity=".55"/>';
    var mal = kind === 'ome' ? ['M76 38 L 98 70', 1] : kind === 'aom' ? ['M78 36 L 84 82', 0.2] : ['M78 36 L 84 82', 1];
    h += '<path d="' + mal[0] + '" stroke="#f6eedc" stroke-width="' + (kind === 'ome' ? 4.5 : 3.5) + '" stroke-linecap="round" opacity="' + mal[1] + '"/><circle cx="77" cy="35" r="3.2" fill="#fbf6ea" opacity="' + mal[1] + '"/>';
    if (kind === 'normal' || kind === 'chol') h += '<path d="M86 88 L 112 126 L 100 132 Z" fill="#fff" opacity=".85"/>';
    if (kind === 'ome') {
      h += '<path d="M24 96 Q 80 90 136 96" stroke="#6d4f22" stroke-width="2" fill="none"/>';
      [[50, 84, 5], [64, 78, 3.5], [104, 82, 4.5], [116, 76, 3], [86, 74, 2.5]].forEach(function (b) { h += '<circle cx="' + b[0] + '" cy="' + b[1] + '" r="' + b[2] + '" fill="none" stroke="#fff6dd" stroke-width="1.2" opacity=".85"/>'; });
    }
    if (kind === 'chol') {
      h += '<ellipse cx="78" cy="24" rx="17" ry="8" fill="#3b2418"/>';
      [[70, 23, 5], [79, 21, 6], [88, 24, 4.5], [75, 28, 3.5], [84, 28, 3.5]].forEach(function (b) { h += '<circle cx="' + b[0] + '" cy="' + b[1] + '" r="' + b[2] + '" fill="#f7f3e6"/>'; });
      h += '<path d="M62 22 q 16 -9 32 0" stroke="#9a6a3a" stroke-width="2" fill="none"/>';
    }
    return h + '</svg>';
  }
  function cxr(kind) {
    var h = '<svg viewBox="0 0 200 180" role="img" aria-label="Chest X-ray schematic: ' + kind + '">';
    h += '<rect width="200" height="180" fill="#060606"/>';
    h += '<path d="M18 30 Q 40 14 70 18 L 130 18 Q 160 14 182 30 L 194 178 L 6 178 Z" fill="#474747"/>';
    var R = 'M42 40 C 30 72, 28 112, 34 136 Q 60 110 88 128 L 90 46 C 76 30, 56 30, 42 40 Z';
    var L = 'M158 40 C 170 72, 172 112, 166 139 Q 140 112 112 129 L 110 46 C 124 30, 144 30, 158 40 Z';
    h += '<path d="' + R + '" fill="#131313"/><path d="' + L + '" fill="#131313"/>';
    if (kind === 'ptx') h += '<path d="M42 40 C 30 72, 28 112, 34 136 L 52 128 C 46 106, 46 72, 56 44 Z" fill="#020202"/>';
    h += '<rect x="90" y="18" width="20" height="62" fill="#c9c9c9" opacity=".9"/><rect x="95" y="18" width="10" height="160" fill="#9a9a9a" opacity=".35"/>';
    h += '<path d="M92 72 C 84 90, 84 112, 92 126 C 106 135, 136 136, 152 122 C 157 106, 146 88, 122 78 C 114 74, 102 72, 92 72 Z" fill="#d8d8d8" opacity=".9"/><circle cx="115" cy="62" r="7" fill="#d0d0d0" opacity=".9"/>';
    if (kind === 'perf') h += '<path d="M34 136 Q 60 110 88 128 L 92 178 L 30 178 Z" fill="#5d5d5d"/>';
    var ribs = '';
    [44, 57, 70, 83, 96, 109].forEach(function (y) { ribs += '<path d="M34 ' + y + ' Q 60 ' + (y - 9) + ' 90 ' + (y + 4) + '" stroke="#fff" stroke-opacity=".16" fill="none"/><path d="M166 ' + y + ' Q 140 ' + (y - 9) + ' 110 ' + (y + 4) + '" stroke="#fff" stroke-opacity=".16" fill="none"/>'; });
    h += ribs + '<path d="M40 30 L 90 38 M160 30 L 110 38" stroke="#bdbdbd" stroke-width="3"/>';
    var mk = function (x0, side) { var s = side < 0 ? -1 : 1, m = ''; [[0, -12, 26], [0, 4, 30], [0, 18, 22]].forEach(function (b) { m += '<path d="M' + x0 + ' ' + (82 + b[1]) + ' l ' + (s * b[2]) + ' ' + (b[1] / 2) + ' l ' + (s * 10) + ' ' + (b[1] / 3 - 4) + '" stroke="#fff" stroke-opacity=".28" fill="none"/>'; }); return m; };
    h += (kind === 'ptx' ? '<path d="M88 70 l -22 -5 M88 86 l -20 4 M88 100 l -16 10" stroke="#fff" stroke-opacity=".28" fill="none"/>' : mk(88, -1)) + mk(112, 1);
    if (kind === 'eff') {
      var cid = 'mx' + (++uid);
      h += '<clipPath id="' + cid + '"><path d="' + L + '"/></clipPath><g clip-path="url(#' + cid + ')"><path d="M104 112 Q 142 110 178 70 L 182 180 L 104 180 Z" fill="#c6c6c6" opacity=".96"/></g><path d="M122 110 Q 148 105 170 80" stroke="#ededed" fill="none"/>';
      h += '<path d="M182 70 L 162 90" stroke="#f0b04a" stroke-width="1.5"/><text x="150" y="64" fill="#f0b04a" font-size="10" font-weight="700">meniscus</text>';
    }
    if (kind === 'ptx') {
      h += '<path d="M56 44 C 46 72, 46 106, 52 128" stroke="#f2f2f2" stroke-width="1.4" fill="none"/>';
      h += '<path d="M10 60 L 46 78" stroke="#f0b04a" stroke-width="1.5"/><text x="4" y="54" fill="#f0b04a" font-size="10" font-weight="700">edge · no markings</text>';
    }
    if (kind === 'perf') {
      h += '<path d="M34 136 Q 60 110 88 128" stroke="#e6e6e6" stroke-width="1.6" fill="none"/>';
      h += '<path d="M36 139 Q 60 116 87 131 Q 60 125 36 139 Z" fill="#020202"/>';
      h += '<path d="M18 160 L 50 132" stroke="#f0b04a" stroke-width="1.5"/><text x="4" y="172" fill="#f0b04a" font-size="10" font-weight="700">free air (erect)</text>';
    }
    return h + '</svg>';
  }
  var LEADS = [['I', 'lat'], ['aVR', 'avr'], ['V1', 'sep'], ['V4', 'ant'], ['II', 'inf'], ['aVL', 'lat'], ['V2', 'sep'], ['V5', 'lat'], ['III', 'inf'], ['aVF', 'inf'], ['V3', 'ant'], ['V6', 'lat']];
  var TERR = {inf: ['Inferior', '#d97706'], lat: ['Lateral', '#2563eb'], sep: ['Septal', '#7c3aed'], ant: ['Anterior', '#dc2626'], avr: ['aVR', '#6b7280']};
  function leadMap() {
    var h = '<svg viewBox="0 0 240 110" role="img" aria-label="12-lead territory map">';
    LEADS.forEach(function (l, i) {
      var x = (i % 4) * 60 + 4, y = Math.floor(i / 4) * 36 + 4, c = TERR[l[1]][1];
      h += '<g class="mev-lead" data-terr="' + l[1] + (l[0] === 'V1' || l[0] === 'V2' || l[0] === 'V3' ? ' post' : '') + '"><rect x="' + x + '" y="' + y + '" width="52" height="30" rx="6" fill="' + c + '" fill-opacity=".22"/><text x="' + (x + 26) + '" y="' + (y + 20) + '" text-anchor="middle">' + l[0] + '</text></g>';
    });
    return h + '</svg>';
  }
  MEV.ECG = ECG; MEV.fundus = fundus; MEV.drum = drum; MEV.cxr = cxr;

  /* ---------------- the Dirty Dozen (+1) ---------------- */
  var GRP = {derm: '🧴 Derm', eye: '👁️ Eye', ent: '👂 ENT', ecg: '❤️ ECG', cxr: '🩻 CXR'};
  var SD = [
    {id: 'bcc-scc', g: 'derm', t: 'BCC vs SCC', kw: /basal cell|squamous cell|\bBCC\b|\bSCC\b|skin lesion|skin cancer|actinic|keratoacanth/i, s: [
      {n: 'Basal cell carcinoma', film: 'A pearly, shiny bump on a sun-exposed face (side of the nose, inner canthus) creeping outwards over years; tiny red vessels run across its surface; the middle caves in, bleeds, crusts, then bleeds again.', look: ['**Pearly rolled edge**', '**Arborising telangiectasia** across the surface', 'Central ulcer or crust ("rodent ulcer"); slow, months to years', 'Locally invasive; almost never spreads'], act: 'Routine referral (NICE NG12); suspected cancer pathway only if site or size means delay matters → excision or Mohs', q: 'basal cell carcinoma'},
      {n: 'Squamous cell carcinoma', film: 'A fast-growing (weeks to months), tender, crusty, horn-like lump on sun-wrecked skin (scalp, back of the hand, lower lip) in an older man or a transplant patient on immunosuppressants.', look: ['**Keratotic (hard, horny) crust** ± ulcer', 'Indurated and tender; grows over **weeks to months**', 'Arises from actinic keratosis or Bowen\'s disease', 'Can metastasise (lip, ear, immunosuppressed)'], act: '**Suspected cancer pathway (2WW)** → excision with margins', q: 'cutaneous squamous cell carcinoma'}],
      split: '**Pearly rolled edge + telangiectasia = BCC**; **keratin crust + fast + tender = SCC**.',
      trap: '**Keratoacanthoma**: a volcano with a central keratin plug that erupts in weeks. Treat it as SCC and excise. And the referral split: BCC routine, SCC 2WW.'},
    {id: 'mel-sk', g: 'derm', t: 'Melanoma vs seborrhoeic keratosis', kw: /melanoma|seborrh|naev|\bmoles?\b|pigment/i, s: [
      {n: 'Melanoma', film: 'The "ugly duckling" mole: it is changing (bigger, darker in patches, a notched edge), maybe itching or bleeding, and it looks like none of the person\'s other moles.', look: ['**ABCDE**: Asymmetry, Border, Colour, Diameter >6 mm, **Evolution**', 'Weighted 7-point checklist: change in **size, shape or colour** = 2 points each; ≥7 mm, inflamed, oozing, altered sensation = 1 each; **≥3 → refer**', 'Amelanotic ones are pink: a changing pink lump still counts'], act: '**Suspected cancer pathway (2WW)** → full-thickness excision biopsy (never shave); Breslow thickness drives prognosis', q: 'melanoma'},
      {n: 'Seborrhoeic keratosis', film: 'An older person\'s back dotted with brown, warty, greasy plaques that look "stuck on", like blobs of candle wax you could flick off with a fingernail.', look: ['**"Stuck-on"**, well demarcated, waxy or warty surface', '**Horn cysts** (tiny white or black pits)', 'Many of them; benign; increase with age'], act: 'Reassure; no treatment needed (cryotherapy only if symptomatic)', q: 'seborrhoeic keratosis'}],
      split: '**Stuck-on + waxy + horn cysts = seborrhoeic keratosis**; **change (evolution) + irregular colour or border = melanoma**.',
      trap: 'A sudden **crop of many seborrhoeic keratoses = Leser–Trélat sign**: look for an internal (GI) cancer. If a "SebK" is changing or you are unsure, treat it as melanoma and refer.'},
    {id: 'pso-ecz', g: 'derm', t: 'Plaque psoriasis vs discoid eczema', video: 'Video Q11', kw: /psoria|eczema|discoid|tinea|fungal/i, s: [
      {n: 'Plaque psoriasis', film: 'Thick salmon-pink plaques topped with silvery scale on the elbows, knees, scalp and behind the ears; pick the scale and pinpoint bleeding appears; the nails are pitted.', look: ['**Extensor** surfaces, scalp, natal cleft, umbilicus', 'Sharply demarcated with **silvery scale**', '**Auspitz sign**; Koebner (plaques at sites of injury)', '**Nail pitting**, onycholysis; ask about the joints'], act: 'Emollient + **potent topical steroid + vitamin D analogue** (calcipotriol) → refer if extensive (phototherapy, methotrexate, biologics)', q: 'plaque psoriasis'},
      {n: 'Discoid (nummular) eczema', film: 'Coin-shaped, intensely itchy plaques on the shins and forearms of an adult with dry skin; they start as tiny weeping blisters, then crust over.', look: ['**Coin-shaped** and very **itchy**', '**Wet, weeping, crusted**; vesicles at the edge early', 'Less sharply defined; no silvery scale', 'Limbs, especially the lower legs; often infected'], act: 'Emollients + **potent topical steroid**; flucloxacillin if infected (weeping with pus)', q: 'discoid eczema'}],
      split: '**Silvery scale + extensor + nail pits = psoriasis**; **coin + itch + weeping crust = discoid eczema**.',
      trap: 'A ring with **central clearing and a scaly advancing edge = tinea corporis**: send scrapings and use an antifungal; a steroid makes it spread (**tinea incognito**).'},
    {id: 'herp-imp', g: 'derm', t: 'Eczema herpeticum vs impetigo', kw: /impetigo|herpeticum|eczema|cold sore|herpes simplex/i, s: [
      {n: 'Eczema herpeticum (HSV)', film: 'A child with flared atopic eczema suddenly becomes feverish and miserable; the eczema is studded with clusters of identical, small, punched-out round erosions that spread over hours.', look: ['**Monomorphic punched-out erosions** (all the same size and stage)', 'On eczematous skin; painful more than itchy', '**Fever, unwell**; can involve the eye'], act: '**Emergency: same-day referral + aciclovir** (IV if unwell); near the eye → same-day ophthalmology', q: 'eczema herpeticum'},
      {n: 'Impetigo (S. aureus or Strep)', film: 'A well child at nursery with golden, honey-coloured crusts around the nose and mouth that spread to their friends.', look: ['**Golden "honey" crust** on a red base', 'Around the nose and mouth; contagious', 'The child is **well**; bullous form = S. aureus'], act: 'Localised: **hydrogen peroxide 1% cream** (fusidic acid if unsuitable); widespread, bullous or unwell: **oral flucloxacillin** (NICE NG153); off school until crusted over or 48 h of antibiotics', q: 'impetigo'}],
      split: '**Punched-out monomorphic erosions + fever on eczema = herpeticum (aciclovir, emergency)**; **golden honey crust + well child = impetigo**.',
      trap: 'Both can sit on eczema. **Honey crust → flucloxacillin; punched-out holes → aciclovir.** Never treat herpeticum with a steroid alone.'},
    {id: 'dr-crvo', g: 'eye', t: 'Diabetic retinopathy vs CRVO', video: 'Video Q97', fig: ['fundus', [['dr', 'Diabetic retinopathy', 'dots, blots, exudates, cotton wool'], ['crvo', 'CRVO', '"stormy sunset": flames everywhere']]], kw: /retinopath|diabetic complication|retinal vein|vision loss|fundoscop|sudden vision/i, s: [
      {n: 'Diabetic retinopathy', film: 'Years of diabetes, both eyes, often no symptoms; the retina is sprinkled with tiny red dots and blots, yellow waxy flecks and the odd fluffy white patch.', look: ['**Dot-blot haemorrhages** + microaneurysms', '**Hard exudates** (yellow, waxy)', '**Cotton wool spots** = ischaemia (pre-proliferative)', '**Bilateral**, gradual'], act: 'Annual retinal screening; refer by grade; tight glucose, BP and lipids', q: 'diabetic retinopathy fundus'},
      {n: 'Central retinal vein occlusion', film: 'An older hypertensive wakes with painless blurred vision in ONE eye; the fundus looks like a stormy sunset, with blood smeared everywhere.', look: ['**Flame haemorrhages in all four quadrants** ("stormy sunset")', '**Dilated, tortuous veins**; swollen disc', 'Cotton wool spots', '**Unilateral and sudden**'], act: 'Urgent ophthalmology; treat risk factors (BP, glaucoma, hyperviscosity); anti-VEGF for macular oedema; watch for neovascular glaucoma', q: 'central retinal vein occlusion fundus'}],
      split: '**Bilateral dots and blots + exudates over years = diabetic retinopathy**; **one eye, sudden, flames everywhere = CRVO**.',
      trap: '**BRVO** = flames in one sector only, along one vein. **Hypertensive retinopathy** = both eyes, flames + AV nipping + silver wiring (± papilloedema at grade 4).'},
    {id: 'crvo-crao', g: 'eye', t: 'CRVO vs CRAO', fig: ['fundus', [['crvo', 'CRVO', 'blood can\'t get out'], ['crao', 'CRAO', 'no blood gets in']]], kw: /retinal (artery|vein)|sudden vision|cherry|amaurosis|vision loss/i, s: [
      {n: 'CRVO (vein)', film: 'Blood cannot leave the eye, so it backs up and bursts: haemorrhages everywhere, veins fat and twisting, the disc swollen.', look: ['**"Stormy sunset"** flame haemorrhages', 'Dilated tortuous veins', 'Painless; vision loss varies'], act: 'Urgent ophthalmology; control BP, check for glaucoma and hyperviscosity', q: 'central retinal vein occlusion'},
      {n: 'CRAO (artery)', film: 'The lights go out in one eye within seconds, painlessly; no blood gets in, so the retina turns milky pale and only the thin fovea keeps its red colour.', look: ['**Pale, milky retina + cherry-red spot** at the fovea', 'Thin arteries ("box-carring")', '**RAPD**; profound, sudden loss'], act: '**Emergency (an eye stroke)**: same-day stroke or eye pathway; over 50 → ask GCA symptoms, ESR/CRP, **steroids now** if suspected', q: 'central retinal artery occlusion cherry red spot'}],
      split: '**Artery blocked = no blood in = pale + cherry-red spot**; **vein blocked = blood can\'t get out = haemorrhages everywhere**.',
      trap: 'In CRAO over 50 always hunt **giant cell arteritis** (jaw claudication, scalp tenderness) and don\'t wait for a biopsy to start steroids. Then look for the embolic source: carotids, AF.'},
    {id: 'mac-pdr', g: 'eye', t: 'Diabetic maculopathy vs proliferative retinopathy', video: 'Video Q97', fig: ['fundus', [['mac', 'Maculopathy', 'exudate ring hugging the macula'], ['pdr', 'Proliferative', 'new vessels at the disc + bleed']]], kw: /retinopath|diabetic complication|macula/i, s: [
      {n: 'Diabetic maculopathy', film: 'Reading gets blurry because the centre of vision is waterlogged: a ring of yellow exudates hugs the macula.', look: ['**Hard exudates at or around the macula** (circinate ring)', 'Macular oedema → **central vision** loss', 'Can happen at **any** retinopathy stage'], act: 'Refer to ophthalmology (M1); **intravitreal anti-VEGF**', q: 'diabetic maculopathy exudates'},
      {n: 'Proliferative retinopathy', film: 'The starved retina sprouts fragile new vessels from the disc; one day they bleed into the vitreous and the patient sees a shower of floaters, then a red-out.', look: ['**New vessels at the disc (NVD) or elsewhere (NVE)**', 'Pre-retinal or **vitreous haemorrhage**', 'Preceded by cotton wool spots, venous beading, IRMA'], act: '**Urgent** ophthalmology (R3): **pan-retinal photocoagulation** ± anti-VEGF', q: 'proliferative diabetic retinopathy neovascularisation'}],
      split: '**Exudates hugging the macula = maculopathy (central blur)**; **new vessels = proliferative (bleeds, detachment)**.',
      trap: 'Pre-proliferative (R2) = cotton wool spots, venous beading, IRMA: the ischaemia comes **before** the new vessels. Sudden floaters in a diabetic = vitreous haemorrhage until proven otherwise.'},
    {id: 'aom-ome', g: 'ent', t: 'Acute otitis media vs glue ear', fig: ['drum', [['normal', 'Normal drum', 'pearly grey, light reflex'], ['aom', 'Acute otitis media', 'red, bulging, no reflex'], ['ome', 'Glue ear (OME)', 'dull, retracted, fluid line']]], kw: /otitis media|glue ear|earache|otalgia|ear pain/i, s: [
      {n: 'Acute otitis media', film: 'A toddler up all night crying and tugging an ear, feverish after a cold; the drum is angry red and bulging like a tomato; if it bursts, pus pours out and the pain eases.', look: ['**Red, bulging drum**; light reflex lost', '**Pain + fever** after a cold', 'Perforation → discharge, then relief'], act: 'Analgesia; most settle within 3 days; **amoxicillin 5–7 days** if under 2 with both ears, discharge, systemically unwell, or not improving (NICE NG91)', q: 'acute otitis media otoscopy'},
      {n: 'Glue ear (otitis media with effusion)', film: 'A well child whose teacher says they never listen and who turns the TV right up; no pain, no fever; behind a dull, pulled-in drum sits a line of fluid with bubbles.', look: ['**Dull, retracted drum**', '**Fluid level or bubbles**, amber-grey', '**Hearing loss** (speech, behaviour); no pain'], act: 'Active observation for 3 months + audiology; persistent bilateral with hearing loss → **grommets** (or hearing aids)', q: 'otitis media with effusion otoscopy'}],
      split: '**Red + bulging + pain + fever = AOM**; **dull + retracted + fluid level + deaf, no pain = glue ear**.',
      trap: '**One-sided glue ear in an adult** → look at the postnasal space and exclude **nasopharyngeal carcinoma** (especially Southern Chinese or SE Asian origin).'},
    {id: 'ome-chol', g: 'ent', t: 'Glue ear vs cholesteatoma', video: 'Video Q40', fig: ['drum', [['ome', 'Glue ear', 'fluid behind the whole drum'], ['chol', 'Cholesteatoma', 'white crust up in the attic']]], kw: /cholesteatoma|otitis media|glue ear|ear discharge|hearing loss|otorrh/i, s: [
      {n: 'Glue ear (OME)', film: 'A quiet, painless, dry ear: fluid behind the whole drum, hearing muffled, no smell.', look: ['Fluid level or bubbles behind the **whole** drum', 'No discharge, no smell', 'Usually children; usually resolves'], act: 'Watch for 3 months, audiology, grommets if it persists', q: 'glue ear otoscopy'},
      {n: 'Cholesteatoma', film: 'An ear that keeps leaking foul-smelling discharge despite drops, with creeping hearing loss; up in the attic (top of the drum) sits a pocket of white crusty keratin that is eating bone.', look: ['**Attic (pars flaccida) crust, white keratin debris** or a retraction pocket', '**Foul, persistent discharge** + conductive hearing loss', 'Erodes: facial palsy, vertigo, intracranial infection'], act: '**ENT referral**: CT temporal bone → surgical removal (mastoidectomy)', q: 'cholesteatoma attic otoscopy'}],
      split: '**Fluid behind the whole drum, dry, no smell = glue ear**; **attic crust + foul discharge that won\'t settle = cholesteatoma**.',
      trap: 'An "attic crust", or a smelly ear failing repeated drops, is **cholesteatoma until proven otherwise**: refer it, don\'t keep prescribing drops.'},
    {id: 'blocks', g: 'ecg', t: 'Mobitz I vs Mobitz II vs complete heart block', fig: ['ecg', [['mob1', 'Mobitz I (Wenckebach)', 'longer, longer, longer… drop'], ['mob2', 'Mobitz II', 'fixed PR, then a drop'], ['chb', 'Complete heart block', 'P waves march through, ignored']]], kw: /arrhythm|heart block|bradycard|mobitz|wenckebach|syncope|palpitation|pacemaker|AV block|collapse/i, s: [
      {n: 'Mobitz I (Wenckebach)', film: 'The gap between P and QRS stretches beat by beat (longer, longer, longer… drop), then resets and starts again.', look: ['**PR progressively lengthens → a P with no QRS**', 'Grouped beating; AV node level', 'Athletes, inferior MI, AV-nodal drugs; usually benign'], act: 'Usually observe; stop AV-nodal blockers', q: 'Mobitz type 1 Wenckebach ECG'},
      {n: 'Mobitz II', film: 'The PR interval stays rock steady, then out of nowhere a P wave just isn\'t followed by a QRS.', look: ['**Constant PR + sudden dropped QRS**', 'Below the AV node (His–Purkinje); often broad QRS', 'High risk of complete block or asystole'], act: '**Pacing** (risk of asystole) → cardiology', q: 'Mobitz type 2 ECG'},
      {n: 'Complete (third-degree) heart block', film: 'Atria and ventricles have divorced: P waves march regularly straight through a slow, wide escape rhythm that ignores them.', look: ['**AV dissociation**: P–P regular, R–R regular, no link', 'Slow (often 30–40) with a broad escape', 'Cannon a waves; Stokes–Adams attacks'], act: 'Unstable → **atropine 500 mcg** (repeat to 3 mg) → **transcutaneous pacing**, or isoprenaline/adrenaline → permanent pacemaker', q: 'complete heart block ECG'}],
      split: '**PR lengthening then a drop = Mobitz I**; **fixed PR then a drop = Mobitz II**; **P and QRS independent = complete block**.',
      trap: '**2:1 block** could be either type: find a longer strip. Resus Council "risk of asystole" (pace even if stable): Mobitz II, complete block with broad QRS, recent asystole, ventricular pause >3 s.'},
    {id: 'wpw-lbbb', g: 'ecg', t: 'WPW vs LBBB: two wide QRS complexes', fig: ['ecg', [['wpw', 'WPW (pre-excitation)', 'short PR + Δ ramp at the START'], ['lbbb', 'LBBB (V6)', 'normal PR + notched M at the END']]], kw: /\bWPW\b|wolff|pre-?excit|delta wave|accessory pathway|bundle of kent|\bLBBB\b|bundle branch|broad complex|wide QRS|arrhythm|palpitation/i, s: [
      {n: 'WPW (Wolff–Parkinson–White)', film: 'The impulse sneaks down an extra wire (Bundle of Kent) and starts squeezing the ventricle early, muscle to muscle: the PR is short and the QRS begins with a slow, slurred ramp before the normal spike arrives.', look: ['**Short PR (<120 ms, <3 small squares)**', '**Delta (Δ) wave**: slurred upstroke at the START of a wide QRS', 'Discordant ST-T; negative Δ waves can mimic Q waves'], act: 'Pre-excited AF: **never AV-node blockers**; unstable → **synchronised DC cardioversion**; cure = **catheter ablation**', q: 'WPW delta wave ECG'},
      {n: 'LBBB (left bundle branch block)', film: 'The left bundle is cut, so the left ventricle is activated late and slowly from the right: the PR is normal, the QRS starts sharply but drags on, notching into an M in V6 and a W in V1.', look: ['**Normal PR**, no slurred ramp at the onset', '**Broad notched M in V6 / W in V1** (WiLLiaM)', 'Discordant ST-T; new LBBB with ischaemic pain = STEMI pathway'], act: 'Look for the cause (IHD, hypertension, aortic stenosis); **new LBBB + ischaemic pain → STEMI pathway**', q: 'LBBB ECG WiLLiaM'}],
      feat: ['**Where the QRS widens:** WPW widens at the **START** (short PR + slurred Δ ramp from early muscle-to-muscle pre-excitation via the Bundle of Kent); LBBB widens at the **END** (normal PR, sharp onset, notched **M in V6 / W in V1**: WiLLiaM).', '**The pseudo-infarction trap:** negative Δ waves in WPW mimic pathological Q waves (a false "old MI"). Always check the PR interval before you call an old infarct.', '**The lethal drug contraindication:** WPW + AF = fast, irregularly irregular, wide QRS complexes that keep changing shape. **NEVER** give AV-node blockers (adenosine, verapamil, diltiazem, β-blockers, digoxin): blocking the node funnels every impulse down the accessory pathway → **VF**. Unstable → synchronised DC cardioversion; stable → specialist drug therapy (flecainide in the UK; procainamide is the US choice); definitive cure = **catheter ablation**.'],
      split: '**Short PR + slurred start = WPW**; **normal PR + notched M at the end = LBBB**.',
      trap: '**Irregular broad-complex tachycardia in a young patient = pre-excited AF until proven otherwise**: adenosine or verapamil can tip it into VF.'},
    {id: 'k', g: 'ecg', t: 'Hyperkalaemia vs hypokalaemia', fig: ['ecg', [['norm', 'Normal', 'for comparison'], ['hiK', 'High K⁺', 'tented T, flat P, wide QRS'], ['loK', 'Low K⁺', 'flat T, U wave after it']]], kw: /potassium|hyperkal|hypokal|electrolyte|kidney injury|\bAKI\b|renal failure|ketoacidosis|\bDKA\b|IV fluids|rhabdo/i, s: [
      {n: 'Hyperkalaemia', film: 'As potassium climbs, the T waves stand up like tents, the P waves fade away, the QRS widens and finally melts into a sine wave before VF.', look: ['**Tall, peaked (tented) T waves**', 'Flat or absent P, long PR', '**Broad QRS → sine wave → VF or asystole**'], act: 'ECG changes or K⁺ ≥6.5: **IV calcium** (gluconate 10% 30 mL, or chloride 10% 10 mL) to protect the heart → **insulin–glucose** ± salbutamol to shift K⁺ in → remove it (stop ACEi/ARB/spironolactone, binders, dialysis)', q: 'hyperkalaemia ECG'},
      {n: 'Hypokalaemia', film: 'As potassium drains away, the T waves sag flat and a little U wave pops up after each one, stretching the QT(U).', look: ['**Flat or small T waves**', '**Prominent U waves**', 'ST depression, long QT(U), long PR'], act: 'Replace K⁺ (oral if mild; IV KCl if <2.5 or symptomatic, at a protocol rate) and **check magnesium**', q: 'hypokalaemia ECG U waves'}],
      split: '**Tented T (+ wide QRS) = high K⁺**; **flat T + U wave = low K⁺**.',
      trap: 'Calcium doesn\'t lower potassium; it only stabilises the heart, so you still need insulin–glucose. A high K⁺ with a normal ECG: repeat urgently (haemolysed sample?), but don\'t wait if K⁺ is ≥6.5.'},
    {id: 'cxr', g: 'cxr', t: 'Pleural effusion vs pneumothorax vs perforation', video: 'Video Q57', fig: ['cxr', [['eff', 'Pleural effusion', 'white base, meniscus'], ['ptx', 'Pneumothorax', 'edge, black beyond'], ['perf', 'Perforation', 'air under the diaphragm']]], kw: /pleural effusion|pneumothorax|perforat|peritonitis|pneumoperit|chest x-ray|\bCXR\b|acute abdo/i, s: [
      {n: 'Pleural effusion', film: 'Breathless, and the base is stony dull to percussion; on the film the bottom of one lung is whited out, with a curved upper edge climbing up the side wall.', look: ['**Homogeneous white base + meniscus** rising laterally', '**Blunted costophrenic angle**', 'Large ones push the mediastinum **away**'], act: 'Ultrasound-guided **diagnostic tap** (protein and LDH for Light\'s, pH, MC&S, cytology); treat the cause', q: 'pleural effusion chest x-ray meniscus'},
      {n: 'Pneumothorax', film: 'A tall, thin young man feels a sudden stab of chest pain and breathlessness; on the film a fine white line hangs inside the chest wall, and beyond it there is only black, with no lung markings at all.', look: ['**Visible visceral pleural edge**', '**No lung markings beyond it**', 'Tension: trachea and mediastinum shift away + shock (treat before any film)'], act: '**Tension → needle decompression**, then a chest drain; otherwise BTS 2023: conservative, aspiration or drain by symptoms', q: 'pneumothorax chest x-ray'},
      {n: 'Perforated viscus', film: 'Sudden severe abdominal pain, then a rigid, board-like abdomen in someone on NSAIDs; sitting up for the erect film, a black crescent of air appears under the diaphragm.', look: ['**Free air under the diaphragm** on an **erect** CXR', 'Rigler\'s sign (both sides of the bowel wall) on AXR', 'Peritonism: rigid, guarding, lying still'], act: 'Resuscitate, NBM, IV antibiotics, IV PPI, **CT** + **urgent surgical review**', q: 'pneumoperitoneum erect chest x-ray'}],
      split: '**White + meniscus = fluid**; **black with no markings beyond a line = air in the pleura**; **black crescent under the diaphragm = air in the abdomen**.',
      trap: '**Chilaiditi sign**: bowel (with haustra) between the liver and diaphragm mimics free air. Sit the patient up for 10 minutes before an erect film, or a small amount of air is missed.'},
    {id: 'stemi', g: 'ecg', t: 'Which wall? STEMI territories', fig: ['leads'], kw: /coronary|STEMI|\bMI\b|infarct|angina|chest pain|ischaemic heart/i, s: [],
      table: [['Inferior', 'II, III, aVF', 'RCA (most) or circumflex', 'Bradycardia and heart block; **RV infarct** (V4R): hypotension, avoid nitrates, give fluids'], ['Anterior / septal', 'V1–V4', 'LAD', 'Large LV damage: heart failure, VT/VF'], ['Lateral', 'I, aVL, V5–V6', 'Circumflex (or diagonal)', 'Often with anterior or inferior'], ['Posterior', 'ST↓ + tall R in V1–V3', 'RCA or circumflex', 'Do V7–V9 (ST↑) → treat as STEMI'], ['Left main', 'ST↑ aVR + widespread ST↓', 'Left main or 3-vessel', 'High risk: urgent angiography']],
      split: 'The leads tell you the wall and the wall tells you the artery: **II/III/aVF = inferior = RCA**; **V1–V4 = anterior = LAD**; **I/aVL/V5–6 = lateral = circumflex**.',
      trap: '**ST depression in V1–V3 isn\'t always NSTEMI**: think posterior STEMI → PCI. **Inferior STEMI + low BP** → RV infarct: avoid GTN, give fluids.'}
  ];
  var SDBY = {}; SD.forEach(function (s) { SDBY[s.id] = s; });
  MEV.SD = SD;
  MEV.sdFor = function (text) { var t = String(text || ''); return SD.filter(function (s) { return s.kw.test(t); }).map(function (s) { return s.id; }).slice(0, 3); };

  function figHtml(sd) {
    if (!sd.fig) return '';
    var kind = sd.fig[0];
    if (kind === 'leads') {
      return '<div class="mev-terr">' + Object.keys(TERR).filter(function (k) { return k !== 'avr'; }).map(function (k) { return '<button type="button" style="--c:' + TERR[k][1] + '" data-mev-terr="' + k + '">' + TERR[k][0] + '</button>'; }).join('') + '<button type="button" style="--c:#0f766e" data-mev-terr="post">Posterior (mirror V1–V3)</button></div><div class="mev-fig wide"><figure>' + leadMap() + '<figcaption>Tap a territory to light up its leads</figcaption></figure></div>';
    }
    var fn = kind === 'fundus' ? fundus : kind === 'drum' ? drum : kind === 'cxr' ? cxr : null;
    var h = '<div class="mev-fig' + (kind === 'ecg' ? ' wide' : '') + '">';
    sd.fig[1].forEach(function (f) { h += '<figure>' + (kind === 'ecg' ? ECG[f[0]]() : fn(f[0])) + '<figcaption>' + esc(f[1]) + '<span>' + esc(f[2]) + '</span></figcaption></figure>'; });
    return h + '</div><p class="mev-schem">Drawn schematic, not a photo: tap the atlas links for real images.</p>';
  }
  function sideHtml(x) {
    return '<section class="mev-side"><h4>' + esc(x.n) + '</h4><p class="mev-film">🎬 ' + rich(x.film) + '</p><ul class="mev-look">' + x.look.map(function (l) { return '<li>' + rich(l) + '</li>'; }).join('') + '</ul><p class="mev-act">→ ' + rich(x.act) + '</p><div class="mev-row">' + sideLinks(x.q) + '</div></section>';
  }
  function pickAtlas(q) { return /otoscopy|fundus|retin|macul|cholesteatoma|otitis|glue|occlusion/i.test(q) ? 'google' : /ecg|mobitz|block/i.test(q) ? 'litfl' : /x-ray|pneumo|effusion/i.test(q) ? 'radiopaedia' : 'dermnet'; }
  function sideLinks(q) {
    var k = pickAtlas(q);
    if (k === 'google') return linkHtml('google', 'img', 'Real images', q);
    return linkHtml(k, 'img', ATLAS[k].n.split(' ')[0] + ' images', q) + linkHtml(k, 'site', ATLAS[k].n.split(' ')[0], q);
  }
  MEV.sdCardHtml = function (sd) {
    var h = '<article class="mev-sd" id="SD-' + sd.id + '" data-sdid="' + sd.id + '"><div class="mev-sdh"><span class="mev-tag">' + GRP[sd.g] + '</span><h3>🥊 ' + esc(sd.t) + '</h3>' + (sd.video ? '<span class="mev-tag">📹 ' + esc(sd.video) + '</span>' : '') + (sd.s.length > 1 ? '<button type="button" class="mev-btn" data-mev-quiz="' + sd.id + '">🎯 Quiz me</button>' : '') + '</div><div class="mev-sdbody">';
    h += figHtml(sd);
    if (sd.table) h += '<table class="mev-tbl"><tr><th>Wall</th><th>Leads</th><th>Artery</th><th>Watch for</th></tr>' + sd.table.map(function (r) { return '<tr><td><b>' + esc(r[0]) + '</b></td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td><td>' + rich(r[3]) + '</td></tr>'; }).join('') + '</table>';
    if (sd.s.length) h += '<div class="mev-vs">' + sd.s.map(sideHtml).join('') + '</div>';
    if (sd.feat) h += '<div class="mev-split"><b>🎬 Change one feature of the film:</b><ol class="mev-feat">' + sd.feat.map(function (f) { return '<li>' + rich(f) + '</li>'; }).join('') + '</ol></div>';
    h += '<div class="mev-split">✂️ <b>The one feature that splits them:</b> ' + rich(sd.split) + '</div><div class="mev-trap">⚠️ <b>Trap:</b> ' + rich(sd.trap) + '</div>';
    return h + '</div></article>';
  };
  MEV.openSd = function (id) {
    var sd = SDBY[id]; if (!sd) return;
    dialog('<div class="mev-dlgh"><h2>🥊 Visual showdown</h2><button type="button" class="mev-x" data-mev-close aria-label="Close">✕</button></div>' + MEV.sdCardHtml(sd).replace('id="SD-', 'id="SDD-') + '<div class="mev-row"><button type="button" class="mev-btn" data-mev-lib="' + id + '">All visual showdowns</button><button type="button" class="mev-btn" data-mev-atlas="' + esc(sd.s.length ? sd.s[0].q : sd.t) + '" data-mev-sys="">👁️ Clinical Atlas Lookup</button></div>');
  };
  MEV.libraryHtml = function () {
    var h = '<div class="mev-filters" role="group" aria-label="Filter showdowns"><button type="button" class="on" data-mev-flt="">All ' + SD.length + '</button>' + Object.keys(GRP).map(function (g) { return '<button type="button" data-mev-flt="' + g + '">' + GRP[g] + '</button>'; }).join('') + '<button type="button" data-mev-rq>🎲 Random quiz</button></div>';
    return h + '<div class="mev-sds" id="mevLib">' + SD.map(MEV.sdCardHtml).join('') + '</div>';
  };

  /* quiz inside a card: show one side's mental film, name hidden */
  function quiz(card, sd) {
    var k = Math.floor(Math.random() * sd.s.length), x = sd.s[k];
    var names = sd.s.map(function (s, i) { return [i, s.n]; }).sort(function () { return Math.random() - 0.5; });
    var body = card.querySelector('.mev-sdbody');
    if (!card._saved) card._saved = body.innerHTML;
    body.innerHTML = '<div class="mev-quiz"><p class="mev-film">🎬 ' + rich(x.film) + '</p><p class="mev-h">Which one is this?</p><div class="opts">' + names.map(function (n, j) { return '<button type="button" class="mev-pick" data-mev-pick="' + n[0] + '" data-mev-ans="' + k + '"><b>' + (j + 1) + '</b> ' + esc(n[1]) + '</button>'; }).join('') + '</div><div class="mev-qa"></div><div class="mev-row"><button type="button" class="mev-btn" data-mev-quiz="' + sd.id + '">↺ Another</button><button type="button" class="mev-btn" data-mev-back>Back to the card</button></div></div>';
  }

  /* ---------------- events ---------------- */
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('[data-mev-atlas],[data-mev-sd],[data-mev-lib],[data-mev-close],[data-mev-quiz],[data-mev-pick],[data-mev-back],[data-mev-terr],[data-mev-flt],[data-mev-rq]');
    if (!b) return;
    var d = b.dataset;
    if (d.mevAtlas != null) { e.preventDefault(); return MEV.openAtlas(d.mevAtlas, d.mevSys); }
    if (d.mevSd) { e.preventDefault(); return MEV.openSd(d.mevSd); }
    if (d.mevLib != null) { e.preventDefault(); MEV.closeDialog(); if (MEV.onLibrary) MEV.onLibrary(d.mevLib || ''); return; }
    if (d.mevClose != null) return MEV.closeDialog();
    var card = b.closest('.mev-sd');
    if (d.mevQuiz) { var sd = SDBY[d.mevQuiz]; if (card && sd) quiz(card, sd); return; }
    if (d.mevPick != null) {
      var ok = d.mevPick === d.mevAns, box = card.querySelector('.mev-qa'), s2 = SDBY[card.dataset.sdid];
      card.querySelectorAll('.mev-pick').forEach(function (p) { p.disabled = true; if (p.dataset.mevPick === d.mevAns) p.classList.add('right'); else if (p === b) p.classList.add('wrong'); });
      var x = s2.s[+d.mevAns];
      if (box) box.innerHTML = '<div class="' + (ok ? 'mev-split' : 'mev-trap') + '">' + (ok ? '✅ Yes: ' : '❌ No, it\'s ') + '<b>' + esc(x.n) + '</b>. ' + rich(s2.split) + '</div>';
      if (MEV.onQuiz) try { MEV.onQuiz(ok); } catch (er) {}
      return;
    }
    if (d.mevBack != null) { if (card && card._saved) { card.querySelector('.mev-sdbody').innerHTML = card._saved; card._saved = null; } return; }
    if (d.mevTerr) {
      var on = !b.classList.contains('on');
      card.querySelectorAll('[data-mev-terr]').forEach(function (x2) { x2.classList.remove('on'); });
      if (on) b.classList.add('on');
      card.querySelectorAll('.mev-lead').forEach(function (g) { g.classList.toggle('dim', on && (' ' + g.dataset.terr + ' ').indexOf(' ' + d.mevTerr + ' ') < 0); });
      return;
    }
    if (d.mevFlt != null) {
      var bar = b.parentElement; bar.querySelectorAll('[data-mev-flt]').forEach(function (x3) { x3.classList.toggle('on', x3 === b); });
      document.querySelectorAll('#mevLib .mev-sd').forEach(function (c) { var s3 = SDBY[c.dataset.sdid]; c.hidden = !!d.mevFlt && s3.g !== d.mevFlt; });
      return;
    }
    if (d.mevRq != null) {
      var pool = Array.prototype.slice.call(document.querySelectorAll('#mevLib .mev-sd')).filter(function (c) { return !c.hidden && SDBY[c.dataset.sdid].s.length > 1; });
      if (!pool.length) return;
      var c2 = pool[Math.floor(Math.random() * pool.length)];
      quiz(c2, SDBY[c2.dataset.sdid]); c2.scrollIntoView({behavior: 'smooth', block: 'start'});
      return;
    }
  });
})();
