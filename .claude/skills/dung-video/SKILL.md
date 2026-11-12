---
name: dung-video
description: Agent Dựng video — từ clip quay dọc + nội dung theo mốc giây, dựng video 1440×2560 phong cách giấy xé / scrapbook của kênh @xaykenhdi_ (giấy, washi, sticker 3D, Fluent Emoji, SFX). Dùng khi chủ kênh gửi clip để dựng hoặc góp ý sửa video đã dựng.
---

# Agent Dựng video

Đọc `style/edit-style.md` và `BAN-GIAO.md`. Lần đầu trong phiên: `bash setup.sh` (font Montserrat, TeX Gyre Termes, sticker 3D, Fluent Emoji).

1. **Kiểm tra clip:** `ffprobe` độ dài; contact sheet `ffmpeg -i clip.mov -vf "fps=1,scale=216:-1,tile=6x2" -frames:v 1 sheet.jpg` → xem vùng mặt, chỗ trống đặt chữ.
2. **Kiểm tra nội dung:** lấy `projects/NN-<slug>/noi-dung.md` (hoặc nội dung chủ kênh gửi). Tính lại con số; thiếu CTA thì hỏi, không tự thêm.
3. **Dựng:** copy `compose_template.py` → `projects/NN-<slug>/compose.py`. Thay chữ, mốc `T_*`, kiểu giấy (khác video trước), emoji (`node icons/render.js <tên>`), danh sách SFX `ev`, `SRC_DUR/DUR`.
4. **Xem trước:** chế độ `preview` trên 4 khung (hook, giữa thân, cuối thân, chốt). Kiểm: chữ không đè mặt, không tràn mép, đáy chừa UI, dòng ở lại.
5. **Xuất:** `python3 compose.py clip.mov work/NN-<slug>.mp4`. Crop 1 khung cuối vùng chữ để soát chính tả.
6. Gửi file cho chủ kênh, cập nhật `BOARD.md`. Góp ý của chủ kênh mà là quy tắc chung → thêm vào `style/edit-style.md` mục "Quy tắc bắt buộc".

Media (clip, mp4, wav, frames) để trong `work/`, không commit.
