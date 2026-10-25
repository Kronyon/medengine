/* medengine-OSCE v1.3 pictures: step-through diagrams that play like a GIF (tap ▶) or step with ◀ ▶.
   Every picture is drawn here as SVG or HTML, so it works offline and in both themes. Exposes window.DG. */
(function () {
  var DG = window.DG = {}, R = {}, uid = 0;
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]; }); };
  var rich = function (s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>'); };
  DG.def = function (id, o) { R[id] = o; };
  DG.has = function (id) { return !!R[id]; };
  DG.list = function () { return Object.keys(R); };
  DG.title = function (id) { return R[id] ? R[id].t : ''; };
  var nOf = function (o) { return o.cards ? o.cards.length : o.rows ? o.rows.length : (o.caps || [1]).length; };
  DG.n = function (id) { return R[id] ? nOf(R[id]) : 0; };

  /* ---------- drawing helpers (shared by the drawing files) ---------- */
  var H = DG.H = {
    svg: function (w, h, body, label) { return '<svg class="dg-svg" viewBox="0 0 ' + w + ' ' + h + '" role="img" aria-label="' + esc(label || '') + '">' + body + '</svg>'; },
    t: function (x, y, s, c, a, sz, extra) { return '<text x="' + x + '" y="' + y + '" class="' + (c || 'dg-tx') + '"' + (a ? ' text-anchor="' + a + '"' : '') + (sz ? ' font-size="' + sz + '"' : '') + (extra || '') + '>' + esc(s) + '</text>'; },
    ln: function (x1, y1, x2, y2, c) { return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" class="' + (c || 'dg-ln') + '"/>'; },
    c: function (x, y, r, c) { return '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" class="' + (c || 'dg-ln') + '"/>'; },
    r: function (x, y, w, h, c, rx) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" rx="' + (rx || 0) + '" class="' + (c || 'dg-ln') + '"/>'; },
    p: function (d, c) { return '<path d="' + d + '" class="' + (c === '' ? '' : (c || 'dg-ln')) + '"/>'; },
    on: function (b) { return b ? ' dg-on' : ' dg-off'; },
    arrow: function (x1, y1, x2, y2, c) {
      var a = Math.atan2(y2 - y1, x2 - x1), L = 7, s = '';
      s += '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" class="' + (c || 'dg-ar') + '"/>';
      s += '<path d="M' + x2 + ' ' + y2 + ' L' + (x2 - L * Math.cos(a - 0.45)).toFixed(1) + ' ' + (y2 - L * Math.sin(a - 0.45)).toFixed(1) + ' L' + (x2 - L * Math.cos(a + 0.45)).toFixed(1) + ' ' + (y2 - L * Math.sin(a + 0.45)).toFixed(1) + ' Z" class="' + (c || 'dg-ar') + ' dg-ah"/>';
      return s;
    },
    // a pill label with text
    tag: function (x, y, s, c, a) { var w = Math.max(22, s.length * 6.4 + 12), x0 = a === 'end' ? x - w : a === 'middle' ? x - w / 2 : x; return '<g class="dg-tag ' + (c || '') + '"><rect x="' + x0.toFixed(1) + '" y="' + (y - 11) + '" width="' + w.toFixed(1) + '" height="16" rx="8"/><text x="' + (x0 + w / 2).toFixed(1) + '" y="' + (y + 1) + '" text-anchor="middle">' + esc(s) + '</text></g>'; },
    // a simple standing body outline, front view, centred on cx, top at y0, height h
    body: function (cx, y0, h, c) {
      var k = h / 200, X = function (v) { return (cx + v * k).toFixed(1); }, Y = function (v) { return (y0 + v * k).toFixed(1); };
      return '<g class="' + (c || 'dg-body') + '"><circle cx="' + X(0) + '" cy="' + Y(16) + '" r="' + (14 * k).toFixed(1) + '"/>' +
        '<path d="M' + X(-8) + ' ' + Y(30) + ' L' + X(-8) + ' ' + Y(36) + ' Q' + X(-30) + ' ' + Y(38) + ' ' + X(-34) + ' ' + Y(50) + ' L' + X(-42) + ' ' + Y(104) + ' L' + X(-34) + ' ' + Y(106) + ' L' + X(-24) + ' ' + Y(62) + ' L' + X(-22) + ' ' + Y(108) + ' L' + X(-24) + ' ' + Y(196) + ' L' + X(-8) + ' ' + Y(196) + ' L' + X(0) + ' ' + Y(118) + ' L' + X(8) + ' ' + Y(196) + ' L' + X(24) + ' ' + Y(196) + ' L' + X(22) + ' ' + Y(108) + ' L' + X(24) + ' ' + Y(62) + ' L' + X(34) + ' ' + Y(106) + ' L' + X(42) + ' ' + Y(104) + ' L' + X(34) + ' ' + Y(50) + ' Q' + X(30) + ' ' + Y(38) + ' ' + X(8) + ' ' + Y(36) + ' L' + X(8) + ' ' + Y(30) + ' Z"/></g>';
    },
    torso: function (x, y, w, h, c) {
      var X = function (v) { return (x + v * w / 100).toFixed(1); }, Y = function (v) { return (y + v * h / 100).toFixed(1); };
      return '<path class="' + (c || 'dg-body') + '" d="M' + X(30) + ' ' + Y(0) + ' Q' + X(50) + ' ' + Y(-4) + ' ' + X(70) + ' ' + Y(0) + ' L' + X(92) + ' ' + Y(10) + ' Q' + X(100) + ' ' + Y(16) + ' ' + X(98) + ' ' + Y(30) + ' L' + X(90) + ' ' + Y(100) + ' L' + X(10) + ' ' + Y(100) + ' L' + X(2) + ' ' + Y(30) + ' Q' + X(0) + ' ' + Y(16) + ' ' + X(8) + ' ' + Y(10) + ' Z"/>';
    },
    uid: function () { return 'dg' + (++uid); },
    esc: esc, rich: rich
  };

  /* ---------- rendering ---------- */
  function stageHtml(o, i) {
    if (o.cards) {
      return '<div class="dg-cards">' + o.cards.map(function (c, k) { return '<div class="dg-card' + (k === i ? ' on' : k < i ? ' done' : '') + '"><span class="ic">' + esc(c[0]) + '</span><b>' + rich(c[1]) + '</b>' + (k === i && c[2] ? '<span class="sm">' + rich(c[2]) + '</span>' : '') + '</div>'; }).join('') + '</div>';
    }
    if (o.rows) {
      var hd = o.head ? '<tr>' + o.head.map(function (x) { return '<th>' + rich(x) + '</th>'; }).join('') + '</tr>' : '';
      return '<div class="dg-tw"><table class="dg-tab">' + hd + o.rows.map(function (r, k) { return '<tr class="' + (k === i ? 'on' : o.keep && k < i ? 'done' : '') + '">' + r.map(function (x, j) { return (j === 0 ? '<th>' : '<td>') + rich(x) + (j === 0 ? '</th>' : '</td>'); }).join('') + '</tr>'; }).join('') + '</table></div>';
    }
    try { return o.draw(i); } catch (e) { return '<p class="hint">Picture unavailable.</p>'; }
  }
  function capOf(o, i) {
    if (o.cards) return o.caps ? o.caps[i] : '';
    if (o.rows) return o.caps ? o.caps[i] : '';
    return (o.caps || [])[i] || '';
  }
  DG.html = function (id) {
    var o = R[id]; if (!o) return '';
    var n = nOf(o);
    return '<figure class="dg" data-dg="' + esc(id) + '" data-i="0"><div class="dg-head"><b>' + rich(o.t) + '</b>' + (n > 1 ? '<span class="dg-n">1 / ' + n + '</span><button type="button" class="dg-b" data-dgp aria-label="Play">▶</button>' : '') + '</div><div class="dg-stage">' + stageHtml(o, 0) + '</div><figcaption class="dg-cap">' + rich(capOf(o, 0)) + '</figcaption>' + (n > 1 ? '<div class="dg-nav"><button type="button" class="dg-b" data-dgn="-1" aria-label="Previous step">◀</button><span class="dg-dots">' + Array.apply(null, Array(n)).map(function (_, k) { return '<i data-dgi="' + k + '"' + (k === 0 ? ' class="on"' : '') + '></i>'; }).join('') + '</span><button type="button" class="dg-b" data-dgn="1" aria-label="Next step">▶</button></div>' : '') + '</figure>';
  };
  // a case picture for the imaging stations: {k:'cxr'|'ecg'|'axr'|'ct', a: kind}
  DG.img = function (spec) {
    if (!spec) return '';
    var M = window.MEV || {}, h = '';
    try {
      if (spec.k === 'ecg') h = (DG.ECG[spec.a] || (M.ECG || {})[spec.a] || function () { return ''; })();
      else if (spec.k === 'cxr') h = DG.cxr(spec.a);
      else if (spec.k === 'axr') h = DG.axr(spec.a);
      else if (spec.k === 'ct') h = DG.ct(spec.a);
    } catch (e) { h = ''; }
    return h ? '<div class="dg-img dg-img-' + esc(spec.k) + '">' + h + '</div>' : '';
  };
  function show(fig, i) {
    var o = R[fig.dataset.dg]; if (!o) return;
    var n = nOf(o); i = (i + n) % n; fig.dataset.i = i;
    fig.classList.remove('dg-rev');
    var st = fig.querySelector('.dg-stage'); st.innerHTML = stageHtml(o, i);
    fig.querySelector('.dg-cap').innerHTML = rich(capOf(o, i));
    var c = fig.querySelector('.dg-n'); if (c) c.textContent = (i + 1) + ' / ' + n;
    Array.prototype.forEach.call(fig.querySelectorAll('[data-dgi]'), function (d, k) { d.classList.toggle('on', k === i); });
  }
  DG.show = show;
  var timers = new Map();
  function stop(fig) { var t = timers.get(fig); if (t) { clearInterval(t); timers.delete(fig); } var b = fig.querySelector('[data-dgp]'); if (b) { b.textContent = '▶'; b.setAttribute('aria-label', 'Play'); } fig.classList.remove('playing'); }
  function play(fig) {
    timers.forEach(function (_, f) { if (f !== fig) stop(f); });
    var b = fig.querySelector('[data-dgp]'); if (b) { b.textContent = '❚❚'; b.setAttribute('aria-label', 'Pause'); }
    fig.classList.add('playing');
    var o = R[fig.dataset.dg], gap = (o && o.ms) || 2200;
    timers.set(fig, setInterval(function () { if (!document.body.contains(fig)) return stop(fig); show(fig, +fig.dataset.i + 1); }, gap));
  }
  DG.stopAll = function () { timers.forEach(function (_, f) { stop(f); }); };
  document.addEventListener('click', function (e) {
    var tm = document.body.classList.contains('dg-testing') && e.target.closest && !e.target.closest('button') && e.target.closest('.dg-stage,.dg-cap');
    if (tm) { var tf = tm.closest('.dg'); if (tf) { tf.classList.toggle('dg-rev'); return; } }
    var b = e.target.closest && e.target.closest('[data-dgn],[data-dgp],[data-dgi]'); if (!b) return;
    var fig = b.closest('.dg'); if (!fig) return;
    e.preventDefault();
    if (b.dataset.dgp != null) return timers.has(fig) ? stop(fig) : play(fig);
    stop(fig);
    if (b.dataset.dgn != null) show(fig, +fig.dataset.i + (+b.dataset.dgn));
    else show(fig, +b.dataset.dgi);
  });
  // swipe left or right on a picture to step
  var sx = null;
  document.addEventListener('touchstart', function (e) { var f = e.target.closest && e.target.closest('.dg-stage'); sx = f ? [e.touches[0].clientX, e.touches[0].clientY, f.closest('.dg')] : null; }, {passive: true});
  document.addEventListener('touchend', function (e) { if (!sx) return; var dx = e.changedTouches[0].clientX - sx[0], dy = e.changedTouches[0].clientY - sx[1]; if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) { stop(sx[2]); show(sx[2], +sx[2].dataset.i + (dx < 0 ? 1 : -1)); } sx = null; }, {passive: true});

  /* ---------- styles ---------- */
  var css = '.dg-testing .dg:not(.dg-rev) .dg-cap,.dg-testing .dg:not(.dg-rev) .dg-cap b,.dg-testing .dg:not(.dg-rev) .dg-card:not(.done) b,.dg-testing .dg:not(.dg-rev) .dg-card .sm,.dg-testing .dg:not(.dg-rev) .dg-tab tr:not(.done) td{color:transparent!important;text-shadow:0 0 8px var(--muted);user-select:none}' +
    '.dg-testing .dg:not(.dg-rev) .dg-svg text:not(.keep),.dg-testing .dg:not(.dg-rev) .dg-tag,.dg-testing .dg:not(.dg-rev) .dg-img text{opacity:0}' +
    '.dg-testing .dg:not(.dg-rev) .dg-cap::before{content:"👆 Say it, then tap the picture to check";display:block;color:var(--muted);text-shadow:none;font-size:.85rem}' +
    '.dg-testing .dg-stage,.dg-testing .dg-cap{cursor:pointer}.dg-testing .dg.dg-rev{outline:2px solid var(--accent);outline-offset:2px}' +
    '.dg{margin:0;border:1px solid var(--line);border-radius:12px;background:var(--surface-2);padding:10px 12px;display:flex;flex-direction:column;gap:8px;min-width:0}' +
    '.dg-head{display:flex;align-items:center;gap:8px}.dg-head b{flex:1;font-family:var(--f-display);font-size:1rem;line-height:1.25}' +
    '.dg-n{font-family:var(--f-mono);font-size:.72rem;color:var(--muted)}' +
    '.dg-b{border:1px solid var(--line);background:var(--surface);border-radius:999px;min-width:34px;height:30px;padding:0 10px;font-size:.85rem;line-height:1}' +
    '.dg-b:hover{border-color:var(--accent)}.dg.playing [data-dgp]{background:var(--accent);color:var(--on-accent);border-color:var(--accent)}' +
    '.dg-stage{min-height:60px;touch-action:pan-y}.dg-stage .dg-svg,.dg-img svg{width:100%;height:auto;max-height:340px;display:block;margin:0 auto}' +
    '.dg-cap{font-size:.95rem;min-height:2.6em;line-height:1.45}.dg-cap b{color:var(--accent-ink)}' +
    '.dg-nav{display:flex;align-items:center;justify-content:center;gap:10px}.dg-dots{display:flex;gap:5px;flex-wrap:wrap;justify-content:center;max-width:70%}' +
    '.dg-dots i{width:8px;height:8px;border-radius:50%;background:var(--line);cursor:pointer}.dg-dots i.on{background:var(--accent);transform:scale(1.25)}' +
    '.dg-svg text{fill:var(--ink);font-family:var(--f-body);font-size:11px}.dg-svg .dg-tm{fill:var(--muted);font-size:9.5px}.dg-svg .dg-ta{fill:var(--accent-ink);font-weight:700}.dg-svg .dg-tb{font-weight:700}.dg-svg .dg-tr{fill:var(--bad);font-weight:700}' +
    '.dg-ln{stroke:var(--ink);fill:none;stroke-width:1.6;stroke-linecap:round;stroke-linejoin:round}.dg-thin{stroke:var(--muted);fill:none;stroke-width:1}.dg-dash{stroke:var(--muted);fill:none;stroke-width:1;stroke-dasharray:3 3}' +
    '.dg-body,.dg-body *{fill:var(--surface);stroke:var(--muted);stroke-width:1.4}.dg-skin{fill:var(--surface);stroke:var(--muted);stroke-width:1.4}' +
    '.dg-pt{fill:var(--surface);stroke:var(--accent);stroke-width:2}.dg-pt.dg-on,.dg-fa{fill:var(--accent);stroke:var(--accent)}' +
    '.dg-hl{fill:var(--accent);fill-opacity:.28;stroke:var(--accent);stroke-width:1.4}.dg-wl{fill:var(--warn);fill-opacity:.3;stroke:var(--warn);stroke-width:1.4}.dg-bl{fill:var(--bad);fill-opacity:.28;stroke:var(--bad);stroke-width:1.4}' +
    '.dg-red{fill:var(--bad)}.dg-grn{fill:var(--good)}.dg-amb{fill:var(--warn)}.dg-acc{fill:var(--accent)}.dg-mut{fill:var(--line)}.dg-ink{fill:var(--ink)}.dg-srf{fill:var(--surface)}' +
    '.dg-ar{stroke:var(--accent);stroke-width:2;fill:none}.dg-ar.dg-ah{fill:var(--accent);stroke:none}.dg-arr{stroke:var(--bad);stroke-width:2;fill:none}.dg-arr.dg-ah{fill:var(--bad);stroke:none}' +
    '.dg-off{opacity:.16;transition:opacity .35s}.dg-on{opacity:1;transition:opacity .35s}' +
    '.dg-tag rect{fill:var(--accent)}.dg-tag text{fill:var(--on-accent)!important;font-size:9.5px;font-weight:700}.dg-tag.w rect{fill:var(--warn)}.dg-tag.b rect{fill:var(--bad)}.dg-tag.g rect{fill:var(--good)}.dg-tag.m rect{fill:var(--muted)}' +
    '.dg-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(118px,1fr));gap:6px}' +
    '.dg-card{display:flex;flex-direction:column;gap:2px;border:1px solid var(--line);border-radius:10px;padding:8px;background:var(--surface);opacity:.5;transition:opacity .3s,border-color .3s,transform .3s}' +
    '.dg-card .ic{font-size:1.35rem;line-height:1.2}.dg-card b{font-size:.9rem;line-height:1.25}.dg-card .sm{font-size:.82rem;color:var(--muted);line-height:1.35}' +
    '.dg-card.done{opacity:.85}.dg-card.on{opacity:1;border-color:var(--accent);box-shadow:0 0 0 2px var(--accent-soft);transform:translateY(-1px)}' +
    '.dg-tw{overflow-x:auto}.dg-tab{border-collapse:collapse;width:100%;font-size:.86rem}.dg-tab th,.dg-tab td{border:1px solid var(--line);padding:5px 7px;text-align:left;vertical-align:top}' +
    '.dg-tab tr{opacity:.55;transition:opacity .3s}.dg-tab tr:first-child,.dg-tab tr.on,.dg-tab tr.done{opacity:1}.dg-tab tr.on{background:var(--accent-soft)}.dg-tab tr.on th{color:var(--accent-ink)}' +
    '.dg-img{border-radius:10px;overflow:hidden;background:#000;max-width:520px}.dg-img-ecg{background:transparent}' +
    '@media (prefers-reduced-motion:reduce){.dg-off,.dg-on,.dg-card{transition:none}}';
  var st = document.createElement('style'); st.textContent = css; (document.head || document.documentElement).appendChild(st);
})();
