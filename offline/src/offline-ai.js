// medengine offline AI layer.
// The downloaded app has no claude.ai and no server, so the AI patient, voice stations and
// examiner marking call the Anthropic API directly with the user's own API key.
// The key is stored only in this browser (localStorage) and is sent only to api.anthropic.com.
(function () {
  'use strict';
  var KEY = 'medengine-anthropic-key', MODELS_KEY = 'medengine-models';
  var DEFAULT_MODELS = { quick: 'claude-haiku-5-5', smart: 'claude-sonnet-5-5' };
  var MAX_TOKENS = { quick: 600, default: 4000, complex: 8000 };
  var SYSTEM = 'You are the engine behind medengine-OSCE, a UK OSCE practice app for medical students. Follow the instructions in the user turn exactly.';

  function get(k) { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } }
  function set(k, v) { try { if (v) localStorage.setItem(k, v); else localStorage.removeItem(k); } catch (e) {} }
  function models() { var m = {}; try { m = JSON.parse(get(MODELS_KEY) || '{}'); } catch (e) {} return { quick: m.quick || DEFAULT_MODELS.quick, smart: m.smart || DEFAULT_MODELS.smart }; }
  function modelFor(tier) { var m = models(); return tier === 'quick' ? m.quick : m.smart; }

  function toMessages(input) {
    var turns = typeof input === 'string' ? [{ role: 'user', content: input }] : Array.isArray(input) ? input : [];
    var out = [];
    turns.forEach(function (t) {
      var role = t && t.role === 'assistant' ? 'assistant' : 'user';
      var content = String((t && t.content) || '').trim();
      if (!content) return;
      if (out.length && out[out.length - 1].role === role) out[out.length - 1].content += '\n\n' + content;
      else out.push({ role: role, content: content });
    });
    while (out.length && out[0].role !== 'user') out.shift();
    while (out.length && out[out.length - 1].role !== 'user') out.pop();
    return out;
  }

  function parseJsonLoose(text) {
    var t = String(text || '').trim();
    try { return JSON.parse(t); } catch (e) {}
    var fence = t.match(/```(?:json)?\s*([\s\S]*?)```/i);
    if (fence) { try { return JSON.parse(fence[1]); } catch (e) {} }
    var a = Math.min.apply(null, ['{', '['].map(function (c) { var i = t.indexOf(c); return i < 0 ? Infinity : i; }));
    var b = Math.max(t.lastIndexOf('}'), t.lastIndexOf(']'));
    if (a !== Infinity && b > a) { try { return JSON.parse(t.slice(a, b + 1)); } catch (e) {} }
    return undefined;
  }

  var IMG_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'], IMG_MAX = 5 * 1024 * 1024;
  async function b64(blob) {
    var buf = new Uint8Array(await blob.arrayBuffer()), s = '';
    for (var i = 0; i < buf.length; i += 0x8000) s += String.fromCharCode.apply(null, buf.subarray(i, i + 0x8000));
    return btoa(s);
  }

  async function sample(input, opts) {
    opts = opts || {};
    var key = get(KEY);
    if (!key) throw { code: 'sign_in_required', message: 'Add your AI key first' };
    var messages = toMessages(input);
    if (!messages.length) throw { code: 'invalid_request', message: 'Empty prompt' };
    // images (a question's ECG or X-ray) go with the last user turn, as the API's image blocks
    var imgs = !opts.images ? [] : (typeof Blob !== 'undefined' && opts.images instanceof Blob) ? [opts.images] : Array.prototype.slice.call(opts.images);
    if (imgs.length) {
      if (imgs.length > 5) throw { code: 'image_rejected', message: 'Too many images' };
      var blocks = [];
      for (var ii = 0; ii < imgs.length; ii++) {
        var im = imgs[ii];
        if (IMG_TYPES.indexOf(im.type) < 0 || im.size > IMG_MAX) throw { code: 'image_rejected', message: 'Use a JPEG, PNG, GIF or WebP image under 5 MB' };
        blocks.push({ type: 'image', source: { type: 'base64', media_type: im.type, data: await b64(im) } });
      }
      var last = messages[messages.length - 1];
      blocks.push({ type: 'text', text: last.content });
      last.content = blocks;
    }
    var tier = MAX_TOKENS[opts.modelTier] ? opts.modelTier : 'default';
    var stream = typeof opts.onText === 'function';
    // Newer models think by default and thinking counts toward max_tokens, so a small budget can end
    // with no text at all ("Empty answer"). Quick replies switch thinking off; the rest get room to think.
    var noThink = tier === 'quick';
    var maxTok = Math.max(MAX_TOKENS[tier], +opts.maxTokens || 0);
    var res, retried = false;
    for (;;) {
    try {
      res = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        signal: opts.signal,
        headers: {
          'content-type': 'application/json',
          'x-api-key': key,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify(Object.assign({
          model: modelFor(tier),
          max_tokens: maxTok,
          system: SYSTEM + (opts._json ? ' Reply with ONLY one valid JSON value, no prose and no code fences.' : ''),
          messages: messages,
          stream: stream
        }, noThink ? { thinking: { type: 'disabled' } } : {}))
      });
    } catch (e) {
      if (e && e.name === 'AbortError') throw { code: 'cancelled', message: 'cancelled' };
      throw { code: 'upstream_error', message: 'No internet connection, so the AI cannot answer. Everything else still works offline.' };
    }
    if (!res.ok) {
      var body = {};
      try { body = await res.json(); } catch (e) {}
      var msg = (body.error && body.error.message) || ('HTTP ' + res.status);
      // a custom model that does not take the thinking switch: ask once more without it
      if (res.status === 400 && noThink && !retried && /thinking/i.test(msg)) { noThink = false; retried = true; maxTok = Math.max(maxTok, 4000); continue; }
      if (res.status === 401 || res.status === 403) { msg = 'That key was rejected (' + msg + '). Check it and paste it again.'; openKey(msg); throw { code: 'upstream_error', message: msg }; }
      if (res.status === 429) throw { code: 'rate_limited', message: msg };
      if (res.status === 404 || /model/i.test(msg)) { msg = 'The model name was not recognised (' + msg + '). Update the model names under "Models".'; openKey(msg); throw { code: 'upstream_error', message: msg }; }
      if (/credit|billing|balance/i.test(msg)) { msg = 'Your Anthropic account needs credit: ' + msg; openKey(msg); throw { code: 'upstream_error', message: msg }; }
      throw { code: 'upstream_error', message: msg };
    }
    break;
    }
    var text = '', stop = null;
    if (!stream) {
      var data = await res.json();
      text = (data.content || []).filter(function (c) { return c.type === 'text'; }).map(function (c) { return c.text; }).join('');
      stop = data.stop_reason;
    } else {
      var reader = res.body.getReader(), dec = new TextDecoder(), buf = '';
      try {
        for (;;) {
          var r = await reader.read();
          if (r.done) break;
          buf += dec.decode(r.value, { stream: true });
          var lines = buf.split('\n'); buf = lines.pop();
          for (var i = 0; i < lines.length; i++) {
            var line = lines[i];
            if (line.indexOf('data:') !== 0) continue;
            var ev; try { ev = JSON.parse(line.slice(5)); } catch (e) { continue; }
            if (ev.type === 'content_block_delta' && ev.delta && ev.delta.type === 'text_delta') {
              text += ev.delta.text;
              try { opts.onText({ text: text, delta: ev.delta.text }); } catch (e) {}
            } else if (ev.type === 'message_delta' && ev.delta) {
              stop = ev.delta.stop_reason || stop;
            } else if (ev.type === 'error') {
              throw { code: 'upstream_error', message: (ev.error && ev.error.message) || 'Stream error' };
            }
          }
        }
      } catch (e) {
        if (e && e.name === 'AbortError') throw { code: 'cancelled', message: 'cancelled' };
        throw e && e.code ? e : { code: 'upstream_error', message: 'The connection dropped mid-answer' };
      }
    }
    if (!text.trim()) throw { code: 'empty_completion', message: stop === 'max_tokens' ? 'The AI ran out of room before answering. Try again.' : 'The AI sent back an empty answer. Try again.' };
    return { text: text, truncated: stop === 'max_tokens', modelTierApplied: tier };
  }
  sample.json = async function (input, opts) {
    var r = await sample(input, Object.assign({}, opts || {}, { _json: true, onText: undefined }));
    var v = parseJsonLoose(r.text);
    if (v === undefined) throw { code: 'invalid_json', message: 'Could not read the reply', text: r.text };
    return v;
  };
  sample.limits = async function () { return { maxPromptBytes: 262144, images: { maxCount: 5, maxInputBytes: IMG_MAX, mediaTypes: IMG_TYPES.slice() } }; };

  window.claude = { use: async function (name) { return name === 'sample' ? sample : null; } };

  /* ---------- key panel ---------- */
  var dlg = null;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function mask(k) { return k ? k.slice(0, 10) + '…' + k.slice(-4) : ''; }

  function draw(note) {
    var k = get(KEY), m = models();
    dlg.innerHTML =
      '<form method="dialog" class="okey">' +
      '<h2>🔑 AI key</h2>' +
      '<p class="hint">The AI patient, voice stations and examiner marking need an <b>Anthropic API key</b>. Everything else (scripts, frameworks, hooks, friend practice, self-marking) works with no key and no internet.</p>' +
      (k ? '<p>Saved key: <code>' + esc(mask(k)) + '</code></p>' : '') +
      '<label class="fld">' + (k ? 'Replace key' : 'Paste your key') + '<input class="sel" id="okKey" type="password" autocomplete="off" spellcheck="false" placeholder="sk-ant-..."></label>' +
      '<details><summary>Models</summary>' +
      '<label class="fld">Fast model (patient replies)<input class="sel" id="okQuick" value="' + esc(m.quick) + '"></label>' +
      '<label class="fld">Smart model (marking and feedback)<input class="sel" id="okSmart" value="' + esc(m.smart) + '"></label></details>' +
      (note ? '<div class="alert">' + esc(note) + '</div>' : '') +
      '<p class="hint small">Get a key at console.anthropic.com → API keys (pay as you go, billed by Anthropic). The key stays in this browser on this device and is only ever sent to api.anthropic.com. Do not use this on a shared computer.</p>' +
      '<div class="row">' +
      '<button class="btn primary" value="save" id="okSave">Save</button>' +
      (k ? '<button class="btn" value="test" id="okTest">Test</button><button class="btn" value="remove" id="okRemove">Remove key</button>' : '') +
      '<button class="btn" value="close" id="okClose">Close</button></div></form>';
    dlg.querySelector('#okSave').onclick = function (e) {
      e.preventDefault();
      var v = dlg.querySelector('#okKey').value.trim();
      if (v) set(KEY, v);
      var q = dlg.querySelector('#okQuick').value.trim(), s = dlg.querySelector('#okSmart').value.trim();
      set(MODELS_KEY, JSON.stringify({ quick: q && q !== DEFAULT_MODELS.quick ? q : undefined, smart: s && s !== DEFAULT_MODELS.smart ? s : undefined }));
      paintBtn();
      if (!get(KEY)) return draw('Paste a key first.');
      draw('Saved. Press Test to check it.');
    };
    var t = dlg.querySelector('#okTest');
    if (t) t.onclick = async function (e) {
      e.preventDefault(); t.disabled = true; t.textContent = 'Testing…';
      try { await sample('Reply with the single word: ready', { modelTier: 'quick' }); draw('✅ Key works. The AI patient and examiner are ready.'); }
      catch (err) { if (dlg.open) draw('Test failed: ' + ((err && err.message) || 'unknown error')); }
    };
    var rm = dlg.querySelector('#okRemove');
    if (rm) rm.onclick = function (e) { e.preventDefault(); set(KEY, ''); paintBtn(); draw('Key removed from this browser.'); };
    dlg.querySelector('#okClose').onclick = function (e) { e.preventDefault(); dlg.close(); };
  }

  function openKey(note) {
    if (!dlg) { dlg = document.createElement('dialog'); dlg.className = 'acct'; document.body.appendChild(dlg); }
    draw(note || '');
    if (!dlg.open) dlg.showModal();
  }
  window.medengineAccount = { open: function (code) { openKey(code === 'sign_in_required' ? 'Add your key to use the AI patient and examiner.' : ''); }, refresh: function () {} };

  function paintBtn() { var b = document.getElementById('aiKeyBtn'); if (b) b.innerHTML = (get(KEY) ? '🟢' : '🔑') + '<span class="al"> AI key</span>'; }
  function mount() {
    var bar = document.querySelector('header.top .bar');
    if (!bar || document.getElementById('aiKeyBtn')) return;
    var b = document.createElement('button');
    b.className = 'btn sm'; b.id = 'aiKeyBtn'; b.type = 'button'; b.setAttribute('aria-label', 'AI key');
    b.addEventListener('click', function () { openKey(); });
    bar.appendChild(b); paintBtn();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
