import numpy as np, sys, wave
SR = 48000
rng = np.random.default_rng(3)

def env_exp(n, tau): return np.exp(-np.arange(n) / (tau * SR))
def lp(x, a):  # one-pole lowpass, a in (0,1)
    y = np.empty_like(x); s = 0.0
    for i, v in enumerate(x): s += a * (v - s); y[i] = s
    return y
def hp(x, a): return x - lp(x, a)

def pop(f0=880, f1=260, dur=0.12, vol=0.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / 0.018)
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = np.sin(ph) * env_exp(n, 0.035)
    x[:60] += rng.normal(0, 0.5, 60) * np.linspace(1, 0, 60)
    return x * vol

def whoosh(dur=0.42, vol=0.45, up=True):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    noise = rng.normal(0, 1, n)
    out = np.zeros(n); seg = 480
    for i in range(0, n, seg):
        p = t[i] if up else 1 - t[i]
        a = 0.03 + 0.25 * p
        out[i:i + seg] = lp(noise[i:i + seg], a)
    out = hp(out, 0.02)
    e = np.sin(np.pi * t) ** 1.6 * (t ** 0.4 if up else 1)
    out = out * e
    return out / (np.abs(out).max() + 1e-9) * vol

def rip(dur=0.32, vol=0.5):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    noise = hp(rng.normal(0, 1, n), 0.25)
    crack = np.zeros(n)
    idx = np.sort(rng.choice(n, int(n / 140), replace=False))
    for i in idx:
        L = min(n - i, int(rng.uniform(40, 200)))
        crack[i:i + L] += rng.uniform(0.4, 1) * np.exp(-np.arange(L) / 40)
    env = np.clip(t * 12, 0, 1) * (1 - t) ** 0.6
    x = noise * (0.25 + crack) * env
    return x / (np.abs(x).max() + 1e-9) * vol

def ding(base=1568, dur=1.1, vol=0.32):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.zeros(n)
    for k, (m, a, tau) in enumerate([(1, 1, 0.45), (2.0, 0.5, 0.25), (3.01, 0.3, 0.15), (4.2, 0.15, 0.08)]):
        x += a * np.sin(2 * np.pi * base * m * t) * np.exp(-t / tau)
    x[:200] *= np.linspace(0, 1, 200)
    return x / np.abs(x).max() * vol

def sparkle(dur=0.6, vol=0.22):
    n = int(dur * SR); x = np.zeros(n)
    for k, f in enumerate([2637, 3136, 3951, 4699]):
        s = int(k * 0.06 * SR); m = n - s; t = np.arange(m) / SR
        x[s:] += np.sin(2 * np.pi * f * t) * np.exp(-t / 0.12)
    return x / np.abs(x).max() * vol

def tick(f=1400, vol=0.35):
    return pop(f * 1.6, f, 0.07, vol)

def build(events, total, out):
    buf = np.zeros(int(total * SR) + SR)
    for t0, snd in events:
        i = int(t0 * SR); buf[i:i + len(snd)] += snd[:len(buf) - i]
    buf = buf[:int(total * SR)]
    st = np.stack([buf, buf], 1)
    st = np.clip(st, -1, 1)
    with wave.open(out, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype('<i2').tobytes())
