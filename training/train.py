import os
import torch
from torch.utils.data import Dataset
from transformers import (
    BertConfig, BertForMaskedLM, PreTrainedTokenizerFast,
    DataCollatorForLanguageModeling, Trainer, TrainingArguments
)

NORMALIZED_LOGS = "data_pipeline/parsed_data/normalized_logs.txt"
TOKENIZER_PATH = "kortex_model/tokenizer.json"
MODEL_OUTPUT_FILE = "kortex_model/kortex_model.bin"

if not all(os.path.exists(p) for p in [NORMALIZED_LOGS, TOKENIZER_PATH]):
    print("[!] Error: Missing required files for training. Run the data pipeline first.")
    exit(1)

class LogsDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        with open(file_path, "r", encoding="utf-8") as f:
            self.lines = [line.strip() for line in f if line.strip()]
        self.tokenizer = tokenizer; self.max_length = max_length
    def __len__(self): return len(self.lines)
    def __getitem__(self, idx):
        encoding = self.tokenizer(self.lines[idx], truncation=True, max_length=self.max_length, padding="max_length", return_tensors="pt")
        return {key: val.squeeze() for key, val in encoding.items()}

tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
if tokenizer.pad_token is None: tokenizer.add_special_tokens({'pad_token': '[PAD]'})

dataset = LogsDataset(NORMALIZED_LOGS, tokenizer)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)
config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512, max_position_embeddings=128)
model = BertForMaskedLM(config)
print(f"[+] Model created with {model.num_parameters():,} trainable parameters.")

training_args = TrainingArguments(output_dir="./training_results", overwrite_output_dir=True, num_train_epochs=5, per_device_train_batch_size=32, save_steps=10_000, save_total_limit=1, logging_steps=100, report_to="none", fp16=torch.cuda.is_available())
trainer = Trainer(model=model, args=training_args, data_collator=data_collator, train_dataset=dataset)

print("[+] Training started..."); trainer.train(); print("[+] Training finished.")
os.makedirs(os.path.dirname(MODEL_OUTPUT_FILE), exist_ok=True)
torch.save(model.state_dict(), MODEL_OUTPUT_FILE)
print(f"✅ Model saved -> {MODEL_OUTPUT_FILE}")