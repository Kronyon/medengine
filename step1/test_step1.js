// Unit tests for the pure parts of the STEP1 add-on: node step1/test_step1.js
const A = require('./ext_step1.js');
let fail = 0, n = 0;
const ok = (c, msg) => { n++; if (!c) { fail++; console.log('FAIL', msg); } };
const has = (r, s) => r.summary.toLowerCase().includes(s.toLowerCase());

// classic gases: [label, input, phrases the summary must contain, phrases it must not]
const CASES = [
  ['DKA', {ph: 7.21, pco2: 24, hco3: 10, na: 134, cl: 99, alb: 4}, ['high anion gap metabolic acidosis', 'appropriately compensated'], ['respiratory']],
  ['diarrhoea', {ph: 7.30, pco2: 31, hco3: 15, na: 137, cl: 114}, ['normal anion gap metabolic acidosis'], ['high anion gap']],
  ['vomiting', {ph: 7.52, pco2: 48, hco3: 37, na: 136, cl: 88}, ['metabolic alkalosis', 'appropriately compensated'], ['acidosis']],
  ['opioid overdose', {ph: 7.22, pco2: 68, hco3: 26}, ['acute respiratory acidosis'], ['metabolic']],
  ['COPD retainer', {ph: 7.35, pco2: 60, hco3: 31}, ['chronic respiratory acidosis'], ['metabolic']],
  ['panic attack', {ph: 7.56, pco2: 24, hco3: 21}, ['respiratory alkalosis'], ['metabolic']],
  ['aspirin', {ph: 7.45, pco2: 20, hco3: 14, na: 140, cl: 102}, ['respiratory alkalosis', 'high anion gap metabolic acidosis'], []],
  ['COPD on diuretics', {ph: 7.40, pco2: 60, hco3: 36}, ['respiratory acidosis', 'metabolic alkalosis'], []],
  ['DKA plus vomiting', {ph: 7.40, pco2: 40, hco3: 24, na: 140, cl: 95}, ['high anion gap metabolic acidosis', 'metabolic alkalosis'], []],
  ['normal', {ph: 7.40, pco2: 40, hco3: 24, na: 140, cl: 104}, ['no acid-base disorder'], []],
  ['tiring asthmatic in DKA', {ph: 7.05, pco2: 35, hco3: 9.5, na: 138, cl: 100}, ['metabolic acidosis', 'respiratory acidosis'], []]
];
CASES.forEach(([lab, inp, yes, no]) => {
  const r = A.abgSolve(inp);
  ok(r.ok, lab + ': solved');
  yes.forEach(s => ok(has(r, s), lab + ': expected "' + s + '" in "' + r.summary + '"'));
  no.forEach(s => ok(!has(r, s), lab + ': did not expect "' + s + '" in "' + r.summary + '"'));
});
// numbers
const dka = A.abgSolve({ph: 7.21, pco2: 24, hco3: 10, na: 134, cl: 99});
ok(dka.ag === 25 && dka.dd === 0.93, 'DKA anion gap 25 and delta ratio 0.93, got ' + dka.ag + ' ' + dka.dd);
const glycol = A.abgSolve({ph: 7.15, pco2: 20, hco3: 7, na: 140, cl: 102, osm: 330, glu: 90, bun: 14});
ok(glycol.og === 40, 'antifreeze osmolar gap 40, got ' + glycol.og);
const alb = A.abgSolve({ph: 7.30, pco2: 30, hco3: 15, na: 140, cl: 114, alb: 2});
ok(alb.ag === 11 && alb.agc === 16, 'albumin 2 corrects a gap of 11 to 16, got ' + alb.ag + ' ' + alb.agc);
ok(has(alb, 'high anion gap'), 'albumin correction unmasks a high gap');
ok(!A.abgSolve({ph: '', pco2: 40, hco3: 24}).ok, 'missing pH refused');
ok(A.abgSolve({ph: 7.4, pco2: 80, hco3: 10}).flags.length > 0, 'impossible gas flagged by Henderson-Hasselbalch');
// lab bridge
const row = name => A.LABS.find(r => r[1].startsWith(name));
ok(A.siRange(row('Creatinine')) === '53–106', 'creatinine to µmol/L: ' + A.siRange(row('Creatinine')));
ok(A.siRange(row('Glucose, fasting')) === '3.89–5.55', 'glucose to mmol/L: ' + A.siRange(row('Glucose, fasting')));
ok(A.siRange(row('HbA1c')) === '<39', 'HbA1c to mmol/mol: ' + A.siRange(row('HbA1c')));
ok(A.siRange(row('White cells')) === '4.5–11', 'white cells to 10⁹/L: ' + A.siRange(row('White cells')));
ok(Math.abs(A.convert(row('PaCO₂'), 7.5 / 0.133, false) - 7.5) < 0.01, 'PaCO₂ round trip');
ok(Math.abs(A.convert(row('HbA1c'), A.convert(row('HbA1c'), 6.5, false), true) - 6.5) < 1e-9, 'HbA1c round trip');
ok(A.LABS.every(r => r.length === 7 && r[0] && r[1] && r[2]), 'every lab row complete');
console.log(n - fail + ' / ' + n + ' passed');
process.exit(fail ? 1 : 0);
