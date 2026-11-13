# Video 26 · Bị bóp view? 20 lỗi cần kiểm tra — bộ màu "Băng cảnh báo"
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
HZ = (255, 210, 0); BK = (24, 24, 24); RD = (210, 40, 40); WH = (255, 255, 250); HZ2 = (255, 236, 150)
PAGES = parse_pages(MD)
def prepare(items, clip, pw): return fitf('Bold', items, pw - 260, 46 if clip else 54, 28)
def draw_row(R, dr, it, j, rowh, clip, c, f):
    n, s = it; cy = rowh / 2
    dr.rectangle([40, cy - 30, 100, cy + 30], fill=WH + (255,), outline=BK + (255,), width=5)
    dr.line([(52, cy - 18), (88, cy + 18)], fill=RD + (255,), width=8); dr.line([(52, cy + 18), (88, cy - 18)], fill=RD + (255,), width=8)
    dr.text((126, cy + f.size * 0.36), f'{n}. ' + s, font=f, fill=BK, anchor='ls')
run(dict(num=26, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=16.7, page_dur=2.8, rstep=0.12, rowh=(112, 134), page_low=True, hook_y=[1450, 1790, 2010], big_size=160,
         theme=dict(hookA=HZ, hookA_fg=BK, hookA_tape=BK, hookB=BK, hookB_fg=HZ, hookB_hl=RD, sub=WH, sub_fg=BK,
                    label_bg=BK, label_fg=HZ, label_sh=RD, title_fg=BK, tape=[BK, BK], header_rule=BK, out=HZ, out_fg=BK, out_hl=WH,
                    doodle=RD, dots=BK),
         styles=[(HZ, 'plain'), (HZ2, 'plain')],
         hook=('VIDEO BỊ\nBÓP VIEW?', 'đừng trách thuật toán vội', 'thuật toán', '20 lỗi kiểm tra trong 5 phút'),
         outro=('Đừng sửa tất cả cùng lúc.', 'Sửa từng lỗi một', 'từng lỗi một'), emojis=('warning', 'check-mark-button'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
