#!/usr/bin/env python3
"""v3.3.3: 🎯 Accurate dictation in 📋 Grade, using Whisper through your own AI key.

The browser's built-in speech recognition guesses medical words ("date to Beth", "puppet",
"sifting bonus"). With a Groq (gsk_…) or OpenAI (sk-…) key, 🎯 Accurate dictate records your
station and sends the audio to Whisper with a vocabulary hint: the clinical words of the
station you are on, plus common OSCE words. The text drops into the box and is marked.
Website copy only (the claude.ai version has no key). Audio goes to the provider of your key.
"""
import pathlib

F = pathlib.Path(__file__).resolve().parents[1] / 'osce.html'
t = F.read_text(encoding='utf-8')


def one(t, old, new):
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'expected 1 of {old[:80]!r}, found {n}')
    return t.replace(old, new)


if 'function whisperVocab(' in t:
    raise SystemExit('already applied')

JS = r"""
/* ---------- v3.3.3 🎯 Accurate dictation: Whisper through your own key ---------- */
const WH = {rec: null, chunks: [], on: false, busy: false, sec: 0, tmr: null, stream: null};
const WH_BASE = 'UK medical OSCE. Hello, I am Nana, a fourth-year medical student. Could you confirm your name and date of birth? Is that OK? Would you like a chaperone? Palpate, palpation, percuss, percussion, auscultate, shifting dullness, guarding, rigidity, rebound tenderness, Murphy\'s sign, Rovsing\'s sign, iliac fossa, epigastric, hypochondrium, hernial orifices, bruits, tourniquet, chlorhexidine, venepuncture, sharps bin, Datix, PALS, ramipril, amlodipine, bradykinin, terbinafine, SOCRATES, ICE.';
function whisperKey(){ let k = ''; try { k = localStorage.getItem('medengine-anthropic-key') || ''; } catch (e) {} k = k.trim(); return /^gsk_/i.test(k) ? {k, p: 'groq'} : /^sk-/i.test(k) ? {k, p: 'openai'} : null; }
function whisperVocab(st){
  const words = [];
  const add = s => String(s || '').replace(/<[^>]+>/g, ' ').split(/[^A-Za-z'’-]+/).forEach(w => { if (w.length >= 6 && !words.includes(w.toLowerCase()) && !ANCHOR_COMMON.has(w.toLowerCase())) words.push(w.toLowerCase()); });
  if (st) { add(st.t); (buildChecklist(st, (cur && cur.vk) || null) || []).forEach(sc => sc.items.forEach(it => add(it.t))); }
  return (WH_BASE + ' ' + words.slice(0, 40).join(', ')).slice(0, 560);  // Whisper reads at most 224 tokens of prompt
}
function whisperPaint(){
  const b = $('[data-ttwhisper]'); if (!b) return;
  b.classList.toggle('on', WH.on);
  b.textContent = WH.busy ? '⏳ Transcribing…' : WH.on ? '⏹ Stop (' + mmss(WH.sec) + ')' : '🎯 Accurate dictate';
  b.disabled = WH.busy;
}
async function whisperToggle(){
  if (WH.busy) return;
  if (WH.on) { WH.on = false; clearInterval(WH.tmr); try { WH.rec.stop(); } catch (e) {} return whisperPaint(); }
  const key = whisperKey(); if (!key) return toast('🎯 needs a Groq (gsk_…) or OpenAI (sk-…) key: tap 🔑');
  if (!navigator.mediaDevices || !window.MediaRecorder) return toast('This browser cannot record audio here');
  if (typeof ttDictState !== 'undefined' && ttDictState.on) stopTtDictate();
  let stream; try { stream = await navigator.mediaDevices.getUserMedia({audio: true}); } catch (e) { return toast('🎙️ Microphone blocked: allow it in the browser settings'); }
  const mime = ['audio/webm;codecs=opus', 'audio/webm', 'audio/mp4', 'audio/ogg'].find(m => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(m)) || '';
  const st = cur && cur.st;
  WH.stream = stream; WH.chunks = []; WH.sec = 0; WH.on = true;
  WH.rec = new MediaRecorder(stream, mime ? {mimeType: mime} : undefined);
  WH.rec.ondataavailable = e => { if (e.data && e.data.size) WH.chunks.push(e.data); };
  WH.rec.onstop = () => { stream.getTracks().forEach(tr => tr.stop()); whisperSend(st, key, WH.rec.mimeType || mime || 'audio/webm'); };
  WH.rec.start(1000);
  WH.tmr = setInterval(() => { WH.sec++; whisperPaint(); if (WH.sec >= 900) whisperToggle(); }, 1000);
  whisperPaint(); toast('🎯 Recording: talk through the station, then tap ⏹ Stop');
}
async function whisperSend(st, key, mime){
  const blob = new Blob(WH.chunks, {type: mime.split(';')[0]});
  if (!blob.size) return toast('No audio was recorded');
  WH.busy = true; whisperPaint();
  const ext = /mp4/.test(mime) ? 'm4a' : /ogg/.test(mime) ? 'ogg' : 'webm';
  const url = key.p === 'groq' ? 'https://api.groq.com/openai/v1/audio/transcriptions' : 'https://api.openai.com/v1/audio/transcriptions';
  const models = key.p === 'groq' ? ['whisper-large-v3-turbo', 'whisper-large-v3'] : ['whisper-1'];
  let text = '', err = '';
  for (const model of models) {
    const fd = new FormData();
    fd.append('file', blob, 'station.' + ext); fd.append('model', model); fd.append('language', 'en'); fd.append('temperature', '0');
    fd.append('prompt', whisperVocab(st)); fd.append('response_format', 'json');
    try {
      const r = await fetch(url, {method: 'POST', headers: {Authorization: 'Bearer ' + key.k}, body: fd});
      const d = await r.json().catch(() => ({}));
      if (r.ok && d && typeof d.text === 'string') { text = d.text.trim(); break; }
      err = (d && d.error && d.error.message) || ('error ' + r.status);
      if (r.status === 401) break;
    } catch (e) { err = 'could not reach the transcription service'; }
  }
  WH.busy = false; whisperPaint();
  if (!text) return toast('🎯 Transcription failed: ' + String(err).slice(0, 90));
  const ta = $('#ttTranscriptInput'); if (!ta) return;
  ta.value = (ta.value.trim() ? ta.value.trim() + ' ' : '') + text; ttGradeState.raw = ta.value;
  const mk = $('[data-ttmark]'); if (mk) mk.click();
  toast('🎯 Transcribed with Whisper and marked');
}
document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ttwhisper]'); if (b) whisperToggle(); });
"""

anchor = "document.addEventListener('click', e => { const b = e.target.closest && e.target.closest('[data-ttpaste]'); if (b) talkPaste(); });"
t = one(t, anchor, anchor + '\n' + JS)

paste_btn = "  if (!window.MEDENGINE_ARTIFACT) h += '<button type=\"button\" class=\"btn sm\" data-ttpaste title=\"Paste what TalkType copied and mark it\">📋 Paste &amp; mark</button>';\n"
t = one(t, paste_btn, paste_btn + "  if (!window.MEDENGINE_ARTIFACT) h += '<button type=\"button\" class=\"btn sm' + (WH.on ? ' on' : '') + '\" data-ttwhisper title=\"Records you, then Whisper transcribes with this station\\'s medical words (uses your Groq or OpenAI key)\"' + (WH.busy ? ' disabled' : '') + '>' + (WH.busy ? '⏳ Transcribing…' : WH.on ? '⏹ Stop (' + mmss(WH.sec) + ')' : '🎯 Accurate dictate') + '</button>';\n")

F.write_text(t, encoding='utf-8')
print('v3.3.3 Whisper dictation applied')
