# Video 25 · 12 thứ trên trang cá nhân — bộ màu "Xanh dương cổ điển" (thẻ thư viện)
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
CARD = (250, 250, 244); INKB = (28, 48, 92); BL = (80, 120, 190); YL = (255, 214, 64); STAMP = (190, 45, 55)
PAGES = parse_pages(MD)
def prepare(items, clip, pw): return fitf('Bold', items, pw - 330, 46 if clip else 54, 28)
def draw_row(R, dr, it, j, rowh, clip, c, f):
    n, s = it; cy = rowh / 2
    dr.rectangle([36, cy - 32, 106, cy + 32], fill=INKB + (255,))
    dr.text((71, cy), str(n), font=F('Black', 32), fill=YL, anchor='mm')
    dr.text((136, cy + f.size * 0.36), s, font=f, fill=INKB, anchor='ls')
    bx = R.width - 110
    dr.rectangle([bx, cy - 24, bx + 48, cy + 24], outline=INKB + (255,), width=4)
    dr.line([(bx + 8, cy), (bx + 20, cy + 14), (bx + 44, cy - 18)], fill=STAMP + (255,), width=6, joint='curve')
run(dict(num=25, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=11.5, page_dur=3.0, rstep=0.12, rowh=(112, 134), page_low=True, hook_y=[1450, 1790, 2010], big_size=140,
         theme=dict(hookA=CARD, hookA_fg=INKB, hookA_tape=BL, hookB=INKB, hookB_fg=CARD, hookB_hl=STAMP, sub=YL, sub_fg=INKB,
                    label_bg=INKB, label_fg=YL, label_sh=BL, title_fg=INKB, tape=[YL, BL], out=CARD, out_fg=INKB, out_hl=YL,
                    doodle=STAMP, dots=BL, keep_kind=True),
         styles=[(CARD, 'grid'), (CARD, 'grid')],
         hook=('12 THỨ TRÊN\nTRANG CÁ NHÂN', 'người lạ bấm theo dõi', 'theo dõi', 'Sửa xong trong 1 buổi'),
         outro=('Người ta', 'xem trang trước, rồi mới theo dõi', 'xem trang'), emojis=('bust-in-silhouette', 'check-mark-button'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
