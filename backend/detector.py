import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def extract_features(df):
    features = []
    for ip in df['ip'].unique():
        ip_logs = df[df['ip'] == ip]
        failed_logins = len(ip_logs[ip_logs['status_code'] == 401])
        forbidden = len(ip_logs[ip_logs['status_code'] == 403])
        not_found = len(ip_logs[ip_logs['status_code'] == 404])
        total_requests = len(ip_logs)
        unique_paths = ip_logs['request'].nunique()
        features.append({
            'ip': ip,
            'total_requests': total_requests,
            'failed_logins': failed_logins,
            'forbidden_hits': forbidden,
            'not_found_hits': not_found,
            'unique_paths': unique_paths
        })
    return pd.DataFrame(features)

def detect_threats(df):
    feature_df = extract_features(df)
    X = feature_df[['total_requests', 'failed_logins', 'forbidden_hits', 'not_found_hits', 'unique_paths']]
    model = IsolationForest(contamination=0.3, random_state=42)
    feature_df['anomaly'] = model.fit_predict(X)
    feature_df['threat'] = feature_df['anomaly'] == -1

    threats = []
    for _, row in feature_df.iterrows():
        reasons = []
        if row['failed_logins'] >= 3:
            reasons.append("Brute force attack detected")
        if row['not_found_hits'] >= 2:
            reasons.append("Directory scanning detected")
        if row['forbidden_hits'] >= 1:
            reasons.append("Unauthorized access attempt")

        threats.append({
            'ip': row['ip'],
            'threat_detected': row['threat'] or len(reasons) > 0,
            'reasons': reasons,
            'total_requests': int(row['total_requests']),
            'failed_logins': int(row['failed_logins'])
        })

    return threats

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from backend.log_parser import load_logs
    df = load_logs('logs/sample.log')
    threats = detect_threats(df)
    print("\n=== THREAT DETECTION RESULTS ===")
    for t in threats:
        status = "THREAT" if t['threat_detected'] else "CLEAN"
        print(f"[{status}] IP: {t['ip']} | Requests: {t['total_requests']} | Reasons: {t['reasons']}")