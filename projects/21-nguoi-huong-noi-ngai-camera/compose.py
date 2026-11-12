# Video 21 · Ngại camera? 15 mẹo quay 1 lần là xong — bộ màu "Tím oải hương"
# Chạy: python3 compose.py <clip.mov | none> <ra.mp4> [preview]
import sys, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
from listvid import *

LAV = (217, 204, 242); LAV2 = (236, 229, 250); NAVY = (59, 44, 94); LEMON = (228, 243, 90); WHITE_ = (255, 255, 255)
md = open(os.path.join(HERE, 'noi-dung.md'), encoding='utf-8').read()
GROUPS = re.findall(r'Trang \d+: ([^(\n]+?) \((\d+)–(\d+)\)', md)
ITEMS = {int(n): t.strip() for n, t in re.findall(r'(?m)^- \*\*(\d+)\.\*\* (.+)$', md)}
assert len(GROUPS) == 3 and len(ITEMS) == 15

def prepare(items, clip, pw):
    for sz in (range(48, 31, -1) if clip else range(58, 37, -1)):
        f = F('Bold', sz)
        if max(f.getlength(s) for _, s in items) <= pw - 230: return f
    return f
def draw_row(R, dr, it, j, rowh, clip, c, ctx):
    n, s = it; cy = rowh / 2
    # thẻ ghi chú nhỏ xếp tầng làm số thứ tự
    dr.rectangle([34, cy - 36, 110, cy + 36], fill=NAVY + (255,)); dr.rectangle([28, cy - 42, 104, cy + 30], fill=LEMON + (255,))
    dr.text((66, cy - 6), str(n), font=F('Black', 34), fill=NAVY, anchor='mm')
    dr.text((140, cy + ctx.size * 0.36), s, font=ctx, fill=NAVY, anchor='ls')

run(dict(num=21, src=sys.argv[1], out=sys.argv[2], preview=len(sys.argv) > 3, dur=14.5, page_dur=3.0, rstep=0.12,
         rowh=(118, 140),
         theme=dict(hookA=WHITE_, hookA_fg=NAVY, hookA_tape=LEMON, hookB=NAVY, hookB_fg=WHITE_, hookB_hl=(150, 120, 215), sub=LEMON, sub_fg=NAVY,
                    label_bg=NAVY, label_fg=LEMON, label_sh=(150, 130, 200), title_fg=NAVY, tape=[LEMON, WHITE_, LEMON],
                    out=LAV2, out_fg=NAVY, out_hl=LEMON, doodle=NAVY, dots=NAVY),
         styles=[(LAV, 'plain'), (WHITE_, 'lined'), (LAV, 'plain')],
         hook=('NGẠI CAMERA?', '15 mẹo cho\nngười hướng nội', '15 mẹo', None), hook_y=[1430, 1760, 1990], big_size=140, acc_size=150,
         outro=('Không cần tự tin.', 'Chỉ cần quay xong.', 'quay xong'), emojis=('megaphone', 'bookmark'),
         pages=[(f'{int(a):02d}–{int(b):02d}', g, [(n, ITEMS[n]) for n in range(int(a), int(b) + 1)]) for g, a, b in GROUPS],
         prepare=prepare, draw_row=draw_row))
