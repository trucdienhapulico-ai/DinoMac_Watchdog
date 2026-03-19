# DinoMac Watchdog - Đặc vụ Gác Cổng (Giám sát Internet Sân Golf)

Đây là công cụ cứu cánh cuối cùng giúp sếp biết được khi nào mạng Internet ở Sân Golf bị sập hoàn toàn (khiến các Đặc vụ AI khác mất liên lạc).

## ⚠️ LƯU Ý QUAN TRỌNG:
Công cụ này **KHÔNG CÀI Ở SÂN GOLF**. Sếp phải cài nó ở một máy tính luôn có mạng tại nhà sếp, hoặc trên VPS ảo, hoặc trên điện thoại (qua Termux). 

## Cách hoạt động:
1.  Định kỳ 5 phút quét (Ping) IP Tailscale của Synology NAS (`onecloud.tail030e1.ts.net`) và Máy tính Master.
2.  Nếu Ping thất bại quá 3 lần (khoảng 15 phút) -> Tự động bắn tin Telegram báo động `CRITICAL` cho sếp.

## Cài đặt:
1. Cài Python 3.12 và thư viện `requests`, `python-dotenv`.
2. Tạo tệp `.env` điền Token Telegram của sếp.
3. Chạy lệnh: `python watchdog.py`.

---
*DinoMac MEP Command Center - Watchdog Module*
