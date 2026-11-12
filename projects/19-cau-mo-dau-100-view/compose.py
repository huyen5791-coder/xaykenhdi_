# Video 19 · Câu mở đầu 100 view và 1 triệu view — bộ màu "Báo cũ đen trắng"
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
from listvid import *

INK = (30, 28, 26); NEWS = (236, 232, 222); NEWS2 = (226, 221, 208); RED_ = (170, 50, 62); YEL = (255, 228, 92); GREY = (92, 88, 80)
md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 4 and len(ITEMS) == 20

def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; old, new = [x.strip() for x in s.split('→', 1)]
    rr = 30 if clip else 36; cy = rowh / 2
    dr.ellipse([70 - rr, cy - rr, 70 + rr, cy + rr], fill=INK + (255,))
    dr.text((70, cy), str(n), font=F('Black', 28 if clip else 34), fill=NEWS, anchor='mm')
    fo = F('Medium', 30 if clip else 36); fn = F('ExtraBold', 38 if clip else 46)
    while fn.getlength('→ ' + new) > R.width - 180 and fn.size > 26: fn = F('ExtraBold', fn.size - 2)
    while fo.getlength(old) > R.width - 180 and fo.size > 20: fo = F('Medium', fo.size - 2)
    y1 = rowh * 0.40; y2 = rowh * 0.84; x = 128
    dr.text((x, y1), old, font=fo, fill=GREY, anchor='ls')
    w = fo.getlength(old); r_ = random.Random(n)
    pts = [(x - 6 + k * (w + 12) / 12, y1 - fo.size * 0.32 + r_.uniform(-3, 3)) for k in range(13)]
    dr.line(pts, fill=RED_ + (230,), width=3, joint='curve')
    asc = fn.getmetrics()[0]; wa = fn.getlength('→ ')
    dr.rectangle([x + wa - 6, y2 - asc * 0.78, x + fn.getlength('→ ' + new) + 8, y2 + asc * 0.16], fill=YEL + (255,))
    dr.text((x, y2), '→ ', font=fn, fill=RED_, anchor='ls'); dr.text((x + wa, y2), new, font=fn, fill=INK, anchor='ls')

run(dict(num=19, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=16.7, page_dur=2.8, rstep=0.1,
         rowh=(132, 150), page_low=True, hook_y=[1530, 1830, 2030], big_size=170,
         theme=dict(hookA=NEWS, hookA_fg=INK, hookA_tape=RED_, hookB=INK, hookB_fg=NEWS, hookB_hl=RED_, sub=YEL, sub_fg=INK,
                    label_bg=INK, label_fg=YEL, label_sh=RED_, title_fg=INK, tape=[(240, 236, 226)] * 4, header_rule=INK,
                    out=NEWS, out_fg=INK, out_hl=YEL, doodle=RED_, dots=INK, badges=[INK]),
         styles=[(NEWS, 'plain'), (NEWS2, 'plain')],
         hook=('CÂU MỞ ĐẦU\n100 VIEW', 'và câu 1 triệu view', '1 triệu view', '20 cặp sửa trước → sau (ví dụ minh hoạ)'),
         outro=('Đừng chào.', 'Nói ngay điều người xem cần', 'Nói ngay'), emojis=('megaphone', 'memo'),
         pages=[(f'{int(a):02d}–{int(b):02d}', g, [(n, ITEMS[n]) for n in range(int(a), int(b) + 1)]) for g, a, b in GROUPS],
         draw_row=draw_row))
