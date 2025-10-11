#!/usr/bin/env bash
set -e
CYAN='\033[0;36m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; RESET='\033[0m'
progress_bar() { local D=${1} M=${2}; C=$(tput cols 2>/dev/null||echo 80); W=$((C-${#M}-10)); echo -e -n "${CYAN}${M}${RESET} ["; for i in $(seq 1 $W); do sleep $(bc -l<<<"$D/$W"); echo -n "▓"; done; echo -e "] ${GREEN}COMPLETE${RESET}"; }
clear; echo -e "${CYAN}"; cat << "EOF"
    _  __         __          ___________     .__.__    ___________.__
   / |/ |_______|  | __ ____ \_   _____/____ |__|  |   \__    ___/|  |__
  /    ~   /  ___/  |/ // __ \ |    __) \__  \|  |  |     |    |   |  |  \
 /     |   \___ \|    <\  ___/ |     \   / __ \|  |  |__   |    |   |   Y  \
/______|__ /____  >__|_ \\___  > \___  /  (____  /__|____/   |____|   |___|  /
               \/     \/    \/      \/        \/                         \/
EOF
echo -e "${RESET}"; echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${YELLOW}        KORTEX SHIELD :: AI-DRIVEN ANOMALY DETECTION SYSTEM        ${RESET}"
echo -e "${BLUE}=======================================================================${RESET}"; sleep 1; echo ""
progress_bar 1 "🧠 Initializing System..."
echo -e "${CYAN}┠─[ PHASE 1: ALLOCATING FILE SYSTEM NODES ]${RESET}"; sleep 0.5
mkdir -p nginx/logs nginx/auth kortex_model detections data_pipeline/parsed_data
echo -e "${GREEN}┃  ✔ Directory structure synchronized.${RESET}"; echo ""
echo -e "${CYAN}┠─[ PHASE 2: ESTABLISHING SECURE ACCESS PROTOCOL ]${RESET}"; sleep 0.5
if [ -f "nginx/auth/.htpasswd" ]; then echo -e "${YELLOW}┃  ! Secure access credentials already exist.${RESET}"; else
    echo -e "${YELLOW}┃  ! User intervention required for credential generation.${RESET}"; read -p "┃  Enter ACCESS USERNAME: " username
    echo -e "${YELLOW}┃  [*] Awaiting secure password input...${RESET}"; htpasswd -c nginx/auth/.htpasswd "$username"
    echo -e "${GREEN}┃  ✔ Authentication token successfully generated.${RESET}"; fi
echo ""; echo -e "${CYAN}┠─[ PHASE 3: CONFIGURING PERMISSIONS MATRIX ]${RESET}"; sleep 0.5
echo -e "${YELLOW}┃  Querying container runtime for Nginx User ID...${RESET}"
NGINX_UID=$(docker run --rm nginx:1.25 id -u nginx 2>/dev/null || { docker pull nginx:1.25 > /dev/null && docker run --rm nginx:1.25 id -u nginx; })
echo -e "${GREEN}┃  ✔ Nginx User ID identified as: ${NGINX_UID}${RESET}"
sudo chown -R $NGINX_UID:$NGINX_UID nginx/logs detections
echo -e "${GREEN}┃  ✔ Data stream write-permissions granted.${RESET}"; echo ""
progress_bar 1 "✅ System Configuration Complete."; echo ""
echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${YELLOW}                       MISSION BRIEFING                              ${RESET}"
echo -e "${BLUE}=======================================================================${RESET}"
echo -e "${CYAN}You are now ready to run the full training and deployment pipeline:${RESET}"
echo -e "${GREEN}./run_training_pipeline.sh${RESET}"
echo -e "${BLUE}=======================================================================${RESET}"
