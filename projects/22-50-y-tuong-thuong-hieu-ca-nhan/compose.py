# Video 22 · 50 ý tưởng content thương hiệu cá nhân — bộ màu "Cà phê sữa"
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
KRAFT = (204, 168, 128); MILK = (246, 237, 221); ESP = (62, 40, 28); TERRA = (217, 119, 59)
PAGES = parse_pages(MD)
def prepare(items, clip, pw): return fitf('SemiBold', items, pw - 230, 36 if clip else 46, 26)
def draw_row(R, dr, it, j, rowh, clip, c, f):
    n, s = it; cy = rowh / 2
    # tem bưu chính: viền răng cưa
    x0, y0, x1, y1 = 40, cy - 30, 112, cy + 30
    dr.rectangle([x0, y0, x1, y1], fill=MILK + (255,))
    for xx in range(x0, x1 + 1, 9): dr.ellipse([xx - 3, y0 - 3, xx + 3, y0 + 3], fill=(0, 0, 0, 0)); dr.ellipse([xx - 3, y1 - 3, xx + 3, y1 + 3], fill=(0, 0, 0, 0))
    dr.rectangle([x0 + 6, y0 + 6, x1 - 6, y1 - 6], outline=TERRA + (255,), width=2)
    dr.text(((x0 + x1) / 2, cy), str(n), font=F('Black', 26), fill=ESP, anchor='mm')
    blank = s.split('___')
    x = 136; y = cy + f.size * 0.36
    for k, part in enumerate(blank):
        if k: dr.line([(x + 6, y + 4), (x + 70, y + 4)], fill=TERRA + (255,), width=4); x += 76
        if part: dr.text((x, y), part, font=f, fill=ESP, anchor='ls'); x += f.getlength(part)
run(dict(num=22, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=18.0, page_low=True, hook_y=[1450, 1790, 2010], big_size=150,
         theme=dict(hookA=KRAFT, hookA_fg=ESP, hookA_tape=MILK, hookB=MILK, hookB_fg=ESP, hookB_hl=TERRA, sub=TERRA, sub_fg=MILK,
                    label_bg=ESP, label_fg=MILK, label_sh=TERRA, title_fg=ESP, tape=[MILK, TERRA], out=MILK, out_fg=ESP, out_hl=(240, 190, 140),
                    doodle=TERRA, dots=ESP),
         styles=[(MILK, 'plain'), (KRAFT, 'plain')],
         hook=('50 Ý TƯỞNG\nCONTENT', 'xây thương hiệu cá nhân', 'thương hiệu', 'Chưa có sản phẩm vẫn đăng đều mỗi ngày'),
         outro=('Không cần bán gì.', 'Cần người ta nhớ bạn.', 'nhớ bạn'), emojis=('hot-beverage', 'bookmark'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
