#!/usr/bin/env bash
# start_stack.sh - Setup, build and start the kortex-shield stack
# Usage:
#   ./start_stack.sh            # setup, package wars, build images, start stack
#   TRAIN=1 ./start_stack.sh    # also run tokenizer + light training before starting (may be slow)

set -euo pipefail
IFS=$'\n\t'

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
export COMPOSE_PROJECT_NAME=kortex_shield

echo "BASE_DIR=$BASE_DIR"
cd "$BASE_DIR"

# Utilities
log() { printf "\n=== %s ===\n" "$1"; }
err() { printf "ERROR: %s\n" "$1" >&2; exit 1; }

# 1) Run setup.sh to create required dirs and htpasswd (idempotent)
if [ -x "./setup.sh" ]; then
  log "Running setup.sh (creates nginx auth and log dirs if missing)"
  sudo bash ./setup.sh
else
  log "setup.sh not executable; attempting to chmod +x and run"
  chmod +x ./setup.sh || true
  sudo bash ./setup.sh
fi

# 2) Package WARs (create simple .war archives for Tomcat deployment)
log "Packaging WAR files from wars/* directories"
WAR_ROOT="$BASE_DIR/wars"
cd "$WAR_ROOT"
for d in */ ; do
  appdir="${d%/}"
  # Only package if directory contains files
  if [ -d "$appdir" ] && [ -n "$(ls -A "$appdir" 2>/dev/null)" ]; then
    warname="${appdir}.war"
    # If war already exists and is newer than source dir, skip
    if [ -f "$warname" ] && [ "$warname" -nt "$appdir" ]; then
      echo " - $warname up-to-date, skipping"
      continue
    fi
    echo " - Creating $warname from $appdir/"
    # prefer jar tool, fall back to zip
    if command -v jar >/dev/null 2>&1; then
      (cd "$appdir" && jar -cvf "../$warname" .) >/dev/null 2>&1 || true
    else
      (cd "$appdir" && zip -r "../$warname" .) >/dev/null 2>&1 || true
    fi
  fi
done
cd "$BASE_DIR"

# 3) Optionally run tokenizer + (toy) training locally to create kortex model artifacts
if [ "${TRAIN:-0}" != "0" ]; then
  log "TRAIN=1 detected — building tokenizer and running lightweight training (may take time)"
  # ensure virtualenv or python deps available; advise user if missing
  if ! command -v python3 >/dev/null 2>&1; then
    err "python3 is not installed. Install python3 and necessary pip packages (tokenizers, transformers, torch)."
  fi

  # Create data directory if needed
  mkdir -p data

  # Run create_tokenizer.py
  if [ -f "./data_pipeline/create_tokenizer.py" ]; then
    echo " - Creating tokenizer (data_pipeline/create_tokenizer.py)"
    python3 ./data_pipeline/create_tokenizer.py || echo "create_tokenizer.py finished with non-zero exit (continue)"
  else
    echo " - create_tokenizer.py not found, skipping tokenizer build"
  fi

  # Run training script (use --small to keep it light)
  if [ -f "./training/train.py" ]; then
    echo " - Running training/train.py --small (toy training)"
    python3 ./training/train.py --small --epochs 2 || echo "training finished (may have failed) — check logs"
  else
    echo " - training/train.py not found, skipping training"
  fi
else
  log "TRAIN not requested. Skipping tokenizer/training."
fi

# 4) Build docker images and bring up stack
log "Building and starting docker-compose services"

# If docker-compose CLI v2 (docker compose) present, prefer docker compose; else docker-compose
if command -v docker-compose >/dev/null 2>&1; then
  DC="docker-compose"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  DC="docker compose"
else
  err "docker-compose / docker compose not found. Install Docker and docker-compose (or use Docker Desktop)."
fi

# Build (in case inference Dockerfile changed). This will also pull base images.
echo " - Building images with: $DC build --pull --no-cache"
$DC build --pull --no-cache || {
  echo " - Build failed. Trying without --no-cache (fallback)"
  $DC build || true
}

# Start services detached
echo " - Starting services: $DC up -d"
$DC up -d

# 5) Health checks -- simple readiness probes
log "Checking basic service readiness (nginx:80, inference:9000)"

check_http() {
  url="$1"
  expected="$2"  # optional expected string
  for i in $(seq 1 20); do
    if curl -sS --max-time 3 "$url" >/dev/null 2>&1; then
      if [ -z "$expected" ]; then
        echo "   OK: $url"
        return 0
      else
        if curl -sS --max-time 3 "$url" | grep -q "$expected"; then
          echo "   OK: $url (matched expected)"
          return 0
        fi
      fi
    fi
    printf "."
    sleep 1
  done
  echo
  echo "   WARNING: $url did not become ready after retries"
  return 1
}

# NGINX root (proxied to tomcat). If nginx is protected by basic auth, the root should still respond if proxying.
check_http "http://localhost:80/" || echo " - nginx may be unavailable (check containers with 'docker ps')"

# Inference health: attempt to hit /metrics then /analyze
if check_http "http://localhost:9000/metrics"; then
  echo " - inference metrics endpoint OK"
else
  echo " - inference metrics not responding; waiting a bit and re-checking"
  sleep 3
  check_http "http://localhost:9000/metrics" || echo " - inference may be down"
fi

# Try a minimal analyze call (if inference is running). Use JSON minimal request.
if command -v curl >/dev/null 2>&1; then
  echo " - Testing inference /analyze (POST) with sample payload"
  set +e
  resp=$(curl -sS -X POST "http://localhost:9000/analyze" -H "Content-Type: application/json" -d '{"path":"/wars/app1/index.jsp","method":"GET"}' --max-time 5)
  set -e
  if [ -n "$resp" ]; then
    echo "   inference responded: $resp"
  else
    echo "   inference did not return a response (it may be initializing)."
  fi
else
  echo " - curl not available to test inference endpoint"
fi

# 6) Final status and instructions
log "Stack start complete (or in progress). Useful commands:"
echo "  - View containers:    $DC ps"
echo "  - View logs (nginx):  docker logs \$(docker ps -qf \"name=nginx\")"
echo "  - Tail all logs:      $DC logs -f"
echo ""
echo "Notes:"
echo "  - Tomcat will auto-deploy the .war files placed in ./wars (we built .war packages into wars/*.war)."
echo "  - The demo JSP apps are intentionally vulnerable — run only in an isolated lab environment."
echo "  - To tear down:        $DC down"
echo ""
echo "If you want me to also provide a 'stop_stack.sh' teardown script or a systemd unit for auto-start, tell me and I'll add it."
