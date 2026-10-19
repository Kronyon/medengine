// medengine.exe: AI proxy. The browser never sees the Anthropic key.
// Body: { input: string | [{role, content}], tier: 'quick'|'default'|'complex', json?: boolean }
// Returns: { text, truncated, tier, remaining }  (remaining = free turns left today, or null for Pro)
import { Client, Users } from 'node-appwrite';

const MODELS = {
  quick: process.env.MODEL_QUICK || 'claude-haiku-5-5',
  default: process.env.MODEL_DEFAULT || 'claude-sonnet-5-5',
  complex: process.env.MODEL_COMPLEX || 'claude-sonnet-5-5',
};
const MAX_TOKENS = { quick: 400, default: 4000, complex: 6000 };
const FREE_PER_DAY = +(process.env.FREE_AI_PER_DAY || 25);
const PRO_PER_DAY = +(process.env.PRO_AI_PER_DAY || 800);
const MAX_INPUT_CHARS = 200000;

export function toMessages(input) {
  const turns = typeof input === 'string' ? [{ role: 'user', content: input }] : Array.isArray(input) ? input : [];
  const out = [];
  for (const t of turns) {
    const role = t && t.role === 'assistant' ? 'assistant' : 'user';
    const content = String((t && t.content) || '').trim();
    if (!content) continue;
    if (out.length && out[out.length - 1].role === role) out[out.length - 1].content += '\n\n' + content;
    else out.push({ role, content });
  }
  while (out.length && out[0].role !== 'user') out.shift();
  while (out.length && out[out.length - 1].role !== 'user') out.pop();
  return out;
}

export default async ({ req, res, log, error }) => {
  const userId = req.headers['x-appwrite-user-id'];
  if (!userId) return res.json({ error: 'Sign in first', code: 'sign_in_required' }, 401);
  if (!process.env.ANTHROPIC_API_KEY) return res.json({ error: 'AI is not configured', code: 'sampling_disabled' }, 503);

  let body;
  try { body = JSON.parse(req.bodyText || req.bodyRaw || '{}'); } catch (e) { return res.json({ error: 'Bad request', code: 'invalid_request' }, 400); }
  const tier = MODELS[body.tier] ? body.tier : 'default';
  const messages = toMessages(body.input);
  if (!messages.length) return res.json({ error: 'Empty prompt', code: 'invalid_request' }, 400);
  if (JSON.stringify(messages).length > MAX_INPUT_CHARS) return res.json({ error: 'Prompt too large', code: 'prompt_too_large' }, 413);

  // Daily allowance, kept in the user's prefs (aiDay, aiCount).
  const client = new Client()
    .setEndpoint(process.env.APPWRITE_FUNCTION_API_ENDPOINT)
    .setProject(process.env.APPWRITE_FUNCTION_PROJECT_ID)
    .setKey(req.headers['x-appwrite-key'] || process.env.APPWRITE_API_KEY || '');
  const users = new Users(client);
  const user = await users.get({ userId });
  const pro = (user.labels || []).includes('pro');
  const prefs = user.prefs || {};
  const today = new Date().toISOString().slice(0, 10);
  const used = prefs.aiDay === today ? +prefs.aiCount || 0 : 0;
  const limit = pro ? PRO_PER_DAY : FREE_PER_DAY;
  if (used >= limit) return res.json({ error: pro ? 'Daily fair-use limit reached' : 'Free AI turns used up for today', code: pro ? 'rate_limited' : 'upgrade_required' }, 429);
  await users.updatePrefs({ userId, prefs: { ...prefs, aiDay: today, aiCount: used + 1 } });

  const system = 'You are the engine behind medengine.exe, a UK OSCE practice app for medical students. Follow the instructions in the user turn exactly.'
    + (body.json ? ' Reply with ONLY one valid JSON value, no prose and no code fences.' : '');
  let r;
  try {
    r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: MODELS[tier], max_tokens: MAX_TOKENS[tier], system, messages }),
    });
  } catch (e) {
    error('Anthropic request failed: ' + e.message);
    return res.json({ error: 'The AI service could not be reached', code: 'upstream_error' }, 502);
  }
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    error('Anthropic ' + r.status + ': ' + JSON.stringify(data).slice(0, 500));
    return res.json({ error: 'The AI service returned an error', code: r.status === 429 ? 'rate_limited' : 'upstream_error' }, r.status === 429 ? 429 : 502);
  }
  const text = (data.content || []).filter((c) => c.type === 'text').map((c) => c.text).join('');
  if (!text.trim()) return res.json({ error: 'Empty answer', code: 'empty_completion' }, 502);
  log(`ai ${tier} user=${userId} in=${data.usage?.input_tokens} out=${data.usage?.output_tokens}`);
  return res.json({ text, truncated: data.stop_reason === 'max_tokens', tier, remaining: pro ? null : Math.max(0, limit - used - 1) });
};
