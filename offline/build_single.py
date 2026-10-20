#!/usr/bin/env python3
"""Builds medengine.html: ONE self-contained file with the launcher, medengine-OSCE,
medengine-STUDY and every STUDY page image inside it. No folders, no sign-in.

Run offline/build.py first (it prepares osce.html and study.html in offline/dist/medengine/).

How it works: the launcher is the page. Each app is kept as text inside the file and opened in a
full-screen srcdoc frame (same storage as the file itself) the first time you tap it, then kept alive, so switching back and forth is instant
and nothing reloads. Links between the apps (OSCE's "medengine-STUDY" button, STUDY's "OSCE pack"
buttons) jump straight to the other app at the right place. The browser's back button returns home.
"""
import base64, json, pathlib, re

OFF = pathlib.Path(__file__).resolve().parent
SRC = OFF / 'dist' / 'medengine'
OUT = OFF / 'dist' / 'medengine.html'

LINK_JS = """<script>
document.addEventListener('click', function (e) {
  var a = e.target && e.target.closest ? e.target.closest('a[href^="medengine:"]') : null;
  if (!a) return;
  e.preventDefault(); e.stopPropagation();
  var h = a.getAttribute('href').slice(10), i = h.indexOf('#');
  try { parent.postMessage({ medengine: 'go', app: i < 0 ? h : h.slice(0, i), hash: i < 0 ? '' : h.slice(i + 1) }, '*'); } catch (err) {}
}, true);
</script>
"""
IMG_JS = """<script>
function __meImg(k) { try { return (parent.__MEIMG && parent.__MEIMG[k]) || ''; } catch (e) { return ''; } }
</script>
"""

CONTROLLER = r"""
<div id="apps" hidden>
  <iframe id="f-osce" title="medengine-OSCE" allow="microphone; autoplay; clipboard-write"></iframe>
  <iframe id="f-study" title="medengine-STUDY" allow="microphone; autoplay; clipboard-write"></iframe>
</div>
<script>
(function () {
  var frames = { osce: document.getElementById('f-osce'), study: document.getElementById('f-study') };
  var current = '';
  // srcdoc frames share this file's storage, so progress saves the same way as the normal apps.
  function open(f, app, hash) {
    if (hash) f.addEventListener('load', function () { try { f.contentWindow.location.hash = hash; } catch (e) {} }, { once: true });
    f.srcdoc = window.__MEAPPS[app];
  }
  function show(app, hash) {
    var home = document.querySelector('main');
    if (!frames[app]) {
      current = '';
      document.getElementById('apps').hidden = true; home.hidden = false;
      document.documentElement.classList.remove('in-app');
      document.title = 'medengine.exe';
      return;
    }
    var f = frames[app];
    if (!f.hasAttribute('srcdoc')) open(f, app, hash);
    else if (hash) { try { f.contentWindow.location.hash = hash; } catch (e) {} }
    Object.keys(frames).forEach(function (k) { frames[k].classList.toggle('on', k === app); });
    document.getElementById('apps').hidden = false; home.hidden = true;
    document.documentElement.classList.add('in-app');
    document.title = 'medengine-' + app.toUpperCase();
    current = app;
    try { f.focus(); } catch (e) {}
  }
  window.medengineGo = function (app, hash) {
    if (location.hash !== '#' + app) { history.pushState(null, '', '#' + app); }
    show(app, hash);
  };
  window.addEventListener('popstate', function () { show(location.hash.slice(1)); });
  window.addEventListener('hashchange', function () { var a = location.hash.slice(1); if (a !== current) show(a); });
  window.addEventListener('message', function (e) {
    var d = e.data;
    if (!d || d.medengine !== 'go' || !frames[d.app]) return;
    if (e.source !== frames.osce.contentWindow && e.source !== frames.study.contentWindow) return;
    window.medengineGo(d.app, d.hash);
  });
  document.querySelectorAll('[data-go]').forEach(function (a) {
    a.addEventListener('click', function (e) { e.preventDefault(); window.medengineGo(a.getAttribute('data-go')); });
  });
  document.addEventListener('keydown', function (e) {
    if (current || e.metaKey || e.ctrlKey || e.altKey) return;
    if (e.key === '1') window.medengineGo('osce');
    if (e.key === '2') window.medengineGo('study');
  });
  var start = location.hash.slice(1);
  if (frames[start]) show(start);
})();
</script>
"""

