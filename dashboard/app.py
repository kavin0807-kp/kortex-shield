import json
from flask import Flask, render_template
app = Flask(__name__)
LOG_FILE = "/detections/detections.log"
@app.route('/')
def home():
    detections = []
    try:
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try: detections.append(json.loads(line))
                except json.JSONDecodeError: continue
    except FileNotFoundError: pass
    detections.reverse()
    return render_template('index.html', detections=detections)
if __name__ == '__main__': app.run(host='0.0.0.0', port=5001)
