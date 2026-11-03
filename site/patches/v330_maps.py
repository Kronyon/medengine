#!/usr/bin/env python3
"""v3.3.0 thought maps in site/study.html (applied once; kept as a record).

v3.2.0 padded every map to 4 "if instead" flips. About 1 in 10 of the added flips were wrong
(for example "gliclazide if a long fast with risk of low sugar"), and 1,383 of them were not
flips at all but reasons an option is wrong, shown under "change one thing and…".

  - the 2,122 curated maps go back to their hand-written source (study/snap/maps), re-validated
    against today's stems and options (cues verbatim, flips point at real wrong options)
  - v3.2.0's "✗ …" reasons are kept, as a separate ❌ "Why not the others" list (tm.x)
  - the 200 new MS AKT 2026 maps: symbols turned into words, dashes and brackets removed,
    flips dropped where the question asks which feature or finding (a flip makes no sense there)
"""
import json, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SITE.parent / 'study' / 'snap'))
import maps  # noqa: E402

F = SITE / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
M = maps.parse()
stats = {'restored': 0, 'why_not': 0, 'new_cleaned': 0, 'new_flips_dropped': 0, 'errors': []}


def tidy(s):
    """light touch for prose reasons: no long dashes, keep everything else"""
    s = re.sub(r'(\d)\s*[–—]\s*(\d)', r'\1 to \2', s)
    s = re.sub(r'\s*[–—]\s*', ', ', s).strip(' ,')
    return s[:1].upper() + s[1:] if s else s


def words(s):
    s = re.sub(r'\s*→\s*', ', so ', s)
    s = re.sub(r'\s+\+\s+', ' and ', s)
    s = re.sub(r'\s+−\s+', ' without ', s)
    s = re.sub(r'\s+-\s+', ', ', s)
    s = re.sub(r'\s+=\s+', ': ', s)
    s = re.sub(r'(\d)\s*[–—]\s*(\d)', r'\1 to \2', s)
    s = re.sub(r'\s*[–—]\s*', ', ', s)
    s = re.sub(r'\s*\(\s*', ', ', s).replace(')', '')
    s = re.sub(r',\s*,', ',', s)
    s = re.sub(r'\s{2,}', ' ', s).strip(' ,')
    return s[:1].upper() + s[1:] if s else s


FEATURE_Q = re.compile(r'\b(which|what) (feature|finding|sign|aspect|factor|history|part of)|red flag|most supports|best supports', re.I)

for k in ('hq', 'mock', 'off'):
    for q in D[k]['q']:
        tm = q.get('tm') or {}
        opts = [maps.norm(o) for o in q['o']]
        if q['id'] in M:
            mp = M[q['id']]
            bad = maps.problems(q, mp)
            if bad:
                stats['errors'] += [q['id'] + ': ' + b for b in bad]
                continue
            why = []
            for c, i in tm.get('f', []):
                s = str(c).strip()
                if re.match(r'^[✗❌]', s) and i != q['a']:
                    why.append([i, tidy(re.sub(r'^[✗❌]\s*', '', s))])
            new = {'c': mp['c'], 'm': mp['m'], 'g': mp['g'], 'f': [[c, opts.index(maps.norm(t))] for c, t in mp['f']]}
            if why:
                new['x'] = sorted(why)
                stats['why_not'] += len(why)
            if tm.get('bt'):
                new['bt'] = tm['bt']
            q['tm'] = new
            stats['restored'] += 1
        elif q['id'].startswith('o-mla26') and tm:
            tm['m'] = words(tm['m'])
            tm['g'] = words(tm['g'])
            if FEATURE_Q.search(q.get('ql', '')):
                stats['new_flips_dropped'] += len(tm['f'])
                tm['f'] = []
            else:
                tm['f'] = [[words(c), i] for c, i in tm['f'] if i != q['a']]
            mp = {'c': tm['c'], 'm': tm['m'], 'g': tm['g'], 'f': [[c, q['o'][i]] for c, i in tm['f']]}
            bad = [b for b in maps.problems(q, mp) if b != 'at most 3 flips']
            if bad:
                stats['errors'] += [q['id'] + ': ' + b for b in bad]
            stats['new_cleaned'] += 1

if stats['errors']:
    raise SystemExit('thought maps:\n' + '\n'.join(stats['errors'][:40]))

blob = json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
page = page[:mt.start(2)] + blob + page[mt.end(2):]

# UI: flips are only "if instead"; reasons get their own list
old = """        const s = String(c || '').trim(), isWhy = /^[✗❌]/.test(s);
        return '<div class="tm-f"><span class="tm-fa" aria-hidden="true">↳ 🔀</span><span>' + (isWhy ? esc(s) : 'If ' + esc(s)) + ' <span class="tm-fx">➔</span> <b>' + L[i] + '. ' + esc(it.o[i]) + '</b></span></div>';
      }).join('') + '</div>';"""
new = """        const s = String(c || '').trim();
        if (/^[✗❌]/.test(s)) return '';
        return '<div class="tm-f"><span class="tm-fa" aria-hidden="true">↳ 🔀</span><span>If ' + esc(s) + ' <span class="tm-fx">➔</span> <b>' + L[i] + '. ' + esc(it.o[i]) + '</b></span></div>';
      }).join('') + '</div>';"""
if page.count(old) != 1:
    raise SystemExit('tmHtml flip block changed')
page = page.replace(old, new)
old2 = "    + '</div>' + fl + '<div class=\"tm-score\" data-tmscore></div></div>';"
new2 = ("    + '</div>' + fl + ((tm.x || []).length ? '<div class=\"tm-x\"><span class=\"tm-fk\">❌ Why not the others</span>' + tm.x.map(([i, s]) => '<div class=\"tm-xr\"><b>' + L[i] + '. ' + esc(it.o[i]) + '</b><span>' + esc(s) + '</span></div>').join('') + '</div>' : '')"
        " + '<div class=\"tm-score\" data-tmscore></div></div>';")
if page.count(old2) != 1:
    raise SystemExit('tmHtml tail changed')
page = page.replace(old2, new2)
css_anchor = '.tm-cue-2{background:rgba(139,92,246,.2);border-left:3px solid #8b5cf6}'
if page.count(css_anchor) != 1:
    raise SystemExit('tm css anchor changed')
page = page.replace(css_anchor, css_anchor + '\n.tm-x{margin-top:10px;display:flex;flex-direction:column;gap:5px}\n.tm-xr{display:flex;flex-direction:column;gap:1px;padding:6px 9px;border-radius:8px;border-left:3px solid #ef4444;background:rgba(239,68,68,.09);line-height:1.4}\n.tm-xr b{font-size:.9rem}\n.tm-xr span{font-size:.88rem}')

F.write_text(page, encoding='utf-8')
print({k: v for k, v in stats.items() if k != 'errors'})
