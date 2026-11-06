#!/usr/bin/env python3
"""v3.6.15 UI: a calmer sidebar and a new dashboard (inspired by Passmedicine, Quesmed, UWorld and Bootcamp).
Sidebar: Practise (Dashboard, Hammer SBAs, Triggers, Posters, Why it happens, First move vs cure), then Systems &
presentations with the ILO weeks, then everything else folded under "Other" (opens by itself when you are on one of them).
Dashboard: greeting, four stat cards, Continue card, activity heatmap, six shortcuts, three recommended weeks, and the
weeks as compact rows with two progress bars. No button wall."""
import pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')


def must(old, new, n=1):
    global s
    assert s.count(old) == n, ('found %d' % s.count(old), old[:100])
    s = s.replace(old, new)


# ------------------------------------------------------------------ sidebar
OLD_Q = s[s.index("  h += qb('home', '🏠', 'Dashboard') + extNav('top') + qb('leaderboard'"):]
OLD_Q = OLD_Q[:OLD_Q.index('\n') + 1]
assert "qb('vault', '📋', 'Screenshot vault'" in OLD_Q
must(OLD_Q, """  h += qb('home', '🏠', 'Dashboard') + extNav('top') + qb('hammer', '🔨', 'Hammer SBAs', hqCount()) + qb('triggers', '🧲', 'Triggers', trgCount()) + qb('posters', '🗺️', 'Posters', (D.master || []).length + new Set(Object.values(D.snap || {}).map(x => x.n)).size) + qb('why', '🧬', 'Why it happens', ROOTS.length) + qb('act', '⚡', 'First move vs cure', ACTS.length);
  const other = qb('misses', '🔥', 'My misses', msLoad().items.filter(x => !x.fixed).length || null) + qb('weak', '♻️', 'Weak spots', weakN) + qb('sprint', '⚡', 'Sprint mode') + qb('leaderboard', '🏆', 'Leaderboard') + qb('sketchy', '🎬', 'Visual scenes', new Set(Object.values(D.snap || {}).map(x => x.n)).size) + qb('remix', '🔄', 'Remix a missed question') + qb('sniper', '🎯', 'Blind clincher sniper') + qb('fw', '🧠', 'Frameworks · ↕ · 🔎', FW.length) + qb('all', '📖', 'All ILO notes on one page') + qb('gloss', '🔤', 'Abbreviations', GLOSS.length) + qb('visual', '👁️', 'Visual showdowns', MEV.SD.length) + qb('jargon', '🔺', 'Jargon decoder', JG.length) + qb('vault', '📋', 'Screenshot vault', shotsCache ? shotsCache.length : 0) + extNav('end');
  const otherOn = /data-go="([a-z]+)"/g, onOther = [...other.matchAll(otherOn)].some(m => m[1] === route.view);
""")
must("  h += extNav('end') + '</div>' + jumpHtml() + '<h4>'",
     "  h += '</div><div class=\"side-sec\">Systems &amp; presentations</div>' + jumpHtml() + '<h4>'")
must("""  $('#side').innerHTML = h;
  function qb(v, ico, label, n){""",
     """  h += '<details class="side-other"' + (S.set.navOther || onOther ? ' open' : '') + '><summary><span>🧰</span>Other<span class="so-hint">misses, sprint, leaderboard, tools</span></summary><div class="quick">' + other + '</div></details>';
  $('#side').innerHTML = '<div class="side-sec first">Practise</div>' + h;
  function qb(v, ico, label, n){""")
must("""<summary>🗂 Systems &amp; presentations' + (sys ? ' · ' + esc(MEV.sysLabel(sys)) : '') + '</summary>""",
     """<summary>🗂 Filter by system or jump to…' + (sys ? ' · ' + esc(MEV.sysLabel(sys)) : '') + '</summary>""")

