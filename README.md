# DinoMac Watchdog (v3.2.0) - Đặc vụ Gác Cổng Sân Golf

Giám sát Internet Sân Golf 24/7. Tự động báo Telegram khi mất kết nối.

## ⚡ Cài đặt 1 lệnh duy nhất (v3.2.0):

```bash
sudo bash -c "$(curl -sL https://raw.githubusercontent.com/trucdienhapulico-ai/DinoMac_Watchdog/master/setup.sh)"
```

## 📱 Lệnh Telegram (Gõ trực tiếp cho Bot):
| Lệnh | Chức năng |
| :--- | :--- |
| `/ping` | Kiểm tra Đặc vụ còn thức hay không |
| `/status` | Báo cáo chi tiết NAS và Master PC |

> 💡 **Gợi ý lệnh tự động:** Vào `@BotFather` → `/setcommands` → Chọn Bot → Dán nội dung sau:
> ```
> ping - Kiểm tra nhanh Đặc vụ còn thức hay không
> status - Báo cáo chi tiết hiện trạng thiết bị Sân Golf
> ```

## ⚠️ LƯU Ý:
- Công cụ này **KHÔNG CÀI Ở SÂN GOLF**. Cài ở nhà sếp hoặc VPS.
- Chạy thủ công: `./venv/bin/python3 watchdog.py`
- Xem log: `tail -f watchdog.log`
- Dừng lại: `pkill -f watchdog.py`

## 🔄 Cách hoạt động:
1. Mỗi 5 phút quét Ping NAS + Master PC qua Tailscale.
2. Mất kết nối 3 lần (~15 phút) → Telegram báo **CRITICAL**.
3. Có mạng lại → Telegram báo **RECOVERED**.

---
*DinoMac MEP v3.2.0 - Watchdog Module*
