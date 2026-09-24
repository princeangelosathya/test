#!/usr/bin/env bash
# Runs once when the cloud workspace is built (or pre-built by the organizer). Students never run this.
set -e
cd "$(dirname "$0")/.."
pip install -q -r backend/requirements.txt
[ -f backend/.env ] || cp backend/.env.example backend/.env
(cd frontend && npm install --silent)
python backend/verify_install.py
echo "Workspace ready"
