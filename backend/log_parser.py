import re
import pandas as pd
import sys
import os

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

def generate_sample_logs():
    sample_logs = [
        '192.168.1.1 - - [14/Jun/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 1024',
        '10.0.0.5 - - [14/Jun/2026:10:00:03 +0000] "POST /login HTTP/1.1" 401 512',
        '10.0.0.5 - - [14/Jun/2026:10:00:04 +0000] "POST /login HTTP/1.1" 401 512',
        '10.0.0.5 - - [14/Jun/2026:10:00:05 +0000] "POST /login HTTP/1.1" 401 512',
        '185.220.101.1 - - [14/Jun/2026:10:00:08 +0000] "GET /admin HTTP/1.1" 403 256',
        '185.220.101.1 - - [14/Jun/2026:10:00:10 +0000] "GET /wp-admin HTTP/1.1" 404 128',
        '185.220.101.1 - - [14/Jun/2026:10:00:11 +0000] "GET /phpmyadmin HTTP/1.1" 404 128',
        '192.168.1.3 - - [14/Jun/2026:10:00:09 +0000] "GET /products.html HTTP/1.1" 200 4096',
    ]
    os.makedirs('logs', exist_ok=True)
    with open('logs/sample.log', 'w') as f:
        f.write('\n'.join(sample_logs))
    print("Sample logs generated!")

def load_logs(filepath):
    parsed = []
    with open(filepath, 'r') as f:
        for line in f:
            result = parse_log_line(line.strip())
            if result:
                parsed.append(result)
    return pd.DataFrame(parsed)

if __name__ == "__main__":
    print("Starting log parser...")
    generate_sample_logs()
    df = load_logs('logs/sample.log')
    print("Parsed", len(df), "log entries")
    print(df.to_string())