// medengine.exe: open the Stripe customer portal (cancel, change card, invoices). Returns { url }.
import { Client, Users } from 'node-appwrite';
import Stripe from 'stripe';

export default async ({ req, res, error }) => {
  const userId = req.headers['x-appwrite-user-id'];
  if (!userId) return res.json({ error: 'Sign in first', code: 'sign_in_required' }, 401);
  const { STRIPE_SECRET_KEY, SITE_URL } = process.env;
  if (!STRIPE_SECRET_KEY || !SITE_URL) return res.json({ error: 'Payments are not configured yet' }, 503);
  const users = new Users(new Client()
    .setEndpoint(process.env.APPWRITE_FUNCTION_API_ENDPOINT)
    .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
    .setKey(req.headers['x-appwrite-key'] || process.env.APPWRITE_API_KEY || ''));
  try {
    const prefs = await users.getPrefs({ userId });
    if (!prefs.stripeCustomerId) return res.json({ error: 'No billing account yet' }, 404);
    const s = await new Stripe(STRIPE_SECRET_KEY).billingPortal.sessions.create({ customer: prefs.stripeCustomerId, return_url: SITE_URL });
    return res.json({ url: s.url });
  } catch (e) {
    error('portal: ' + e.message);
    return res.json({ error: 'Could not open billing' }, 500);
  }
};
