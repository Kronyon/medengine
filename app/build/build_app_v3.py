import json, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
head = open(f'{R}/src/app_head.html', encoding='utf8').read()
js = open(f'{R}/src/app_script.html', encoding='utf8').read()
data = open(f'{R}/build/osce_data_v3.json', encoding='utf8').read().replace('</', '<\\/')
html = head + js.replace('__DATA__', data, 1)
os.makedirs(f'{R}/out', exist_ok=True)
open(f'{R}/out/index.html', 'w', encoding='utf8').write(html)
print('out/index.html', len(html) // 1024, 'KB')
