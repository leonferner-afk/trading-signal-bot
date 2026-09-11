#!/usr/bin/env bash
# One-command local dev launcher: creates the venv if missing, installs
# dependencies, copies .env.example -> .env on first run, and starts the
# API + dashboard on http://localhost:8000.
set -euo pipefail
cd "$(dirname "$0")/.."

if [ ! -d .venv ]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q -r requirements.txt

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example — edit it (Telegram token/chat id, watchlist, etc.) then re-run this script."
fi

echo "Starting Sagoton on http://localhost:8000 (Ctrl+C to stop)..."
uvicorn app.main:app --reload --port 8000
