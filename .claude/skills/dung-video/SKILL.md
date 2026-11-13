---
name: dung-video
description: Agent Dựng video — từ clip quay dọc + nội dung theo mốc giây, dựng video 1440×2560 phong cách giấy xé / scrapbook của kênh @xaykenhdi_ (giấy, washi, sticker 3D, Fluent Emoji, SFX). Dùng khi chủ kênh gửi clip để dựng hoặc góp ý sửa video đã dựng.
---

# Agent Dựng video

Đọc `style/edit-style.md` và `BAN-GIAO.md`. Video khuôn **Bản đồ 3D**: đọc thêm `style/map-3d.md`. Lần đầu trong phiên: `bash setup.sh` (font Montserrat, TeX Gyre Termes, sticker 3D, Fluent Emoji).

1. **Kiểm tra clip:** `ffprobe` độ dài; contact sheet `ffmpeg -i clip.mov -vf "fps=1,scale=216:-1,tile=6x2" -frames:v 1 sheet.jpg` → xem vùng mặt, chỗ trống đặt chữ.
2. **Kiểm tra nội dung:** lấy `projects/NN-<slug>/noi-dung.md` (hoặc nội dung chủ kênh gửi). Tính lại con số; thiếu CTA thì hỏi, không tự thêm.
3. **Dựng:** copy `compose_template.py` → `projects/NN-<slug>/compose.py`. Thay chữ, mốc `T_*`, kiểu giấy (khác video trước), emoji (`node icons/render.js <tên>`), danh sách SFX `ev`, `SRC_DUR/DUR`.
4. **Xem trước:** chế độ `preview` trên 4 khung (hook, giữa thân, cuối thân, chốt). Kiểm: chữ không đè mặt, không tràn mép, đáy chừa UI, dòng ở lại.
5. **Xuất:** `python3 compose.py clip.mov work/NN-<slug>.mp4`. Crop 1 khung cuối vùng chữ để soát chính tả.
6. Gửi file cho chủ kênh, cập nhật `BOARD.md`. Góp ý của chủ kênh mà là quy tắc chung → thêm vào `style/edit-style.md` mục "Quy tắc bắt buộc".

Media (clip, mp4, wav, frames) để trong `work/`, không commit.

## Dựng hàng loạt (từ Drive)
1. Đọc `BOARD.md` "Đang làm", lấy các video trạng thái "sẵn sàng dựng" (script đã duyệt + có clip trong `1-nguon`).
2. Với mỗi video: đọc lại Google Doc kịch bản (bản chủ kênh đã sửa) → cập nhật `noi-dung.md` → tải clip trong `1-nguon` về `work/` → dựng như các bước trên.
3. Up mp4 vào `2-xuat`, đổi trạng thái "đã dựng" trong `BOARD.md`. Xong cả đợt thì gửi chủ kênh danh sách link.
4. **Giới hạn công cụ Drive:** tải về tối đa 10 MB, gửi lên tối đa ~3 MB mỗi lần. Vì vậy:
   - Clip nguồn: lấy từ thư mục chung `0-CLIP-NGUON` (id `1KhNs9QuilvKp8bR-_R-FQbmN7v83sbs9`), gán theo thứ tự tên cho các video chờ dựng (xem CLAUDE.md). Thư mục cũ `1-nguon` đã bật "ai có link đều xem" (chủ kênh cho phép 12/11). Tải bằng `curl -sSL -o work/srcNN/<tên> "https://drive.usercontent.google.com/download?id=<fileId>&export=download&confirm=t"` (lấy fileId bằng search_files `parentId = '<id 1-nguon>'`). Thư mục `1-nguon` tạo mới cũng phải bật chia sẻ link (share_file, permissionId `anyoneWithLink`, role `reader`).
   - Video xuất: gửi chủ kênh qua chat (SendUserFile); chỉ up vào `2-xuat` nếu file < 3 MB.
5. Clip quay mặt: xem contact sheet, mặt ở nửa trên → dồn chữ xuống nửa dưới, thu nhỏ dòng, dùng giấy trơn (đường kẻ cắt ngang chữ nhỏ). Mẫu: `projects/16-50-cau-mo-dau/compose.py` (tự đổi bố cục khi có clip).
6. Video dạng danh sách nhiều trang: dùng khung chung `listvid.py` (hook có sẵn từ khung 0, tự đổi bố cục khi có clip). Mẫu: `projects/16-*/compose.py` (câu có chỗ trống), `17-*` (mỗi dòng viết bằng chính phông đó — phông tải từ Google Fonts vào `work/fonts17/`, kiểm dấu bằng fontTools), `18-*` (lịch theo ngày).
7. **Bộ màu:** mỗi video truyền `theme=` + `styles=` vào `listvid.run` theo dòng **Style:** của script (bảng ở `style/edit-style.md`). Mẫu: `19-*` (báo cũ, chữ ransom, gạch đỏ → tô vàng), `20-*` (bạc hà, thẻ mẫu màu sơn, 2 phông/dòng), `21-*` (tím, giấy note xếp tầng). `page_low=True` + `hook_y` khi mặt quay gần, cằm thấp.
