#!/bin/bash
echo "📦 DinoMac Watchdog v3.2.1 - Bắt đầu cài đặt..."
cd ~
rm -rf DinoMac_Watchdog
git clone https://github.com/trucdienhapulico-ai/DinoMac_Watchdog.git
cd DinoMac_Watchdog
apt-get install -y python3-venv python3-pip 2>/dev/null
python3 -m venv venv
./venv/bin/pip install requests python-dotenv
echo ""
echo "✅ Cài đặt môi trường hoàn tất!"
echo ""
echo "🔐 Cấu hình Telegram (Nhập lần lượt):"
read -p "   Nhập TELEGRAM_BOT_TOKEN: " bot_token
read -p "   Nhập TELEGRAM_CHAT_ID:   " chat_id
printf "TELEGRAM_BOT_TOKEN=\"%s\"\nTELEGRAM_CHAT_ID=\"%s\"" "$bot_token" "$chat_id" > .env
echo ""
echo "✅ Đã lưu cấu hình vào .env"
echo "🚀 Đang khởi động Đặc vụ Gác cổng v3.2.1..."
nohup ./venv/bin/python3 watchdog.py > watchdog.log 2>&1 &
sleep 3
tail -20 watchdog.log
echo ""
echo "🎉 Đặc vụ đã Online! Gõ /ping trên Telegram để kiểm tra."
