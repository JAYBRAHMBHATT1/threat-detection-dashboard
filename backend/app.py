from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_parser import load_logs, generate_live_logs
from detector import detect_threats

app = Flask(__name__)
CORS(app)

LOG_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'live.log'
))

generate_live_logs(LOG_PATH, interval=3)

@app.route('/api/threats', methods=['GET'])
def get_threats():
    df = load_logs(LOG_PATH)
    if df.empty:
        return jsonify([])
    return jsonify(detect_threats(df))

@app.route('/api/logs', methods=['GET'])
def get_logs():
    df = load_logs(LOG_PATH)
    if df.empty:
        return jsonify([])
    return jsonify(df.tail(20).to_dict(orient='records'))

@app.route('/api/summary', methods=['GET'])
def get_summary():
    df = load_logs(LOG_PATH)
    if df.empty:
        return jsonify({'total_ips': 0, 'threats_detected': 0, 'clean_ips': 0, 'threat_percentage': 0, 'total_requests': 0})
    threats = detect_threats(df)
    total = len(threats)
    threat_count = sum(1 for t in threats if t['threat_detected'])
    return jsonify({
        'total_ips': total,
        'threats_detected': threat_count,
        'clean_ips': total - threat_count,
        'threat_percentage': round((threat_count / total) * 100, 1) if total > 0 else 0,
        'total_requests': len(df)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)