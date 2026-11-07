import sys, json, numpy as np, soundfile as sf
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from story import LINES, FEMALE
from kokoro_onnx import Kokoro
k = Kokoro('models/kokoro-v1.0.onnx', 'models/voices-v1.0.bin')
sr_out = 24000; parts = []; times = []; t = 0.0
lead = np.zeros(int(0.3*sr_out), dtype=np.float32); parts.append(lead); t += 0.3
VAR = [1.0, 1.04, 0.97, 1.03]  # small tempo changes per line so the narrator doesn't sound flat
N = len(LINES)
for i, (text, scene, pause) in enumerate(LINES):
    voice = 'af_nicole' if text in FEMALE else 'am_fenrir'
    sp = (0.94 if i >= N-2 else VAR[i % 4]) if voice == 'am_fenrir' else 0.85
    a, sr = k.create(text, voice=voice, speed=sp, lang='en-us')
    a = a.astype(np.float32)
    start = t; parts.append(a); t += len(a)/sr
    parts.append(np.zeros(int(pause*sr), dtype=np.float32)); t += pause
    times.append([start, t])
audio = np.concatenate(parts); audio = audio/np.max(np.abs(audio))*0.9
sf.write('voice.wav', audio, sr_out)
json.dump(times, open('times.json','w'))
print(t)
