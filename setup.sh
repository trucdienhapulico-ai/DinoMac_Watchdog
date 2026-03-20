#!/bin/bash
echo "📦 DinoMac Watchdog v3.2.1 - Bắt đầu cài đặt..."
cd ~
rm -rf DinoMac_Watchdog
git clone https://github.com/trucdienhapulico-ai/DinoMac_Watchdog.git
cd DinoMac_Watchdog
apt-get install -y python3-venv python3-pip 2>/dev/null
python3 -m venv venv
./venv/bin/pip install requests python-dotenv
printf 'TELEGRAM_BOT_TOKEN=""\nTELEGRAM_CHAT_ID=""' > .env
echo ""
echo "✅ Cài đặt hoàn tất v3.2.1!"
echo "👉 Bước tiếp theo: Điền Token và Chat ID vào file .env"
echo "   nano ~/DinoMac_Watchdog/.env"
echo ""
echo "   Sau khi điền xong, chạy lệnh:"
echo "   cd ~/DinoMac_Watchdog && nohup ./venv/bin/python3 watchdog.py > watchdog.log 2>&1 &"
