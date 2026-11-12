import sys, math, random, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

D = os.path.dirname(os.path.abspath(__file__))
SRC = OUT = None
PREVIEW = False
W, H, FPS = 1440, 2560, 30
DUR = 9.5667
NF = int(round(DUR * FPS))

CREAM = (251, 248, 237); GREEN = (77, 85, 73); BROWN = (79, 60, 53)
LIME = (205, 253, 132); PINK = (241, 160, 214); YELLOW = (255, 253, 96); WHITE = (255, 255, 255)

TG = '/usr/share/texmf/fonts/opentype/public/tex-gyre/'
MO = D + '/mont/fonts/ttf/'
def F(name, size):
    path = {'tbi': TG + 'texgyretermes-bolditalic.otf', 'tb': TG + 'texgyretermes-bold.otf',
            'ti': TG + 'texgyretermes-italic.otf'}.get(name) or MO + f'Montserrat-{name}.ttf'
    return ImageFont.truetype(path, size)

# ---------------- helpers ----------------
def smooth_noise(n, amp, seed, smooth=6):
    r = np.random.default_rng(seed)
    v = r.normal(0, 1, n + smooth * 4)
    k = np.ones(smooth) / smooth
    v = np.convolve(v, k, 'same')[smooth * 2: smooth * 2 + n]
    v = v / (np.abs(v).max() + 1e-6)
    return v * amp + r.normal(0, amp * 0.18, n)

def torn_poly(w, h, m, seed, amp=9, step=5, edges='tblr'):
    pts = []
    def edge(p0, p1, normal, s, torn):
        L = math.dist(p0, p1); n = max(2, int(L / step))
        off = smooth_noise(n, amp, s) if torn else np.zeros(n)
        for i in range(n):
            t = i / n
            x = p0[0] + (p1[0] - p0[0]) * t + normal[0] * off[i]
            y = p0[1] + (p1[1] - p0[1]) * t + normal[1] * off[i]
            pts.append((x, y))
    edge((m, m), (m + w, m), (0, 1), seed, 't' in edges)
    edge((m + w, m), (m + w, m + h), (1, 0), seed + 1, 'r' in edges)
    edge((m + w, m + h), (m, m + h), (0, 1), seed + 2, 'b' in edges)
    edge((m, m + h), (m, m), (1, 0), seed + 3, 'l' in edges)
    return pts

