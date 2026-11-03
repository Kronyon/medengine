// v3.3.0 STUDY security checks against a mock Supabase
const { chromium } = require('playwright');
const fails = []; const ok = (c, m) => { console.log((c ? '  ✓ ' : '  ✗ ') + m); if (!c) fails.push(m); };
(async () => {
  const b = await chromium.launch(); const ctx = await b.newContext(); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const log = []; let backupGets = 0;
  const UID = '11111111-1111-4111-8111-111111111111';
  const user = {id: UID, email: 'nana@test.uk'};
  await ctx.route(/supabase\.co\//, async route => {
    const r = route.request(), u = r.url(), auth = r.headers()['authorization'] || '';
    log.push({m: r.method(), u: u.replace(/^https:\/\/[^/]+/, ''), auth});
    const json = (s, d) => route.fulfill({status: s, contentType: 'application/json', body: JSON.stringify(d)});
    if (/grant_type=password/.test(u)) return json(200, {access_token: 'AT1', refresh_token: 'RT1', expires_in: 3600, user});
    if (/grant_type=refresh_token/.test(u)) return json(200, {access_token: 'AT2', refresh_token: 'RT2', expires_in: 3600, user});
    if (/\/auth\/v1\/user/.test(u)) return json(200, user);
    if (/med_backups/.test(u) && r.method() === 'GET') { backupGets++; if (backupGets === 1) return json(401, {message: 'JWT expired'}); return json(200, []); }
    if (/med_profiles/.test(u) && r.method() === 'GET') return json(200, [
      {id: '22222222-2222-4222-8222-222222222222', handle: 'evil_one', name: '<img src=x onerror="window.__xss=1">', avatar: '<svg onload="window.__xss=2">', overall_pct: 99, total_done: 500, sys_stats_json: {'cardio': {done: 10, right: 9}, '<b>x': {done: 1, right: 1}}},
      {id: UID, handle: 'nana_o', name: 'Nana', avatar: '🩺', overall_pct: 70, total_done: 100}]);
    return json(200, []);
  });
  await p.addInitScript(() => {
    if (!sessionStorage.getItem('seeded')) {
      sessionStorage.setItem('seeded', '1');
      localStorage.setItem('medengine-accounts-v3', JSON.stringify({nana: {handle: 'nana', pass: 'hunter2', pin: '1234'}}));
    }
  });
  await p.goto('http://127.0.0.1:8765/study.html'); await p.waitForTimeout(2500);
  const reg = await p.evaluate(() => localStorage.getItem('medengine-accounts-v3'));
  ok(reg === null, 'v3.2.0 plaintext password registry removed on load');
  ok(!(await p.evaluate(() => JSON.stringify(localStorage))).includes('hunter2'), 'no password anywhere in localStorage');
  ok(!log.some(x => /\/rest\/v1\//.test(x.u)), 'signed out: no data requests at all (' + log.length + ' requests)');
  await p.goto('http://127.0.0.1:8765/study.html#leaderboard'); await p.waitForTimeout(1200);
  ok(!log.some(x => /\/rest\/v1\//.test(x.u)), 'signed out leaderboard does not fetch other people');

  console.log('sign in');
  await p.click('#acctBtn'); await p.waitForTimeout(400);
  const tabBtn = p.locator('[data-acct-tab="auth"]'); if (await tabBtn.count()) { await tabBtn.first().click(); await p.waitForTimeout(300); }
  await p.fill('#auEmail', 'nana@test.uk'); await p.fill('#auPass', 'correct horse battery');
  await p.click('[data-auth-submit="login"]'); await p.waitForTimeout(3500);
  const rest = log.filter(x => /\/rest\/v1\//.test(x.u));
  ok(rest.length > 0, 'signed in: sync made ' + rest.length + ' data requests');
  ok(rest.every(x => /^Bearer AT[12]$/.test(x.auth)), 'every data request carries the user token, never the bare key');
  ok(log.some(x => /grant_type=refresh_token/.test(x.u)), 'a 401 triggers a token refresh');
  ok(log.filter(x => /med_backups/.test(x.u) && x.m === 'GET').length >= 2 && rest.slice(-3).every(x => x.auth === 'Bearer AT2'), 'request retried with the refreshed token');
  const store = await p.evaluate(() => JSON.stringify(localStorage));
  ok(!store.includes('correct horse battery'), 'the password is never stored');
  await p.click('[data-acct-close]').catch(() => {});
  await p.goto('http://127.0.0.1:8765/study.html#home'); await p.waitForTimeout(500);
  await p.goto('http://127.0.0.1:8765/study.html#leaderboard'); await p.waitForTimeout(2500);
  const xss = await p.evaluate(() => ({flag: window.__xss || 0, imgs: document.querySelectorAll('#main img[onerror], #main svg[onload]').length, text: document.querySelector('#main').textContent}));
  ok(xss.flag === 0 && xss.imgs === 0, 'hostile name and avatar from the network do not run (flag ' + xss.flag + ', nodes ' + xss.imgs + ')');
  ok(errs.length === 0, 'no page errors ' + errs.slice(0, 2).join(' | '));
  await b.close();
  console.log(fails.length ? 'FAILED ' + fails.length : 'ALL PASSED'); process.exit(fails.length ? 1 : 0);
})();
