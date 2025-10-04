#!/usr/bin/env bash
set -e

# --- Kortex Shield Automatic Fine-Tuning Script ---
PROJECT_DIR="/path/to/your/kortex-shield" # IMPORTANT: Set this to the ABSOLUTE PATH
LOG_FILE="${PROJECT_DIR}/fine_tune.log"

cd "$PROJECT_DIR" || { echo "ERROR: Project directory not found at $PROJECT_DIR" >> "$LOG_FILE"; exit 1; }

echo "=================================================" >> "$LOG_FILE"
echo "Starting Kortex Shield fine-tuning job at $(date)" >> "$LOG_FILE"
echo "-------------------------------------------------" >> "$LOG_FILE"

echo "[+] Running fine_tune/update_kortex.py..." >> "$LOG_FILE"
python3 fine_tune/update_kortex.py >> "$LOG_FILE" 2>&1

echo "[+] Model fine-tuning successful." >> "$LOG_FILE"
echo "[+] Restarting kortex-shield container to load new model..." >> "$LOG_FILE"
docker compose restart kortex-shield >> "$LOG_FILE" 2>&1
echo "[+] Container restarted successfully." >> "$LOG_FILE"

echo "Fine-tuning job finished at $(date)" >> "$LOG_FILE"
echo "=================================================" >> "$LOG_FILE"; echo "" >> "$LOG_FILE"