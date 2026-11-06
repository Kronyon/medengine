#!/usr/bin/env python3
"""v3.3+ build. site/index.html, site/osce.html and site/study.html are the source of truth
(Antigravity and Claude both edit these three files directly).

Outputs
  offline/dist/medengine/                 index.html (launcher), medengine.html (same launcher), osce.html,
                                          study.html, img/, READ ME.txt
  offline/dist/medengine-website.zip      Netlify: index.html, osce.html, study.html, img/ at the top level
  offline/dist/medengine-code-audit.zip   the same without img/ (stays under 20 MB for audit tools)
  offline/dist/medengine-vX-offline.zip   the folder above, for download
  app/dist/app.html                       claude.ai OSCE artifact (derived: no key shim, claude.ai links)
  study/medengine-study.html              claude.ai STUDY artifact (derived the same way)
  step1/medengine-step1.html              claude.ai STEP1 artifact: the STUDY engine with the Step 1 pack (make_step1)
"""
import json, pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
OFF = ROOT / 'offline'
OUT = OFF / 'dist' / 'medengine'
OSCE_URL = 'https://claude.ai/artifact/2inAuiJNGrZaB4XqP7uQYm'
STEP1_URL = 'https://claude.ai/artifact/GVUEwVwVsrm1akHoL9jJYX'
STUDY_URL = 'https://claude.ai/artifact/NexSvgTB8VhqktVFfko6JR'
ARTIFACT_FLAG = '<script>window.MEDENGINE_ARTIFACT = true;</script>\n'


def must(s, old, new, count=None):
    n = s.count(old)
    if not n or (count is not None and n != count):
        raise SystemExit(f'expected {count or "some"} of {old[:70]!r}, found {n}')
    return s.replace(old, new)


def version_of(html, rx):
    m = re.search(rx, html)
    return m.group(1) if m else None


def check_versions(osce, study, index):
    vs = {
        'osce header': version_of(osce, r'<span class="ver">v([\d.]+)</span>'),
        'osce APP_VERSION': version_of(osce, r"APP_VERSION = '([\d.]+)'"),
        'study header': version_of(study, r'<small>v([\d.]+)</small>'),
        'launcher': version_of(index, r'<span class="ver">v([\d.]+)</span>'),
    }
    if len(set(vs.values())) != 1:
        raise SystemExit('version mismatch: ' + repr(vs))
    return next(iter(vs.values()))


