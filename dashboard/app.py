import json
import os
from flask import Flask, render_template

app = Flask(__name__)
LOG_FILE = "detections/detections.log"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    open(LOG_FILE, "w").close()

@app.route('/')
def home():
    detections = []

    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    detections.append(json.loads(line))
                except json.JSONDecodeError:
                    # Auto-fix double quotes in payload
                    fixed_line = line.replace('""', '"')
                    try:
                        detections.append(json.loads(fixed_line))
                    except json.JSONDecodeError:
                        print("Skipping invalid JSON:", line)
                        continue
    except FileNotFoundError:
        print(f"Log file not found: {LOG_FILE}")

    detections.reverse()
    return render_template('index.html', detections=detections)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
