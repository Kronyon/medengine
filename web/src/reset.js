// Password reset page: Appwrite sends users here with ?userId=&secret=
import { Client, Account } from 'appwrite';
const CFG = window.MEDENGINE_CONFIG || {};
const account = new Account(new Client().setEndpoint(CFG.endpoint).setProject(CFG.projectId));
const q = new URLSearchParams(location.search), msg = document.getElementById('msg');
document.getElementById('go').addEventListener('click', async () => {
  const p1 = document.getElementById('p1').value, p2 = document.getElementById('p2').value;
  if (p1.length < 8) { msg.textContent = 'Use at least 8 characters.'; return; }
  if (p1 !== p2) { msg.textContent = 'The passwords do not match.'; return; }
  try {
    await account.updateRecovery({ userId: q.get('userId'), secret: q.get('secret'), password: p1 });
    msg.textContent = 'Password updated. You can sign in now.';
    setTimeout(() => { location.href = '/'; }, 1500);
  } catch (e) { msg.textContent = (e && e.message) || 'That link has expired. Request a new one.'; }
});
