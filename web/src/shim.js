// medengine.exe website shim.
// Inside claude.ai the app talks to `window.claude` (AI, user, db). On the public
// website there is no claude.ai runtime, so this file provides the same interface
// backed by Appwrite: accounts (Account), AI (the `ai` Appwrite Function, which
// calls the Anthropic API server-side), and Stripe billing (`checkout`, `portal`).
import { Client, Account, Functions, ID } from 'appwrite';

const CFG = window.MEDENGINE_CONFIG || {};
const client = new Client().setEndpoint(CFG.endpoint).setProject(CFG.projectId);
const account = new Account(client);
const functions = new Functions(client);

let me = null;
let quota = null; // free AI turns left today (null = unknown / unlimited)
const isPro = () => !!(me && (me.labels || []).includes('pro'));

async function refreshMe() {
  try { me = await account.get(); } catch (e) { me = null; }
  renderAcct();
  return me;
}

async function exec(functionId, payload) {
  const ex = await functions.createExecution({ functionId, body: JSON.stringify(payload), async: false });
  let body = {};
  try { body = JSON.parse(ex.responseBody || '{}'); } catch (e) { body = {}; }
  if (ex.status === 'failed' || ex.responseStatusCode >= 400 || body.error) {
    throw { code: body.code || 'upstream_error', message: body.error || 'The server could not answer' };
  }
  return body;
}

function parseJsonLoose(text) {
  const t = String(text || '').trim();
  try { return JSON.parse(t); } catch (e) {}
  const fence = t.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fence) { try { return JSON.parse(fence[1]); } catch (e) {} }
  const a = Math.min(...['{', '['].map(c => { const i = t.indexOf(c); return i < 0 ? Infinity : i; }));
  const b = Math.max(t.lastIndexOf('}'), t.lastIndexOf(']'));
  if (a !== Infinity && b > a) { try { return JSON.parse(t.slice(a, b + 1)); } catch (e) {} }
  return undefined;
}

// Same contract as claude.ai's sample(): resolves {text, truncated}; rejects {code, message}.
function sample(input, opts = {}) {
  return (async () => {
    if (opts.signal && opts.signal.aborted) throw { code: 'cancelled', message: 'cancelled' };
    if (!me) await refreshMe();
    if (!me) throw { code: 'sign_in_required', message: 'Sign in first' };
    const call = exec('ai', { input, tier: opts.modelTier || 'default', json: !!opts._json });
    const aborted = new Promise((_, rej) => {
      if (opts.signal) opts.signal.addEventListener('abort', () => rej({ code: 'cancelled', message: 'cancelled' }), { once: true });
    });
    const r = await Promise.race([call, aborted]);
    if (typeof r.remaining === 'number') { quota = r.remaining; renderAcct(); }
    if (opts.onText && r.text) { try { opts.onText({ text: r.text, delta: r.text }); } catch (e) {} }
    return { text: r.text, truncated: !!r.truncated, modelTierApplied: r.tier || opts.modelTier || 'default' };
  })();
}
sample.json = async (input, opts = {}) => {
  const r = await sample(input, Object.assign({}, opts, { _json: true, onText: undefined }));
  const v = parseJsonLoose(r.text);
  if (v === undefined) throw { code: 'invalid_json', message: 'Could not read the reply', text: r.text };
  return v;
};
sample.limits = async () => ({ maxPromptBytes: 262144 });

const userNs = {
  id: async () => (me || (await refreshMe()) || {}).$id || null,
  isOwner: () => false,
  canEdit: () => false,
  can: () => null,
};

window.claude = {
  use: async (name) => (name === 'sample' ? sample : name === 'user' ? (me || (await refreshMe()) ? userNs : null) : null),
};

/* ---------- account panel ---------- */
const $ = (s) => document.querySelector(s);
const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
let modal = null, view = 'signin', note = '';

function renderAcct() {
  const b = $('#acctBtn');
  if (b) b.innerHTML = me ? (isPro() ? '⭐<span class="al"> Pro</span>' : '👤<span class="al"> Account</span>') : '🔑<span class="al"> Sign in</span>';
  if (modal && modal.open) drawModal();
}

