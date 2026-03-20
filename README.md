# DinoMac Watchdog - Đặc vụ Gác Cổng (Giám sát Internet Sân Golf)

Đây là công cụ cứu cánh cuối cùng giúp sếp biết được khi nào mạng Internet ở Sân Golf bị sập hoàn toàn (khiến các Đặc vụ AI khác mất liên lạc).

## ⚡ Cài đặt nhanh (Quick Install - Copy & Paste):

Dành cho sếp khi vừa thuê VPS mới (Ubuntu/Debian) hoặc WSL chạy 1 phát sướng luôn:

```bash
# 1. Tải về (Clone)
git clone https://github.com/trucdienhapulico-ai/DinoMac_Watchdog.git && cd DinoMac_Watchdog

# 2. Cấu hình nhanh (Thay Token và ID của sếp vào đây)
cat <<EOF > .env
TELEGRAM_BOT_TOKEN="8309852170:AAFPaUp_wRGBt-xick-zzDokUfNAZ_wSGHI"
TELEGRAM_CHAT_ID="293490789"
EOF

# 3. Chạy lệnh cài đặt tự động (Cài python/venv/deps)
chmod +x deploy.sh && ./deploy.sh

# 4. Chạy Đặc vụ ở chế độ nền (Nohup - Chạy vĩnh viễn)
nohup ./venv/bin/python watchdog.py > watchdog.log 2>&1 &

# 5. Kiểm tra log ngay lập tức
tail -f watchdog.log
```

## 🚀 Tính năng mới (Bản Pro V2):
- **Định vị Đặc vụ:** Tự động báo cáo Hostname và IP máy đang chạy Watchdog (Tiện khi sếp chạy nhiều máy).
- **Giám sát Đa điểm:** Theo dõi Synology NAS, Master PC qua Tailscale.
- **Tối ưu VPS:** Thiết kế để chạy 24/7 trên Oracle Cloud/GCP/AWS (Phù hợp cho sếp đã có thẻ Visa).

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
