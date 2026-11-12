# MẪU DỰNG VIDEO (template) — video "10 ngách không lộ mặt"
# Chạy:  python3 compose_template.py <video_goc.mov> <video_ra.mp4>
#        python3 compose_template.py <video_goc.mov> x preview   (xuất ảnh xem trước, cần frames/q15_*.png)
# Cấu trúc: HOOK 0–3s -> nội dung chính (trang giấy, dòng hiện dần và Ở LẠI) -> câu chốt + CTA.
import sys, math, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from lib2 import *
import sfx

SRC = sys.argv[1]; OUT = sys.argv[2]
PREVIEW = len(sys.argv) > 3 and sys.argv[3] == 'preview'
SRC_DUR = 11.44
DUR = 11.44
NF = int(DUR * FPS)

def spaced(d, x, y, s, font, fill, gap=2.4, anchor='ls'):
    for ch in s:
        d.text((x, y), ch, font=font, fill=fill, anchor=anchor); x += font.getlength(ch) + gap
    return x
def spaced_w(s, font, gap): return sum(font.getlength(c) + gap for c in s)

def pill(texts, h, fill, outline, pad=38, shadow=BROWN):
    tw = sum(f.getlength(s) for s, f, _ in texts)
    w = int(tw) + pad * 2
    P = Image.new('RGBA', (w + 20, h + 20), (0, 0, 0, 0))
    d = ImageDraw.Draw(P)
    d.rounded_rectangle([6, 9, w + 6, h + 9], h // 2, fill=shadow + (210,))
    d.rounded_rectangle([0, 0, w, h], h // 2, fill=fill + (255,), outline=outline + (255,), width=3)
    x = pad
    for s, f, c in texts:
        d.text((x, h / 2 + 1), s, font=f, fill=c, anchor='lm'); x += f.getlength(s)
    return P

def drop_shadow(im, off=(8, 14), blur=12, op=0.4):
    pad = 40
    out = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    a = im.split()[3].point(lambda v: int(v * op))
    sh = Image.new('RGBA', im.size, (40, 30, 25, 255)); sh.putalpha(a)
    out.alpha_composite(sh, (pad + off[0], pad + off[1])); out = out.filter(ImageFilter.GaussianBlur(blur))
    out.alpha_composite(im, (pad, pad)); return out

def washi(text, font, h, color, fg, seed, alpha=255):
    w = int(font.getlength(text)) + 100
    m = 6
    T = Image.new('RGBA', (w + 2 * m, h + 2 * m), (0, 0, 0, 0))
    r = random.Random(seed); zig = 8; pts = []
    pts += [(m + 14, m), (m + w - 14, m)]
    for i in range(1, zig):
        pts.append((m + w - (0 if i % 2 else 16) + r.uniform(-2, 2), m + h * i / zig))
    pts += [(m + w - 14, m + h), (m + 14, m + h)]
    for i in range(zig - 1, 0, -1):
        pts.append((m + (0 if i % 2 else 16) + r.uniform(-2, 2), m + h * i / zig))
    ImageDraw.Draw(T).polygon(pts, fill=color + (alpha,))
    T = grain(T, 5, seed)
    d = ImageDraw.Draw(T)
    d.line([(m + 20, m + 5), (m + w - 20, m + 5)], fill=(255, 255, 255, 70), width=3)
    d.text((T.width / 2, T.height / 2 + 2), text, font=font, fill=fg, anchor='mm')
    return drop_shadow(T, (5, 8), 6, 0.35)

def rich_wrap(text, font, maxw):
    words = text.split(' '); lines = [[]]; cur = 0; sp = font.getlength(' ')
    for w_ in words:
        wl = font.getlength(w_) + (16 if '[' in w_ else 0)
        if lines[-1] and cur + sp + wl > maxw:
            lines.append([]); cur = 0
        cur += (sp if lines[-1] else 0) + wl; lines[-1].append(w_)
    return lines

def draw_rich(img, x0, y0, lines, font, lh, fg, hl_bg, hl_fg=None):
    d = ImageDraw.Draw(img); sp = font.getlength(' ')
    asc = font.getmetrics()[0]
    for i, ws in enumerate(lines):
        x = x0; y = y0 + i * lh
        for w_ in ws:
            if '[' in w_:
                core = w_[:w_.index(']') + 1]; tail = w_[w_.index(']') + 1:]
                tw = font.getlength(core)
                d.rounded_rectangle([x, y - asc * 0.78, x + tw + 16, y + asc * 0.28], 10, fill=hl_bg + (255,))
                d.text((x + 8, y), core, font=font, fill=hl_fg or fg, anchor='ls'); x += tw + 16
                if tail: d.text((x, y), tail, font=font, fill=fg, anchor='ls'); x += font.getlength(tail)
                x += sp
            else:
                d.text((x, y), w_, font=font, fill=fg, anchor='ls'); x += font.getlength(w_) + sp
    return d

HANDLE = pill([('@xaykenhdi_', F('Bold', 42), CREAM)], 80, GREEN, LIME, pad=32)

RED = (170, 50, 62)
def emoji(name, size):
    im = Image.open(f'{D}/icons/png/{name}.png').convert('RGBA')
    im = im.crop(im.getbbox()); sc = size / max(im.size)
    return im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
def wrapw(s, font, maxw):
    words = s.split(' '); lines = []; cur = ''
    for w_ in words:
        t_ = (cur + ' ' + w_).strip()
        if font.getlength(t_) <= maxw: cur = t_
        else: lines.append(cur); cur = w_
    lines.append(cur); return lines

# ================= HOOK =================
fA = F('Black', 82)
LA, ma = paper_sheet(1140, 150, CREAM, 2101, amp=10, cells=40)
ImageDraw.Draw(LA).text((ma + 570, ma + 110), 'CHƯA BIẾT LÀM KÊNH GÌ', font=fA, fill=BROWN, anchor='ms')
LA = shadowed(rot(LA, -1.5), (7, 12), 10, 0.38)
fB = F('tbi', 100)
LB, mb = paper_sheet(1000, 165, YELLOW, 2102, amp=11, cells=40)
d = ImageDraw.Draw(LB)
pre = 'mà không lộ '; full = pre + 'mặt?'
xb = mb + 500 - fB.getlength(full) / 2
d.text((xb, mb + 120), full, font=fB, fill=GREEN, anchor='ls')
MAT_X = xb + fB.getlength(pre); MAT_W = fB.getlength('mặt')
LB.alpha_composite(tape(130, 44, 2103, color=PINK, alpha=215), (mb + 860, mb - 22))
LB = rot(LB, 1.8)
SUB = washi('10 ngách hợp nhất', F('ExtraBold', 56), 104, LIME, BROWN, 2105)
SUB = rot(SUB, -1.5)
E_MONKEY = emoji('see-no-evil-monkey', 210); E_THINK = emoji('thinking-face', 150)

# ================= NICHE PAGES =================
NICHES = [('Nấu ăn', 'quay tay và chảo', 'cooking'), ('Dọn nhà, sắp xếp', 'trước và sau', 'broom'),
          ('Học tập', 'sổ ghi chép, màn hình', 'books'), ('Chi tiêu cá nhân', 'sổ, bảng tính', 'money-with-wings'),
          ('Review sách', 'tay lật trang', 'open-book'),
          ('Bán hàng, làm nội dung', 'quay màn hình', 'mobile-phone'), ('Đồ thủ công', 'quá trình làm', 'yarn'),
          ('Chăm cây', 'cây lớn qua từng tuần', 'potted-plant'), ('Thú cưng', 'bé là nhân vật chính', 'cat-face'),
          ('Đi bộ khám phá phố', 'góc nhìn người đi', 'person-walking')]
PW = 1240; ROWH = 178; HEAD = 120
PH = HEAD + 5 * ROWH + 20
fN = F('tbi', 64); fTi = F('ExtraBold', 50); fDe = F('Medium', 40)
PAGES = []
for pi in range(2):
    col, kind, holes = [(PINK, 'plain', None), (LIME, 'lined', 'left')][pi]
    S, m = paper_sheet(PW, PH, col, 2200 + pi * 7, kind=kind, holes=holes, amp=10, cells=60)
    d = ImageDraw.Draw(S)
    x0 = m + (70 if holes else 50)
    d.rectangle([x0 + 5, m + 36, x0 + 225, m + 104], fill=BROWN + (255,))
    d.rectangle([x0, m + 30, x0 + 220, m + 98], fill=GREEN + (255,))
    d.text((x0 + 110, m + 66), ['01–05', '06–10'][pi], font=F('Black', 44), fill=YELLOW, anchor='mm')
    spaced(d, x0 + 250, m + 82, 'NGÁCH KHÔNG LỘ MẶT', F('ExtraBold', 36), BROWN, 3)
    S.alpha_composite(tape(170, 50, 2210 + pi, color=[YELLOW, PINK][pi], alpha=215), ((m + PW - 160) if pi == 0 else (m - 40), m - 24))
    rows = []
    for j in range(5):
        k = pi * 5 + j; ti, de, emo = NICHES[k]
        R = Image.new('RGBA', (PW - 40, ROWH), (0, 0, 0, 0)); dr = ImageDraw.Draw(R)
        # white emoji badge
        dr.ellipse([46, 30, 166, 150], fill=CREAM + (255,), outline=BROWN + (255,), width=4)
        E = emoji(emo, 92); R.alpha_composite(E, (int(106 - E.width / 2), int(90 - E.height / 2)))
        dr.text((270, 88), f'{k + 1}.', font=fN, fill=GREEN, anchor='rs')
        dr.text((290, 86), ti, font=fTi, fill=BROWN, anchor='ls')
        dr.text((292, 138), '→ ' + de, font=fDe, fill=GREEN, anchor='ls')
        if j < 4:
            for xx in range(60, PW - 100, 14): dr.ellipse([xx, ROWH - 6, xx + 4, ROWH - 2], fill=GREEN + (60,))
        rows.append((R, x0 - 50 + (20 if holes else 0), m + HEAD + j * ROWH))
    PAGES.append((S, m, rows))
PAGE_TOP = 1220
PAGE_ANG = [-1.0, 0.9]

# ================= OUTRO =================
fO = F('tbi', 92)
O, om = paper_sheet(1180, 290, CREAM, 2301, amp=12, cells=60)
d = ImageDraw.Draw(O)
d.text((om + 590, om + 115), 'Chọn ngách mà', font=fO, fill=BROWN, anchor='ms')
l2 = 'chính tay sốp làm mỗi ngày'
x2 = om + 590 - fO.getlength(l2) / 2; wct = fO.getlength('chính tay')
d.rounded_rectangle([x2 - 12, om + 160, x2 + wct + 10, om + 250], 16, fill=LIME + (255,))
d.text((om + 590, om + 230), l2, font=fO, fill=BROWN, anchor='ms')
O.alpha_composite(tape(150, 46, 2302, color=PINK, alpha=215), (om - 40, om - 22))
O = shadowed(rot(O, -1.5), (8, 13), 11, 0.38)
E_HAND = emoji('writing-hand', 170)
CTA = washi('Follow và cmt “PLAN” nhận bộ tài liệu hướng dẫn xây kênh nhé', F('Bold', 36), 86, YELLOW, BROWN, 2310)
CTA = rot(CTA, 1.0)

ST = {k: load_seq(k, s) for k, s in [('arrow', 150), ('star', 170), ('sparkle', 150), ('heart', 150)]}
def sf(name, t, speed=0.5, ph=0.0): return ST[name][int(((t * speed + ph) % 1) * 24) % 24]
TW = {s: sparkle2d(s, c, BROWN) for s, c in [(54, YELLOW), (44, LIME), (38, CREAM), (42, PINK)]}
D_STAR = doodle('star', 110, RED, 2401); D_HEART = doodle('heart', 100, RED, 2402)

# ================= timeline =================
T_LA, T_LB, T_CEN, T_SUB = 0.06, 0.45, 0.85, 1.35
T_HOOK_OUT = 2.72
T_PG = [3.0, 6.0]; RSTEP = 0.45
T_PG_OUT = 8.85
T_O, T_CTA = 9.0, 9.6

def frame(t):
    cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ph = ease_out_back(prog(t, 0.0, 0.4))
    paste(cv, HANDLE, 70 + HANDLE.width / 2, 175, ph, 0, 1)
    paste(cv, TW[38], 70 + HANDLE.width + 12, 150, ph * (0.8 + 0.2 * math.sin(t * 6)), t * 50, 1)

    out = ease_in_cubic(prog(t, T_HOOK_OUT, 0.3))
    if t < T_HOOK_OUT + 0.35:
        ha = 1 - out; up = -260 * out
        p = prog(t, T_LA, 0.35)
        paste(cv, LA, 720, 1420 + up, 0.5 + 0.5 * ease_out_back(p), 0, min(1, p * 3) * ha)
        p = ease_out_back(prog(t, T_LB, 0.35))
        cxb, cyb = 760, 1610 + up
        paste(cv, shadowed(LB, (7, 12), 10, 0.38), cxb, cyb, p, 0, min(1, p * 3) * ha)
        pm_ = ease_out_back(prog(t, T_CEN + 0.1, 0.35))
        paste(cv, E_MONKEY, 1250, 1200 + up + 8 * math.sin(t * 4), pm_, 6 * math.sin(t * 3), ha)
        paste(cv, E_THINK, 170, 1790 + up + 8 * math.sin(t * 3.4), pm_ * 0.9, -6, ha)
        p = ease_out_cubic(prog(t, T_SUB, 0.35))
        paste(cv, SUB, 660 - 1000 * (1 - p), 1890 - up * 0.8, 1, 0, min(1, prog(t, T_SUB, 0.12)) * ha)
        pa = ease_out_back(prog(t, T_SUB + 0.25, 0.3))
        paste(cv, sf('arrow', t, 0.7), 660 + SUB.width / 2 + 25, 1895 + 18 * abs(math.sin(t * 5)) - up * 0.8, pa, 0, ha)

    for pi in range(2):
        t0 = T_PG[pi]; t1 = T_PG[1] if pi == 0 else T_PG_OUT
        if not (t0 <= t < t1 + 0.35): continue
        S, m, rows = PAGES[pi]; L = S.copy()
        for j, (R, rx, ry) in enumerate(rows):
            q = prog(t, t0 + 0.3 + j * RSTEP, 0.28)
            if q <= 0: continue
            e = ease_out_cubic(q); RR = R if q >= 1 else R.copy()
            if q < 1: RR.putalpha(R.split()[3].point(lambda v, e=e: int(v * e)))
            L.alpha_composite(RR, (rx + int(-50 * (1 - e)), ry))
        pin = ease_out_cubic(prog(t, t0, 0.35)); pout = ease_in_cubic(prog(t, t1 - 0.05, 0.33))
        s_ = -1 if pi == 0 else 1
        x = 720 + (-s_) * 1300 * (1 - pin) + s_ * 1350 * pout
        ang = PAGE_ANG[pi] + (-s_) * 10 * (1 - pin) + s_ * 18 * pout
        paste(cv, shadowed(L, (8, 14), 12, 0.38), x, PAGE_TOP + PH / 2, 1, ang, 1)
        pk = ease_out_back(prog(t, t0 + 0.3, 0.3)) * (1 - pout)
        paste(cv, [D_STAR, D_HEART][pi], x + 560, PAGE_TOP - 20, pk, 8 * math.sin(t * 3), 1)
        paste(cv, TW[54], 110, PAGE_TOP + PH + 20, pk * (0.8 + 0.2 * math.sin(t * 7)), t * 40, 1)

    if t >= T_O:
        p = prog(t, T_O, 0.38)
        paste(cv, O, 720, 1650, 0.45 + 0.55 * ease_out_back(p), -8 * (1 - ease_out_cubic(p)), min(1, p * 3))
        pk = ease_out_back(prog(t, T_O + 0.25, 0.35))
        paste(cv, E_HAND, 1250, 1440 + 8 * math.sin(t * 4), pk, 8 * math.sin(t * 5), 1)
        paste(cv, sf('sparkle', t, 0.45), 170, 1470, pk * 0.8, 0, 1)
        pc = ease_out_cubic(prog(t, T_CTA, 0.35))
        if pc > 0:
            paste(cv, CTA, 720 + 900 * (1 - pc), 1950, 1, 0, min(1, prog(t, T_CTA, 0.12)))
    return cv

if PREVIEW:
    ts_ = [2.0, 5.5, 8.5, 11.2]
    ims = []
    for ts in ts_:
        bg = Image.open(f'{D}/frames/q15_{ts}.png').convert('RGBA').resize((W, H))
        bg.alpha_composite(frame(ts)); ims.append(bg.convert('RGB').resize((540, 960)))
    s = Image.new('RGB', (540 * len(ims), 960)); [s.paste(im, (i * 540, 0)) for i, im in enumerate(ims)]
    s.save(f'{D}/frames/prev15.png')
    bg = Image.open(f'{D}/frames/q15_5.5.png').convert('RGBA'); bg.alpha_composite(frame(5.5)); bg.convert('RGB').crop((0, 1100, 1440, 2450)).resize((720, 675)).save(f'{D}/frames/prev15_p.png')
    sys.exit()

ev = [(T_LA + 0.05, sfx.rip(0.3, 0.45)), (T_LA + 0.12, sfx.pop(600, 180, 0.15, 0.5)), (T_LB, sfx.pop(900, 330, 0.12, 0.5)),
      (T_CEN + 0.15, sfx.pop(300, 100, 0.2, 0.55)),
      (T_SUB - 0.05, sfx.whoosh(0.3, 0.3)), (T_SUB + 0.25, sfx.tick(1500, 0.3)), (T_HOOK_OUT - 0.05, sfx.whoosh(0.4, 0.38))]
for pi, tp in enumerate(T_PG):
    if pi: ev.append((tp - 0.08, sfx.rip(0.4, 0.5)))
    ev.append((tp, sfx.whoosh(0.3, 0.3)))
    for j in range(5): ev.append((tp + 0.3 + j * RSTEP, sfx.pop(850 + j * 120 + pi * 60, 330, 0.11, 0.42)))
ev += [(T_PG_OUT - 0.05, sfx.whoosh(0.4, 0.38, up=False)), (T_O, sfx.rip(0.3, 0.45)), (T_O + 0.1, sfx.pop(650, 200, 0.16, 0.5)),
       (T_O + 0.3, sfx.ding(1318, 1.2, 0.24)), (T_CTA - 0.05, sfx.whoosh(0.3, 0.28)), (T_CTA + 0.2, sfx.sparkle(0.7, 0.2))]
WAV = f'{D}/sfx15.wav'
sfx.build(ev, DUR, WAV)
cmd = ['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-i', WAV,
       '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
       '-filter_complex',
       '[0:v]scale=1440:2560,setsar=1,fps=30,format=yuv420p[b];[b][2:v]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v];'
       '[0:a]aresample=48000,volume=0.75[a0];[1:a]volume=1.0[a1];[a1][a0]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]',
       '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-profile:v', 'high',
       '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(DUR), OUT]
pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
for n in range(NF):
    pr.stdin.write(frame(n / FPS).tobytes())
pr.stdin.close(); pr.wait(); print('done', pr.returncode)
