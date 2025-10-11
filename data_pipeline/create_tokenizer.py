from tokenizers import Tokenizer, models, trainers, pre_tokenizers
import os
INPUT_PATH = "data_pipeline/parsed_data/normalized_logs.txt"
OUTPUT_PATH = "kortex_model/tokenizer.json"
def create_tokenizer():
    if not os.path.exists(INPUT_PATH): print(f"[!] Normalized log file not found: {INPUT_PATH}."); return
    tokenizer = Tokenizer(models.WordLevel(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = pre_tokenizers.Whitespace()
    trainer = trainers.WordLevelTrainer(special_tokens=["[UNK]", "[PAD]", "[MASK]"])
    with open(INPUT_PATH, "r") as f: tokenizer.train_from_iterator(f, trainer)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True); tokenizer.save(OUTPUT_PATH)
    print(f"[+] Tokenizer with vocab size {tokenizer.get_vocab_size()} saved -> {OUTPUT_PATH}")
if __name__ == "__main__": create_tokenizer()
