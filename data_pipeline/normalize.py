import json
import os
import urllib.parse
import base64

INPUT_PATH = "data_pipeline/parsed_data/parsed_logs.json"
OUTPUT_PATH = "data_pipeline/parsed_data/normalized_logs.txt"

def decode_string(s):
    try:
        decoded_s = urllib.parse.unquote_plus(s)
        if decoded_s != s: return decode_string(decoded_s)
    except Exception: decoded_s = s
    try:
        decoded_s += '=' * (-len(decoded_s) % 4)
        base64_decoded = base64.b64decode(decoded_s).decode('utf-8', 'ignore')
        if sum(c.isprintable() for c in base64_decoded) / len(base64_decoded) > 0.8:
            return decode_string(base64_decoded)
    except Exception: pass
    return decoded_s

def normalize(entry):
    method = entry.get("method", "NULL")
    path = entry.get("path", "NULL")
    status = entry.get("status", "NULL")
    agent = entry.get("agent", "NULL").split("/")[0] if entry.get("agent") else "NULL"
    decoded_path = decode_string(path) if path else "NULL"
    return f"{method} {decoded_path} status={status} agent={agent}"

def normalize_logs():
    if not os.path.exists(INPUT_PATH):
        print(f"[!] Parsed log file not found at {INPUT_PATH}. Please run parse_logs.py first.")
        return
    with open(INPUT_PATH, "r") as f: records = json.load(f)
    with open(OUTPUT_PATH, "w") as out:
        for entry in records: out.write(normalize(entry) + "\n")
    print(f"[+] Normalized and decoded {len(records)} logs -> {OUTPUT_PATH}")

if __name__ == "__main__":
    normalize_logs()