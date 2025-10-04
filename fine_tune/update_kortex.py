import os
import torch
from training.train import LogsDataset
from transformers import (
    BertConfig, BertForMaskedLM, PreTrainedTokenizerFast,
    DataCollatorForLanguageModeling, Trainer, TrainingArguments
)
from data_pipeline.parse_logs import parse_line
from data_pipeline.normalize import normalize

ACCESS_LOG = "nginx/logs/access.log"
TOKENIZER_PATH = "kortex_model/tokenizer.json"
MODEL_PATH = "kortex_model/kortex_model.bin"
UPDATED_MODEL_PATH = "kortex_model/kortex_model.bin"

new_data = [normalize(parsed) for line in open(ACCESS_LOG,"r") if (parsed:=parse_line(line)) and parsed.get("status")=="200"]
if not new_data: print("[!] No new benign logs found to fine-tune on."); exit()

tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
if tokenizer.pad_token is None: tokenizer.add_special_tokens({'pad_token': '[PAD]'})

config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512, max_position_embeddings=128)
model = BertForMaskedLM(config)
model.load_state_dict(torch.load(MODEL_PATH)); model.train()

dataset = LogsDataset.__new__(LogsDataset)
dataset.lines = new_data; dataset.tokenizer = tokenizer; dataset.max_length = 128
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)

training_args = TrainingArguments(output_dir="./finetune_results", overwrite_output_dir=True, num_train_epochs=2, per_device_train_batch_size=16, save_steps=5000, save_total_limit=1, logging_steps=50, report_to="none", fp16=torch.cuda.is_available())
trainer = Trainer(model=model, args=training_args, data_collator=data_collator, train_dataset=dataset)

print(f"[+] Fine-tuning on {len(new_data)} new benign requests..."); trainer.train()
torch.save(model.state_dict(), UPDATED_MODEL_PATH)
print(f"✅ Updated model saved -> {UPDATED_MODEL_PATH}")