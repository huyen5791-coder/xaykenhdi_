# Khuôn "Bản đồ 3D" — kênh @xaykenhdi_

Khuôn mới (chủ kênh gửi ảnh mẫu 12/11/2026): **thành phố nhìn nghiêng 45° từ trên cao (isometric)**, nhiều tầng, đường đi uốn quanh lên đỉnh, mỗi công trình là một "trạm". Ẩn dụ chính: **xây kênh = xây thành phố**.
Ảnh mẫu chỉ để tham khảo **thể loại** (bản đồ thành phố kiểu game chiến thuật). Mọi công trình tự dựng bằng `three.js`, **không chép** lâu đài, nhà, bố cục hay chi tiết của bất kỳ game có sẵn nào.

## Khi nào dùng
- Nội dung có **nhiều phần ghép thành một hệ thống** (kênh gồm những bộ phận gì) hoặc **đi theo đường / lên tầng** (lộ trình, lên cấp).
- Hợp với khuôn: Lộ trình, Lên cấp, Danh sách 4–8 mục. Không dùng cho Câu lệnh AI hay Tính toán (cần chữ dày, để đứng yên).
- Tối đa **1 video bản đồ / 4 video** để không nhàm.

## Bản đồ trông thế nào
- **Đảo nổi** hình tròn bo, 3–5 **tầng bậc thang**, đường lát đá kem uốn từ cổng dưới lên đỉnh. Đỉnh = mục tiêu (vd "1.000 follow", "đơn đầu tiên") — **con số phải lấy từ nội dung đã duyệt**.
- Phong cách **low-poly bo tròn, đồ chơi bóng** — cùng chất nhựa bóng với sticker `r3d` (không vẽ chi tiết hiện thực).
- Màu theo brand: nền đất/đường kem `#FBF8ED`, cỏ & mái xanh rêu `#4D5549` + xanh chuối `#CDFD84`, gỗ/tường nâu `#4F3C35`, điểm nhấn hồng `#F1A0D6` / vàng `#FFFD60`. Trời: gradient kem → hồng nhạt, mây bông 3D.
- **Mỗi mục nội dung = 1 công trình** có đồ vật nhận ra ngay (không cần đọc chữ cũng hiểu):
  | Ý | Công trình gợi ý |
  |---|---|
  | Hook / mở đầu | Cổng thành có loa |
  | Kịch bản, câu lệnh | Thư viện / bàn viết |
  | Quay | Xưởng có máy quay, đèn |
  | Dựng | Xưởng mộc / bàn cắt |
  | Đăng, lịch đăng | Tháp đồng hồ |
  | Tương tác, bình luận | Quảng trường, bảng tin |
  | Bán hàng | Chợ, sạp có mái vải |
  | Tiền, lãi lỗ | Kho có rương / cân |
  | Quảng cáo | Tháp phát sóng (không logo) |
  | Phân tích số liệu | Đài quan sát có kính viễn vọng |
- Không cờ, biển hiệu, logo nền tảng thật; chỉ ghi **tên nền tảng bằng chữ** nếu cần.

## Bố cục khung 1440×2560
- Khung dọc: đảo chiếm ~70% chiều cao, đỉnh ở trên, cổng ở dưới — giống ảnh mẫu (đường đi từ dưới lên).
- Clip chủ kênh: **ô tròn / khung polaroid** góc dưới trái (~420 px) hoặc bỏ hẳn nếu chủ kênh chỉ thu tiếng. Kênh giấu mặt nên mặc định dùng **tay / màn hình** trong ô.
- Chữ vẫn trên **giấy xé / washi** (giữ chất scrapbook của kênh) dán nổi lên trên bản đồ, không viết chữ 3D trên công trình.
- Handle `@xaykenhdi_` góc trên trái như mọi video. Chừa ~350 px đáy cho UI.

## Chuyển động (máy quay)
| Mốc | Chuyển động |
|---|---|
| Hook 0–3 s | Toàn cảnh đảo, máy quay hạ từ trên mây xuống (easeOutCubic ~1 s); dòng hook trên giấy xé bật vào |
| Thân | Máy quay **lướt theo đường đi** tới từng công trình (~0,45–0,8 s/trạm), công trình nảy lên (scale 0,9→1,05→1, easeOutBack) + thẻ giấy tên mục hiện cạnh. Thẻ đã hiện **ở lại** (thu nhỏ thành danh sách bên phải), đúng quy tắc "dòng ở lại" |
| Chốt ~2,5 s | Kéo ra toàn cảnh, đỉnh sáng lên + pháo giấy / sparkle; câu chốt trên giấy kem, CTA washi vàng (chỉ khi chủ kênh duyệt CTA) |
- SFX: whoosh khi máy quay di chuyển, "cộp gỗ" / pop khi công trình nảy, ding ở đỉnh. Không nhạc nền trừ khi chủ kênh gửi.
- Nhịp không được chậm hơn khuôn thường: video vẫn 9–15 s, ≤ 8 trạm.

## Kỹ thuật dựng
- Dựng cảnh trong `r3d/` (three.js, Playwright + SwiftShader như sticker): một file `r3d/map.html` chung, công trình là các hàm dựng sẵn để tái dùng giữa video.
- Render chuỗi PNG 1440×2560 nền trong suốt hoặc có trời → ghép trong `compose.py` như lớp nền, chữ giấy chồng lên bằng Pillow như cũ.
- Camera isometric: `OrthographicCamera` hoặc Perspective FOV ≤ 25°, góc nhìn ~35° từ trên, xoay 45°.
- Xem trước 4 khung (toàn cảnh, trạm 1, trạm cuối, chốt) trước khi render đủ.
- Frames render để trong `r3d/out` / `work/`, không commit.
