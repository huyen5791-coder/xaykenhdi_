# Video 17 · 50 phông chữ Việt hoá trong canva
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]
# Cần phông ở work/fonts17/<số>.ttf (tải từ Google Fonts; đã kiểm đủ dấu tiếng Việt bằng fontTools).
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT_ = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, ROOT_)
from listvid import *

md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 5 and len(ITEMS) == 50
SAMPLE = 'Xây kênh từ 0'
def ff(n, size): return ImageFont.truetype(f'{ROOT_}/work/fonts17/{n}.ttf', size)

def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, name = it; cy = rowh / 2; rr = 28 if clip else 36
    dr.ellipse([76 - rr, cy - rr, 76 + rr, cy + rr], fill=c + (255,), outline=BROWN + (255,), width=4)
    dr.text((76, cy), str(n), font=F('Black', 26 if clip else 34), fill=BROWN, anchor='mm')
    def sized(text, target_h, maxw):
        f = ff(n, 60); bb = dr.textbbox((0, 0), 'xe', font=f, anchor='ls'); h = max(1, bb[3] - bb[1])
        f = ff(n, max(16, int(60 * target_h / h)))
        while f.getlength(text) > maxw and f.size > 16: f = ff(n, f.size - 2)
        return f
    fn = sized(name, rowh * 0.27, 600)
    dr.text((130, cy + rowh * 0.2), name, font=fn, fill=BROWN, anchor='ls')
    fs = sized(SAMPLE, rowh * 0.21, 480)
    dr.text((R.width - 50, cy + rowh * 0.18), SAMPLE, font=fs, fill=GREEN, anchor='rs')

run(dict(num=17, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=18.0,
         hook=('50 PHÔNG CHỮ VIỆT HOÁ', 'nhìn sang ngay', 'sang', 'Có sẵn trong canva · không lỗi dấu'),
         outro=('Tiêu đề 1 phông, nội dung 1 phông', 'đừng dùng quá 2', 'quá 2'), emojis=('memo', 'bookmark'),
         pages=[(f'{int(a):02d}–{int(b):02d}', g, [(n, ITEMS[n]) for n in range(int(a), int(b) + 1)]) for g, a, b in GROUPS],
         draw_row=draw_row))
