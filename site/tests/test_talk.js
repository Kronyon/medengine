// v3.3.1: TalkType → 📋 Grade (link catcher, waiting transcript, paste & mark)
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://127.0.0.1:8765', PACK = process.argv[3];
const fails = []; const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails.push(m); };
const TXT = "Hello my name is Nana, could you confirm your name and date of birth and wristband. Any allergies? Tourniquet on, cleaning with chlorhexidine for 30 seconds and letting it dry. Sharp scratch. Gold bottle. Releasing the tourniquet then removing the needle into the sharps bin. Labelling at the bedside.";
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
  const p = await ctx.newPage(); const errs = []; p.on('pageerror', e => errs.push(e.message));
  const graded = () => p.evaluate(() => !!(ttGradeState.result && document.querySelector('.tt-banner')) && document.querySelector('#ttTranscriptInput').value.length);

  console.log('link opens your last station and marks it');
  await p.goto(BASE + '/osce.html#p-venep'); await p.waitForTimeout(600);
  await p.goto('about:blank');
  await p.goto(BASE + '/osce.html#talk=' + encodeURIComponent(TXT)); await p.waitForTimeout(1500);
  ok(/#s-P-venep$/.test(p.url()), 'routed to the last station: ' + p.url().split('#')[1]);
  ok(await graded() > 100, 'transcript filled and marked in 📋 Grade');
  ok(!/talk=/.test(p.url()), 'the transcript is removed from the address bar');

  console.log('no last station: waits for the next one you open');
  await p.evaluate(() => { localStorage.removeItem('medengine-last-station'); });
  await p.goto('about:blank');
  await p.goto(BASE + '/osce.html#talk=' + encodeURIComponent(TXT)); await p.waitForTimeout(900);
  ok(await p.evaluate(() => route.v === 'home'), 'lands on home');
  await p.goto(BASE + '/osce.html#p-venep'); await p.waitForTimeout(1200);
  ok(await graded() > 100, 'marked when the station opens');

  console.log('link arriving while the page is open');
  await p.evaluate(t => { location.hash = 'talk=' + encodeURIComponent(t + ' extra words'); }, TXT); await p.waitForTimeout(1500);
  ok(/extra words/.test(await p.inputValue('#ttTranscriptInput')), 'new transcript replaces the old one');

  console.log('📋 Paste & mark');
  await p.evaluate(t => navigator.clipboard.writeText(t + ' pasted'), TXT);
  await p.click('[data-ttpaste]'); await p.waitForTimeout(800);
  ok(/pasted/.test(await p.inputValue('#ttTranscriptInput')) && await graded() > 100, 'clipboard pasted and marked');

  if (PACK) {
    console.log('private station: waits for unlock');
    await p.goto(BASE + '/osce.html#my'); await p.waitForTimeout(400);
    await p.setInputFiles('#myFile', PACK); await p.waitForTimeout(300);
    await p.fill('#myP1', 'correct horse battery'); await p.fill('#myP2', 'correct horse battery');
    await p.click('[data-myseal]'); await p.waitForFunction(() => document.querySelectorAll('#main .li').length > 3, null, {timeout: 20000});
    const id = await p.evaluate(() => MY.pack.stations[3].id);
    await p.goto(BASE + '/osce.html#s-' + id); await p.waitForTimeout(700);
    await p.goto('about:blank');
    await p.goto(BASE + '/osce.html#talk=' + encodeURIComponent(TXT)); await p.waitForTimeout(900);
    ok(/#my$/.test(p.url()), 'locked: sent to 🔒 My circuit');
    await p.fill('#myPw', 'correct horse battery'); await p.press('#myPw', 'Enter');
    await p.waitForFunction(() => document.querySelectorAll('#main .li').length > 3, null, {timeout: 20000});
    await p.locator('#main .li').nth(3).click(); await p.waitForTimeout(1300);
    ok(await graded() > 100, 'unlocked station picks up the waiting transcript');
  }
  ok(errs.length === 0, 'no page errors ' + errs.slice(0, 2).join(' | '));
  await b.close(); console.log(fails.length ? 'FAILED ' + fails.length : 'ALL PASSED'); process.exit(fails.length ? 1 : 0);
})();
