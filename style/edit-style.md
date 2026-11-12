# Style dựng kênh @xaykenhdi_

## Thông số
- 1440×2560, 30fps, H.264 CRF 18, AAC 192k. Overlay RGBA dựng bằng Pillow, pipe vào ffmpeg (xem `compose_template.py`).
- Tiếng gốc volume 0.75 + SFX từ `sfx.py` đúng nhịp chữ (rip khi giấy vào, pop mỗi dòng, whoosh chuyển trang, ding/sparkle ở câu chốt). Không nhạc nền trừ khi chủ kênh gửi.
- Clip ngắn hơn nội dung: giữ khung cuối (`tpad=stop_mode=clone`). Cuối clip nhòe / sát mặt: cắt sớm rồi giữ khung.

## Brand
- Màu: kem `#FBF8ED` · xanh rêu `#4D5549` · nâu `#4F3C35` · xanh chuối `#CDFD84` · hồng `#F1A0D6` · vàng `#FFFD60` · đỏ doodle `#AA323E`.
- Font: TeX Gyre Termes nghiêng đậm (tiêu đề, câu nhấn) · Montserrat (thân, nhãn; Black cho dòng hook in hoa).
- Handle `@xaykenhdi_` góc trên trái suốt video: pill xanh rêu, viền xanh chuối, có sao lấp lánh nhỏ.

## Chất liệu (đổi giữa các video, giữ màu + font)
Giấy xé viền sợi trắng · giấy nhàu · ô li · kẻ dòng · giấy báo · vở lò xo · lịch xé · hoá đơn in nhiệt · bảng ghim · băng dính washi (có chữ) · sticker 3D bóng (`r3d`) · chữ cắt dán ransom · doodle vẽ tay trên giấy báo · Fluent Emoji.

## Bố cục & chuyển động
- Hook đặt dưới mặt (y ≈ 1400–1900), giấy xoay nhẹ ±1–2°, bật vào bằng easeOutBack ~0,35 s.
- Thân: trang giấy trượt vào từ cạnh, dòng hiện dần cách 0,45 s và ở lại; trang cũ bay ra phía đối diện.
- Câu chốt: giấy kem, 1–2 chữ tô nền xanh chuối; CTA trên washi vàng trượt vào từ phải.
- Chữ không đè lên mặt; chừa ~350 px đáy cho UI TikTok/Reels.

## Quy tắc bắt buộc (chủ kênh đã chốt)
- Danh sách / bước hiện dần và **ở lại**, không biến mất từng dòng.
- **Không** thêm thanh đen hay hiệu ứng che chữ khi không được yêu cầu.
- Không tự bịa CTA.
- 👇 và emoji chỉ hướng → mũi tên 3D; emoji minh hoạ → Fluent Emoji tương ứng (`icons/pick.js` kiểm tra tên).
- Chỉ viết tên nền tảng, không dùng logo thật; không vẽ nhân vật / logo có bản quyền.
- Kiểm tra lại con số trong nội dung trước khi dựng.
