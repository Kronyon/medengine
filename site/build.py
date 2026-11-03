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
"""
import pathlib, re, shutil, sys, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / 'site'
OFF = ROOT / 'offline'
OUT = OFF / 'dist' / 'medengine'
OSCE_URL = 'https://claude.ai/artifact/2inAuiJNGrZaB4XqP7uQYm'
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
    if 'href="osce.html' in a:
        raise SystemExit('STUDY artifact still links to osce.html')
    return must(a, '<title>medengine-STUDY</title>', '<title>medengine-STUDY</title>\n' + ARTIFACT_FLAG, 1)


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
    for name, html in (('osce.html', osce), ('study.html', study), ('index.html', index), ('medengine.html', index)):
        (OUT / name).write_text(html, encoding='utf-8')
    shutil.copytree(OFF / 'img', OUT / 'img')
    shutil.copy(OFF / 'src' / 'READ ME.txt', OUT / 'READ ME.txt')

    dist = OFF / 'dist'
    site_files = [(OUT / n, n) for n in ('index.html', 'osce.html', 'study.html')]
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
    print('derived app/dist/app.html and study/medengine-study.html for claude.ai')


if __name__ == '__main__':
    build()
