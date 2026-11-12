# Video 20 · 20 cặp phông chữ Việt hoá — bộ màu "Bạc hà san hô"
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]   — phông lấy từ work/fonts17 (đã kiểm dấu ở video 17)
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT_ = os.path.abspath(os.path.join(HERE, '..', '..')); sys.path.insert(0, ROOT_)
from listvid import *

MINT = (191, 232, 214); WHITE_ = (255, 255, 255); DG = (47, 74, 58); CORAL = (255, 127, 110); MINT2 = (222, 244, 234)
md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 4 and len(ITEMS) == 20
md17 = open(f'{ROOT_}/projects/17-50-phong-chu-viet-hoa/noi-dung.md', encoding='utf-8').read()
FILE = {t.strip(): int(n) for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md17)}
def ff(name, size): return ImageFont.truetype(f'{ROOT_}/work/fonts17/{FILE[name]}.ttf', size)
def sized(dr, name, text, target_h, maxw):
    f = ff(name, 60); bb = dr.textbbox((0, 0), 'xe', font=f, anchor='ls'); h = max(1, bb[3] - bb[1])
    f = ff(name, max(16, int(60 * target_h / h)))
    while f.getlength(text) > maxw and f.size > 16: f = ff(name, f.size - 2)
    return f

def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; a, b = [x.strip() for x in s.split('+')]
    # thẻ mẫu màu sơn: dải màu san hô bên trái
    dr.rounded_rectangle([30, 10, 112, rowh - 14], 12, fill=(CORAL if j % 2 == 0 else DG) + (255,))
    dr.text((71, rowh / 2 - 2), str(n), font=F('Black', 30 if clip else 36), fill=WHITE_, anchor='mm')
    fa = sized(dr, a, a, rowh * 0.20, 560); fb = sized(dr, b, b, rowh * 0.13, 560)
    dr.text((140, rowh * 0.48), a, font=fa, fill=DG, anchor='ls')
    dr.text((140, rowh * 0.84), '+ ', font=F('Bold', int(rowh * 0.2)), fill=CORAL, anchor='ls')
    dr.text((140 + F('Bold', int(rowh * 0.2)).getlength('+ '), rowh * 0.84), b, font=fb, fill=DG, anchor='ls')
    fs = sized(dr, a, 'Xây kênh từ 0', rowh * 0.17, 420); fs2 = sized(dr, b, 'chia sẻ mỗi ngày', rowh * 0.11, 420)
    dr.text((R.width - 50, rowh * 0.48), 'Xây kênh từ 0', font=fs, fill=DG, anchor='rs')
    dr.text((R.width - 50, rowh * 0.84), 'chia sẻ mỗi ngày', font=fs2, fill=(90, 120, 104), anchor='rs')

run(dict(num=20, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=16.7, page_dur=2.8, rstep=0.1,
         rowh=(140, 156), page_low=True,
         theme=dict(hookA=WHITE_, hookA_fg=DG, hookA_tape=CORAL, hookB=MINT, hookB_fg=DG, hookB_hl=CORAL, sub=CORAL, sub_fg=WHITE_,
                    label_bg=CORAL, label_fg=WHITE_, label_sh=DG, title_fg=DG, tape=[CORAL, MINT, CORAL, MINT], header_rule=None,
                    out=WHITE_, out_fg=DG, out_hl=MINT, doodle=CORAL, dots=DG, badges=[CORAL]),
         styles=[(MINT2, 'plain'), (WHITE_, 'grid'), (MINT2, 'plain'), (WHITE_, 'grid')],
         hook=('20 CẶP PHÔNG CHỮ VIỆT HOÁ', 'tiêu đề + nội dung', 'tiêu đề', 'Copy là dùng · đủ dấu tiếng Việt'),
         outro=('Tiêu đề đậm, nội dung dễ đọc', '— vậy là đủ', 'vậy là đủ'), emojis=('memo', 'bookmark'),
         pages=[(f'{int(a):02d}–{int(b):02d}', g, [(n, ITEMS[n]) for n in range(int(a), int(b) + 1)]) for g, a, b in GROUPS],
         draw_row=draw_row))
