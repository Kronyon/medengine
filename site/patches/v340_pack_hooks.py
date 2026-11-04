#!/usr/bin/env python3
"""v3.4.0: content-pack hooks in the STUDY engine (applied once to site/study.html; kept as a record).

The same engine now runs two packs: the FFP pack inside study.html and the Step 1 pack that site/build.py
puts into step1.html. With no pack declared nothing changes for STUDY.

  PACK          window.MEDENGINE_PACK, set by the page before the engine runs ({id: 'study'} if absent)
  HIDE_NAV      views a pack switches off (sidebar and home buttons)
  EXT_VIEWS     extra views a pack registers (route.view -> render function)
  window.ME     a small API for pack add-ons, and window.ME_EXT, a queue of add-ons run before the first render
  arrows        roles per variable (p primary, k knock-on, c compensation) and 'change the film' flips (fl)
"""
import pathlib, re

F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
assert 'window.MEDENGINE_PACK' not in s, 'already applied'


def must(old, new, count=1):
    global s
    n = s.count(old)
    assert n == count, (n, old[:90])
    s = s.replace(old, new)


must("const D = JSON.parse(document.getElementById('qqdata').textContent);\n",
     "const D = JSON.parse(document.getElementById('qqdata').textContent);\n"
     "const PACK = window.MEDENGINE_PACK || {id: 'study'}, HIDE_NAV = new Set(PACK.hideNav || []), EXT_VIEWS = {}, EXT_NAV = [], EXT = {};\n")

# sidebar: hidden views drop out, pack views slot in after the dashboard and at the end
must("  function qb(v, ico, label, n){ return '<button class=\"qbtn'",
     "  function qb(v, ico, label, n){ if (HIDE_NAV.has(v)) return ''; return '<button class=\"qbtn'")
must("  h += qb('home', '🏠', 'Dashboard') + qb('leaderboard',",
     "  const extNav = pos => EXT_NAV.filter(x => x[0] === pos).map(x => qb(x[1], x[2], x[3], x[4] ? x[4]() : null)).join('');\n"
     "  h += qb('home', '🏠', 'Dashboard') + extNav('top') + qb('leaderboard',")
must("  h += '</div>' + jumpHtml() + '<h4>'", "  h += extNav('end') + '</div>' + jumpHtml() + '<h4>'")

must("  else if (route.view === 'leaderboard' && typeof viewLeaderboard === 'function') viewLeaderboard(m);",
     "  else if (EXT_VIEWS[route.view]) EXT_VIEWS[route.view](m);\n"
     "  else if (route.view === 'leaderboard' && typeof viewLeaderboard === 'function') viewLeaderboard(m);")

# home: a pack can add a panel and hide buttons for views it switched off
must("  h += '<div class=\"tiles\">' + '<div class=\"tile shop-tile\"",
     "  if (EXT.homeTop) h += EXT.homeTop();\n  h += '<div class=\"tiles\">' + '<div class=\"tile shop-tile\"")
must("""twice for the browser\\'s own find.</p></div>';\n  return h;""",
     """twice for the browser\\'s own find.</p></div>';\n"""
     """  if (HIDE_NAV.size) h = h.replace(/<button class="btn" data-go="([a-z]+)">[^<]*<\\/button>/g, (x, v) => HIDE_NAV.has(v) ? '' : x);\n  return h;""")

# condition page: pack panel at the top; a pack can fill topics that have no notes yet; OSCE link only where OSCE exists
must("  h += '<div class=\"srcs\"><a class=\"src\" style=\"text-decoration:none;color:var(--ink)\" href=\"osce.html#u' + u.i + '\">🩺 medengine-OSCE pack and stations for this ILO ↗</a></div>';",
     "  if (!PACK.noOsce) h += '<div class=\"srcs\"><a class=\"src\" style=\"text-decoration:none;color:var(--ink)\" href=\"osce.html#u' + u.i + '\">🩺 medengine-OSCE pack and stations for this ILO ↗</a></div>';\n"
     "  if (EXT.unitTop) h += EXT.unitTop(u);")
must("  if (!u.refs.length) { m.innerHTML = h + '<div class=\"panel empty\">Nothing in the Quack Quack notes",
     "  if (!u.refs.length && EXT.unitEmpty) { m.innerHTML = h + EXT.unitEmpty(u) + '</div>'; return; }\n"
     "  if (!u.refs.length) { m.innerHTML = h + '<div class=\"panel empty\">Nothing in the Quack Quack notes")

# ---- arrows: a key may point at a flip ('7~0'); roles colour the domino chain; flips change one feature of the film ----
must("function arHtml(i){\n  const a = AR[i]; if (!a) return '';\n",
     "const ARROLE = {p: ['🔴', 'Primary insult'], k: ['🟡', 'Knock-on'], c: ['🟢', 'Compensation']};\n"
     "function arItem(key){\n"
     "  const [i, f] = String(key).split('~'), a = AR[+i]; if (!a) return null; if (f == null) return a;\n"
     "  const x = (a.fl || [])[+f]; return x ? Object.assign({}, a, {id: a.id + '~' + f, s: x.s, v: x.v, r: x.r || a.r, k: x.k, m: x.m || [], uk: x.uk || '', fl: [], flip: x.t}) : null;\n"
     "}\n"
     "function arHtml(i){\n  const a = arItem(i); if (!a) return '';\n")
