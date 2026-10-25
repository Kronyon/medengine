/* medengine-OSCE v1.3: step cards and step tables (the mnemonics, one tile lights up at a time). */
(function () {
  var d = DG.def;
  d('cn12', {t: 'Cranial nerves: walk the head top to bottom', cards: [
    ['👃', 'I · Smell', 'Ask about any change in smell or taste.'], ['👁️', 'II · See', '**Acuity → pupils → fields → fundi.** Swinging torch for a relative afferent defect.'],
    ['↔️', 'III · IV · VI · Move', 'H pattern, head still. **LR6 SO4**, the rest are III.'], ['🖐️', 'V · Feel and chew', 'Forehead, cheek, jaw. Clench; open against resistance: the jaw goes to the weak side.'],
    ['😬', 'VII · Face', 'Eyebrows, eyes shut tight, cheeks, teeth. **Forehead spared = stroke.**'], ['👂', 'VIII · Hear', 'Whisper test, then Rinne and Weber.'],
    ['😮', 'IX · X · Say ahh', 'The uvula moves **away** from the weak side.'], ['🤷', 'XI · Shrug', 'Shrug and turn the head against resistance.'],
    ['👅', 'XII · Tongue', 'Wasting and twitching at rest; sticks out **towards** the weak side.']]});
  d('reflex', {t: 'Reflex roots: count up from the feet', cards: [
    ['👟', '1, 2 · buckle my shoe', '**Ankle jerk = S1, S2.**'], ['🚪', '3, 4 · kick the door', '**Knee jerk = L3, L4.**'],
    ['🥢', '5, 6 · pick up sticks', '**Biceps = C5, C6. Supinator = C6.**'], ['📏', '7, 8 · lay them straight', '**Triceps = C7, C8.**'],
    ['🦶', 'Plantar response', 'Toe goes **up = upper motor neurone**, Babinski positive.'], ['🦷', 'Reinforce', 'Clench the teeth or pull the hands apart before calling a reflex absent.']]});
  d('umnlmn', {t: 'Upper vs lower motor neurone', head: ['', 'Upper motor neurone', 'Lower motor neurone'], keep: true, rows: [
    ['Tone', '**Up**: spastic, clasp-knife', '**Down**: floppy'], ['Power', 'Extensors weaker in the arms, flexors in the legs', 'Weakness in the muscles of that root or nerve'],
    ['Reflexes', '**Brisk**, with clonus', '**Reduced or absent**'], ['Plantars', '**Up**', 'Down'], ['Wasting', 'Little, late', '**Early and marked**'],
    ['Twitching', 'None', '**Fasciculations**'], ['Think of', 'Stroke, cord compression, MS', 'Root, nerve, MND has both']],
    caps: ['Tone first: tight vs floppy.', 'Pyramidal pattern of weakness vs one root or nerve.', '**UMN goes UP, LMN goes DOWN.**', 'An upgoing plantar is a sign of the upper motor neurone.', 'Early wasting points to the lower motor neurone.', 'Fasciculation = lower motor neurone.', 'Motor neurone disease is the one that shows both.']});
  d('lungsigns', {t: 'Chest signs: which side and what is it', head: ['', 'Trachea', 'Expansion', 'Percussion', 'Breath sounds', 'Vocal resonance'], rows: [
    ['Consolidation', 'Central', '↓ on the side', '**Dull**', '**Bronchial**, crackles', '**↑**'], ['Pleural effusion', 'Away if big', '↓', '**Stony dull**', '**↓ or absent**', '**↓**'],
    ['Pneumothorax', 'Away if tension', '↓', '**Hyper-resonant**', '**↓ or absent**', '↓'], ['Collapse', '**Towards**', '↓', 'Dull', '↓', '↓'],
    ['Fibrosis', 'Central or towards', '↓ both', 'Normal', '**Fine end-inspiratory crackles**', 'Normal or ↑'], ['COPD', 'Central', '↓ both', 'Hyper-resonant', 'Wheeze, quiet', 'Normal']],
    caps: ['Pneumonia: **dull + bronchial breathing + louder ninety-nine**.', 'Fluid: **stony dull and silent**; the trachea is pushed away if it is big.', 'Air: **hyper-resonant and silent**; tension pushes the trachea away and drops the BP.', 'Collapse **pulls** the trachea towards it.', 'Velcro crackles at both bases with clubbing.', 'Barrel chest, pursed lips, wheeze.']});
  d('msk', {t: 'Every joint: the same 6 moves', cards: [
    ['👀', 'Look', 'Standing and lying; front, side, behind. Swelling, wasting, deformity, scars; then gait.'], ['✋', 'Feel', 'Temperature with the back of the hand, then bony landmarks, joint line, tenderness.'],
    ['🔄', 'Move', '**Active first, then passive**, watching the face. Lost active but full passive = tendon or nerve.'], ['🧪', 'Special tests', 'Only the ones for that joint, explained before you do them.'],
    ['🚶', 'Function', 'What it means for them: walking, reaching, buttons.'], ['➕', 'Complete', '"I would examine the **joint above and below**, check the **nerves and pulses**, and request an **X-ray**."']]});
  d('knee', {t: 'Knee special tests', cards: [
    ['💧', 'Sweep test', '**Small effusion**: stroke up the inner side, then down the outer side, and watch the inner side bulge.'], ['🎾', 'Patellar tap', '**Large effusion**: squeeze fluid down from above, then tap the kneecap.'],
    ['↔️', 'Valgus and varus at 20 to 30°', '**Valgus opens the inside = MCL. Varus opens the outside = LCL.**'], ['⬇️', 'Posterior sag', 'Look first at 90°. A sag = PCL, and it fakes a positive anterior drawer.'],
    ['⬆️', 'Anterior drawer and Lachman\'s', '**ACL.** Lachman\'s at 20 to 30° is the more sensitive.'], ['🔒', 'Joint line and McMurray\'s', '**Meniscus**: joint line tenderness, locking, giving way.']]});
  d('elbow', {t: 'Elbow: outside vs inside', cards: [
    ['🎾', 'Lateral epicondyle = tennis', 'Extensors. A backhand pulls the wrist back.'], ['⛳', 'Medial epicondyle = golfer\'s', 'Flexors.'],
    ['✊', 'Cozen\'s test', 'Elbow straight, fist, cock the wrist back against you: **lateral pain = tennis elbow.**'], ['🔻', 'Resisted wrist flexion', '**Medial pain = golfer\'s elbow.**'],
    ['🖐️', 'Pronation and supination', 'Elbows tucked in, thumbs up, so the shoulder can\'t cheat.'], ['⚡', 'Ulnar nerve', 'Behind the medial epicondyle: tingling into the little finger.']]});
  d('hand', {t: 'Hand: RA vs OA, and the three nerves', cards: [
    ['🔥', 'Rheumatoid arthritis', '**Soft, warm, symmetrical MCPs and PIPs; DIPs spared.** Ulnar deviation, swan neck, boutonnière, Z-thumb.'],
    ['🪨', 'Osteoarthritis', '**Hard nodes: B before H.** Bouchard\'s at the PIP comes before Heberden\'s at the DIP, walking out to the tip. Squared thumb base.'],
    ['👍', 'Median nerve', 'Thumb to the ceiling against resistance; sensation at the index pulp. **Carpal tunnel.**'], ['🖐️', 'Ulnar nerve', 'Spread the fingers; Froment\'s with paper; sensation at the little finger pulp.'],
    ['🖖', 'Radial nerve', 'Cock the wrist back; sensation over the back of the thumb web.'], ['🔘', 'Function', 'Grip, pinch, a coin, a button, writing.']]});
  d('genit', {t: 'External genitalia: the sweep', cards: [
    ['🧤', 'Chaperone, consent, gloves', 'Umbilicus to knees exposed.'], ['〰️', 'Groin', 'Lumps, nodes, cough impulse.'], ['🔍', 'Shaft', 'Ulcers, warts, rashes.'],
    ['⬅️', 'Retract', 'Glans and meatus: discharge, ulcers, hypospadias.'], ['➡️', 'REPLACE the foreskin', '**Forgetting causes paraphimosis.** A critical item.'],
    ['🥚', 'Scrotum and testes', 'One at a time, the good side first.'], ['🧪', 'Complete', 'Swabs, urine, full sexual health screen.']]});
  d('mhx', {t: 'Psychiatric history: the order', cards: [
    ['💬', 'Their story', 'Open question, then listen.'], ['🌧️', 'Mood', 'Low mood, no interest, no energy; sleep, appetite, weight, concentration.'],
    ['😰', 'Anxiety', 'Worry, panic, avoidance.'], ['👂', 'Psychosis', 'Voices, beliefs, feeling watched, thoughts being interfered with.'], ['⚡', 'Mania', 'Very high mood, little sleep, spending, big plans.'],
    ['🍺', 'Substances', 'Units of alcohol, drugs, smoking.'], ['⚠️', 'Risk', '**To self, to others, from others.** Ask about suicide directly.'],
    ['📖', 'Life story', 'Past psychiatric, drugs, family, childhood, work, relationships, housing, money, forensic, support.'], ['🎤', 'Present', 'Summary, diagnosis, risk level, plan.']]});
  d('spikes', {t: 'SPIKES: breaking bad news', cards: [
    ['🚪', 'S · Setting', 'Private, sitting, phone silenced, tissues, someone with them.'], ['🔭', 'P · Perception', '"What do you understand about why you had the scan?"'],
    ['🙋', 'I · Invitation', '"Would it be OK if I went through the results?"'], ['📢', 'K · Knowledge', '**Warning shot → the word cancer → silence.**'],
    ['💗', 'E · Emotions', 'Name it: "I can see this is a terrible shock." Count to 10 in the silence.'], ['🧭', 'S · Strategy and summary', 'Next steps, specialist nurse, follow-up date, who to call.']]});
  d('swab', {t: 'Swabs: the right tube and the right spot', cards: [
    ['🧫', 'Bacteria → gel', 'Amies or charcoal transport medium.'], ['🧪', 'Virus → liquid', 'Viral transport medium; snap the stick at the line.'],
    ['😮', 'Throat', 'Both tonsils and the back wall, **not the tongue or cheeks**.'], ['👃', 'Nose', 'Along the floor of the nose about 2 cm, parallel to the roof of the mouth; rotate.'],
    ['🩹', 'Wound', 'Clean off pus with saline, then **zig-zag and rotate** across viable tissue.'], ['🏷️', 'Label and send', 'At the bedside; clinical details and **any antibiotics** on the form.']]});
  d('cath', {t: 'Catheter: the critical moves', cards: [
    ['✋', 'Two hands, two jobs', 'Non-dominant hand holds and becomes dirty; dominant hand stays sterile.'], ['🧊', 'Gel, then wait', 'Lidocaine gel; wait 3 to 5 minutes.'],
    ['⬆️', 'Penis up at 90°', 'Straightens the urethra.'], ['📏', 'To the hilt', 'In men, all the way to the Y junction.'],
    ['💧', 'Urine FIRST, then inflate', '10 ml sterile water; stop if painful.'], ['➡️', 'Replace the foreskin', 'Then document size, batch, residual volume.'],
    ['🦵', 'Female: knees bent and apart', 'Separate the labia; clean front to back, one swab per stroke.'], ['🎯', 'Wrong hole?', 'Leave that catheter in the vagina as a signpost; use a new one just above it.']]});
  d('pen', {t: 'Insulin pen: every injection', cards: [
    ['🧼', 'Wash and check', 'Right insulin, right dose, in date, clear or evenly mixed.'], ['💨', 'Prime 2 units', 'An air shot until a drop appears.'],
    ['📐', '90 degrees', 'With a 4 mm needle no pinch is usually needed.'], ['⏱️', 'Count to 10', 'Hold the button down, then withdraw.'],
    ['🔁', 'Rotate sites', 'Tummy, thighs, buttocks. Lumpy skin stops insulin working.'], ['🗑️', 'New needle each time', 'Into the sharps bin.']]});
  d('inhaler', {t: 'Metered-dose inhaler: 7 steps', cards: [
    ['🧢', 'Cap off, shake', 'Check the counter and expiry.'], ['😮‍💨', 'Breathe out fully', 'Away from the inhaler.'], ['👄', 'Seal the lips', 'Upright, chin up.'],
    ['🐢', 'Press as you start a SLOW breath', '**3 to 5 seconds.** A dry powder inhaler is the opposite: quick and deep.'], ['⏸️', 'Hold for 10', 'Or as long as comfortable.'],
    ['⏳', 'Wait 30 to 60 seconds', 'Before a second puff.'], ['🚰', 'Rinse and spit', 'After a steroid: prevents thrush and a hoarse voice.']]});
  d('pefr', {t: 'Peak flow: huff, don\'t puff', cards: [
    ['0️⃣', 'Pointer to zero', 'New mouthpiece; fingers off the scale.'], ['🧍', 'Stand or sit up', ''], ['🫁', 'Biggest breath in', ''],
    ['💥', 'Blast it out', '**Short, hard and fast**, like blowing out candles. Not long.'], ['3️⃣', 'Best of 3', 'Record the highest, not the average.'],
    ['📈', 'Compare', 'With predicted and their best. **Over 20% variation morning to evening = asthma.**']]});
  d('wash', {t: 'Hand washing: 6 steps, each 5 times', ms: 2000, cards: [
    ['1', 'Palm to palm', ''], ['2', 'Palm over the back, fingers laced', 'Both sides.'], ['3', 'Palm to palm, fingers laced', ''],
    ['4', 'Backs of fingers locked into the palm', ''], ['5', 'Thumbs, rotated in the opposite palm', '**The most missed area.**'], ['6', 'Fingertips, rotated in the palm', ''],
    ['⏱️', 'Wash 40 to 60 s · rub 20 to 30 s', 'Dry with a paper towel; turn the tap off with it.'], ['🧼', 'Soap, not gel', 'For **C. difficile and norovirus**: alcohol doesn\'t kill spores.']]});
  d('cbg', {t: 'Capillary glucose: the side, not the pad', cards: [
    ['🧼', 'Their hands washed', 'Sugar on the skin reads falsely high.'], ['✅', 'Meter checked', 'Quality control done; strips in date.'],
    ['👉', 'Side of the fingertip', 'Middle or ring finger. **Not the pad, not the thumb or index.**'], ['🗑️', 'Lancet straight to sharps', ''],
    ['4️⃣', 'Four is the floor', 'Under 4 = hypo: treat now. Over 11 in type 1: check ketones.']]});
  d('sadmans', {t: 'Sick-day rules: SADMANS', cards: [
    ['S', 'Sulfonylureas', 'Gliclazide: hypos when not eating.'], ['A', 'ACE inhibitors', 'Kidney injury when dry.'], ['D', 'Diuretics', 'Dehydration.'],
    ['M', 'Metformin', 'Lactic acidosis when dry.'], ['A', 'ARBs', 'Kidney injury.'], ['N', 'NSAIDs', 'Kidney injury.'], ['S', 'SGLT2 inhibitors', 'Ketoacidosis, even with normal sugar.'],
    ['🔁', 'Restart', 'When eating and drinking normally for 24 to 48 hours.']]});
  d('axrsys', {t: 'Abdominal X-ray: the order', cards: [
    ['🏷️', 'Details', 'Name, date, supine or erect.'], ['🫧', 'Bowel gas', 'Small bowel central, colon peripheral. **3-6-9.**'], ['☁️', 'Outside the bowel', 'Rigler\'s sign; gas in the biliary tree.'],
    ['🦴', 'Bones', 'Spine, pelvis, hips.'], ['🫘', 'Soft tissues and organs', 'Liver, spleen, kidneys, psoas.'], ['💎', 'Calcification', 'Kidney stones, gallstones, aortic wall.'], ['📎', 'Artefacts', 'Lines, clips, stents.']]});
  d('chads', {t: 'CHA2DS2-VASc: stroke risk in AF', head: ['Letter', 'Means', 'Points', 'Edna, 77'], keep: true, rows: [
    ['C', 'Congestive heart failure', '1', '0'], ['H', 'Hypertension', '1', '**1**'], ['A2', 'Age 75 or over', '**2**', '**2**'], ['D', 'Diabetes', '1', '0'],
    ['S2', 'Stroke, TIA or clot before', '**2**', '0'], ['V', 'Vascular disease: MI, PAD', '1', '0'], ['A', 'Age 65 to 74', '1', '0'], ['Sc', 'Sex category: female', '1', '**1**'], ['Total', '2 or more → offer anticoagulation', '', '**4**']],
    caps: ['Heart failure scores 1.', 'Hypertension: Edna has it, 1.', 'Age 75 or over scores **2**: Edna is 77.', 'Diabetes 1.', 'Previous stroke or TIA scores **2**.', 'Vascular disease 1.', 'Age 65 to 74 scores 1 instead of 2.', 'Female scores 1.', 'Edna = **4**: about 4 to 5 strokes per 100 people a year without treatment. **Offer a DOAC.**']});
  d('orbit', {t: 'ORBIT: bleeding risk on anticoagulants', head: ['Letter', 'Means', 'Points', 'Elsie, 82'], keep: true, rows: [
    ['O', 'Older: 75 or over', '1', '**1**'], ['R', 'Reduced haemoglobin or anaemia', '**2**', '0'], ['B', 'Bleeding history', '**2**', '0'],
    ['I', 'Insufficient kidney function: eGFR under 60', '1', '0'], ['T', 'Treatment with an antiplatelet', '1', '**1**'], ['Total', '0 to 2 low · 3 medium · 4 or more high', '', '**2: low**']],
    caps: ['Age 75 or over: 1.', 'Anaemia scores 2.', 'Previous bleeding scores 2.', 'Kidneys: eGFR under 60 scores 1.', 'Aspirin with the DOAC scores 1: **stop it if there is no clear reason**.', 'A high score is **not a reason to stop**. It tells you what to fix. **Falls aren\'t either.**']});
  d('news2', {t: 'NEWS2: scores and the response', head: ['', '3', '2', '1', '0', '1', '2', '3'], keep: false, rows: [
    ['Resp rate', '≤8', '', '9–11', '12–20', '', '21–24', '≥25'], ['SpO2 scale 1', '≤91', '92–93', '94–95', '≥96', '', '', ''],
    ['Air or oxygen', '', 'Oxygen', '', 'Air', '', '', ''], ['Systolic BP', '≤90', '91–100', '101–110', '111–219', '', '', '≥220'],
    ['Pulse', '≤40', '', '41–50', '51–90', '91–110', '111–130', '≥131'], ['Consciousness', '', '', '', 'Alert', '', '', '**New confusion, V, P or U**'],
    ['Temperature', '≤35.0', '', '35.1–36.0', '36.1–38.0', '38.1–39.0', '≥39.1', ''], ['Response', '**7 or more: emergency team**', '', '**5 to 6 or a red 3: urgent review**', '0 to 4: ward review', '', '', '']],
    caps: ['Count the breathing for a full 30 to 60 seconds. It changes first.', 'Scale 2 only if the target is 88 to 92%.', 'Any oxygen scores 2.', 'Low blood pressure scores high.', 'Pulse scores on both sides.', '**New confusion scores 3 on its own.**', 'Fever and low temperature both score.', '**The score means nothing unless you escalate:** SBAR to the right person.']});
})();
