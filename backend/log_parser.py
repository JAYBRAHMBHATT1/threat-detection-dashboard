import re
import pandas as pd
import random
import time
import threading
import os
from datetime import datetime

# Pool of realistic IPs - mix of normal and malicious
NORMAL_IPS = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "10.0.0.1", "10.0.0.2"]
MALICIOUS_IPS = ["185.220.101.1", "45.33.32.156", "192.241.235.193", "198.199.119.161"]

NORMAL_PAGES = ["/index.html", "/about.html", "/products.html", "/contact.html", "/blog.html"]
ATTACK_PATHS = ["/admin", "/wp-admin", "/phpmyadmin", "/.env", "/config.php", "/.git"]

def generate_log_line(ip, path, status, method="GET"):
    timestamp = datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")
    size = random.randint(128, 8192)
    return f'{ip} - - [{timestamp}] "{method} {path} HTTP/1.1" {status} {size}'

def generate_live_logs(filepath, interval=3):
    """Continuously write new log entries to simulate live traffic."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    def write_logs():
        while True:
            lines = []
            # Normal traffic
            for _ in range(random.randint(2, 4)):
                ip = random.choice(NORMAL_IPS)
                path = random.choice(NORMAL_PAGES)
                lines.append(generate_log_line(ip, path, 200))

            # Simulate attacks randomly
            if random.random() < 0.6:
                attacker = random.choice(MALICIOUS_IPS)
                # Brute force
                for _ in range(random.randint(3, 6)):
                    lines.append(generate_log_line(attacker, "/login", 401, "POST"))
                # Directory scanning
                for path in random.sample(ATTACK_PATHS, random.randint(2, 4)):
                    lines.append(generate_log_line(attacker, path, random.choice([403, 404])))

            with open(filepath, 'a') as f:
                f.write('\n'.join(lines) + '\n')

            time.sleep(interval)

    thread = threading.Thread(target=write_logs, daemon=True)
    thread.start()

def parse_log_line(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] "(.*?)" (\d+) (\d+)'
    match = re.match(pattern, line)
    if match:
        return {
            'ip': match.group(1),
            'timestamp': match.group(2),
            'request': match.group(3),
            'status_code': int(match.group(4)),
            'bytes': int(match.group(5))
        }
    return None

def load_logs(filepath):
    """Load last 200 lines from log file."""
    if not os.path.exists(filepath):
        return pd.DataFrame()
    parsed = []
    with open(filepath, 'r') as f:
        lines = f.readlines()[-200:]
    for line in lines:
        result = parse_log_line(line.strip())
        if result:
            parsed.append(result)
    if not parsed:
        return pd.DataFrame()
    return pd.DataFrame(parsed)