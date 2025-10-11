#!/usr/bin/env python3
"""
Fine-tune loop: loads latest checkpoint and trains on new labeled examples.
Designed for safe continuous learning pipeline.
"""
import torch
from pathlib import Path
from training.train import load_training_data, SimpleDataset, collate_batch
from tokenizers import Tokenizer
from torch.utils.data import DataLoader

CKPT = Path("../kortex_model/kortex_model.pt")
TOKENIZER_PATH = Path("../kortex_model/tokenizer.json")

def incremental_train(epochs=1, lr=1e-5):
    if not CKPT.exists():
        print("No checkpoint found at", CKPT)
        return
    ckpt = torch.load(CKPT, map_location="cpu")
    model_name = ckpt.get("model_name")
    state = ckpt.get("state_dict")
    from transformers import AutoConfig, AutoModelForSequenceClassification, AdamW
    config = AutoConfig.from_pretrained(model_name, num_labels=2)
    model = AutoModelForSequenceClassification.from_config(config)
    model.load_state_dict(state)
    tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH)) if TOKENIZER_PATH.exists() else None

    samples, labels = load_training_data()
    ds = SimpleDataset(samples, labels, tokenizer)
    dl = DataLoader(ds, batch_size=8, shuffle=True, collate_fn=collate_batch)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    opt = AdamW(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        for X, y in dl:
            X = X.to(device)
            y = y.to(device)
            opt.zero_grad()
            out = model(X, labels=y)
            loss = out.loss
            loss.backward()
            opt.step()
        print("Epoch done")

    # save updated checkpoint
    torch.save({
        "model_name": model_name,
        "state_dict": model.state_dict(),
    }, CKPT)
    print("Saved updated checkpoint to", CKPT)

if __name__ == "__main__":
    incremental_train()
