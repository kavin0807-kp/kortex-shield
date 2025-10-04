from tokenizers import Tokenizer, models, trainers, pre_tokenizers
from transformers import PreTrainedTokenizerFast
import os

INPUT_PATH = "data_pipeline/parsed_data/normalized_logs.txt"
OUTPUT_PATH = "kortex_model/tokenizer.json"

def create_tokenizer():
    if not os.path.exists(INPUT_PATH):
        print(f"[!] Normalized log file not found: {INPUT_PATH}. Run normalize.py first.")
        return
    
    # Train tokenizer (WordLevel)
    tokenizer = Tokenizer(models.WordLevel(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.WordLevelTrainer(
        special_tokens=["[UNK]", "[PAD]", "[MASK]"]
    )
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        tokenizer.train_from_iterator(f, trainer)

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    tokenizer.save(OUTPUT_PATH)

    # Wrap into Hugging Face interface
    hf_tokenizer = PreTrainedTokenizerFast(tokenizer_file=OUTPUT_PATH)

    # Force-add special tokens
    if hf_tokenizer.pad_token is None:
        hf_tokenizer.add_special_tokens({"pad_token": "[PAD]"})
    if hf_tokenizer.mask_token is None:
        hf_tokenizer.add_special_tokens({"mask_token": "[MASK]"})

    # Save Hugging Face tokenizer package
    hf_tokenizer.save_pretrained("kortex_model")

    print(f"[+] Tokenizer with vocab size {hf_tokenizer.vocab_size} saved -> {OUTPUT_PATH}")

if __name__ == "__main__":
    create_tokenizer()
