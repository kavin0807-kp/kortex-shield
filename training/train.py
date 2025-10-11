import os, torch, subprocess, numpy as np, evaluate
from torch.utils.data import Dataset
from transformers import BertConfig, BertForSequenceClassification, PreTrainedTokenizerFast, Trainer, TrainingArguments, DataCollatorWithPadding
from datasets import Dataset as HFDataset

NORMALIZED_LOGS = "data_pipeline/parsed_data/normalized_logs.txt"
MALICIOUS_LOGS = "malicious_payloads.txt"
TOKENIZER_DIR = "kortex_model"
MODEL_SAVE_DIR = "kortex_model"

def load_or_rebuild_tokenizer():
    try:
        tok = PreTrainedTokenizerFast.from_pretrained(TOKENIZER_DIR)
        if tok.vocab_size == 0: raise ValueError("Empty vocab")
        return tok
    except Exception:
        print("[!] Tokenizer invalid/missing. Rebuilding..."); subprocess.run(["python3","data_pipeline/create_tokenizer.py"],check=True)
        return PreTrainedTokenizerFast.from_pretrained(TOKENIZER_DIR)

tokenizer = load_or_rebuild_tokenizer()
if tokenizer.pad_token is None: tokenizer.add_special_tokens({'pad_token': '[PAD]'})

accuracy_metric = evaluate.load("accuracy")
f1_metric = evaluate.load("f1")
def compute_metrics(eval_pred):
    logits, labels = eval_pred; predictions = np.argmax(logits, axis=-1)
    accuracy = accuracy_metric.compute(predictions=predictions, references=labels)
    f1 = f1_metric.compute(predictions=predictions, references=labels)
    return {"accuracy": accuracy["accuracy"], "f1": f1["f1"]}

def load_data():
    data = []
    with open(NORMALIZED_LOGS, "r") as f:
        for line in f:
            if line.strip(): data.append({"text": line.strip(), "label": 0})
    with open(MALICIOUS_LOGS, "r") as f:
        for line in f:
            if line.strip() and not line.startswith("#"): data.append({"text": line.strip(), "label": 1})
    print(f"[+] Loaded {len(data)} total samples.")
    return HFDataset.from_list(data)

def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

full_dataset = load_data().map(tokenize_function, batched=True)
train_test_split = full_dataset.train_test_split(test_size=0.1)
train_dataset = train_test_split["train"]
eval_dataset = train_test_split["test"]

config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512, max_position_embeddings=128, num_labels=2, id2label={0:"BENIGN", 1:"MALICIOUS"}, label2id={"BENIGN":0, "MALICIOUS":1}, pad_token_id=tokenizer.pad_token_id)
model = BertForSequenceClassification(config)
print(f"[+] Classification model created: {model.num_parameters():,} parameters.")

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
training_args = TrainingArguments(output_dir="./training_results", overwrite_output_dir=True, num_train_epochs=3, per_device_train_batch_size=16, per_device_eval_batch_size=16, logging_steps=50, report_to="none", save_strategy="epoch", evaluation_strategy="epoch", learning_rate=5e-5, load_best_model_at_end=True)
trainer = Trainer(model=model, args=training_args, train_dataset=train_dataset, eval_dataset=eval_dataset, compute_metrics=compute_metrics, data_collator=data_collator)

print("[+] Supervised training started..."); trainer.train(); print("[+] Training finished.")
trainer.save_model(MODEL_SAVE_DIR)
print(f"✅ Best classification model saved to -> {MODEL_SAVE_DIR}")
