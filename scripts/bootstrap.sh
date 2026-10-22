#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
STUDIO_PYTHON="${PYTHON:-python3}"
if [ -x .venv/bin/python ]; then STUDIO_PYTHON=.venv/bin/python; fi
"$STUDIO_PYTHON" studio/scripts/bootstrap.py --install-missing "$@"
"$STUDIO_PYTHON" scripts/validate_skills.py
echo "Working dependencies reused or missing pins installed. Environment publication is separate."
