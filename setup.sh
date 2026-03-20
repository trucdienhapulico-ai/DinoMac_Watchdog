#!/bin/bash
echo "📦 DinoMac Watchdog v3.2.0 - Bắt đầu cài đặt..."
cd ~
rm -rf DinoMac_Watchdog
git clone https://github.com/trucdienhapulico-ai/DinoMac_Watchdog.git
cd DinoMac_Watchdog
printf 'TELEGRAM_BOT_TOKEN="8309852170:AAFPaUp_wRGBt-xick-zzDokUfNAZ_wSGHI"\nTELEGRAM_CHAT_ID="293490789"' > .env
apt-get install -y python3-venv python3-pip 2>/dev/null
python3 -m venv venv
./venv/bin/pip install requests python-dotenv
echo "✅ Cài đặt hoàn tất v3.2.0! Đang khởi động Đặc vụ..."
nohup ./venv/bin/python3 watchdog.py > watchdog.log 2>&1 &
sleep 3
tail -20 watchdog.log
echo "🚀 Đặc vụ Gác cổng đã Online! Gõ /ping trên Telegram để kiểm tra."
