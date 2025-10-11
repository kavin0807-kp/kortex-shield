#!/usr/bin/env python3
"""
Parse nginx access.log into CSV lines with structured features for training.
"""
import re
import csv
from datetime import datetime
from pathlib import Path

LOG = Path("../nginx/logs/access.log")
OUT = Path("../data/parsed_requests.csv")

# Regex for combined log format
LOG_RE = re.compile(r'(?P<ip>\S+) \S+ \S+ \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+)(?: \S+)?" (?P<status>\d{3}) (?P<size>\S+) "(?P<ref>[^"]*)" "(?P<ua>[^"]*)"')

def parse_line(line):
    m = LOG_RE.match(line)
    if not m:
        return None
    gd = m.groupdict()
    # convert time
    try:
        ts = datetime.strptime(gd["time"].split()[0], "%d/%b/%Y:%H:%M:%S")
    except Exception:
        ts = None
    return {
        "ip": gd["ip"],
        "time": ts.isoformat() if ts else "",
        "method": gd["method"],
        "path": gd["path"],
        "status": gd["status"],
        "size": gd["size"],
        "referrer": gd["ref"],
        "user_agent": gd["ua"],
    }

def main():
    if not LOG.exists():
        print("Log file not found:", LOG)
        return

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open() as lf, OUT.open("w", newline='') as outf:
        writer = csv.DictWriter(outf, fieldnames=["ip","time","method","path","status","size","referrer","user_agent"])
        writer.writeheader()
        for line in lf:
            parsed = parse_line(line.strip())
            if parsed:
                writer.writerow(parsed)
    print("Wrote parsed CSV to", OUT)

if __name__ == "__main__":
    main()
