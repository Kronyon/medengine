// medengine.exe: start a Stripe Checkout session for Pro. Returns { url }.
import { Client, Users } from 'node-appwrite';
import Stripe from 'stripe';

export default async ({ req, res, error }) => {
  const userId = req.headers['x-appwrite-user-id'];
  if (!userId) return res.json({ error: 'Sign in first', code: 'sign_in_required' }, 401);
  const { STRIPE_SECRET_KEY, STRIPE_PRICE_ID, SITE_URL } = process.env;
  if (!STRIPE_SECRET_KEY || !STRIPE_PRICE_ID || !SITE_URL) return res.json({ error: 'Payments are not configured yet' }, 503);
  const stripe = new Stripe(STRIPE_SECRET_KEY);
  const users = new Users(new Client()
    .setEndpoint(process.env.APPWRITE_FUNCTION_API_ENDPOINT)
    .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
    .setKey(req.headers['x-appwrite-key'] || process.env.APPWRITE_API_KEY || ''));
  try {
    const user = await users.get({ userId });
    if ((user.labels || []).includes('pro')) return res.json({ error: 'You already have Pro' }, 409);
    const prefs = user.prefs || {};
    let customer = prefs.stripeCustomerId;
    if (!customer) {
      const c = await stripe.customers.create({ email: user.email, name: user.name || undefined, metadata: { userId } });
      customer = c.id;
      await users.updatePrefs({ userId, prefs: { ...prefs, stripeCustomerId: customer } });
    }
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      customer,
      client_reference_id: userId,
      line_items: [{ price: STRIPE_PRICE_ID, quantity: 1 }],
      subscription_data: { metadata: { userId } },
      allow_promotion_codes: true,
      success_url: SITE_URL.replace(/\/$/, '') + '/?pro=success',
      cancel_url: SITE_URL.replace(/\/$/, '') + '/?pro=cancel',
    });
    return res.json({ url: session.url });
  } catch (e) {
    error('checkout: ' + e.message);
    return res.json({ error: 'Could not start checkout' }, 500);
  }
};
