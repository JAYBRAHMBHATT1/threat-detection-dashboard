# threat-detection-dashboard
AI-powered real-time security threat detection and monitoring system
# Threat Detection Dashboard

A real-time AI-powered security monitoring system that analyzes web server logs, detects malicious behaviour using machine learning, and displays live alerts on a dashboard.

## What it does

- Parses real Apache/Nginx access logs
- Detects brute force attacks, directory scanning, and unauthorized access attempts
- Uses Isolation Forest ML algorithm to identify anomalous IP behaviour
- Displays live threat alerts on a web dashboard that auto-refreshes every 10 seconds
- REST API built with Flask serving real-time threat data

## Tech Stack

- **Backend:** Python, Flask, scikit-learn, pandas
- **ML Model:** Isolation Forest (anomaly detection)
- **Frontend:** HTML, CSS, JavaScript
- **API:** RESTful endpoints for threats, logs, and summary data

## How to run

1. Clone the repository
   git clone https://github.com/JAYBRAHMBHATT1/threat-detection-dashboard.git

2. Install dependencies
   pip install -r requirements.txt

3. Start the Flask API
   python backend/app.py

4. Open frontend/index.html in your browser

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| /api/threats | Returns threat analysis per IP |
| /api/logs | Returns all parsed log entries |
| /api/summary | Returns summary statistics |

## Threats Detected

- Brute force login attacks (repeated 401s)
- Directory scanning (probing /admin, /phpmyadmin etc)
- Unauthorized access attempts (403s)
- Anomalous traffic patterns via ML

## Author

Jay Brahmbhatt 