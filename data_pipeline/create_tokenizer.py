#!/usr/bin/env python3
"""
Create a simple HuggingFace WordPiece-style tokenizer from normalized paths.
This requires 'tokenizers' library.
"""
import json
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, processors, normalizers
from tokenizers.pre_tokenizers import Whitespace

SAMPLE_FILE = "../data/parsed_requests.csv"
OUT = "../kortex_model/tokenizer.json"

def build_tokenizer(samples, out=OUT):
    tokenizer = Tokenizer(models.WordPiece(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.WordPieceTrainer(vocab_size=4000, min_frequency=2, special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])
    tokenizer.train_from_iterator(samples, trainer=trainer)
    tokenizer.post_processor = processors.TemplateProcessing(single="[CLS] $A [SEP]", pair="[CLS] $A [SEP] $B:1 [SEP]:1", special_tokens=[("[CLS]",1),("[SEP]",2)])
    tokenizer.save(out)
    print("Saved tokenizer to", out)

def sample_paths_from_csv(path=SAMPLE_FILE, limit=10000):
    import csv
    out = []
    try:
        with open(path) as f:
            r = csv.DictReader(f)
            for i,row in enumerate(r):
                out.append(row.get("path",""))
                if i >= limit:
                    break
    except FileNotFoundError:
        print("No parsed CSV found:", path)
    return out

if __name__ == "__main__":
    samples = sample_paths_from_csv()
    if not samples:
        samples = ["/wars/app1/vulnerable-sqli.jsp?uid=1", "/wars/app2/reflected-xss.jsp?msg=hello"]
    build_tokenizer(samples)