# ------------------------------------------------------------------ dashboard
a = s.index('function viewHome(){\n'); b = s.index('\nfunction unitPages(u)', a)
assert 'Your ILO weeks' in s[a:b]
HOME = r"""function viewHome(){
  const st1 = PACK.id === 'step1', real = UNITS.filter(u => u.refs.length);
  const touched = real.filter(u => unitStatus(u)).length, mastered = real.filter(u => unitStatus(u) === 2).length;
  const all = hqAll(), hs = hqPctStats(all), todayN = (S.days || {})[today()] || 0, streak = dayStreak();
  const fmt = n => Number(n || 0).toLocaleString('en-GB'), hid = v => HIDE_NAV.has(v);
  const hr = new Date().getHours(), greet = hr < 12 ? 'Good morning' : hr < 18 ? 'Good afternoon' : 'Good evening';
  const last = S.last && UNITS[S.last.u];
  let h = '<div class="wrap db">';
  /* 1. greeting */
  h += '<div class="db-head"><div><h1>' + greet + '</h1><p class="db-sub">' + real.length + (st1 ? ' topics · ' : ' ILO conditions · ') + WEEKS.length + (st1 ? ' First Aid chapters · ' : ' weeks · ') + fmt(all.length) + ' questions</p></div>'
    + '<div class="db-head-act"><button class="btn ghost sm" data-rand="1">🎲 Random ' + (st1 ? 'topic' : 'condition') + '</button>' + (hid('sprint') ? '' : '<button class="btn ghost sm" data-go="sprint">⚡ 5-min sprint</button>') + '</div></div>';
  if (EXT.homeTop) h += EXT.homeTop();
  /* 2. four numbers */
  const stat = (ic, l, v, sub, tone) => '<div class="db-stat' + (tone ? ' ' + tone : '') + '"><div><div class="l">' + l + '</div><div class="v">' + v + '</div><div class="s">' + sub + '</div></div><span class="ic" aria-hidden="true">' + ic + '</span></div>';
  h += '<div class="db-stats">'
    + stat('🎯', 'Question score', hs.done ? hs.pct + '%' : '–', hs.done ? fmt(hs.right) + ' right of ' + fmt(hs.done) : 'Answer one to start', hs.cls)
    + stat('🔨', 'Bank used', (() => { const p = hs.total ? hs.done / hs.total * 100 : 0; return (p && p < 1 ? p.toFixed(1) : Math.round(p)) + '%'; })(), fmt(hs.done) + ' of ' + fmt(hs.total) + ' questions')
    + stat('🔥', 'Streak', streak + (streak === 1 ? ' day' : ' days'), todayN ? todayN + ' done today' : 'Nothing yet today')
    + stat('🏅', 'Mastered', mastered + ' / ' + real.length, touched + (st1 ? ' topics' : ' conditions') + ' touched') + '</div>';
  /* 3. continue + activity */
  const runs = hqRuns().filter(r => r.ids && r.ids.length).slice().sort((x, y) => (y.ts || 0) - (x.ts || 0));
  const live = runs.find(r => hqRunScore(r).done < r.ids.length);
  const missN = all.filter(it => it.t !== 'm' && it.t !== 'o' && (hqStat(it.id) || [])[2] === 0).length;
  h += '<div class="db-row"><section class="db-card db-cont"><h2>Continue</h2>';
  if (live) {
    const sc = hqRunScore(live), n = live.ids.length;
    h += '<p class="db-cont-t">' + esc(live.lbl || '🔀 Mixed run') + '</p><p class="db-cont-m">Question ' + Math.min((live.i || 0) + 1, n) + ' of ' + n + ' · ' + sc.done + ' answered' + (sc.done ? ' · ' + Math.round(sc.pct) + '% so far' : '') + ' · ' + hqAgo(live.ts) + '</p>'
      + '<div class="db-bar"><i style="width:' + Math.round(sc.done / n * 100) + '%"></i></div>'
      + '<div class="db-btns"><button class="btn primary" data-hqresume="' + esc(live.rid) + '">▶ Resume</button><button class="btn" data-dbstart="20">New 20 questions</button>';
  } else {
    h += '<p class="db-cont-t">Start a block of 20</p><p class="db-cont-m">Mixed single best answers from every ' + (st1 ? 'chapter' : 'ILO week') + '. Your place, answers and highlights are saved as you go.</p>'
      + '<div class="db-btns"><button class="btn primary" data-dbstart="20">▶ Start 20 questions</button><button class="btn" data-go="hammer">Choose topics</button>';
  }
  if (missN) h += '<button class="btn ghost" data-hqtgt="srcm:u">🔥 Redo ' + missN + ' missed</button>';
  h += '</div>';
  if (last) h += '<div class="db-last"><span>📖 Last ' + (st1 ? 'topic' : 'condition') + ': <b>' + esc(last.name) + '</b></span><button class="linkbtn" data-u="' + last.i + '" data-mode="' + esc(S.last.mode || 'fill') + '">Open →</button></div>';
  h += '</section>' + dbHeat() + '</div>';
  /* 4. six shortcuts */
  const posters = (D.master || []).length + new Set(Object.values(D.snap || {}).map(x => x.n)).size, mN = msLoad().items.filter(x => !x.fixed).length;
  const acts = [['hammer', '🔨', 'Hammer SBAs', fmt(all.length) + ' questions, every ' + (st1 ? 'topic' : 'ILO')], ['triggers', '🧲', 'Triggers', fmt(trgCount() || 0) + ' one-line scenes'], ['posters', '🗺️', 'Posters', posters + ' one-page maps'],
    ['why', '🧬', 'Why it happens', ROOTS.length + ' mechanisms'], ['act', '⚡', 'First move vs cure', ACTS.length + ' emergencies'], mN ? ['misses', '🔥', 'My misses', mN + ' still to fix'] : ['weak', '♻️', 'Weak spots', Object.keys(S.weak).length + ' queued']].filter(x => !hid(x[0]));
  h += '<div class="db-acts">' + acts.map(([v, ic, t, sub]) => '<button class="db-act" data-go="' + v + '"><span class="ic" aria-hidden="true">' + ic + '</span><span class="tx"><b>' + t + '</b><span class="s">' + sub + '</span></span><span class="chev" aria-hidden="true">›</span></button>').join('') + '</div>';
  /* 5. recommended next: lowest scores first, then weeks not started */
  const wk = WEEKS.map(w => ({w, st: hqWeekStats(w.id)})).filter(x => x.st.total);
  const rec = wk.filter(x => x.st.done >= 5).sort((p, q) => p.st.pct - q.st.pct).slice(0, 3);
  wk.filter(x => !x.st.done).forEach(x => { if (rec.length < 3) rec.push(x); });
  if (rec.length) h += '<section class="db-card db-rec"><h2>Recommended next</h2>' + rec.map(({w, st}) => '<div class="db-rec-row" style="--h:' + wkHue[w.id] + '"><span class="nm"><span class="dot"></span>' + esc(w.name) + '</span>'
    + '<span class="sc">' + (st.done ? '<span class="db-bar sm"><i class="' + st.cls + '" style="width:' + st.pct + '%"></i></span><b class="' + st.cls + '">' + st.pct + '%</b>' : '<span class="hint">Not started</span>') + '</span>'
    + '<span class="an">' + st.done + ' / ' + st.total + '</span><button class="btn sm" data-hqtgt="wk:' + esc(w.id) + '">Practise</button></div>').join('') + '</section>';
  /* 6. the weeks */
  h += '<div class="db-wh"><h2>' + (st1 ? 'First Aid chapters' : 'Your ILO weeks') + '</h2><span class="hint">Bars: questions answered · ' + (st1 ? 'topics' : 'conditions') + ' covered</span></div><div class="db-weeks">';
  WEEKS.forEach(w => {
    const us = unitsOf(w.id), st = hqWeekStats(w.id), cov = Math.round(wkProgress(w.id) * 100);
    h += '<button class="db-wk" style="--h:' + wkHue[w.id] + '" data-wkopen="' + w.id + '"><span class="dot"></span><span class="nm">' + esc(w.name) + '</span><span class="pc ' + (st.done ? st.cls : '') + '">' + (st.done ? st.pct + '%' : '') + '</span>'
      + '<span class="bars"><span><span class="db-bar sm"><i style="width:' + (st.total ? Math.round(st.done / st.total * 100) : 0) + '%"></i></span><span class="bl">' + st.done + ' / ' + st.total + ' questions</span></span>'
      + '<span><span class="db-bar sm cov"><i style="width:' + cov + '%"></i></span><span class="bl">' + us.length + (st1 ? ' topics' : ' conditions') + '</span></span></span></button>';
  });
  h += '</div>' + homeSysHtml() + '<p class="hint db-foot">Press <span class="kbd">/</span> or <span class="kbd">⌘F</span> to search every condition, every line of the notes and the posters.</p></div>';
  return h;
}
function dbHeat(){
  const days = S.days || {}, now = new Date(), dow = (now.getDay() + 6) % 7, W = 18;
  const start = new Date(now); start.setDate(now.getDate() - dow - 7 * (W - 1));
  let cells = '', active = 0;
  for (let i = 0; i < W * 7; i++) {
    const d = new Date(start); d.setDate(start.getDate() + i);
    const k = d.toISOString().slice(0, 10), n = days[k] || 0, fut = d > now;
    if (n && !fut) active++;
    cells += '<i class="l' + (n === 0 ? 0 : n < 5 ? 1 : n < 15 ? 2 : n < 40 ? 3 : 4) + (fut ? ' fut' : '') + '" title="' + k + ': ' + n + '"></i>';
  }
  const ks = Object.keys(days).filter(k => days[k]).sort(); let best = 0, run = 0, prev = null;
  ks.forEach(k => { const t = Date.parse(k); run = prev != null && t - prev === 864e5 ? run + 1 : 1; best = Math.max(best, run); prev = t; });
  return '<section class="db-card db-act-card"><h2>Activity · last ' + W + ' weeks</h2><div class="db-heatw"><span class="db-dl" aria-hidden="true"><b>M</b><b></b><b>W</b><b></b><b>F</b><b></b><b>S</b></span><div class="db-heat" role="img" aria-label="Activity heatmap">' + cells + '</div></div>'
    + '<div class="db-heatk"><span>' + active + ' active days · best streak ' + best + '</span><span class="db-leg">Less <i class="l0"></i><i class="l1"></i><i class="l2"></i><i class="l3"></i><i class="l4"></i> More</span></div></section>';
}
document.addEventListener('click', e => {
  const t = e.target.closest && e.target.closest('[data-dbstart]'); if (!t) return;
  e.preventDefault(); go({view: 'hammer'}); hqSess = null; hqStart(+t.dataset.dbstart || 20);
});
document.addEventListener('click', e => { const sm = e.target.closest && e.target.closest('.side-other>summary'); if (sm) { S.set.navOther = !sm.parentElement.open; save(); } });"""
s = s[:a] + HOME + s[b:]

