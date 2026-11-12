# Video 16 · 50 câu mở đầu copy dùng ngay
# Chạy:  python3 compose.py none ra.mp4            (chưa có clip: nền giấy chấm bi)
#        python3 compose.py clip.mov ra.mp4         (có clip: clip làm nền, mờ nhẹ sau trang giấy)
#        python3 compose.py none x preview          (ảnh xem trước 5 khung -> work/prev16.png)
# Nội dung đọc từ noi-dung.md cùng thư mục (dòng "- **N.** ..." và tiêu đề "### ... Trang k: <nhóm> (..)").
import sys, os, re, math, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, ROOT)
from lib import *
from lib2 import *
import sfx

SRC = sys.argv[1]; OUT = sys.argv[2]
PREVIEW = len(sys.argv) > 3 and sys.argv[3] == 'preview'
DUR = 18.0
NF = int(DUR * FPS)
RED = (170, 50, 62)
_paste = paste
def paste(canvas, im, cx, cy, scale=1.0, angle=0.0, alpha=1.0):
    r = max(im.width, im.height) * max(scale, 0.01) * 0.75
    if cx + r < 0 or cx - r > W or cy + r < 0 or cy - r > H: return
    try: _paste(canvas, im, cx, cy, scale, angle, alpha)
    except ValueError: pass

# ---------- đọc nội dung ----------
md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 5 and len(ITEMS) == 50, (len(GROUPS), len(ITEMS))

def emoji(name, size):
    im = Image.open(f'{ROOT}/icons/png/{name}.png').convert('RGBA')
    im = im.crop(im.getbbox()); sc = size / max(im.size)
    return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)