function drawModal() {
  const body = modal.querySelector('.mbody');
  if (me) {
    body.innerHTML = `<h2>${esc(me.name || me.email)}</h2>
      <p class="hint">${esc(me.email)}</p>
      <p><b>Plan:</b> ${isPro() ? '⭐ Pro: unlimited AI patient, voice stations and examiner marking' : 'Free: scripts, frameworks, hooks and friend practice, plus a few AI turns a day' + (quota != null ? ` (${quota} left today)` : '')}</p>
      ${note ? `<div class="alert">${esc(note)}</div>` : ''}
      <div class="row">${isPro() ? '<button class="btn" data-acct="portal">Manage billing</button>' : '<button class="btn primary" data-acct="pro">⭐ Go Pro</button>'}
      <button class="btn" data-acct="signout">Sign out</button><button class="btn" data-acct="close">Close</button></div>`;
    return;
  }
  const f = (id, label, type, ac) => `<label class="fld">${label}<input class="sel" id="${id}" type="${type}" autocomplete="${ac}" required></label>`;
  if (view === 'reset') {
    body.innerHTML = `<h2>Reset your password</h2>${f('aEmail', 'Email', 'email', 'email')}${note ? `<div class="alert">${esc(note)}</div>` : ''}
      <div class="row"><button class="btn primary" data-acct="sendreset">Send reset link</button><button class="btn" data-acct="signin-view">Back</button></div>`;
    return;
  }
  const up = view === 'signup';
  body.innerHTML = `<h2>${up ? 'Create your account' : 'Sign in'}</h2>
    <p class="hint">${up ? 'Free to start. Upgrade to Pro for unlimited AI and voice stations.' : 'Sign in to use the AI patient, voice stations and examiner marking.'}</p>
    ${up ? f('aName', 'Name', 'text', 'name') : ''}${f('aEmail', 'Email', 'email', 'email')}${f('aPass', 'Password (8+ characters)', 'password', up ? 'new-password' : 'current-password')}
    ${note ? `<div class="alert">${esc(note)}</div>` : ''}
    <div class="row"><button class="btn primary" data-acct="${up ? 'signup' : 'signin'}">${up ? 'Create account' : 'Sign in'}</button>
    <button class="btn" data-acct="${up ? 'signin-view' : 'signup-view'}">${up ? 'I have an account' : 'Create an account'}</button>
    ${up ? '' : '<button class="btn sm" data-acct="reset-view">Forgot password?</button>'}<button class="btn sm" data-acct="close">Close</button></div>`;
}

function openModal(reason) {
  if (!modal) {
    modal = document.createElement('dialog');
    modal.className = 'acct';
    modal.innerHTML = '<div class="mbody"></div>';
    document.body.appendChild(modal);
    modal.addEventListener('click', onClick);
  }
  note = reason === 'upgrade_required' ? "You've used today's free AI turns. Go Pro for unlimited stations." : reason === 'sign_in_required' ? 'Sign in to use the AI patient and examiner.' : '';
  view = 'signin';
  drawModal();
  if (!modal.open) modal.showModal();
}

async function onClick(e) {
  const b = e.target.closest('[data-acct]');
  if (!b) return;
  const a = b.dataset.acct, v = (id) => (($('#' + id) || {}).value || '').trim();
  b.disabled = true;
  try {
    if (a === 'close') { modal.close(); return; }
    if (a === 'signin-view' || a === 'signup-view' || a === 'reset-view') { view = a.replace('-view', ''); note = ''; return drawModal(); }
    if (a === 'signin') {
      await account.createEmailPasswordSession({ email: v('aEmail'), password: v('aPass') });
      note = ''; await refreshMe();
    } else if (a === 'signup') {
      await account.create({ userId: ID.unique(), email: v('aEmail'), password: v('aPass'), name: v('aName') || undefined });
      await account.createEmailPasswordSession({ email: v('aEmail'), password: v('aPass') });
      note = 'Welcome to medengine-OSCE.'; await refreshMe();
    } else if (a === 'sendreset') {
      await account.createRecovery({ email: v('aEmail'), url: location.origin + '/reset.html' });
      note = 'If that email has an account, a reset link is on its way.'; drawModal();
    } else if (a === 'signout') {
      await account.deleteSession({ sessionId: 'current' }); me = null; quota = null; note = ''; renderAcct();
    } else if (a === 'pro') {
      const r = await exec('checkout', {});
      if (r.url) location.href = r.url;
    } else if (a === 'portal') {
      const r = await exec('portal', {});
      if (r.url) location.href = r.url;
    }
  } catch (err) {
    note = (err && (err.message || err.code)) || 'Something went wrong. Try again.';
    drawModal();
  } finally {
    b.disabled = false;
  }
}

window.medengineAccount = { open: openModal, refresh: refreshMe };

function mountButton() {
  const bar = document.querySelector('header.top .bar');
  if (!bar || $('#acctBtn')) return;
  const btn = document.createElement('button');
  btn.className = 'btn sm';
  btn.id = 'acctBtn';
  btn.type = 'button';
  btn.setAttribute('aria-label', 'Account');
  btn.innerHTML = '🔑<span class="al"> Sign in</span>';
  btn.addEventListener('click', () => openModal());
  bar.appendChild(btn);
}

function boot() {
  mountButton();
  refreshMe().then(() => {
    const q = new URLSearchParams(location.search);
    if (q.get('pro') === 'success') {
      openModal();
      note = 'Thanks! Your Pro upgrade is being activated; this can take a few seconds.';
      drawModal();
      let n = 0;
      const t = setInterval(async () => { await refreshMe(); if (isPro() || ++n > 10) { clearInterval(t); if (isPro()) { note = '⭐ Pro is active. Enjoy unlimited stations.'; drawModal(); } } }, 3000);
      history.replaceState(null, '', location.pathname + location.hash);
    }
  });
}
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
