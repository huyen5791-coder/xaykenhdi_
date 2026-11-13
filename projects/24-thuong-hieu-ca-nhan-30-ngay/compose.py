# Video 24 · Thương hiệu cá nhân từ 0 trong 30 ngày — bộ màu "Cam đào"
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
PEACH = (255, 211, 182); WH = (255, 252, 247); BRN = (90, 55, 40); BLUE = (58, 110, 165)
PAGES = parse_pages(MD, 'tuan')
def prepare(items, clip, pw): return fitf('SemiBold', items, pw - 300, 42 if clip else 50, 26)
def draw_row(R, dr, it, j, rowh, clip, c, f):
    n, s = it; cy = rowh / 2
    # ô lịch: khoen tròn + số ngày
    dr.rounded_rectangle([34, cy - 34, 124, cy + 36], 10, fill=WH + (255,), outline=BLUE + (255,), width=3)
    dr.rectangle([34, cy - 34, 124, cy - 14], fill=BLUE + (255,))
    for xx in (58, 100): dr.ellipse([xx - 5, cy - 42, xx + 5, cy - 30], fill=BRN + (255,))
    dr.text((79, cy + 12), str(n), font=F('Black', 30), fill=BLUE, anchor='mm')
    dr.text((150, cy + f.size * 0.36), s, font=f, fill=BRN, anchor='ls')
    tx = R.width - 70; dr.line([(tx - 18, cy), (tx - 6, cy + 13), (tx + 18, cy - 15)], fill=BLUE + (255,), width=6, joint='curve')
run(dict(num=24, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=17.5, page_dur=3.0, rstep=0.09, rowh=(94, 118), page_low=True, hook_y=[1450, 1790, 2010], big_size=140,
         theme=dict(hookA=WH, hookA_fg=BRN, hookA_tape=BLUE, hookB=BLUE, hookB_fg=WH, hookB_hl=(240, 150, 110), sub=PEACH, sub_fg=BRN,
                    label_bg=BLUE, label_fg=WH, label_sh=BRN, title_fg=BRN, tape=[BLUE, PEACH], out=WH, out_fg=BRN, out_hl=PEACH,
                    doodle=BLUE, dots=BRN),
         styles=[(PEACH, 'plain'), (WH, 'plain')],
         hook=('THƯƠNG HIỆU\nCÁ NHÂN TỪ 0', '30 ngày · mỗi ngày 1 việc', '1 việc', 'Làm theo đúng thứ tự này là xong'),
         outro=('Người ta nhớ người', 'xuất hiện đều', 'xuất hiện đều'), emojis=('spiral-calendar', 'check-mark-button'),
         pages=PAGES, prepare=prepare, draw_row=draw_row))
