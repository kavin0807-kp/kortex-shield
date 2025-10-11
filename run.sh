#!/usr/bin/env bash
set -e
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; RESET='\033[0m'
print_header() { echo ""; echo -e "${CYAN}┠─[ PHASE ${1}: ${2} ]${RESET}"; sleep 0.5; }
clear; echo -e "${CYAN}"; cat << "EOF"
    _  __         __          ___________     .__.__    ___________.__
   / |/ |_______|  | __ ____ \_   _____/____ |__|  |   \__    ___/|  |__
  /    ~   /  ___/  |/ // __ \ |    __) \__  \|  |  |     |    |   |  |  \
 /     |   \___ \|    <\  ___/ |     \   / __ \|  |  |__   |    |   |   Y  \
/______|__ /____  >__|_ \\___  > \___  /  (____  /__|____/   |____|   |___|  /
               \/     \/    \/      \/        \/                         \/
EOF
echo -e "${RESET}"; echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${YELLOW}       KORTEX SHIELD :: MODEL TRAINING & DEPLOYMENT PIPELINE         ${RESET}"
echo -e "${BLUE}=======================================================================${RESET}"; sleep 1

print_header 1 "SYSTEM ACTIVATION"; echo -e "${YELLOW}┃  Initializing containerized environment...${RESET}"
docker compose up --build -d; echo -e "${GREEN}┃  ✔ Services activated.${RESET}"

print_header 2 "BENIGN TRAFFIC SIMULATION"
echo -e "${YELLOW}┃  Action Required: Please open a NEW terminal window.${RESET}"
echo -e "${YELLOW}┃  In that new terminal, navigate to this project folder and run:${RESET}"
echo -e "${GREEN}┃  python3 benign_crawler/benign_crawler.py${RESET}"
echo -e "${YELLOW}┃  Let it run for 5-10 minutes, then press Ctrl+C in that new window to stop it.${RESET}"; echo ""
read -p "Once you have stopped the crawler, press [Enter] here to continue..."

print_header 3 "COGNITIVE MATRIX CONSTRUCTION"
echo -e "${YELLOW}┃  Parsing raw log data...${RESET}"; python3 data_pipeline/parse_logs.py
echo -e "${YELLOW}┃  Normalizing with feature engineering...${RESET}"; python3 data_pipeline/normalize.py
echo -e "${YELLOW}┃  Generating neural vocabulary (tokenizer)...${RESET}"; python3 data_pipeline/create_tokenizer.py
echo -e "${YELLOW}┃  Executing supervised learning sequence (training model)...${RESET}"; echo -e "${YELLOW}┃  This may take several minutes.${RESET}"; python3 training/train.py

print_header 4 "SHIELD ACTIVATION"; echo -e "${YELLOW}┃  Loading the intelligent matrix into the shield...${RESET}"
docker compose restart kortex-shield; echo -e "${GREEN}┃  ✔ Shield is active.${RESET}"

echo ""; echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${GREEN}                     MISSION COMPLETE                              ${RESET}"
echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${CYAN}Kortex Shield is live and using the supervised model.${RESET}"; echo ""
echo -e "${CYAN}To monitor detections, view the live dashboard at:${RESET}"
echo -e "${GREEN}http://localhost:5001 (or Port 5001 in your cloud environment's Web Preview)${RESET}"; echo ""
echo -e "${BLUE}=======================================================================${RESET}"
