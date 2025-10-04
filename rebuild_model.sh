#!/usr/bin/env bash
set -e

# --- Color Definitions ---
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RESET='\033[0m'

echo -e "${YELLOW}This script will delete the old model and tokenizer and rebuild them.${RESET}"
read -p "Are you sure you want to continue? (y/N) " -n 1 -r; echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then exit 1; fi

echo -e "\n${CYAN}--- Deleting old model files... ---${RESET}"
rm -f kortex_model/tokenizer.json
rm -f kortex_model/kortex_model.bin
echo -e "${GREEN}✔ Done.${RESET}"

echo -e "\n${CYAN}--- Step 1: Re-creating the tokenizer... ---${RESET}"
python3 data_pipeline/create_tokenizer.py

echo -e "\n${CYAN}--- Step 2: Re-training the AI model... ---${RESET}"
python3 training/train.py

echo -e "\n${GREEN}✅ Model rebuilt successfully!${RESET}"
echo -e "${YELLOW}Please run 'docker compose restart kortex-shield' to activate it.${RESET}"