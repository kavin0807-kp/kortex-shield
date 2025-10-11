import re, json, os
LOG_PATH = "nginx/logs/access.log"
OUTPUT_PATH = "data_pipeline/parsed_data/parsed_logs.json"
LOG_PATTERN = re.compile(r'(?P<ip>[\d\.]+) - (?P<user>[^ ]+) \[(?P<time>[^\]]+)\] "(?P<request_line>[^"]+)" (?P<status>\d{3}) (?P<size>\d+) "(?P<referer>[^"]*)" "(?P<agent>[^"]*)"')
def parse_line(line):
    match = LOG_PATTERN.match(line)
    if not match: return None
    data = match.groupdict()
    try: parts = data['request_line'].split(); data['method'] = parts[0]; data['path'] = parts[1]
    except (ValueError, IndexError): data['method'], data['path'] = "INVALID", "INVALID"
    return data
def parse_logs():
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0: print("[!] Log file missing or empty. Please run the crawler first."); return
    records = [p for l in open(LOG_PATH, "r") if (p := parse_line(l))]
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w") as f: json.dump(records, f, indent=2)
    print(f"[+] Parsed {len(records)} log entries -> {OUTPUT_PATH}")
if __name__ == "__main__": parse_logs()
