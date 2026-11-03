// v3.3.3: 🎯 Accurate dictate records, sends to Whisper with the station's words, fills and marks
const { chromium } = require('playwright');
const BASE = process.argv[2] || 'http://127.0.0.1:8765';
const fails = []; const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails.push(m); };
(async () => {
  const b = await chromium.launch({ args: ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream'] });
  const ctx = await b.newContext({ permissions: ['microphone'] }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const sent = [];
  await ctx.route('https://api.groq.com/**', async route => {
    const r = route.request(); const body = r.postDataBuffer() ? r.postDataBuffer().toString('latin1') : '';
    sent.push({ auth: r.headers()['authorization'], model: (body.match(/name="model"\r\n\r\n([^\r]*)/) || [])[1], prompt: (body.match(/name="prompt"\r\n\r\n([^\r]*)/) || [])[1] || '', file: /filename="station\.(webm|m4a|ogg)"/.test(body) });
    route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ text: "Hello, I'm Nana. Could you confirm your name and date of birth? I'm going to percuss the liver and check for shifting dullness." }) });
  });
  await p.addInitScript(() => { try { localStorage.setItem('medengine-anthropic-key', 'gsk_test_key'); } catch (e) {} });
  await p.goto(BASE + '/osce.html#e-abdo'); await p.waitForTimeout(800);
  await p.evaluate(() => setMode('grade')); await p.waitForTimeout(300);
  ok(await p.locator('[data-ttwhisper]').count() === 1, '🎯 Accurate dictate button shows with a Groq key');
  await p.click('[data-ttwhisper]'); await p.waitForTimeout(2200);
  ok(/Stop/.test(await p.textContent('[data-ttwhisper]')), 'recording with a running timer');
  await p.click('[data-ttwhisper]'); await p.waitForTimeout(2000);
  ok(sent.length === 1 && sent[0].auth === 'Bearer gsk_test_key' && sent[0].model === 'whisper-large-v3-turbo' && sent[0].file, 'audio sent to Groq Whisper with your key');
  ok(/percuss/.test(sent[0] && sent[0].prompt) && /hernial/i.test(sent[0] && sent[0].prompt), 'vocabulary hint includes OSCE and station words');
  ok(/percuss the liver/.test(await p.inputValue('#ttTranscriptInput')), 'transcript dropped into the box');
  ok(await p.evaluate(() => !!ttGradeState.result), 'and marked');
  await p.evaluate(() => localStorage.removeItem('medengine-anthropic-key'));
  await p.click('[data-ttwhisper]'); await p.waitForTimeout(400);
  ok(sent.length === 1, 'no key: nothing is sent');
  ok(errs.length === 0, 'no page errors ' + errs.slice(0, 2).join(' | '));
  await b.close(); console.log(fails.length ? 'FAILED ' + fails.length : 'ALL PASSED'); process.exit(fails.length ? 1 : 0);
})();
