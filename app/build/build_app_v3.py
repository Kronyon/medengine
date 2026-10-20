import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
head = open(f'{R}/src/app_head.html', encoding='utf8').read()
js = open(f'{R}/src/app_script.html', encoding='utf8').read()
data = open(f'{R}/build/osce_data_v3.json', encoding='utf8').read().replace('</', '<\\/')
mev_css = open(f'{R}/src/mev.css', encoding='utf8').read()
mev_js = open(f'{R}/src/mev.js', encoding='utf8').read()
assert '</script' not in mev_js and '<header class="top">' in head
head = head.replace('<header class="top">', '<style>\n' + mev_css + '</style>\n<header class="top">', 1)
html = head + '<script>\n' + mev_js + '</script>\n' + js.replace('__DATA__', data, 1)
os.makedirs(f'{R}/out', exist_ok=True)
open(f'{R}/out/index.html', 'w', encoding='utf8').write(html)
print('out/index.html', len(html) // 1024, 'KB')
