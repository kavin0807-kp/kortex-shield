import json, os, urllib.parse, base64, math
from collections import Counter
INPUT_PATH = "data_pipeline/parsed_data/parsed_logs.json"
OUTPUT_PATH = "data_pipeline/parsed_data/normalized_logs.txt"
def decode_string(s):
    try:
        d = urllib.parse.unquote_plus(s);
        if d != s: return decode_string(d)
    except Exception: d = s
    try:
        d += '='*(-len(d)%4); b = base64.b64decode(d).decode('utf-8','ignore')
        if sum(c.isprintable() for c in b)/len(b) > 0.8: return decode_string(b)
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
def normalize(entry):
    m, p, s, a = entry.get("method","N"), entry.get("path","N"), entry.get("status","N"), entry.get("agent","N").split("/")[0] if entry.get("agent") else "N"
    dp = decode_string(p) if p else "NULL"; fs = categorize_features(dp)
    return f"{m} {dp} {fs} status={s} agent={a}"
def normalize_logs():
    if not os.path.exists(INPUT_PATH): print("[!] Parsed log file not found. Run parse_logs.py first."); return
    with open(INPUT_PATH, "r") as f: records = json.load(f)
    with open(OUTPUT_PATH, "w") as out:
        for entry in records: out.write(normalize(entry)+"\n")
    print(f"[+] Normalized {len(records)} logs with enhanced features -> {OUTPUT_PATH}")
if __name__ == "__main__": normalize_logs()
