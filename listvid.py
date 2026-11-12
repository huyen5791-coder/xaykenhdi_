# Khung dựng chung cho video "danh sách nhiều trang" (16, 17, 18…)
# HOOK hiện đủ ngay từ khung đầu tiên (chủ kênh chốt 12/11) -> nhiều trang giấy, dòng hiện nhanh rồi Ở LẠI -> câu chốt.
# Có clip quay mặt: mặt ở nửa trên -> chữ dồn xuống nửa dưới, giấy trơn. Không clip ('none'): nền giấy chấm bi.
import sys, os, math, subprocess, json
from lib import *
from lib2 import *
import sfx

RED = (170, 50, 62)
ROOT = os.path.dirname(os.path.abspath(__file__))
_paste = paste
def paste(canvas, im, cx, cy, scale=1.0, angle=0.0, alpha=1.0):
    r = max(im.width, im.height) * max(scale, 0.01) * 0.75
    if cx + r < 0 or cx - r > W or cy + r < 0 or cy - r > H: return
    try: _paste(canvas, im, cx, cy, scale, angle, alpha)
    except ValueError: pass

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

def fit(name, size, text, maxw, minsize=40):
    for s in range(size, minsize - 1, -2):
        f = F(name, s)
        if f.getlength(text) <= maxw: return f
    return F(name, minsize)

def hl_line(d, cx, y, text, hl, font, fg, hl_bg):
    x = cx - font.getlength(text) / 2
    if hl and hl in text:
        x0 = x + font.getlength(text[:text.index(hl)]); w_ = font.getlength(hl)
        asc = font.getmetrics()[0]
        d.rounded_rectangle([x0 - 12, y - asc * 0.80, x0 + w_ + 12, y + asc * 0.18], 16, fill=hl_bg + (255,))
    d.text((cx, y), text, font=font, fill=fg, anchor='ms')

