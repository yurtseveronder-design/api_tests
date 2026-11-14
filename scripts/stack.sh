#!/usr/bin/env bash
# Start / stop the full Sentinel stack for local runs and CI.
#   scripts/stack.sh start         start semantic (8100), ai-sentinel (8000), sentinel-ui (8200)
#   scripts/stack.sh restart-gateway   restart only ai-sentinel (fresh rate-limit window)
#   scripts/stack.sh stop
# Expects the three projects installed/cloned: see README. Paths can be overridden:
#   SENTINEL_UI_DIR (default .sut/sentinel-ui)
set -euo pipefail

ROOT="$(pwd)"
STATE="$ROOT/.stack"
UI_DIR="${SENTINEL_UI_DIR:-$ROOT/.sut/sentinel-ui}"
SEMANTIC_KEY="${SEMANTIC_API_KEY:-test-semantic-key}"
SENTINEL_KEY="${SENTINEL_API_KEY:-test-api-key}"
UI_KEY="${UI_API_KEY:-ui-test-key}"
mkdir -p "$STATE"

wait_for() {  # url name
  for _ in $(seq 1 40); do curl -sf "$1/health" >/dev/null && return 0; sleep 1; done
  echo "$2 did not become healthy; log:"; cat "$STATE/$2.log"; exit 1
}

start_semantic() {
  SEMANTIC_ENGINE=keyword SEMANTIC_API_KEY="$SEMANTIC_KEY" \
    nohup sentinel-semantic --port 8100 > "$STATE/semantic.log" 2>&1 & echo $! > "$STATE/semantic.pid"
  wait_for http://127.0.0.1:8100 semantic
}

start_gateway() {
  AI_SENTINEL_API_KEY="$SENTINEL_KEY" SENTINEL_SEMANTIC_URL=http://127.0.0.1:8100 \
    SENTINEL_SEMANTIC_API_KEY="$SEMANTIC_KEY" \
    nohup uvicorn ai_sentinel.api.gateway:app --port 8000 > "$STATE/gateway.log" 2>&1 & echo $! > "$STATE/gateway.pid"
  wait_for http://127.0.0.1:8000 gateway
}

start_ui() {
  (cd "$UI_DIR" && SENTINEL_API_KEYS="$UI_KEY" SENTINEL_JWT_SECRET=ui-test-secret \
    AI_SENTINEL_URL=http://127.0.0.1:8000 AI_SENTINEL_API_KEY="$SENTINEL_KEY" \
    nohup uvicorn gateway:app --port 8200 > "$STATE/ui.log" 2>&1 & echo $! > "$STATE/ui.pid")
  wait_for http://127.0.0.1:8200 ui
}

stop_one() { [ -f "$STATE/$1.pid" ] && kill "$(cat "$STATE/$1.pid")" 2>/dev/null || true; rm -f "$STATE/$1.pid"; }

case "${1:-}" in
  start) start_semantic; start_gateway; start_ui; echo "stack is up" ;;
  restart-gateway) stop_one gateway; sleep 1; start_gateway ;;
  stop) stop_one ui; stop_one gateway; stop_one semantic ;;
  *) echo "usage: $0 start|restart-gateway|stop"; exit 2 ;;
esac
