// Local tests for the Appwrite Functions with Appwrite, Anthropic and Stripe faked.
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const req_ = (p) => createRequire(import.meta.url)(p);
const ok = (m) => console.log('  ✓ ' + m);

function fakeUsers(Users, db) {
  Users.prototype.get = async function ({ userId }) { if (!db[userId]) throw new Error('no user'); return structuredClone(db[userId]); };
  Users.prototype.getPrefs = async function ({ userId }) { return structuredClone(db[userId].prefs || {}); };
  Users.prototype.updatePrefs = async function ({ userId, prefs }) { db[userId].prefs = structuredClone(prefs); return prefs; };
  Users.prototype.updateLabels = async function ({ userId, labels }) { db[userId].labels = [...labels]; return db[userId]; };
}
const ctx = (headers, body) => {
  const out = {};
  return { out, c: { req: { headers, bodyText: typeof body === 'string' ? body : JSON.stringify(body) }, res: { json: (o, s = 200) => (out.body = o, out.status = s, out) }, log: () => {}, error: () => {} } };
};
process.env.APPWRITE_FUNCTION_API_ENDPOINT = 'https://example.invalid/v1';
process.env.APPWRITE_FUNCTION_PROJECT_ID = 'test';

// ---------- ai ----------
{
  console.log('ai');
  const { Users } = await import('../ai/node_modules/node-appwrite/dist/index.mjs');
  const db = { u1: { $id: 'u1', labels: [], prefs: {} }, u2: { $id: 'u2', labels: ['pro'], prefs: {} } };
  fakeUsers(Users, db);
  process.env.ANTHROPIC_API_KEY = 'sk-test'; process.env.FREE_AI_PER_DAY = '2';
  let sent = null;
  globalThis.fetch = async (url, o) => { sent = JSON.parse(o.body); return { ok: true, status: 200, json: async () => ({ content: [{ type: 'text', text: 'It started this morning.' }], stop_reason: 'end_turn', usage: {} }) }; };
  const { default: ai, toMessages } = await import('../ai/src/main.js');
  assert.deepEqual(toMessages([{ role: 'user', content: 'rules' }, { role: 'user', content: 'go' }, { role: 'assistant', content: 'hi' }, { role: 'user', content: 'q' }]).map((m) => m.role), ['user', 'assistant', 'user']); ok('merges consecutive turns and keeps user first and last');
  let t = ctx({}, { input: 'x' }); await ai(t.c); assert.equal(t.out.status, 401); assert.equal(t.out.body.code, 'sign_in_required'); ok('rejects signed-out callers');
  t = ctx({ 'x-appwrite-user-id': 'u1' }, { input: [{ role: 'user', content: 'hello' }], tier: 'quick' }); await ai(t.c);
  assert.equal(t.out.status, 200); assert.equal(t.out.body.text, 'It started this morning.'); assert.equal(t.out.body.remaining, 1); assert.equal(sent.model, 'claude-haiku-5-5'); ok('free user: answers on the quick model and counts the turn');
  t = ctx({ 'x-appwrite-user-id': 'u1' }, { input: 'again', json: true }); await ai(t.c); assert.match(sent.system, /ONLY one valid JSON/); ok('JSON mode instruction');
  t = ctx({ 'x-appwrite-user-id': 'u1' }, { input: 'third' }); await ai(t.c); assert.equal(t.out.status, 429); assert.equal(t.out.body.code, 'upgrade_required'); ok('free daily limit returns upgrade_required');
  t = ctx({ 'x-appwrite-user-id': 'u2' }, { input: 'mark me', tier: 'complex' }); await ai(t.c); assert.equal(t.out.status, 200); assert.equal(t.out.body.remaining, null); ok('Pro user: unlimited (fair-use) and remaining is null');
  globalThis.fetch = async () => ({ ok: false, status: 529, json: async () => ({ error: { type: 'overloaded' } }) });
  t = ctx({ 'x-appwrite-user-id': 'u2' }, { input: 'x' }); await ai(t.c); assert.equal(t.out.status, 502); ok('upstream error is reported, not crashed');
}

// ---------- stripe-webhook ----------
{
  console.log('stripe-webhook');
  const { Users } = await import('../stripe-webhook/node_modules/node-appwrite/dist/index.mjs');
  const db = { u9: { $id: 'u9', labels: ['beta'], prefs: { a: 1 } } };
  fakeUsers(Users, db);
  process.env.STRIPE_SECRET_KEY = 'sk_test_x'; process.env.STRIPE_WEBHOOK_SECRET = 'whsec_test';
  const Stripe = (await import('../stripe-webhook/node_modules/stripe/esm/stripe.esm.node.js')).default;
  const s = new Stripe('sk_test_x');
  const { default: hook } = await import('../stripe-webhook/src/main.js');
  const send = async (evt, secret = 'whsec_test') => { const payload = JSON.stringify(evt); const sig = s.webhooks.generateTestHeaderString({ payload, secret }); const t = ctx({ 'stripe-signature': sig }, payload); await hook(t.c); return t.out; };
  let o = await send({ id: 'e1', type: 'checkout.session.completed', data: { object: { client_reference_id: 'u9', customer: 'cus_1', subscription: 'sub_1' } } }, 'whsec_wrong');
  assert.equal(o.status, 400); ok('rejects a bad signature');
  o = await send({ id: 'e2', type: 'checkout.session.completed', data: { object: { client_reference_id: 'u9', customer: 'cus_1', subscription: 'sub_1' } } });
  assert.equal(o.status, 200); assert.deepEqual(db.u9.labels.sort(), ['beta', 'pro']); assert.equal(db.u9.prefs.stripeCustomerId, 'cus_1'); assert.equal(db.u9.prefs.a, 1); ok('checkout completed → pro label on, other labels and prefs kept');
  o = await send({ id: 'e3', type: 'customer.subscription.updated', data: { object: { id: 'sub_1', status: 'unpaid', metadata: { userId: 'u9' } } } });
  assert.deepEqual(db.u9.labels, ['beta']); ok('subscription unpaid → pro removed');
  o = await send({ id: 'e4', type: 'customer.subscription.updated', data: { object: { id: 'sub_1', status: 'active', metadata: { userId: 'u9' } } } });
  assert.ok(db.u9.labels.includes('pro')); ok('subscription active → pro back on');
  o = await send({ id: 'e5', type: 'customer.subscription.deleted', data: { object: { id: 'sub_1', status: 'canceled', metadata: { userId: 'u9' } } } });
  assert.ok(!db.u9.labels.includes('pro')); ok('subscription deleted → pro removed');
}

// ---------- checkout / portal guards ----------
{
  console.log('checkout and portal');
  const { default: checkout } = await import('../checkout/src/main.js');
  const { default: portal } = await import('../portal/src/main.js');
  let t = ctx({}, {}); await checkout(t.c); assert.equal(t.out.status, 401); ok('checkout needs a signed-in user');
  delete process.env.STRIPE_PRICE_ID; t = ctx({ 'x-appwrite-user-id': 'u1' }, {}); await checkout(t.c); assert.equal(t.out.status, 503); ok('checkout reports missing configuration');
  t = ctx({}, {}); await portal(t.c); assert.equal(t.out.status, 401); ok('portal needs a signed-in user');
}
console.log('all function tests passed');
