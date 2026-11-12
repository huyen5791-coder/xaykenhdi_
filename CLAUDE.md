# Xưởng nội dung video @xaykenhdi_

Đội agent làm video ngắn dọc cho kênh **@xaykenhdi_**: xây kênh TikTok / Reels từ 0, kênh giấu mặt, bán hàng online.
Nói chuyện với chủ kênh bằng **tiếng Việt**, ngắn gọn.

## Quy trình (chủ kênh chốt 12/11)
```
y-tuong ─> [chủ kênh duyệt ý] ─> noi-dung-video: viết script TẤT CẢ ý đã duyệt + tạo thư mục Drive
        ─> [chủ kênh duyệt script + up clip nguồn lên Drive] ─> dung-video: dựng HÀNG LOẠT ─> mp4 lên Drive
```
Thư mục Drive (tạo bằng công cụ Google Drive, mỗi video 1 thư mục):
```
xaykenhdi_ - Video/
  NN-<slug>/
    Kich ban NN - <tên>   (Google Doc: script để chủ kênh duyệt / bình luận)
    1-nguon/               (chủ kênh up clip quay dọc vào đây)
    2-xuat/                (video đã dựng; file > 3 MB agent gửi qua chat, chủ kênh tự kéo vào)
```
Ghi link thư mục vào `BOARD.md` mục "Đang làm". Chỉ dựng video có script đã duyệt **và** đã có clip trong `1-nguon`.

| Agent (skill) | Việc | Đầu ra |
|---|---|---|
| `y-tuong` | Đề xuất chủ đề, không trùng video cũ | Bảng ý tưởng trong `BOARD.md` |
| `noi-dung-video` | Nội dung chữ theo mốc giây + caption + gợi ý quay | `projects/NN-<slug>/noi-dung.md` |
| `dung-video` | Clip + nội dung → video giấy xé scrapbook | `work/NN-<slug>.mp4` |

## Tài liệu
- `style/content-style.md` — giọng văn, khuôn chủ đề, format mốc giây, CTA.
- `style/edit-style.md` — brand, chất liệu, chuyển động, quy tắc dựng bắt buộc.
- `BAN-GIAO.md` — ghi chú bàn giao gốc (15 video đầu). Trang bàn giao: https://claude.ai/artifact/C3Q8SveEL6rh6WJNpBxVWd
- Bản đồ 3D quy trình (xem trực quan 7 trạm): https://claude.ai/artifact/EkLGfEYm3AdF38scq2czgK
- `BOARD.md` — danh sách video đã làm / đang làm / ý tưởng chờ duyệt.

## Quy tắc chung
- Không bịa số liệu hay trải nghiệm của chủ kênh; câu chưa chắc ghi **[xác nhận]**.
- Không tự thêm CTA; đề xuất thì ghi "(đề xuất, chờ duyệt)".
- Không logo nền tảng thật, không nhân vật có bản quyền.
- Không đưa tên model AI vào file, commit hay video.
- Media (clip, mp4, wav, frames, `r3d/out`, `icons/png`, `mont/`, `node_modules/`) không commit.
