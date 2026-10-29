#!/usr/bin/env python3
"""Builds the downloadable medengine.exe bundle: no claude.ai, no sign-in, works offline.

offline/dist/medengine/
  medengine.html   launcher: double-click this
  osce.html        medengine-OSCE (AI via your own Anthropic key, everything else offline)
  study.html       medengine-STUDY
  img/             STUDY page images
  READ ME.txt

Inputs: app/dist/app.html (built OSCE app), study/medengine-study.html, offline/img/ (STUDY images),
offline/src/offline-ai.js, offline/src/launcher.html.
"""
import os, re, shutil, zipfile, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
OFF = ROOT / 'offline'
OUT = OFF / 'dist' / 'medengine'
OSCE_URL = 'https://claude.ai/artifact/2inAuiJNGrZaB4XqP7uQYm'
STUDY_URL = 'https://claude.ai/artifact/NexSvgTB8VhqktVFfko6JR'
SKELETON = '<!doctype html>\n<html lang="en-GB">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
DIALOG_CSS = """<style>
dialog.acct{border:1px solid var(--line);border-radius:16px;background:var(--surface);color:var(--ink);padding:0;width:min(460px,calc(100vw - 32px));box-shadow:var(--shadow)}
dialog.acct::backdrop{background:rgba(10,20,25,.45)}
dialog.acct .okey{padding:18px;display:flex;flex-direction:column;gap:10px;margin:0}
dialog.acct h2,dialog.acct p{margin:0}
dialog.acct .small{font-size:.8rem}
dialog.acct .fld{display:flex;flex-direction:column;gap:4px;font-size:.82rem;font-weight:700;color:var(--muted)}
dialog.acct .fld input{width:100%;font-size:1rem}
dialog.acct details summary{cursor:pointer;font-size:.85rem;color:var(--muted)}
dialog.acct details .fld{margin-top:8px}
dialog.acct code{font-family:var(--f-mono);font-size:.85rem}
#aiKeyBtn{white-space:nowrap;flex:none}
@media (max-width:620px){#aiKeyBtn .al{display:none}}
</style>
"""


def must_replace(s, old, new, count=None):
    n = s.count(old)
    if not n or (count is not None and n != count):
        raise SystemExit(f'expected {count or "some"} of {old[:60]!r}, found {n}')
    return s.replace(old, new)


def same_tab(s, href_re, count):
    # Links between the two apps open in the same tab, so tapping goes straight there.
    s, n = re.subn('(' + href_re + r')\s+target="_blank" rel="noopener"', r'\1', s)
    if n != count:
        raise SystemExit(f'expected {count} cross-app links, changed {n}')
    return s


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    # medengine-OSCE
    osce = (ROOT / 'app' / 'dist' / 'app.html').read_text(encoding='utf-8')
    osce = must_replace(osce, "DRILL = '" + STUDY_URL + "'", "DRILL = 'study.html'", 1)
    osce = must_replace(osce, 'id="drillLink" data-private href="' + STUDY_URL + '"', 'id="drillLink" href="study.html"', 1)
    osce = must_replace(osce, "'Sign in to use the AI patient and examiner'", "'Add your AI key to use the AI patient and examiner'", 1)
    osce = must_replace(osce, 'AI works on the published page only', 'Add your AI key (top right) to use the AI')
    if STUDY_URL in osce:
        raise SystemExit('a STUDY link was left pointing at claude.ai')
    osce = same_tab(osce, r'href="(?:study\.html|\' \+ DRILL \+ [^"]*)"', 3)
    shim = (OFF / 'src' / 'offline-ai.js').read_text(encoding='utf-8')
    app_script = osce.index('<script>\nconst D = ')
    osce = osce[:app_script] + DIALOG_CSS + '<script>\n' + shim + '\n</script>\n' + osce[app_script:]
    (OUT / 'osce.html').write_text(SKELETON + osce, encoding='utf-8')

    # medengine-STUDY
    study = (ROOT / 'study' / 'medengine-study.html').read_text(encoding='utf-8')
    study = must_replace(study, OSCE_URL, 'osce.html')
    study = same_tab(study, r'href="osce\.html[^"]*"', 2)
    if 'claude.ai/artifact' in study:
        raise SystemExit('STUDY still links to claude.ai')
    # the Remix AI: same key shim as OSCE (same origin, so the key saved in OSCE is reused)
    study = must_replace(study, '<header class="top">', DIALOG_CSS + '<script>\n' + shim + '\n</script>\n<header class="top">', 1)
    (OUT / 'study.html').write_text(SKELETON + study, encoding='utf-8')
    shutil.copytree(OFF / 'img', OUT / 'img')

    # launcher + read me
    shutil.copy(OFF / 'src' / 'launcher.html', OUT / 'medengine.html')
    shutil.copy(OFF / 'src' / 'READ ME.txt', OUT / 'READ ME.txt')

    z = OFF / 'dist' / 'medengine-v2.7.0-offline.zip'
    if z.exists():
        z.unlink()
    with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.rglob('*')):
            if p.is_file():
                zf.write(p, 'medengine/' + p.relative_to(OUT).as_posix())
    print('built', OUT, 'and', z.name, f'{z.stat().st_size / 1e6:.1f} MB')


if __name__ == '__main__':
    build()
