#!/usr/bin/env bash
# Cài môi trường dựng video "xaykenhdi_" (Linux/macOS). Chạy trong thư mục chứa lib.py.
set -e
# 1) Python: Pillow + numpy (+ ffmpeg phải có sẵn trong PATH)
pip install --break-system-packages pillow numpy 2>/dev/null || pip install pillow numpy
command -v ffmpeg >/dev/null || echo "!! Cần cài ffmpeg (brew install ffmpeg / apt install ffmpeg)"

# 2) Font brand
#    - Montserrat: tải về thư mục ./mont (lib.py đọc mont/fonts/ttf/Montserrat-*.ttf)
[ -d mont ] || git clone --depth 1 https://github.com/JulietaUla/Montserrat.git mont
#    - TeX Gyre Termes: lib.py mặc định đọc /usr/share/texmf/fonts/opentype/public/tex-gyre/
#      Nếu máy không có, tải bộ TeX Gyre Termes (GUST) và sửa biến TG trong lib.py trỏ tới thư mục chứa
#      texgyretermes-bold.otf / -bolditalic.otf / -italic.otf

# 3) Sticker 3D (three.js render qua Playwright/Chromium)
cd r3d && npm init -y >/dev/null && npm i three@0.160.0 playwright && npx playwright install chromium
node render.js star,heart,sparkle,arrow,bubble,ring,blob,cube,pin,clock,hourglass,coins,warn,check,mega,calc,bulb,cursor,magnifier,pencil,camera,play,cake,pushpin,clip,xmark,eye,bottle,drop,trophy
cd ..

# 4) Hình minh họa Fluent Emoji (Microsoft, giấy phép MIT)
cd icons && npm init -y >/dev/null && npm i @iconify-json/fluent-emoji playwright
#    Xuất hình theo tên:  node render.js see-no-evil-monkey thinking-face ...   -> icons/png/<tên>.png
#    Kiểm tra tên:        node pick.js <tên> ...
cd ..
echo "Xong. Thử: python3 compose_template.py video_goc.mov ra.mp4"