def grain(img, strength=10, seed=0):
    r = np.random.default_rng(seed)
    a = np.asarray(img).astype(np.int16)
    n = r.normal(0, strength, a.shape[:2])
    n = np.asarray(Image.fromarray(np.clip(n + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.int16) - 128
    for c in range(3):
        a[..., c] = np.clip(a[..., c] + n, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

def torn_paper(w, h, color, seed, amp=9, edges='tblr', shadow=True, rim=True):
    m = 40
    S = (w + 2 * m, h + 2 * m)
    base = Image.new('RGBA', S, (0, 0, 0, 0))
    # white fibrous rim
    if rim:
        rim_mask = Image.new('L', S, 0)
        ImageDraw.Draw(rim_mask).polygon(torn_poly(w + 10, h + 10, m - 5, seed + 50, amp * 1.1, 4, edges), fill=255)
        rim_mask = rim_mask.filter(ImageFilter.GaussianBlur(0.6))
        rimimg = Image.new('RGBA', S, (250, 250, 246, 255)); rimimg.putalpha(rim_mask)
        rimimg = grain(rimimg, 14, seed + 7)
    mask = Image.new('L', S, 0)
    ImageDraw.Draw(mask).polygon(torn_poly(w, h, m, seed, amp, 5, edges), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(0.5))
    paper = Image.new('RGBA', S, color + (255,)); paper.putalpha(mask)
    paper = grain(paper, 7, seed + 3)
    if shadow:
        a = (rim_mask if rim else mask)
        sh = Image.new('RGBA', S, (40, 30, 25, 0))
        sh.putalpha(a.point(lambda v: int(v * 0.42)))
        sh = sh.filter(ImageFilter.GaussianBlur(10))
        base.alpha_composite(sh, (6, 12))
    if rim:
        base.alpha_composite(rimimg)
    base.alpha_composite(paper)
    return base, m

def tape(w, h, seed, color=(250, 246, 225), alpha=175):
    m = 6
    im = Image.new('RGBA', (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    pts = []
    r = random.Random(seed)
    zig = 7
    pts.append((m, m))
    pts.append((m + w, m))
    for i in range(1, zig):
        pts.append((m + w + (r.uniform(-6, 2) if i % 2 else r.uniform(-1, 3)), m + h * i / zig))
    pts.append((m + w, m + h)); pts.append((m, m + h))
    for i in range(zig - 1, 0, -1):
        pts.append((m + (r.uniform(-2, 6) if i % 2 else r.uniform(-3, 1)), m + h * i / zig))
    ImageDraw.Draw(im).polygon(pts, fill=color + (alpha,))
    im = grain(im, 9, seed)
    # faint stripes
    d = ImageDraw.Draw(im)
    for x in range(m, m + w, 14):
        d.line([(x, m), (x, m + h)], fill=(255, 255, 255, 25), width=4)
    return im

def text_w(font, s):
    return font.getlength(s)

def rot(im, deg):
    return im.rotate(deg, resample=Image.BICUBIC, expand=True)

def sparkle2d(size, color, outline=None):
    s = size * 4
    im = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = s / 2; R = s / 2 - 4; k = R * 0.16
    pts = []
    for i in range(4):
        a = i * math.pi / 2 - math.pi / 2
        pts.append((c + R * math.cos(a), c + R * math.sin(a)))
        a2 = a + math.pi / 4
        pts.append((c + k * math.cos(a2), c + k * math.sin(a2)))
    if outline:
        d.polygon(pts, fill=color + (255,), outline=outline + (255,), width=10)
    else:
        d.polygon(pts, fill=color + (255,))
    return im.resize((size, size), Image.LANCZOS)

def load_seq(name, size):
    seq = []
    for i in range(24):
        im = Image.open(f'{D}/r3d/out/{name}_{i:02d}.png').convert('RGBA')
        bb = im.getbbox(); im = im.crop(bb)
        sc = size / max(im.size)
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.LANCZOS)
        # soft contact shadow
        sh = Image.new('RGBA', (im.width + 60, im.height + 60), (0, 0, 0, 0))
        a = im.split()[3].point(lambda v: int(v * 0.35))
        blk = Image.new('RGBA', im.size, (40, 30, 25, 255)); blk.putalpha(a)
        sh.alpha_composite(blk, (30 + 6, 30 + 14)); sh = sh.filter(ImageFilter.GaussianBlur(9))
        sh.alpha_composite(im, (30, 30))
        seq.append(sh)
    return seq

# easing
def clamp(x, a=0, b=1): return max(a, min(b, x))
def prog(t, t0, d): return clamp((t - t0) / d)
def ease_out_cubic(p): return 1 - (1 - p) ** 3
def ease_in_cubic(p): return p ** 3
def ease_out_back(p, s=1.9):
    p -= 1; return 1 + (s + 1) * p ** 3 + s * p ** 2

def paste(canvas, im, cx, cy, scale=1.0, angle=0.0, alpha=1.0):
    if alpha <= 0.003 or scale <= 0.01: return
    if abs(scale - 1) > 0.005:
        im = im.resize((max(1, int(im.width * scale)), max(1, int(im.height * scale))), Image.BILINEAR)
    if abs(angle) > 0.05:
        im = im.rotate(angle, resample=Image.BILINEAR, expand=True)
    if alpha < 0.997:
        a = im.split()[3].point(lambda v: int(v * alpha))
        im = im.copy(); im.putalpha(a)
    x = int(round(cx - im.width / 2)); y = int(round(cy - im.height / 2))
    canvas.alpha_composite(im, dest=(max(0, x), max(0, y)), source=(max(0, -x), max(0, -y)))

