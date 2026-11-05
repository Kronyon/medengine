#!/usr/bin/env python3
"""v3.6.9 polish on the official-paper explanations (safe to run again):
- drop the generic chatbot opener "Based on the information given, " from MS AKT explanations, keeping the sentence;
- replace "the most likely diagnosis is E." (a bare letter) with the option it names."""
import json, re, pathlib
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
page = F.read_text(encoding='utf-8')
mt = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', page, re.S)
D = json.loads(mt.group(2))
GEN = re.compile(r"^\s*Based on (?:the |this |these )?(?:(?:patient’s |patient's )?(?:clinical )?(?:symptoms|signs|information|presentation|history|clinical features|investigations|features)(?: and (?:signs|history|investigations|laboratory results))?(?: (?:described|given|provided|presented))?|(?:given|provided|presented) information|information (?:given|provided)), ")
n = l = 0
for q in D['off']['q']:
    w = q.get('w') or ''
    m = GEN.match(w)
    if m:
        rest = w[m.end():]; q['w'] = rest[:1].upper() + rest[1:]; n += 1
    m2 = re.search(r'\bis ([A-E])\.', q['w'] or '')
    if m2:
        i = 'ABCDE'.index(m2.group(1))
        if i < len(q['o']):
            opt = q['o'][i].rstrip('.'); tail = q['w'][m2.end():]
            tail = re.sub(r'^\s*' + re.escape(opt) + r'\.', '', tail, flags=re.I)   # "is B. Migraine." -> "is migraine."
            q['w'] = q['w'][:m2.start(1)] + opt + '.' + tail; l += 1
page = page[:mt.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + page[mt.end(2):]
F.write_text(page, encoding='utf-8')
print('explanations: generic opener removed', n, '| bare letter replaced', l)
