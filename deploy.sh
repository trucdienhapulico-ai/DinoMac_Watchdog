#!/bin/bash

# DinoMac Watchdog - Super Pro Deployment Script (WSL/VPS)
echo "------------------------------------------------"
echo "🚀 Đang triển khai DinoMac Watchdog Super Pro..."
echo "------------------------------------------------"

# 1. Cài đặt Tailscale (Nếu chưa có)
if ! command -v tailscale &> /dev/null
then
    echo "⚠️  Chưa tìm thấy Tailscale. Đang tiến hành cài đặt..."
    curl -fsSL https://tailscale.com/install.sh | sh
    sudo tailscale up --accept-dns=false
else
    echo "✅ Tailscale đã được cài đặt."
fi

# 2. Cập nhật hệ thống
sudo apt update && sudo apt install -y python3-pip python3-venv git

# 3. Setup Virtual Environment
cd ~/DinoMac_Watchdog
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv

# 4. Kiểm tra .env
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📢 Đã tạo file .env. Sếp hãy sửa file này bằng lệnh: nano .env"
fi

echo "------------------------------------------------"
echo "✅ Hoàn tất cài đặt!"
echo "➡️  Để chạy ngầm: nohup ./venv/bin/python watchdog.py > watchdog.log 2>&1 &"
echo "------------------------------------------------"
