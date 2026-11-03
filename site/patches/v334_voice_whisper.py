#!/usr/bin/env python3
"""v3.3.4: 🎙 Voice stations get Whisper marking too.

With a Groq or OpenAI key, a Voice station quietly records your own turns (it pauses while the
patient or examiner is speaking, so their voice is not mixed in). ⚡ End & Mark then sends that
recording to Whisper, primed with the station's words, and marks the accurate transcript instead
of the browser's guesses. Without a key, or if anything fails, it marks the browser text as before.
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'osce.html'
t = F.read_text(encoding='utf-8')


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


if 'function whvStart(' in t:
    raise SystemExit('already applied')

JS = r"""
/* ---------- v3.3.4 🎯 Whisper for Voice stations: records your turns only ---------- */
const WHV = {rec: null, chunks: [], stream: null, mime: '', st: null};
async function whvStart(){
  whvStop(true);
  if (window.MEDENGINE_ARTIFACT || !whisperKey() || !navigator.mediaDevices || !window.MediaRecorder) return;
  try {
    const stream = await navigator.mediaDevices.getUserMedia({audio: true});
    const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4', 'audio/ogg'].find(m => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) || '';
    WHV.stream = stream; WHV.chunks = []; WHV.st = cur && cur.st;
    WHV.rec = new MediaRecorder(stream, mime ? {mimeType: mime} : undefined); WHV.mime = WHV.rec.mimeType || mime || 'audio/webm';
    WHV.rec.ondataavailable = e => { if (e.data && e.data.size) WHV.chunks.push(e.data); };
    WHV.rec.start(1000);
    if (VO && VO.speaking) whvPause();
  } catch (e) { WHV.rec = null; }
}
function whvPause(){ try { if (WHV.rec && WHV.rec.state === 'recording') WHV.rec.pause(); } catch (e) {} }
function whvResume(){ try { if (WHV.rec && WHV.rec.state === 'paused') WHV.rec.resume(); } catch (e) {} }
function whvStop(discard){
  const r = WHV.rec;
  return new Promise(res => {
    if (!r || r.state === 'inactive') { if (WHV.stream) WHV.stream.getTracks().forEach(x => x.stop()); WHV.stream = null; if (discard) WHV.chunks = []; return res(); }
    r.onstop = () => { if (WHV.stream) WHV.stream.getTracks().forEach(x => x.stop()); WHV.stream = null; if (discard) WHV.chunks = []; res(); };
    try { r.stop(); } catch (e) { res(); }
  });
}
async function whvEndGrade(){
  const key = whisperKey();
  if (!key || !WHV.rec) return pipeChatToGrade();
  const st = (cur && cur.st) || WHV.st;
  await whvStop(false); WHV.rec = null;
  const blob = new Blob(WHV.chunks, {type: WHV.mime.split(';')[0]}); WHV.chunks = [];
  if (blob.size < 2000) return pipeChatToGrade();
  toast('🎯 Whisper is transcribing your station…');
  const btn = $('[data-vendgrade]'); if (btn) { btn.disabled = true; btn.textContent = '⏳ Transcribing…'; }
  const ext = /mp4/.test(WHV.mime) ? 'm4a' : /ogg/.test(WHV.mime) ? 'ogg' : 'webm';
  const url = key.p === 'groq' ? 'https://api.groq.com/openai/v1/audio/transcriptions' : 'https://api.openai.com/v1/audio/transcriptions';
  let text = '';
  for (const model of (key.p === 'groq' ? ['whisper-large-v3-turbo', 'whisper-large-v3'] : ['whisper-1'])) {
    const fd = new FormData();
    fd.append('file', blob, 'station.' + ext); fd.append('model', model); fd.append('language', 'en'); fd.append('temperature', '0'); fd.append('prompt', whisperVocab(st)); fd.append('response_format', 'json');
    try { const r = await fetch(url, {method: 'POST', headers: {Authorization: 'Bearer ' + key.k}, body: fd}); const d = await r.json().catch(() => ({})); if (r.ok && typeof d.text === 'string') { text = d.text.trim(); break; } if (r.status === 401) break; } catch (e) {}
  }
  if (btn) { btn.disabled = false; btn.textContent = '⚡ End & Mark in 📋 Grade'; }
  if (!text) { toast('🎯 Whisper failed: marking the browser transcript instead'); return pipeChatToGrade(); }
  stopTimer(); if (VO) vShutdown();
  const v = curVar();
  ttGradeState = {stId: st.id, raw: text, mode: v && v.k ? String(v.k) : 'normal', result: null, retryMode: false, open: true};
  ttGradeState.result = gradeStationTranscript(st, text, null);
  awardOsceBounty(10);
  setMode('grade'); redrawSniperStationWrap();
  const ta = $('#ttTranscriptInput'); if (ta) ta.value = text;
  const gd = $('#gradeDrawer'); if (gd) { gd.open = true; gd.scrollIntoView({behavior: 'smooth', block: 'start'}); }
  toast('🎯 Marked from the Whisper transcript');
}
"""
anchor = "document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ttwhisper]'); if (b) whisperToggle(); });"
t = one(t, anchor, anchor + '\n' + JS)

# start with the live station; pause while the patient or examiner talks; stop on shutdown
t = one(t, "  clearInterval(VO.rT); VO.phase = 'live'; VO.on = true; drawVoiceCtl();\n",
        "  clearInterval(VO.rT); VO.phase = 'live'; VO.on = true; drawVoiceCtl(); whvStart();\n")
t = one(t, "  VO.pending++; VO.speaking = true; vStopRec();", "  VO.pending++; VO.speaking = true; whvPause(); vStopRec();")
t = one(t, "if (!VO.pending) { VO.speaking = false; if (!VO.busy && VO.on) setTimeout(vListen, 120); } };",
        "if (!VO.pending) { VO.speaking = false; whvResume(); if (!VO.busy && VO.on) setTimeout(vListen, 120); } };")
t = one(t, "VO.pending = 0; VO.qEnd = 0; VO.speaking = false; VO.barge++;", "VO.pending = 0; VO.qEnd = 0; VO.speaking = false; whvResume(); VO.barge++;")
t = one(t, "  if (d.vendgrade != null) return pipeChatToGrade();", "  if (d.vendgrade != null) return whvEndGrade();")

# say so on the Voice card
t = one(t, "the examiner gives the findings. Beeps at 5:00 and 9:00;",
        "the examiner gives the findings. ' + (!window.MEDENGINE_ARTIFACT && whisperKey() ? '<b>🎯 Your key is on, so ⚡ End &amp; Mark re-transcribes your words with Whisper for accurate marking.</b> ' : '') + 'Beeps at 5:00 and 9:00;")

t = one(t, "function vShutdown(){ if (!VO) return; VO.on = false;", "function vShutdown(){ if (!VO) return; if (WHV.rec && VO.on) whvStop(true); VO.on = false;")
F.write_text(t, encoding='utf-8')
print('v3.3.4 Voice Whisper applied')
