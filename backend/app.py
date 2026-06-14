from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from log_parser import load_logs, generate_sample_logs
from detector import detect_threats

app = Flask(__name__)
CORS(app)

LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs', 'sample.log')
LOG_PATH = os.path.normpath(LOG_PATH)

@app.route('/api/threats', methods=['GET'])
def get_threats():
    if not os.path.exists(LOG_PATH):
        generate_sample_logs()
    df = load_logs(LOG_PATH)
    threats = detect_threats(df)
    return jsonify(threats)

@app.route('/api/logs', methods=['GET'])
def get_logs():
    if not os.path.exists(LOG_PATH):
        generate_sample_logs()
    df = load_logs(LOG_PATH)
    return jsonify(df.to_dict(orient='records'))

@app.route('/api/summary', methods=['GET'])
def get_summary():
    if not os.path.exists(LOG_PATH):
        generate_sample_logs()
    df = load_logs(LOG_PATH)
    threats = detect_threats(df)
    total = len(threats)
    threat_count = sum(1 for t in threats if t['threat_detected'])
    return jsonify({
        'total_ips': total,
        'threats_detected': threat_count,
        'clean_ips': total - threat_count,
        'threat_percentage': round((threat_count / total) * 100, 1) if total > 0 else 0
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)