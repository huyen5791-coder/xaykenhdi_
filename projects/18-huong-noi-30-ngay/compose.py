# Video 18 · Người hướng nội xây kênh: 30 ngày, 30 video
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
from listvid import *

md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
WEEKS = re.findall(r'Tờ \d+: Tuần (\d+) · ([^(\n]+?) \(ngày (\d+)–(\d+)\)', md)
DAYS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- Ngày (\d+) → (.+)$', md)}
assert len(WEEKS) == 4 and len(DAYS) == 30

def prepare(items, clip, pw):
    for sz in (range(44, 27, -1) if clip else range(48, 33, -1)):
        f = F('SemiBold', sz)
        if max(f.getlength(s) for _, s in items) <= pw - 260: return f
    return f
def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; cy = rowh / 2; rr = 32 if clip else 40
    dr.rounded_rectangle([76 - rr - 8, cy - rr, 76 + rr + 8, cy + rr], 14, fill=c + (255,), outline=BROWN + (255,), width=4)
    dr.text((76, cy), f'N{n}', font=F('Black', 26 if clip else 30), fill=BROWN, anchor='mm')
    dr.text((150, cy + ctx.size * 0.36), s, font=ctx, fill=BROWN, anchor='ls')

run(dict(num=18, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=17.5, page_dur=3.0, rstep=0.09, rowh=(94, 118),
         hook=('NGƯỜI HƯỚNG NỘI XÂY KÊNH', '30 ngày · 30 video', '30 video', 'Không cần nói 1 câu, không cần lộ mặt'),
         outro=('Không cần nói hay,', 'chỉ cần đăng đều', 'đăng đều'), emojis=('pencil', 'bookmark'),
         styles=[(CREAM, 'grid'), (PINK, 'plain'), (LIME, 'grid'), (YELLOW, 'plain')],
         pages=[(f'TUẦN {w}', ti, [(n, DAYS[n]) for n in range(int(a), int(b) + 1)]) for w, ti, a, b in WEEKS],
         prepare=prepare, draw_row=draw_row))
