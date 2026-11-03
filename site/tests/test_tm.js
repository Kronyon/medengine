const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 860 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/study.html#hq-u4'); await p.waitForTimeout(2500);
  // find an answer option button inside the question
  const opt = p.locator('#main [data-hqpick], #main [data-pick], #main .hq-opt, #main button.opt').first();
  console.log('option buttons:', await p.locator('#main [data-hqpick]').count());
  await opt.click(); await p.waitForTimeout(300); await p.locator('#main [data-hqpick]').first().click(); await p.waitForTimeout(600);
  const cfm = p.locator('#main [data-hqcommit], #main [data-hqcfm]').first();
  if (await cfm.count()) { await cfm.click(); await p.waitForTimeout(500); }
  console.log('thought map:', await p.locator('#main .tm').count(), '| flips:', await p.locator('#main .tm-f').count(), '| why-not rows:', await p.locator('#main .tm-xr').count());
  const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  console.log('overflow at 390:', over);
  if (await p.locator('#main .tm').count()) await p.locator('#main .tm').first().screenshot({ path: require('os').tmpdir() + '/shot-tm-390.png' });
  console.log('errors', errs.slice(0, 3));
  await b.close();
})();
