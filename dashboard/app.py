import json
import os
from flask import Flask, render_template

app = Flask(__name__)

# Log file path inside container
LOG_FILE = "detections.log"

# Ensure log file exists
if not os.path.exists(LOG_FILE):
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
                    # Skip malformed lines
                    print("Skipping invalid JSON:", line)
                    continue
    except FileNotFoundError:
        print(f"Log file not found: {LOG_FILE}")

    # Show newest detections first
    detections.reverse()

    return render_template('index.html', detections=detections)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
