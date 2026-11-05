#!/bin/sh
# v3.6.4: rebuild STUDY from the 3.6.3 page so every rewrite file is applied fresh and in order
set -e
cd "$(dirname "$0")/../../.."
cp site/study_pre364.html site/study.html
python3 site/patches/v364_engine.py
python3 site/patches/v364_rw.py
python3 site/patches/v364_ml.py
