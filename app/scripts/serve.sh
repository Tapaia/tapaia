#!/usr/bin/env bash
# Build and (re)start the prototype in the background on $PORT (default 4417). Logs: app/server.log
set -e
cd "$(dirname "$0")/.."
PORT="${PORT:-4417}"
npm run build >/dev/null
pkill -f "tsx server/index.ts" 2>/dev/null || true
sleep 0.5
PORT=$PORT NODE_ENV=production nohup setsid npx tsx server/index.ts > server.log 2>&1 < /dev/null &
echo "Tapaia prototype starting on http://localhost:$PORT (logs: app/server.log)"
