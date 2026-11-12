import sys, json, subprocess, urllib.request, numpy as np, soundfile as sf
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from story import LINES, FEMALE
import story as _story
SIGNOFF = getattr(_story, 'SIGNOFF', 'File closed. For now.')
HAS_SIGN = len(LINES) > 1 and LINES[-1][0].strip() == SIGNOFF  # v3: calm low sign-off after the twist
# Narration: ElevenLabs when the ELEVENLABS_API_KEY secret is available (real human-sounding voices),
# otherwise the free local Kokoro voices. Voices can be changed in voices.json.
CFG = {'narrator': 'nPczCjzI2devNBz1zQrb', 'female': 'EXAVITQu4vr4xnSDxMaL', 'model': 'eleven_multilingual_v2'}
try: CFG.update(json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'voices.json'))))
except Exception: pass
KEY = os.environ.get('ELEVENLABS_API_KEY', '').strip()
sr_out = 24000

def eleven(text, female, prev_text, next_text):
    vid = CFG['female'] if female else CFG['narrator']
    calm = text.strip() == SIGNOFF
    body = {'text': text, 'model_id': CFG['model'], 'previous_text': prev_text, 'next_text': next_text,
            'voice_settings': ({'stability': 0.30, 'similarity_boost': 0.75, 'style': 0.55, 'use_speaker_boost': True} if female else
                               {'stability': 0.75 if calm else 0.38, 'similarity_boost': 0.80, 'style': 0.10 if calm else 0.45, 'use_speaker_boost': True})}
    req = urllib.request.Request(f'https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128',
                                 data=json.dumps(body).encode(), headers={'xi-api-key': KEY, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    mp3 = urllib.request.urlopen(req, timeout=60).read()
    pcm = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', '-', '-f', 'f32le', '-ac', '1', '-ar', str(sr_out), '-'],
                         input=mp3, capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.float32).copy()
    # trim leading/trailing silence so pauses stay as written in story.py
    nz = np.where(np.abs(a) > 0.01)[0]
    if len(nz): a = a[max(0, nz[0]-240):nz[-1]+1200]
    return a

def kokoro_lines():
    from kokoro_onnx import Kokoro
    k = Kokoro('models/kokoro-v1.0.onnx', 'models/voices-v1.0.bin')
    VAR = [1.0, 1.04, 0.97, 1.03]; N = len(LINES); out = []
    for i, (text, scene, pause) in enumerate(LINES):
        voice = 'af_nicole' if text in FEMALE else 'am_fenrir'
        sp = (0.94 if i >= N-2 else VAR[i % 4]) if voice == 'am_fenrir' else 0.85
        if HAS_SIGN and i == N-1: sp = 0.85
        a, sr = k.create(text, voice=voice, speed=sp, lang='en-us'); out.append(a.astype(np.float32))
    return out

clips = None; engine = 'kokoro'
if KEY:
    try:
        clips = []
        for i, (text, scene, pause) in enumerate(LINES):
            prev_t = ' '.join(l[0] for l in LINES[max(0, i-2):i]); next_t = LINES[i+1][0] if i+1 < len(LINES) else ''
            clips.append(eleven(text, text in FEMALE, prev_t, next_t))
        engine = 'elevenlabs'
    except Exception as e:
        print('ElevenLabs failed, falling back to Kokoro:', e); clips = None
if clips is None: clips = kokoro_lines()
print('voice engine:', engine)
open('engine.txt', 'w').write(engine)

# Faster, tighter delivery (Hamza, 10 Nov 2026: 81% swiped away, so pace matters):
# speed every clip up (pitch-preserving), start talking almost at once, cap the pauses.
TEMPO = float(CFG.get('tempo', 1.12))
def speed(a, f):
    if abs(f-1.0) < 0.01: return a
    out = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr_out), '-ac', '1', '-i', '-',
                          '-filter:a', f'atempo={f}', '-f', 'f32le', '-ac', '1', '-ar', str(sr_out), '-'],
                         input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(out, dtype=np.float32).copy()
N = len(LINES)
clips = [a if (HAS_SIGN and i == N-1) else speed(a, 1.04 if LINES[i][0] in FEMALE else TEMPO) for i, a in enumerate(clips)]
if HAS_SIGN:  # sign-off: no speed-up, pitch lowered ~8% (low, calm voice)
    a = clips[-1]
    clips[-1] = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 'f32le', '-ar', str(sr_out), '-ac', '1', '-i', '-',
        '-filter:a', f'asetrate={int(sr_out*0.92)},aresample={sr_out},atempo=1.04', '-f', 'f32le', '-ac', '1', '-ar', str(sr_out), '-'],
        input=a.astype(np.float32).tobytes(), capture_output=True, check=True).stdout, dtype=np.float32).copy()
TW = N-2 if HAS_SIGN else N-1  # the twist line
def cap(i, p): return min(p, 0.6) if i == TW-1 else (min(p, 0.4) if HAS_SIGN and i == TW else min(p, 0.3))
parts = []; times = []; speech = []; t = 0.0
lead = np.zeros(int(0.05*sr_out), dtype=np.float32); parts.append(lead); t += 0.05
for i, ((text, scene, pause), a) in enumerate(zip(LINES, clips)):
    pause = cap(i, pause)
    start = t; parts.append(a); t += len(a)/sr_out
    speech.append([start, t])
    parts.append(np.zeros(int(pause*sr_out), dtype=np.float32)); t += pause
    times.append([start, t])
audio = np.concatenate(parts); audio = audio/np.max(np.abs(audio))*0.9
sf.write('voice.wav', audio, sr_out)
json.dump(times, open('times.json','w'))
json.dump(speech, open('speech.json','w'))  # when each line's words are actually spoken (for word captions)
try:
    import sfx
    if HAS_SIGN: sfx.build(LINES[:-1], times[:-1], speech[:-1], t)  # twist sting on the last story line, not the sign-off
    else: sfx.build(LINES, times, speech, t)  # sound effects + music bed -> sfx.wav
except Exception as e:
    print('sfx failed:', e)
print(t)
