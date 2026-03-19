import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

# Tải cấu hình từ .env
load_dotenv()

# Cấu hình danh sách thiết bị CẦN GIÁM SÁT TẠI SÂN GOLF (Qua Tailscale)
NODES_TO_WATCH = [
    {"name": "Synology NAS (Database Hub)", "ip": "onecloud.tail030e1.ts.net"},
    {"name": "Máy tính Master (Luôn bật)",  "ip": "master-pc.tail030e1.ts.net"} # <--- Sếp thay IP master nếu cần
]

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_alert(message):
    if not TELEGRAM_TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": f"🚨 [WATCHDOG - BÁO ĐỘNG NGOẠI TUYẾN]\n\n{message}"}
    try: requests.post(url, json=payload, timeout=10)
    except: pass

def check_ping(ip):
    # Ping 1 lần, chờ tối đa 2 giây
    param = "-n 1 -w 2000" if os.name == 'nt' else "-c 1 -W 2"
    response = os.system(f"ping {param} {ip}")
    return response == 0

print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang khởi động Đặc vụ Gác cổng (Watchdog)...")
print("Lưu ý: Công cụ này đang chạy NGOÀI Sân Golf để giám sát Internet.")

# Theo dõi số lần mất kết nối liên tiếp
fail_counters = {node['ip']: 0 for node in NODES_TO_WATCH}

while True:
    for node in NODES_TO_WATCH:
        ip = node['ip']
        name = node['name']
        
        is_alive = check_ping(ip)
        
        if not is_alive:
            fail_counters[ip] += 1
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔴 Cảnh báo: {name} ({ip}) Mất kết nối lần {fail_counters[ip]}")
        else:
            if fail_counters[ip] > 0:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 🟢 {name} Đã trực tuyến trở lại.")
                fail_counters[ip] = 0
        
        # Ngưỡng báo động: Nếu mất mạng 3 lần liên tiếp (khoảng 15 phút)
        if fail_counters[ip] == 3:
            msg = f"THIẾT BỊ TẠI SÂN GOLF MẤT KẾT NỐI!\nTên: {name}\nĐịa chỉ: {ip}\nTrạng thái: OFFLINE (Internet có thể đã bị ngắt)."
            send_alert(msg)
            
    time.sleep(300) # 5 phút kiểm tra lại một lần
