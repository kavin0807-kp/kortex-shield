import os, torch, logging, urllib.parse, base64, math
from fastapi import FastAPI, Request
from transformers import BertForSequenceClassification, PreTrainedTokenizerFast
from starlette_prometheus import metrics, PrometheusMiddleware
from collections import Counter
MODEL_DIR = "kortex_model"; DETECTIONS_LOG_FILE = "detections/detections.log"
logging.basicConfig(filename=DETECTIONS_LOG_FILE, level=logging.INFO, format='{"timestamp":"%(asctime)s","client_ip":"%(client_ip)s","prediction":"%(prediction)s","payload":"%(payload)s"}', datefmt='%Y-%m-%dT%H:%M:%S%z')
tokenizer = PreTrainedTokenizerFast.from_pretrained(MODEL_DIR)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = BertForSequenceClassification.from_pretrained(MODEL_DIR); model.to(device); model.eval()
app = FastAPI(); app.add_middleware(PrometheusMiddleware); app.add_route("/metrics", metrics)
def decode_string(s):
    try: d = urllib.parse.unquote_plus(s);
        if d != s: return decode_string(d)
    except Exception: d = s
    try: d += '=' * (-len(d)%4); b = base64.b64decode(d).decode('utf-8','ignore');
        if sum(c.isprintable() for c in b)/len(b)>0.8: return decode_string(b)
    except Exception: pass
    return d
def get_entropy(t):
    if not t: return 0.0
    c = Counter(t); p = [v/len(t) for v in c.values()]; e = -sum(i*math.log2(i) for i in p); return e
def categorize_features(p):
    l, sc, e = len(p), sum(1 for c in p if c in "<>'();&"), get_entropy(p)
    lc = "len=long" if l > 200 else "len=medium" if l > 75 else "len=short"
    scc = "chars=high" if sc > 5 else "chars=low" if sc > 0 else "chars=none"
    ec = "entropy=high" if e > 4.5 else "entropy=medium" if e > 3.5 else "entropy=low"
    return f"{lc} {scc} {ec}"
def normalize_request_line(method: str, path: str) -> str:
    dp = decode_string(path) if path else "NULL"; fs = categorize_features(dp)
    return f"{method} {dp} {fs} status=200 agent=Unknown"
@app.post("/analyze")
async def analyze_request(request: Request):
    client_ip = request.client.host; method = request.headers.get("X-Original-Method", "GET"); path = request.headers.get("X-Original-URI", "/")
    normalized_text = normalize_request_line(method, path)
    inputs = tokenizer(normalized_text, return_tensors="pt", truncation=True, padding="max_length", max_length=128).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits; prediction_id = torch.argmax(logits, dim=1).item(); prediction = model.config.id2label[prediction_id]
    if prediction == "MALICIOUS":
        log_extra = {'client_ip': client_ip, 'prediction': prediction, 'payload': f'"{method} {path}"'}
        logging.info("MALICIOUS DETECTED", extra=log_extra)
    return {"status": "analyzed", "prediction": prediction}
