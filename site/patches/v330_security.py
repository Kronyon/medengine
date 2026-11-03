#!/usr/bin/env python3
"""v3.3.0 security patch for site/study.html (applied once; kept as a record).

Replaces Antigravity's v3.2.0 cloud layer:
  - open Supabase tables (anyone could read, edit and delete every row)  -> per-user RLS schema
  - plaintext password + PIN registry in localStorage                     -> removed; Supabase Auth only
  - full progress copy in the public profile row                          -> private backup table
  - unescaped avatar / stats from the network                             -> cleaned and escaped
  - 9 full localStorage snapshots (quota bomb, silent save failures)      -> IndexedDB snapshots
Usage: python3 site/patches/v330_security.py <snippet dir>
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SNIP = pathlib.Path(sys.argv[1])
F = ROOT / 'site' / 'study.html'
t = F.read_text(encoding='utf-8')


def region(t, start, end, new, keep_end=True):
    i = t.index(start)
    if t.count(start) != 1:
        raise SystemExit(f'start marker not unique: {start[:60]!r}')
    j = t.index(end, i + len(start))
    return t[:i] + new + t[j:] if keep_end else t[:i] + new + t[j + len(end):]


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:70]!r}, found {n}')
    return t.replace(old, new)


snip = lambda n: (SNIP / n).read_text(encoding='utf-8')

# 1. secure SQL
sql = snip('sql.txt').rstrip('\n')
t = region(t, 'const SUPABASE_SQL_SETUP = `', '`;\n\n(function injectV3Styles(){', 'const SUPABASE_SQL_SETUP = `' + sql)

# 2. cloud client + peers
t = region(t, '/* ----- ☁️ Direct Browser-to-Supabase REST Client (0 Netlify Credits, 0 SDK Bloat) ----- */',
           '/* ----- PARAMOUNT: Progress Shield (Non-Destructive Backup + Additive Merge) ----- */', snip('medcloud.js'))

# 3. shield, legacy registry wipe, sync orchestration
t = region(t, '/* ----- PARAMOUNT: Progress Shield (Non-Destructive Backup + Additive Merge) ----- */',
           '/* ----- Celebration Fireworks & Emotes on Correct Answer ----- */', snip('shield.js'))

# 4-5. account modal: auth and cloud tabs
t = region(t, "  if (_acctTab === 'auth') {", "  } else if (_acctTab === 'profile') {", snip('acct_ui.js'))
t = region(t, "  } else if (_acctTab === 'cloud') {", "  } else if (_acctTab === 'shield') {", snip('acct_cloud_tab.js'))

# 6-7. handlers
t = region(t, '  if (el.dataset.cloudTest) {', '  if (el.dataset.pingJump) {', snip('acct_handlers_cloud.js'))
t = region(t, '  if (el.dataset.authSubmit) {', '  if (el.dataset.pfSave) {', snip('acct_handlers_auth.js'))

# 8. profile save: valid handle, allowed avatar
t = one(t, "    if (nm) S.acct.name = nm;\n    if (hd) S.acct.handle = hd;\n    S.acct.ava = av;",
        "    if (nm) S.acct.name = nm.slice(0, 40);\n"
        "    if (hd) { if (!MedCloud.goodHandle(MedCloud.handle(hd))) { _acctMsg = '⚠️ Handle: 3 to 20 characters, using a to z, 0 to 9 and _.'; renderAcctModal(); return; } S.acct.handle = MedCloud.handle(hd); }\n"
        "    S.acct.ava = MedCloud.avatars.includes(av) ? av : '🩺';")
t = one(t, "_acctMsg = '✅ Profile & Celebration FX saved locally and pushed to Supabase Cloud!';",
        "_acctMsg = MedCloud.signedIn() ? '✅ Profile saved and syncing.' : '✅ Profile saved on this device.';")

# 9. friends: no copies of other people's progress
t = one(t, "          sys: cp.sys || 'cardio',\n          savedState: cp.full_state_backup_json || null\n        };",
        "          sys: cp.sys || 'cardio'\n        };")
t = one(t, "    const h = ((inp && inp.value) || '').trim().replace(/^@/, '').toLowerCase();\n    if (!h) return;",
        "    const h = MedCloud.handle((inp && inp.value) || '');\n    if (!MedCloud.goodHandle(h)) { _acctMsg = '⚠️ Enter a valid @handle.'; renderAcctModal(); return; }")

# 10. restore from IndexedDB
old_restore = """    const snap = (getShieldStore().snaps || []).find(s => s.id === id);
    if (snap && snap.state) {
      mergeAccountProgressSafely(snap.state);
      refreshChrome();
      refreshAcctBadge();
      render();
      _acctMsg = '♻️ Snapshot merged into your active progress! Zero items lost.';
      renderAcctModal();
    }
    return;"""
new_restore = """    if (!window.indexedDB) { _acctMsg = '⚠️ This browser cannot open saved snapshots.'; renderAcctModal(); return; }
    shieldGet(id).then(snap => {
      if (!snap || !snap.state) { _acctMsg = '⚠️ That snapshot is no longer available.'; renderAcctModal(); return; }
      mergeAccountProgressSafely(snap.state);
      refreshChrome(); refreshAcctBadge(); render();
      _acctMsg = '♻️ Snapshot merged into your progress. Nothing was removed.';
      renderAcctModal();
    }).catch(() => { _acctMsg = '⚠️ Could not open that snapshot.'; renderAcctModal(); });
    return;"""
t = one(t, old_restore, new_restore)
t = one(t, "a.download = 'medengine-v3.1-progress-shield-'", "a.download = 'medengine-progress-'")

# 11. escape everything from other people on the leaderboard
t = one(t, "' + topPeer.ava + ' <b>' + esc(topPeer.name)", "' + esc(topPeer.ava) + ' <b>' + esc(topPeer.name)")
t = one(t, "'<div><b>' + r.ava + ' ' + esc(r.name)", "'<div><b>' + esc(r.ava) + ' ' + esc(r.name)")
t = one(t, "+ '<p class=\"sub\" style=\"margin:0\">Compare live accuracy by <b>Organ System</b>, <b>ILO Week</b>, <b>Exam Paper</b>, or <b>Condition</b> across your cohort (0 Netlify credits).</p></div>'",
        "+ '<p class=\"sub\" style=\"margin:0\">Compare accuracy by <b>system</b>, <b>ILO week</b>, <b>paper</b> or <b>condition</b> across your cohort.' + (MedCloud.signedIn() ? '' : ' <b>Sign in (👤) to see your cohort.</b>') + '</p></div>'")

# 12. one vote per person, and you can take it back
old_like = """      S.upvotedIds = S.upvotedIds || {};
      item.likes = (item.likes || 1) + 1;
      S.upvotedIds[cid] = 1;
      save();
      el.textContent = '👍 ' + item.likes;
      el.classList.add('on');
      MedCloud.upvoteComment(cid, item.likes);"""
new_like = """      S.upvotedIds = S.upvotedIds || {};
      const on = !S.upvotedIds[cid];
      item.likes = Math.max(0, (item.likes || 0) + (on ? 1 : -1));
      if (on) S.upvotedIds[cid] = 1; else delete S.upvotedIds[cid];
      save();
      el.textContent = '👍 ' + item.likes;
      el.classList.toggle('on', on);
      MedCloud.vote(cid, on);"""
t = one(t, old_like, new_like)

# 13. no competitor branding in the interface
t = one(t, '💬 Passmedicine Discussion', '💬 Discussion')
t = t.replace('Passmedicine-style question scorecard.', 'question scorecard.')

F.write_text(t, encoding='utf-8')
print('security patch applied:', F)
