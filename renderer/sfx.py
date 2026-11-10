# Procedural sound design for The 3AM Files (no external audio files needed).
# build() writes sfx.wav: tension music bed + whooshes on cuts + keyword sound effects
# + heartbeat/riser before the twist + impact sting on the last line.
import numpy as np, soundfile as sf
SR = 44100
rng = np.random.default_rng(7)

def env(n, a=0.005, r=None):
    e = np.ones(n, np.float32); na = max(1, int(a*SR)); e[:na] = np.linspace(0, 1, na)
    if r: nr = min(n, int(r*SR)); e[-nr:] *= np.linspace(1, 0, nr)
    return e
def lp(x, a):  # one-pole lowpass, a in (0,1): smaller = darker
    y = np.empty_like(x); s = 0.0
    for i in range(len(x)): s += a*(x[i]-s); y[i] = s
    return y
def lp_fast(x, k):  # moving-average lowpass
    k = max(1, int(k)); return np.convolve(x, np.ones(k)/k, mode='same').astype(np.float32)
def t_(d): return np.arange(int(d*SR))/SR

def whoosh(d=0.45):
    n = int(d*SR); x = rng.normal(0, 1, n).astype(np.float32)
    a = np.concatenate([np.linspace(0.02, 0.35, n//2), np.linspace(0.35, 0.02, n-n//2)])
    y = np.empty_like(x); s = 0.0
    for i in range(n): s += a[i]*(x[i]-s); y[i] = s
    e = np.sin(np.linspace(0, np.pi, n))**2
    return y*e*0.9
def thump(f=60, d=0.25, decay=18, click=0.3):
    t = t_(d); y = np.sin(2*np.pi*f*t*(1-0.3*t/d))*np.exp(-decay*t)
    y[:int(0.01*SR)] += rng.normal(0, click, int(0.01*SR))*np.linspace(1, 0, int(0.01*SR))
    return y.astype(np.float32)
def knock():
    out = np.zeros(int(0.9*SR), np.float32)
    for k in range(3):
        s = thump(170, 0.18, 30, 0.6) + 0.5*thump(95, 0.18, 22, 0)
        i = int(k*0.26*SR); out[i:i+len(s)] += s
    return out*0.9
def heartbeat(n_beats=4, bpm=90):
    gap = 60/bpm; out = np.zeros(int((n_beats*gap+0.4)*SR), np.float32)
    for k in range(n_beats):
        for off, amp in ((0, 1.0), (0.18, 0.7)):
            s = lp(thump(48, 0.22, 16, 0), 0.08)*amp*3; i = int((k*gap+off)*SR); out[i:i+len(s)] += s
    return out
def ring(d=1.6):
    t = t_(d); y = (np.sin(2*np.pi*440*t)+np.sin(2*np.pi*480*t))*0.5
    gate = (np.sin(2*np.pi*20*t) > 0).astype(np.float32); cyc = ((t % 0.8) < 0.55).astype(np.float32)
    return (y*gate*cyc*env(len(t), 0.01, 0.05)*0.35).astype(np.float32)
def creak(d=0.9):
    t = t_(d); f = 70+60*np.sin(2*np.pi*0.9*t)+25*np.sin(2*np.pi*3.1*t)
    ph = 2*np.pi*np.cumsum(f)/SR; y = ((ph/(2*np.pi)) % 1.0)*2-1
    y = lp_fast(y, 6)*(0.6+0.4*np.sin(2*np.pi*11*t))
    return (y*env(len(t), 0.05, 0.2)*0.35).astype(np.float32)
def steps(n=4):
    out = np.zeros(int((n*0.5+0.3)*SR), np.float32)
    for k in range(n):
        s = lp(thump(80, 0.15, 25, 0.5), 0.2)*1.5; i = int(k*0.5*SR); out[i:i+len(s)] += s
    return out
def static(d=0.6):
    x = rng.normal(0, 1, int(d*SR)).astype(np.float32)
    g = (rng.random(len(x)) > 0.3).astype(np.float32)
    return x*g*env(len(x), 0.01, 0.1)*0.12
def riser(d=2.0):
    t = t_(d); f = 200*(2**(2.5*t/d)); ph = 2*np.pi*np.cumsum(f)/SR
    y = 0.25*np.sin(ph)+0.25*np.sin(ph*1.5)+lp_fast(rng.normal(0, 0.5, len(t)), 3)*(t/d)
    return (y*(t/d)**2*0.5).astype(np.float32)
def impact():
    t = t_(2.5); f = 55*np.exp(-t*1.2)+28
    boom = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*2.2)*1.2
    nb = lp(rng.normal(0, 1, len(t)).astype(np.float32), 0.05)*np.exp(-t*6)*2.0
    sting = sum(np.sin(2*np.pi*fr*t+fr) for fr in (440, 466.2, 622.3, 880, 932.3))*np.exp(-t*1.6)*0.09
    sting *= np.minimum(1, t/0.01)
    return (boom+nb+sting).astype(np.float32)
def music(total):
    t = t_(total); n = len(t); prog = t/total
    pad = np.zeros(n, np.float32)
    for f, a in ((55, 0.5), (55.4, 0.4), (82.4, 0.25), (116.5, 0.18), (130.8, 0.12)):  # A, E, Bb, C: dark cluster
        pad += a*np.sin(2*np.pi*f*t + 0.5*np.sin(2*np.pi*0.07*t))
    pad *= 0.5+0.5*np.sin(2*np.pi*0.15*t)**2
    high = 0.06*np.sin(2*np.pi*(880+40*prog)*t)*np.sin(2*np.pi*0.3*t)**2*prog  # eerie whistle that grows
    pulse = np.zeros(n, np.float32)  # low pulse that speeds up towards the end
    beat_t = 0.0
    while beat_t < total-1:
        s = thump(42, 0.3, 10, 0)*0.6; i = int(beat_t*SR); pulse[i:i+len(s)] += s[:max(0, min(len(s), n-i))]
        beat_t += 1.1-0.5*(beat_t/total)
    y = (pad*0.22*(0.6+0.6*prog) + high + pulse*0.5)
    y *= np.minimum(1, t/0.15)  # no slow fade-in: the first second must already feel tense
    return y.astype(np.float32)

KEYS = [(('knock',), knock), (('ring', 'call', 'phone'), ring), (('creak', 'door'), creak),
        (('step', 'footstep', 'walk'), steps), (('static', 'radio', 'tv', 'screen', 'camera'), static),
        (('heart',), lambda: heartbeat(3, 100))]

def build(lines, times, speech, total, out='sfx.wav'):
    total = float(total)+1.5; n = int(total*SR); mix = np.zeros(n, np.float32)
    def put(sig, at, vol):
        i = int(max(0, at)*SR); j = min(n, i+len(sig))
        if j > i: mix[i:j] += sig[:j-i]*vol
    N = len(lines); twist = speech[-1][0]
    mus = music(total)
    # music drops out just before the twist, then comes back under the impact
    duck = np.ones(n, np.float32); a, b = int((twist-0.5)*SR), int(twist*SR)
    duck[max(0, a):b] = np.linspace(1, 0.15, max(1, b-max(0, a))); duck[b:b+int(1.0*SR)] = 0.15
    mix += mus[:n]*duck
    for i, (text, scene, pause) in enumerate(lines):
        st = speech[i][0]; low = text.lower()
        if 0 < i < N-1: put(whoosh(), st-0.25, 0.35)
        for keys, fn in KEYS:
            if any(k in low for k in keys): put(fn(), st+0.15, 0.55); break
    if N >= 3: put(heartbeat(5, 95), speech[N-3][0], 0.8)
    put(riser(min(2.0, max(0.8, twist-speech[N-2][0]))), twist-min(2.0, max(0.8, twist-speech[N-2][0])), 0.5)
    put(impact(), twist-0.05, 0.9)
    put(impact()[:int(1.2*SR)]*np.linspace(1, 0, int(1.2*SR)).astype(np.float32), 0.0, 0.7)  # opening hit on frame 1
    put(whoosh(0.3)[::-1].copy(), 0.0, 0.4)
    mix = mix/max(1e-6, np.abs(mix).max())*0.85
    sf.write(out, mix, SR)
    return out
