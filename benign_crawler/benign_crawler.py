#!/usr/bin/env python3
"""
A simple benign traffic generator to exercise the apps.
Use responsibly; this is for generating diverse but harmless requests.
"""
import requests
import random
import time
from urllib.parse import urljoin

BASE = "http://localhost:80/"  # nginx entry

paths = [
    "wars/app1/index.jsp",
    "wars/app1/vulnerable-sqli.jsp?uid=1",
    "wars/app2/index.jsp",
    "wars/app2/reflected-xss.jsp?msg=hello",
    "wars/app3/index.jsp",
]

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "curl/7.68.0",
    "Mozilla/5.0 (Linux; Android 10)",
]

def random_query_variants():
    return [
        "?uid=1",
        "?uid=2",
        "?uid=10",
        "?msg=hi+there",
    ]

def run(iterations=200, delay=(0.05, 0.3)):
    s = requests.Session()
    for i in range(iterations):
        p = random.choice(paths)
        url = urljoin(BASE, p) + (random.choice(random_query_variants()) if random.random() < 0.2 else "")
        headers = {"User-Agent": random.choice(user_agents)}
        try:
            r = s.get(url, headers=headers, timeout=5)
            print(f"[{i}] {r.status_code} {url}")
        except Exception as e:
            print("request error:", e)
        time.sleep(random.uniform(*delay))

if __name__ == "__main__":
    run()