def has_audio(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', path], capture_output=True, text=True)
    return bool(r.stdout.strip())

def run(cfg):
    """cfg: num, src, out, preview, hook=(big, accent, accent_hl, sub), outro=(l1, l2, hl),
    pages=[(label, title, [row_items])], draw_row(dr, item, idx, rowh, clip, rowcolor), row_max_w(items, clip)->font sizes handled by draw_row,
    page_t0=3.0, page_dur=2.5, dur, emojis=(hook, outro), styles=[(color, kind)]"""
    SRC, OUT, PREVIEW = cfg['src'], cfg['out'], cfg.get('preview', False)
    T = dict(ink=BROWN, hookA=CREAM, hookA_fg=BROWN, hookB=LIME, hookB_fg=GREEN, hookB_hl=YELLOW, sub=YELLOW, sub_fg=BROWN,
             label_bg=GREEN, label_fg=YELLOW, label_sh=BROWN, title_fg=BROWN, tape=[YELLOW, LIME, PINK, LIME, PINK], hookA_tape=PINK,
             out=CREAM, out_fg=BROWN, out_hl=LIME, doodle=RED, dots=GREEN, header_rule=None, ransom=False)
    T.update(cfg.get('theme', {}))
    CLIP = SRC != 'none'
    DUR = cfg['dur']; NF = int(DUR * FPS); num = cfg['num']
    HOOK_Y = cfg.get('hook_y', [1450, 1690, 1920]) if CLIP else [1150, 1400, 1650]

    BG = None
    if not CLIP:
        BG = Image.new('RGBA', (W, H), CREAM + (255,)); d = ImageDraw.Draw(BG)
        for y in range(40, H, 48):
            for x in range(40, W, 48): d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=GREEN + (38,))
        BG = grain(BG, 6, num)

    # ---- HOOK ----
    big, acc, acc_hl, sub = cfg['hook']
    HANDLE = pill('@xaykenhdi_', F('Bold', 42), 80, GREEN, LIME, CREAM)
    fA = fit('Black', 132, big, 1100, 70)
    LA, ma = paper_sheet(1200, 210, T['hookA'], num * 100 + 1, amp=10, cells=40)
    if T['ransom']:
        tiles = ransom_word(big, 96, num * 100 + 7); tw = sum((t[0].width - 6) if t else 34 for t in tiles)
        RW = Image.new('RGBA', (tw + 40, 200), (0, 0, 0, 0)); x = 20
        for t in tiles:
            if not t: x += 34; continue
            RW.alpha_composite(t[0], (int(x), int(100 - t[0].height / 2 + t[1] * 0.5))); x += t[0].width - 6
        sc = min(1, 1140 / RW.width); RW = RW.resize((int(RW.width * sc), int(RW.height * sc)), Image.LANCZOS)
        LA.alpha_composite(RW, (int(ma + 600 - RW.width / 2), int(ma + 105 - RW.height / 2)))
    else:
        ImageDraw.Draw(LA).text((ma + 600, ma + 105 + fA.size * 0.36), big, font=fA, fill=T['hookA_fg'], anchor='ms')
    LA.alpha_composite(tape(150, 46, num * 100 + 2, color=T['hookA_tape'], alpha=215), (ma - 30, ma - 22))
    LA = shadowed(rot(LA, -1.5), (7, 12), 10, 0.38)
    fB = fit('tbi', 118, acc, 820, 70)
    LB, mb = paper_sheet(920, 175, T['hookB'], num * 100 + 3, amp=11, cells=40)
    hl_line(ImageDraw.Draw(LB), mb + 460, mb + 128, acc, acc_hl, fB, T['hookB_fg'], T['hookB_hl'])
    LB = shadowed(rot(LB, 1.8), (7, 12), 10, 0.38)
    SUB = rot(washi(sub, fit('ExtraBold', 46, sub, 1150, 32), 100, T['sub'], T['sub_fg'], num * 100 + 5), -1.5)
    E_HOOK = emoji(cfg['emojis'][0], 200); E_OUT = emoji(cfg['emojis'][1], 180)

    # ---- PAGES ----
    PW = 1340 if CLIP else 1300; HEAD = 118 if CLIP else 150
    ROWH = cfg.get('rowh', (82, 112))[0 if CLIP else 1]
    STYLE = cfg.get('styles', [(CREAM, 'grid'), (PINK, 'plain'), (LIME, 'grid'), (YELLOW, 'plain'), (CREAM, 'lined')])
    if CLIP: STYLE = [(c, 'plain') for c, _ in STYLE]
    TAPE = T['tape']
    fHead = F('ExtraBold', 40)
    PAGES = []
    for pi, (label, title, items) in enumerate(cfg['pages']):
        col, kind = STYLE[pi % len(STYLE)]
        ph = HEAD + len(items) * ROWH + 30
        S, m = paper_sheet(PW, ph, col, num * 100 + 10 + pi * 11, kind=kind, amp=10, cells=60)
        d = ImageDraw.Draw(S); x0 = m + 60; hy = -14 if CLIP else 0
        fL = fit('Black', 44, label, 200, 28)
        d.rectangle([x0 + 5, m + 40 + hy, x0 + 235, m + 112 + hy], fill=T['label_sh'] + (255,))
        d.rectangle([x0, m + 34 + hy, x0 + 230, m + 106 + hy], fill=T['label_bg'] + (255,))
        d.text((x0 + 115, m + 71 + hy), label, font=fL, fill=T['label_fg'], anchor='mm')
        if T['header_rule']:
            for k_, wd in ((0, 5), (12, 2)): d.line([(m + 40, m + HEAD - 10 + k_), (m + PW - 40, m + HEAD - 10 + k_)], fill=T['header_rule'] + (255,), width=wd)
        fT = fit('ExtraBold', 40, title.upper(), PW - 380, 26); x = x0 + 262
        for ch in title.upper(): d.text((x, m + 88 + hy), ch, font=fT, fill=T['title_fg'], anchor='ls'); x += fT.getlength(ch) + 3
        S.alpha_composite(tape(180, 52, num * 100 + 50 + pi, color=TAPE[pi % 5], alpha=215), ((m + PW - 170) if pi % 2 == 0 else (m - 40), m - 26))
        ctx = cfg['prepare'](items, CLIP, PW) if 'prepare' in cfg else None
        rows = []
        for j, it in enumerate(items):
            R = Image.new('RGBA', (PW - 40, ROWH), (0, 0, 0, 0)); dr = ImageDraw.Draw(R)
            c = T['badges'][j % len(T['badges'])] if 'badges' in T else ([PINK, LIME][j % 2] if col not in (PINK, LIME) else CREAM)
            cfg['draw_row'](R, dr, it, j, ROWH, CLIP, c, ctx)
            if j < len(items) - 1:
                for xx in range(130, PW - 120, 14): dr.ellipse([xx, ROWH - 5, xx + 4, ROWH - 1], fill=T['dots'] + (55,))
            rows.append((R, m + 20, m + HEAD + j * ROWH))
        PAGES.append((S, m, rows, ph))
    NP = len(PAGES)
    T_PG = [cfg.get('page_t0', 3.0) + i * cfg.get('page_dur', 2.5) for i in range(NP)]
    T_O = T_PG[-1] + cfg.get('page_dur', 2.5); T_PG_END = T_O - 0.15
    PAGE_ANG = [-0.9, 0.8, -0.7, 0.9, -0.8, 0.7]
    def page_cy(ph):  # có clip: mép dưới trang cố định ~2200 (chừa UI), không lên quá 1180 (mặt)
        if CLIP and cfg.get('page_low'): return 2200 - ph / 2
        return (min(2200 - ph / 2, max(1180 + ph / 2, 1700))) if CLIP else 1230

    # ---- OUTRO ----
    l1, l2, ohl = cfg['outro']
    fO = fit('tbi', 100, max(l1, l2, key=len), 1080, 60)
    O, om = paper_sheet(1180, 300, T['out'], num * 100 + 80, amp=12, cells=60)
    d = ImageDraw.Draw(O)
    d.text((om + 590, om + 120), l1, font=fO, fill=T['out_fg'], anchor='ms')
    hl_line(d, om + 590, om + 240, l2, ohl, fO, T['out_fg'], T['out_hl'])
    O.alpha_composite(tape(150, 46, num * 100 + 81, color=YELLOW, alpha=215), (om + 1050, om - 22))
    O = shadowed(rot(O, -1.5), (8, 13), 11, 0.38)

    ST = {k: load_seq(k, s) for k, s in [('sparkle', 150), ('star', 140), ('pencil', 230)]}
    def sf(name, t, speed=0.5, ph=0.0): return ST[name][int(((t * speed + ph) % 1) * 24) % 24]
    TW = {s: sparkle2d(s, c, BROWN) for s, c in [(54, YELLOW), (44, LIME), (38, CREAM)]}
    D_STAR = doodle('star', 110, T['doodle'], num * 100 + 90); D_HEART = doodle('heart', 100, T['doodle'], num * 100 + 91)
    T_HOOK_OUT = T_PG[0] - 0.28; RSTEP = cfg.get('rstep', 0.07)

    def frame(t):
        cv = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        paste(cv, HANDLE, 70 + HANDLE.width / 2, 175, 1, 0, 1)
        paste(cv, TW[38], 70 + HANDLE.width + 12, 150, 0.8 + 0.2 * math.sin(t * 6), t * 50, 1)
        if t < T_HOOK_OUT + 0.35:
            # HOOK: hiện đủ ngay khung 0, chỉ "thở" nhẹ
            out = ease_in_cubic(prog(t, T_HOOK_OUT, 0.3)); ha = 1 - out; up = -260 * out
            br = 1 + 0.015 * math.sin(t * 3.2)
            paste(cv, LA, 720, HOOK_Y[0] + up, br, 0, ha)
            paste(cv, LB, 760, HOOK_Y[1] + up, 1 + 0.02 * math.sin(t * 3.2 + 1), 0, ha)
            paste(cv, E_HOOK, 1250, HOOK_Y[0] - 250 + up + 8 * math.sin(t * 4), 1, 6 * math.sin(t * 3), ha)
            paste(cv, sf('pencil', t, 0.5), 200, HOOK_Y[1] + 120 + up, 0.9, 0, ha)
            paste(cv, SUB, 720, HOOK_Y[2] - up * 0.8, 1, 0, ha)
            paste(cv, sf('sparkle', t, 0.45), 1260, HOOK_Y[2] - 90, 0.8 * ha, 0, 1)
        for pi in range(NP):
            t0 = T_PG[pi]; t1 = T_PG[pi + 1] if pi < NP - 1 else T_PG_END
            if not (t0 <= t < t1 + 0.35): continue
            S, m, rows, ph = PAGES[pi]; L = S.copy(); cy = page_cy(ph)
            for j, (R, rx, ry) in enumerate(rows):
                q = prog(t, t0 + 0.22 + j * RSTEP, 0.2)
                if q <= 0: continue
                e = ease_out_cubic(q); RR = R if q >= 1 else R.copy()
                if q < 1: RR.putalpha(R.split()[3].point(lambda v, e=e: int(v * e)))
                L.alpha_composite(RR, (rx + int(-40 * (1 - e)), ry))
            pin = ease_out_cubic(prog(t, t0, 0.33)); pout = ease_in_cubic(prog(t, t1 - 0.05, 0.33))
            s_ = -1 if pi % 2 == 0 else 1
            x = 720 + (-s_) * 1400 * (1 - pin) + s_ * 1450 * pout
            ang = PAGE_ANG[pi % 6] + (-s_) * 10 * (1 - pin) + s_ * 18 * pout
            paste(cv, shadowed(L, (8, 14), 12, 0.38), x, cy, 1, ang, 1)
            pk = ease_out_back(prog(t, t0 + 0.3, 0.3)) * (1 - pout)
            paste(cv, [D_STAR, D_HEART][pi % 2], x + 560, cy - ph / 2 - 10, pk, 8 * math.sin(t * 3), 1)
            paste(cv, sf('star', t, 0.4), x + (-540 if pi % 2 == 0 else 540), cy + ph / 2 + 30, pk * 0.8, 0, 1)
        if t >= T_O:
            p = prog(t, T_O, 0.38); oy = 1700 if CLIP else 1250
            paste(cv, O, 720, oy, 0.45 + 0.55 * ease_out_back(p), -8 * (1 - ease_out_cubic(p)), min(1, p * 3))
            pk = ease_out_back(prog(t, T_O + 0.25, 0.35))
            paste(cv, E_OUT, 1210, oy - 230 + 8 * math.sin(t * 4), pk, 8 * math.sin(t * 5), 1)
            paste(cv, sf('sparkle', t, 0.45), 210, oy + 230, pk * 0.8, 0, 1)
            paste(cv, TW[54], 1180, oy + 250, pk * (0.8 + 0.2 * math.sin(t * 7)), t * 40, 1)
        return cv

    CF = {}
    def with_bg(t):
        if BG is not None: im = BG.copy()
        else:
            k = round(min(t, 11.5), 2)
            if k not in CF:
                raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(k), '-i', SRC, '-frames:v', '1', '-vf', 'scale=1440:2560', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-'], capture_output=True).stdout
                CF[k] = Image.frombytes('RGBA', (W, H), raw)
            im = CF[k].copy()
        im.alpha_composite(frame(t)); return im

    os.makedirs(f'{ROOT}/work', exist_ok=True)
    if PREVIEW:
        ts_ = [0.0, T_PG[0] + 1.5, T_PG[NP // 2] + 1.5, T_PG[-1] + 1.5, DUR - 0.5]
        ims = [with_bg(ts).convert('RGB').resize((432, 768)) for ts in ts_]
        s = Image.new('RGB', (432 * len(ims), 768)); [s.paste(im, (i * 432, 0)) for i, im in enumerate(ims)]
        s.save(f'{ROOT}/work/prev{num}.png')
        p = PAGES[1]; cy = page_cy(p[3])
        with_bg(T_PG[1] + 1.5).convert('RGB').crop((0, int(cy - p[3] / 2 - 60), 1440, int(cy + p[3] / 2 + 60))).resize((720, int((p[3] + 120) / 2))).save(f'{ROOT}/work/prev{num}_p.png')
        return

    ev = [(0.0, sfx.rip(0.3, 0.45)), (0.05, sfx.pop(600, 180, 0.15, 0.5)), (0.4, sfx.tick(1500, 0.3)),
          (T_HOOK_OUT - 0.05, sfx.whoosh(0.4, 0.38))]
    for pi, tp in enumerate(T_PG):
        if pi: ev.append((tp - 0.08, sfx.rip(0.4, 0.45)))
        ev.append((tp, sfx.whoosh(0.3, 0.3)))
        for j in range(0, len(PAGES[pi][2]), 2): ev.append((tp + 0.22 + j * RSTEP, sfx.pop(850 + j * 60 + pi * 40, 330, 0.09, 0.32)))
    ev += [(T_PG_END - 0.05, sfx.whoosh(0.4, 0.38, up=False)), (T_O, sfx.rip(0.3, 0.45)), (T_O + 0.1, sfx.pop(650, 200, 0.16, 0.5)),
           (T_O + 0.3, sfx.ding(1318, 1.2, 0.24)), (T_O + 0.6, sfx.sparkle(0.7, 0.2))]
    WAV = f'{ROOT}/work/sfx{num}.wav'
    sfx.build(ev, DUR, WAV)
    enc = ['-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(DUR), OUT]
    if not CLIP:
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-', '-i', WAV, '-map', '0:v', '-map', '1:a'] + enc
        get = with_bg
    else:
        aud = ('[0:a]aresample=48000,volume=0.75,apad[a0];[1:a]volume=1.0[a1];[a1][a0]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.95[a]'
               if has_audio(SRC) else '[1:a]anull[a]')
        cmd = ['ffmpeg', '-v', 'error', '-y', '-i', SRC, '-i', WAV, '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
               '-filter_complex',
               '[0:v]scale=1440:2560:force_original_aspect_ratio=increase,crop=1440:2560,setsar=1,fps=30,tpad=stop_mode=clone:stop_duration=30,format=yuv420p[b];'
               '[b][2:v]overlay=0:0:format=auto:eof_action=pass,format=yuv420p[v];' + aud,
               '-map', '[v]', '-map', '[a]'] + enc
        get = frame
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(NF): pr.stdin.write(get(n / FPS).tobytes())
    pr.stdin.close(); pr.wait(); print('done', pr.returncode)
