# Video 16 · 50 câu mở đầu copy dùng ngay
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]    — nội dung đọc từ noi-dung.md
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
from listvid import *

md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 5 and len(ITEMS) == 50

def blank_w(s, f, slot): return sum(f.getlength(p) for p in s.split('___')) + slot * s.count('___')
def prepare(items, clip, pw):
    slot = 76 if clip else 96
    for sz in (range(36, 27, -1) if clip else range(46, 33, -1)):
        f = F('SemiBold', sz)
        if max(blank_w(s, f, slot) for _, s in items) <= pw - 230: return f, slot
    return f, slot
def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; f, slot = ctx; cy = rowh / 2; rr = 28 if clip else 36
    dr.ellipse([76 - rr, cy - rr, 76 + rr, cy + rr], fill=c + (255,), outline=BROWN + (255,), width=4)
    dr.text((76, cy), str(n), font=F('Black', 26 if clip else 34), fill=BROWN, anchor='mm')
    x = 130; y = cy + f.size * 0.36; asc = f.getmetrics()[0]
    for k, part in enumerate(s.split('___')):
        if k:
            dr.rounded_rectangle([x + 4, y - asc * 0.70, x + slot - 4, y + 8], 8, fill=YELLOW + (255,))
            dr.line([(x + 10, y + 4), (x + slot - 10, y + 4)], fill=BROWN + (255,), width=4); x += slot
        if part: dr.text((x, y), part, font=f, fill=BROWN, anchor='ls'); x += f.getlength(part)

run(dict(num=16, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=18.0,
         hook=('50 CÂU MỞ ĐẦU', 'copy dùng ngay', 'copy', 'Thay tên ngách của bạn vào chỗ ___ là xong'),
         outro=('Lưu lại,', 'mỗi ngày dùng 1 câu', 'mỗi ngày'), emojis=('writing-hand', 'bookmark'),
         pages=[(f'{int(a):02d}–{int(b):02d}', g, [(n, ITEMS[n]) for n in range(int(a), int(b) + 1)]) for g, a, b in GROUPS],
         prepare=prepare, draw_row=draw_row))
