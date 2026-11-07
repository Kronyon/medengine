#!/bin/sh
# Rebuild site/study.html from the pristine 3.6.3 page:
#   engine patches -> rw_01..10 (my rewrites, data versions 3..12) -> import the v3.6.12 Antigravity bank with
#   correct run migration (data version 13, ov 14) -> rw_13+ (fixes on top, data version 15+) -> triage flags ->
#   Mock-like flags and week weights -> explanation polish -> release number from study/snap/rw/VERSION.
# Run site/build.py after.
set -e
cd "$(dirname "$0")/../../.."
cp site/study_pre364.html site/study.html
python3 site/patches/v364_engine.py
python3 site/patches/v369_engine.py
python3 site/patches/v3613_engine.py
python3 site/patches/v3614_ui.py
python3 site/patches/v3614_css.py
python3 site/patches/v3615_ui.py
python3 site/patches/v3616_ui.py
python3 site/patches/v3617_tt.py
RW_MAX=10 python3 site/patches/v364_rw.py
python3 site/patches/v3613_import.py
RW_MIN=13 python3 site/patches/v364_rw.py
python3 study/snap/rw/detect.py > /dev/null
python3 site/patches/v364_ml.py
python3 site/patches/v369_polish.py
python3 site/patches/v3614_mock.py
V=$(cat study/snap/rw/VERSION)
sed -i "s#<small>v3\.6\.[0-9]*</small>#<small>v$V</small>#" site/study.html
sed -i "s#<span class=\"ver\">v3\.6\.[0-9]*</span>#<span class=\"ver\">v$V</span>#" site/index.html site/osce.html
sed -i "s#APP_VERSION = '3\.6\.[0-9]*'#APP_VERSION = '$V'#" site/osce.html
echo "stamped v$V"
