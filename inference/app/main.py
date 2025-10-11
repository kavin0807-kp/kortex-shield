from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
import os
import torch
from transformers import AutoConfig, AutoModelForSequenceClassification
from tokenizers import Tokenizer
from typing import Dict
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

MODEL_DIR = "/app/kortex_model"
MODEL_PATH = os.path.join(MODEL_DIR, "kortex_model.pt")  # produced by training/train.py
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.json")

app = FastAPI(title="Kortex Inference")

# Prometheus metrics
REQUEST_COUNT = Counter("kortex_requests_total", "Total inference requests")
REQUEST_LATENCY = Histogram("kortex_request_latency_seconds", "Inference latency seconds")

# Lazy load
model = None
tokenizer = None
device = "cpu"

class AnalyzeRequest(BaseModel):
    path: str
    method: str = "GET"
    headers: Dict[str, str] = {}

def load_model():
    global model, tokenizer
    if model is None:
        if os.path.exists(MODEL_PATH):
            print("Loading model from", MODEL_PATH)
            # Expecting a saved torch checkpoint with model state dict and config name
            ckpt = torch.load(MODEL_PATH, map_location=device)
            model_name = ckpt.get("model_name", None)
            if model_name:
                config = AutoConfig.from_pretrained(model_name)
                model = AutoModelForSequenceClassification.from_config(config)
                model.load_state_dict(ckpt["state_dict"])
            else:
                # fallback: saved full model
                model = ckpt["model"]
            model.eval()
        else:
            print("Model not found at", MODEL_PATH, "- returning dummy responses.")
            model = None
        if os.path.exists(TOKENIZER_PATH):
            tokenizer = Tokenizer.from_file(TOKENIZER_PATH)
        else:
            tokenizer = None

@app.on_event("startup")
def startup_event():
    load_model()

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    REQUEST_COUNT.inc()
    t0 = time.time()
    # Basic input normalization
    text = req.path.lower()
    # Tokenize with tokenizer if available
    score = 0.0
    label = "unknown"
    if model is None:
        label = "benign"
        score = 0.01
    else:
        # A simple deterministic mapping: token ids sum -> fake logits if model absent
        try:
            enc = tokenizer.encode(text).ids if tokenizer else [1]
            ids = torch.tensor([enc], dtype=torch.long)
            with torch.no_grad():
                out = model(ids)
                logits = out.logits[0].cpu().numpy()
                import numpy as np
                probs = np.exp(logits) / np.sum(np.exp(logits))
                score = float(probs.max())
                label = "malicious" if probs.argmax() == 1 else "benign"
        except Exception as e:
            label = "error"
            score = 0.0

    REQUEST_LATENCY.observe(time.time() - t0)
    return {"label": label, "score": score, "path": req.path}

@app.get("/metrics")
def metrics():
    return generate_latest()