must("""'<div class="ar-s">' + fmtRich(a.s) + '</div><div class="ar-rows">'""",
     """(a.flip ? '<div class="ar-flip">🔀 ' + esc(a.flip) + '</div>' : '') + '<div class="ar-s">' + fmtRich(a.s) + '</div><div class="ar-rows">'""")
must("  const [i, j, sy] = t.dataset.arp.split('|'), a = AR[+i], box = t.closest('.ar'), row = t.closest('.ar-r');",
     "  const [i, j, sy] = t.dataset.arp.split('|'), a = arItem(i), box = t.closest('.ar'), row = t.closest('.ar-r');")
must("""  k.innerHTML = '<div class="ar-sc' + (all ? ' ok' : '') + '">' + right + ' / ' + n + (all ? ' · nailed it' : ' · read the why') + '</div><div class="ar-key">🔑 ' + fmtRich(a.k) + '</div>' +""",
     """  if (a.r) rows.forEach((r, j2) => { const ro = ARROLE[a.r[j2]]; if (ro) { r.classList.add('ar-' + a.r[j2]); const n0 = $('.ar-n', r); if (n0 && !$('.ar-role', r)) n0.insertAdjacentHTML('beforeend', ' <span class="ar-role" title="' + ro[1] + '">' + ro[0] + '</span>'); } });\n"""
     """  k.innerHTML = '<div class="ar-sc' + (all ? ' ok' : '') + '">' + right + ' / ' + n + (all ? ' · nailed it' : ' · read the why') + '</div><div class="ar-key">🔑 ' + fmtRich(a.k) + '</div>' +\n"""
     """    (a.r ? '<div class="ar-leg">' + Object.entries(ARROLE).filter(([c]) => a.r.includes(c)).map(([c, v]) => '<span>' + v[0] + ' ' + v[1] + '</span>').join('') + '</div>' : '') +""")
must("""  k.hidden = false; $('[data-arreset]', box).hidden = false;\n}""",
     """  if ((a.fl || []).length) k.insertAdjacentHTML('beforeend', '<div class="ar-fls">' + a.fl.map((x, f) => '<button class="btn sm ar-flb" data-arflip="' + i + '~' + f + '">🔀 ' + esc(x.t) + '</button>').join('') + '</div>');\n"""
     """  k.hidden = false; $('[data-arreset]', box).hidden = false;\n}\n"""
     """document.addEventListener('click', e => {\n"""
     """  const b = e.target.closest && e.target.closest('[data-arflip]'); if (!b) return;\n"""
     """  const box = b.closest('.ar'), key = b.dataset.arflip, open = box.parentNode.querySelector('.ar[data-ari="' + key + '"]');\n"""
     """  if (open) { open.scrollIntoView({block: 'nearest', behavior: 'smooth'}); return; }\n"""
     """  box.insertAdjacentHTML('afterend', arHtml(key)); b.classList.add('on');\n"""
     """});""")
must("""<div class="ar" data-ari="' + i + '">""", """<div class="ar' + (a.flip ? ' ar-isflip' : '') + '" data-ari="' + i + '">""")

# styles for roles and flips
must(".ar-sc.ok{color:var(--good)}",
     ".ar-sc.ok{color:var(--good)}\n"
     ".ar-role{font-size:.8em;margin-left:4px}\n.ar-leg{display:flex;flex-wrap:wrap;gap:10px;font-size:.78rem;color:var(--muted);margin:6px 0}\n"
     ".ar-fls{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}\n.ar-flb.on{opacity:.6}\n"
     ".ar-isflip{border-left:3px solid var(--accent,#7c5cff);margin-left:10px}\n.ar-flip{font-weight:700;font-size:.85rem;margin:4px 0}")

# ---- API for pack add-ons, run before the first render ----
must("\ngo(fromHash(), false);\n})();",
     "\nwindow.ME = {PACK, D, UNITS, WEEKS, EXT, esc, toast, get S(){ return S; }, get route(){ return route; },\n"
     "  save: () => save(), go: (r, p) => go(r, p), render: () => render(), fmtRich: t => fmtRich(t), addXp: n => addXp(n),\n"
     "  hqItem: id => hqItem(id), hqAll: () => hqAll(), hqNewRun: (l, t, c) => hqNewRun(l, t, c), arHtml: k => arHtml(k), huntHtml: ids => huntHtml(ids),\n"
     "  view: (name, fn) => { EXT_VIEWS[name] = fn; }, nav: (pos, v, ico, label, n) => { EXT_NAV.push([pos, v, ico, label, n]); }};\n"
     "(window.ME_EXT || []).forEach(f => { try { f(window.ME); } catch (e) { console.error('pack add-on failed', e); } });\n"
     "go(fromHash(), false);\n})();")

F.write_text(s, encoding='utf-8')
print('v3.4.0 pack hooks applied')
