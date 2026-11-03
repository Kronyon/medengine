// v3.3.0 OSCE checks: mnemonics, grader safety checks, private circuit vault, voice hint, STUDY bridge
const { chromium } = require('playwright');
const path = require('path');
const BASE = process.argv[2] || 'http://localhost:8765';
const PACK = process.argv[3];
const PK = PACK ? JSON.parse(require('fs').readFileSync(PACK, 'utf8')) : null;
const OUT = require('os').tmpdir();
const fails = [];
const ok = (c, m) => { if (!c) { fails.push(m); console.log('  ✗ ' + m); } else console.log('  ✓ ' + m); };

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error' && !/Failed to load resource|net::ERR|favicon/i.test(m.text())) errors.push('console: ' + m.text()); });

  console.log('load');
  await page.goto(BASE + '/osce.html', { waitUntil: 'load' });
  await page.waitForTimeout(800);
  ok(errors.length === 0, 'no errors on load ' + errors.join(' | '));
  ok(await page.locator('#nav button[data-v="mn"]').count() === 1, 'nav has 🧬 Mnemonics');
  ok(await page.locator('#nav button[data-v="my"]').count() === 1, 'nav has 🔒 My circuit');
  const eyebrow = await page.locator('.hero .eyebrow').first().textContent();
  ok(/v3\.3\.\d/.test(eyebrow), "home shows the version: " + eyebrow.slice(0, 40));

  console.log('mnemonic hub');
  await page.click('#nav button[data-v="mn"]');
  await page.waitForTimeout(300);
  const items = await page.locator('#mnList .mn-item').count();
  ok(items >= 80, 'hub lists all mnemonics (' + items + ')');
  await page.fill('#mnQ', 'tray');
  await page.waitForTimeout(200);
  const tray = await page.locator('#mnList .mn-item').count();
  ok(tray >= 1 && tray < 10, 'search filters (' + tray + ' for "tray")');
  ok(await page.locator('#mnQ').evaluate(el => document.activeElement === el), 'search box keeps focus while typing');
  await page.fill('#mnQ', '');
  await page.selectOption('#mnK', 'none');
  await page.waitForTimeout(200);
  const nones = await page.locator('#mnList .mn-item').count();
  ok(nones >= 2 && nones <= 6, 'kind filter: ⛔ no-mnemonic entries (' + nones + ')');
  await page.selectOption('#mnK', '');
  await page.click('[data-mnquiz]');
  await page.waitForTimeout(200);
  const hidden = await page.locator('#mnList .mn-l.hid').count();
  ok(hidden > 50, 'quiz hides the meanings (' + hidden + ')');
  await page.locator('#mnList .mn-l.hid').first().click();
  await page.waitForTimeout(150);
  ok(await page.locator('#mnList .mn-l.hid').count() === hidden - 1, 'tap reveals one letter');
  await page.click('[data-mnquiz]');

  console.log('station mnemonic card (venepuncture)');
  await page.goto(BASE + '/osce.html#p-venep');
  await page.waitForTimeout(600);
  const card = page.locator('#mnCard');
  ok(await card.count() === 1, 'mnemonic card on the station');
  const codes = await page.locator('#mnCard .mn-code').allTextContents();
  ok(codes.some(c => /TAGBS-P/.test(c)), 'TAGBS-P shown (' + codes.slice(0, 6).join(', ') + ')');
  await page.locator('#mnCard > summary').click();
  await page.click('#mnCard [data-mnadd]');
  await page.fill('#mnCode', 'TEST-1');
  await page.fill('#mnFor', 'my test');
  await page.fill('#mnLetters', 'T = Tourniquet\nE = Elbow');
  await page.click('[data-mnsave]');
  await page.waitForTimeout(200);
  ok((await page.locator('#mnCard .mn-code').allTextContents()).includes('TEST-1'), 'custom mnemonic saved to the station');
  await page.locator('#mnCard [data-mndel]').first().click();
  await page.waitForTimeout(200);
  ok(!(await page.locator('#mnCard .mn-code').allTextContents()).includes('TEST-1'), 'custom mnemonic deleted');

  console.log('grade: safety and order checks');
  const grade = async (txt) => page.evaluate(t => { const r = gradeStationTranscript(cur.st, t, null); return {pct: r.pct, raw: r.rawPct, crit: r.chk.filter(x => !x.ok && x.c).map(x => x.t), bad: r.chk.filter(x => !x.ok).map(x => x.t), n: r.chk.length}; }, txt);
  const good = "I've washed my hands. Hello my name is Nana I'm a fourth year medical student, could you confirm your name and date of birth and I'll check your wristband. Any allergies to latex or plasters? Any arm to avoid like a fistula? I need to take some blood, is that okay? Tourniquet on, feeling for a bouncy vein. Cleaning with chlorhexidine for 30 seconds and letting it dry, I won't re-palpate. Sharp scratch. Filling the gold bottle then the purple bottle. Releasing the tourniquet, then removing the needle, straight into the sharps bin. Pressure with gauze. Labelling the bottles at the bedside. If it bleeds or swells let the nurse know.";
  const g1 = await grade(good);
  ok(g1.n >= 10 && g1.crit.length === 0, 'good venepuncture: no critical misses (' + g1.pct + '%, missed: ' + g1.bad.join('; ') + ')');
  const badOrder = good.replace('Releasing the tourniquet, then removing the needle', 'Removing the needle, then releasing the tourniquet');
  const g2 = await grade(badOrder);
  ok(g2.crit.some(x => /Tourniquet off before/.test(x)) && g2.pct <= 54, 'needle out first: critical, capped (' + g2.pct + '% from ' + g2.raw + '%)');
  const g3 = await grade(good + ' I will resheath the needle.');
  ok(g3.crit.some(x => /Sharps/.test(x)), 'resheathing flagged');
  const g4 = await grade(good.replace("I won't re-palpate", 'no allergies so tourniquet on'));
  ok(!g4.bad.some(x => /Tourniquet on/.test(x)), 'presence checks are not fooled by a nearby "no" (unpunctuated dictation)');

  const vague = await page.evaluate(() => gradeStationTranscript(getStation('E-abdo'), 'Hello my name is Nana. Today I have been asked to examine your abdomen. This involves having a look, feel and listen to your abdomen. Do you have any questions?', null).rawPct);
  ok(vague < 30, 'a vague opening does not earn domain marks (' + vague + '%)');
  console.log('grade drawer UI');
  await page.evaluate(() => setMode('grade'));
  await page.waitForTimeout(300);
  await page.fill('#ttTranscriptInput', badOrder + ' the tourney kit');
  await page.click('[data-ttmark]');
  await page.waitForTimeout(400);
  ok(await page.locator('.tt-sec.chk').count() === 1, '🛡️ checks panel shows');
  ok(/capped at 54%/.test(await page.locator('.tt-sec.chk').textContent()), 'cap explained in the panel');
  ok(/Safety/.test(await page.locator('.tt-kc .change').textContent()), '"One thing to change" leads with the safety step');
  const fixBtn = page.locator('[data-ttfix]');
  if (await fixBtn.count()) { await fixBtn.click(); await page.waitForTimeout(150); ok(/tourniquet\s*$/i.test((await page.inputValue('#ttTranscriptInput')).trim()), 'fix button swaps "tourney kit" for "tourniquet"'); }
  else ok(false, 'fix button appears after a rescue');
  const bridge = page.locator('#gradeDrawer a[href*="#hq-u"]');
  ok(await bridge.count() === 1, 'STUDY SBA bridge link: ' + (await bridge.count() ? await bridge.getAttribute('href') : 'none'));

  console.log('scoped voice fixes');
  const sc = await page.evaluate(() => ({
    abdoThorough: normalizeTalkType('I will do a thorough examination', getStation('E-abdo')).norm,
    thyThorough: normalizeTalkType('I will do a thorough examination', getStation('E-thyroid') || ST.find(s => (s.ex || []).includes('thyroid'))).norm,
    deflated: normalizeTalkType('I feel deflated', ST[0]).norm,
  }));
  ok(!/thyroid/.test(sc.abdoThorough), '"thorough examination" is left alone in an abdominal station');
  ok(/thyroid/.test(sc.thyThorough), '"thorough examination" becomes thyroid in a thyroid station');
  ok(/deflated/.test(sc.deflated), '"deflated" is no longer turned into "lethargic"');

  console.log('offline examiner honesty');
  const ex = await page.evaluate(async () => { cur.chat = [{role: 'user', content: 'hello my name is nana', t: 5}]; const r = await window.medengineOfflineRespond([{role: 'user', content: 'mark me'}], {_json: true}); return JSON.parse(r.text); });
  ok(Array.isArray(ex.non_negotiables) && ex.non_negotiables.length === 0, 'no invented non-negotiables');
  ok(Array.isArray(ex.timeline) && ex.timeline.length === 0, 'no invented timeline');
  ok(ex.reasoning_sentence && ex.reasoning_sentence.said === false, 'reasoning sentence only ticked when said');

  console.log('voice hint');
  await page.evaluate(() => setMode('voice'));
  await page.waitForTimeout(300);
  ok(/2\.5 s/.test(await page.locator('#vWaitHint').textContent()), 'voice card says it waits 2.5 s');

  if (PACK) {
  console.log('my circuit vault');
  await page.goto(BASE + '/osce.html#my');
  await page.waitForTimeout(400);
  ok(/Import your private pack/.test(await page.locator('#main').textContent()), 'empty vault invites an import');
  await page.setInputFiles('#myFile', PACK);
  await page.waitForTimeout(400);
  ok(/6 stations/.test(await page.locator('#main').textContent()), 'pack read: 6 stations');
  await page.fill('#myP1', 'short');
  await page.fill('#myP2', 'short');
  await page.click('[data-myseal]');
  await page.waitForTimeout(300);
  ok(/at least 8/.test(await page.locator('#main').textContent()), 'short password refused');
  await page.fill('#myP1', 'correct horse battery');
  await page.fill('#myP2', 'correct horse battery');
  await page.click('[data-myseal]');
  await page.waitForFunction(() => /Encrypted and unlocked/.test(document.querySelector('#main').textContent), null, {timeout: 20000});
  ok(await page.locator('#main .li').count() === 6, 'unlocked list shows 6 stations');
  const store = await page.evaluate(() => { const all = {}; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); all[k] = localStorage.getItem(k); } return all; });
  const sealed = JSON.parse(store['medengine-private-v1']);
  ok(sealed.kind === 'medengine-sealed' && sealed.iter === 600000 && sealed.ct.length > 1000, 'sealed blob stored (PBKDF2 600k, AES-GCM)');
  const leak = Object.values(store).some(v => PK.stations.some(s => v.includes(s.vars[0].who) || v.includes(s.secs[0].items[0].say)));
  ok(!leak, 'no station text in plain localStorage');
  await page.locator('#main .li').first().click();
  await page.waitForTimeout(600);
  ok((await page.locator('#main').textContent()).includes(PK.stations[0].t), 'MY1 opens as a station');
  ok(await page.locator('#nav button[data-v="my"].on').count() === 1, 'nav highlights 🔒 My circuit on a private station');
  const myCodes = await page.locator('#mnCard .mn-code').allTextContents();
  ok(myCodes.includes(PK.stations[0].mn[0].code), 'private station shows its own mnemonics (' + myCodes.slice(0, 4).join(', ') + ')');
  const g5 = await page.evaluate(() => { const r = gradeStationTranscript(cur.st, 'hello name and date of birth. any pain? lie flat on one pillow. I will examine', null); return {pct: r.pct, crit: r.chk.filter(x => !x.ok && x.c).map(x => x.t)}; });
  ok(g5.crit.length >= 1 && g5.pct <= 54, 'private station uses its own checks (' + g5.crit.join('; ') + ')');
  await page.goto(BASE + '/osce.html#my');
  await page.waitForTimeout(300);
  await page.click('[data-mylock]');
  await page.waitForTimeout(300);
  ok(await page.evaluate(() => !getStation('MY1')), 'lock removes the stations from memory');
  await page.reload();
  await page.waitForTimeout(500);
  ok(await page.evaluate(() => !getStation('MY1')), 'after reload the stations are locked');
  await page.fill('#myPw', 'wrong password');
  await page.click('[data-myopen]');
  await page.waitForFunction(() => /Wrong password|Unlocking/.test(document.querySelector('#main').textContent), null, {timeout: 20000});
  await page.waitForFunction(() => !/Unlocking/.test(document.querySelector('#main').textContent), null, {timeout: 20000});
  ok(/Wrong password/.test(await page.locator('#main').textContent()), 'wrong password refused');
  await page.fill('#myPw', 'correct horse battery');
  await page.press('#myPw', 'Enter');
  await page.waitForFunction(() => document.querySelectorAll('#main .li').length === 6, null, {timeout: 20000});
  ok(true, 'right password (Enter key) unlocks');
  await page.goto(BASE + '/osce.html#s-' + PK.stations[3].id);
  await page.waitForTimeout(500);
  ok((await page.locator('#main').textContent()).includes(PK.stations[3].t), 'deep link to a private station works while unlocked');
  await page.evaluate(() => setMode('script'));
  await page.waitForTimeout(300);
  const scr = await page.locator('#scriptCard').textContent();
  ok(scr.includes(PK.stations[3].secs[1].items[2].say.slice(0, 40)), 'script mode shows the full verbatim lines');

  } else console.log('my circuit vault: skipped (pass the private pack path as the 2nd argument)');

  console.log('layout');
  for (const w of [390, 1280]) {
    await page.setViewportSize({ width: w, height: 860 });
    for (const h of ['#mn', '#my', '#s-MY1', '#p-venep']) {
      await page.goto(BASE + '/osce.html' + h);
      await page.waitForTimeout(450);
      const over = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      ok(over <= 1, w + 'px ' + h + ' no sideways scroll (' + over + ')');
    }
  }
  await page.setViewportSize({ width: 390, height: 860 });
  await page.goto(BASE + '/osce.html#p-venep');
  await page.waitForTimeout(500);
  await page.evaluate(() => { setMode('script'); const c = document.querySelector('#mnCard'); if (c) c.open = true; });
  await page.waitForTimeout(200);
  await page.locator('#mnCard').screenshot({ path: path.join(OUT, 'shot-mncard-390.png') });
  await page.goto(BASE + '/osce.html#mn');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, 'shot-hub-390.png') });
  await page.emulateMedia({ colorScheme: 'dark' });
  await page.goto(BASE + '/osce.html#my');
  await page.waitForTimeout(400);
  await page.screenshot({ path: path.join(OUT, 'shot-my-390-dark.png') });

  ok(errors.length === 0, 'no page errors during the run ' + errors.slice(0, 3).join(' | '));
  await browser.close();
  console.log(fails.length ? '\nFAILED: ' + fails.length : '\nALL PASSED');
  process.exit(fails.length ? 1 : 0);
})();