CSS = """
/* v3.6.15 sidebar + dashboard */
.side-sec{font:600 .66rem var(--f-mono);letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin:18px 10px 6px}
.side-sec.first{margin-top:2px}
.side .jump{margin:4px 0 2px}
.side-other{margin-top:16px;border-top:1px solid var(--line);padding-top:8px}
.side-other>summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:8px 10px;border-radius:8px;font-size:.92rem;font-weight:600}
.side-other>summary::-webkit-details-marker{display:none}
.side-other>summary:hover{background:var(--surface-2)}
.side-other>summary::after{content:'▸';margin-left:auto;color:var(--muted);transition:transform .15s}
.side-other[open]>summary::after{transform:rotate(90deg)}
.side-other .so-hint{font-size:.72rem;font-weight:400;color:var(--muted);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.side-other[open] .so-hint{display:none}
.side-other .quick{padding-top:4px}
.db{display:flex;flex-direction:column;gap:16px;max-width:1180px}
.db h1{margin:0;font-size:clamp(1.45rem,2.6vw,1.95rem);letter-spacing:-.01em}
.db-head{display:flex;align-items:flex-end;justify-content:space-between;gap:12px;flex-wrap:wrap}
.db-sub{margin:4px 0 0;color:var(--muted);font-size:.9rem}
.db-head-act{display:flex;gap:8px;flex-wrap:wrap}
.db-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px}
.db-stat{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:14px 16px;display:flex;justify-content:space-between;align-items:flex-start;gap:10px;min-width:0}
.db-stat .l{font-size:.8rem;color:var(--muted);font-weight:600}
.db-stat .v{font:700 1.55rem/1.15 var(--f-display);margin-top:4px;white-space:nowrap}
.db-stat .s{font-size:.78rem;color:var(--muted);margin-top:2px}
.db-stat .ic{width:38px;height:38px;border-radius:10px;display:grid;place-items:center;background:var(--surface-2);font-size:1.05rem;flex:none}
.db-stat.good .v{color:var(--good)}.db-stat.mid .v{color:var(--warn)}.db-stat.low .v{color:var(--bad)}
.db-row{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,1fr);gap:12px}
.db-card{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:16px 18px;min-width:0}
.db-card h2,.db-wh h2{font:600 .72rem var(--f-mono);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 10px}
.db-cont-t{font:700 1.15rem/1.3 var(--f-display);margin:0}
.db-cont-m{color:var(--muted);font-size:.86rem;margin:4px 0 12px}
.db-bar{display:block;height:6px;border-radius:9px;background:var(--line);overflow:hidden}
.db-bar.sm{height:4px}
.db-bar i{display:block;height:100%;border-radius:9px;background:var(--focus)}
.db-bar i.good,.db-bar.cov i{background:var(--good)}.db-bar i.mid{background:var(--warn)}.db-bar i.low{background:var(--bad)}
.db-btns{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}
.db-last{display:flex;justify-content:space-between;align-items:center;gap:10px;margin-top:14px;padding-top:12px;border-top:1px solid var(--line);font-size:.86rem;color:var(--muted)}
.db-last b{color:var(--ink)}
.linkbtn{border:0;background:none;color:var(--focus);font-weight:700;cursor:pointer;padding:2px 4px;white-space:nowrap}
.db-act-card{--c:14px}.db-heatw{display:flex;gap:6px;overflow-x:auto;padding-bottom:2px}
.db-dl{display:grid;grid-template-rows:repeat(7,var(--c));gap:3px;font:600 .6rem var(--f-mono);color:var(--muted)}
.db-dl b{line-height:var(--c);font-weight:600}
.db-heat{display:grid;grid-template-rows:repeat(7,var(--c));grid-auto-flow:column;grid-auto-columns:var(--c);gap:3px}
.db-heat i{width:var(--c);height:var(--c)}.db-heat i,.db-leg i{display:inline-block;width:11px;height:11px;border-radius:3px;background:var(--surface-2);box-shadow:inset 0 0 0 1px color-mix(in oklab,var(--line) 70%,transparent)}
.db-heat i.l1,.db-leg i.l1{background:color-mix(in oklab,var(--good) 28%,var(--surface-2))}
.db-heat i.l2,.db-leg i.l2{background:color-mix(in oklab,var(--good) 52%,var(--surface-2))}
.db-heat i.l3,.db-leg i.l3{background:color-mix(in oklab,var(--good) 76%,var(--surface-2))}
.db-heat i.l4,.db-leg i.l4{background:var(--good)}
.db-heat i.fut{visibility:hidden}
.db-heatk{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin-top:10px;font-size:.78rem;color:var(--muted)}
.db-leg{display:inline-flex;align-items:center;gap:3px}
.db-acts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}
.db-act{display:flex;align-items:center;gap:12px;text-align:left;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:12px 14px;color:var(--ink);cursor:pointer;min-width:0;transition:border-color .15s,transform .15s}
.db-act:hover{border-color:var(--accent);transform:translateY(-1px)}
.db-act .ic{width:40px;height:40px;border-radius:10px;background:var(--surface-2);display:grid;place-items:center;font-size:1.2rem;flex:none}
.db-act .tx{min-width:0}
.db-act b{display:block;font-size:.95rem}
.db-act .s{display:block;font-size:.8rem;color:var(--muted)}
.db-act .chev{margin-left:auto;color:var(--muted);font-size:1.3rem;line-height:1}
.db-rec-row{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr) auto auto;gap:14px;align-items:center;padding:10px 0;border-top:1px solid var(--line);font-size:.9rem}
.db-rec-row:first-of-type{border-top:0;padding-top:2px}
.db-rec-row .nm{display:flex;align-items:center;gap:8px;font-weight:600;min-width:0}
.db-rec-row .sc{display:flex;align-items:center;gap:8px}
.db-rec-row .sc .db-bar{flex:1}
.db-rec-row .an{font:500 .78rem var(--f-mono);color:var(--muted);white-space:nowrap}
.db-rec-row b.good,.db-wk .pc.good{color:var(--good)}.db-rec-row b.mid,.db-wk .pc.mid{color:var(--warn)}.db-rec-row b.low,.db-wk .pc.low{color:var(--bad)}
.db .dot{width:10px;height:10px;border-radius:3px;background:hsl(var(--h) 70% var(--chip-l));flex:none}
.db-wh{display:flex;justify-content:space-between;align-items:baseline;gap:10px;flex-wrap:wrap;margin-top:4px}
.db-wh h2{margin:0}
.db-weeks{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
.db-wk{display:grid;grid-template-columns:auto minmax(0,1fr) auto;gap:6px 10px;align-items:center;text-align:left;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:11px 14px;color:var(--ink);cursor:pointer;min-width:0;transition:border-color .15s}
.db-wk:hover{border-color:hsl(var(--h) 70% var(--chip-l))}
.db-wk .nm{font-weight:700;font-size:.92rem;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.db-wk .pc{font:700 .8rem var(--f-mono)}
.db-wk .bars{grid-column:2/4;display:grid;grid-template-columns:1fr 1fr;gap:12px}
.db-wk .bars>span{display:flex;flex-direction:column;gap:4px;min-width:0}
.db-wk .bl{font-size:.72rem;color:var(--muted)}
.db .sysrow{margin-top:2px}
.db-foot{margin:0}
@media (max-width:1100px){.db-stats{grid-template-columns:repeat(2,minmax(0,1fr))}.db-row{grid-template-columns:1fr}}
@media (max-width:760px){.db-acts{grid-template-columns:repeat(2,minmax(0,1fr))}.db-weeks{grid-template-columns:1fr}.db-rec-row{grid-template-columns:minmax(0,1fr) auto;gap:6px 10px}.db-rec-row .sc{grid-column:1/2}.db-rec-row .an{grid-row:1;grid-column:2}.db-rec-row .btn{grid-column:2;grid-row:2}}
@media (max-width:480px){.db-act-card{--c:11px}.db-act{padding:10px;gap:9px}.db-act .ic{width:32px;height:32px;font-size:1rem}.db-act .chev{display:none}.db-act b{font-size:.88rem}.db-act .s{font-size:.74rem}.db-stat{padding:12px}.db-stat .v{font-size:1.3rem}.db-stat .ic{display:none}}
"""
must(".tm-score{margin:8px 0 0;font-size:.9rem}\n", ".tm-score{margin:8px 0 0;font-size:.9rem}\n" + CSS)

# every answered question counts towards the day's activity (streak and heatmap), not only XP events
must("function hqMark(id, ok){ S.hq = S.hq || {}; const r = S.hq[id] || [0, 0, 0];", "function hqMark(id, ok){ S.hq = S.hq || {}; S.days = S.days || {}; S.days[today()] = (S.days[today()] || 0) + 1; const r = S.hq[id] || [0, 0, 0];")
F.write_text(s, encoding='utf-8'); print('v3615 ui ok')
