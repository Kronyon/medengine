/* ---------- v2.1: 🧲 Triggers, shared by medengine-OSCE and medengine-STUDY ----------
   The High-Yield pattern: one line = the scene + the word that flips it → the answer. Lines that share a scene stack, so the
   eye sees what stays the same and what changes. One long scroll (⌘F finds anything), a picture on every line, 🔒 Lock
   blurs the answers (still findable), tap or N reveals, L locks. TG.page(T, U, opts) returns the HTML; TG.mount(root)
   wires it. T = D.trg (c, bug, sc, dr, ix, mx); U = {weeks: [[id, name]], units: [{i, name, w, o, h: [[type, clue, ans]]}]}. */
(function () {
  const TG = window.TG = {};
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
  const fmt = s => esc(s).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
  const ST = (() => { try { return JSON.parse(localStorage.getItem('medengine-trg') || '{}'); } catch (e) { return {}; } })();
  const keep = () => { try { localStorage.setItem('medengine-trg', JSON.stringify(ST)); } catch (e) {} };

  /* ----- pictures: one sprite, every line points at a symbol ----- */
  const P = '#7a4fc9', K = '#e0577f', R = '#d0306b';
  const S = (id, body, vb) => '<symbol id="ti-' + id + '" viewBox="' + (vb || '0 0 24 24') + '">' + body + '</symbol>';
  const st = d => '<path d="' + d + '" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>';
  const fl = d => '<path d="' + d + '" fill="currentColor"/>';
  const c = (x, y, r, f) => '<circle cx="' + x + '" cy="' + y + '" r="' + r + '" fill="' + f + '"/>';
  const rod = (x, y, a, f, w) => '<rect x="' + (x - (w || 4.5)) + '" y="' + (y - 1.7) + '" width="' + 2 * (w || 4.5) + '" height="3.4" rx="1.7" fill="' + f + '" transform="rotate(' + a + ' ' + x + ' ' + y + ')"/>';
  const SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + [
    S('heart', fl('M12 20.5s-7.5-4.6-7.5-10.4A4.2 4.2 0 0 1 12 7.4a4.2 4.2 0 0 1 7.5 2.7c0 5.8-7.5 10.4-7.5 10.4z')),
    S('lungs', st('M12 3v8M12 8c-1.5 0-2-1-2-1M12 8c1.5 0 2-1 2-1M10 7.5C7 6 4 8.5 4 13v5.2c0 1.4 1.3 2 2.6 1.3L10.5 17V7.5zM14 7.5C17 6 20 8.5 20 13v5.2c0 1.4-1.3 2-2.6 1.3L13.5 17V7.5z')),
    S('gut', st('M6 4h11a2.2 2.2 0 0 1 0 4.4H8a2.2 2.2 0 0 0 0 4.4h9a2.2 2.2 0 0 1 0 4.4H9a2.2 2.2 0 0 0 0 4.4h7')),
    S('liver', fl('M3 10.5C3 7 7.5 5 12.5 5S21 6.2 21 8.6c0 4.5-6 9.6-11 10.3C6 19.2 3 15 3 10.5z')),
    S('kidney', st('M10 3.5C5.5 3.5 4 7.5 4 12s1.5 8.5 6 8.5c3 0 3.3-3.2 2-5.2-1-1.6-1-3.6 0-5.2 1.3-2.2 1.2-6.6-2-6.6zM12.5 12h3l3 8.5')),
    S('brain', st('M11 4.5a3 3 0 0 0-5.5 1.6 3 3 0 0 0-1.5 5 3 3 0 0 0 1.7 4.9A3 3 0 0 0 11 18.5zM13 4.5a3 3 0 0 1 5.5 1.6 3 3 0 0 1 1.5 5 3 3 0 0 1-1.7 4.9A3 3 0 0 1 13 18.5zM11 4.5V20M13 4.5V20')),
    S('eye', st('M2 12s3.8-6.5 10-6.5S22 12 22 12s-3.8 6.5-10 6.5S2 12 2 12z') + fl('M12 8.8a3.2 3.2 0 1 0 .01 0z')),
    S('ear', st('M7.5 9.5a5 5 0 0 1 10 0c0 3.2-3.2 4-3.2 7.2a3 3 0 0 1-6 .3M10.5 10a2 2 0 0 1 4 0c0 1.6-2 2-2 3.4')),
    S('skin', st('M3 9c3-2 6 2 9 0s6 2 9 0M3 14h18M3 19h18M8 9V4.5M15.5 9V5.5')),
    S('bone', st('M8 6.5a2.3 2.3 0 1 0-2.4 2.8l9.1 9.1a2.3 2.3 0 1 0 2.8 2.4 2.3 2.3 0 1 0 2.4-2.8L10.8 8.9A2.3 2.3 0 1 0 8 6.5z')),
    S('leg', st('M9 3h5l-.8 9.5.8 5.5c.2 1.4-.8 2.5-2.2 2.5H6.5v-1.6l3.2-1.3-.7-5.1z')),
    S('blood', fl('M12 3s6.2 7.1 6.2 11.2a6.2 6.2 0 0 1-12.4 0C5.8 10.1 12 3 12 3z')),
    S('sugar', st('M12 3l8 4.5v9L12 21l-8-4.5v-9zM4 7.5l8 4.5 8-4.5M12 12v9')),
    S('thyroid', st('M12 7v10M12 9.5C10 5.5 5 5.5 5 10.5s4.2 6.2 7 3.2M12 9.5c2-4 7-4 7 1s-4.2 6.2-7 3.2')),
    S('breast', st('M3 8c1 7 5 11.5 9 11.5S20 15 21 8') + c(12, 15, 1.4, 'currentColor')),
    S('mind', st('M14.5 20.5v-3h2a2 2 0 0 0 2-2v-2.3l2-1-2-3.2A7.3 7.3 0 0 0 4.5 10c0 3 1.7 5 3 6v4.5') + fl('M11 6.5l1 2.2 2.3.6-2.3.6-1 2.2-1-2.2-2.3-.6 2.3-.6z')),
    S('nerve', st('M12 6.5a2.8 2.8 0 1 0 .01 0M12 9.3V21M12 17l-3.2 3.5M12 17l3.2 3.5M9.8 5L6.5 2.5M14.2 5l3.3-2.5M9.3 8.3H4.5')),
    S('ecg', st('M2 12.5h4.2l2-5.5 3.2 11 3-13 2.2 7.5H22')),
    S('scan', st('M12 4a8 8 0 1 0 .01 0M12 9a3 3 0 1 0 .01 0M4 20h16')),
    S('lab', st('M8.5 3h7M10 3v14.5a2 2 0 0 0 4 0V3') + fl('M10 12h4v5.5a2 2 0 0 1-4 0z')),
    S('preg', st('M10.5 3.8a2 2 0 1 0 .01 0M9.3 8h2.7c3.2 1 5.2 4.2 4.2 7.2-.6 1.9-3 2.8-5 1.9V21M9.3 8v13')),
    S('child', st('M12 4a2.6 2.6 0 1 0 .01 0M7.5 10.5h9M12 9.5v5.5M8.8 21l3.2-6 3.2 6')),
    S('travel', st('M2.5 13.5l19-7.5-5.5 14.5-3.2-6.3-6.8-1.2zM12.8 14.2L21.5 6')),
    S('drug', st('M8.4 16.6l8.2-8.2a3.6 3.6 0 0 0-5.1-5.1l-8.2 8.2a3.6 3.6 0 0 0 5.1 5.1zM7.3 7.4l5.3 5.3')),
    S('fever', st('M10 4.5a2 2 0 0 1 4 0v9.6a4.2 4.2 0 1 1-4 0zM12 9v8.5')),
    S('old', st('M9.5 3.5a2 2 0 1 0 .01 0M9.5 7.5v6.5L7.5 21M9.5 14l3 7M9.5 9l4 3M16 10.5V21M16 10.5a1.8 1.8 0 0 1 3 0')),
    S('star', fl('M12 2.8l2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3L2.9 9.5l6.3-.9z')),
    S('warn', st('M12 3.5l9.5 17h-19zM12 10v4.8M12 17.6v.4')),
    S('flag', st('M5 21V3.5M5 4h12.5l-2.8 4 2.8 4H5')),
    S('hook', st('M13 3v10.5a4.5 4.5 0 1 1-9 0l2.2 2.2M13 3l2 2')),
    S('pill', st('M8.4 16.6l8.2-8.2a3.6 3.6 0 0 0-5.1-5.1l-8.2 8.2a3.6 3.6 0 0 0 5.1 5.1zM7.3 7.4l5.3 5.3')),
    S('inh', st('M9 3h4.5v6H16a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-6a2 2 0 0 1-2-2V9h1zM8 13.5H3.5v4H8')),
    S('iv', st('M8 3h8v9a4 4 0 0 1-8 0zM12 16v5.5M9.5 21.5h5M8 7.5h8')),
    S('inj', st('M18.5 2.5l3 3M16 5l3 3M17.5 6.5L8 16l-3.2 1.2L6 14l9.5-9.5M9.5 11.5l3 3M2.5 21.5l3-3')),
    S('cream', st('M4 17.5l9.5-9.5 3.2 3.2L7.2 20.7H4zM16 8l3-3M14.5 6.5l3 3')),
    S('drop', st('M12 3s5.2 6 5.2 10a5.2 5.2 0 0 1-10.4 0C6.8 9 12 3 12 3z')),
    S('patch', st('M3.5 8.5l5-5 12 12-5 5zM9 9l6 6') + c(7, 11, .9, 'currentColor') + c(11, 7, .9, 'currentColor') + c(13, 17, .9, 'currentColor') + c(17, 13, .9, 'currentColor')),
    S('spray', st('M7.5 9h6.5v12H7.5zM9.5 9V5.5H13M14.5 6l5-2M14.5 7.5h5M14.5 9l5 2')),
    S('proc', st('M2.5 21.5l9.5-9.5M12 12l7.5-9 2 2-9 7.5z')),
    S('cut', st('M2.5 21.5l9.5-9.5M12 12l7.5-9 2 2-9 7.5z')),
    S('needle', st('M18.5 2.5l3 3M16 5l3 3M17.5 6.5L8 16l-3.2 1.2L6 14l9.5-9.5M2.5 21.5l3-3')),
    S('drain', st('M5 3.5c0 6 4 6 4 11s-4 5-4 7M9 14.5h7a3 3 0 0 1 3 3v4H13v-4M16 9.5l3-3')),
    S('shock', fl('M13.5 2.5L5 13.5h6l-1.5 8 8.5-11h-6z')),
    S('device', st('M7 4.5h8a3 3 0 0 1 3 3v6a3 3 0 0 1-3 3H7a3 3 0 0 1-3-3v-6a3 3 0 0 1 3-3zM18 10.5c2 0 2.5 2.5 2.5 5s-1 5.5-4.5 5.5M7.5 10.5h2l1-2 1.5 4 1-2h2')),
    S('scope', st('M3 5h7.5a3.2 3.2 0 0 1 0 6.4H8.2a3.2 3.2 0 0 0 0 6.4h10.3a3 3 0 0 0 3-3M19.5 12.3a2 2 0 1 0 .01 0')),
    S('laser', st('M3 12h6M12 4v5M12 15v5M5.6 5.6l3.2 3.2M15.2 15.2l3.2 3.2M15.2 8.8l3.2-3.2M5.6 18.4l3.2-3.2') + c(12, 12, 2.4, 'currentColor')),
    S('ray', st('M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M16.3 7.7l2.1-2.1M5.6 18.4l2.1-2.1') + c(12, 12, 3.6, 'currentColor')),
    S('air', st('M6 9.5c0-3.6 2.7-6 6-6s6 2.4 6 6v3.8c0 4-2.7 7.2-6 7.2s-6-3.2-6-7.2zM9.5 13.5h5M12 13.5v7M2.5 11h3.5M18 11h3.5')),
    S('bag', st('M7 3h10v9.5a5 5 0 0 1-10 0zM12 17.5v4M7 7.5h10M10 10.5h4')),
    S('talk', st('M4 5h16v10H10l-4.5 4v-4H4zM8 9.5h8M8 12h5')),
    S('law', st('M12 3v17.5M7 20.5h10M5 6.5h14M5 6.5l-2.5 6.5a2.6 2.6 0 0 0 5 0zM19 6.5l-2.5 6.5a2.6 2.6 0 0 0 5 0z')),
    S('bed', st('M6.5 3.5v5a4.2 4.2 0 0 0 8.4 0v-5M10.7 12.7v2.8a5 5 0 0 0 10 0v-2.3') + c(20.7, 11.2, 1.9, 'currentColor')),
    S('score', st('M8.5 3.5h7v3h-7zM6.5 5H5v16.5h14V5h-1.5M8 11.5h8M8 15h8M8 18.5h5')),
    S('xray', st('M4 3h16v18H4zM12 6v12M8.5 8c-2 2-2 6 0 9M15.5 8c2 2 2 6 0 9M9.5 10.5h5M9.5 13.5h5')),
    S('ct', st('M12 3.5a8.5 8.5 0 1 0 .01 0M12 9a3 3 0 1 0 .01 0M3.5 21h17')),
    S('mri', st('M4.5 4h4.5v8a3 3 0 0 0 6 0V4h4.5v8a7.5 7.5 0 0 1-15 0zM4.5 8H9M15 8h4.5')),
    S('us', st('M9 2.5h6v6.5l2 3H7l2-3zM6.5 15c3.2 3 7.8 3 11 0M4.5 18.2c4.2 4 10.8 4 15 0')),
    // bugs: the real Gram-stain look
    S('b-gpc_cl', [[8, 9], [12, 7.6], [16, 9.6], [10, 12.8], [14.2, 13.4], [8.4, 16.6], [12.6, 17.4], [17, 16.4]].map(([x, y]) => c(x, y, 2.2, P)).join('')),
    S('b-gpc_ch', [[4.5, 19], [7.5, 16.2], [10.4, 13.2], [13.2, 10.2], [16.2, 7.4], [19.4, 4.8]].map(([x, y]) => c(x, y, 1.9, P)).join('')),
    S('b-gpc_pr', '<ellipse cx="12" cy="12" rx="9" ry="6.2" fill="none" stroke="' + P + '" stroke-width="1" stroke-dasharray="2 1.5" opacity=".7"/><ellipse cx="9" cy="12" rx="2.6" ry="3.8" fill="' + P + '"/><ellipse cx="15" cy="12" rx="2.6" ry="3.8" fill="' + P + '"/>'),
    S('b-gnc', '<path d="M10.8 7.5a4.5 4.5 0 0 0 0 9z" fill="' + K + '"/><path d="M13.2 7.5a4.5 4.5 0 0 1 0 9z" fill="' + K + '"/><path d="M4.2 17.5a2.6 2.6 0 0 0 0 5zM5.8 17.5a2.6 2.6 0 0 1 0 5z" fill="' + K + '" opacity=".6"/>'),
    S('b-gncb', [[6, 7, 20], [12, 6, -10], [17.5, 8.5, 30], [8, 13, -25], [14, 13, 10], [9, 18.5, 15], [16, 18, -20]].map(([x, y, a]) => rod(x, y, a, K, 2.2)).join('')),
    S('b-gnr', rod(8, 7, 20, K) + rod(15.5, 11, -15, K) + rod(9, 16.5, -30, K) + rod(17, 18, 25, K, 3.5)),
    S('b-gncv', '<path d="M3.5 8c2.5-3 5 1.5 7.5-1.5M12 15c2.5-3 5 1.5 7.5-1.5M5 19c2-2.4 4 1.2 6-1.2" fill="none" stroke="' + K + '" stroke-width="2.6" stroke-linecap="round"/>'),
    S('b-gpr', rod(8, 7, 20, P) + rod(15.5, 11, -15, P) + rod(9, 16.5, -30, P) + rod(17, 18, 25, P, 3.5)),
    S('b-gprs', rod(8.5, 8, 10, P, 5.5) + '<ellipse cx="13.2" cy="8.8" rx="1.4" ry="1.1" fill="#fff"/>' + rod(14, 16, -15, P, 5.5) + '<ellipse cx="18.8" cy="14.8" rx="1.4" ry="1.1" fill="#fff"/>'),
    S('b-gpbr', '<path d="M3 20c3-3 4-6 7-8s6-2 8-6M10 12c1 3 0 5 2 7M14 9.5c2 1 4 0 6 1" fill="none" stroke="' + P + '" stroke-width="2" stroke-linecap="round"/>'),
    S('b-afb', '<path d="M3.5 7c3 1 5.5 0 8 2M12 14c3 1 5.5 0 8.5 2.5M5 18c2-1.5 4-1 6 0" fill="none" stroke="' + R + '" stroke-width="2.6" stroke-linecap="round" stroke-dasharray="2.2 1"/>'),
    S('b-spiro', '<path d="M2 12c.9-3 1.9 3 2.8 0s1.9 3 2.8 0 1.9 3 2.8 0 1.9 3 2.8 0 1.9 3 2.8 0 1.9 3 2.8 0 1.9 3 2.8 0" fill="none" stroke="#2f8f9d" stroke-width="1.8" stroke-linecap="round"/>'),
    S('b-nowall', [[7, 8, 2], [13, 6.5, 1.3], [17, 10, 2.4], [9, 14, 1.6], [14.5, 15.5, 2], [6.5, 18.5, 1.2], [18, 18, 1.4]].map(([x, y, r]) => c(x, y, r, '#a487c9')).join('')),
    S('b-intra', '<circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.4" opacity=".55"/>' + c(12, 12, 2.6, 'currentColor') + [[7.5, 8.5], [9, 16], [16, 8], [16.5, 15.5], [12.5, 18.5], [6.5, 12.5]].map(([x, y]) => c(x, y, 1.1, K)).join('')),
    S('b-venv', '<circle cx="12" cy="12" r="6" fill="#e3a23c" opacity=".35" stroke="#c07a12" stroke-width="1.6"/>' + st('M12 2.5v3.5M12 18v3.5M2.5 12H6M18 12h3.5M5.3 5.3l2.4 2.4M16.3 16.3l2.4 2.4M16.3 7.7l2.4-2.4M5.3 18.7l2.4-2.4') + c(12, 12, 2, '#c07a12')),
    S('b-vnak', '<path d="M12 3.5l7.4 4.25v8.5L12 20.5l-7.4-4.25v-8.5z" fill="#e3a23c" opacity=".3" stroke="#c07a12" stroke-width="1.6"/><path d="M12 3.5v8.5l7.4 4.25M12 12l-7.4 4.25" fill="none" stroke="#c07a12" stroke-width="1" opacity=".7"/>'),
    S('b-yeast', '<ellipse cx="10" cy="13" rx="5.2" ry="6.2" fill="#c9a03a"/><circle cx="16.6" cy="7.4" r="2.8" fill="#c9a03a"/>'),
    S('b-yeastc', '<circle cx="11.5" cy="12.5" r="9" fill="none" stroke="#c9a03a" stroke-width="1.2" stroke-dasharray="2 1.6"/><circle cx="11.5" cy="12.5" r="4.6" fill="#c9a03a"/>'),
    S('b-mould', '<path d="M3.5 20.5L12 12l8-8.5M12 12l6.5 2M8 16l-1.8-6M16 7.8L15 3M18.5 14l2.5-2M6.2 10l-2.5-1.5" fill="none" stroke="#4f9a5a" stroke-width="2" stroke-linecap="round"/>'),
    S('b-proto', '<path d="M6 12c0-4 3-7 6.5-7S19 8 19 12s-3 6.5-6.5 6.5S6 16 6 12z" fill="#2b9aa0" opacity=".35" stroke="#2b9aa0" stroke-width="1.6"/>' + c(12.5, 11.5, 2.2, '#2b9aa0') + '<path d="M6 12C4 13 4 15.5 2.5 17M7 15.5c-1 1.5-1 3-2.5 4.5" fill="none" stroke="#2b9aa0" stroke-width="1.4" stroke-linecap="round"/>'),
    S('b-mite', '<circle cx="12" cy="12.5" r="5" fill="#8a5a3c"/>' + '<path d="M7.5 10L3 7.5M7.2 12.5H2.5M7.5 15l-4 3M16.5 10L21 7.5M16.8 12.5h4.7M16.5 15l4 3M10 7.8L9 4.5M14 7.8l1-3.3" fill="none" stroke="#8a5a3c" stroke-width="1.5" stroke-linecap="round"/>'),
    S('b-louse', '<ellipse cx="12" cy="13.5" rx="3.8" ry="6" fill="#8a6a4c"/><circle cx="12" cy="5.5" r="2" fill="#8a6a4c"/><path d="M8.5 11L4 9M8.3 14H3.5M8.5 17l-4 2.5M15.5 11L20 9M15.7 14h4.8M15.5 17l4 2.5" fill="none" stroke="#8a6a4c" stroke-width="1.5" stroke-linecap="round"/>'),
    S('b-worm', '<path d="M3.5 18c3 0 3-6 6-6s3 6 6 6 3-8 5-10" fill="none" stroke="#c46a6a" stroke-width="3" stroke-linecap="round"/>'),
  ].join('') + '</svg>';

  /* ----- which picture a clue gets: the kind of clue, else the organ ----- */
  const ORG = {heart: 'heart', lungs: 'lungs', gut: 'gut', hepat: 'liver', uro: 'kidney', scrot: 'kidney', brain: 'brain', nerve: 'nerve', eye: 'eye', ent: 'ear', skin: 'skin', limb: 'leg', joint: 'bone', blood: 'blood', sugar: 'sugar', neck: 'thyroid', breast: 'breast', mind: 'mind', bug: 'b-gnr', pill: 'pill', proc: 'proc'};
  const KIND = [
    [/\becg\b|\bst (?:up|elevation|depression)|\bqrs\b|\bqtc?\b|p waves?|t waves?|\blbbb|\brbbb|delta wave|heart block|av block|bradycardi|tachycardi|torsade/i, 'ecg'],
    [/x-ray|\bcxr\b|\bct\b|\bmri\b|ultrasound|\bscan\b|\becho\b|angiogra|mammogra|\bdexa\b|\bfilm\b|\bhrct\b/i, 'scan'],
    [/\bsodium|potassium|calcium|troponin|\bcrp\b|\bwcc\b|\bhb\b|\bmcv\b|ferritin|\btsh\b|\bt4\b|\blevels?\b|\bbloods?\b|\babg\b|\bph\b|lactate|glucose|platelet|\binr\b|\balp\b|\blfts?\b|egfr|creatinine|antibod|serology|culture|\bcsf\b|\burea\b|bilirubin|amylase|lipase|\bck\b|eosinophil|hba1c|\bpsa\b|d-dimer|\bbnp\b/i, 'lab'],
    [/pregnan|trimester|postpartum|postnatal|breastfe|after birth|antenatal/i, 'preg'],
    [/\bchild|\bbaby|\binfant|newborn|neonat|toddler|teenager|\bboy\b|\bgirl\b|school/i, 'child'],
    [/travel|abroad|returned from|holiday|africa|\basia\b|india|tropic/i, 'travel'],
    [/\bstarted\b|\btaking\b|\btablets?\b|\bmg\b|\bdose\b|overdose|\bdrug\b|statin|steroid|antibiotic|\bssri|\bon (?:a |an )?(?:new )?[a-z-]+(?:pril|sartan|olol|pine|azole|mab|cillin|mycin|floxacin|ide|one)\b/i, 'drug'],
    [/fever|pyrexi|rigors|febrile|temperature/i, 'fever'],
    [/elderly|\bolder\b|over (?:6|7|8)\d\b/i, 'old'],
  ];
  const kindOf = s => { for (const [re, k] of KIND) if (re.test(s)) return k; return ''; };
  const ico = (k, cls) => '<svg class="ti ti-' + k + (cls ? ' ' + cls : '') + '" aria-hidden="true"><use href="#ti-' + k + '"/></svg>';
  const rowH = (k, clueH, ansH, cls, attr) => '<div class="tg' + (cls ? ' ' + cls : '') + '"' + (attr || '') + '>' + ico(k) + '<div class="tc">' + clueH + '</div><div class="ta">' + ansH + '</div></div>';
  /* the answer's key term is bold: whatever is marked, else the part before the first colon */
  const fa = a => { if (a.includes('**')) return fmt(a); const i = a.indexOf(':'); return i > 0 && i <= 48 ? '<b>' + esc(a.slice(0, i)) + '</b>' + fmt(a.slice(i)) : fmt(a); };
  const row = (k, clue, ans, cls, tag, attr) => rowH(k, (tag || '') + fmt(clue), fa(ans), cls, attr);
  const TAG = {'!': ['trap', '⚠️ Trap'], uk: ['uk', '🇬🇧 UK'], hk: ['hk', '🪝 Hook']};
  const PARTS = [['c', '🩺', 'Conditions'], ['b', '🦠', 'Bugs'], ['d', '💊', 'Drugs'], ['x', '🔬', 'Investigations'], ['m', '🛠️', 'Management']];
  const MORPH = [['gpc_cl', 'Purple clusters', 'Staph'], ['gpc_ch', 'Purple chains', 'Strep, Enterococcus'], ['gpc_pr', 'Purple pairs, capsule', 'Pneumococcus'], ['gnc', 'Pink kidney-bean pairs', 'Neisseria, Moraxella'], ['gncb', 'Pink tiny rods', 'Haemophilus, Bordetella'], ['gnr', 'Pink rods', 'E. coli, Pseudomonas, Salmonella'], ['gncv', 'Pink commas', 'Campylobacter, Vibrio, H. pylori'], ['gpr', 'Purple rods', 'Listeria, Corynebacterium'], ['gprs', 'Purple rods with a spore', 'Clostridia, Bacillus'], ['gpbr', 'Purple branches', 'Actinomyces'], ['afb', 'Red beaded rods', 'TB'], ['spiro', 'Spirals', 'Syphilis, Lyme'], ['nowall', 'No wall', 'Mycoplasma'], ['intra', 'Lives inside cells', 'Chlamydia, Coxiella'], ['venv', 'Enveloped virus', 'Herpes, flu, HIV'], ['vnak', 'Naked virus', 'Noro, HPV, parvo'], ['yeast', 'Budding yeast', 'Candida'], ['yeastc', 'Yeast with a capsule', 'Cryptococcus'], ['mould', 'Branching mould', 'Aspergillus, tinea'], ['proto', 'Protozoa', 'Giardia, malaria'], ['mite', 'Mite', 'Scabies'], ['louse', 'Louse', 'Head lice'], ['worm', 'Worm', 'Schistosoma']];

  function itemBlocks(groups, part){
    let h = '';
    groups.forEach(([title, ic, items], gi) => {
      h += '<div class="tg-sec" id="tg-' + part + gi + '" data-sec="' + esc(title) + '"><h3 class="tg-h3">' + ico(ORG[ic] || ic) + esc(title) + '<span class="tg-n">' + items.length + '</span></h3>';
      items.forEach(([name, pic, use, cats]) => {
        const nm = name.split(' · '), al = nm.slice(1).join(' · ');
        h += '<div class="tg-b" data-name="' + esc(name.toLowerCase()) + '">' + rowH(pic, fmt(use), '<b>' + esc(nm[0]) + '</b>' + (al ? ' <span class="tg-al">' + esc(al) + '</span>' : ''), 'go');
        cats.forEach(([cl, an]) => { h += row('warn', cl, an, 'catch'); });
        h += '</div>';
      });
      h += '</div>';
    });
    return h;
  }
  TG.count = (T, U) => Object.keys(T.c || {}).length + U.units.reduce((n, u) => n + u.h.length, 0) + (T.sc || []).reduce((n, s) => n + s[2].length, 0)
    + ['dr', 'ix', 'mx'].reduce((n, k) => n + (T[k] || []).reduce((a, g) => a + g[2].reduce((b, d) => b + 1 + d[3].length, 0), 0), 0);

  let cache = null;
  TG.page = function (T, U, opts) {
    opts = opts || {};
    if (!cache) cache = build(T, U, opts);
    const part = ST.part || 'all', n = TG.count(T, U);
    return '<div class="tgw' + (ST.lock ? ' tg-lock' : '') + '" id="tgRoot" data-part="' + part + '">' + SPRITE
      + '<div class="tg-top"><h1>🧲 Triggers</h1><p class="hint">The scene, the <b class="tg-hlx">word that flips it</b>, then the answer. Lines that share a scene stack under one label, so only the highlighted word changes. Every condition, bug, drug, test and procedure in your ILOs on one scroll. <span class="kbd">⌘F</span> once filters here; twice is your browser\'s own find. 🔒 <span class="kbd">L</span> blurs the answers, tap or <span class="kbd">N</span> to reveal.</p>'
      + '<details class="tg-why"><summary>Why this layout works for you</summary><ul><li><b>One stem, one flipping word.</b> Exams keep the scene and change one word; stacked lines train your eye on that word, the way you already hunt words in stems.</li><li><b>A picture on every line</b> sits next to the words, so each line is stored as an image as well as a sentence. The bug pictures are the real Gram-stain look: purple is positive, pink is negative.</li><li><b>Blur, then pull it out.</b> Recognising an answer feels like knowing it; saying it before you reveal is what makes it stick.</li></ul></details></div>'
      + '<div class="tg-bar"><input id="trq" type="search" placeholder="Filter every trigger: e.g. birds, lithium, CT, child" autocomplete="off" aria-label="Filter triggers" value="' + esc(TG.preset || '') + '">'
      + '<div class="tg-parts">' + [['all', '', 'All']].concat(PARTS).map(([k, e, l]) => '<button class="tg-p' + (part === k ? ' on' : '') + '" data-tgpart="' + k + '">' + (e ? e + ' ' : '') + l + '</button>').join('') + '</div>'
      + '<div class="tg-row2"><select id="tgJump" aria-label="Jump to a section"></select><button class="tg-p' + (ST.lock ? ' on' : '') + '" data-tglock>🔒 Lock</button><span class="tg-cnt" id="tgCnt">' + n.toLocaleString('en-GB') + ' lines</span></div></div>'
      + cache + '<p class="tg-foot hint">Condition clues marked HY and FA are adapted from High-Yield\'s <i>HY Internal Medicine</i> and <i>First Aid Step 1</i> and rewritten for UK practice; everything else is written for your ILOs from NICE, BTS, BNF and MHRA guidance.</p></div>';
  };
  function build(T, U, opts){
    const ua = opts.unitAttr || (i => 'data-u="' + i + '"');
    let h = '<section class="tg-part" data-part="c"><h2 class="tg-h2" id="tg-c">🩺 Conditions</h2>';
    U.weeks.forEach(([wid, wname]) => {
      const us = U.units.filter(u => u.w === wid); if (!us.length) return;
      h += '<div class="tg-sec" id="tg-w-' + esc(wid) + '" data-sec="' + esc(wname) + '"><h3 class="tg-h3">' + esc(wname) + '<span class="tg-n">' + us.length + '</span></h3>';
      us.forEach(u => {
        const org = ORG[u.o] || 'mind', s = (T.c || {})[u.i];
        h += '<div class="tg-b tg-u" id="tg-u' + u.i + '" data-name="' + esc(u.name.toLowerCase()) + '"><div class="tg-uh">' + ico(org) + '<button class="tg-un" ' + ua(u.i) + '>' + esc(u.name) + ' ↗</button><span class="tg-n">' + (u.h.length + (s ? 1 : 0)) + '</span></div>';
        if (s) h += row('star', s[0], s[1], 'star');
        let last = null;
        u.h.forEach(x => {
          const lab = x[3] || '';
          if (lab !== last) { if (last) h += '</div></div>'; if (lab) h += '<div class="tg-stk"><div class="tg-sth">' + esc(lab) + '</div><div class="tg-stb">'; last = lab; }
          const tg = TAG[x[0]]; h += row(x[0] === 'uk' ? 'flag' : x[0] === 'hk' ? 'hook' : kindOf(x[1]) || org, x[1], x[2], tg ? tg[0] : '', tg ? '<span class="tg-t ' + tg[0] + '">' + tg[1] + '</span>' : '');
        });
        if (last) h += '</div></div>';
        h += '</div>';
      });
      h += '</div>';
    });
    h += '</section><section class="tg-part" data-part="b"><h2 class="tg-h2" id="tg-b">🦠 Bugs</h2>';
    h += '<div class="tg-sec" data-sec="Picture key" id="tg-bkey"><h3 class="tg-h3">Picture key · what the stain looks like</h3><div class="tg-key">' + MORPH.map(([m, l, e]) => '<span>' + ico('b-' + m) + '<b>' + l + '</b> ' + esc(e) + '</span>').join('') + '</div>'
      + '<div class="tg-chips">' + Object.entries(T.bug || {}).sort((a, b) => a[1][0].localeCompare(b[1][0])).map(([k, [n, al, m]]) => '<button class="tg-chip" data-tgfind="' + esc(n) + '" title="' + esc(al) + '">' + ico('b-' + m) + esc(n) + '</button>').join('') + '</div></div>';
    (T.sc || []).forEach(([title, ic, lines], si) => {
      h += '<div class="tg-sec" id="tg-b' + si + '" data-sec="' + esc(title) + '"><h3 class="tg-h3">' + ico(ORG[ic] || ic) + esc(title) + '<span class="tg-n">' + lines.length + '</span></h3><div class="tg-b tg-stack">';
      lines.forEach(([k, cl, an]) => { const b = (T.bug || {})[k] || ['', '', 'gnr']; h += row('b-' + b[2], cl, an, '', '', ' data-al="' + esc((b[0] + ' ' + b[1]).toLowerCase()) + '"'); });
      h += '</div></div>';
    });
    h += '</section><section class="tg-part" data-part="d"><h2 class="tg-h2" id="tg-d">💊 Drugs</h2>' + itemBlocks(T.dr || [], 'd') + '</section>';
    h += '<section class="tg-part" data-part="x"><h2 class="tg-h2" id="tg-x">🔬 Investigations</h2>' + itemBlocks(T.ix || [], 'x') + '</section>';
    h += '<section class="tg-part" data-part="m"><h2 class="tg-h2" id="tg-m">🛠️ Management</h2>' + itemBlocks(T.mx || [], 'm') + '</section>';
    return h;
  }

  /* ----- behaviour ----- */
  let idx = null;
  function jumpOpts(root){
    const part = root.dataset.part, sel = root.querySelector('#tgJump'); if (!sel) return;
    const secs = Array.from(root.querySelectorAll('.tg-part' + (part === 'all' ? '' : '[data-part="' + part + '"]') + ' .tg-sec')).filter(s => !s.hidden);
    sel.innerHTML = '<option value="">Jump to…</option>' + secs.map(s => '<option value="' + s.id + '">' + esc(s.dataset.sec) + '</option>').join('');
  }
  function apply(root){
    const q = (root.querySelector('#trq').value || '').toLowerCase().trim(), terms = q.split(/\s+/).filter(Boolean), part = root.dataset.part;
    if (!idx) idx = Array.from(root.querySelectorAll('.tg')).map(r => [r, (r.textContent + ' ' + (r.dataset.al || '')).toLowerCase()]);
    const has = s => terms.every(t => s.includes(t));
    let n = 0, all = 0;
    root.querySelectorAll('.tg-part').forEach(p => { p.hidden = part !== 'all' && p.dataset.part !== part; });
    root.querySelectorAll('.tg-b').forEach(b => { b._nm = !!terms.length && has(b.dataset.name || ''); });
    idx.forEach(([r, t]) => { const b = r.closest('.tg-b'), ok = !terms.length || has(t) || (b && b._nm); r.hidden = !ok; if (!r.closest('.tg-part').hidden) { all++; if (ok) n++; } });
    root.querySelectorAll('.tg-stk').forEach(k => { k.hidden = !k.querySelector('.tg:not([hidden])'); });
    root.querySelectorAll('.tg-b').forEach(b => { b.hidden = !b.querySelector('.tg:not([hidden])'); });
    root.querySelectorAll('.tg-sec').forEach(s => { s.hidden = !!terms.length && !s.querySelector('.tg-b:not([hidden])'); });
    root.querySelectorAll('.tg-part').forEach(p => { if (!p.hidden && terms.length && !p.querySelector('.tg-sec:not([hidden]) .tg:not([hidden])')) p.hidden = true; });
    const cnt = root.querySelector('#tgCnt'); if (cnt) cnt.textContent = terms.length ? n.toLocaleString('en-GB') + ' of ' + all.toLocaleString('en-GB') : all.toLocaleString('en-GB') + ' lines';
    jumpOpts(root);
  }
  TG.mount = function (root) {
    root = root || document.getElementById('tgRoot'); if (!root) return;
    idx = null;
    setTop();
    apply(root);
    if (TG.jump) { const el = document.getElementById(TG.jump); TG.jump = null; if (el) requestAnimationFrame(() => el.scrollIntoView({block: 'start'})); }
    if (TG.preset) { TG.preset = null; }
  };
  /* the bar sits under the app header while the header is on screen, at the very top once it scrolls away */
  let topRaf = 0;
  function setTop(){ const root = document.getElementById('tgRoot'); if (!root) return; const hdr = document.querySelector('header.top'); root.style.setProperty('--tg-top', (hdr ? Math.max(0, Math.round(hdr.getBoundingClientRect().bottom)) : 0) + 'px'); }
  window.addEventListener('scroll', () => { if (topRaf || !document.getElementById('tgRoot')) return; topRaf = requestAnimationFrame(() => { topRaf = 0; setTop(); }); }, {passive: true});
  TG.reset = () => { cache = null; idx = null; };
  TG.go = (where) => { TG.jump = where; };
  let qt = 0;
  document.addEventListener('input', e => { if (e.target.id !== 'trq') return; const root = document.getElementById('tgRoot'); clearTimeout(qt); qt = setTimeout(() => apply(root), 140); });
  document.addEventListener('change', e => { if (e.target.id !== 'tgJump' || !e.target.value) return; const el = document.getElementById(e.target.value); if (el) el.scrollIntoView({block: 'start'}); e.target.value = ''; });
  function toggleLock(root){ ST.lock = !ST.lock; keep(); root.classList.toggle('tg-lock', !!ST.lock); root.querySelectorAll('.tg.rv').forEach(r => r.classList.remove('rv')); const b = root.querySelector('[data-tglock]'); if (b) b.classList.toggle('on', !!ST.lock); }
  document.addEventListener('click', e => {
    const root = document.getElementById('tgRoot'); if (!root || !root.contains(e.target)) return;
    const b = e.target.closest('[data-tgpart],[data-tglock],[data-tgfind]');
    if (b && b.dataset.tgpart) { ST.part = b.dataset.tgpart; keep(); root.dataset.part = ST.part; root.querySelectorAll('[data-tgpart]').forEach(x => x.classList.toggle('on', x === b)); apply(root); const p = root.querySelector('.tg-bar'); if (p) window.scrollTo({top: Math.max(0, root.offsetTop - 8)}); return; }
    if (b && b.dataset.tglock != null) { toggleLock(root); return; }
    if (b && b.dataset.tgfind) { const q = root.querySelector('#trq'); q.value = b.dataset.tgfind; apply(root); q.scrollIntoView({block: 'nearest'}); return; }
    const r = e.target.closest('.tg'); if (r && root.classList.contains('tg-lock') && !e.target.closest('button')) r.classList.toggle('rv');
  });
  document.addEventListener('keydown', e => {
    const root = document.getElementById('tgRoot'); if (!root || !root.isConnected) return;
    const k = (e.key || '').toLowerCase();
    if ((e.metaKey || e.ctrlKey) && !e.altKey && !e.shiftKey && k === 'f') {
      const q = root.querySelector('#trq'); if (!q || document.activeElement === q) return;
      e.preventDefault(); e.stopImmediatePropagation(); q.focus(); q.select(); return;
    }
    const tg = e.target; if (tg && (/^(INPUT|TEXTAREA|SELECT)$/.test(tg.tagName) || tg.isContentEditable)) { if (k === 'escape' && tg.id === 'trq') tg.blur(); return; }
    if (e.metaKey || e.ctrlKey || e.altKey || document.querySelector('.overlay:not([hidden])')) return;
    if (k === 'l') { e.preventDefault(); e.stopImmediatePropagation(); toggleLock(root); }
    else if (k === 'n' && root.classList.contains('tg-lock')) {
      e.preventDefault(); e.stopImmediatePropagation();
      const top = parseInt(getComputedStyle(root).getPropertyValue('--tg-top')) || 0;
      for (const r of root.querySelectorAll('.tg:not(.rv)')) { if (r.hidden || r.closest('[hidden]')) continue; const bb = r.getBoundingClientRect(); if (bb.bottom < top + 120) continue; r.classList.add('rv'); if (bb.top > innerHeight - 60) r.scrollIntoView({block: 'center'}); break; }
    }
  }, true);

  /* ----- styles ----- */
  const css = `
.tgw [hidden]{display:none!important}
.tgw{--tg-hl:#ffd970;--tg-line:var(--line,#d9dfe9);--tg-surf:var(--surface,#fff);--tg-ink:var(--ink,#14213d);--tg-mut:var(--muted,#5a6479);max-width:1060px;width:100%;min-width:0;box-sizing:border-box;margin:0 auto;display:flex;flex-direction:column;gap:10px}
.tgw>*,.tg-bar>*,.tg-part,.tg-sec{min-width:0}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .tgw{--tg-hl:#6b5212}}
:root[data-theme="dark"] .tgw{--tg-hl:#6b5212}
.tg-top h1{margin:0 0 4px}.tg-top .hint{margin:0}
.tg-hlx,.tg .tc b{background:linear-gradient(transparent 55%,var(--tg-hl) 55%);font-weight:700;color:inherit}
.tg-why{margin-top:6px;font-size:.88rem}.tg-why summary{cursor:pointer;color:var(--tg-mut);font-weight:600}.tg-why ul{margin:6px 0 0;padding-left:20px}.tg-why li{margin:3px 0}
.tg-bar{position:sticky;top:var(--tg-top,0px);z-index:20;background:var(--tg-surf);border:1px solid var(--tg-line);border-radius:12px;padding:8px;display:flex;flex-direction:column;gap:6px;box-shadow:0 4px 14px rgb(0 0 0 / .06)}
#trq{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:9px 12px;border:1px solid var(--tg-line);border-radius:9px;background:var(--bg,var(--tg-surf));color:var(--tg-ink)}
.tg-parts{display:flex;gap:5px;overflow-x:auto;scrollbar-width:none;-webkit-overflow-scrolling:touch}.tg-parts::-webkit-scrollbar{display:none}
.tg-p{flex:none;font:inherit;font-size:.84rem;font-weight:600;padding:5px 10px;border-radius:99px;border:1px solid var(--tg-line);background:var(--tg-surf);color:var(--tg-ink);cursor:pointer;white-space:nowrap}
.tg-p.on{background:var(--accent,#ffc21a);border-color:var(--accent,#ffc21a);color:#14213d}
.tg-row2{display:flex;gap:6px;align-items:center}#tgJump{flex:1;min-width:0;font:inherit;font-size:.86rem;padding:5px 8px;border-radius:8px;border:1px solid var(--tg-line);background:var(--tg-surf);color:var(--tg-ink)}
.tg-cnt{font-size:.78rem;color:var(--tg-mut);white-space:nowrap;font-variant-numeric:tabular-nums}
.tg-h2{margin:14px 0 0;font-size:1.25rem;scroll-margin-top:calc(var(--tg-top,0px) + 130px)}
.tg-sec{scroll-margin-top:calc(var(--tg-top,0px) + 130px);content-visibility:auto;contain-intrinsic-size:auto 900px}
.tg-h3{display:flex;align-items:center;gap:8px;margin:12px 0 6px;font-size:1rem;padding-bottom:4px;border-bottom:2px solid var(--tg-line)}
.tg-h3 .ti{width:20px;height:20px}
.tg-n{margin-left:auto;font-size:.72rem;font-weight:600;color:var(--tg-mut);font-variant-numeric:tabular-nums}
.tg-b{scroll-margin-top:calc(var(--tg-top,0px) + 150px);border:1px solid var(--tg-line);border-radius:11px;background:var(--tg-surf);margin:0 0 8px;overflow:hidden}
.tg-uh{display:flex;align-items:center;gap:8px;padding:7px 10px;background:var(--surface-2,var(--tg-surf));border-bottom:1px solid var(--tg-line)}
.tg-uh .ti{width:22px;height:22px}
.tg-un{font:inherit;font-weight:700;font-size:.95rem;background:none;border:0;padding:0;color:var(--tg-ink);cursor:pointer;text-align:left}.tg-un:hover{text-decoration:underline}
.tg{display:grid;grid-template-columns:26px minmax(0,1.2fr) minmax(0,1fr);gap:4px 10px;align-items:start;padding:7px 10px;border-top:1px solid var(--tg-line);font-size:.92rem;line-height:1.4}
.tg-b>.tg:first-child,.tg-uh+.tg{border-top:0}
.tg-stk{display:grid;grid-template-columns:150px minmax(0,1fr);border-top:1px solid var(--tg-line)}
.tg-uh+.tg-stk,.tg-b>.tg-stk:first-child{border-top:0}
.tg-sth{padding:8px 8px 8px 12px;font-size:.74rem;font-weight:700;letter-spacing:.02em;text-transform:uppercase;color:var(--tg-mut);border-right:3px solid var(--accent,#ffc21a);background:var(--surface-2,transparent);line-height:1.3}
.tg-stb{min-width:0}.tg-stb>.tg:first-child{border-top:0}
.tg .ti{width:22px;height:22px;margin-top:1px;transition:transform .2s}
.tg .ta{color:var(--tg-ink)}.tg .ta::before{content:'→ ';color:var(--tg-mut);font-weight:700}
.tg .ta b{font-weight:700}
.tg.go{background:color-mix(in srgb,var(--accent,#ffc21a) 9%,transparent)}
.tg.catch{padding-left:24px;font-size:.88rem}.tg.catch .ti{width:16px;height:16px;color:#c98a00}
.tg.star{background:color-mix(in srgb,var(--accent,#ffc21a) 14%,transparent)}.tg.star .ti{color:#e0a400}
.tg.trap{box-shadow:inset 3px 0 0 #d9534f}.tg.uk{box-shadow:inset 3px 0 0 #3d6fd8}.tg.hk{box-shadow:inset 3px 0 0 #e0a400}
.tg-t{display:inline-block;font-size:.68rem;font-weight:700;padding:0 6px;border-radius:5px;margin-right:6px;vertical-align:1px;background:color-mix(in srgb,currentColor 12%,transparent)}
.tg-t.trap{color:#c0392b}.tg-t.uk{color:#3d6fd8}.tg-t.hk{color:#b07800}
.tg-al{font-weight:400;font-size:.8rem;color:var(--tg-mut)}
.tg-key{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:4px 12px;font-size:.82rem;color:var(--tg-mut);margin-bottom:8px}
.tg-key span{display:flex;align-items:center;gap:6px}.tg-key b{color:var(--tg-ink);font-weight:600}.tg-key .ti{width:22px;height:22px;flex:none}
.tg-chips{display:flex;flex-wrap:wrap;gap:5px;margin-bottom:6px}
.tg-chip{display:inline-flex;align-items:center;gap:5px;font:inherit;font-size:.8rem;padding:3px 9px 3px 5px;border-radius:99px;border:1px solid var(--tg-line);background:var(--tg-surf);color:var(--tg-ink);cursor:pointer}.tg-chip .ti{width:16px;height:16px}
.tg-foot{margin:14px 0 0;font-size:.78rem}
.ti-heart{color:#e0485a}.ti-lungs{color:#3d8fd8}.ti-gut{color:#c27a3a}.ti-liver{color:#a0522d}.ti-kidney{color:#b5527a}.ti-brain{color:#d46aa0}.ti-eye{color:#2f8f9d}.ti-ear{color:#c08a5a}.ti-skin{color:#d08a6a}.ti-bone,.ti-leg{color:#7b8794}.ti-blood{color:#c62828}.ti-sugar{color:#8e6bd8}.ti-thyroid{color:#d4789a}.ti-breast{color:#e07aa0}.ti-mind{color:#7a5fd0}.ti-nerve{color:#e09a20}
.ti-ecg{color:#d9534f}.ti-scan,.ti-ct,.ti-xray,.ti-mri,.ti-us{color:#3d6fd8}.ti-lab{color:#2a9d8f}.ti-preg{color:#d46aa0}.ti-child{color:#e09a20}.ti-travel{color:#2f8f9d}.ti-drug,.ti-pill{color:#8e6bd8}.ti-fever{color:#e0485a}.ti-old{color:#7b8794}.ti-flag{color:#3d6fd8}.ti-hook{color:#b07800}
.ti-inh,.ti-spray{color:#3d8fd8}.ti-iv,.ti-bag{color:#2a9d8f}.ti-inj,.ti-needle{color:#c0392b}.ti-cream{color:#d08a6a}.ti-drop{color:#2f8f9d}.ti-patch{color:#c27a3a}.ti-proc,.ti-cut{color:#5a6479}.ti-drain{color:#2a9d8f}.ti-shock{color:#e0a400}.ti-device{color:#7a5fd0}.ti-scope{color:#3d6fd8}.ti-laser{color:#d9534f}.ti-ray{color:#e09a20}.ti-air{color:#3d8fd8}.ti-talk{color:#7a5fd0}.ti-law{color:#5a6479}.ti-bed{color:#2a9d8f}.ti-score{color:#5a6479}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .ti-proc,:root:not([data-theme="light"]) .ti-cut,:root:not([data-theme="light"]) .ti-law,:root:not([data-theme="light"]) .ti-score{color:#a7b3c6}}
:root[data-theme="dark"] .ti-proc,:root[data-theme="dark"] .ti-cut,:root[data-theme="dark"] .ti-law,:root[data-theme="dark"] .ti-score{color:#a7b3c6}
.tg-lock .tg .ta{filter:blur(5px);user-select:none;cursor:pointer;transition:filter .2s}
.tg-lock .tg.rv .ta{filter:none;user-select:auto}
.tg-lock .tg{cursor:pointer}
@media (hover:hover){.tg:hover .ti{animation:tgwig .7s ease-in-out}.tg:hover .ti-heart,.tg-uh:hover .ti-heart{animation:tgbeat .8s ease-in-out}.tg:hover .ti-lungs{animation:tgbreathe 1.2s ease-in-out}.tg:hover .ti-shock{animation:tgflash .5s steps(2) 2}}
.tg.rv .ti{animation:tgwig .6s ease-in-out}
@keyframes tgwig{0%,100%{transform:none}35%{transform:scale(1.18) rotate(-7deg)}70%{transform:scale(.96) rotate(5deg)}}
@keyframes tgbeat{0%,100%{transform:scale(1)}20%{transform:scale(1.22)}40%{transform:scale(1)}55%{transform:scale(1.15)}}
@keyframes tgbreathe{0%,100%{transform:scale(1)}50%{transform:scale(1.15,1.08)}}
@keyframes tgflash{50%{opacity:.25}}
@media (prefers-reduced-motion:reduce){.tg .ti,.tg-uh .ti{animation:none!important;transition:none}}
@media (max-width:640px){.tg-stk{grid-template-columns:minmax(0,1fr)}.tg-sth{border-right:0;border-left:3px solid var(--accent,#ffc21a);padding:6px 10px}.tg{grid-template-columns:24px minmax(0,1fr)}.tg .ta{grid-column:2}.tg.catch{padding-left:12px}.tg-key{grid-template-columns:1fr 1fr}}
`;
  const el = document.createElement('style'); el.id = 'tg-css'; el.textContent = css; (document.head || document.documentElement).appendChild(el);
})();
