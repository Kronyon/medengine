const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 390, height: 860 } });
  const D = await (async () => { await p.goto('http://127.0.0.1:8765/osce.html'); await p.waitForTimeout(500); return p.evaluate(() => ({ex: EX.map(e => 'e-' + e.id), pr: PR.map(x => 'p-' + x.id), st: ST.filter((s, i) => i % 9 === 0).map(s => 's-' + s.id)})); })();
  const hashes = ['home', 'sniper', 'triggers', 'posters', 'mn', 'my', 't-hx', 't-ex', 't-proc', 't-psych', 'fw', 'rf'].concat(D.ex, D.pr, D.st);
  let bad = 0;
  for (const h of hashes) {
    await p.goto('http://127.0.0.1:8765/osce.html#' + h); await p.waitForTimeout(250);
    const o = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    if (o > 1) { bad++; console.log('overflow', h, o); }
  }
  console.log('checked', hashes.length, 'pages at 390px;', bad, 'overflow');
  await b.close();
})();
