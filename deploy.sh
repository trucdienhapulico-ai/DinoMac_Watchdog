#!/bin/bash

# --- DinoMac Watchdog Auto-Deploy Script ---
echo "🚀 Đang bắt đầu cài đặt Đặc vụ Gác cổng..."

# 1. Cài đặt các thư viện hệ thống cần thiết (Bỏ qua Update để nhanh hơn)
echo "📦 Cài đặt thư viện: python3-venv..."
sudo apt-get install -y python3-venv python3-pip

# 2. Tạo môi trường ảo (Virtual Environment)
echo "🐍 Khởi tạo môi trường ảo Python..."
python3 -m venv venv

# 3. Cài đặt các thư viện cần thiết
echo "🛠️ Cài đặt thư viện: requests, python-dotenv..."
./venv/bin/pip install requests python-dotenv

echo "✅ Cài đặt hoàn tất! Đặc vụ đã sẵn sàng chiến đấu."
