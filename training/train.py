import os
import sys
import subprocess
import torch
from torch.utils.data import Dataset
from transformers import (
    BertConfig, BertForMaskedLM, PreTrainedTokenizerFast,
    DataCollatorForLanguageModeling, Trainer, TrainingArguments
)

# --- Ensure accelerate is available ---
def ensure_accelerate():
    try:
        import accelerate
        from packaging import version
        if version.parse(accelerate.__version__) < version.parse("0.26.0"):
            raise ImportError(f"accelerate version {accelerate.__version__} is too old")
    except Exception as e:
        print(f"[!] Accelerate not found or outdated: {e}")
        print("[*] Installing/Upgrading accelerate...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "accelerate"])
        import accelerate
        print(f"[+] Installed accelerate {accelerate.__version__}")

ensure_accelerate()

# --- Paths ---
NORMALIZED_LOGS = "data_pipeline/parsed_data/normalized_logs.txt"
TOKENIZER_DIR = "kortex_model"
MODEL_OUTPUT_FILE = os.path.join(TOKENIZER_DIR, "kortex_model.bin")

if not os.path.exists(NORMALIZED_LOGS):
    print(f"[!] Error: Missing normalized logs at {NORMALIZED_LOGS}. Run the data pipeline first.")
    exit(1)

# --- Tokenizer handling ---
def load_or_rebuild_tokenizer():
    try:
        tokenizer = PreTrainedTokenizerFast.from_pretrained(TOKENIZER_DIR)

        # Ensure required special tokens exist
        if tokenizer.pad_token is None:
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        if tokenizer.mask_token is None:
            tokenizer.add_special_tokens({'mask_token': '[MASK]'})

        if tokenizer.vocab_size == 0:
            raise ValueError("Empty vocab")
        print(f"[+] Loaded existing tokenizer (vocab size: {tokenizer.vocab_size})")
        return tokenizer
    except Exception as e:
        print(f"[!] Tokenizer invalid or missing: {e}")
        print("[*] Rebuilding tokenizer now...")
        subprocess.run(["python3", "create_tokenizer.py"], check=True)

        tokenizer = PreTrainedTokenizerFast.from_pretrained(TOKENIZER_DIR)

        # Ensure special tokens again after rebuild
        if tokenizer.pad_token is None:
            tokenizer.add_special_tokens({'pad_token': '[PAD]'})
        if tokenizer.mask_token is None:
            tokenizer.add_special_tokens({'mask_token': '[MASK]'})

        print(f"[+] Tokenizer rebuilt (vocab size: {tokenizer.vocab_size})")
        return tokenizer

tokenizer = load_or_rebuild_tokenizer()

# --- Dataset ---
class LogsDataset(Dataset):
    def __init__(self, file_path, tokenizer, max_length=128):
        with open(file_path, "r", encoding="utf-8") as f:
            self.lines = [line.strip() for line in f if line.strip()]
        if not self.lines:
            print(f"[!] No data found in {file_path}. Cannot train on empty dataset.")
            exit(1)
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.lines)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.lines[idx],
            truncation=True,
            max_length=self.max_length,
            padding="max_length",
            return_tensors="pt"
        )
        return {key: val.squeeze() for key, val in encoding.items()}

dataset = LogsDataset(NORMALIZED_LOGS, tokenizer)
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.15
)

# --- Model ---
config = BertConfig(
    vocab_size=tokenizer.vocab_size,
    hidden_size=256,
    num_hidden_layers=4,
    num_attention_heads=4,
    intermediate_size=512,
    max_position_embeddings=128
)
model = BertForMaskedLM(config)
print(f"[+] Model created with {model.num_parameters():,} trainable parameters.")

# --- Training ---
training_args = TrainingArguments(
    output_dir="./training_results",
    overwrite_output_dir=True,
    num_train_epochs=5,
    per_device_train_batch_size=32,
    save_steps=10_000,
    save_total_limit=1,
    logging_steps=100,
    report_to="none",
    fp16=torch.cuda.is_available()
)
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
)

print("[+] Training started...")
trainer.train()
print("[+] Training finished.")

os.makedirs(os.path.dirname(MODEL_OUTPUT_FILE), exist_ok=True)
torch.save(model.state_dict(), MODEL_OUTPUT_FILE)
print(f"✅ Model saved -> {MODEL_OUTPUT_FILE}")
