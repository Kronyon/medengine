// v3.3.4: a Voice station records your turns and ⚡ End & Mark grades the Whisper transcript
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const fails = []; const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails.push(m); };
(async () => {
  const b = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'] });
  const ctx = await b.newContext({ permissions: ['microphone'] }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  let audio = 0;
  await ctx.route('https://api.groq.com/**', async route => {
    const u = route.request().url();
    if (/audio\/transcriptions/.test(u)) { audio++; return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ text: 'Hello I am Nana, could you confirm your name and date of birth? Is that OK? Would you like a chaperone? I will now palpate and percuss.' }) }); }
    if (/models/.test(u)) return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ data: [{ id: 'openai/gpt-oss-120b' }] }) });
    return route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ choices: [{ message: { content: '[Examiner] Carry on.' } }] }) });
  });
  await p.addInitScript(() => { try { localStorage.setItem('medengine-anthropic-key', 'gsk_test_key'); } catch (e) {} });
  await p.goto(BASE + '/osce.html#e-abdo'); await p.waitForTimeout(900);
  await p.evaluate(() => { S.set.vRead = false; setMode('voice'); });
  await p.waitForTimeout(300);
  ok(/Whisper/.test(await p.textContent('#voiceCard')), 'Voice card says Whisper marking is on');
  await p.evaluate(() => vStart()); await p.waitForTimeout(2500);
  ok(await p.evaluate(() => !!WHV.rec && WHV.rec.state === 'recording'), 'recording your turns once the station starts');
  await p.evaluate(() => { whvPause(); }); await p.waitForTimeout(200);
  ok(await p.evaluate(() => WHV.rec.state === 'paused'), 'pauses while the patient or examiner speaks');
  await p.evaluate(() => { whvResume(); cur.chat.push({role: 'user', content: 'hello puppet date to beth', t: 5}); }); await p.waitForTimeout(1500);
  await p.evaluate(() => whvEndGrade()); await p.waitForTimeout(2500);
  ok(audio === 1, 'audio sent to Whisper once');
  const box = await p.inputValue('#ttTranscriptInput').catch(() => '');
  ok(/chaperone/.test(box) && !/puppet/.test(box), 'marked from the Whisper text, not the browser guess');
  ok(await p.evaluate(() => !!ttGradeState.result && /chaperone/.test(ttGradeState.raw)), 'graded from the Whisper transcript');
  ok(await p.evaluate(() => !WHV.stream), 'microphone released');
  ok(errs.length === 0, 'no page errors ' + errs.slice(0, 2).join(' | '));
  await b.close(); console.log(fails.length ? 'FAILED ' + fails.length : 'ALL PASSED'); process.exit(fails.length ? 1 : 0);
})();
