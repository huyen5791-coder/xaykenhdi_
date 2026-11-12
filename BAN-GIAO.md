# Bàn giao: dựng video ngắn cho kênh @xaykenhdi_

Đây là bộ công cụ và quy ước đã dùng để dựng 15 video ngắn (24/10/2026). Đọc hết file này trước khi dựng video mới.

## Quy trình mỗi video
1. Người dùng gửi 1 clip quay dọc (.mov) + nội dung chia theo mốc giây (0–3s hook, 3–Xs thân, cuối: câu chốt + dòng nhỏ CTA).
2. Kiểm tra clip: `ffprobe` độ dài; làm contact sheet `ffmpeg -vf "fps=1,scale=216:-1,tile=6x2"` để xem vùng mặt, chỗ trống.
3. Copy `compose_template.py` thành `composeN.py`, thay nội dung, thời gian (`T_*`), hình minh họa, sound effect (`ev`).
4. Xem trước bằng chế độ `preview` (ghép overlay lên vài khung hình gốc) → chỉnh vị trí → xuất bản cuối.
5. Kiểm tra lại 1 khung hình cuối (crop vùng chữ) trước khi gửi.

## Thông số
- Khung 1440×2560, 30fps, H.264 CRF 18, AAC 192k. Overlay RGBA dựng bằng Pillow, pipe vào ffmpeg.
- Giữ tiếng gốc ở volume 0.75, trộn thêm SFX (sfx.py). Không nhạc nền trừ khi người dùng gửi.
- Nếu video gốc ngắn hơn khung nội dung: giữ khung cuối bằng `tpad=stop_mode=clone` (+ afade tiếng gốc). Nếu cuối clip bị nhòe/sát mặt, cắt sớm hơn (trim) rồi giữ khung.

## Brand
- Màu: kem #FBF8ED · xanh rêu #4D5549 · nâu #4F3C35 · xanh chuối #CDFD84 · hồng #F1A0D6 · vàng #FFFD60 (đỏ phụ cho doodle: #AA323E)
- Font: TeX Gyre Termes (nghiêng đậm cho tiêu đề/câu nhấn), Montserrat (thân chữ, nhãn).
- Handle `@xaykenhdi_` luôn ở góc trên trái (pill xanh rêu, viền xanh chuối) suốt video.
- Phong cách: giấy xé (torn paper có viền sợi trắng), giấy nhàu/ô li/kẻ dòng/giấy báo, băng dính washi, sticker 3D bóng (three.js), chữ cắt dán kiểu ransom note, doodle vẽ tay trên giấy báo, hình Fluent Emoji.

## Quy tắc đã chốt với người dùng (bắt buộc)
- Danh sách/bước hiện dần và **ở lại trên màn hình**, không biến mất từng dòng (quá nhanh khó đọc).
- **Không** thêm thanh đen che chữ ("MẶT") hay hiệu ứng che chữ tự ý.
- Không tự bịa dòng CTA khi người dùng không đưa; hỏi nếu cần.
- Emoji trong nội dung (👇) đổi thành mũi tên 3D; emoji minh họa (🍳📚…) dùng Fluent Emoji tương ứng.
- Đổi đa dạng kiểu giấy và icon giữa các video, nhưng giữ màu + font brand.
- Không dùng logo thật của nền tảng (TikTok, Facebook…), chỉ viết tên.
- Không vẽ nhân vật/logo có bản quyền.
- Chữ không đè lên mặt người trong clip; chừa đáy cho UI TikTok/Reels.

## File
- `lib.py` — màu, font, giấy xé, tape, easing, `paste()`, nạp sticker 3D.
- `lib2.py` — giấy nhàu, `paper_sheet()` (plain/grid/lined/news, lỗ lò xo), chữ ransom, doodle (star/heart/sparkle/arrow/rays/circle).
- `sfx.py` — tạo SFX bằng code: pop, tick, whoosh, rip (giấy xé), ding, sparkle; `build()` ra WAV.
- `r3d/index.html`, `r3d/render.js` — 30 sticker 3D, render 24 khung xoay ra `r3d/out/<tên>_NN.png`.
- `icons/render.js`, `icons/pick.js` — xuất Fluent Emoji ra PNG.
- `compose_template.py` — mẫu một video hoàn chỉnh.
- `setup.sh` — cài đặt.

## Tài liệu liên quan trong Project "Edit video" (claude.ai)
- `claude/brief-kenh-huyen.md` — brief kênh (định vị, định dạng, CTA, làm đẹp da).
- `claude/kich-ban-edit-nhanh-bang-ai.md` — kịch bản video "edit nhanh bằng AI".
- `claude/kich-ban-ai-dau-van-tay.md` — kịch bản NCKH (bản thay thế).
- `claude/tools/beauty.py` — công cụ chỉnh da.
