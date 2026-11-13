# Video 27 · Thuật toán tìm kiếm: 10 chỗ đặt từ khoá — bộ màu "Hồng đất"
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
ROSE = (201, 123, 107); DGR = (47, 74, 58); CRM = (252, 244, 230); YL = (255, 214, 90)
PAGES = parse_pages(MD)
def prepare(items, clip, pw): return fitf('Bold', items, pw - 260, 48 if clip else 56, 28)
def draw_row(R, dr, it, j, rowh, clip, c, f):
    n, s = it; cy = rowh / 2
    dr.ellipse([40, cy - 28, 96, cy + 28], outline=YL + (255,), width=7)
    dr.line([(90, cy + 22), (112, cy + 44)], fill=YL + (255,), width=9)
    dr.text((68, cy), str(n), font=F('Black', 26), fill=CRM, anchor='mm')
    dr.text((140, cy + f.size * 0.36), s, font=f, fill=CRM, anchor='ls')
run(dict(num=27, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=11.5, page_dur=3.0, rstep=0.12, rowh=(112, 134), page_low=True, hook_y=[1450, 1790, 2010], big_size=150,
         theme=dict(hookA=DGR, hookA_fg=CRM, hookA_tape=ROSE, hookB=ROSE, hookB_fg=CRM, hookB_hl=DGR, sub=YL, sub_fg=DGR,
                    label_bg=YL, label_fg=DGR, label_sh=(30, 45, 36), title_fg=CRM, tape=[YL, CRM], out=CRM, out_fg=DGR, out_hl=YL,
                    doodle=YL, dots=CRM),
         styles=[(ROSE, 'plain'), (DGR, 'plain')],
         hook=('THUẬT TOÁN\nTÌM KIẾM', '10 chỗ đặt từ khoá', 'từ khoá', 'Để video hiện khi người ta gõ tìm'),
         outro=('Người ta gõ chữ gì,', 'bạn nói đúng chữ đó', 'đúng chữ đó'), emojis=('magnifying-glass-tilted-left', 'bookmark'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
