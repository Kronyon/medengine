#!/usr/bin/env bash
# Rebuild the app from content/ and src/: data JSON, then the single-file page.
set -euo pipefail
cd "$(dirname "$0")"
python3 build/build_v3.py
python3 build/build_app_v3.py
mkdir -p dist && cp out/index.html dist/app.html
echo "app/dist/app.html updated"
