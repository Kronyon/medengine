# medengine-OSCE · v0.5.0 beta

Part of the **medengine.exe** family (medengine-OSCE and medengine-STUDY).

OSCE practice for UK medical students: a script for every station (what to say and why), one framework per station type with what changes, the non-negotiables, every hook, and an AI patient and examiner you can type to or talk to, with detailed marking.

## What's in this repo

```
offline/          Downloadable app: no sign-in, runs from a folder (python3 offline/build.py)
  src/            launcher, offline AI layer (your own Anthropic key), read-me
  img/            STUDY page images
study/            medengine-STUDY page source
app/              The app itself: content (stations, frameworks), source, build pipeline
  content/        Stations (pp*.txt), frameworks (fw*.txt), money lines, frame why-lines
  src/            Page head (CSS + layout) and script, base data (ILO units, packs, bank)
  build/          build_v3.py (data) · build_app_v3.py (page) · test_v4.py (browser tests)
  dist/app.html   The built single-file app (also what runs inside claude.ai)
web/              The public website (Appwrite Sites, static)
  src/shim.js     Replaces claude.ai's runtime: Appwrite accounts, AI via the `ai` function, billing
  public/         Legal page drafts, password reset page, icon, site CSS
  build.mjs       Injects config + shim into the app → web/dist
functions/        Appwrite Functions (Node 22)
  ai/             Anthropic API proxy with free and Pro daily allowances
  checkout/       Starts a Stripe Checkout subscription
  portal/         Opens the Stripe customer portal
  stripe-webhook/ Grants or removes the `pro` user label from Stripe events
  test/run.mjs    Local tests with Appwrite, Anthropic and Stripe faked
appwrite.json     Project, functions and site definitions for the Appwrite CLI
```

## Build and test

```bash
npm run build:app        # needs Python 3; regenerates app/dist/app.html from content/
npm --prefix web ci && npm run build:web
npm run test:functions   # node, no network needed
npm run test:web         # Playwright + Chromium
npm run test:app         # Playwright + Chromium, full app suite
```

## Download and run (no sign-in)

```bash
npm run build:app && npm run build:offline   # → offline/dist/medengine.html (one file) + medengine-website.zip
npm run test:offline                          # file:// tests with the Anthropic API faked
```

- **`medengine.html`**: one file with both apps and every page image inside. Double-click it, tap OSCE or STUDY (or press 1 / 2). The apps' own buttons jump straight between them.
- **`medengine-website.zip`**: the same apps as a small static site (`index.html` = launcher). iPhone and iPad won't run scripts in a downloaded file, so drop this folder on any static host (Netlify Drop, Appwrite Sites, GitHub Pages) and open the link in Safari; Share → Add to Home Screen makes it an app icon.
 Everything works offline except the AI patient, voice stations and examiner marking, which call the Anthropic API directly with your own key (🔑 AI key in OSCE; stored only in that browser).

## Deploy (Appwrite Cloud + Stripe)

1. **Appwrite project.** Create a project on Appwrite Cloud (note the region endpoint, e.g. `https://fra.cloud.appwrite.io/v1`, and the project ID). In `appwrite.json` set `projectId` to it. Under Auth, keep Email/Password on.
2. **Push functions and site.** `npm i -g appwrite-cli`, `appwrite login`, then `appwrite push functions` and `appwrite push sites`. If the CLI rejects a field (the CLI schema changes between versions), create them in the Console with the same settings: Node 22 runtime, entrypoint `src/main.js`, build command `npm install --omit=dev`, execute access `users` (and `any` for `stripe-webhook`), scopes `users.read` and `users.write`, timeout 120 s for `ai`.
   Site: root directory `.` (repo root), install `npm ci --prefix web`, build `npm run build --prefix web`, output `./web/dist`.
3. **Connect GitHub** (Console → Sites → web → Git) so every push to `main` redeploys.
4. **Environment variables.** Use `.env.example` as the list. Website build: `APPWRITE_ENDPOINT`, `APPWRITE_PROJECT_ID`. Functions: `ANTHROPIC_API_KEY`, the Stripe keys, `SITE_URL`.
5. **Stripe (test mode first).** Create a Product "medengine-OSCE Pro" with a recurring GBP price → `STRIPE_PRICE_ID`. Add a webhook endpoint pointing at the `stripe-webhook` function's domain with events `checkout.session.completed`, `customer.subscription.updated`, `customer.subscription.deleted` → `STRIPE_WEBHOOK_SECRET`. Turn on the customer portal (Settings → Billing → Customer portal).
6. **Allow your site's domain** as a Web platform in the Appwrite project (Overview → Add platform → Web) so the browser SDK can call it.
7. **Test end to end** with Stripe's test card `4242 4242 4242 4242`: sign up → AI works for the free allowance → Go Pro → `pro` label appears on the user → unlimited AI → Manage billing → cancel → label removed.

## How access works

- **Free:** scripts, frameworks, hooks, friend practice and self-marking, plus `FREE_AI_PER_DAY` AI turns a day.
- **Pro:** the AI patient, voice stations and examiner marking, up to the fair-use cap `PRO_AI_PER_DAY`.
- Pro is the Appwrite user label `pro`. Only the Stripe webhook sets or removes it; the `ai` function checks it on every call.
- Progress is stored in each user's browser (localStorage) in this beta.

## Notes

- Voice uses the browser's own speech recognition and speech synthesis (best in Chrome, Edge, Safari). No audio leaves the device; only the text transcript goes to the AI.
- On the website, AI replies arrive whole rather than streamed, so they're a little slower than inside claude.ai.
- Educational use only; not medical advice. Clinical content follows UK guidance as written in 2026; check current NICE and BNF.
