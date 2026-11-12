"""Richer paper + sticker kit: crumpled facets, ransom letters, grid/lined/spiral paper, doodle cut-outs."""
from lib import *
from PIL import ImageOps

def crumple_shade(w, h, seed, cells=60, strength=0.16, crease=0.10):
    """fold-line crumple: many random straight creases, each a soft step in brightness (one side lit, other shaded)"""
    r = np.random.default_rng(seed)
    sw, sh = max(8, w // 3), max(8, h // 3)
    yy, xx = np.mgrid[0:sh, 0:sw].astype(np.float32)
    shade = np.zeros((sh, sw), np.float32); lines = np.zeros((sh, sw), np.float32)
    n = max(6, cells // 3)
    for _ in range(n):
        px, py = r.uniform(0, sw), r.uniform(0, sh); ang = r.uniform(0, np.pi)
        nx, ny = -np.sin(ang), np.cos(ang)
        dist = (xx - px) * nx + (yy - py) * ny
        width = r.uniform(2, 10)
        amp = r.uniform(0.3, 1.0) * r.choice([-1, 1])
        shade += amp * np.tanh(dist / width) * np.exp(-np.abs(dist) / (sw * 0.5))
        lines += np.exp(-(dist / 0.9) ** 2) * r.uniform(0.3, 1)
    shade = shade / (np.abs(shade).max() + 1e-6)
    S = Image.fromarray(((shade * 0.5 + 0.5) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5))
    E = Image.fromarray((np.clip(lines, 0, 1) * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(0.6))
    return (np.asarray(S).astype(np.float32) / 255 - 0.5) * strength * 1.6, np.asarray(E).astype(np.float32) / 255 * crease

def apply_crumple(img, seed, strength=0.11, crease=0.06, cells=60):
    s, e = crumple_shade(img.width, img.height, seed, cells, strength, crease)
    a = np.asarray(img).astype(np.float32)
    k = (1 + s * 1.0 - e)[..., None]
    a[..., :3] = np.clip(a[..., :3] * k, 0, 255)
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

def paper_sheet(w, h, color, seed, kind='plain', torn='tblr', amp=9, holes=None, crumple=True, rim=True, cells=60):
    """kind: plain | grid | lined | news ; holes: None | 'left' | 'top'"""
    S, m = torn_paper(w, h, color, seed, amp=amp, edges=torn, shadow=False, rim=rim)
    d = ImageDraw.Draw(S)
    ink = tuple(int(c * 0.72) for c in color)
    if kind == 'grid':
        for x in range(m + 10, m + w, 34): d.line([(x, m), (x, m + h)], fill=ink + (45,), width=2)
        for y in range(m + 10, m + h, 34): d.line([(m, y), (m + w, y)], fill=ink + (45,), width=2)
    elif kind == 'lined':
        for y in range(m + 70, m + h - 10, 56): d.line([(m, y), (m + w, y)], fill=(120, 150, 190, 90), width=2)
        d.line([(m + 90, m), (m + 90, m + h)], fill=(225, 120, 140, 140), width=3)
    elif kind == 'news':
        r = random.Random(seed)
        for y in range(m + 18, m + h - 10, 11):
            x = m + 14
            while x < m + w - 20:
                L = r.randint(8, 40); d.rectangle([x, y, min(x + L, m + w - 14), y + 3], fill=(90, 85, 80, 60)); x += L + r.randint(5, 9)
    S = apply_crumple(S, seed + 9, cells=cells) if crumple else S
    if holes:
        a = np.asarray(S.split()[3]).copy(); A = Image.fromarray(a); da = ImageDraw.Draw(A)
        if holes == 'left':
            for y in range(m + 40, m + h - 30, 58): da.rectangle([m + 18, y, m + 34, y + 16], fill=0)
        else:
            for x in range(m + 40, m + w - 30, 58): da.ellipse([x, m + 16, x + 20, m + 36], fill=0)
        S.putalpha(A)
    return S, m

def shadowed(im, off=(8, 14), blur=12, op=0.38, pad=40):
    out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: int(v * op))
    sh = Image.new('RGBA', im.size, (40, 30, 25, 255)); sh.putalpha(a)
    out.alpha_composite(sh, (pad + off[0], pad + off[1])); out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(im, (pad, pad)); return out

# ---------- ransom-note letters ----------
RANSOM_STYLES = [  # (font, paper, ink, kind)
    ('tb', CREAM, BROWN, 'plain'), ('Black', GREEN, LIME, 'plain'), ('tbi', PINK, BROWN, 'plain'),
    ('ExtraBold', YELLOW, GREEN, 'grid'), ('tb', LIME, GREEN, 'plain'), ('Black', BROWN, CREAM, 'plain'),
    ('tbi', CREAM, GREEN, 'news'), ('ExtraBold', PINK, CREAM, 'plain'), ('tb', YELLOW, BROWN, 'plain'),
]
def ransom_letter(ch, size, style_i, seed, distress=False):
    fname, paper, ink, kind = RANSOM_STYLES[style_i % len(RANSOM_STYLES)]
    f = F(fname, int(size * (1.05 if fname.startswith('t') else 0.92)))
    bb = f.getbbox(ch, anchor='ls')
    gw, gh = bb[2] - bb[0], bb[3] - bb[1]
    r = random.Random(seed)
    pw, ph = gw + r.randint(30, 60), gh + r.randint(34, 64)
    S, m = paper_sheet(pw, ph, paper, seed, kind=kind, amp=r.uniform(3, 7), rim=r.random() < 0.6, cells=14)
    # jitter cut: shear the quad slightly via polygon mask
    A = Image.new('L', S.size, 0); da = ImageDraw.Draw(A)
    j = lambda: r.uniform(-10, 10)
    da.polygon([(m + j(), m + j()), (m + pw + j(), m + j()), (m + pw + j(), m + ph + j()), (m + j(), m + ph + j())], fill=255)
    S.putalpha(ImageChops.multiply(S.split()[3], A.filter(ImageFilter.GaussianBlur(0.6))))
    T = Image.new('RGBA', S.size, (0, 0, 0, 0))
    ImageDraw.Draw(T).text((m + pw / 2 - (bb[0] + gw / 2), m + ph / 2 + gh / 2 - (bb[3])), ch, font=f, fill=ink + (255,), anchor='ls')
    if distress:
        rr = np.random.default_rng(seed)
        n = rr.random((T.height // 3 + 1, T.width // 3 + 1)) > 0.86
        N = Image.fromarray((~n * 255).astype(np.uint8)).resize(T.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(0.7))
        T.putalpha(ImageChops.multiply(T.split()[3], N))
    S.alpha_composite(T)
    return S

def ransom_word(text, size, seed, start_style=0, gap=-6, distress_every=4):
    r = random.Random(seed)
    tiles = []
    for i, ch in enumerate(text):
        if ch == ' ': tiles.append(None); continue
        L = ransom_letter(ch, size, start_style + i * 2 + r.randint(0, 3), seed + i * 13, distress=(i % distress_every == 1))
        L = L.rotate(r.uniform(-8, 8), resample=Image.BICUBIC, expand=True)
        L = L.crop(L.getbbox())
        tiles.append((L, r.uniform(-14, 14)))
    return tiles   # list of (img, yoff) — caller animates letter by letter

# ---------- doodle cut-out stickers ----------
def _star_pts(cx, cy, R, r, n=5, rot=-90):
    return [(cx + (R if i % 2 == 0 else r) * math.cos(math.radians(rot + i * 180 / n)),
             cy + (R if i % 2 == 0 else r) * math.sin(math.radians(rot + i * 180 / n))) for i in range(2 * n)]

def wobble(pts, amp, seed, closed=True, steps=8):
    r = random.Random(seed); out = []
    P = pts + ([pts[0]] if closed else [])
    for a, b in zip(P[:-1], P[1:]):
        for k in range(steps):
            t = k / steps
            out.append((a[0] + (b[0] - a[0]) * t + r.uniform(-amp, amp), a[1] + (b[1] - a[1]) * t + r.uniform(-amp, amp)))
    if closed: out.append(out[0])
    else: out.append(P[-1])
    return out

def doodle(kind, size, ink, seed, paper=(236, 228, 210), news=True):
    S = size * 2; r = random.Random(seed)
    shape = Image.new('L', (S, S), 0); ds = ImageDraw.Draw(shape)
    ink_l = Image.new('RGBA', (S, S), (0, 0, 0, 0)); di = ImageDraw.Draw(ink_l)
    c = S / 2; lw = max(6, size // 14)
    if kind == 'star':
        pts = _star_pts(c, c + size * 0.05, size * 0.72, size * 0.32)
        W_ = wobble(pts, size * 0.02, seed)
        ds.polygon(pts, fill=255)
        for k in range(-S, S, max(8, size // 18)):    # hatch fill
            di.line([(k, 0), (k + S, S)], fill=ink + (150,), width=max(3, lw // 2))
        hatch_mask = Image.new('L', (S, S), 0); ImageDraw.Draw(hatch_mask).polygon(_star_pts(c, c + size * 0.05, size * 0.62, size * 0.26), fill=255)
        ink_l.putalpha(ImageChops.multiply(ink_l.split()[3], hatch_mask))
        di = ImageDraw.Draw(ink_l); di.line(W_, fill=ink + (255,), width=lw, joint='curve')
    elif kind == 'sparkle':
        pts = []
        for i in range(8):
            a = math.radians(-90 + i * 45); rr_ = size * 0.75 if i % 2 == 0 else size * 0.16
            pts.append((c + rr_ * math.cos(a), c + rr_ * math.sin(a)))
        ds.polygon(pts, fill=255); di.line(wobble(pts, size * 0.015, seed), fill=ink + (255,), width=lw, joint='curve')
    elif kind == 'heart':
        pts = []
        for i in range(60):
            t = i / 60 * 2 * math.pi
            x = 16 * math.sin(t) ** 3; y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((c + x * size * 0.042, c + y * size * 0.042))
        ds.polygon(pts, fill=255); di.line(wobble(pts, size * 0.012, seed, steps=1), fill=ink + (255,), width=lw, joint='curve')
        di.line([(c - size * 0.3, c - size * 0.1), (c - size * 0.15, c - size * 0.3)], fill=ink + (200,), width=lw // 2)
    elif kind == 'arrow':   # loopy arrow pointing down
        pts = []
        for i in range(90):
            t = i / 89
            y = c - size * 0.7 + t * size * 1.3
            x = c + size * 0.25 * math.sin(t * 2.2 * math.pi)
            if 0.35 < t < 0.6:   # loop
                u = (t - 0.35) / 0.25 * 2 * math.pi
                x += size * 0.22 * math.sin(u); y -= size * 0.22 * (1 - math.cos(u)) * 0.6
            pts.append((x, y))
        tip = pts[-1]
        ds.line(pts, fill=255, width=lw * 3); di.line(pts, fill=ink + (255,), width=int(lw * 1.4), joint='curve')
        head = [(tip[0] - size * 0.28, tip[1] - size * 0.26), tip, (tip[0] + size * 0.28, tip[1] - size * 0.24)]
        ds.line(head, fill=255, width=lw * 3); di.line(head, fill=ink + (255,), width=int(lw * 1.4), joint='curve')
    elif kind == 'rays':    # "!" burst lines
        for i in range(5):
            a = math.radians(-160 + i * 35); r0, r1 = size * 0.35, size * 0.8
            p0 = (c + r0 * math.cos(a), c + size * 0.3 + r0 * math.sin(a)); p1 = (c + r1 * math.cos(a), c + size * 0.3 + r1 * math.sin(a))
            ds.line([p0, p1], fill=255, width=lw * 3); di.line([p0, p1], fill=ink + (255,), width=lw * 2)
    elif kind == 'circle':  # hand-drawn loop
        pts = [(c + size * 0.7 * math.cos(t) * (1 + 0.04 * math.sin(5 * t)), c + size * 0.42 * math.sin(t)) for t in np.linspace(-0.3, 2 * math.pi * 1.07, 80)]
        di.line(pts, fill=ink + (255,), width=lw, joint='curve')
        return ink_l.crop(ink_l.getbbox())
    # paper cut-out = dilated shape with rough edge
    cut = shape.filter(ImageFilter.MaxFilter(max(3, (size // 7) | 1)))
    noise = np.random.default_rng(seed).random((S // 6 + 1, S // 6 + 1))
    N = Image.fromarray((noise * 255).astype(np.uint8)).resize((S, S), Image.BILINEAR)
    cut = ImageChops.multiply(cut.filter(ImageFilter.GaussianBlur(5)), Image.eval(N, lambda v: 200 + v // 4))
    cut = cut.point(lambda v: 255 if v > 110 else 0).filter(ImageFilter.GaussianBlur(0.7))
    P = Image.new('RGBA', (S, S), paper + (255,))
    if news:
        dp = ImageDraw.Draw(P); rr = random.Random(seed)
        for y in range(4, S, 10):
            x = 4
            while x < S:
                L = rr.randint(8, 36); dp.rectangle([x, y, x + L, y + 3], fill=(110, 100, 90, 85)); x += L + rr.randint(5, 9)
    P = apply_crumple(P, seed, 0.12, 0.08, 16)
    P.putalpha(cut)
    P.alpha_composite(ink_l)
    bb = P.getbbox(); P = P.crop(bb)
    return shadowed(P, (4, 7), 5, 0.35, 20)
