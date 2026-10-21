#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON="${PYTHON:-python3}"
if [ ! -d .venv ]; then "$PYTHON" -m venv .venv; fi
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/validate_skills.py
echo "Project-local dependencies ready. Font installation and Codex Cloud publishing NOT implied."
