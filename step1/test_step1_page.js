// Browser test for step1.html: node step1/test_step1_page.js http://localhost:PORT/step1.html [shots-dir]
const { chromium } = require('playwright');
const URL = process.argv[2], SHOTS = process.argv[3] || '';
const FFP = {'qq-drill-ilo-v1': '{"sentinel":"study"}', 'medengine-misses-v1': '{"items":[1]}', 'medengine-trg': '{"lock":true}', 'qq-osce-v1': '{"osce":1}', 'medengine-shots-v1': '[]', 'medengine-cloud-cache-v1': '{"x":1}', 'medengine-accounts-v3': '{"a":1}'};
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext({viewport: {width: 1280, height: 900}});
  await ctx.addInitScript(seed => { if (!sessionStorage.getItem('seeded')) { Object.entries(seed).forEach(([k, v]) => localStorage.setItem(k, v)); sessionStorage.setItem('seeded', '1'); } }, FFP);
  const p = await ctx.newPage(); const errs = []; let fails = 0;
  const ok = (c, m) => { if (!c) { fails++; console.log('FAIL', m); } else console.log('ok  ', m); };
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/favicon|net::ERR|Failed to load resource/.test(m.text())) errs.push(m.text()); });
  p.on('dialog', d => d.accept());
  const shot = async n => { if (SHOTS) await p.screenshot({path: SHOTS + '/' + n + '.png'}); };
  await p.goto(URL); await p.waitForTimeout(1200);
  const D = await p.evaluate(() => ({units: ME.UNITS.length, q: ME.D.hq.q.length, pilot: ME.UNITS.filter(u => u.pilot).map(u => u.i), title: document.title}));
  ok(D.title === 'medengine-STEP1' && D.units > 200 && D.q >= 50, 'loads the Step 1 pack: ' + JSON.stringify({units: D.units, q: D.q}));
  // exam date
  await p.fill('#s1Exam', '2027-03-15'); await p.dispatchEvent('#s1Exam', 'change'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => ME.S.s1.exam === '2027-03-15' && !!document.querySelector('.s1-cd')), 'exam date saved and countdown shown');
  await shot('home');
  // a pilot unit: fill blanks drop-downs
  await p.evaluate(u => ME.go({view: 'unit', u, mode: 'fill'}), D.pilot[7]); await p.waitForTimeout(300);
  const dd = await p.$$eval('select.dd', s => s.length);
  ok(dd >= 15, 'pilot topic has drop-down blanks: ' + dd);
  await p.selectOption('select.dd >> nth=0', {index: 1}); await p.waitForTimeout(150);
  ok(await p.$$eval('.rev', r => r.length) === 1, 'answering a drop-down reveals it');
  await shot('unit_fill');
  // think mode: arrows with roles and flips
  const flipU = await p.evaluate(() => { const ar = ME.D.ar || []; const u = ME.UNITS.find(u => u.pilot && ar.some(a => String(a.u) === String(u.i) && (a.fl || []).length)); return u ? u.i : ME.UNITS.filter(u => u.pilot)[5].i; });
  await p.evaluate(u => ME.go({view: 'unit', u, mode: 'think'}), flipU); await p.waitForTimeout(300);
  const nAr = await p.$$eval('.ar', a => a.length);
  ok(nAr >= 1, 'think mode shows arrows: ' + nAr);
  const rows = await p.$$('.ar >> nth=0 >> .ar-r');
  for (const r of rows) { const bt = await r.$('.ar-b'); await bt.click(); }
  await p.waitForTimeout(200);
  ok(await p.$$eval('.ar >> nth=0', () => true) && await p.$$eval('.ar-role', r => r.length) > 0, 'role chips appear after answering');
  const flips = await p.$$eval('[data-arflip]', b => b.length);
  ok(flips > 0, 'change-the-film flip buttons: ' + flips);
  if (flips) { await p.click('[data-arflip] >> nth=0'); await p.waitForTimeout(200); ok(await p.$$eval('.ar-isflip', b => b.length) === 1, 'flip opens a new arrow card'); }
  await shot('think_arrows');
  // hammer: questions for a pilot topic and the 4-box explanation
  await p.evaluate(() => { location.hash = 'hq-u' + ME.UNITS.find(u => u.pilot && ME.D.hq.q.some(q => q.k === String(u.i) && q.src === 'medengine')).i; }); await p.evaluate(() => ME.go(ME.route, false));
  await p.goto(URL.split('#')[0] + '#hq-u' + await p.evaluate(() => ME.UNITS.find(u => u.pilot && ME.D.hq.q.some(q => q.k === String(u.i) && q.src === 'medengine')).i)); await p.waitForTimeout(900);
  const hasQ = await p.$$eval('[data-hqpick]', b => b.length);
  ok(hasQ === 5, 'hammer question shows 5 options');
  await p.click('[data-hqpick="0"]'); await p.waitForTimeout(150);
  const cf = await p.$('[data-hqcommit]'); if (cf) await cf.click(); await p.waitForTimeout(400);
  const tm = await p.evaluate(() => (document.querySelector('.tm') || {}).innerText || '');
  ok(/4-box deconstruct/i.test(tm) && /Red flags/i.test(tm) && /Money line/i.test(tm) && /Inflow → outflow/i.test(tm) && /Change the film/i.test(tm), '4-box explanation labels');
  ok((tm.match(/🔀 Right instead if/g) || []).length >= 4 && (tm.match(/Why not/g) || []).length >= 1, 'every wrong option shows its change-the-film flip in its own card');
  await shot('hammer_4box');
  // timed block
  await p.evaluate(() => ME.go({view: 'block'})); await p.waitForTimeout(200);
  await p.click('[data-bkn="10"]'); await p.click('[data-bkstart]'); await p.waitForTimeout(300);
  ok(await p.$$eval('.s1-nb', b => b.length) === 10, 'block of 10 with a navigator');
  ok(!(await p.$('.hq-qtop')), 'lead-in only at the bottom in exam mode');
  for (let i = 0; i < 4; i++) { await p.keyboard.press('ABCD'[i]); await p.waitForTimeout(80); await p.keyboard.press('ArrowRight'); await p.waitForTimeout(80); }
  await p.click('[data-bkx="1"]'); await p.click('[data-bkmark]'); await p.click('[data-bklabs]'); await p.waitForTimeout(150);
  ok(await p.$eval('#bkLabs', a => !a.hidden), 'lab values drawer opens in the block');
  await shot('block_exam');
  ok(await p.evaluate(() => ME.S.s1.cur && Object.keys(ME.S.s1.cur.pk).length === 4), 'four answers held, no feedback yet');
  await p.click('[data-bkendask]'); await p.waitForTimeout(400);
  ok(await p.$('.s1-result') !== null, 'results panel after ending the block');
  await shot('block_result');
  await p.click('.s1-result [data-bkrev]'); await p.waitForTimeout(500);
  ok(await p.evaluate(() => ME.route.view === 'hammer' && !!document.querySelector('.hq-o.ok')), 'review opens the engine run with answers marked');
  // deconstruct by hand
  await p.evaluate(() => ME.go({view: 'deconstruct'})); await p.waitForTimeout(200);
  await p.click('[data-dcmanual]'); await p.waitForTimeout(150);
  await p.fill('#mTopic', 'Liddle vs Conn'); await p.fill('#mRf', 'low renin\nlow aldosterone'); await p.fill('#mMo', 'Low aldosterone with hypertension means the channel works alone');
  await p.fill('#mIn', 'ENaC stuck open → Na in → volume up → renin down'); await p.fill('#mCf', 'aldosterone high → Conn syndrome'); await p.fill('#mCards', 'Liddle treatment | amiloride');
  await p.click('[data-dcmsave]'); await p.waitForTimeout(300);
  ok(await p.evaluate(() => ME.S.s1.dc.length === 1 && ME.S.s1.dc[0].cards.length === 1 && ME.S.s1.dc[0].film.length === 1), 'manual deconstruction saved with its card and flip');
  await shot('deconstruct');
  // tools
  for (const v of ['abg', 'nephron', 'labs', 'triggers', 'jargon', 'gloss', 'why', 'fw']) { await p.evaluate(v => ME.go({view: v}), v); await p.waitForTimeout(250); }
  await p.evaluate(() => ME.go({view: 'abg'})); await p.click('[data-abgpre="6"]'); await p.waitForTimeout(200);
  ok(/Respiratory alkalosis \+ high anion gap metabolic acidosis/.test(await p.$eval('.s1-abgsum', e => e.innerText)), 'compass reads the aspirin preset as a double disorder');
  await shot('abg');
  await p.evaluate(() => ME.go({view: 'nephron'})); await p.click('[data-nmdrug="Thiazides"]'); await p.waitForTimeout(200);
  ok(/Distal convoluted tubule/.test(await p.$eval('.s1-seginfo h2', e => e.innerText)) && await p.$$eval('.s1-seg.hit', s => s.length) === 1, 'nephron map lights the thiazide segment');
  await shot('nephron');
  await p.evaluate(() => ME.go({view: 'jargon'})); await p.waitForTimeout(200);
  ok(await p.$$eval('.jg', j => j.length) >= 40, 'eponym decoder cards');
  // isolation: STUDY and OSCE keys untouched, new keys are Step 1 or shared only
  const ls = await p.evaluate(() => Object.fromEntries(Object.keys(localStorage).map(k => [k, localStorage.getItem(k)])));
  ok(Object.entries(FFP).every(([k, v]) => ls[k] === v), 'STUDY and OSCE storage untouched');
  const SHARED = /^medengine-(anthropic-key|groq-model|ai-mode|models|launcher-theme|cloud-cfg-v1|dev-pen)$/;
  const stray = Object.keys(ls).filter(k => !(k in FFP) && !/^(qq-step1-|medengine-step1-)/.test(k) && !SHARED.test(k));
  ok(!stray.length, 'no stray storage keys: ' + stray.join(', '));
  ok(await p.evaluate(() => JSON.parse(localStorage.getItem('qq-step1-v1')).s1.blocks.length === 1), 'Step 1 progress lives in qq-step1-v1');
  // phone width
  await p.setViewportSize({width: 390, height: 844}); await p.evaluate(() => ME.go({view: 'home'})); await p.waitForTimeout(300);
  ok(await p.evaluate(() => document.documentElement.scrollWidth <= 392), 'no sideways scroll on a phone');
  await shot('phone_home');
  ok(!errs.length, 'no page errors' + (errs.length ? ': ' + errs.slice(0, 5).join(' | ') : ''));
  console.log(fails ? fails + ' FAILED' : 'ALL PASSED');
  await b.close(); process.exit(fails ? 1 : 0);
})();
