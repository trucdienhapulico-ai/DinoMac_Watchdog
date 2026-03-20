import os
import time
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load configuration from .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- MONITORING CONFIGURATION ---
WATCH_LIST = [
    {"name": "Synology NAS (Sân Golf)", "id": "NAS", "ip": "onecloud.tail030e1.ts.net", "type": "ping"},
    {"name": "chieusang.montanagc.com.vn",    "id": "PC",  "ip": "chieusang.montanagc.com.vn", "type": "ping"},
]

class DinoWatchdog:
    def __init__(self):
        self.fails = {node['id']: 0 for node in WATCH_LIST}

    def log(self, text):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    def notify(self, status, name, msg):
        emoji = "🔴" if status == "CRITICAL" else "🟢"
        if status == "ONLINE": emoji = "🚀"
        
        full_msg = f"{emoji} [DinoMac Watchdog - {status}]\n\n📌 Mục tiêu: {name}\n📝 Thông báo: {msg}\n⏰ Lúc: {datetime.now().strftime('%H:%M:%S')}"
        
        if not TELEGRAM_TOKEN or not CHAT_ID:
            self.log("⚠️ Cảnh báo: Chưa cấu hình Token Telegram trong .env")
            return
            
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": full_msg}, timeout=10)
        except:
            self.log("❌ Lỗi gửi tin nhắn Telegram.")

    def check_ping(self, ip):
        param = "-n 1 -w 2000" if os.name == 'nt' else "-c 1 -W 2"
        quiet = "> NUL 2>&1" if os.name == 'nt' else "> /dev/null 2>&1"
        return os.system(f"ping {param} {ip} {quiet}") == 0

    def initial_check(self):
        self.log("-" * 60)
        self.log("📋 TRẠNG THÁI GIÁM SÁT BAN ĐẦU:")
        for node in WATCH_LIST:
            alive = self.check_ping(node['ip'])
            status_str = "ONLINE" if alive else "OFFLINE"
            self.log(f"   {status_str:7} | {node['name']} ({node['ip']})")
        self.log("-" * 60)

    def start(self):
        self.log(f"🚀 Khởi động DinoMac Watchdog Pro (Super V2)...")
        
        # Bắn tin chào hỏi tới Telegram
        self.notify("ONLINE", "Hệ thống Watchdog (WSL/VPS)", "Đặc vụ Gác cổng đã trực tuyến và bắt đầu giám sát Sân Golf.")
        self.log("🟢 Đã gửi lời chào khởi động tới Telegram!")

        # Kiểm tra trạng thái tức thì
        self.initial_check()
        self.log("🔔 Sẽ bắt đầu vòng lặp giám sát sau 5 phút...")
        
        while True:
            time.sleep(300) # Mỗi 5 phút check 1 lần
            for node in WATCH_LIST:
                nid = node['id']
                alive = self.check_ping(node['ip'])
                
                if not alive:
                    self.fails[nid] += 1
                    self.log(f"🔴 Mất kết nối: {node['name']} (Lần {self.fails[nid]})")
                    if self.fails[nid] == 3:
                        msg = "Thiết bị Offline. Internet Sân Golf có thể đã bị ngắt!"
                        self.notify("CRITICAL", node['name'], msg)
                else:
                    if self.fails[nid] >= 3:
                        self.notify("RECOVERED", node['name'], "Thiết bị đã trực tuyến trở lại.")
                    self.fails[nid] = 0

if __name__ == "__main__":
    try:
        Dino_Watchdog = DinoWatchdog()
        Dino_Watchdog.start()
    except KeyboardInterrupt:
        print("\nStopping Watchdog...")