FRAME_CSS = """<style>
#apps{position:fixed;inset:0;background:var(--bg);z-index:10}
#apps iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:none;background:var(--bg)}
#apps iframe.on{display:block}
html.in-app,html.in-app body{overflow:hidden;height:100%}
html.in-app body{padding:0}
main[hidden],#apps[hidden]{display:none!important}
</style>
"""


def must_replace(s, old, new, count=None):
    n = s.count(old)
    if not n or (count is not None and n != count):
        raise SystemExit(f'expected {count or "some"} of {old[:60]!r}, found {n}')
    return s.replace(old, new)


def js_string(html):
    # Safe inside <script>: no "</script>", no "<!--", no line separators.
    return json.dumps(html, ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')


def build():
    osce = (SRC / 'osce.html').read_text(encoding='utf-8')
    osce = must_replace(osce, "DRILL = 'study.html'", "DRILL = 'medengine:study'", 1)
    osce = must_replace(osce, 'id="drillLink" href="study.html"', 'id="drillLink" href="medengine:study"', 1)
    osce = must_replace(osce, '<script>\nconst D = ', LINK_JS + '<script>\nconst D = ', 1)
    if re.search(r'["\']study\.html', osce):
        raise SystemExit('OSCE still has a study.html link')

    study = (SRC / 'study.html').read_text(encoding='utf-8')
    study = must_replace(study, 'osce.html', 'medengine:osce')
    study = must_replace(study, "'img/o' + String(osts).padStart(3, '0') + '.webp'", "__meImg('o' + String(osts).padStart(3, '0'))", 1)
    study = must_replace(study, "'img/p' + String(n).padStart(3, '0') + '.webp'", "__meImg('p' + String(n).padStart(3, '0'))", 1)
    if 'img/' in study:
        raise SystemExit('STUDY still has an img/ path')
    i = study.index('<script')
    study = study[:i] + IMG_JS + LINK_JS + study[i:]

    imgs = {}
    for p in sorted((SRC / 'img').glob('*.webp')):
        imgs[p.stem] = 'data:image/webp;base64,' + base64.b64encode(p.read_bytes()).decode('ascii')

    page = (OFF / 'src' / 'launcher.html').read_text(encoding='utf-8')
    page = must_replace(page, 'href="osce.html"', 'href="#osce" data-go="osce"', 1)
    page = must_replace(page, 'href="study.html"', 'href="#study" data-go="study"', 1)
    page = must_replace(page, '<span>Runs from this folder: no sign-in, works offline.', '<span>One file: no sign-in, no folders, works offline.', 1)
    # the controller handles the 1 / 2 keys
    page = re.sub(r"document\.addEventListener\('keydown'.*?\n\}\);\n", '', page, count=1, flags=re.S)
    page = must_replace(page, '<title>medengine.exe</title>', '<title>medengine.exe</title>\n<meta name="apple-mobile-web-app-capable" content="yes">\n<meta name="theme-color" content="#0e8f7e">', 1)
    page = must_replace(page, '</head>', FRAME_CSS + '</head>', 1)
    data = ('<script>\nwindow.__MEAPPS = { osce: ' + js_string(osce) + ',\nstudy: ' + js_string(study) + ' };\n</script>\n'
            '<script>\nwindow.__MEIMG = ' + json.dumps(imgs) + ';\n</script>\n')
    page = must_replace(page, '</body>', data + CONTROLLER + '</body>', 1)
    OUT.write_text(page, encoding='utf-8')
    print('built', OUT.name, f'{OUT.stat().st_size / 1e6:.1f} MB', f'({len(imgs)} images)')

    # Website version (for iPhone/iPad, which will not run scripts from a downloaded file):
    # the same folder with the launcher as index.html, ready to drag onto any static host.
    import zipfile
    site = OFF / 'dist' / 'medengine-website.zip'
    with zipfile.ZipFile(site, 'w', zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(SRC.rglob('*')):
            if p.is_file() and p.name != 'READ ME.txt':
                name = 'index.html' if p.name == 'medengine.html' else p.relative_to(SRC).as_posix()
                zf.write(p, 'medengine/' + name)
    print('built', site.name, f'{site.stat().st_size / 1e6:.1f} MB')


if __name__ == '__main__':
    build()