def washi(text, font, h, color, fg, seed):
    w = int(font.getlength(text)) + 100; m = 6
    T = Image.new('RGBA', (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    r = random.Random(seed); zig = 8; pts = [(m + 14, m), (m + w - 14, m)]
    for i in range(1, zig): pts.append((m + w - (0 if i % 2 else 16) + r.uniform(-2, 2), m + h * i / zig))
    pts += [(m + w - 14, m + h), (m + 14, m + h)]
    for i in range(zig - 1, 0, -1): pts.append((m + (0 if i % 2 else 16) + r.uniform(-2, 2), m + h * i / zig))
    ImageDraw.Draw(T).polygon(pts, fill=color + (255,))
    T = grain(T, 5, seed); d = ImageDraw.Draw(T)
    d.text((T.width / 2, T.height / 2 + 2), text, font=font, fill=fg, anchor='mm')
    return shadowed(T, (5, 8), 6, 0.35)

def pill(text, font, h, fill, outline, fg, pad=32):
    w = int(font.getlength(text)) + pad * 2
    P = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(P)
    d.rounded_rectangle([6, 9, w + 6, h + 9], h // 2, fill=BROWN + (210,))
    d.rounded_rectangle([0, 0, w, h], h // 2, fill=fill + (255,), outline=outline + (255,), width=3)
    d.text((pad, h / 2 + 1), text, font=font, fill=fg, anchor='lm'); return P

def blank_text(d, x, y, s, font, fg, slot=96):
    """Vẽ câu có chỗ trống ___ thành ô tô vàng có gạch chân."""
    asc = font.getmetrics()[0]
    for k, part in enumerate(s.split('___')):
        if k:
            d.rounded_rectangle([x + 4, y - asc * 0.70, x + slot - 4, y + 8], 8, fill=YELLOW + (255,))
            d.line([(x + 10, y + 4), (x + slot - 10, y + 4)], fill=BROWN + (255,), width=4)
            x += slot
        if part:
            d.text((x, y), part, font=font, fill=fg, anchor='ls'); x += font.getlength(part)
    return x
def blank_w(s, font, slot=96): return sum(font.getlength(p) for p in s.split('___')) + slot * s.count('___')

# ---------- nền khi chưa có clip ----------
def make_bg():
    bg = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(bg)
    for y in range(40, H, 48):
        for x in range(40, W, 48): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=GREEN + (38,))
    bg = grain(bg, 6, 16)
    v = Image.new('L', (W, H), 0); dv = ImageDraw.Draw(v)
    dv.ellipse([-500, -300, W + 500, H + 300], fill=255); v = v.filter(ImageFilter.GaussianBlur(260))
    dark = Image.new('RGBA', (W, H), (205, 190, 160, 255)); dark.putalpha(v.point(lambda a: int((255 - a) * 0.55)))
    bg.alpha_composite(dark); return bg
BG = make_bg() if SRC == 'none' else None
CLIP = SRC != 'none'   # có clip quay mặt: mặt ở nửa trên (y≈380–1150) -> chữ dồn xuống dưới
HOOK_Y = [1450, 1690, 1920] if CLIP else [1150, 1400, 1650]

# ---------- HOOK ----------
HANDLE = pill('@xaykenhdi_', F('Bold', 42), 80, GREEN, LIME, CREAM)
fA = F('Black', 132)
LA, ma = paper_sheet(1180, 210, CREAM, 1601, amp=10, cells=40)
ImageDraw.Draw(LA).text((ma + 590, ma + 155), '50 CÂU MỞ ĐẦU', font=fA, fill=BROWN, anchor='ms')
LA.alpha_composite(tape(150, 46, 1602, color=PINK, alpha=215), (ma - 30, ma - 22))
LA = shadowed(rot(LA, -1.5), (7, 12), 10, 0.38)
fB = F('tbi', 118)
LB, mb = paper_sheet(900, 175, LIME, 1603, amp=11, cells=40)
d = ImageDraw.Draw(LB); full = 'copy dùng ngay'
xb = mb + 450 - fB.getlength(full) / 2; wc = fB.getlength('copy')
d.rounded_rectangle([xb - 12, mb + 36, xb + wc + 12, mb + 150], 18, fill=YELLOW + (255,))
d.text((xb, mb + 128), full, font=fB, fill=GREEN, anchor='ls')
LB = shadowed(rot(LB, 1.8), (7, 12), 10, 0.38)
SUB = rot(washi('Thay tên ngách của bạn vào chỗ ___ là xong', F('ExtraBold', 46), 100, YELLOW, BROWN, 1605), -1.5)
E_HAND = emoji('writing-hand', 200); E_MEMO = emoji('memo', 150)

# ---------- 5 TRANG ----------
PW = 1340 if CLIP else 1300; HEAD = 118 if CLIP else 150; ROWH = 82 if CLIP else 112; PH = HEAD + 10 * ROWH + 30
STYLE = [(CREAM, 'grid'), (PINK, 'plain'), (LIME, 'grid'), (YELLOW, 'plain'), (CREAM, 'lined')]
if CLIP: STYLE = [(c, 'plain') for c, _ in STYLE]   # chữ nhỏ: bỏ đường kẻ để không cắt ngang chữ
TAPE = [YELLOW, LIME, PINK, LIME, PINK]
fNum = F('Black', 34); fHead = F('ExtraBold', 40)
def row_font(texts):
    for sz in (range(36, 27, -1) if CLIP else range(46, 33, -1)):
        f = F('SemiBold', sz)
        if max(blank_w(s, f) for s in texts) <= PW - 230: return f
    return F('SemiBold', 28 if CLIP else 34)
PAGES = []
for pi, (gname, a, b) in enumerate(GROUPS):
    a, b = int(a), int(b); col, kind = STYLE[pi]
    S, m = paper_sheet(PW, PH, col, 1700 + pi * 11, kind=kind, amp=10, cells=60)
    d = ImageDraw.Draw(S); x0 = m + 60
    hy = -14 if CLIP else 0
    d.rectangle([x0 + 5, m + 40 + hy, x0 + 235, m + 112 + hy], fill=BROWN + (255,))
    d.rectangle([x0, m + 34 + hy, x0 + 230, m + 106 + hy], fill=GREEN + (255,))
    d.text((x0 + 115, m + 71 + hy), f'{a:02d}–{b:02d}', font=F('Black', 44), fill=YELLOW, anchor='mm')
    x = x0 + 262
    for ch in gname.upper(): d.text((x, m + 88 + hy), ch, font=fHead, fill=BROWN, anchor='ls'); x += fHead.getlength(ch) + 3
    S.alpha_composite(tape(180, 52, 1750 + pi, color=TAPE[pi], alpha=215), ((m + PW - 170) if pi % 2 == 0 else (m - 40), m - 26))
    texts = [ITEMS[n] for n in range(a, b + 1)]; fR = row_font(texts)
    rows = []
    for j, n in enumerate(range(a, b + 1)):
        R = Image.new('RGBA', (PW - 40, ROWH), (0, 0, 0, 0)); dr = ImageDraw.Draw(R)
        c = [PINK, LIME][j % 2] if col not in (PINK, LIME) else CREAM
        cy_ = ROWH / 2; rr = 28 if CLIP else 36
        dr.ellipse([76 - rr, cy_ - rr, 76 + rr, cy_ + rr], fill=c + (255,), outline=BROWN + (255,), width=4)
        dr.text((76, cy_), str(n), font=F('Black', 26) if CLIP else fNum, fill=BROWN, anchor='mm')
        blank_text(dr, 130, cy_ + fR.size * 0.36, ITEMS[n], fR, BROWN, slot=76 if CLIP else 96)
        if j < 9:
            for xx in range(140, PW - 120, 14): dr.ellipse([xx, ROWH - 5, xx + 4, ROWH - 1], fill=GREEN + (55,))
        rows.append((R, m + 20, m + HEAD + j * ROWH))
    PAGES.append((S, m, rows))
PAGE_CY = 1700 if CLIP else 1230
PAGE_ANG = [-0.9, 0.8, -0.7, 0.9, -0.8]

# ---------- CHỐT ----------
fO = F('tbi', 100)
O, om = paper_sheet(1180, 300, CREAM, 1801, amp=12, cells=60)
d = ImageDraw.Draw(O)
d.text((om + 590, om + 120), 'Lưu lại,', font=fO, fill=BROWN, anchor='ms')
l2 = 'mỗi ngày dùng 1 câu'; x2 = om + 590 - fO.getlength(l2) / 2; wm = fO.getlength('mỗi ngày')
d.rounded_rectangle([x2 - 12, om + 168, x2 + wm + 12, om + 262], 16, fill=LIME + (255,))
d.text((om + 590, om + 240), l2, font=fO, fill=BROWN, anchor='ms')
O.alpha_composite(tape(150, 46, 1802, color=YELLOW, alpha=215), (om + 1050, om - 22))
O = shadowed(rot(O, -1.5), (8, 13), 11, 0.38)
E_BOOK = emoji('bookmark', 180)

ST = {k: load_seq(k, s) for k, s in [('sparkle', 150), ('star', 140), ('pencil', 230)]}
def sf(name, t, speed=0.5, ph=0.0): return ST[name][int(((t * speed + ph) % 1) * 24) % 24]
TW = {s: sparkle2d(s, c, BROWN) for s, c in [(54, YELLOW), (44, LIME), (38, CREAM)]}
D_STAR = doodle('star', 110, RED, 1901); D_HEART = doodle('heart', 100, RED, 1902)

# ---------- timeline ----------
T_LA, T_LB, T_SUB, T_HOOK_OUT = 0.06, 0.45, 1.25, 2.72
T_PG = [3.0, 5.5, 8.0, 10.5, 13.0]; T_PG_END = 15.35; RSTEP = 0.07
T_O = 15.5

def frame(t):
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ph = ease_out_back(prog(t, 0.0, 0.4))
    paste(cv, HANDLE, 70 + HANDLE.width / 2, 175, ph, 0, 1)
    paste(cv, TW[38], 70 + HANDLE.width + 12, 150, ph * (0.8 + 0.2 * math.sin(t * 6)), t * 50, 1)

    if t < T_HOOK_OUT + 0.35:
        out = ease_in_cubic(prog(t, T_HOOK_OUT, 0.3)); ha = 1 - out; up = -260 * out
        p = prog(t, T_LA, 0.35)
        paste(cv, LA, 720, HOOK_Y[0] + up, 0.5 + 0.5 * ease_out_back(p), 0, min(1, p * 3) * ha)
        p = ease_out_back(prog(t, T_LB, 0.35))
        paste(cv, LB, 760, HOOK_Y[1] + up, p, 0, min(1, p * 3) * ha)
        pm = ease_out_back(prog(t, T_LB + 0.2, 0.35))
        paste(cv, E_HAND, 1250, HOOK_Y[0] - 250 + up + 8 * math.sin(t * 4), pm, 6 * math.sin(t * 3), ha)
        paste(cv, sf('pencil', t, 0.5), 200, HOOK_Y[1] + 120 + up, pm * 0.9, 0, ha)
        p = ease_out_cubic(prog(t, T_SUB, 0.35))
        paste(cv, SUB, 720 - 1100 * (1 - p), HOOK_Y[2] - up * 0.8, 1, 0, min(1, prog(t, T_SUB, 0.12)) * ha)
        paste(cv, sf('sparkle', t, 0.45), 1260, HOOK_Y[2] - 90, ease_out_back(prog(t, T_SUB + 0.2, 0.3)) * 0.8 * ha, 0, 1)

    for pi in range(5):
        t0 = T_PG[pi]; t1 = T_PG[pi + 1] if pi < 4 else T_PG_END
        if not (t0 <= t < t1 + 0.35): continue
        S, m, rows = PAGES[pi]; L = S.copy()
        for j, (R, rx, ry) in enumerate(rows):
            q = prog(t, t0 + 0.22 + j * RSTEP, 0.2)
            if q <= 0: continue
            e = ease_out_cubic(q); RR = R if q >= 1 else R.copy()
            if q < 1: RR.putalpha(R.split()[3].point(lambda v, e=e: int(v * e)))
            L.alpha_composite(RR, (rx + int(-40 * (1 - e)), ry))
        pin = ease_out_cubic(prog(t, t0, 0.33)); pout = ease_in_cubic(prog(t, t1 - 0.05, 0.33))
        s_ = -1 if pi % 2 == 0 else 1
        x = 720 + (-s_) * 1400 * (1 - pin) + s_ * 1450 * pout
        ang = PAGE_ANG[pi] + (-s_) * 10 * (1 - pin) + s_ * 18 * pout
        paste(cv, shadowed(L, (8, 14), 12, 0.38), x, PAGE_CY, 1, ang, 1)
        pk = ease_out_back(prog(t, t0 + 0.3, 0.3)) * (1 - pout)
        paste(cv, [D_STAR, D_HEART][pi % 2], x + (560 if pi % 2 == 0 else -560), PAGE_CY - PH / 2 - 10, pk, 8 * math.sin(t * 3), 1)
        paste(cv, sf('star', t, 0.4), x + (-540 if pi % 2 == 0 else 540), PAGE_CY + PH / 2 + 30, pk * 0.8, 0, 1)

    if t >= T_O:
        p = prog(t, T_O, 0.38)
        paste(cv, O, 720, 1700 if CLIP else 1250, 0.45 + 0.55 * ease_out_back(p), -8 * (1 - ease_out_cubic(p)), min(1, p * 3))
        pk = ease_out_back(prog(t, T_O + 0.25, 0.35))
        paste(cv, E_BOOK, 1210, (1470 if CLIP else 1020) + 8 * math.sin(t * 4), pk, 8 * math.sin(t * 5), 1)
        paste(cv, sf('sparkle', t, 0.45), 210, 1930 if CLIP else 1480, pk * 0.8, 0, 1)
        paste(cv, TW[54], 1180, 1950 if CLIP else 1500, pk * (0.8 + 0.2 * math.sin(t * 7)), t * 40, 1)
    return cv

_CF = {}
def with_bg(t):
    if BG is not None: im = BG.copy()
    else:
        k = min(t, 12.3)
        if k not in _CF:
            raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(k), '-i', SRC, '-frames:v', '1', '-vf', 'scale=1440:2560', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
            _CF[k] = Image.frombytes('RGBA', (W, H), raw)
        im = _CF[k].copy()
    im.alpha_composite(frame(t)); return im

if PREVIEW:
    os.makedirs(f'{ROOT}/work', exist_ok=True)
    ts_ = [2.0, 4.5, 9.5, 14.5, 17.5]
    ims = [with_bg(ts).convert('RGB').resize((432, 768)) for ts in ts_]
    s = Image.new('RGB', (432 * len(ims), 768)); [s.paste(im, (i * 432, 0)) for i, im in enumerate(ims)]
    s.save(f'{ROOT}/work/prev16.png'); with_bg(9.5).convert('RGB').crop((0, 520, 1440, 1960)).resize((720, 720)).save(f'{ROOT}/work/prev16_p.png')
    sys.exit()

ev = [(T_LA + 0.05, sfx.rip(0.3, 0.45)), (T_LA + 0.12, sfx.pop(600, 180, 0.15, 0.5)), (T_LB, sfx.pop(900, 330, 0.12, 0.5)),
      (T_SUB - 0.05, sfx.whoosh(0.3, 0.3)), (T_SUB + 0.25, sfx.tick(1500, 0.3)), (T_HOOK_OUT - 0.05, sfx.whoosh(0.4, 0.38))]
for pi, tp in enumerate(T_PG):
    if pi: ev.append((tp - 0.08, sfx.rip(0.4, 0.45)))
    ev.append((tp, sfx.whoosh(0.3, 0.3)))
    for j in range(0, 10, 2): ev.append((tp + 0.22 + j * RSTEP, sfx.pop(850 + j * 60 + pi * 40, 330, 0.09, 0.32)))
ev += [(T_PG_END - 0.05, sfx.whoosh(0.4, 0.38, up=False)), (T_O, sfx.rip(0.3, 0.45)), (T_O + 0.1, sfx.pop(650, 200, 0.16, 0.5)),
       (T_O + 0.3, sfx.ding(1318, 1.2, 0.24)), (T_O + 0.6, sfx.sparkle(0.7, 0.2))]
os.makedirs(f'{ROOT}/work', exist_ok=True)
WAV = f'{ROOT}/work/sfx16.wav'
sfx.build(ev, DUR, WAV)
if SRC == 'none':
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', WAV,
           '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(DUR), OUT]
    get = lambda t: with_bg(t)
else:
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-i', WAV,
           '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-filter_complex',
           '[0:v]scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=30,format=yuv420p[b];'
           '[b][2:v]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v];'
           '[0:a]aresample=48000,volume=0.75,apad[a0];[1:a]volume=1.0[a1];[a1][a0]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]',
           '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-profile:v', 'high',
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(DUR), OUT]
    get = frame
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(NF): pr.stdin.write(get(n / FPS).tobytes())
pr.stdin.close(); pr.wait(); print('done', pr.returncode)
