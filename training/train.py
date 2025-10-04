import os
import torch
from torch.utils.data import Dataset
from transformers import (
    BertConfig, BertForMaskedLM, PreTrainedTokenizerFast,
    DataCollatorForLanguageModeling, Trainer, TrainingArguments
)
from tokenizers import Tokenizer, models, trainers, pre_tokenizers

# --- Define File Paths ---
NORMALIZED_LOGS = "data_pipeline/parsed_data/normalized_logs.txt"
TOKENIZER_PATH = "kortex_model/tokenizer.json"
MODEL_OUTPUT_FILE = "kortex_model/kortex_model.bin"

# --- NEW: Self-Correction Function that RETURNS the tokenizer ---
def load_or_rebuild_tokenizer():
    """Checks if the tokenizer is valid. If not, rebuilds it. Returns a working tokenizer object."""
    must_rebuild = False
    if not os.path.exists(TOKENIZER_PATH):
        must_rebuild = True
    else:
        try:
            # Check if the existing tokenizer has a mask token
            temp_tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
            if temp_tokenizer.mask_token is None:
                must_rebuild = True
        except Exception:
            must_rebuild = True

    if must_rebuild:
        print(f"[!] Tokenizer is invalid or missing. Rebuilding it now...")
        if not os.path.exists(NORMALIZED_LOGS):
            print(f"[!] CRITICAL ERROR: Cannot rebuild tokenizer because {NORMALIZED_LOGS} is missing.")
            exit(1)
        
        # Build a new tokenizer from the tokenizers library
        new_tokenizer = Tokenizer(models.WordLevel(unk_token="[UNK]"))
        new_tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
        trainer = trainers.WordLevelTrainer(special_tokens=["[UNK]", "[PAD]", "[MASK]"])
        with open(NORMALIZED_LOGS, "r") as f:
            new_tokenizer.train_from_iterator(f, trainer)
        
        os.makedirs(os.path.dirname(TOKENIZER_PATH), exist_ok=True)
        new_tokenizer.save(TOKENIZER_PATH)
        print(f"[+] Tokenizer rebuilt successfully.")

    # Always load the file from disk to ensure we use the PreTrainedTokenizerFast class
    final_tokenizer = PreTrainedTokenizerFast(tokenizer_file=TOKENIZER_PATH)
    if final_tokenizer.pad_token is None:
        final_tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    
    return final_tokenizer

# --- Main Training Script ---

# Load the tokenizer using our new robust function
tokenizer = load_or_rebuild_tokenizer()

# Check if the tokenizer is valid one last time before proceeding
if tokenizer.mask_token is None:
    print("[!] CRITICAL FAILURE: The tokenizer was rebuilt but is still invalid. Please check file permissions.")
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

dataset = LogsDataset(NORMALIZED_LOGS, tokenizer)
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=True, mlm_probability=0.15)
config = BertConfig(vocab_size=tokenizer.vocab_size, hidden_size=256, num_hidden_layers=4, num_attention_heads=4, intermediate_size=512, max_position_embeddings=128)
model = BertForMaskedLM(config)
print(f"[+] Model created with {model.num_parameters():,} trainable parameters.")

training_args = TrainingArguments(output_dir="./training_results", overwrite_output_dir=True, num_train_epochs=5, per_device_train_batch_size=32, save_steps=10_000, save_total_limit=1, logging_steps=100, report_to="none", fp16=torch.cuda.is_available())
trainer = Trainer(model=model, args=training_args, data_collator=data_collator, train_dataset=dataset)

print("[+] Starting final training..."); trainer.train(); print("[+] Training finished.")
torch.save(model.state_dict(), MODEL_OUTPUT_FILE)
print(f"✅ Model saved -> {MODEL_OUTPUT_FILE}")