import os, torch, logging, urllib.parse, base64
from fastapi import FastAPI, Request
from transformers import BertConfig, BertForMaskedLM, PreTrainedTokenizerFast

TOKENIZER_PATH = "kortex_model/tokenizer.json"
MODEL_PATH = "kortex_model/kortex_model.bin"
DETECTIONS_LOG_FILE = "detections/detections.log"

logging.basicConfig(
    filename=DETECTIONS_LOG_FILE, level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "client_ip": "%(client_ip)s", "score": %(score).4f, "payload": "%(payload)s"}',
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)

tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
if tokenizer.pad_token is None: tokenizer.add_special_tokens({'pad_token': '[PAD]'})

config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512, max_position_embeddings=128)
device = "cuda" if torch.cuda.is_available() else "cpu"
model = BertForMaskedLM(config)
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device); model.eval()

ANOMALY_THRESHOLD = 2.0
app = FastAPI()

def decode_string(s):
    try:
        decoded_s = urllib.parse.unquote_plus(s);
        if decoded_s != s: return decode_string(decoded_s)
    except Exception: decoded_s = s
    try:
        decoded_s += '=' * (-len(decoded_s) % 4)
        base64_decoded = base64.b64decode(decoded_s).decode('utf-8', 'ignore')
        if sum(c.isprintable() for c in base64_decoded) / len(base64_decoded) > 0.8: return decode_string(base64_decoded)
    except Exception: pass
    return decoded_s

def normalize_request_line(method: str, path: str) -> str:
    decoded_path = decode_string(path) if path else "NULL"
    return f"{method} {decoded_path} status=MIRRORED agent=Unknown"

@app.post("/analyze")
async def analyze_request(request: Request):
    client_ip = request.client.host
    method = request.headers.get("X-Original-Method", "GET")
    path = request.headers.get("X-Original-URI", "/")
    normalized_text = normalize_request_line(method, path)
    inputs = tokenizer(normalized_text, return_tensors="pt", truncation=True, padding="max_length", max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss.item()
    if loss > ANOMALY_THRESHOLD:
        log_extra = {'client_ip': client_ip, 'score': loss, 'payload': f'"{method} {path}"'}
        logging.info("ANOMALY DETECTED", extra=log_extra)
    return {"status": "analyzed"}