def strip_key_shim(html):
    # the browser-key AI layer is for the website only; claude.ai supplies its own AI
    out, n = re.subn(r'<script>\n// medengine AI layer.*?\n</script>\n', '', html, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('AI key shim not found')
    return out


def derive_osce(osce):
    a = strip_key_shim(osce)
    a = must(a, '<a class="switch" id="drillLink" href="study.html"',
             '<a class="switch" id="drillLink" data-private href="' + STUDY_URL + '" target="_blank" rel="noopener"', 1)
    a = must(a, "const DRILL = 'study.html';", "const DRILL = '" + STUDY_URL + "';", 1)
    a = must(a, "-read\">📖 Notes in medengine-STUDY ↗</a>", "-read\" target=\"_blank\" rel=\"noopener\">📖 Notes in medengine-STUDY ↗</a>", 1)
    a = must(a, "-think\">🧠 Think tab in medengine-STUDY ↗</a>", "-think\" target=\"_blank\" rel=\"noopener\">🧠 Think tab in medengine-STUDY ↗</a>", 1)
    a = a.replace('Add your AI key (top right) to use the AI', 'AI works on the published page only')
    a = a.replace('Add your AI key to use the AI patient and examiner', 'Sign in to use the AI patient and examiner')
    return must(a, '<title>medengine-OSCE</title>', '<title>medengine-OSCE</title>\n' + ARTIFACT_FLAG, 1)


def derive_study(study):
    a = strip_key_shim(study)
    a = must(a, '<a class="oscelink" href="osce.html"', '<a class="oscelink" href="' + OSCE_URL + '" target="_blank" rel="noopener"', 1)
    a = must(a, 'href="osce.html#u\' + u.i + \'">', 'href="' + OSCE_URL + '#u\' + u.i + \'" target="_blank" rel="noopener">', 1)
    a = must(a, '<a class="oscelink" href="step1.html"', '<a class="oscelink" href="' + STEP1_URL + '" target="_blank" rel="noopener"', 1)
    if 'href="osce.html' in a:
        raise SystemExit('STUDY artifact still links to osce.html')
    return must(a, '<title>medengine-STUDY</title>', '<title>medengine-STUDY</title>\n' + ARTIFACT_FLAG, 1)


# ---------------------------------------------------------------- medengine-STEP1
# The same engine as STUDY with the Step 1 pack (step1/pack.json from step1/build_pack.py) and the Step 1 add-on
# (step1/ext_step1.js and .css). Saves never touch STUDY or OSCE: every storage key, the IndexedDB names, the cloud
# backup table and the discussion threads get their own names, and the leaderboard profile is never pushed.
STEP1 = ROOT / 'step1'
STEP1_PACK = {'id': 'step1', 'noOsce': True, 'noFig': True, 'noProfile': True,
              'hideNav': ['leaderboard']}
STEP1_KEYS = [  # old literal, new literal, how many times it appears in study.html
    ("'qq-drill-ilo-v1'", "'qq-step1-v1'", 4), ("'medengine-shots-v1'", "'medengine-step1-shots-v1'", 4),
    ("'medengine-ig-v1'", "'medengine-step1-ig-v1'", 4), ("'medengine-cosmetics'", "'medengine-step1-cosmetics'", 4),
    ("'medengine-study'", "'medengine-step1'", 3), ("'medengine-remix-v1'", "'medengine-step1-remix-v1'", 3),
    ("'medengine-misses-v1'", "'medengine-step1-misses-v1'", 3), ("'medengine-trg'", "'medengine-step1-trg'", 2),
    ("'medengine-study-save-'", "'medengine-step1-save-'", 1), ("'medengine-shield'", "'medengine-step1-shield'", 1),
    ("'medengine-remix-vault-'", "'medengine-step1-remix-vault-'", 1),
    ("'medengine-progress-shield-v1'", "'medengine-step1-progress-shield-v1'", 1),
    ("'medengine-progress-'", "'medengine-step1-progress-'", 1), ("'medengine-cloud-cache-v1'", "'medengine-step1-cloud-cache-v1'", 1),
    ("'medengine-accounts-v3'", "'medengine-step1-accounts-v3'", 1),
    ("  'qq-osce-v1',\n", "", 1),                                   # never snapshot or restore OSCE progress from STEP1
    ("/^(qq-|medengine-)/", "/^(qq-step1-|medengine-step1-)/", 2),  # save files carry STEP1 keys only
    ("/rest/v1/med_backups?", "/rest/v1/med_backups_step1?", 2),    # its own private backup table (step1/supabase_step1.sql)
    ("discBoxHtml('u:' + u.i", "discBoxHtml('s1u:' + u.i", 1), ("const tid = 'u:' + u.i;", "const tid = 's1u:' + u.i;", 1),
    ("async function pushProfile(){\n    ensureV3State();", "async function pushProfile(){\n    if (PACK.noProfile) return null;\n    ensureV3State();", 1),
]
STEP1_OLD_KEYS = ['qq-drill-ilo-v1', 'qq-osce-v1', 'medengine-misses-v1', 'medengine-remix-v1', 'medengine-shots-v1', 'medengine-ig-v1',
                  "'medengine-cosmetics'", "'medengine-study'", 'medengine-accounts-v3', 'medengine-cloud-cache-v1', 'medengine-progress-shield-v1',
                  "'medengine-trg'", "'medengine-shield'", '/rest/v1/med_backups?']
STEP1_TEXT = [  # wording: First Aid chapters and topics instead of ILO weeks and conditions; the 4-box explanation
    ('<title>medengine-STUDY</title>', '<title>medengine-STEP1</title>', 1),
    ('aria-label="medengine-STUDY home"', 'aria-label="medengine-STEP1 home"', 1),
    ('<span class="word">medengine-STUDY</span>', '<span class="word">medengine-STEP1</span>', 1),
    ('<a class="oscelink" href="osce.html" title="Open medengine-OSCE: stations, exams, DOPS, AI patient"><span class="od">m</span>medengine-OSCE ↗</a>',
     '<a class="oscelink" href="study.html" title="Open medengine-STUDY, your FFP revision"><span class="od">m</span>medengine-STUDY ↗</a>', 1),
    ("'ILO weeks · '", "'First Aid chapters · '", 1), ("' conditions</h4>'", "' topics</h4>'", 1),
    ("' conditions</span>", "' topics</span>", 2),
    ('search every condition, every line of the notes and the posters', 'search every topic and every line of the notes', 1),
    ("'All ILO notes on one page'", "'All Step 1 notes on one page'", 1), ("'Frameworks · ↕ · 🔎'", "'Domino arrows · 🔎 hunt'", 1),
    ("'Jargon decoder'", "'Eponym decoder'", 1), ("'Abbreviations'", "'US abbreviations ↔ UK'", 1),
    ("qb('why', '🧬', 'Why it happens'", "qb('why', '🌊', 'Inflow → outflow'", 1),
    ('⚡ Thought map', '⚡ 4-box deconstruct', 1), ("'🎯 Cues'", "'🎯 Red flags'", 1),
    ("'⚙️ Mechanism'", "'🌊 Inflow → outflow'", 1), ("'⚖️ Decisive gate'", "'💰 Money line'", 1),
    ('❌ Why not the others · 🔀 change one thing and…', '❌ Why not the others · 🔀 change the film and…', 1),
    ("'Quack Quack page'", "'Step 1 notes, written fresh'", 1),
    ('Arrows and word hunt adapted from High-Yield’s <i>HY Arrows</i> and <i>HY Internal Medicine</i> (HY) and <i>First Aid for the USMLE Step 1 2026</i> (FA), filtered to your ILOs and rewritten for UK practice (NICE, BTS, BASHH, MHRA).',
     'Arrows and trigger lines are written fresh in the one-line format of High-Yield’s <i>HY Arrows</i> and <i>HY Internal Medicine</i>, organised by <i>First Aid for the USMLE Step 1</i> chapter. Nothing is copied from either book.', 1),
    ('🧬 Why it happens · Pathophysiology', '🌊 Inflow → outflow', 2), ("' Pathophysiology cards<", "' mechanism chains<", 1),
    ('Roots after <i>Pathophysiology: Fundamentals of Pathology</i>.', 'Mechanism chains written fresh.', 1),
    ('🇬🇧 US book vs UK (go UK)', '🇬🇧 US vs UK (answer the US way on Step 1)', 1),
    ('Every condition, bug, drug, test and procedure in your ILOs on one scroll.', 'Every First Aid topic on one scroll.', 1),
    ("Condition clues marked HY and FA are adapted from High-Yield\\'s <i>HY Internal Medicine</i> and <i>First Aid Step 1</i> and rewritten for UK practice; everything else is written for your ILOs from NICE, BTS, BNF and MHRA guidance.",
     "Every line is written fresh in the one-line format of High-Yield\\'s <i>HY Internal Medicine</i> and organised by <i>First Aid</i> chapter; nothing is copied.", 1),
    ("['u', '🩺', 'Conditions']", "['u', '🩺', 'Step 1 topics']", 1),
    ('First Aid, UK-adapted', 'First Aid chapter line, written fresh', 1),
    ('<h1>Jargon Decoder</h1>', '<h1>Eponym Decoder</h1>', 1),
    ('<a class="oscelink" href="step1.html" title="Open medengine-STEP1: USMLE Step 1"><span class="od">s1</span>medengine-STEP1 ↗</a>\n',
     '<button type="button" class="btn sm ghost" data-go="labs" title="US lab values with the UK bridge">🧪 Labs (US↔UK)</button>\n', 1),
    ("qb('act', '⚡', 'First move vs cure'", "qb('act', '🔬', 'Lab sim & next steps'", 1),
    ("icon: '⚡', title: 'First move vs cure', unit: 'cards'", "icon: '🔬', title: 'Lab sim & next-step actions', unit: 'sims'", 1),
    ('<b class="grow">⚡ First move vs cure</b>', '<b class="grow">🔬 Lab sim & next-step actions</b>', 1),
    ('Remix: answer a clinical vignette,', 'Remix: answer the question on UWorld,', 1),
    ("+ Math.min(20, list.length) + '</button>' + (list.length > 20 ?", "+ Math.min(20, list.length) + '</button><button class=\"btn\" data-go=\"block\" title=\"20 questions, 30 minutes, exam rules\">⏱️ 20Q block (30 min)</button>' + (list.length > 20 ?", 1),
    ('Miss an image question on SBA Bank?', 'Miss an image question on UWorld?', 1),
    ('Answer it on SBA Bank first,', 'Answer it on UWorld first,', 1),
    ("Submit it on SBA Bank first,", "Submit it on UWorld first,", 1),
    ("Three questions for every ILO condition, drug group, test and procedure, plus the off-map topics, your own mock and 599 questions from the official practice papers (incl. Sept 2026 P1 &amp; P2) 🏛️. ",
     "Step 1 single best answers in NBME style: US units in the stems, the 4-box explanation and a change-the-film flip for every wrong option. ", 1),
    ("Random single-best-answer questions from the ILO weeks you pick.", "Random questions from the First Aid chapters you pick.", 1),
    ("📖 All ILO notes</span><span>' + UNITS.length + ' conditions on one scroll", "📖 All Step 1 notes</span><span>' + UNITS.length + ' topics on one scroll", 1),
    ("Everything your ILOs need, searchable", "Every Step 1 topic, searchable", 1), ("filed under their ILO condition", "filed under their topic", 1),
    ('placeholder="Search your ILO conditions: drug, sign, topic…"', 'placeholder="Search every Step 1 topic: drug, sign, bug…"', 1),
    ('>Systems &amp; presentations</div>', '>USMLE systems</div>', 1),
    ("['why', '🧬', 'Why it happens', ", "['why', '🌊', 'Inflow → outflow', ", 1),
    ("qb('fw', '🧠', ", "qb('fw', '↕', ", 1), ("'High-Yield HY'", "'High-Yield-style HY line, written fresh'", 1),
]


def make_step1(study):
    pack = (STEP1 / 'pack.json').read_text(encoding='utf-8')
    links = STEP1 / 'img_links_v3612.json'   # v3.6.13: question images linked in v3.6.12 (their figures already ship in off.img)
    if links.exists():
        P = json.loads(pack); L = json.loads(links.read_text(encoding='utf-8'))['img']
        for q in P['hq']['q']:
            if q['id'] in L and not q.get('img'): q['img'] = L[q['id']]
        pack = json.dumps(P, ensure_ascii=False, separators=(',', ':'))
    js = (STEP1 / 'ext_step1.js').read_text(encoding='utf-8')
    css = (STEP1 / 'ext_step1.css').read_text(encoding='utf-8')
    if '</script' in js.lower() or '</style' in css.lower():
        raise SystemExit('STEP1 add-on contains a closing tag')
    a = study
    mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', a, re.S)
    a = a[:mt.start(2)] + pack.replace('</', '<\\/') + a[mt.end(2):]
    a = must(a, '<script id="qqdata"', '<style id="step1css">\n' + css + '\n</style>\n<script>window.MEDENGINE_PACK = '
             + json.dumps(STEP1_PACK) + ';</script>\n<script>\n' + js + '\n</script>\n<script id="qqdata"', 1)
    for old, new, n in STEP1_KEYS + STEP1_TEXT:
        a = must(a, old, new, n)
    a = re.sub(r'\bpublic\.med_backups\b', 'public.med_backups_step1', a)
    left = [k for k in STEP1_OLD_KEYS if k in a]
    if left:
        raise SystemExit('STEP1 still uses STUDY storage: ' + ', '.join(left))
    return a


def derive_step1(step1):
    a = strip_key_shim(step1)
    a = must(a, '<a class="oscelink" href="study.html"', '<a class="oscelink" href="' + STUDY_URL + '" target="_blank" rel="noopener"', 1)
    return must(a, '<title>medengine-STEP1</title>', '<title>medengine-STEP1</title>\n' + ARTIFACT_FLAG, 1)


def zip_dir(path, files, prefix=''):
    if path.exists():
        path.unlink()
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for p, name in files:
            zf.write(p, prefix + name)
    return path.stat().st_size


def build():
    osce = (SITE / 'osce.html').read_text(encoding='utf-8')
    study = (SITE / 'study.html').read_text(encoding='utf-8')
    index = (SITE / 'index.html').read_text(encoding='utf-8')
    ver = check_versions(osce, study, index)
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    step1 = make_step1(study)
    for name, html in (('osce.html', osce), ('study.html', study), ('step1.html', step1), ('index.html', index), ('medengine.html', index)):
        (OUT / name).write_text(html, encoding='utf-8')
    shutil.copytree(OFF / 'img', OUT / 'img')
    shutil.copy(OFF / 'src' / 'READ ME.txt', OUT / 'READ ME.txt')

    dist = OFF / 'dist'
    site_files = [(OUT / n, n) for n in ('index.html', 'osce.html', 'study.html', 'step1.html')]
    imgs = [(p, 'img/' + p.name) for p in sorted((OUT / 'img').iterdir()) if p.is_file()]
    n1 = zip_dir(dist / 'medengine-website.zip', site_files + imgs)
    n2 = zip_dir(dist / 'medengine-code-audit.zip', site_files)
    if n2 >= 20e6:
        raise SystemExit('code-only zip is over 20 MB')
    off_files = [(p, p.relative_to(OUT).as_posix()) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name != 'index.html']
    n3 = zip_dir(dist / f'medengine-v{ver}-offline.zip', off_files, 'medengine/')
    print(f'v{ver}: website {n1/1e6:.1f} MB, code-only {n2/1e6:.1f} MB, offline {n3/1e6:.1f} MB')

    (ROOT / 'app' / 'dist').mkdir(parents=True, exist_ok=True)
    (ROOT / 'app' / 'dist' / 'app.html').write_text(derive_osce(osce), encoding='utf-8')
    (ROOT / 'study' / 'medengine-study.html').write_text(derive_study(study), encoding='utf-8')
    (STEP1 / 'medengine-step1.html').write_text(derive_step1(step1), encoding='utf-8')
    print('derived app/dist/app.html, study/medengine-study.html and step1/medengine-step1.html for claude.ai')


if __name__ == '__main__':
    build()
