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
# type: "ping" for hardware, "rpc" for blockchain/api
WATCH_LIST = [
    {"name": "Synology NAS (Sân Golf)", "id": "NAS", "ip": "onecloud.tail030e1.ts.net", "type": "ping"},
    {"name": "Master PC (Sân Golf)",    "id": "PC",  "ip": "master-pc.tail030e1.ts.net", "type": "ping"},
    # Future Blockchain node example:
    # {"name": "Ethereum Node", "id": "ETH", "rpc": "http://localhost:8545", "type": "rpc"}
]

class DinoWatchdog:
    def __init__(self):
        self.fails = {node['id']: 0 for node in WATCH_LIST}
        self.last_heights = {}

    def log(self, text):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}")

    def notify(self, status, name, msg):
        emoji = "🔴" if status == "CRITICAL" else "🟢"
        full_msg = f"{emoji} [DinoMac Watchdog - {status}]\n\n📌 Mục tiêu: {name}\n📝 Thông báo: {msg}\n⏰ Lúc: {datetime.now().strftime('%H:%M:%S')}"
        
        if not TELEGRAM_TOKEN or not CHAT_ID:
            self.log("Lỗi: Chưa cấu hình TELEGRAM_BOT_TOKEN hoặc TELEGRAM_CHAT_ID trong .env")
            return
            
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, json={"chat_id": CHAT_ID, "text": full_msg}, timeout=10)
        except Exception as e:
            self.log(f"Lỗi gửi Telegram: {e}")

    def check_ping(self, ip):
        # Universal ping command
        param = "-n 1 -w 2000" if os.name == 'nt' else "-c 1 -W 2"
        # Silence output
        quiet = "> NUL 2>&1" if os.name == 'nt' else "> /dev/null 2>&1"
        return os.system(f"ping {param} {ip} {quiet}") == 0

    def check_rpc(self, node):
        # Optional: Placeholder for blockchain RPC checks
        try:
            payload = {"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1}
            r = requests.post(node['rpc'], json=payload, timeout=5)
            if r.status_code == 200:
                result = r.json().get('result')
                return int(result, 16) if isinstance(result, str) else result
        except:
            return None

    def start(self):
        self.log("🚀 DinoMac Watchdog Pro started. Monitoring Golf Course via Tailscale...")
        self.log("Mode: EXTERNAL (Running on VPS/Home to monitor Sân Golf)")
        
        while True:
            for node in WATCH_LIST:
                nid = node['id']
                name = node['name']
                
                is_alive = False
                if node['type'] == "ping":
                    is_alive = self.check_ping(node['ip'])
                elif node['type'] == "rpc":
                    res = self.check_rpc(node)
                    is_alive = res is not None
                
                if not is_alive:
                    self.fails[nid] += 1
                    self.log(f"🔴 Fail: {name} (Attempt {self.fails[nid]})")
                    
                    # Alert at exactly 3 fails (~15 mins)
                    if self.fails[nid] == 3:
                        msg = "Thiết bị Offline. Internet Sân Golf có thể đã bị ngắt hoặc thiết bị mất điện."
                        self.notify("CRITICAL", name, msg)
                else:
                    # If it was down but now back up
                    if self.fails[nid] >= 3:
                        self.notify("RECOVERED", name, "Thiết bị đã trực tuyến trở lại.")
                    
                    if self.fails[nid] > 0:
                        self.log(f"🟢 OK: {name} is back.")
                        
                    self.fails[nid] = 0
            
            time.sleep(300) # Wait 5 minutes

if __name__ == "__main__":
    try:
        Watchdog = DinoWatchdog()
        Watchdog.start()
    except KeyboardInterrupt:
        print("\nStopping Watchdog...")
