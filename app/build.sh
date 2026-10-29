#!/usr/bin/env bash
# Rebuild the app from content/ and src/: v3 data (units, packs, past papers), v4 single-task stations, then the page.
set -euo pipefail
cd "$(dirname "$0")"
python3 build/build_v3.py
python3 build/build_v4.py
python3 build/build_cases.py
python3 build/build_app_v4.py
mkdir -p dist && cp out/index.html dist/app.html
echo "app/dist/app.html updated"
