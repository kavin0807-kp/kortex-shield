import re
import json
import os

LOG_PATH = "nginx/logs/access.log"
OUTPUT_DIR = "data_pipeline/parsed_data"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "parsed_logs.json")

LOG_PATTERN = re.compile(
    r'(?P<ip>[\d\.]+) - (?P<user>[^ ]+) \[(?P<time>[^\]]+)\] '
    r'"(?P<request_line>[^"]+)" '
    r'(?P<status>\d{3}) (?P<size>\d+) '
    r'"(?P<referer>[^"]*)" "(?P<agent>[^"]*)"'
)

def parse_line(line):
    match = LOG_PATTERN.match(line)
    if not match: return None
    data = match.groupdict()
    try:
        parts = data['request_line'].split()
        data['method'] = parts[0]
        data['path'] = parts[1]
    except (ValueError, IndexError):
        data['method'], data['path'] = "INVALID", "INVALID"
    return data

def parse_logs():
    if not os.path.exists(LOG_PATH) or os.path.getsize(LOG_PATH) == 0:
        print(f"[!] Log file is missing or empty at {LOG_PATH}. Please generate traffic first.")
        return
    records = [parsed for line in open(LOG_PATH, "r") if (parsed := parse_line(line))]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w") as out:
        json.dump(records, out, indent=2)
    print(f"[+] Parsed {len(records)} log entries -> {OUTPUT_PATH}")

if __name__ == "__main__":
    parse_logs()