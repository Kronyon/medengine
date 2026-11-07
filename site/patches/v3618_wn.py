#!/usr/bin/env python3
"""v3.6.18: the robotic why-not text goes.
- 823 "Ruled out here: requires X, whereas this patient has Y" lines are dropped. Every one repeated its option's flip
  (X) and Y was a broken stem fragment ("A 56 year old woman with"). The flip line stays, so the row now reads the
  slim way: "↳ 🔀 an ulcer that can be probed down to bone ➔ C. Acute osteomyelitis".
- 2,679 filler flips "the presentation instead showed features specific to X (why line)" are dropped: each only
  repeated the why line beside it.
- 19 flips that had been matched from the wrong card (a mnemonic about hypoglycaemia under a dapagliflozin question,
  venous eczema under Fournier's gangrene...) are rewritten for their own question.
Checked: no wrong option is left with neither a why line nor a flip. Options are untouched, so saved runs are safe."""
import json, pathlib, re
F = pathlib.Path(__file__).resolve().parents[1] / 'study.html'
s = F.read_text(encoding='utf-8')
m = re.search(r'(<script id="qqdata" type="application/json">)(.*?)(</script>)', s, re.S)
D = json.loads(m.group(2))
FIX = {
 ('h0049', 'Genital warts in pregnancy: cryotherapy'): 'a small superficial BCC on the trunk or a limb',
 ('h0060', 'Wheals that move and fade in hours = urticaria. One spot lasting days = something else.'): 'itchy wheals that fade within 24 hours, with a normal C4',
 ('h0064', 'Emollients are the foundation; steroids put out the flares.'): 'itchy, weeping eczema with no punched-out erosions and no fever',
 ('h0077', 'Both legs red and warm is rarely cellulitis: think venous eczema.'): 'warm, red scrotal skin with no crepitus, dusky patches or shock',
 ('h0215', 'The silent killer: no symptoms, all the damage. Treat the number before it treats you.'): 'the question asked which condition is most linked to retinal vein occlusion',
 ('h0230', 'Dry is slow and has drusen; wet is fast and needs injections.'): 'gradual central distortion in an older person with drusen at the macula',
 ('h0451', 'Anxiety is a smoke alarm that rings for toast. CBT recalibrates the alarm.'): 'worry about many different things on most days for at least 6 months',
 ('h0577', 'Never give an antidepressant alone in bipolar: it can flip someone into mania.'): 'elevated mood with no steroid, drug or medical trigger',
 ('h0730', 'Four is the floor; 15 and 15.'): 'the question asked about a sulfonylurea such as gliclazide',
 ('h0745', 'Epilepsy: avoid bupropion'): 'varenicline was not tolerated and she has no epilepsy or eating disorder',
 ('h0765', 'Lower UTI in early pregnancy: nitrofurantoin for 7 days'): 'a pregnant woman with a lower urinary tract infection',
 ('h0803', "Nausea in Parkinson's disease: domperidone"): "nausea in someone with Parkinson's disease",
 ('h0827', "Type 1 has no insulin; type 2 has insulin that isn't listened to."): 'glycosuria with a high blood glucose and a high urine osmolality',
 ('h0883', 'Two adequate antipsychotic trials failed: clozapine'): 'schizophrenia that has failed two adequate antipsychotic trials',
 ('h0886', 'Faint: brief, quick recovery, pale. Fit: tongue bitten, long confusion after.'): 'the question asked who needs extra caution rather than who cannot have it',
 ('h0896', 'Food poisoning clock: within 6 h = toxin from Staph or Bacillus; days later = a germ that has to grow.'): 'the drug were metformin or an SSRI rather than zopiclone',
 ('h0919', 'Long-term androgen deprivation: screen for osteoporosis'): 'the drug were long-term androgen deprivation or oral steroids',
 ('h0989', 'Biliary colic comes and goes; cholecystitis stays and adds a fever.'): 'a smooth lump under the skin with a central punctum',
 ('h1449', 'Pearly, rolled, slow, rarely spreads: the cancer that destroys locally.'): 'the question asked which lesion suits cryotherapy',
}
rx = fl = fx = 0
for q in D['hq']['q']:
    tm = q.get('tm')
    if not tm: continue
    if 'x' in tm:
        n0 = len(tm['x']); tm['x'] = [r for r in tm['x'] if not r[1].startswith('Ruled out here')]; rx += n0 - len(tm['x'])
    if 'f' in tm:
        n0 = len(tm['f']); tm['f'] = [r for r in tm['f'] if not r[0].startswith('the presentation instead showed features specific to')]; fl += n0 - len(tm['f'])
        for r in tm['f']:
            k = (q['id'], r[0])
            if k in FIX: r[0] = FIX.pop(k); fx += 1
    xs = {i for i, _ in tm.get('x', [])}; fs = {i for _, i in tm.get('f', [])}
    for i in range(len(q['o'])):
        assert i == q['a'] or i in xs or i in fs, ('empty why-not', q['id'], i)
assert not FIX, FIX
assert rx == 823 and fl == 2679, (rx, fl)
s = s[:m.start(2)] + json.dumps(D, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + s[m.end(2):]
F.write_text(s, encoding='utf-8')
print('why-nots: dropped %d template lines and %d filler flips, rewrote %d flips' % (rx, fl, fx))
