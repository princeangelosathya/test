#!/usr/bin/env bash
cd "$(dirname "$0")"
[ -f backend/.venv/bin/activate ] && source backend/.venv/bin/activate
(cd backend && python app.py) &
BACK=$!
trap "kill $BACK" EXIT
cd frontend && npm run dev
