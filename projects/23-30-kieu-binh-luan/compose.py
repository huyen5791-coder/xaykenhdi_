# Video 23 · 30 kiểu bình luận biến thành video — bộ màu "Đêm xanh"
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from listvid import *
MD = open(os.path.join(HERE, "noi-dung.md"), encoding="utf-8").read()
def fitf(name, items, maxw, hi, lo):
    for sz in range(hi, lo - 1, -1):
        f = F(name, sz)
        if max(f.getlength(s) for _, s in items) <= maxw: return f
    return F(name, lo)
NAVY = (31, 42, 68); NAVY2 = (44, 58, 92); CREAM_ = (250, 244, 228); SUN = (255, 200, 70); WH = (255, 255, 255)
PAGES = parse_pages(MD)
def prepare(items, clip, pw):
    fa = F('SemiBold', 28 if clip else 34); fb = F('Bold', 30 if clip else 36)
    while max(fa.getlength(s.split('→')[0].strip()) for _, s in items) > 600 and fa.size > 20: fa = F('SemiBold', fa.size - 1)
    while max(fb.getlength(s.split('→')[1].strip()) for _, s in items) > pw - 820 and fb.size > 20: fb = F('Bold', fb.size - 1)
    return fa, fb
def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; fa, fb = ctx; a, b = [x.strip() for x in s.split('→', 1)]; cy = rowh / 2
    dr.text((62, cy), f'{n:02d}', font=F('Black', 30), fill=SUN, anchor='mm')
    w = fa.getlength(a) + 40
    dr.rounded_rectangle([108, cy - 28, 108 + w, cy + 26], 22, fill=WH + (255,))
    dr.polygon([(124, cy + 20), (118, cy + 38), (140, cy + 24)], fill=WH + (255,))
    dr.text((128, cy + fa.size * 0.36), a, font=fa, fill=NAVY, anchor='ls')
    xb = 108 + max(w, 620) + 20
    dr.text((xb, cy + fb.size * 0.36), '→ ', font=fb, fill=SUN, anchor='ls')
    dr.text((xb + fb.getlength('→ '), cy + fb.size * 0.36), b, font=fb, fill=CREAM_, anchor='ls')
run(dict(num=23, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=14.5, page_dur=3.0, rstep=0.09, page_low=True, hook_y=[1450, 1790, 2010], big_size=150,
         theme=dict(hookA=NAVY, hookA_fg=CREAM_, hookA_tape=SUN, hookB=SUN, hookB_fg=NAVY, hookB_hl=WH, sub=WH, sub_fg=NAVY,
                    label_bg=SUN, label_fg=NAVY, label_sh=(10, 16, 30), title_fg=CREAM_, tape=[SUN, WH, SUN], out=NAVY, out_fg=CREAM_, out_hl=(120, 100, 30),
                    doodle=SUN, dots=CREAM_),
         styles=[(NAVY, 'plain'), (NAVY2, 'plain')],
         hook=('BÍ Ý TƯỞNG\nCONTENT?', 'mở phần bình luận ra', 'bình luận', '30 kiểu bình luận biến thành video ngay'),
         outro=('Người xem đã', 'viết sẵn kịch bản cho bạn', 'viết sẵn'), emojis=('speech-balloon', 'bookmark'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
