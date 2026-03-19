#!/bin/bash

# DinoMac Watchdog Deployment Script for Linux VPS
# Hướng dẫn: Dán lệnh này vào VPS Ubuntu của sếp

echo "------------------------------------------------"
echo "🚀 Đang triển khai DinoMac Watchdog..."
echo "------------------------------------------------"

# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git tailscale

# 2. Cấu hình Tailscale (nếu chưa có)
if ! command -v tailscale &> /dev/null
then
    curl -fsSL https://tailscale.com/install.sh | sh
    sudo tailscale up
fi

# 3. Tạo môi trường ảo và cài thư viện
cd ~/DinoMac_Watchdog
python3 -m venv venv
source venv/bin/activate
pip install requests python-dotenv

# 4. Kiểm tra file .env
if [ ! -f .env ]; then
    echo "⚠️  CẢNH BÁO: Chưa tìm thấy file .env"
    echo "Sếp hãy chạy lệnh: nano ~/DinoMac_Watchdog/.env để điền Token Telegram."
fi

# 5. Thiết lập Systemd Service để chạy vĩnh viễn
USER_NAME=$(whoami)
SERVICE_FILE="/etc/systemd/system/watchdog.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOF
[Unit]
Description=DinoMac Watchdog Service
After=network.target tailscaled.service

[Service]
ExecStart=/home/$USER_NAME/DinoMac_Watchdog/venv/bin/python /home/$USER_NAME/DinoMac_Watchdog/watchdog.py
WorkingDirectory=/home/$USER_NAME/DinoMac_Watchdog
Restart=always
User=$USER_NAME

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable watchdog

echo "------------------------------------------------"
echo "✅ Hoàn tất! Để bắt đầu, sếp chạy lệnh:"
echo "sudo systemctl start watchdog"
echo "Để xem log: journalctl -u watchdog -f"
echo "------------------------------------------------"
