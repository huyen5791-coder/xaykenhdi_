# Style dựng kênh @xaykenhdi_

## Thông số
- 1440×2560, 30fps, H.264 CRF 18, AAC 192k. Overlay RGBA dựng bằng Pillow, pipe vào ffmpeg (xem `compose_template.py`).
- Tiếng gốc volume 0.75 + SFX từ `sfx.py` đúng nhịp chữ (rip khi giấy vào, pop mỗi dòng, whoosh chuyển trang, ding/sparkle ở câu chốt). Không nhạc nền trừ khi chủ kênh gửi.
- Clip ngắn hơn nội dung: giữ khung cuối (`tpad=stop_mode=clone`). Cuối clip nhòe / sát mặt: cắt sớm rồi giữ khung.

## Brand
- Màu: kem `#FBF8ED` · xanh rêu `#4D5549` · nâu `#4F3C35` · xanh chuối `#CDFD84` · hồng `#F1A0D6` · vàng `#FFFD60` · đỏ doodle `#AA323E`.
- Font: TeX Gyre Termes nghiêng đậm (tiêu đề, câu nhấn) · Montserrat (thân, nhãn; Black cho dòng hook in hoa).
- Handle `@xaykenhdi_` góc trên trái suốt video: pill xanh rêu, viền xanh chuối, có sao lấp lánh nhỏ.

## Bộ màu & kiểu dựng — ĐỔI MỖI VIDEO (chủ kênh chốt 12/11)
Không dùng cùng 1 bộ màu cho 2 video liền nhau. Giữ cố định: handle `@xaykenhdi_`, font chữ (TeX Gyre Termes + Montserrat), quy tắc bắt buộc. Đổi: màu giấy, màu chữ, màu nhấn, chất liệu, đồ trang trí. Script ghi rõ dòng **Style:** ở đầu.
| Bộ | Giấy / nền chữ | Chữ | Nhấn | Chất liệu, trang trí | Đã dùng |
|---|---|---|---|---|---|
| Kẹo ngọt | kem, hồng, xanh chuối, vàng | nâu | xanh chuối / vàng | giấy xé, washi | 16, 17, 18 |
| Báo cũ đen trắng | giấy báo xám | đen | đỏ doodle `#AA323E`, vàng | chữ ransom, gạch đỏ | 19 |
| Bạc hà san hô | bạc hà `#BFE8D6`, trắng | xanh rêu đậm | san hô `#FF7F6E` | thẻ mẫu màu sơn | 20 |
| Tím oải hương | tím nhạt `#D9CCF2`, trắng | tím than `#3B2C5E` | vàng chanh | giấy note xếp tầng | 21 |
| Cà phê sữa | kraft `#C8A27A`, kem | nâu đậm | cam đất `#D9773B` | tem bưu chính, dây gai | 22 |
| Đêm xanh | xanh than `#1F2A44` | kem | vàng nắng | bong bóng chat giấy, sao bạc | 23 |
| Cam đào | cam đào `#FFD3B6`, trắng | nâu | xanh dương `#3A6EA5` | lịch bàn khoen tròn, tick | 24 |
| Xanh dương cổ điển | thẻ thư viện kẻ ô xanh | xanh than | vàng, mộc đỏ | dấu mộc "ĐÃ SỬA" | 25 |
| Băng cảnh báo | vàng + sọc đen | đen | đỏ | ô đánh dấu, dấu X | 26 |
| Hồng đất | hồng đất `#C97B6B`, xanh lá đậm `#2F4A3A` | kem | vàng | ô tìm kiếm cắt giấy, kính lúp | 27 |
Hết bảng thì quay vòng nhưng đổi chất liệu. Mỗi bộ màu đã có mã sẵn trong `projects/NN-*/compose.py` (19–27) để tái dùng.

## Chất liệu (đổi giữa các video)
Giấy xé viền sợi trắng · giấy nhàu · ô li · kẻ dòng · giấy báo · vở lò xo · lịch xé · hoá đơn in nhiệt · bảng ghim · băng dính washi (có chữ) · sticker 3D bóng (`r3d`) · chữ cắt dán ransom · doodle vẽ tay trên giấy báo · Fluent Emoji · **bản đồ 3D isometric** (nền thành phố three.js, chữ vẫn trên giấy — xem `style/map-3d.md`).

## Bố cục & chuyển động
- Hook đặt dưới mặt (y ≈ 1400–1900), giấy xoay nhẹ ±1–2°, **có sẵn từ khung 0** (không hiệu ứng vào).
- Thân: trang giấy trượt vào từ cạnh, dòng hiện dần cách 0,45 s và ở lại; trang cũ bay ra phía đối diện.
- Câu chốt: giấy kem, 1–2 chữ tô nền xanh chuối; CTA trên washi vàng trượt vào từ phải.
- Chữ không đè lên mặt; chừa ~350 px đáy cho UI TikTok/Reels.

## Quy tắc bắt buộc (chủ kênh đã chốt)
- **Chữ hook phải to, đọc ngay được:** không dùng chữ cắt dán ransom cho dòng hook (khó đọc); dòng lớn ngắt 2 dòng nếu dài; dòng nào cần nhấn thì phải TO NHẤT, không để thành dòng phụ nhỏ. (12/11)
- **Hook hiện đủ ngay từ khung đầu tiên (giây 0)** — không bật / trượt / mờ dần vào; chỉ được "thở" nhẹ tại chỗ. (12/11)
- Danh sách / bước hiện dần và **ở lại**, không biến mất từng dòng.
- **Không** thêm thanh đen hay hiệu ứng che chữ khi không được yêu cầu.
- Không tự bịa CTA.
- 👇 và emoji chỉ hướng → mũi tên 3D; emoji minh hoạ → Fluent Emoji tương ứng (`icons/pick.js` kiểm tra tên).
- Chỉ viết tên nền tảng, không dùng logo thật; không vẽ nhân vật / logo có bản quyền.
- Kiểm tra lại con số trong nội dung trước khi dựng.
