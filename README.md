# DinoMac Watchdog - Đặc vụ Gác Cổng (Giám sát Internet Sân Golf)

Đây là công cụ cứu cánh cuối cùng giúp sếp biết được khi nào mạng Internet ở Sân Golf bị sập hoàn toàn (khiến các Đặc vụ AI khác mất liên lạc).

## 🚀 Tính năng mới (Bản Pro V2):
- **Giám sát Đa điểm:** Theo dõi Synology NAS, Master PC qua Tailscale.
- **Hỗ trợ Blockchain (Tùy chọn):** Có sẵn khung code để giám sát RPC Node (kiểm tra block sync).
- **Tối ưu VPS:** Thiết kế để chạy 24/7 trên Oracle Cloud/GCP/AWS (Phù hợp cho sếp đã có thẻ Visa).
- **Triển khai 1-click:** Có sẵn file `deploy.sh` để cài đặt lên Linux VPS trong 30 giây.

## ⚠️ LƯU Ý QUAN TRỌNG:
Công cụ này **KHÔNG CÀI Ở SÂN GOLF**. Sếp phải cài nó ở một máy tính luôn có mạng tại nhà sếp, hoặc trên VPS ảo.

## 🛠️ Hướng dẫn triển khai (WSL / VPS):

1. **Setup:** 
   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```
2. **Cấu hình:** Sửa file `.env` điền Token Telegram.
3. **Chạy ngầm (Vĩnh viễn):**
   Để Watchdog chạy vĩnh viễn ngay cả khi sếp tắt cửa sổ Terminal, hãy dùng lệnh:
   ```bash
   nohup ./venv/bin/python watchdog.py > watchdog.log 2>&1 &
   ```
4. **Quản lý:**
   - Xem log: `tail -f watchdog.log`
   - Dừng lại: `pkill -f watchdog.py`

## Cách hoạt động:
1. Định kỳ 5 phút quét (Ping) IP Tailscale của các thiết bị tại Sân Golf.
2. Nếu Ping thất bại 3 lần liên tiếp (~15 phút) -> Tự động bắn tin Telegram báo động **CRITICAL** cho sếp.
3. Khi có mạng lại -> Bắn tin **RECOVERED**.

---
*DinoMac MEP Command Center - Watchdog Module*
