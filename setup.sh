#!/usr/bin/env bash
set -euo pipefail

# Basic setup script to create directories, htpasswd and initial logs.
# Run: sudo bash setup.sh

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Creating required directories..."
mkdir -p "$BASE_DIR/nginx/logs"
mkdir -p "$BASE_DIR/nginx/auth"
mkdir -p "$BASE_DIR/wars"
mkdir -p "$BASE_DIR/kortex_model"

# Create placeholder nginx log files
touch "$BASE_DIR/nginx/logs/access.log" "$BASE_DIR/nginx/logs/error.log"

# Create a basic htpasswd file (username:kortexadmin). Replace password interactively.
if ! command -v htpasswd >/dev/null 2>&1; then
  echo "Installing apache2-utils (htpasswd)..."
  if command -v apt-get >/dev/null 2>&1; then
    apt-get update && apt-get install -y apache2-utils
  elif command -v yum >/dev/null 2>&1; then
    yum install -y httpd-tools
  else
    echo "Please install 'apache2-utils' or 'httpd-tools' to create htpasswd, or create .htpasswd manually."
  fi
fi

HTPASS="$BASE_DIR/nginx/auth/.htpasswd"
if [ ! -f "$HTPASS" ]; then
  echo "Creating htpasswd user 'kortexadmin' (you will be prompted for password)..."
  htpasswd -cb "$HTPASS" kortexadmin kortexadmin
  echo "Created $HTPASS with default password 'kortexadmin'. Change it immediately with: htpasswd $HTPASS kortexadmin"
else
  echo "$HTPASS already exists, skipping."
fi

echo "Setup complete. Run 'docker-compose up --build' to start services."
