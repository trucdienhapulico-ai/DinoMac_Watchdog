import socket
import os
import time
import requests
import threading
from dotenv import load_dotenv
from datetime import datetime

# --- DinoMac Watchdog Configuration ---
VERSION = "3.2.0 (Interactive Mode)"
# --------------------------------------

# Load configuration from .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def get_local_info():
    try:
        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return hostname, local_ip
    except:
        return socket.gethostname(), "Unknown IP"

# --- MONITORING CONFIGURATION ---
WATCH_LIST = [
    {"name": "Synology NAS (Sân Golf)", "id": "NAS", "ip": "onecloud.tail030e1.ts.net", "type": "ping"},
    {"name": "Chiếu sáng Sân Golf",     "id": "CS",  "ip": "chieusang.montanagc.com.vn", "type": "http", "port": 81},
]

class DinoWatchdog:
    def __init__(self):
        self.fails = {node['id']: 0 for node in WATCH_LIST}
        self.hostname, self.local_ip = get_local_info()
        self.last_update_id = 0

    def log(self, text):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    def notify(self, status, name, msg):
        emoji = "🔴" if status == "CRITICAL" else "🟢"
        if status == "ONLINE": emoji = "🚀"
        if status == "RESPONSE": emoji = "💬"
        
        full_msg = (
            f"{emoji} [DinoMac Watchdog - {status}]\n\n"
            f"📌 Mục tiêu: {name}\n"
            f"📝 Thông báo: {msg}\n"
            f"⏰ Lúc: {datetime.now().strftime('%H:%M:%S')}\n"
            f"---------------------------\n"
            f"📍 Gửi từ: {self.hostname}\n"
            f"🌐 IP Watchdog: {self.local_ip}"
        )
        
        if not TELEGRAM_TOKEN or not CHAT_ID: return
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": full_msg}, timeout=10)
        except:
            self.log("❌ Lỗi gửi tin nhắn Telegram.")

    def check_ping(self, ip):
        param = "-n 1 -w 2000" if os.name == 'nt' else "-c 1 -W 2"
        quiet = "> NUL 2>&1" if os.name == 'nt' else "> /dev/null 2>&1"
        return os.system(f"ping {param} {ip} {quiet}") == 0

    def check_http(self, ip, port=80):
        """Kiểm tra dịch vụ web trên cổng cụ thể (dành cho server chặn Ping)"""
        try:
            r = requests.get(f"http://{ip}:{port}", timeout=5)
            return r.status_code < 500
        except:
            return False

    def check_node(self, node):
        """Tự động chọn phương thức kiểm tra phù hợp"""
        if node.get("type") == "http":
            return self.check_http(node['ip'], node.get('port', 80))
        return self.check_ping(node['ip'])

    def get_full_status(self):
        reports = []
        for node in WATCH_LIST:
            alive = self.check_node(node)
            status_emoji = "✅ ONLINE" if alive else "❌ OFFLINE"
            reports.append(f"{node['name']}: {status_emoji}")
        return "\n".join(reports)

    def initial_check(self):
        self.log("-" * 60)
        self.log("📋 TRẠNG THÁI GIÁM SÁT BAN ĐẦU:")
        for node in WATCH_LIST:
            alive = self.check_ping(node['ip'])
            status_str = "ONLINE" if alive else "OFFLINE"
            self.log(f"   {status_str:7} | {node['name']} ({node['ip']})")
        self.log("-" * 60)

    def listen_commands(self):
        """Luồng lắng nghe lệnh từ Telegram (Interactive Mode)"""
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        self.log("💬 Luồng lắng nghe Telegram đã bắt đầu...")
        
        while True:
            try:
                params = {"offset": self.last_update_id + 1, "timeout": 30}
                response = requests.get(url, params=params, timeout=35).json()
                
                if response.get("ok") and response.get("result"):
                    for update in response["result"]:
                        self.last_update_id = update["update_id"]
                        if "message" in update and "text" in update["message"]:
                            msg_text = update["message"]["text"].lower()
                            from_id = str(update["message"]["chat"]["id"])
                            
                            # Chỉ phản hồi nếu đúng là sếp nhắn
                            if from_id == str(CHAT_ID):
                                if msg_text == "/ping":
                                    self.notify("RESPONSE", "Báo cáo nội bộ", "Pong! Đặc vụ vẫn đang gác cửa Sân Golf sếp ơi! 🫡")
                                elif msg_text == "/status":
                                    current_status = self.get_full_status()
                                    self.notify("RESPONSE", "Báo cáo hiện trạng", f"Trạng thái thiết bị tại Sân Golf:\n\n{current_status}")
            except Exception as e:
                time.sleep(10) # Tránh lặp lỗi quá nhanh

    def start(self):
        self.log(f"🚀 Khởi động DinoMac Watchdog Pro v{VERSION}")
        self.log(f"📍 Chạy trên: {self.hostname} ({self.local_ip})")
        
        # Bắn tin chào hỏi tới Telegram
        location_info = f"Đặc vụ Gác cổng đã trực tuyến tại {self.hostname} ({self.local_ip}). Bắt đầu giám sát Sân Golf.\nPhiên bản: {VERSION}"
        self.notify("ONLINE", "Hệ thống Watchdog", location_info)
        self.log("🟢 Đã gửi lời chào khởi động tới Telegram!")

        # Khởi động luồng lắng nghe riêng biệt
        threading.Thread(target=self.listen_commands, daemon=True).start()

        while True:
            for node in WATCH_LIST:
                nid = node['id']
                alive = self.check_node(node)
                
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
            time.sleep(300)

if __name__ == "__main__":
    try:
        Dino_Watchdog = DinoWatchdog()
        Dino_Watchdog.start()
    except KeyboardInterrupt:
        print("\nStopping Watchdog...")
