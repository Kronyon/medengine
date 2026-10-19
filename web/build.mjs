// Builds the public website into web/dist:
//   1. bundles src/shim.js (Appwrite SDK + account panel) into dist/shim.js
//   2. takes the single-file app (../app/dist/app.html) and injects config, the shim and site extras
//   3. copies public/ (legal pages, password reset, icon) into dist/
import { build } from 'esbuild';
import { readFileSync, writeFileSync, mkdirSync, cpSync, existsSync } from 'node:fs';

const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url)));
const cfg = {
  endpoint: process.env.APPWRITE_ENDPOINT || process.env.APPWRITE_SITE_API_ENDPOINT || 'https://cloud.appwrite.io/v1',
  projectId: process.env.APPWRITE_PROJECT_ID || process.env.APPWRITE_SITE_PROJECT_ID || 'medengine',
  version: pkg.version,
};

mkdirSync('dist', { recursive: true });
await build({ entryPoints: ['src/shim.js'], bundle: true, minify: true, format: 'iife', target: 'es2020', outfile: 'dist/shim.js' });
await build({ entryPoints: ['src/reset.js'], bundle: true, minify: true, format: 'iife', target: 'es2020', outfile: 'dist/reset.js' });
writeFileSync('dist/config.js', 'window.MEDENGINE_CONFIG = ' + JSON.stringify(cfg) + ';\n');

let html = readFileSync('../app/dist/app.html', 'utf8');

// Public build: no personal name in the scripts, no private claude.ai links.
html = html.replace(/\bNana\b/g, '[your name]');
// The claude.ai host adds the document skeleton; a plain website needs it explicitly (emoji break without the charset).
html = '<!doctype html>\n<html lang="en-GB">\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n' + html;

const head = `<meta name="description" content="medengine-OSCE: OSCE practice with scripts, frameworks, hooks, and an AI patient and examiner you can talk to.">
<link rel="icon" href="icon.svg"><link rel="stylesheet" href="site.css">`;
html = html.replace('</title>', '</title>\n' + head);

const inject = `<footer class="site-foot"><span>medengine-OSCE v${cfg.version}. For education and exam practice only; not medical advice. Always follow current UK guidance (NICE, BNF) and your medical school's teaching. Not affiliated with or endorsed by any university.</span><span><a href="terms.html">Terms</a> · <a href="privacy.html">Privacy</a></span></footer>
<script>window.MEDENGINE_PUBLIC = true; window.MEDENGINE_CONFIG = ${JSON.stringify(cfg)};</script>
<script src="shim.js"></script>
`;
const appScript = html.indexOf('<script>\nconst D = ');
if (appScript < 0) throw new Error('app script not found');
html = html.slice(0, appScript) + inject + html.slice(appScript);
writeFileSync('dist/index.html', html);
if (existsSync('public')) cpSync('public', 'dist', { recursive: true });
console.log('dist/ built for project', cfg.projectId, 'at', cfg.endpoint);
