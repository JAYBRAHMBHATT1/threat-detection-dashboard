from flask import Flask, jsonify
from flask_cors import CORS
from log_parser import load_logs, generate_sample_logs
from detector import detect_threats
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, 'logs', 'sample.log')

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
    app.run(debug=True, port=5000)