/* medengine-STEP1 add-on. Runs inside the STUDY engine through window.ME (site/patches/v340_pack_hooks*.py).
   Views: ⚡ UWorld Deconstruct · ⏱️ timed 20-question block · 🧭 acid-base compass · 🫘 nephron map · 🧪 US lab values ↔ UK.
   Written fresh: nothing here is copied from UWorld, First Aid, Mehlman, Boards and Beyond or Bootcamp.
   The pure parts at the top (abgSolve, LABS, convert) also run under Node in step1/test_step1.js. */
(function () {
  'use strict';

  /* ================================================================ pure: acid-base compass */
  const rd = (x, d) => { const p = Math.pow(10, d == null ? 1 : d); return Math.round(x * p) / p; };
  const num = v => (v === '' || v == null || isNaN(+v)) ? null : +v;
  const CAUSES = {
    hagma: 'MUDPILES: methanol, uraemia, DKA, propylene glycol, iron or isoniazid, lactic acidosis, ethylene glycol, salicylates',
    nagma: 'HARDASS: hyperalimentation, Addison disease, renal tubular acidosis, diarrhoea, acetazolamide, spironolactone, saline infusion. Urine anion gap negative points to the gut, positive to the kidney (RTA)',
    malk: 'Urine Cl⁻ under 20 mEq/L: vomiting, nasogastric suction, past diuretics (fixes with saline) · Urine Cl⁻ over 20 with high BP: hyperaldosteronism, Cushing, Liddle · over 20 with normal BP: current diuretics, Bartter, Gitelman',
    racid: 'Hypoventilation: opioids or sedatives, COPD, neuromuscular weakness (myasthenia, Guillain-Barré, ALS), chest wall disease, obesity hypoventilation',
    ralk: 'Hyperventilation: anxiety or pain, high altitude, pulmonary embolism, early salicylate toxicity, pregnancy, sepsis, liver failure'
  };
  const NAMES = {metAcid: 'metabolic acidosis', metAlk: 'metabolic alkalosis', respAcid: 'respiratory acidosis', respAlk: 'respiratory alkalosis'};

  function abgSolve(v) {
    const ph = num(v.ph), pc = num(v.pco2), hc = num(v.hco3), na = num(v.na), cl = num(v.cl), alb = num(v.alb);
    const osm = num(v.osm), glu = num(v.glu), bun = num(v.bun);
    const out = {ok: false, steps: [], dx: [], extra: [], causes: [], flags: [], ag: null, agc: null, dd: null, og: null};
    if (ph == null || pc == null || hc == null || ph < 6.5 || ph > 8 || pc < 5 || pc > 160 || hc < 1 || hc > 70) { out.err = 'Enter pH, PaCO₂ (mmHg) and HCO₃⁻ (mEq/L).'; return out; }
    out.ok = true;
    const hh = 6.1 + Math.log10(hc / (0.03 * pc));
    out.hh = rd(hh, 2);
    if (Math.abs(hh - ph) > 0.06) out.flags.push('These three numbers do not fit together (Henderson-Hasselbalch gives pH ' + rd(hh, 2) + '): recheck the entry or the sample.');
    out.side = ph < 7.35 ? 'acidaemia' : ph > 7.45 ? 'alkalaemia' : 'normal pH';
    out.steps.push(['1️⃣', 'pH ' + ph, ph < 7.35 ? 'Acidaemia: something is adding acid or removing base.' : ph > 7.45 ? 'Alkalaemia: something is removing acid or adding base.' : 'pH in range: either normal, fully compensated, or two opposite disorders cancelling out.', ph < 7.35 || ph > 7.45 ? 'warn' : '']);
    const ra = pc > 45, rk = pc < 35, ma = hc < 22, mk = hc > 28;
    let prim = [];
    if (ph < 7.4 || (ph === 7.4 && (ra || ma) && !(rk || mk))) {
      if (ma) prim.push('metAcid');
      if (ra) prim.push('respAcid');
    } else if (ph > 7.4 || (ph === 7.4 && (rk || mk) && !(ra || ma))) {
      if (mk) prim.push('metAlk');
      if (rk) prim.push('respAlk');
    } else if (ph === 7.4) {
      if (ra && mk) prim = ['respAcid', 'metAlk'];
      else if (rk && ma) prim = ['respAlk', 'metAcid'];
    }
    if (!prim.length && (ra || rk || ma || mk) && out.side !== 'normal pH') out.flags.push('The pH points one way but neither PaCO₂ nor HCO₃⁻ moved that way: recheck the numbers.');
    out.dx = prim.slice();
    let t2 = !prim.length ? (ra || rk || ma || mk ? 'Values move in a way that a single disorder cannot explain.' : 'PaCO₂ and HCO₃⁻ are both in range: no primary acid-base disorder (unless the anion gap says otherwise).')
      : prim.length > 1 ? 'Two primary processes: ' + prim.map(p => NAMES[p]).join(' plus ') + '.'
      : 'Primary ' + NAMES[prim[0]] + ': the ' + (prim[0].startsWith('met') ? 'bicarbonate (HCO₃⁻ ' + hc + ')' : 'CO₂ (PaCO₂ ' + pc + ')') + ' moved in the same direction as the pH.';
    out.steps.push(['2️⃣', 'Primary process', t2, prim.length ? '' : 'ok']);
    // 3. expected compensation, only meaningful for a single primary process
    if (prim.length === 1) {
      const p = prim[0];
      let t3 = '', tone = 'ok';
      if (p === 'metAcid') {
        const e = 1.5 * hc + 8;
        out.exp = [e - 2, e + 2];
        t3 = 'Winter: expected PaCO₂ = 1.5 × ' + hc + ' + 8 ± 2 = ' + rd(e - 2) + ' to ' + rd(e + 2) + ' mmHg. Measured ' + pc + '.';
        if (pc > e + 2) { out.extra.push('respAcid'); t3 += ' Higher than expected: a respiratory acidosis is hiding as well (tiring, sedated, or lung disease).'; tone = 'bad'; }
        else if (pc < e - 2) { out.extra.push('respAlk'); t3 += ' Lower than expected: a respiratory alkalosis is there too (think salicylates, sepsis).'; tone = 'bad'; }
        else t3 += ' Within range: appropriate respiratory compensation.';
      } else if (p === 'metAlk') {
        const e = 40 + 0.7 * (hc - 24);
        out.exp = [e - 2, e + 2];
        t3 = 'Expected PaCO₂ = 40 + 0.7 × (' + hc + ' − 24) ± 2 = ' + rd(e - 2) + ' to ' + rd(e + 2) + ' mmHg. Measured ' + pc + '.';
        if (pc > e + 2) { out.extra.push('respAcid'); t3 += ' Higher than expected: an added respiratory acidosis.'; tone = 'bad'; }
        else if (pc < e - 2) { out.extra.push('respAlk'); t3 += ' Lower than expected: an added respiratory alkalosis.'; tone = 'bad'; }
        else t3 += ' Within range: appropriate hypoventilation.';
      } else {
        const acid = p === 'respAcid', d = Math.abs(pc - 40);
        const ac = acid ? 24 + 0.1 * d : 24 - 0.2 * d, ch = acid ? 24 + 0.35 * d : 24 - 0.4 * d;
        out.exp = [Math.min(ac, ch) - 2, Math.max(ac, ch) + 2];
        t3 = 'Expected HCO₃⁻: acute ' + rd(ac) + ', chronic ' + rd(ch) + ' (±2) mEq/L for a PaCO₂ of ' + pc + '. Measured ' + hc + '.';
        const hiE = Math.max(ac, ch) + 2, loE = Math.min(ac, ch) - 2;
        if (hc > hiE) { out.extra.push('metAlk'); t3 += ' Above both: a metabolic alkalosis as well.'; tone = 'bad'; }
        else if (hc < loE) { out.extra.push('metAcid'); t3 += ' Below both: a metabolic acidosis as well.'; tone = 'bad'; }
        else {
          const nearA = Math.abs(hc - ac) <= 2, nearC = Math.abs(hc - ch) <= 2;
          out.time = nearA && !nearC ? 'acute' : nearC && !nearA ? 'chronic' : nearA && nearC ? 'acute or chronic' : 'acute on chronic';
          t3 += ' Fits ' + (out.time === 'acute on chronic' ? 'between the two: acute on chronic, or still compensating' : out.time === 'acute or chronic' ? 'either: the change is too small to tell' : 'a ' + out.time + ' ' + NAMES[p]) + '.';
          if (out.time === 'chronic') t3 += acid ? ' The kidney has had 3 to 5 days to hold on to bicarbonate.' : ' The kidney has had days to dump bicarbonate.';
        }
      }
      out.steps.push(['3️⃣', 'Compensation', t3, tone]);
    } else if (prim.length > 1) {
      out.steps.push(['3️⃣', 'Compensation', 'Not applicable: with two primary processes there is nothing to compensate.', 'bad']);
    }
    // 4. anion gap and delta ratio
    if (na != null && cl != null) {
      const ag = na - cl - hc, agc = alb != null ? ag + 2.5 * (4 - alb) : ag;
      out.ag = rd(ag); out.agc = rd(agc);
      let t4 = 'Anion gap = ' + na + ' − (' + cl + ' + ' + hc + ') = ' + rd(ag) + (alb != null && alb < 4 ? '; corrected for albumin ' + alb + ' g/dL: ' + rd(agc) : '') + ' (normal 8 to 12).';
      let tone = 'ok';
      const metAcidSeen = out.dx.includes('metAcid') || out.extra.includes('metAcid');
      if (agc > 12) {
        tone = 'bad';
        if (hc < 24) {
          out.dd = rd((agc - 12) / (24 - hc), 2);
          t4 += ' High: a high anion gap metabolic acidosis. Delta ratio (gap rise ÷ bicarbonate fall) = ' + out.dd + ': ';
          if (out.dd < 0.8) { t4 += 'bicarbonate fell more than the gap rose, so a normal-gap acidosis is mixed in.'; out.causes.push(['➕ Normal gap too', CAUSES.nagma]); out.mixNag = true; }
          else if (out.dd > 2) { t4 += 'bicarbonate fell less than the gap rose, so a metabolic alkalosis (or a chronic CO₂ retainer\'s extra HCO₃⁻) is mixed in.'; out.causes.push(['➕ Alkalosis too', CAUSES.malk]); if (!out.dx.includes('respAcid') && !out.extra.includes('metAlk')) out.extra.push('metAlk'); }
          else t4 += 'the two match, so a single high-gap acidosis.';
        } else {
          t4 += ' High gap with a normal or high bicarbonate: a high-gap acidosis hidden by a metabolic alkalosis.';
          out.causes.push(['➕ Alkalosis too', CAUSES.malk]);
          if (!out.dx.includes('metAlk') && !out.extra.includes('metAlk')) out.extra.push('metAlk');
        }
        if (!metAcidSeen) out.extra.push('metAcid');
        out.causes.unshift(['🔺 High gap', CAUSES.hagma]);
        out.gap = 'high';
      } else {
        out.gap = 'normal';
        if (metAcidSeen) { t4 += ' Normal: a hyperchloraemic, normal anion gap acidosis.'; out.causes.unshift(['🔹 Normal gap', CAUSES.nagma]); }
        else t4 += ' Normal.';
      }
      out.steps.push(['4️⃣', 'Anion gap', t4, tone]);
    } else if (out.dx.includes('metAcid') || out.extra.includes('metAcid')) {
      out.steps.push(['4️⃣', 'Anion gap', 'Add sodium and chloride to split a high-gap acidosis from a normal-gap one.', 'warn']);
    }
    // a metabolic process found by the gap means the bicarbonate was not pure compensation for a respiratory primary
    if (out.time && out.dx.length === 1 && out.dx[0].startsWith('resp') && out.extra.some(x => x.startsWith('met'))) {
      out.time = null;
      const s3 = out.steps.find(x => x[1] === 'Compensation'); if (s3) { s3[2] += ' But the anion gap shows a metabolic process too, so the bicarbonate cannot be read as pure compensation.'; s3[3] = 'bad'; }
    }
    // 5. osmolar gap
    if (osm != null && na != null && glu != null && bun != null) {
      const calc = 2 * na + glu / 18 + bun / 2.8;
      out.og = rd(osm - calc);
      out.steps.push(['5️⃣', 'Osmolar gap', 'Calculated osmolality = 2 × ' + na + ' + ' + glu + '/18 + ' + bun + '/2.8 = ' + rd(calc) + '. Measured ' + osm + ', so the gap is ' + out.og + (out.og > 10 ? ': over 10, so something unmeasured is dissolved in the blood. With a high anion gap, think methanol or ethylene glycol: fomepizole.' : ': normal (under 10).'), out.og > 10 ? 'bad' : 'ok']);
    }
    const all = out.dx.concat(out.extra.filter(x => !out.dx.includes(x)));
    out.all = all;
    if (all.includes('metAcid') && !out.causes.length) out.causes.push(['🔺 Metabolic acidosis', 'Add sodium and chloride to sort the causes by anion gap']);
    if (all.includes('metAlk') && !out.causes.some(c => c[1] === CAUSES.malk)) out.causes.push(['🔸 Metabolic alkalosis', CAUSES.malk]);
    if (all.includes('respAcid')) out.causes.push(['🫁 Respiratory acidosis', CAUSES.racid]);
    if (all.includes('respAlk')) out.causes.push(['🫁 Respiratory alkalosis', CAUSES.ralk]);
    const label = p => p === 'metAcid' && out.gap === 'high' ? 'high anion gap metabolic acidosis' : p === 'metAcid' && out.gap === 'normal' ? 'normal anion gap metabolic acidosis' : (p.startsWith('resp') && out.time && out.dx.length === 1 && out.time !== 'acute or chronic' ? out.time + ' ' : '') + NAMES[p];
    out.summary = !all.length ? 'No acid-base disorder' : all.map(label).join(' + ');
    out.summary = out.summary.charAt(0).toUpperCase() + out.summary.slice(1) + (out.mixNag ? ' with a normal-gap component' : '') + (all.length === 1 && out.dx.length === 1 ? ', appropriately compensated' : '');
    return out;
  }

  /* ================================================================ pure: US lab values with the UK (SI) bridge
     [group, test, US range, US unit, factor US→SI (or 'a1c'), SI unit, bridge note]. Typical adult ranges written for
     revision; on exam day use the lab sheet the exam gives you. */
  const LABS = [
    ['Serum', 'Sodium (Na⁺)', '136–145', 'mEq/L', 1, 'mmol/L', 'Same number in both systems'],
    ['Serum', 'Potassium (K⁺)', '3.5–5.0', 'mEq/L', 1, 'mmol/L', 'Same number'],
    ['Serum', 'Chloride (Cl⁻)', '95–105', 'mEq/L', 1, 'mmol/L', 'Same number'],
    ['Serum', 'Bicarbonate (HCO₃⁻)', '22–28', 'mEq/L', 1, 'mmol/L', 'Same number'],
    ['Serum', 'BUN (blood urea nitrogen)', '7–18', 'mg/dL', 0.357, 'mmol/L urea', 'UK reports urea, not BUN'],
    ['Serum', 'Creatinine', '0.6–1.2', 'mg/dL', 88.4, 'µmol/L', '× 88.4'],
    ['Serum', 'Glucose, fasting', '70–100', 'mg/dL', 0.0555, 'mmol/L', '÷ 18'],
    ['Serum', 'Calcium, total', '8.4–10.2', 'mg/dL', 0.25, 'mmol/L', '÷ 4'],
    ['Serum', 'Magnesium', '1.5–2.0', 'mg/dL', 0.411, 'mmol/L', ''],
    ['Serum', 'Phosphate', '3.0–4.5', 'mg/dL', 0.323, 'mmol/L', ''],
    ['Serum', 'Uric acid', '3.0–8.2', 'mg/dL', 59.48, 'µmol/L', ''],
    ['Serum', 'Osmolality', '275–295', 'mOsm/kg', 1, 'mOsm/kg', 'Calculated: 2 × Na⁺ + glucose/18 + BUN/2.8'],
    ['Serum', 'Albumin', '3.5–5.5', 'g/dL', 10, 'g/L', '× 10'],
    ['Serum', 'Total protein', '6.0–7.8', 'g/dL', 10, 'g/L', '× 10'],
    ['Liver and pancreas', 'Bilirubin, total', '0.1–1.0', 'mg/dL', 17.1, 'µmol/L', '× 17'],
    ['Liver and pancreas', 'Bilirubin, direct', '0.0–0.3', 'mg/dL', 17.1, 'µmol/L', 'Conjugated'],
    ['Liver and pancreas', 'ALT', '10–40', 'U/L', 1, 'U/L', 'Ranges vary by lab'],
    ['Liver and pancreas', 'AST', '12–38', 'U/L', 1, 'U/L', 'AST over 2 × ALT: alcohol'],
    ['Liver and pancreas', 'Alkaline phosphatase', '25–100', 'U/L', 1, 'U/L', 'UK adult ranges run higher, about 30 to 130'],
    ['Liver and pancreas', 'Amylase', '25–125', 'U/L', 1, 'U/L', ''],
    ['Liver and pancreas', 'Lipase', 'lab-specific', 'U/L', 1, 'U/L', 'Over 3 × the upper limit supports pancreatitis'],
    ['Liver and pancreas', 'LDH', '45–200', 'U/L', 1, 'U/L', 'Rises with haemolysis and cell turnover'],
    ['Lipids', 'Cholesterol, total', '<200', 'mg/dL', 0.0259, 'mmol/L', ''],
    ['Lipids', 'LDL, optimal', '<100', 'mg/dL', 0.0259, 'mmol/L', ''],
    ['Lipids', 'HDL', '40–60', 'mg/dL', 0.0259, 'mmol/L', ''],
    ['Lipids', 'Triglycerides', '<150', 'mg/dL', 0.0113, 'mmol/L', ''],
    ['Endocrine', 'TSH', '0.4–4.0', 'µU/mL', 1, 'mU/L', 'Same number'],
    ['Endocrine', 'Free T₄', '0.9–1.7', 'ng/dL', 12.87, 'pmol/L', ''],
    ['Endocrine', 'Cortisol, 8 am', '5–23', 'µg/dL', 27.59, 'nmol/L', ''],
    ['Endocrine', 'Prolactin', '<20', 'ng/mL', 21.2, 'mIU/L', ''],
    ['Endocrine', 'PTH', '10–65', 'pg/mL', 0.106, 'pmol/L', ''],
    ['Endocrine', '25-OH vitamin D', '30–100', 'ng/mL', 2.496, 'nmol/L', 'UK calls over 50 nmol/L sufficient'],
    ['Endocrine', 'HbA1c', '<5.7', '%', 'a1c', 'mmol/mol', 'UK uses mmol/mol: diabetes at 48 (6.5%)'],
    ['Blood count', 'Haemoglobin, men', '13.5–17.5', 'g/dL', 10, 'g/L', '× 10'],
    ['Blood count', 'Haemoglobin, women', '12.0–16.0', 'g/dL', 10, 'g/L', '× 10'],
    ['Blood count', 'Haematocrit, men', '41–53', '%', 0.01, 'L/L', ''],
    ['Blood count', 'Haematocrit, women', '36–46', '%', 0.01, 'L/L', ''],
    ['Blood count', 'MCV', '80–100', 'fL', 1, 'fL', 'Same number'],
    ['Blood count', 'White cells', '4,500–11,000', '/mm³', 0.001, '× 10⁹/L', '÷ 1000'],
    ['Blood count', 'Platelets', '150,000–400,000', '/mm³', 0.001, '× 10⁹/L', '÷ 1000'],
    ['Blood count', 'Reticulocytes', '0.5–1.5', '% of red cells', 1, '%', ''],
    ['Blood count', 'ESR, men', '0–15', 'mm/h', 1, 'mm/h', 'Same number'],
    ['Blood count', 'Ferritin, men', '20–250', 'ng/mL', 1, 'µg/L', 'Same number'],
    ['Blood count', 'Ferritin, women', '10–120', 'ng/mL', 1, 'µg/L', 'Same number'],
    ['Blood count', 'Iron', '50–170', 'µg/dL', 0.179, 'µmol/L', ''],
    ['Blood count', 'TIBC', '250–400', 'µg/dL', 0.179, 'µmol/L', ''],
    ['Clotting', 'Prothrombin time', '11–15', 's', 1, 's', 'INR about 1'],
    ['Clotting', 'aPTT', '25–40', 's', 1, 's', ''],
    ['Clotting', 'Fibrinogen', '200–400', 'mg/dL', 0.01, 'g/L', '÷ 100'],
    ['Arterial gas', 'pH', '7.35–7.45', '', 1, '', ''],
    ['Arterial gas', 'PaCO₂', '35–45', 'mmHg', 0.133, 'kPa', 'UK gases read in kPa: ÷ 7.5'],
    ['Arterial gas', 'PaO₂', '75–105', 'mmHg', 0.133, 'kPa', '÷ 7.5'],
    ['Arterial gas', 'Lactate', '0.5–2.2', 'mmol/L', 1, 'mmol/L', ''],
    ['CSF', 'Opening pressure', '70–180', 'mm H₂O', 0.1, 'cm H₂O', 'UK quotes cm H₂O'],
    ['CSF', 'Glucose', '40–70', 'mg/dL', 0.0555, 'mmol/L', 'About 60% of the blood glucose'],
    ['CSF', 'Protein', '<40', 'mg/dL', 0.01, 'g/L', ''],
    ['CSF', 'White cells', '0–5', '/mm³', 1, '/mm³', 'Mostly lymphocytes'],
    ['Urine', 'Osmolality', '50–1200', 'mOsm/kg', 1, 'mOsm/kg', 'Follows ADH'],
    ['Urine', 'Protein', '<150', 'mg/24 h', 0.001, 'g/24 h', ''],
    ['Urine', 'Creatinine clearance, men', '97–137', 'mL/min', 1, 'mL/min', '']
  ];
  const fmtN = x => { const a = Math.abs(x); const d = a >= 100 ? 0 : a >= 10 ? 1 : a >= 1 ? 2 : 3; return String(+x.toFixed(d)); };
  function convert(row, x, back) {
    const f = row[4];
    if (f === 'a1c') return back ? x / 10.929 + 2.15 : (x - 2.15) * 10.929;
    return back ? x / f : x * f;
  }
  function siRange(row) {
    if (row[4] === 1 || !/\d/.test(row[2])) return row[2];
    return row[2].replace(/[\d,.]+/g, m => { const v = convert(row, +m.replace(/,/g, '')); return row[4] === 'a1c' ? String(Math.round(v)) : fmtN(v); });
  }

  const API = {abgSolve, LABS, convert, siRange, fmtN};
  if (typeof module !== 'undefined' && module.exports) { module.exports = API; return; }
  window.MEDENGINE_STEP1 = API;
  window.ME_EXT = (window.ME_EXT || []).concat([boot]);

  /* ================================================================ the add-on */
  function boot(ME) {
    const D = ME.D, esc = ME.esc, U = ME.UNITS, W = ME.WEEKS;
    const $ = (q, r) => (r || document).querySelector(q), $$ = (q, r) => Array.from((r || document).querySelectorAll(q));
    const st = () => { const S = ME.S; S.s1 = S.s1 || {}; const s = S.s1; s.blocks = s.blocks || []; s.dc = s.dc || []; return s; };
    const rich = t => esc(t).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>');
    const uByName = {}; U.forEach(u => { uByName[u.name.toLowerCase()] = u.i; });
    const pilotN = U.filter(u => u.pilot).length;
    const s1 = D.s1 || {sys: []};

    /* --- systems: the USMLE content outline instead of the FFP systems --- */
    if (window.MEV && s1.sys.length) {
      MEV.SYS = s1.sys;
      MEV.unitSys = (i) => (U[i] && U[i].sys) || 'multi';
    }
    /* --- the reference ranges inside every question: US units with the UK value alongside --- */
    if (ME.refRanges) {
      const groups = [];
      LABS.forEach(r => { let g = groups.find(x => x[0] === r[0]); if (!g) groups.push(g = [r[0], []]); g[1].push([r[1], r[2] + (r[3] ? ' ' + r[3] : '') + (r[4] !== 1 && /\d/.test(r[2]) ? '  (UK ' + siRange(r) + ' ' + r[5] + ')' : '')]); });
      ME.refRanges.splice(0, ME.refRanges.length, ...groups);
    }

    /* ---------------- navigation ---------------- */
    ME.nav('top', 'block', '⏱️', 'Timed block · 20 Q', () => st().blocks.length || null);
    ME.nav('top', 'deconstruct', '⚡', 'UWorld Deconstruct', () => st().dc.length || null);
    ME.nav('top', 'abg', '🧭', 'Acid-base compass');
    ME.nav('top', 'nephron', '🫘', 'Nephron map');
    ME.nav('top', 'atlas', '🫀', 'System maps');
    ME.nav('top', 'labs', '🧪', 'US lab values ↔ UK');

    /* ---------------- home: the Step 1 loop ---------------- */
    ME.EXT.homeTop = () => {
      const s = st(), done = s.blocks.filter(b => b.n), avg = done.length ? Math.round(done.reduce((a, b) => a + b.right / b.n, 0) / done.length * 100) : null;
      const days = s.exam ? Math.ceil((new Date(s.exam + 'T09:00:00') - Date.now()) / 864e5) : null;
      const nq = (D.hq.q || []).length;
      return '<section class="panel s1-home"><div class="s1-hrow"><b class="s1-ttl">🎯 Step 1 · ' + U.length + ' topics · ' + nq + ' questions</b><label class="s1-date">Exam date <input type="date" id="s1Exam" value="' + esc(s.exam || '') + '"></label>'
        + (days != null ? '<span class="s1-cd' + (days < 30 ? ' soon' : '') + '">' + (days >= 0 ? days + ' days to go' : 'exam passed') + '</span>' : '') + '</div>'
        + '<div class="s1-tiles"><div><b>' + done.length + '</b><span>timed blocks' + (avg != null ? ' · ' + avg + '% average' : '') + '</span></div><div><b>' + s.dc.length + '</b><span>UWorld misses deconstructed</span></div><div><b>' + U.length + '</b><span>topics with triggers (breadth)</span></div><div><b>' + pilotN + '</b><span>topics in deep mode: all 16 chapters</span></div></div>'
        + '<ol class="s1-loop"><li><button class="btn primary sm" data-go="block">⏱️ 20 questions in 30 minutes</button> timed, no feedback, like the real block</li>'
        + '<li><button class="btn sm" data-go="deconstruct">⚡ Deconstruct every miss</button> 4 boxes, a twin question and Anki cards from each UWorld miss</li>'
        + '<li><button class="btn sm" data-go="triggers">🧲 Triggers for that chapter</button> the scene, the flip word, the answer</li>'
        + '<li><button class="btn sm" data-go="fw">↕ Domino arrows</button> primary insult, knock-on, compensation; then 🔀 change the film</li></ol>'
        + '<p class="hint s1-fmt">The exam now runs in blocks of up to 20 questions with 30 minutes each, so every block here is 20 questions at 90 seconds a question. Stems use US units and drug names; the explanations stay in British English.</p></section>';
    };
    document.addEventListener('change', e => {
      if (e.target && e.target.id === 's1Exam') { st().exam = e.target.value; ME.save(); ME.render(); }
    });

    /* ---------------- each topic: what it is and how to use it ---------------- */
    ME.EXT.unitTop = u => {
      const sys = (s1.sys.find(x => x[0] === u.sys) || [])[1] || '';
      const nq = (D.hq.q || []).filter(q => q.k === String(u.i)).length;
      return '<div class="s1-unit"><span class="s1-chip">' + esc(sys) + '</span>' + (u.disc || []).map(d => '<span class="s1-chip ghost">' + esc(d) + '</span>').join('')
        + (u.pilot ? '<span class="s1-chip deep">🔬 Deep mode: notes, ' + nq + ' questions, arrows</span>' : '<span class="s1-chip">🦴 Breadth: triggers</span>')
        + '<button class="btn ghost sm" data-s1dc="' + u.i + '">⚡ Deconstruct a UWorld miss here</button></div>'
        + (u.pilot ? '' : '<p class="hint s1-uhint">Deep notes, questions and arrows arrive chapter by chapter; renal is the first. Until then: drill these triggers (✍️ Fill blanks), and turn every UWorld miss on this topic into a twin question with ⚡ Deconstruct.</p>');
    };
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-s1dc]'); if (!b) return;
      dc.unit = +b.dataset.s1dc; ME.go({view: 'deconstruct'});
    });

    /* ================================================================ ⚡ UWorld Deconstruct */
    const dc = {unit: null, busy: false, err: '', out: null, img: null, open: null, manual: false};
    const ERRS = [['knowledge', '📚 Did not know the fact'], ['step', '🔗 Missed a step in the chain'], ['misread', '👀 Missed a red flag'], ['changed', '🔄 Changed a right answer'], ['split', '🎲 Down to two, picked wrong'], ['rushed', '⏱️ Rushed']];
    let AI = null, AI_IMG = false;
    (async () => {
      try { if (window.claude && window.claude.use) AI = await window.claude.use('sample'); } catch (e) { AI = null; }
      try { const lim = AI && AI.limits ? await AI.limits() : null; AI_IMG = !!(lim && lim.images); } catch (e) { AI_IMG = false; }
      if (ME.route.view === 'deconstruct') ME.render();
    })();
    const topicList = () => U.map(u => u.name).join(' · ');
    function prompt(paste, note, err) {
      return 'You are a USMLE Step 1 tutor. A student missed a question in a question bank. Below is what they pasted (the question, the explanation, or their own notes), and maybe a screenshot.\n'
        + 'Teach the point back in your own words. Never quote or closely paraphrase the pasted text, and never reproduce its stem, options or explanation: everything you write must be new.\n'
        + 'Return JSON only, exactly this shape:\n'
        + '{"topic": "short name of the tested concept",\n "unit": "the closest name from TOPICS, copied exactly, or an empty string",\n'
        + ' "error": "one of knowledge, step, misread, changed, split, rushed: your best guess of why it was missed",\n'
        + ' "red_flags": ["2 to 4 short stem clues that decide this kind of question"],\n'
        + ' "money_line": "one sentence: the single fact that decides it",\n'
        + ' "inflow": ["3 to 6 short links from the root cause to what the question asks about, each under 12 words"],\n'
        + ' "film": [{"if": "one detail of the case changes", "then": "what the answer becomes"}, 3 or 4 of these, ideally the worlds where the wrong options would be right],\n'
        + ' "arrows": {"scene": "a fresh one-sentence scenario", "rows": [["variable", "↑ or ↓ or ↔", "p for primary insult, k for knock-on, c for compensation"]], "key": "the logic in one line"} or null if arrows do not fit,\n'
        + ' "twin": {"stem": "a NEW 60 to 90 word USMLE-style vignette that tests the same fact with a different patient, US units and US drug names", "question": "the lead-in", "options": ["5 options in alphabetical order"], "answer": index of the right option (0 to 4), "why": "2 or 3 sentences"},\n'
        + ' "cards": [["front", "back"], 3 to 6 Anki cards, one fact each]}\n'
        + 'Rules: British spelling in money_line, inflow, film, why and cards; US units and drug names inside the twin stem; no em dashes anywhere.\n'
        + 'TOPICS: ' + topicList() + '\n'
        + (err ? 'The student says the miss was: ' + err + '\n' : '') + (note ? 'Student note: ' + note + '\n' : '')
        + 'PASTE:\n' + paste.slice(0, 12000);
    }
    function clean(j, unitHint) {
      const A = x => Array.isArray(x) ? x : [], S = x => typeof x === 'string' ? x.replace(/—/g, ', ').trim() : '';
      const o = {id: 'dc' + Date.now().toString(36), at: Date.now(), topic: S(j.topic) || 'Untitled', err: S(j.error),
        rf: A(j.red_flags).map(S).filter(Boolean).slice(0, 5), money: S(j.money_line), inflow: A(j.inflow).map(S).filter(Boolean).slice(0, 7),
        film: A(j.film).map(f => [S(f && f.if), S(f && f.then)]).filter(f => f[0] && f[1]).slice(0, 5), cards: A(j.cards).map(c => [S(c && c[0]), S(c && c[1])]).filter(c => c[0] && c[1]).slice(0, 8)};
      const nm = S(j.unit).toLowerCase();
      o.u = unitHint != null ? unitHint : uByName[nm] != null ? uByName[nm] : (() => { const k = Object.keys(uByName).find(n => nm && (n.includes(nm) || nm.includes(n))); return k ? uByName[k] : null; })();
      const ar = j.arrows;
      if (ar && A(ar.rows).length >= 2 && S(ar.scene)) {
        const rows = A(ar.rows).filter(r => r && S(r[0]) && /^[↑↓↔]+$/.test(S(r[1]))).slice(0, 6);
        if (rows.length >= 2) o.ar = {s: S(ar.scene), v: rows.map(r => [S(r[0]), S(r[1])]), r: rows.map(r => /^[pkc]$/.test(S(r[2])) ? S(r[2]) : '-').join(''), k: S(ar.key)};
      }
      const tw = j.twin;
      if (tw && S(tw.stem) && A(tw.options).length >= 4 && Number.isInteger(+tw.answer) && +tw.answer >= 0 && +tw.answer < A(tw.options).length)
        o.tw = {s: S(tw.stem), ql: S(tw.question) || 'Which of the following is the most likely answer?', o: A(tw.options).map(S).slice(0, 6), a: +tw.answer, w: S(tw.why)};
      return o;
    }
    function arKey(o) {
      if (!o.ar) return null;
      const id = 's1-' + o.id;
      let i = D.ar.findIndex(a => a.id === id);
      if (i < 0) { D.ar.push({id, f: '⚡ From my misses', s: o.ar.s, v: o.ar.v, r: o.ar.r.replace(/-/g, '') ? o.ar.r : '', k: o.ar.k || '', m: [], uk: '', u: o.u != null ? [o.u] : [], fl: []}); i = D.ar.length - 1; }
      return i;
    }
    function boxesHtml(o) {
      return '<div class="s1-4box">'
        + '<div class="s1-b rf"><span class="s1-bk">🎯 Red flags</span><ul>' + o.rf.map(x => '<li>' + rich(x) + '</li>').join('') + '</ul></div>'
        + '<div class="s1-b mo"><span class="s1-bk">💰 Money line</span><p>' + rich(o.money) + '</p></div>'
        + '<div class="s1-b fl"><span class="s1-bk">🌊 Inflow → outflow</span><p class="s1-chain">' + o.inflow.map(rich).join(' <span>→</span> ') + '</p></div>'
        + '<div class="s1-b cf"><span class="s1-bk">🔀 Change the film</span><ul>' + o.film.map(f => '<li>If ' + rich(f[0]) + ' <b>→ ' + rich(f[1]) + '</b></li>').join('') + '</ul></div></div>';
    }
    function twinHtml(o) {
      if (!o.tw) return '';
      const t = o.tw, L = 'ABCDEF';
      return '<div class="s1-twin" data-tw="' + o.id + '"><div class="s1-bk">🔗 Twin question · same fact, new patient</div><p>' + rich(t.s) + '</p><p><b>' + rich(t.ql) + '</b></p>'
        + t.o.map((x, k) => '<button class="hq-o s1-two" data-twp="' + o.id + '|' + k + '"><span class="hq-l">' + L[k] + '</span><span class="hq-ot">' + esc(x) + '</span></button>').join('')
        + '<div class="s1-tww" hidden>' + rich(t.w) + '</div></div>';
    }
    function cardsHtml(o) {
      if (!o.cards.length) return '';
      return '<details class="s1-cards"><summary>🃏 ' + o.cards.length + ' Anki card' + (o.cards.length > 1 ? 's' : '') + '</summary><table>' + o.cards.map(c => '<tr><td>' + rich(c[0]) + '</td><td>' + rich(c[1]) + '</td></tr>').join('') + '</table>'
        + '<div class="toolbar"><button class="btn sm" data-dccopy="' + o.id + '">📋 Copy for Anki (tab-separated)</button></div></details>';
    }
    function dcCard(o, open) {
      const u = o.u != null ? U[o.u] : null, e = ERRS.find(x => x[0] === o.err);
      const k = arKey(o);
      return '<article class="panel s1-dc" id="DC-' + o.id + '"><div class="s1-dch"><b>' + esc(o.topic) + '</b>' + (u ? '<button class="ulink" data-u="' + u.i + '" data-mode="fill">↗ ' + esc(u.name) + '</button>' : '') + (e ? '<span class="s1-chip ghost">' + e[1] + '</span>' : '')
        + '<span class="grow"></span><span class="hint">' + new Date(o.at).toLocaleDateString('en-GB') + '</span><button class="btn ghost sm" data-dcdel="' + o.id + '" title="Delete this card">🗑</button></div>'
        + boxesHtml(o) + (k != null ? '<div class="s1-ar">' + ME.arHtml(k) + '</div>' : '') + twinHtml(o) + cardsHtml(o) + '</article>';
    }
    function viewDeconstruct(m) {
      const s = st(), list = s.dc.slice().reverse();
      const sel = '<select id="dcUnit" class="jsel"><option value="">Let the AI pick the topic</option>' + W.map(w => '<optgroup label="' + esc(w.name) + '">' + U.filter(u => u.w === w.id).map(u => '<option value="' + u.i + '"' + (dc.unit === u.i ? ' selected' : '') + '>' + esc(u.name) + '</option>').join('') + '</optgroup>').join('') + '</select>';
      let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">⚡ Deconstruct</span><span>' + s.dc.length + ' saved</span></div><h1>Turn a UWorld miss into a weapon</h1>'
        + '<p class="hint" style="margin:0">Paste the question and explanation you just missed, or drop a screenshot. It goes only to your AI (Claude here, or your own key on the website) and is never stored; what you keep is the deconstruction in fresh words: the 4 boxes, the domino arrows, a twin question and Anki cards.</p></div>';
      h += '<div class="panel s1-dcin"><textarea id="dcIn" rows="7" placeholder="Paste the stem, the options and the explanation, or just your own notes on what you missed…"></textarea>'
        + '<div class="s1-drop" id="dcDrop" tabindex="0">' + (dc.img ? '🖼️ Screenshot attached · <button class="btn ghost sm" data-dcimgx>remove</button>' : '📸 Drop or paste a screenshot here' + (AI_IMG ? '' : ' (needs an AI that reads images)')) + '</div>'
        + '<div class="s1-errs">' + ERRS.map(([k, l]) => '<button class="chip' + (dc.err === k ? ' on' : '') + '" data-dcerr="' + k + '">' + l + '</button>').join('') + '</div>'
        + '<input id="dcNote" class="search" placeholder="Optional: why you picked what you picked" style="padding-left:14px">'
        + '<div class="toolbar">' + sel + '<span class="grow"></span>'
        + (dc.busy ? '<span class="rmx-busy">Deconstructing…</span>' : AI ? '<button class="btn primary" data-dcgo>⚡ Deconstruct</button>' : '<span class="hint">🔑 Add your AI key (top right) for the AI version</span>')
        + '<button class="btn" data-dcmanual>✍️ By hand</button></div>' + (dc.err2 ? '<p class="s1-err">' + esc(dc.err2) + '</p>' : '') + '</div>';
      if (dc.manual) h += manualForm();
      if (dc.out) h += '<h2 class="s1-h2">Just now</h2>' + dcCard(dc.out, true);
      const rest = list.filter(o => !dc.out || o.id !== dc.out.id);
      if (rest.length) {
        h += '<div class="toolbar s1-dctools"><h2 class="s1-h2 grow">Saved · ' + s.dc.length + '</h2>' + (s.dc.some(o => o.tw) ? '<button class="btn sm" data-dctwins>🔗 Drill all twins</button>' : '') + '<button class="btn sm" data-dccopyall>📋 Copy every Anki card</button></div>';
        h += rest.map(o => '<details class="s1-dcfold"><summary><b>' + esc(o.topic) + '</b><span class="hint"> · ' + (o.u != null ? esc(U[o.u].name) + ' · ' : '') + new Date(o.at).toLocaleDateString('en-GB') + '</span></summary>' + dcCard(o) + '</details>').join('');
      }
      m.innerHTML = h + '</div>';
    }
    function manualForm() {
      return '<div class="panel s1-man"><b>✍️ Your own 4 boxes</b><input id="mTopic" class="search" placeholder="Concept, e.g. Liddle syndrome vs Conn syndrome" style="padding-left:14px">'
        + '<textarea id="mRf" rows="2" placeholder="🎯 Red flags, one per line"></textarea><textarea id="mMo" rows="2" placeholder="💰 Money line: the one fact that decides it"></textarea>'
        + '<textarea id="mIn" rows="2" placeholder="🌊 Inflow → outflow: cause → step → step → what they ask (separate with →)"></textarea>'
        + '<textarea id="mCf" rows="3" placeholder="🔀 Change the film, one per line: if X changes → answer Y"></textarea>'
        + '<textarea id="mCards" rows="3" placeholder="🃏 Anki cards, one per line: front | back"></textarea><div class="toolbar"><span class="grow"></span><button class="btn primary" data-dcmsave>Save card</button></div></div>';
    }
    async function runAi() {
      const paste = ($('#dcIn') || {}).value || '', note = ($('#dcNote') || {}).value || '';
      if (!AI || dc.busy) return;
      if (paste.trim().length < 40 && !dc.img) { dc.err2 = 'Paste a bit more (the stem and the explanation), or attach a screenshot.'; return ME.render(); }
      const unitSel = ($('#dcUnit') || {}).value;
      dc.unit = unitSel === '' ? null : +unitSel;
      dc.busy = true; dc.err2 = ''; ME.render();
      const ta = $('#dcIn'); if (ta) ta.value = paste;
      try {
        const opts = {modelTier: 'quick', maxTokens: 2600, cache: false};
        if (dc.img && AI_IMG) opts.images = dc.img;
        const errTxt = (ERRS.find(x => x[0] === dc.err) || [])[1] || '';
        const j = await AI.json(prompt(paste, note, errTxt), opts);
        const o = clean(j || {}, dc.unit);
        if (!o.money || !o.rf.length) throw {code: 'thin'};
        if (dc.err && !o.err) o.err = dc.err;
        st().dc.push(o); dc.out = o; dc.img = null; ME.addXp(10); ME.save();
        if (ta) ta.value = '';
      } catch (e) {
        const c = e && e.code;
        dc.err2 = c === 'thin' ? 'The AI reply was too thin to keep. Try again, or paste more of the explanation.' : c === 'invalid_json' ? 'The AI reply came back garbled. Try again.' : c === 'rate_limited' ? 'Too many requests just now. Wait a minute.' : 'The AI could not answer (' + (c || (e && e.message) || 'error') + '). Try again, or use ✍️ By hand.';
        if (c === 'sign_in_required' && window.medengineAccount) window.medengineAccount.open(c);
      }
      dc.busy = false; ME.render();
      const keep = $('#dcIn'); if (keep && dc.err2) keep.value = paste;
    }
    function saveManual() {
      const v = id => (($('#' + id) || {}).value || '').trim(), lines = id => v(id).split('\n').map(x => x.trim()).filter(Boolean);
      if (!v('mTopic') || !v('mMo')) return ME.toast('Add at least the concept and the money line');
      const unitSel = ($('#dcUnit') || {}).value;
      const o = {id: 'dc' + Date.now().toString(36), at: Date.now(), topic: v('mTopic'), err: dc.err || '', rf: lines('mRf'), money: v('mMo'),
        inflow: v('mIn').split(/→|->/).map(x => x.trim()).filter(Boolean), film: lines('mCf').map(l => l.split(/→|->/).map(x => x.trim())).filter(f => f.length > 1).map(f => [f[0].replace(/^if\s+/i, ''), f.slice(1).join(' → ')]),
        cards: lines('mCards').map(l => l.split('|').map(x => x.trim())).filter(c => c.length > 1 && c[0] && c[1]).map(c => [c[0], c.slice(1).join(' | ')]), u: unitSel === '' ? null : +unitSel};
      st().dc.push(o); dc.out = o; dc.manual = false; ME.addXp(5); ME.save(); ME.render();
    }
    const tsv = list => list.flatMap(o => o.cards.map(c => [c[0], c[1], 'step1 ' + (o.u != null ? U[o.u].w : 'misc')].map(x => String(x).replace(/[\t\n]+/g, ' ')).join('\t'))).join('\n');
    async function copy(text, what) {
      try { await navigator.clipboard.writeText(text); ME.toast('Copied ' + what); }
      catch (e) { const t = document.createElement('textarea'); t.value = text; document.body.appendChild(t); t.select(); try { document.execCommand('copy'); ME.toast('Copied ' + what); } catch (er) { ME.toast('Copy blocked: select and copy by hand'); } t.remove(); }
    }
    function readImg(file) {
      if (!file || !/^image\//.test(file.type)) return;
      if (file.size > 4.5e6) return ME.toast('That image is over 4.5 MB: crop it first');
      dc.img = file; ME.render();
    }
    document.addEventListener('click', e => {
      const t = e.target.closest && e.target.closest('[data-dcgo],[data-dcmanual],[data-dcmsave],[data-dcerr],[data-dcdel],[data-dccopy],[data-dccopyall],[data-dcimgx],[data-twp],[data-dctwins]');
      if (!t || ME.route.view !== 'deconstruct' && !t.dataset.twp) return;
      const d = t.dataset, s = st();
      if (d.dcgo != null) runAi();
      else if (d.dcmanual != null) { dc.manual = !dc.manual; const p = ($('#dcIn') || {}).value; ME.render(); if (p) $('#dcIn').value = p; }
      else if (d.dcmsave != null) saveManual();
      else if (d.dcerr) { dc.err = dc.err === d.dcerr ? '' : d.dcerr; $$('[data-dcerr]').forEach(b => b.classList.toggle('on', b.dataset.dcerr === dc.err)); }
      else if (d.dcdel) { if (!confirm('Delete this deconstruction?')) return; s.dc = s.dc.filter(o => o.id !== d.dcdel); if (dc.out && dc.out.id === d.dcdel) dc.out = null; ME.save(); ME.render(); }
      else if (d.dccopy) { const o = s.dc.find(x => x.id === d.dccopy); if (o) copy(tsv([o]), o.cards.length + ' cards'); }
      else if (d.dccopyall) copy(tsv(s.dc), s.dc.reduce((a, o) => a + o.cards.length, 0) + ' cards');
      else if (d.dcimgx != null) { dc.img = null; ME.render(); }
      else if (d.dctwins != null) { twinRun(); }
      else if (d.twp) {
        const [id, k] = d.twp.split('|'), o = s.dc.find(x => x.id === id) || (tw.cur && tw.cur.id === id ? tw.cur : null); if (!o || !o.tw) return;
        const box = t.closest('.s1-twin'); if (box.classList.contains('done')) return;
        box.classList.add('done');
        $$('[data-twp]', box).forEach(b => { const kk = +b.dataset.twp.split('|')[1]; b.disabled = true; b.classList.add(kk === o.tw.a ? 'ok' : kk === +k ? 'bad' : 'dim'); });
        $('.s1-tww', box).hidden = false;
        o.tws = o.tws || [0, 0]; o.tws[0]++; if (+k === o.tw.a) { o.tws[1]++; ME.addXp(3); } ME.save();
        if (tw.on) { const nx = document.createElement('div'); nx.className = 'toolbar'; nx.innerHTML = '<span class="grow"></span><button class="btn primary" data-twnext>Next twin →</button>'; box.appendChild(nx); }
      }
    });
    document.addEventListener('paste', e => { if (ME.route.view !== 'deconstruct') return; const f = Array.from((e.clipboardData || {}).files || [])[0]; if (f && /^image\//.test(f.type)) { e.preventDefault(); readImg(f); } });
    document.addEventListener('dragover', e => { if (e.target.closest && e.target.closest('#dcDrop')) e.preventDefault(); });
    document.addEventListener('drop', e => { const z = e.target.closest && e.target.closest('#dcDrop'); if (!z) return; e.preventDefault(); readImg((e.dataTransfer.files || [])[0]); });
    /* drill every saved twin in a row */
    const tw = {on: false, q: [], i: 0, cur: null};
    function twinRun() {
      tw.q = st().dc.filter(o => o.tw).sort(() => Math.random() - 0.5); tw.i = 0; tw.on = true; drawTwin();
    }
    function drawTwin() {
      const m = $('#main'), o = tw.q[tw.i];
      if (!o) { tw.on = false; ME.toast('All twins done'); return ME.render(); }
      tw.cur = o;
      m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🔗 Twin ' + (tw.i + 1) + ' / ' + tw.q.length + '</span><span class="grow"></span><button class="btn ghost sm" data-go="deconstruct">✕ Stop</button></div></div>' + twinHtml(o) + '</div>';
    }
    document.addEventListener('click', e => { if (e.target.closest && e.target.closest('[data-twnext]')) { tw.i++; drawTwin(); } });
    ME.view('deconstruct', m => { tw.on = false; viewDeconstruct(m); });

    /* ================================================================ ⏱️ timed block */
    const blk = {cfg: {n: 20, src: 'all', ch: '', st: 'any'}};
    const L5 = 'ABCDEFGHI';
    const seen = () => { const m = {}; (ME.hqRuns() || []).forEach(r => Object.entries(r.pk || {}).forEach(([id, p]) => { const q = ME.hqItem(id); if (q) m[id] = m[id] === false ? false : p === q.a; })); st().blocks.forEach(b => (b.ids || []).forEach((id, j) => { const q = ME.hqItem(id), p = b.pk[j]; if (q && p != null) m[id] = (m[id] !== false) && p === q.a; })); return m; };
    function pool() {
      const c = blk.cfg, sn = seen();
      let list = (D.hq.q || []).slice();
      if (c.src === 'pilot') list = list.filter(q => U[+q.k] && U[+q.k].w === 'renal');
      if (c.ch) list = list.filter(q => U[+q.k] && U[+q.k].w === c.ch);
      if (c.st === 'new') list = list.filter(q => !(q.id in sn));
      if (c.st === 'miss') list = list.filter(q => sn[q.id] === false);
      return list;
    }
    function viewBlockSetup(m) {
      const s = st(), c = blk.cfg, n = pool().length, cur = s.cur;
      const chs = W.filter(w => (D.hq.q || []).some(q => U[+q.k] && U[+q.k].w === w.id));
      let h = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">⏱️ Timed block</span><span>' + s.blocks.length + ' done</span></div><h1>One block, exam rules</h1>'
        + '<p class="hint" style="margin:0">20 questions, 30 minutes, no feedback until the end. Mark and strike out as you go, open 🧪 lab values whenever you like, then review every answer with the 4 boxes.</p></div>';
      if (cur) h += '<div class="panel s1-resume"><b>⏸ A block is still open</b> · question ' + (cur.i + 1) + ' of ' + cur.ids.length + ' · ' + mmss(cur.left) + ' left<div class="toolbar"><button class="btn primary" data-bkresume>Carry on</button><button class="btn ghost" data-bkend>End it now</button></div></div>';
      h += '<div class="panel s1-setup"><div class="s1-row"><span>Questions</span>' + [10, 20, 40].map(k => '<button class="chip' + (c.n === k ? ' on' : '') + '" data-bkn="' + k + '">' + k + (k === 20 ? ' · real block' : '') + '</button>').join('') + '</div>'
        + '<div class="s1-row"><span>From</span><button class="chip' + (c.src === 'all' && !c.ch ? ' on' : '') + '" data-bksrc="all">Everything</button><button class="chip' + (c.src === 'pilot' ? ' on' : '') + '" data-bksrc="pilot">🫘 Renal focus</button>'
        + '<select class="jsel" id="bkCh"><option value="">Any chapter</option>' + chs.map(w => '<option value="' + w.id + '"' + (c.ch === w.id ? ' selected' : '') + '>' + esc(w.name) + '</option>').join('') + '</select></div>'
        + '<div class="s1-row"><span>Which</span>' + [['any', 'Any'], ['new', '🆕 Unseen'], ['miss', '🔥 Missed before']].map(([k, l]) => '<button class="chip' + (c.st === k ? ' on' : '') + '" data-bkst="' + k + '">' + l + '</button>').join('') + '</div>'
        + '<div class="toolbar"><span class="hint grow">' + n + ' questions match · ' + Math.min(n, c.n) + ' in this block · ' + Math.round(Math.min(n, c.n) * 1.5) + ' minutes</span><button class="btn primary" data-bkstart' + (n ? '' : ' disabled') + '>▶ Start the block</button></div></div>';
      const done = s.blocks.slice().reverse().slice(0, 12);
      if (done.length) h += '<div class="panel"><b>Past blocks</b><table class="s1-hist"><tr><th>Date</th><th>Score</th><th>Time used</th><th></th></tr>' + done.map(b => '<tr><td>' + new Date(b.at).toLocaleDateString('en-GB') + '</td><td><b>' + Math.round(b.right / b.n * 100) + '%</b> (' + b.right + '/' + b.n + ')</td><td>' + mmss(b.used) + '</td><td>' + (b.rid ? '<button class="btn ghost sm" data-bkrev="' + b.rid + '">Review</button>' : '') + '</td></tr>').join('') + '</table></div>';
      m.innerHTML = h + '</div>';
    }
    const mmss = s => { s = Math.max(0, Math.round(s || 0)); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
    let tick = 0;
    function startBlock() {
      const list = pool().sort(() => Math.random() - 0.5).slice(0, blk.cfg.n);
      if (!list.length) return;
      st().cur = {ids: list.map(q => q.id), i: 0, pk: {}, x: {}, mk: {}, left: list.length * 90, total: list.length * 90, at: Date.now()};
      ME.save(); drawBlock();
    }
    function drawBlock() {
      const s = st(), c = s.cur, m = $('#main'); if (!c) return ME.go({view: 'block'});
      document.body.classList.add('s1-examing');
      const it = ME.hqItem(c.ids[c.i]); if (!it) { c.ids.splice(c.i, 1); return drawBlock(); }
      const xs = c.x[it.id] || [], pk = c.pk[it.id];
      let h = '<div class="wrap s1-exam' + (blk.labs ? ' labs-open' : '') + '"><div class="s1-bar"><b>Item ' + (c.i + 1) + ' of ' + c.ids.length + '</b><button class="btn sm' + (c.mk[it.id] ? ' on' : '') + '" data-bkmark>🚩 ' + (c.mk[it.id] ? 'Marked' : 'Mark') + '</button>'
        + '<button class="btn sm" data-bklabs>🧪 Lab values</button><span class="grow"></span><span class="s1-clock' + (c.left < 300 ? ' low' : '') + '" id="bkClock">⏱ ' + mmss(c.left) + '</span><button class="btn ghost sm" data-bkendask>End block</button></div>'
        + '<div class="s1-nav">' + c.ids.map((id, j) => '<button class="s1-nb' + (j === c.i ? ' on' : '') + (c.pk[id] != null ? ' done' : '') + (c.mk[id] ? ' mk' : '') + '" data-bkgo="' + j + '">' + (j + 1) + '</button>').join('') + '</div>'
        + '<div class="panel hq-q">' + ME.hqStem(it).replace(/<p class="hq-ql hq-qtop">[\s\S]*?<\/p>/, '') + '<div class="hq-os">'
        + it.o.map((o, k) => '<div class="hq-orow"><button class="hq-o' + (xs.includes(k) ? ' x' : '') + (pk === k ? ' pend' : '') + '" data-bkpick="' + k + '"><span class="hq-l">' + L5[k] + '</span><span class="hq-ot">' + esc(o) + '</span></button><button class="hq-xb' + (xs.includes(k) ? ' on' : '') + '" data-bkx="' + k + '" title="Strike out" aria-label="Strike out ' + L5[k] + '">✕</button></div>').join('')
        + '</div><div class="toolbar"><button class="btn" data-bkgo="' + (c.i - 1) + '"' + (c.i ? '' : ' disabled') + '>← Previous</button><span class="grow"></span>' + (c.i + 1 < c.ids.length ? '<button class="btn primary" data-bkgo="' + (c.i + 1) + '">Next →</button>' : '<button class="btn primary" data-bkendask>Finish ✓</button>') + '</div></div>'
        + '<aside class="s1-labd" id="bkLabs"' + (blk.labs ? '' : ' hidden') + '>' + labsTable(true) + '</aside></div>';
      m.innerHTML = h; window.scrollTo({top: 0});
      clearInterval(tick);
      tick = setInterval(() => {
        const cc = st().cur; if (!cc || ME.route.view !== 'block') { clearInterval(tick); document.body.classList.remove('s1-examing'); return; }
        cc.left -= 1; const k = $('#bkClock'); if (k) { k.textContent = '⏱ ' + mmss(cc.left); k.classList.toggle('low', cc.left < 300); }
        if (cc.left % 10 === 0) ME.save();
        if (cc.left <= 0) { clearInterval(tick); ME.toast('⏱ Time: the block is over'); endBlock(); }
      }, 1000);
    }
    function toggleLabs() {
      blk.labs = !blk.labs; const a = $('#bkLabs'), w = $('.s1-exam');
      if (a) a.hidden = !blk.labs; if (w) w.classList.toggle('labs-open', !!blk.labs);
      const q = blk.labs && a && a.querySelector('.s1-labq'); if (q) q.focus({preventScroll: true});
    }
    function endBlock() {
      const s = st(), c = s.cur; if (!c) return;
      clearInterval(tick); document.body.classList.remove('s1-examing');
      let right = 0; const pkArr = c.ids.map(id => { const p = c.pk[id]; const q = ME.hqItem(id); if (q && p === q.a) right++; return p == null ? null : p; });
      const rid = 'r' + Date.now().toString(36) + 'b';
      const answered = {}; c.ids.forEach(id => { if (c.pk[id] != null) answered[id] = c.pk[id]; });
      const runs = ME.hqRuns(); const n = c.ids.length, done = Object.keys(answered).length;
      runs.unshift({rid, ids: c.ids, i: 0, pk: answered, x: c.x, lbl: '⏱️ Block ' + new Date().toLocaleDateString('en-GB') + ' · ' + right + '/' + n, customLbl: 1, done, right, pct: done ? Math.round(right / done * 1000) / 10 : null, ts: Date.now(), ov: 2});
      s.blocks.push({at: Date.now(), n, right, used: c.total - Math.max(0, c.left), ids: c.ids, pk: pkArr, rid});
      s.last = {n, right, used: c.total - Math.max(0, c.left), rid, ids: c.ids, pk: pkArr};
      delete s.cur; ME.addXp(right * 2); ME.save();
      ME.go({view: 'block'});
    }
    function resultHtml() {
      const s = st(), r = s.last; if (!r) return '';
      const by = {};
      r.ids.forEach((id, j) => { const q = ME.hqItem(id); if (!q) return; const w = (U[+q.k] || {}).w; const g = by[w] = by[w] || [0, 0]; g[1]++; if (r.pk[j] === q.a) g[0]++; });
      const pct = Math.round(r.right / r.n * 100);
      return '<div class="panel s1-result"><div class="s1-score ' + (pct >= 70 ? 'ok' : pct >= 55 ? 'mid' : 'low') + '">' + pct + '%</div><div><b>' + r.right + ' of ' + r.n + ' right</b> in ' + mmss(r.used) + '<div class="s1-by">' + Object.entries(by).map(([w, g]) => '<span class="s1-chip ghost">' + esc((W.find(x => x.id === w) || {}).name || w) + ' ' + g[0] + '/' + g[1] + '</span>').join('') + '</div>'
        + '<div class="toolbar"><button class="btn primary" data-bkrev="' + r.rid + '">🔍 Review with the 4 boxes →</button><button class="btn" data-go="deconstruct">⚡ Deconstruct the misses</button><button class="btn ghost" data-bkclose>Close</button></div></div></div>';
    }
    function labsTable(compact) {
      const groups = [];
      LABS.forEach(r => { let g = groups.find(x => x[0] === r[0]); if (!g) groups.push(g = [r[0], []]); g[1].push(r); });
      return '<div class="s1-labs' + (compact ? ' compact' : '') + '">' + (compact ? '<input class="search s1-labq" placeholder="Find a test" style="padding-left:12px">' : '') + groups.map(([g, rows]) => '<table><caption>' + esc(g) + '</caption>' + rows.map(r => '<tr data-lq="' + esc((r[1] + ' ' + g).toLowerCase()) + '"><td>' + esc(r[1]) + '</td><td><b>' + esc(r[2]) + '</b> ' + esc(r[3]) + '</td>' + (compact ? '' : '<td class="s1-si">' + (r[4] === 1 || !/\d/.test(r[2]) ? '<span class="hint">same</span>' : esc(siRange(r)) + ' ' + esc(r[5])) + '</td><td class="hint">' + esc(r[6]) + '</td>') + '</tr>').join('') + '</table>').join('') + '</div>';
    }
    document.addEventListener('input', e => {
      if (!e.target.classList || !e.target.classList.contains('s1-labq')) return;
      const q = e.target.value.toLowerCase().trim(), box = e.target.closest('.s1-labs');
      $$('tr[data-lq]', box).forEach(r => { r.hidden = !!q && !r.dataset.lq.includes(q); });
    });
    document.addEventListener('click', e => {
      const t = e.target.closest && e.target.closest('[data-bkn],[data-bksrc],[data-bkst],[data-bkstart],[data-bkresume],[data-bkend],[data-bkendask],[data-bkgo],[data-bkpick],[data-bkx],[data-bkmark],[data-bklabs],[data-bkrev],[data-bkclose]');
      if (!t || ME.route.view !== 'block') return;
      const d = t.dataset, s = st(), c = s.cur;
      if (d.bkn) { blk.cfg.n = +d.bkn; return viewBlockSetup($('#main')); }
      if (d.bksrc) { blk.cfg.src = d.bksrc; if (d.bksrc === 'all') blk.cfg.ch = ''; return viewBlockSetup($('#main')); }
      if (d.bkst) { blk.cfg.st = d.bkst; return viewBlockSetup($('#main')); }
      if (d.bkstart != null) return startBlock();
      if (d.bkresume != null) return drawBlock();
      if (d.bkend != null) return endBlock();
      if (d.bkclose != null) { delete s.last; ME.save(); return viewBlockSetup($('#main')); }
      if (d.bkrev) { ME.go({view: 'hammer'}); if (!ME.hqResume(d.bkrev)) ME.toast('That review is no longer saved'); return; }
      if (!c) return;
      const it = ME.hqItem(c.ids[c.i]);
      if (d.bkendask != null) { const left = c.ids.filter(id => c.pk[id] == null).length; if (!left || confirm(left + ' question' + (left > 1 ? 's are' : ' is') + ' unanswered. End the block?')) endBlock(); return; }
      if (d.bkgo != null) { const j = +d.bkgo; if (j >= 0 && j < c.ids.length) { c.i = j; ME.save(); drawBlock(); } return; }
      if (d.bkpick != null) { const k = +d.bkpick; if ((c.x[it.id] || []).includes(k)) return; c.pk[it.id] = c.pk[it.id] === k ? undefined : k; if (c.pk[it.id] === undefined) delete c.pk[it.id]; ME.save(); return drawBlock(); }
      if (d.bkx != null) { const k = +d.bkx, xs = c.x[it.id] = c.x[it.id] || []; const at = xs.indexOf(k); if (at >= 0) xs.splice(at, 1); else { xs.push(k); if (c.pk[it.id] === k) delete c.pk[it.id]; } ME.save(); return drawBlock(); }
      if (d.bkmark != null) { c.mk[it.id] = !c.mk[it.id]; ME.save(); return drawBlock(); }
      if (d.bklabs != null) toggleLabs();
    });
    /* capture phase, so the engine's own question keys (which follow any open hammer run) never fire during a block */
    document.addEventListener('keydown', e => {
      if (ME.route.view !== 'block' || !st().cur || !$('.s1-exam') || /input|textarea|select/i.test((e.target.tagName || ''))) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const c = st().cur, k = e.key.length === 1 ? e.key.toUpperCase() : e.key;
      const mine = (k >= 'A' && k <= 'E' && k.length === 1) || ['ArrowRight', 'ArrowLeft', 'Escape', 'Enter', ' ', 'S', 'M', 'L'].includes(k);
      if (!mine) return;
      e.preventDefault(); e.stopImmediatePropagation();
      if (k.length === 1 && k >= 'A' && k <= 'E') { const b = $('[data-bkpick="' + (k.charCodeAt(0) - 65) + '"]'); if (b) b.click(); }
      else if ((k === 'ArrowRight' || k === 'Enter') && c.i + 1 < c.ids.length) { c.i++; ME.save(); drawBlock(); }
      else if (k === 'ArrowLeft' && c.i > 0) { c.i--; ME.save(); drawBlock(); }
      else if (k === 'M') { const b = $('[data-bkmark]'); if (b) b.click(); }
      else if (k === 'L') toggleLabs();
    }, true);
    ME.view('block', m => { if (st().cur && blk.resumeOnOpen) { blk.resumeOnOpen = false; return drawBlock(); } viewBlockSetup(m); const r = resultHtml(); if (r) m.querySelector('.ph').insertAdjacentHTML('afterend', r); });

    /* ================================================================ 🧪 lab values */
    let cv = {row: 4, v: '', back: false};
    ME.view('labs', m => {
      const r = LABS[cv.row];
      m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🧪 Lab values</span></div><h1>US lab values with the UK bridge</h1><p class="hint" style="margin:0">Step 1 stems use US units. Read the US value first; the UK column is there so the numbers you already know still mean something. Typical adult ranges for revision: on exam day, use the sheet the exam gives you.</p></div>'
        + '<div class="panel s1-conv"><b>🔁 Convert</b><select class="jsel" id="cvRow">' + LABS.map((x, i) => x[4] !== 1 && /\d/.test(x[2]) ? '<option value="' + i + '"' + (i === cv.row ? ' selected' : '') + '>' + esc(x[1]) + '</option>' : '').join('') + '</select>'
        + '<input id="cvIn" type="number" step="any" inputmode="decimal" placeholder="value" value="' + esc(cv.v) + '"><button class="chip' + (cv.back ? '' : ' on') + '" data-cvdir="0">' + esc(r[3]) + ' → ' + esc(r[5]) + '</button><button class="chip' + (cv.back ? ' on' : '') + '" data-cvdir="1">' + esc(r[5]) + ' → ' + esc(r[3]) + '</button>'
        + '<span class="s1-cvout" id="cvOut">' + cvOut() + '</span></div>' + labsTable(false) + '</div>';
    });
    function cvOut() { const r = LABS[cv.row], x = parseFloat(cv.v); if (isNaN(x)) return ''; return '= <b>' + fmtN(convert(r, x, cv.back)) + '</b> ' + esc(cv.back ? r[3] : r[5]); }
    document.addEventListener('input', e => { if (e.target.id === 'cvIn') { cv.v = e.target.value; const o = $('#cvOut'); if (o) o.innerHTML = cvOut(); } });
    document.addEventListener('change', e => { if (e.target.id === 'cvRow') { cv.row = +e.target.value; ME.render(); } if (e.target.id === 'bkCh') { blk.cfg.ch = e.target.value; if (e.target.value) blk.cfg.src = 'all'; viewBlockSetup($('#main')); } });
    document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-cvdir]'); if (b) { cv.back = b.dataset.cvdir === '1'; ME.render(); } });

    /* ================================================================ 🧭 acid-base compass */
    const PRE = [
      ['DKA', {ph: 7.21, pco2: 24, hco3: 10, na: 134, cl: 99, alb: 4, osm: '', glu: 480, bun: 30}],
      ['Diarrhoea', {ph: 7.30, pco2: 31, hco3: 15, na: 137, cl: 114, alb: 4}],
      ['Vomiting', {ph: 7.52, pco2: 48, hco3: 37, na: 136, cl: 88, alb: 4}],
      ['Opioid overdose', {ph: 7.22, pco2: 68, hco3: 26, na: 140, cl: 104}],
      ['COPD retainer', {ph: 7.35, pco2: 60, hco3: 31, na: 140, cl: 98}],
      ['Panic attack', {ph: 7.56, pco2: 24, hco3: 21, na: 140, cl: 106}],
      ['Aspirin overdose', {ph: 7.45, pco2: 20, hco3: 14, na: 140, cl: 102}],
      ['Antifreeze', {ph: 7.15, pco2: 20, hco3: 7, na: 140, cl: 102, osm: 330, glu: 90, bun: 14}]
    ];
    let abg = Object.assign({}, PRE[0][1]);
    const F = [['ph', 'pH', ''], ['pco2', 'PaCO₂', 'mmHg'], ['hco3', 'HCO₃⁻', 'mEq/L'], ['na', 'Na⁺', 'mEq/L'], ['cl', 'Cl⁻', 'mEq/L'], ['alb', 'Albumin', 'g/dL'], ['osm', 'Measured osm', 'mOsm/kg'], ['glu', 'Glucose', 'mg/dL'], ['bun', 'BUN', 'mg/dL']];
    ME.view('abg', m => {
      m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🧭 Acid-base compass</span></div><h1>Read any gas in 5 steps</h1><p class="hint" style="margin:0">pH, then the primary process, then whether compensation fits, then the anion gap and delta ratio, then the osmolar gap. The map shows where the numbers sit against every expected-compensation band.</p></div>'
        + '<div class="panel"><div class="s1-pre">' + PRE.map(([n], i) => '<button class="chip" data-abgpre="' + i + '">' + esc(n) + '</button>').join('') + '<button class="chip" data-abgpre="-1">Clear</button></div>'
        + '<div class="s1-abgin">' + F.map(([k, l, u]) => '<label><span>' + l + '</span><input type="number" step="any" inputmode="decimal" data-abg="' + k + '" value="' + esc(abg[k] == null ? '' : abg[k]) + '"><em>' + u + '</em></label>').join('') + '</div></div>'
        + '<div class="s1-abgout" id="abgOut"></div></div>';
      drawAbg();
    });
    function drawAbg() {
      const o = $('#abgOut'); if (!o) return;
      const r = abgSolve(abg);
      if (!r.ok) { o.innerHTML = '<div class="panel"><p class="hint">' + esc(r.err) + '</p></div>'; return; }
      o.innerHTML = '<div class="panel s1-abgsum"><span class="s1-bk">🧭 Reading</span><b>' + esc(r.summary) + '</b>' + r.flags.map(f => '<p class="s1-err">⚠️ ' + esc(f) + '</p>').join('') + '</div>'
        + '<div class="s1-abggrid"><div class="panel">' + r.steps.map(s => '<div class="s1-step ' + s[3] + '"><span>' + s[0] + '</span><div><b>' + esc(s[1]) + '</b><p>' + esc(s[2]) + '</p></div></div>').join('')
        + (r.causes.length ? '<div class="s1-causes">' + r.causes.map(c => '<p><b>' + esc(c[0]) + '</b> ' + esc(c[1]) + '</p>').join('') + '</div>' : '') + '</div>'
        + '<div class="panel s1-map">' + compassSvg(+abg.hco3, +abg.pco2) + '<p class="hint">x: HCO₃⁻ (mEq/L) · y: PaCO₂ (mmHg). Shaded bands are where a single, compensated disorder lands; dashed lines are constant pH. A dot outside every band means two disorders.</p></div></div>';
    }
    function compassSvg(hc, pc) {
      const X = v => 46 + v / 50 * 344, Y = v => 286 - (v - 10) / 90 * 266;
      const band = (fn, a, b, w, cls, axis) => { const up = [], dn = []; for (let t = a; t <= b + 1e-9; t += (b - a) / 24) { const c = fn(t); if (axis === 'x') { up.push([X(t), Y(c + w)]); dn.push([X(t), Y(c - w)]); } else { up.push([X(c + w), Y(t)]); dn.push([X(c - w), Y(t)]); } } return '<polygon class="s1-band ' + cls + '" points="' + up.concat(dn.reverse()).map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ') + '"/>'; };
      const iso = ph => { const pts = []; for (let h = 2; h <= 50; h += 2) { const p = h / (0.03 * Math.pow(10, ph - 6.1)); if (p >= 10 && p <= 100) pts.push(X(h).toFixed(1) + ',' + Y(p).toFixed(1)); } return '<polyline class="s1-iso" points="' + pts.join(' ') + '"/>'; };
      let g = '<svg class="s1-compass" viewBox="0 0 400 320" role="img" aria-label="Acid-base map: bicarbonate against carbon dioxide">';
      for (let h = 0; h <= 50; h += 10) g += '<line class="s1-grid" x1="' + X(h) + '" y1="' + Y(10) + '" x2="' + X(h) + '" y2="' + Y(100) + '"/><text class="s1-ax" x="' + X(h) + '" y="302" text-anchor="middle">' + h + '</text>';
      for (let p = 10; p <= 100; p += 15) g += '<line class="s1-grid" x1="' + X(0) + '" y1="' + Y(p) + '" x2="' + X(50) + '" y2="' + Y(p) + '"/><text class="s1-ax" x="40" y="' + (Y(p) + 4) + '" text-anchor="end">' + p + '</text>';
      g += iso(7.2) + iso(7.4) + iso(7.6) + '<text class="s1-isot" x="' + X(9) + '" y="' + (Y(9 / (0.03 * Math.pow(10, 1.1))) - 4) + '">7.2</text><text class="s1-isot" x="' + X(23) + '" y="' + (Y(100) + 12) + '">pH 7.4</text><text class="s1-isot" x="' + X(46) + '" y="' + (Y(46 / (0.03 * Math.pow(10, 1.5))) - 4) + '">7.6</text>';
      g += band(h => 1.5 * h + 8, 4, 22, 2, 'ma', 'x') + band(h => 40 + 0.7 * (h - 24), 28, 46, 2, 'mk', 'x');
      g += band(p => 24 + 0.1 * (p - 40), 45, 100, 2, 'ra', 'y') + band(p => 24 + 0.35 * (p - 40), 45, 100, 2, 'ra2', 'y');
      g += band(p => 24 - 0.2 * (40 - p), 12, 35, 2, 'rk', 'y') + band(p => 24 - 0.4 * (40 - p), 12, 35, 2, 'rk2', 'y');
      g += '<rect class="s1-norm" x="' + X(22) + '" y="' + Y(45) + '" width="' + (X(28) - X(22)) + '" height="' + (Y(35) - Y(45)) + '"/>';
      g += '<text class="s1-bl ma" x="' + X(5) + '" y="' + Y(30) + '">Metabolic acidosis</text><text class="s1-bl mk" x="' + X(31) + '" y="' + Y(64) + '">Metabolic alkalosis</text>'
        + '<text class="s1-bl ra" x="' + X(26.5) + '" y="' + Y(96) + '">Resp acidosis: acute</text><text class="s1-bl ra" x="' + X(36) + '" y="' + Y(82) + '">chronic</text>'
        + '<text class="s1-bl rk" x="' + X(23) + '" y="' + Y(13) + '">Resp alkalosis: acute</text><text class="s1-bl rk" x="' + X(6) + '" y="' + Y(19) + '">chronic</text>';
      if (hc > 0 && hc <= 50 && pc >= 10 && pc <= 100) g += '<circle class="s1-dot" cx="' + X(hc) + '" cy="' + Y(pc) + '" r="7"/><circle class="s1-dot2" cx="' + X(hc) + '" cy="' + Y(pc) + '" r="13"/>';
      return g + '</svg>';
    }
    document.addEventListener('input', e => { const k = e.target.dataset && e.target.dataset.abg; if (!k) return; abg[k] = e.target.value; drawAbg(); });
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-abgpre]'); if (!b) return;
      const i = +b.dataset.abgpre; abg = i < 0 ? {} : Object.assign({}, PRE[i][1]); ME.render();
    });

    /* ================================================================ 🫘 nephron map */
    const SEG = {
      glom: {t: 'Glomerulus and the JG apparatus', c: '#7a4fc9', d: ['Filters about 20% of the plasma that arrives (filtration fraction); GFR about 100 to 125 mL/min', 'Barrier: fenestrated endothelium, a negatively charged basement membrane, then podocyte slits (nephrin)', 'Afferent arteriole sets the inflow, efferent the outflow: constrict efferent and GFR rises while flow falls', 'Juxtaglomerular cells release renin when pressure falls, with sympathetic β1 drive, or when the macula densa senses little NaCl'],
        h: ['Angiotensin II squeezes the efferent arteriole', 'Prostaglandins dilate the afferent arteriole', 'ANP dilates afferent, constricts efferent'], rx: ['ACE inhibitors and ARBs: efferent relaxes, GFR falls', 'NSAIDs: blocks prostaglandin synthesis -> loss of afferent vasodilation (decreased dilation, not direct constriction), so GFR falls'], dz: ['Nephritic: inflamed capillaries leak red cells (RBC casts)', 'Nephrotic: podocyte injury leaks protein over 3.5 g a day'], u: ['Glomerular filtration and clearance', 'Nephritic syndrome', 'Nephrotic syndrome']},
      pct: {t: 'Proximal convoluted tubule', c: '#d0306b', d: ['Takes back 65 to 80% of filtered Na⁺ and water, isotonically', 'Reclaims all the glucose (SGLT2) and amino acids, and most of the HCO₃⁻ (carbonic anhydrase, Na⁺/H⁺ exchange)', 'Secretes organic acids and drugs (penicillin, PAH, urate) and makes NH₄⁺ from glutamine', 'Holds 1α-hydroxylase: calcidiol to calcitriol'],
        h: ['Angiotensin II: more Na⁺/H⁺ exchange, so contraction alkalosis', 'PTH: blocks Na⁺/phosphate cotransport (phosphaturia) and switches on 1α-hydroxylase'], rx: ['Acetazolamide: carbonic anhydrase blocked, HCO₃⁻ lost, normal-gap acidosis', 'SGLT2 inhibitors: glucose in the urine', 'Mannitol works here and in the thin descending limb'], dz: ['Fanconi syndrome: glucose, amino acids, phosphate and HCO₃⁻ all lost (type 2 RTA)', 'Most exposed to ischaemic and toxic ATN', 'Cystinuria and Hartnup: transporter defects'], u: ['Proximal convoluted tubule', 'Renal tubular acidosis', 'Diuretics']},
      tdl: {t: 'Thin descending limb', c: '#3a7bd5', d: ['Water leaves through aquaporin 1 into the salty medulla; salt stays in', 'So the fluid gets more concentrated on the way down'], h: [], rx: ['Mannitol: holds water in the tubule'], dz: [], u: ['Loop of Henle and Bartter syndrome']},
      tal: {t: 'Thick ascending limb', c: '#e07b00', d: ['NKCC2 moves 1 Na⁺, 1 K⁺ and 2 Cl⁻ in; about a quarter of filtered Na⁺', 'K⁺ leaks back out through ROMK, so the lumen turns positive and pushes Mg²⁺ and Ca²⁺ through the gaps between cells', 'No water follows: the fluid is diluted (the first diluting segment)', 'Makes uromodulin (Tamm-Horsfall), the matrix of every cast'],
        h: ['PTH and calcium sensing tune Ca²⁺ and Mg²⁺ reabsorption here'], rx: ['Loop diuretics (furosemide, bumetanide, torsemide, ethacrynic acid): NKCC2 blocked, so Ca²⁺ and Mg²⁺ are lost too', 'NSAIDs blunt the loop effect by removing prostaglandins'], dz: ['Bartter syndrome: a loop diuretic you are born with, hypokalaemic alkalosis with high urine calcium'], u: ['Loop of Henle and Bartter syndrome', 'Diuretics', 'Calcium, phosphate and magnesium']},
      md: {t: 'Macula densa', c: '#2f9e44', d: ['Specialised cells where the thick ascending limb touches its own glomerulus', 'Low NaCl here: the afferent arteriole dilates and renin is released (tubuloglomerular feedback)'], h: [], rx: ['Loop diuretics blind the macula densa, so renin rises'], dz: [], u: ['Renin-angiotensin-aldosterone and renal hormones']},
      dct: {t: 'Distal convoluted tubule', c: '#0e9f8f', d: ['NCC moves Na⁺ and Cl⁻ in; 5 to 10% of filtered Na⁺', 'Still no water: the second diluting segment', 'PTH adds Ca²⁺ reabsorption here'], h: ['PTH: more Ca²⁺ reabsorbed'], rx: ['Thiazides (hydrochlorothiazide, chlorthalidone, metolazone): NCC blocked, so calcium is kept (hypocalciuria)'], dz: ['Gitelman syndrome: a thiazide you are born with, low K⁺, low Mg²⁺, low urine calcium'], u: ['Distal tubule, collecting duct, Gitelman and Liddle', 'Diuretics']},
      cd: {t: 'Collecting duct', c: '#5c6bc0', d: ['Principal cells: ENaC takes Na⁺ in, ROMK sends K⁺ out; aldosterone turns up both and the Na⁺/K⁺ pump', 'ADH acts on V2 receptors: aquaporin 2 slides into the luminal membrane and water follows into the medulla', 'Alpha-intercalated cells secrete H⁺ and reclaim HCO₃⁻; beta-intercalated cells do the reverse', 'ADH also opens urea channels deep in the medulla, which keeps the medulla salty'],
        h: ['Aldosterone: Na⁺ in, K⁺ and H⁺ out', 'ADH: aquaporin 2 and urea channels'], rx: ['Spironolactone and eplerenone: aldosterone receptor blocked', 'Amiloride and triamterene: ENaC blocked', 'Tolvaptan and conivaptan: V2 blocked, free water lost (SIADH)', 'Lithium and demeclocycline: nephrogenic DI'], dz: ['Liddle syndrome: ENaC stuck open', 'Type 1 RTA: alpha-intercalated cells cannot secrete H⁺', 'Type 4 RTA: too little aldosterone action', 'Nephrogenic DI: V2 or aquaporin 2 ignores ADH'], u: ['Distal tubule, collecting duct, Gitelman and Liddle', 'Renal tubular acidosis', 'Sodium and water', 'Potassium']}
    };
    const DRUG = [['Acetazolamide', ['pct']], ['SGLT2 inhibitors', ['pct']], ['Mannitol', ['pct', 'tdl']], ['Loop diuretics', ['tal']], ['Thiazides', ['dct']], ['Spironolactone', ['cd']], ['Amiloride', ['cd']], ['Tolvaptan', ['cd']], ['ACE inhibitors', ['glom']]];
    const nm = {seg: 'pct', drug: ''};
    ME.view('nephron', m => {
      const on = nm.drug ? (DRUG.find(d => d[0] === nm.drug) || [0, []])[1] : [];
      const S = SEG[nm.seg];
      const path = (k, dd) => '<path class="s1-seg' + (nm.seg === k ? ' on' : '') + (on.includes(k) ? ' hit' : '') + '" data-seg="' + k + '" d="' + dd + '" style="--sc:' + SEG[k].c + '"><title>' + SEG[k].t + '</title></path>';
      const svg = '<svg class="s1-neph" viewBox="0 0 520 380" role="img" aria-label="Nephron map: tap a segment">'
        + '<rect class="s1-cortex" x="0" y="0" width="520" height="165"/><rect class="s1-med" x="0" y="165" width="520" height="215"/>'
        + '<text class="s1-zone" x="508" y="20" text-anchor="end">Cortex</text><text class="s1-zone" x="508" y="185" text-anchor="end">Medulla</text>'
        + '<path class="s1-vessel" d="M8 52 C 40 52, 50 60, 66 66"/><path class="s1-vessel" d="M112 62 C 130 50, 150 44, 186 40"/><text class="s1-lab" x="8" y="44">afferent</text><text class="s1-lab" x="150" y="34">efferent</text>'
        + '<circle class="s1-bow" cx="90" cy="78" r="40"/>'
        + '<g class="s1-segg" data-seg="glom"><circle class="s1-seg s1-glom' + (nm.seg === 'glom' ? ' on' : '') + (on.includes('glom') ? ' hit' : '') + '" data-seg="glom" cx="90" cy="78" r="26" style="--sc:' + SEG.glom.c + '"><title>' + SEG.glom.t + '</title></circle></g>'
        + path('pct', 'M118 104 C 150 120, 140 150, 175 140 C 205 130, 185 100, 215 105 C 240 110, 230 140, 238 160')
        + path('tdl', 'M238 160 L 238 330')
        + path('tal', 'M238 330 C 238 352, 270 352, 272 330 L 272 150 C 272 130, 250 122, 150 118')
        + '<circle class="s1-seg s1-md' + (nm.seg === 'md' ? ' on' : '') + '" data-seg="md" cx="146" cy="117" r="9" style="--sc:' + SEG.md.c + '"><title>' + SEG.md.t + '</title></circle>'
        + path('dct', 'M150 118 C 200 70, 260 60, 300 80 C 340 100, 330 60, 372 64')
        + path('cd', 'M372 64 C 400 66, 410 90, 410 120 L 410 360')
        + '<text class="s1-lab" x="160" y="170">PCT</text><text class="s1-lab" x="200" y="260">thin ↓</text><text class="s1-lab" x="280" y="260">thick ↑</text><text class="s1-lab" x="304" y="58">DCT</text><text class="s1-lab" x="418" y="250">collecting duct</text><text class="s1-lab" x="40" y="132">glomerulus</text><text class="s1-lab" x="96" y="140">macula densa</text>'
        + '</svg>';
      const li = a => a.length ? '<ul>' + a.map(x => '<li>' + rich(x) + '</li>').join('') + '</ul>' : '<p class="hint">None that Step 1 asks about.</p>';
      m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🫘 Nephron map</span></div><h1>Walk the nephron</h1><p class="hint" style="margin:0">Tap a segment to see what it moves, which hormones and drugs act there, and what happens when it breaks. Pick a drug to light up where it works.</p></div>'
        + '<div class="s1-drugs">' + DRUG.map(([n]) => '<button class="chip' + (nm.drug === n ? ' on' : '') + '" data-nmdrug="' + esc(n) + '">💊 ' + esc(n) + '</button>').join('') + '</div>'
        + '<div class="s1-nephgrid"><div class="panel">' + svg + '</div><div class="panel s1-seginfo" style="--sc:' + S.c + '"><h2>' + esc(S.t) + '</h2>'
        + '<span class="s1-bk">⚙️ What it does</span>' + li(S.d) + '<span class="s1-bk">🧬 Hormones here</span>' + li(S.h) + '<span class="s1-bk">💊 Drugs here</span>' + li(S.rx) + '<span class="s1-bk">💥 When it breaks</span>' + li(S.dz)
        + '<div class="fw-u">' + S.u.filter(n => uByName[n.toLowerCase()] != null).map(n => '<button class="ulink" data-u="' + uByName[n.toLowerCase()] + '" data-mode="fill">↗ ' + esc(n) + '</button>').join('') + '</div></div></div></div>';
    });
    document.addEventListener('click', e => {
      if (ME.route.view !== 'nephron') return;
      const s = e.target.closest && e.target.closest('[data-seg]'), d = e.target.closest && e.target.closest('[data-nmdrug]');
      if (s) { nm.seg = s.dataset.seg; ME.render(); }
      else if (d) { nm.drug = nm.drug === d.dataset.nmdrug ? '' : d.dataset.nmdrug; const hit = (DRUG.find(x => x[0] === nm.drug) || [0, []])[1]; if (hit.length) nm.seg = hit[0]; ME.render(); }
    });

    /* ================================================================ 🫀 System maps (8-tab visual Step 1 atlas + PV loop shifter + 60 UWorld plates) */
    const atl = {tab: 'glom', pv: 'norm'};
    const ATL_TABS = [
      ['glom', '🫘 Glomerular & 60 UWorld Plates'],
      ['pv', '📈 Interactive PV-Loops'],
      ['shock', '🫀 Shock & Murmurs'],
      ['resp', '🫁 Spirometry & V/Q'],
      ['cah', '🦋 CAH & Endocrine'],
      ['heme', '🩸 Coag & Anaemia'],
      ['neuro', '🧠 Brainstem & Cord'],
      ['storage', '🧬 Storage Disease Subway']
    ];
    const PV_STATES = {
      norm: {name: 'Normal Baseline', edv: 120, esv: 50, pmax: 120, edp: 8, isov: true, desc: 'Normal left ventricular pressure-volume loop: EDV 120 mL, ESV 50 mL, Stroke Volume (SV) = 70 mL, Ejection Fraction (EF) = 58%.'},
      preload_up: {name: '↑ Preload (IV Fluid Bolus)', edv: 155, esv: 50, pmax: 128, edp: 14, isov: true, desc: 'Increased venous return shifts the right border (EDV) rightward -> Frank-Starling mechanism increases Stroke Volume (SV rises to 105 mL).'},
      afterload_up: {name: '↑ Afterload / Hypertension', edv: 120, esv: 75, pmax: 165, edp: 10, isov: true, desc: 'Increased arterial pressure forces the LV to generate higher peak systolic pressure -> less blood is ejected -> ↑ ESV (75 mL) and ↓ Stroke Volume (45 mL).'},
      inotropy_up: {name: '↑ Contractility (Dobutamine / β1)', edv: 120, esv: 30, pmax: 145, edp: 6, isov: true, desc: 'Positive inotropy shifts the ESPVR line to the left -> LV ejects more completely -> ↓ ESV (30 mL), ↑ Stroke Volume (90 mL), and ↑ Ejection Fraction (75%).'},
      as: {name: 'Aortic Stenosis (AS)', edv: 125, esv: 70, pmax: 195, edp: 18, isov: true, desc: 'Calcified stenotic aortic valve creates a massive systolic pressure gradient -> dome-shaped tall PV loop with ↑↑ peak LV pressure, ↑ ESV, and ↓ SV.'},
      ar: {name: 'Aortic Regurgitation (AR)', edv: 185, esv: 60, pmax: 150, edp: 16, isov: false, desc: 'Blood leaks back into LV during diastole -> loss of true isovolumetric relaxation, huge ↑↑ EDV (volume overload), and massive Stroke Volume + wide pulse pressure.'},
      ms: {name: 'Mitral Stenosis (MS)', edv: 85, esv: 45, pmax: 105, edp: 5, isov: true, desc: 'Impaired LA-to-LV diastolic filling starves the left ventricle of preload -> shifted left with ↓ EDV (85 mL) and ↓ Stroke Volume (40 mL).'},
      mr: {name: 'Mitral Regurgitation (MR)', edv: 170, esv: 40, pmax: 115, edp: 14, isov: false, desc: 'Blood leaks backward into low-pressure LA during systole -> loss of isovolumetric contraction, ↓ afterload (↓ ESV), and ↑ EDV from extra LA volume.'}
    };
    function pvSvgHtml(mode) {
      const b = PV_STATES.norm, c = PV_STATES[mode] || b;
      const X = v => 55 + (v / 210) * 360, Y = p => 250 - (p / 215) * 220;
      const loopPath = st => {
        const x1 = X(st.esv), x2 = X(st.edv), y0 = Y(st.edp), yOpen = Y(80), yPeak = Y(st.pmax), yClose = Y(95);
        if (!st.isov) {
          return 'M ' + x1 + ' ' + (y0 + 8) + ' Q ' + ((x1 + x2) / 2) + ' ' + (y0 + 18) + ' ' + x2 + ' ' + y0
            + ' Q ' + (x2 + 12) + ' ' + ((y0 + yPeak) / 2) + ' ' + ((x1 + x2) / 2) + ' ' + yPeak
            + ' Q ' + (x1 - 12) + ' ' + ((yPeak + y0) / 2) + ' ' + x1 + ' ' + (y0 + 8) + ' Z';
        }
        return 'M ' + x1 + ' ' + (y0 - 2) + ' Q ' + ((x1 + x2) / 2) + ' ' + (y0 + 8) + ' ' + x2 + ' ' + y0
          + ' L ' + x2 + ' ' + yOpen + ' Q ' + ((x1 + x2) / 2) + ' ' + (yPeak - 18) + ' ' + x1 + ' ' + yClose + ' Z';
      };
      return '<svg viewBox="0 0 450 285" style="width:100%;max-width:520px;background:var(--surface-2);border-radius:10px;border:1px solid var(--line)">'
        + '<line x1="55" y1="20" x2="55" y2="250" stroke="var(--muted)" stroke-width="1.5"/>'
        + '<line x1="55" y1="250" x2="425" y2="250" stroke="var(--muted)" stroke-width="1.5"/>'
        + '<text x="240" y="276" text-anchor="middle" font-size="11" fill="var(--ink)">Left Ventricular Volume (mL) — EDV minus ESV = Stroke Volume</text>'
        + '<text x="16" y="135" text-anchor="middle" font-size="11" fill="var(--ink)" transform="rotate(-90 16 135)">LV Pressure (mmHg)</text>'
        + '<line x1="55" y1="250" x2="' + X(95) + '" y2="25" stroke="var(--muted)" stroke-dasharray="4,4" stroke-width="1.2"/>'
        + '<text x="' + (X(95) + 4) + '" y="34" font-size="10" fill="var(--muted)">ESPVR</text>'
        + '<path d="' + loopPath(b) + '" fill="rgba(120,140,180,0.12)" stroke="var(--muted)" stroke-width="2" stroke-dasharray="5,4"/>'
        + (mode !== 'norm' ? '<path d="' + loopPath(c) + '" fill="rgba(255,194,26,0.22)" stroke="#e07b00" stroke-width="3"/>' : '<path d="' + loopPath(b) + '" fill="rgba(47,111,237,0.18)" stroke="#2f6fed" stroke-width="3"/>')
        + '<text x="315" y="34" font-size="11" font-weight="700" fill="var(--ink)">Dashed = Normal · Solid = ' + c.name + '</text>'
        + '</svg>';
    }
    const UW_GALLERY_ITEMS = [
      ['uw_mcd_em', 'MCD · Podocyte effacement (EM)'], ['uw_fsgs_silver', 'FSGS · Segmental sclerosis (Silver)'],
      ['uw_kw_nodules', 'Diabetic · Kimmelstiel-Wilson nodules'], ['uw_goodpasture_linear', 'Goodpasture · Linear IgG (IF)'],
      ['uw_goodpasture_if', 'Goodpasture · Anti-GBM crescent'], ['uw_rpgn_he', 'RPGN · Cellular crescent (H&E)'],
      ['uw_rpgn_path', 'RPGN · Crescentic cascade'], ['uw_crescent_osm', 'Nephron · Osmolarity gradient'],
      ['uw_atn_histology', 'ATN · Muddy brown casts'], ['uw_ischemic_atn_medulla', 'ATN · Medullary ischaemia'],
      ['uw_adh_atn', 'ATN · Patchy basement denudation'], ['uw_cholesterol_clefts', 'Atheroemboli · Cholesterol clefts'],
      ['uw_malignant_htn', 'Malignant HTN · Onion-skinning'], ['uw_wbc_cast', 'Pyelonephritis · WBC cast'],
      ['uw_waxy_cast', 'ESRD · Broad waxy cast'], ['uw_analgesic_nephropathy', 'Papillary necrosis · Analgesic'],
      ['uw_staghorn_ct', 'Struvite · Staghorn calculus (CT)'], ['uw_struvite_path', 'Struvite · Urease splits urea'],
      ['uw_adpkd_ct', 'ADPKD · Bilateral cysts (CT)'], ['uw_horseshoe_ct', 'Horseshoe kidney · Trapped on IMA'],
      ['uw_turner_horseshoe', 'Turner 45,XO · Horseshoe kidney'], ['uw_wilms_ct', 'Wilms tumour · WT1 renal mass (CT)'],
      ['uw_rcc_gross_aml', 'RCC & Angiomyolipoma gross'], ['uw_rcc_ivc', 'RCC · Renal vein & IVC invasion'],
      ['uw_renal_infarction', 'Wedge-shaped renal infarction'], ['uw_kidney_embryo', 'Embryo · Ureteric bud + metanephros'],
      ['uw_puv', 'Posterior urethral valves · Keyhole'], ['uw_ureter_anatomy', 'Ureter · 3 stone constriction sites'],
      ['uw_suprapubic', 'Pelvic fracture · Urethral injury'], ['uw_lhf_cascade', 'Heart failure · RAAS & ADH cascade'],
      ['uw_acid_base_nomogram', 'Acid-Base · Compensation nomogram'], ['uw_gfr_autoreg', 'GFR & RPF · Myogenic & TGF autoreg'],
      ['uw_darrow_yannet', 'Darrow-Yannet · ICF vs ECF shifts'], ['uw_sphingolipidoses', 'Sphingolipidoses · Pathway map'],
      ['uw_ebstein', 'Ebstein anomaly · Lithium tricuspid'], ['uw_pituitary_embryo', 'Pituitary · Rathke pouch embryo'],
      ['uw_hirschsprung', 'Hirschsprung · Aganglionic megacolon'], ['uw_double_bubble', 'Duodenal atresia · Double bubble'],
      ['uw_hand_nerves', 'Hand · Median vs Ulnar vs Radial'], ['uw_cpa_schwannoma', 'NF2 · CPA Vestibular Schwannoma'],
      ['uw_cell_injury', 'Pathology · Reversible vs Irreversible'], ['uw_hepb_serology', 'HBV · Window period serology'],
      ['uw_pemphigus_bp', 'Pemphigus vs Bullous Pemphigoid IF'], ['uw_wpw_delta', 'WPW · Bundle of Kent & Delta wave'],
      ['uw_pv_afterload', 'Cardio · Afterload PV-Loop shift'], ['uw_aortic_dissection', 'Stanford Type A vs B Dissection'],
      ['uw_dose_response', 'Pharm · Competitive vs Non-comp'], ['uw_folate_b12_trap', 'Biochem · B12 Methyl-THF trap'],
      ['uw_cftr_processing', 'CFTR F508del · RER misfolding'], ['uw_flow_volume_loops', 'Resp · Flow-Volume Loop patterns'],
      ['uw_ibd_comparison', 'GI · Crohn vs Ulcerative Colitis'], ['uw_ethanol_metabolism', 'Biochem · Ethanol NADH/NAD+'],
      ['uw_hcm_disarray', 'HCM · Myofibrillar disarray'], ['uw_aschoff_body', 'Rheumatic fever · Aschoff body'],
      ['uw_psammoma_bodies', 'Papillary thyroid · Psammoma bodies'], ['uw_signet_ring', 'Diffuse gastric · Signet-ring cells'],
      ['uw_gaucher_cell', 'Gaucher · Crinkled-paper macrophage'], ['uw_aspergillus_hyphae', 'Aspergillus · 45° septate hyphae'],
      ['uw_gbm_butterfly', 'Glioblastoma · Butterfly glioma'], ['uw_saddle_pe', 'Massive Saddle Pulmonary Embolism']
    ];
    ME.view('atlas', m => {
      let body = '';
      if (atl.tab === 'glom') {
        body = '<div class="panel"><h2>🫘 Glomerular Pathology: LM · IF · EM · UWorld Biopsies</h2>'
          + '<table><tr><th>Syndrome</th><th>Light Microscopy (LM)</th><th>Immunofluorescence (IF)</th><th>Electron Microscopy (EM)</th><th>Key Step 1 Trigger</th></tr>'
          + '<tr><td><b>Minimal change disease</b></td><td>Normal glomeruli</td><td>Negative</td><td><b>Diffuse podocyte foot process effacement</b></td><td>Child after URI, Hodgkin lymphoma; selective albuminuria; steroid-responsive</td></tr>'
          + '<tr><td><b>FSGS</b></td><td><b>Segmental sclerosis and hyalinosis</b></td><td>Negative (or IgM/C3)</td><td>Foot process effacement</td><td>HIV, heroin, sickle cell, obesity, interferon; steroid-resistant</td></tr>'
          + '<tr><td><b>Membranous nephropathy</b></td><td>Diffuse capillary thickening; <b>spike and dome</b></td><td><b>Granular</b> IgG and C3</td><td><b>Subepithelial</b> dense deposits</td><td>Anti-PLA2R, SLE (class V), HBV/HCV, solid tumours; renal vein thrombosis</td></tr>'
          + '<tr><td><b>Diabetic nephropathy</b></td><td>Mesangial expansion; <b>Kimmelstiel-Wilson nodules</b></td><td>Non-specific linear trapping</td><td><b>GBM thickening</b></td><td>Non-enzymatic glycosylation of efferent &gt; afferent arteriole -&gt; hyperfiltration</td></tr>'
          + '<tr><td><b>Amyloidosis (AL / AA)</b></td><td><b>Congo red apple-green birefringence</b></td><td>Kappa/lambda (AL) or AA</td><td><b>8-12 nm non-branching fibrils</b></td><td>Multiple myeloma (AL) or chronic inflammatory states like RA/IBD/TB (AA)</td></tr>'
          + '<tr><td><b>MPGN (Type I vs II)</b></td><td><b>Tram-track</b> double contour GBM splitting</td><td>Granular IgG/C3 vs C3 only</td><td><b>Subendothelial</b> vs <b>intramembranous ribbon</b></td><td>HBV/HCV cryoglobulinaemia (Type I); C3 nephritic factor (Type II)</td></tr>'
          + '<tr><td><b>Poststreptococcal GN</b></td><td>Hypercellular glomeruli with neutrophils</td><td><b>Starry-sky granular</b> IgG, C3</td><td><b>Subepithelial humps</b></td><td>2-4 weeks after group A strep pharynx/skin; low C3</td></tr>'
          + '<tr><td><b>IgA nephropathy (Berger)</b></td><td>Mesangial proliferation</td><td><b>Mesangial IgA</b></td><td><b>Mesangial</b> dense deposits</td><td>Gross haematuria <b>within 1-3 days</b> of URI/GI infection (synpharyngitic)</td></tr>'
          + '<tr><td><b>Goodpasture (Anti-GBM)</b></td><td>Crescents in Bowman space</td><td><b>Smooth linear IgG</b></td><td>GBM rupture</td><td>Haemoptysis + RPGN; antibodies against <b>alpha-3 chain of type IV collagen</b></td></tr>'
          + '<tr><td><b>Pauci-immune RPGN</b></td><td>Crescents in Bowman space</td><td><b>Negative (pauci-immune)</b></td><td>No immune deposits</td><td><b>PR3-ANCA/c-ANCA</b> (GPA), <b>MPO-ANCA/p-ANCA</b> (MPA, EGPA)</td></tr>'
          + '<tr><td><b>Alport syndrome</b></td><td>Foam cells in interstitium</td><td>Negative</td><td><b>Basket-weave splitting</b> of GBM</td><td>X-linked mutation in <b>alpha-5 chain of type IV collagen</b>; deafness + lenticonus</td></tr></table></div>'
          + '<div class="panel"><h2>🔬 Complete 60-Plate UWorld Pathology, Radiology, Embryology & Pathway Gallery</h2><div class="chgrid" style="grid-template-columns:repeat(auto-fill,minmax(195px,1fr))">'
          + UW_GALLERY_ITEMS.map(([id, cap]) => '<figure style="margin:0;padding:8px;border:1px solid var(--line);border-radius:10px;background:var(--surface)"><img src="img/' + id + '.jpg" alt="' + esc(cap) + '" style="width:100%;height:145px;object-fit:cover;border-radius:6px" loading="lazy"><figcaption style="font-size:.78rem;margin-top:6px;font-weight:700">' + esc(cap) + '</figcaption></figure>').join('') + '</div></div>';
      } else if (atl.tab === 'pv') {
        const curPv = PV_STATES[atl.pv] || PV_STATES.norm;
        body = '<div class="panel"><h2>📈 Interactive Left Ventricular Pressure-Volume (PV) Loop Shifter</h2><p class="hint" style="margin:0">Tap any haemodynamic perturbation or valvular lesion below to watch how EDV, ESV, Stroke Volume (width), and Peak Systolic Pressure (height) shift against the normal baseline loop.</p>'
          + '<div class="chips">' + Object.entries(PV_STATES).map(([k, v]) => '<button class="chip' + (atl.pv === k ? ' on' : '') + '" data-pvmode="' + k + '">' + esc(v.name) + '</button>').join('') + '</div>'
          + '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;align-items:center;margin-top:8px"><div>' + pvSvgHtml(atl.pv) + '</div>'
          + '<div class="panel" style="background:var(--surface-2)"><h3>' + esc(curPv.name) + '</h3><p>' + esc(curPv.desc) + '</p>'
          + '<table><tr><th>Parameter</th><th>Value</th><th>Shift vs Normal</th></tr>'
          + '<tr><td><b>End-Diastolic Volume (EDV)</b></td><td>' + curPv.edv + ' mL</td><td>' + (curPv.edv > 120 ? '↑ Increased' : curPv.edv < 120 ? '↓ Decreased' : '↔ Unchanged') + '</td></tr>'
          + '<tr><td><b>End-Systolic Volume (ESV)</b></td><td>' + curPv.esv + ' mL</td><td>' + (curPv.esv > 50 ? '↑ Increased' : curPv.esv < 50 ? '↓ Decreased' : '↔ Unchanged') + '</td></tr>'
          + '<tr><td><b>Stroke Volume (EDV - ESV)</b></td><td><b>' + (curPv.edv - curPv.esv) + ' mL</b></td><td>' + ((curPv.edv - curPv.esv) > 70 ? '↑ Widened loop' : (curPv.edv - curPv.esv) < 70 ? '↓ Narrowed loop' : '↔ Normal width') + '</td></tr>'
          + '<tr><td><b>Peak LV Systolic Pressure</b></td><td>' + curPv.pmax + ' mmHg</td><td>' + (curPv.pmax > 120 ? '↑ Taller loop' : curPv.pmax < 120 ? '↓ Shorter loop' : '↔ Normal height') + '</td></tr></table></div></div></div>';
      } else if (atl.tab === 'shock') {
        body = '<div class="panel"><h2>🫀 Shock Haemodynamic Profiles</h2>'
          + '<table><tr><th>Shock Type</th><th>Preload (CVP / PCWP)</th><th>Cardiac Output (CO)</th><th>Afterload (SVR)</th><th>Mixed Venous O2 (SvO2)</th><th>Classic Triggers</th></tr>'
          + '<tr><td><b>Hypovolaemic</b></td><td>↓</td><td>↓</td><td>↑ (sympathetic)</td><td>↓</td><td>Haemorrhage, severe dehydration, burns, DKA</td></tr>'
          + '<tr><td><b>Cardiogenic</b></td><td><b>↑↑</b></td><td>↓↓</td><td>↑</td><td>↓</td><td>Massive anterior MI, myocarditis, acute MR/VSD</td></tr>'
          + '<tr><td><b>Obstructive</b></td><td><b>↑ CVP</b> (PCWP ↓ in PE, ↑ in tamponade)</td><td>↓</td><td>↑</td><td>↓</td><td>Cardiac tamponade, tension pneumothorax, massive saddle PE</td></tr>'
          + '<tr><td><b>Distributive · Septic / Anaphylactic</b></td><td>↓</td><td><b>↑ (early warm)</b></td><td><b>↓↓</b></td><td><b>↑</b></td><td>Gram-negative endotoxin (TNF-α, IL-1, NO), IgE mast-cell histamine</td></tr>'
          + '<tr><td><b>Distributive · Neurogenic</b></td><td>↓</td><td>↓ (bradycardia)</td><td><b>↓↓</b></td><td>↓ or ↔</td><td>Cervical/high thoracic spinal cord trauma (loss of sympathetic tone -&gt; warm dry skin + bradycardia)</td></tr></table></div>'
          + '<div class="panel"><h2>🩺 Dynamic Auscultation Maneuvers</h2>'
          + '<table><tr><th>Maneuver</th><th>Haemodynamic Change</th><th>Murmurs That get LOUDER</th><th>Murmurs That get SOFTER (or shift)</th></tr>'
          + '<tr><td><b>Inspiration</b></td><td>↑ Venous return to right heart</td><td>All <b>right-sided murmurs</b> (TR, TS, PR, PS)</td><td>Left-sided murmurs</td></tr>'
          + '<tr><td><b>Valsalva strain / Standing</b></td><td><b>↓ Preload</b> (smaller LV cavity)</td><td><b>HCM</b> (louder), <b>MVP</b> (click moves earlier, longer murmur)</td><td>AS, MR, AR, VSD all get softer</td></tr>'
          + '<tr><td><b>Rapid Squatting / Passive leg raise</b></td><td><b>↑ Preload &amp; ↑ Afterload</b> (larger LV cavity)</td><td>AS, MR, AR, VSD get louder</td><td><b>HCM</b> (softer), <b>MVP</b> (click moves later, shorter murmur)</td></tr>'
          + '<tr><td><b>Sustained Handgrip</b></td><td><b>↑ Afterload (SVR)</b></td><td><b>AR, MR, VSD</b> (more backward flow)</td><td><b>AS, HCM</b> (reduced forward ejection / wider LVOT)</td></tr></table></div>';
      } else if (atl.tab === 'resp') {
        body = '<div class="panel"><h2>🫁 Spirometry, Lung Volumes &amp; DLCO</h2>'
          + '<table><tr><th>Pattern</th><th>FEV1 / FVC</th><th>TLC &amp; RV</th><th>DLCO</th><th>A-a Gradient</th><th>Classic Diseases</th></tr>'
          + '<tr><td><b>Obstructive · Emphysema</b></td><td><b>&lt; 0.70 (↓↓)</b></td><td>↑ TLC, ↑↑ RV (air trapping)</td><td><b>↓↓</b> (alveolar wall destruction)</td><td>↑</td><td>Smoking (centriacinar upper lobe), alpha-1 antitrypsin deficiency (panacinar lower lobe)</td></tr>'
          + '<tr><td><b>Obstructive · Chronic Bronchitis / Asthma</b></td><td><b>&lt; 0.70 (↓↓)</b></td><td>↑ TLC, ↑ RV</td><td><b>↔ Normal</b> (or ↑ in asthma)</td><td>↑ in flare</td><td>Reid index &gt; 0.50 (bronchitis); reversible with albuterol / methacholine-positive (asthma)</td></tr>'
          + '<tr><td><b>Restrictive · Parenchymal (ILD)</b></td><td><b>≥ 0.70 (Normal or ↑)</b></td><td><b>↓↓ TLC, ↓ RV</b></td><td><b>↓↓</b> (thickened alveolar-capillary membrane)</td><td><b>↑</b></td><td>Idiopathic pulmonary fibrosis (honeycombing), sarcoidosis, pneumoconioses, amiodarone/bleomycin</td></tr>'
          + '<tr><td><b>Restrictive · Extraparenchymal</b></td><td><b>≥ 0.70 (Normal or ↑)</b></td><td><b>↓↓ TLC</b></td><td><b>↔ Normal</b> (intact alveolar membrane)</td><td><b>↔ Normal</b> (pure hypoventilation)</td><td>ALS, myasthenia gravis, Guillain-Barré, phrenic nerve injury, severe kyphoscoliosis, obesity</td></tr>'
          + '<tr><td><b>Pulmonary Vascular Disease</b></td><td>↔ Normal</td><td>↔ Normal</td><td><b>↓↓</b></td><td><b>↑</b></td><td>Pulmonary embolism, idiopathic pulmonary arterial hypertension (BMPR2)</td></tr></table></div>';
      } else if (atl.tab === 'cah') {
        body = '<div class="panel"><h2>🦋 Congenital Adrenal Hyperplasia (CAH) Matrix</h2>'
          + '<table><tr><th>Enzyme Deficiency</th><th>Blood Pressure</th><th>Serum K+ &amp; Renin</th><th>17-OH Progesterone</th><th>Adrenal Androgens</th><th>Phenotype (46,XX vs 46,XY)</th></tr>'
          + '<tr><td><b>21-Hydroxylase</b> (commonest)</td><td><b>↓↓ Salt-wasting shock</b></td><td><b>↑↑ K+</b>, ↑ Renin, ↓ Aldosterone</td><td><b>↑↑↑</b></td><td><b>↑↑</b></td><td><b>46,XX</b>: ambiguous genitalia (clitoromegaly) with normal ovaries/uterus; <b>46,XY</b>: normal at birth, precocious puberty</td></tr>'
          + '<tr><td><b>11β-Hydroxylase</b></td><td><b>↑↑ Hypertension</b> (high 11-DOC)</td><td><b>↓↓ K+</b>, ↓ Renin, ↓ Aldosterone</td><td><b>↑↑</b> (and ↑ 11-deoxycortisol)</td><td><b>↑↑</b></td><td><b>46,XX</b>: virilised / ambiguous genitalia + high BP; <b>46,XY</b>: precocious puberty + high BP</td></tr>'
          + '<tr><td><b>17α-Hydroxylase</b></td><td><b>↑↑ Hypertension</b> (high 11-DOC)</td><td><b>↓↓ K+</b>, ↓ Renin, ↓ Aldosterone</td><td><b>↓↓</b></td><td><b>↓↓</b> (absent DHEA &amp; oestrogens)</td><td><b>46,XX</b>: primary amenorrhoea, no pubic hair; <b>46,XY</b>: female external genitalia, blind vagina, intra-abdominal testes</td></tr></table></div>';
      } else if (atl.tab === 'heme') {
        body = '<div class="panel"><h2>🩸 Coagulation &amp; Platelet Disorder Matrix</h2>'
          + '<table><tr><th>Disorder</th><th>Platelet Count</th><th>Bleeding Time</th><th>PT (INR)</th><th>aPTT</th><th>Key Mechanism &amp; Peripheral Smear</th></tr>'
          + '<tr><td><b>ITP</b></td><td><b>↓↓</b></td><td><b>↑</b></td><td>↔</td><td>↔</td><td>Anti-GpIIb/IIIa IgG -&gt; splenic macrophage phagocytosis; ↑ megakaryocytes on marrow</td></tr>'
          + '<tr><td><b>TTP / HUS</b></td><td><b>↓↓</b></td><td><b>↑</b></td><td><b>↔ Normal</b></td><td><b>↔ Normal</b></td><td>ADAMTS13 deficiency (TTP) or Shiga toxin O157:H7 (HUS) -&gt; platelet microthrombi + <b>schistocytes</b> without factor consumption</td></tr>'
          + '<tr><td><b>DIC</b></td><td><b>↓↓</b></td><td><b>↑</b></td><td><b>↑↑</b></td><td><b>↑↑</b></td><td>Tissue factor activation (sepsis, obstetrics, APL M3) -&gt; ↓ fibrinogen, ↑ D-dimer, <b>schistocytes</b></td></tr>'
          + '<tr><td><b>Von Willebrand disease</b></td><td>↔ Normal</td><td><b>↑</b></td><td>↔</td><td><b>↑ or ↔</b> (carries FVIII)</td><td>Defective vWF impairs GpIb platelet adhesion AND reduces factor VIII half-life; treat with desmopressin</td></tr>'
          + '<tr><td><b>Haemophilia A / B</b></td><td>↔</td><td>↔</td><td>↔</td><td><b>↑↑</b></td><td>X-linked Factor VIII (A) or IX (B) deficiency; haemarthrosis, deep muscle haematomas; mixes correct aPTT</td></tr>'
          + '<tr><td><b>Bernard-Soulier vs Glanzmann</b></td><td>↓ (giant platelets in BS) vs ↔ (Glanzmann)</td><td><b>↑↑</b></td><td>↔</td><td>↔</td><td><b>GpIb</b> adhesion defect (fails ristocetin) vs <b>GpIIb/IIIa</b> aggregation defect (no clumping on smear)</td></tr></table></div>';
      } else if (atl.tab === 'neuro') {
        body = '<div class="panel"><h2>🧠 Brainstem Vascular Syndromes (Rule of 4s) &amp; Spinal Cord Tracts</h2>'
          + '<table><tr><th>Syndrome &amp; Artery</th><th>Ipsilateral Signs</th><th>Contralateral Signs</th><th>Decisive Localising Clue</th></tr>'
          + '<tr><td><b>Lateral Medullary (Wallenberg) · PICA</b></td><td>Horner, ataxia (ICP), loss of facial pain/temp (CN V), dysphagia/hoarseness/loss of gag (<b>CN IX, X: nucleus ambiguus</b>), vertigo/nystagmus (CN VIII)</td><td>Loss of body pain and temperature (spinothalamic)</td><td><b>Dysphagia, hoarseness, hiccups, absent gag reflex</b> (CN IX/X)</td></tr>'
          + '<tr><td><b>Lateral Pontine · AICA</b></td><td>Facial paralysis (<b>CN VII</b>), loss of facial sensation (CN V), <b>sensorineural deafness &amp; vertigo (CN VIII / labyrinthine artery)</b>, Horner, ataxia</td><td>Loss of body pain and temperature</td><td><b>Facial droop (CN VII) + ipsilateral deafness</b></td></tr>'
          + '<tr><td><b>Medial Medullary · ASA</b></td><td><b>Tongue deviates toward lesion (CN XII)</b></td><td>Hemiparesis (corticospinal pyramid) + loss of vibration/proprioception (medial lemniscus)</td><td><b>CN XII lower motor neuron tongue deviation</b></td></tr>'
          + '<tr><td><b>Medial Midbrain (Weber) · PCA</b></td><td><b>CN III palsy</b> (eye down and out, ptosis, blown pupil)</td><td>Contralateral hemiparesis (cerebral peduncle)</td><td><b>Oculomotor palsy + crossed hemiplegia</b></td></tr>'
          + '<tr><td><b>Syringomyelia (central canal)</b></td><td colspan="2">Bilateral <b>cape-like loss of pain and temperature</b> across shoulders/arms (anterior white commissure) + intrinsic hand LMN weakness; spares dorsal columns</td><td>Associated with <b>Chiari I malformation</b></td></tr>'
          + '<tr><td><b>Subacute Combined Degeneration (B12)</b></td><td colspan="2">Bilateral <b>dorsal columns</b> (vibration/proprioception loss, positive Romberg) + <b>lateral corticospinal tracts</b> (spastic paresis, Babinski)</td><td>Vitamin B12 deficiency, nitrous oxide abuse, Diphyllobothrium latum</td></tr>'
          + '<tr><td><b>Anterior Spinal Artery (ASA) Occlusion</b></td><td colspan="2">Bilateral corticospinal paralysis + bilateral spinothalamic pain/temp loss below lesion; <b>dorsal column vibration and proprioception SPARED</b></td><td>Thoracic aortic aneurysm repair (artery of Adamkiewicz)</td></tr></table></div>';
      } else if (atl.tab === 'storage') {
        body = '<div class="panel"><h2>🧬 Lysosomal Storage Diseases (Sphingolipidoses &amp; Mucopolysaccharidoses)</h2>'
          + '<table><tr><th>Disease</th><th>Deficient Enzyme</th><th>Accumulated Substrate</th><th>Decisive Step 1 Clinical &amp; Histology Triggers</th></tr>'
          + '<tr><td><b>Tay-Sachs</b></td><td><b>Hexosaminidase A</b></td><td><b>GM2 ganglioside</b></td><td>Infant neurodegeneration, startle, <b>cherry-red macular spot</b>, <b>NO hepatosplenomegaly</b>, EM <b>onion-skin lysosomes</b></td></tr>'
          + '<tr><td><b>Niemann-Pick</b></td><td><b>Sphingomyelinase</b></td><td><b>Sphingomyelin</b></td><td>Infant neurodegeneration, <b>cherry-red spot PLUS massive hepatosplenomegaly</b>, <b>foamy macrophages</b> (zebra bodies)</td></tr>'
          + '<tr><td><b>Gaucher (commonest)</b></td><td><b>β-Glucocerebrosidase</b></td><td><b>Glucocerebroside</b></td><td>Hepatosplenomegaly, pancytopenia, bone crises / <b>femoral AVN</b>, <b>crinkled tissue-paper macrophages</b></td></tr>'
          + '<tr><td><b>Fabry (X-linked)</b></td><td><b>α-Galactosidase A</b></td><td><b>Ceramide trihexoside (Gb3)</b></td><td>Boys with triad of <b>episodic peripheral neuropathy, angiokeratomas, hypohidrosis</b> -&gt; renal/cardiac failure</td></tr>'
          + '<tr><td><b>Krabbe</b></td><td><b>Galactocerebrosidase</b></td><td><b>Galactocerebroside &amp; psychosine</b></td><td>Peripheral neuropathy, developmental delay, <b>optic atrophy (NO cherry-red spot)</b>, multinucleated <b>globoid cells</b></td></tr>'
          + '<tr><td><b>Metachromatic Leukodystrophy</b></td><td><b>Arylsulfatase A</b></td><td><b>Cerebroside sulfate</b></td><td>Central and peripheral demyelination with <b>ataxia, dementia, absent reflexes</b></td></tr>'
          + '<tr><td><b>Hurler vs Hunter (X-linked)</b></td><td><b>α-L-iduronidase</b> vs <b>Iduronate-2-sulfatase</b></td><td><b>Heparan &amp; dermatan sulfate</b></td><td>Coarse facies, hepatosplenomegaly; <b>Hunter = X-linked, Milder, NO corneal clouding</b> (Hunters see clearly)</td></tr>'
          + '<tr><td><b>I-Cell Disease</b></td><td><b>GlcNAc-1-phosphotransferase</b></td><td>Uncleaved lysosomal substrates</td><td>Golgi fails to add <b>mannose-6-phosphate</b> tag -&gt; high plasma lysosomal enzymes, coarse facies, <b>corneal clouding</b></td></tr></table></div>'
          + '<div class="panel"><h2>🍬 Glycogen Storage Diseases (Types I, II, III, V)</h2>'
          + '<table><tr><th>Type</th><th>Deficient Enzyme</th><th>Key Step 1 Discriminators</th></tr>'
          + '<tr><td><b>Type I (Von Gierke)</b></td><td><b>Glucose-6-phosphatase</b></td><td>Severe fasting hypoglycaemia, <b>↑↑ blood lactate, ↑↑ uric acid (gout), ↑↑ triglycerides</b>, massive hepatorenomegaly</td></tr>'
          + '<tr><td><b>Type II (Pompe)</b></td><td><b>Lysosomal α-1,4-glucosidase (acid maltase)</b></td><td><b>Cardiomegaly / hypertrophic cardiomyopathy, macroglossia, profound hypotonia</b> (Pompe trashes the Pump)</td></tr>'
          + '<tr><td><b>Type III (Cori)</b></td><td><b>Debranching enzyme</b></td><td>Milder fasting hypoglycaemia, hepatomegaly, accumulation of cytosolic <b>limit dextrin</b>, and <b>NORMAL blood lactate</b></td></tr>'
          + '<tr><td><b>Type V (McArdle)</b></td><td><b>Skeletal muscle glycogen phosphorylase (myophosphorylase)</b></td><td>Exercise cramps, myoglobinuria, <b>flat venous lactate curve with ↑ ammonia</b>, and <b>second-wind phenomenon</b></td></tr></table></div>';
      }
      m.innerHTML = '<div class="wrap"><div class="ph"><div class="crumbs"><span class="code">🫀 System maps</span></div><h1>High-Yield USMLE Step 1 Visual Matrices</h1><p class="hint" style="margin:0">Rapid-scan visual tables, interactive PV-loop simulator, storage disease subway, and all 60 UWorld pathology/radiology plates.</p></div>'
        + '<div class="s1-drugs">' + ATL_TABS.map(([k, l]) => '<button class="chip' + (atl.tab === k ? ' on' : '') + '" data-atltab="' + k + '">' + l + '</button>').join('') + '</div>'
        + body + '</div>';
    });
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-atltab],[data-pvmode],[data-hqtwpick]');
      if (!b) return;
      if (b.dataset.hqtwpick) {
        const [qid, pickStr] = b.dataset.hqtwpick.split('|'), pick = +pickStr;
        const qObj = ME.hqItem(qid); if (!qObj || !qObj.tw) return;
        const box = b.closest('[data-hqtw]'); if (!box || box.classList.contains('done')) return;
        box.classList.add('done');
        $$('[data-hqtwpick]', box).forEach(btn => {
          const k = +btn.dataset.hqtwpick.split('|')[1];
          btn.disabled = true;
          btn.classList.add(k === qObj.tw.a ? 'right' : k === pick ? 'wrong' : '');
        });
        const whyEl = box.querySelector('.hq-twwhy'); if (whyEl) whyEl.hidden = false;
        if (pick === qObj.tw.a) ME.addXp(3);
        return;
      }
      if (ME.route.view !== 'atlas') return;
      if (b.dataset.atltab) { atl.tab = b.dataset.atltab; ME.render(); }
      else if (b.dataset.pvmode) { atl.pv = b.dataset.pvmode; ME.render(); }
    });


    /* ================================================================ v3.6.1: bank sources, performance map, AI 4-box and twins */
    const SRC = q => q.src === 'medengine' ? 'me' : q.src === 'UWorld' || q.uw_qid || q.uworld_qid ? 'uw' : q.src === 'Mehlman HY Arrows' ? 'mh' : 'me';
    const SRCL = {uw: '🟦 UWorld', mh: '↕ Mehlman arrows', me: '🎯 medengine originals'};
    blk.cfg.so = blk.cfg.so || 'all';
    const basePool = pool;
    pool = function () { const so = blk.cfg.so; return basePool().filter(q => so === 'all' || SRC(q) === so); };
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-bkso]'); if (!b || ME.route.view !== 'block') return;
      blk.cfg.so = b.dataset.bkso; viewBlockSetup($('#main'));
    }, true);
    const baseSetup = viewBlockSetup;
    viewBlockSetup = function (m) {
      baseSetup(m);
      const row = m.querySelector('.s1-setup .s1-row:nth-child(2)'); if (!row) return;
      const cnt = k => (D.hq.q || []).filter(q => k === 'all' || SRC(q) === k).length;
      row.insertAdjacentHTML('afterend', '<div class="s1-row"><span>Bank</span>' + ['all', 'uw', 'mh', 'me'].map(k => '<button class="chip' + (blk.cfg.so === k ? ' on' : '') + '" data-bkso="' + k + '">' + (k === 'all' ? 'All' : SRCL[k]) + ' · ' + cnt(k) + '</button>').join('') + '</div>');
    };
    ME.view('block', m => { viewBlockSetup(m); const r = resultHtml(); if (r) m.querySelector('.ph').insertAdjacentHTML('afterend', r); });

    /* last answer to every question, from Hammer runs and timed blocks */
    function lastAnswers() {
      const m = {};
      (ME.hqRuns() || []).slice().reverse().forEach(r => Object.entries(r.pk || {}).forEach(([id, p]) => { const q = ME.hqItem(id); if (q) m[id] = p === q.a; }));
      st().blocks.forEach(b => (b.ids || []).forEach((id, j) => { const q = ME.hqItem(id), p = (b.pk || [])[j]; if (q && p != null) m[id] = p === q.a; }));
      return m;
    }
    function perfHtml() {
      const la = lastAnswers(), by = {};
      Object.entries(la).forEach(([id, ok]) => { const q = ME.hqItem(id); if (!q || !U[+q.k]) return; const w = U[+q.k].w; const g = by[w] = by[w] || [0, 0]; g[1]++; if (ok) g[0]++; });
      const rows = W.map(w => [w, by[w.id] || [0, 0], (D.hq.q || []).filter(q => U[+q.k] && U[+q.k].w === w.id).length]).filter(r => r[2]);
      const seenN = Object.keys(la).length;
      if (!seenN) return '<section class="panel s1-perf"><b>📊 Where you stand</b><p class="hint" style="margin:0">Answer a block and every First Aid chapter gets a score here, weakest first, each one a tap away from a targeted block.</p></section>';
      const weak = rows.filter(r => r[1][1] >= 3).sort((a, b) => a[1][0] / a[1][1] - b[1][0] / b[1][1]).slice(0, 3);
      return '<section class="panel s1-perf"><div class="toolbar"><b class="grow">📊 Where you stand · ' + seenN + ' of ' + D.hq.q.length + ' questions done</b></div>'
        + '<div class="s1-bars">' + rows.map(([w, g, n]) => { const pc = g[1] ? Math.round(g[0] / g[1] * 100) : null; return '<div class="s1-bar1" title="' + esc(w.name) + ': ' + g[0] + ' of ' + g[1] + ' right, ' + n + ' in the bank"><span class="s1-bn">' + esc(w.name) + '</span><span class="s1-bt"><i style="width:' + Math.round(g[1] / n * 100) + '%" class="seen"></i><i style="width:' + (pc == null ? 0 : Math.round(g[0] / n * 100)) + '%" class="' + (pc == null ? '' : pc >= 70 ? 'ok' : pc >= 55 ? 'mid' : 'low') + '"></i></span><b>' + (pc == null ? '·' : pc + '%') + '</b></div>'; }).join('') + '</div>'
        + (weak.length ? '<div class="toolbar"><span class="hint grow">Weakest: ' + weak.map(r => esc(r[0].name) + ' ' + Math.round(r[1][0] / r[1][1] * 100) + '%').join(' · ') + '</span>' + weak.map(r => '<button class="btn sm" data-s1weak="' + r[0].id + '">⏱️ ' + esc(r[0].name.split(/[ ,&]/)[0]) + ' block</button>').join('') + '</div>' : '')
        + '<p class="hint" style="margin:0">Bar length is how much of the chapter you have seen; colour is how much of it you got right last time.</p></section>';
    }
    const baseHome = ME.EXT.homeTop;
    ME.EXT.homeTop = () => baseHome() + perfHtml();
    document.addEventListener('click', e => {
      const b = e.target.closest && e.target.closest('[data-s1weak]'); if (!b) return;
      Object.assign(blk.cfg, {ch: b.dataset.s1weak, src: 'all', st: 'any', so: 'all', n: 20}); ME.go({view: 'block'});
    });

    /* AI: sharpen any question's 4 boxes, or make a twin with a new patient; cached per question in your Step 1 save */
    const ai = () => { const s = st(); s.ai = s.ai || {}; return s.ai; };
    const aiBusy = {};
    function applyAi(q) {
      const a = ai()[q.id]; if (!a || !a.tm) return;
      q.tm = Object.assign({}, q.tm || {}, a.tm);
    }
    (D.hq.q || []).forEach(applyAi);
    const LET = 'ABCDEFGHI';
    function qPrompt(q, task) {
      return 'You are a USMLE Step 1 tutor. ' + task + '\nWrite everything in your own words in British English, no em dashes. Return JSON only.\n'
        + 'STEM: ' + q.s.replace(/\n/g, ' ') + '\nQUESTION: ' + q.ql + '\nOPTIONS: ' + q.o.map((o, i) => LET[i] + '. ' + o).join(' | ') + '\nANSWER: ' + LET[q.a] + '. ' + q.o[q.a]
        + '\nEXPLANATION: ' + String(q.w || '').slice(0, 4000) + (q.eo ? '\nOBJECTIVE: ' + q.eo : '');
    }
    async function aiSharpen(q) {
      if (!AI || aiBusy[q.id]) return; aiBusy[q.id] = 1; rerender(q.id);
      try {
        const j = await AI.json(qPrompt(q, 'Rebuild this question\'s 4-box explanation. Shape: {"red_flags": ["2 to 4 short phrases copied EXACTLY from the stem that decide it"], "money_line": "one sentence: the fact that decides it", "inflow": ["3 to 6 short links from root cause to what is asked"], "film": [{"option": "letter of a WRONG option", "if": "the one change to the case that would make that option right"}, one for every wrong option], "why_not": [{"option": "letter of a WRONG option", "why": "one sentence"}, one for every wrong option]}'), {modelTier: 'default', maxTokens: 1800});
        const idx = l => LET.indexOf(String(l || '').trim().charAt(0).toUpperCase());
        const S = x => String(x || '').replace(/—/g, ', ').trim();
        const tm = {c: (j.red_flags || []).map(S).filter(c => c && q.s.toLowerCase().includes(c.toLowerCase())).slice(0, 4), g: S(j.money_line), m: (j.inflow || []).map(S).filter(Boolean).join(' → '),
          f: (j.film || []).map(f => [S(f.if), idx(f.option)]).filter(f => f[0] && f[1] >= 0 && f[1] !== q.a && f[1] < q.o.length), x: (j.why_not || []).map(x => [idx(x.option), S(x.why)]).filter(x => x[1] && x[0] >= 0 && x[0] !== q.a && x[0] < q.o.length)};
        if (!tm.g || tm.f.length < 2) throw {code: 'thin'};
        if (tm.c.length < 2) tm.c = (q.tm && q.tm.c) || tm.c;
        ai()[q.id] = Object.assign(ai()[q.id] || {}, {tm, at: Date.now()}); applyAi(q); ME.addXp(2); ME.save();
      } catch (e) { ME.toast(e && e.code === 'thin' ? 'The AI reply was too thin. Try again.' : 'The AI could not answer (' + ((e && (e.code || e.message)) || 'error') + ')'); }
      delete aiBusy[q.id]; rerender(q.id);
    }
    async function aiTwin(q) {
      if (!AI || aiBusy[q.id]) return; aiBusy[q.id] = 1; rerender(q.id);
      try {
        const j = await AI.json(qPrompt(q, 'Write ONE new twin question that tests the same fact with a different patient, different wording and US units and drug names. Shape: {"stem": "60 to 100 words", "question": "lead-in", "options": ["5 options, alphabetical"], "answer": 0, "why": "2 or 3 sentences, British English"}'), {modelTier: 'default', maxTokens: 1400});
        const o = (j.options || []).map(x => String(x).trim()).filter(Boolean);
        if (!j.stem || o.length < 4 || !(+j.answer >= 0 && +j.answer < o.length)) throw {code: 'thin'};
        ai()[q.id] = Object.assign(ai()[q.id] || {}, {tw: {s: String(j.stem), ql: String(j.question || 'Which of the following is most likely?'), o, a: +j.answer, w: String(j.why || '')}});
        ME.addXp(2); ME.save();
      } catch (e) { ME.toast(e && e.code === 'thin' ? 'The twin came back incomplete. Try again.' : 'The AI could not answer (' + ((e && (e.code || e.message)) || 'error') + ')'); }
      delete aiBusy[q.id]; rerender(q.id);
    }
    function rerender(id) {
      if (ME.route.view === 'hammer') { const y = window.scrollY; ME.render(); window.scrollTo(0, y); return; }
      const ex = document.querySelector('[data-s1x="' + id + '"]'), q = ME.hqItem(id); if (ex && q) ex.outerHTML = extraHtml(q);
    }
    function extraHtml(it) {
      const q = ME.hqItem(it.id) || it, a = ai()[q.id] || {}, sk = SRC(q), busy = aiBusy[q.id];
      let h = '<div class="s1-x" data-s1x="' + esc(q.id) + '"><div class="s1-xh"><span class="s1-chip ghost">' + SRCL[sk] + (q.uw_qid || q.uworld_qid ? ' · QID ' + esc(String(q.uw_qid || q.uworld_qid)) : '') + '</span>'
        + (U[+q.k] ? '<button class="ulink" data-u="' + U[+q.k].i + '" data-mode="fill">↗ ' + esc(U[+q.k].name) + '</button>' : '') + (a.tm ? '<span class="s1-chip deep">🤖 4 boxes sharpened by AI</span>' : '') + '<span class="grow"></span>'
        + (busy ? '<span class="rmx-busy">Thinking…</span>' : AI ? (a.tm ? '' : '<button class="btn sm" data-s1sharp="' + esc(q.id) + '">🤖 Sharpen the 4 boxes</button>') + (a.tw ? '' : '<button class="btn sm" data-s1twin="' + esc(q.id) + '">🔗 Make a twin</button>') : '<span class="hint">🔑 Add an AI key for twins and sharper boxes</span>') + '</div>';
      if (a.tw) {
        const t = a.tw;
        h += '<div class="s1-twin" data-aitw="' + esc(q.id) + '"><div class="s1-bk">🔗 Twin: same fact, new patient</div><p>' + rich(t.s) + '</p><p><b>' + rich(t.ql) + '</b></p>'
          + t.o.map((x, k) => '<button class="hq-o s1-two" data-aitwp="' + esc(q.id) + '|' + k + '"><span class="hq-l">' + LET[k] + '</span><span class="hq-ot">' + esc(x) + '</span></button>').join('') + '<div class="s1-tww" hidden>' + rich(t.w) + '</div></div>';
      }
      if ((q.cards || []).length) h += '<details class="s1-cards"><summary>🃏 ' + q.cards.length + ' Anki card' + (q.cards.length > 1 ? 's' : '') + ' from this question</summary><table>' + q.cards.map(c => '<tr><td>' + rich(c[0]) + '</td><td>' + rich(c[1]) + '</td></tr>').join('') + '</table><div class="toolbar"><button class="btn sm" data-s1qcopy="' + esc(q.id) + '">📋 Copy for Anki</button></div></details>';
      return h + '</div>';
    }
    ME.EXT.tmExtra = it => extraHtml(it);
    document.addEventListener('click', e => {
      const t = e.target.closest && e.target.closest('[data-s1sharp],[data-s1twin],[data-aitwp],[data-s1qcopy]'); if (!t) return;
      const d = t.dataset;
      if (d.s1sharp) { const q = ME.hqItem(d.s1sharp); if (q) aiSharpen(q); }
      else if (d.s1twin) { const q = ME.hqItem(d.s1twin); if (q) aiTwin(q); }
      else if (d.s1qcopy) { const q = ME.hqItem(d.s1qcopy); if (q) copy(q.cards.map(c => [c[0], c[1], 'step1 ' + ((U[+q.k] || {}).w || '')].map(x => String(x).replace(/\*\*/g, '').replace(/[\t\n]+/g, ' ')).join('\t')).join('\n'), q.cards.length + ' cards'); }
      else if (d.aitwp) {
        const [id, k] = d.aitwp.split('|'), tw = (ai()[id] || {}).tw, box = t.closest('.s1-twin'); if (!tw || box.classList.contains('done')) return;
        box.classList.add('done');
        $$('[data-aitwp]', box).forEach(b => { const kk = +b.dataset.aitwp.split('|')[1]; b.disabled = true; b.classList.add(kk === tw.a ? 'ok' : kk === +k ? 'bad' : 'dim'); });
        $('.s1-tww', box).hidden = false; if (+k === tw.a) ME.addXp(3);
      }
    });

  }
})();
