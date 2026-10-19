// medengine.exe: Stripe webhook. Grants or removes the `pro` label.
// Point a Stripe webhook endpoint at this function's domain with these events:
//   checkout.session.completed, customer.subscription.updated, customer.subscription.deleted
import { Client, Users } from 'node-appwrite';
import Stripe from 'stripe';

const ACTIVE = new Set(['active', 'trialing', 'past_due']);

export async function setPro(users, userId, on, extra = {}) {
  const user = await users.get({ userId });
  const labels = new Set(user.labels || []);
  if (on) labels.add('pro'); else labels.delete('pro');
  await users.updateLabels({ userId, labels: [...labels] });
  if (Object.keys(extra).length) await users.updatePrefs({ userId, prefs: { ...(user.prefs || {}), ...extra } });
}

export default async ({ req, res, log, error }) => {
  const { STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET } = process.env;
  if (!STRIPE_SECRET_KEY || !STRIPE_WEBHOOK_SECRET) return res.json({ error: 'not configured' }, 503);
  const stripe = new Stripe(STRIPE_SECRET_KEY);
  let event;
  try {
    event = stripe.webhooks.constructEvent(req.bodyText ?? req.bodyRaw ?? '', req.headers['stripe-signature'], STRIPE_WEBHOOK_SECRET);
  } catch (e) {
    error('bad signature: ' + e.message);
    return res.json({ error: 'invalid signature' }, 400);
  }
  const users = new Users(new Client()
    .setEndpoint(process.env.APPWRITE_FUNCTION_API_ENDPOINT)
    .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
    .setKey(req.headers['x-appwrite-key'] || process.env.APPWRITE_API_KEY || ''));
  try {
    const o = event.data.object;
    if (event.type === 'checkout.session.completed' && o.client_reference_id) {
      await setPro(users, o.client_reference_id, true, { stripeCustomerId: o.customer, stripeSubscriptionId: o.subscription });
      log('pro on ' + o.client_reference_id);
    } else if (event.type === 'customer.subscription.updated' || event.type === 'customer.subscription.deleted') {
      const userId = o.metadata && o.metadata.userId;
      if (userId) {
        const on = event.type === 'customer.subscription.updated' && ACTIVE.has(o.status);
        await setPro(users, userId, on, { stripeSubscriptionId: o.id, stripeStatus: o.status });
        log(`pro ${on ? 'on' : 'off'} ${userId} (${o.status})`);
      }
    }
  } catch (e) {
    error('webhook handling failed: ' + e.message);
    return res.json({ error: 'handler failed' }, 500); // Stripe will retry
  }
  return res.json({ received: true });
};
