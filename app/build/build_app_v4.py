"""medengine-OSCE v1.3: single-file page = head + MEV schematics + pictures (dg_*.js) + engine + data."""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: open(f'{R}/{p}', encoding='utf8').read()
head, js = rd('src/app_head.html'), rd('src/app_script.html')
data = rd('build/osce_data_v4.json').replace('</', '<\\/')
mev_css, mev_js = rd('src/mev.css'), rd('src/mev.js')
dg_js = '\n'.join(rd('src/' + f) for f in ('dg_core.js', 'dg_cards.js', 'dg_ex.js', 'dg_img.js', 'dg_more.js'))
assert '</script' not in mev_js + dg_js and '<header class="top">' in head
head = head.replace('<header class="top">', '<style>\n' + mev_css + '</style>\n<header class="top">', 1)
html = head + '<script>\n' + mev_js + '</script>\n<script>\n' + dg_js + '\n</script>\n' + js.replace('__DATA__', data, 1)
os.makedirs(f'{R}/out', exist_ok=True)
open(f'{R}/out/index.html', 'w', encoding='utf8').write(html)
print('out/index.html', len(html) // 1024, 'KB')
