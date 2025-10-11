#!/usr/bin/env python3
"""
Normalize request path and parameters for tokenization.
- Lowercase
- Remove long numeric IDs
- Collapse query param names/values to tokens
"""
import re
from urllib.parse import urlparse, parse_qs

NUM_RE = re.compile(r'\b\d{4,}\b')

def normalize_path(path: str) -> str:
    if not path:
        return ""
    u = urlparse(path)
    p = u.path.lower()
    p = NUM_RE.sub('<NUM>', p)
    q = parse_qs(u.query)
    qparts = []
    for k, vals in q.items():
        qparts.append(f"{k}=<VAL>")
    normalized = p + ("?" + "&".join(qparts) if qparts else "")
    return normalized

if __name__ == "__main__":
    # quick demo
    examples = [
        "/user/123456/profile?tab=2",
        "/search?q=hello&id=987654321",
    ]
    for e in examples:
        print(e, "->", normalize_path(e))
