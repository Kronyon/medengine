#!/bin/sh
# Rebuild site/study.html from the pristine 3.6.3 page: engine patch, all rw_NN rewrites, Mock-like flags,
# then stamp the release number in study/snap/rw/VERSION on STUDY, the launcher and OSCE. Run site/build.py after.
set -e
cd "$(dirname "$0")/../../.."
cp site/study_pre364.html site/study.html
python3 site/patches/v364_engine.py
python3 site/patches/v364_rw.py
python3 site/patches/v364_ml.py
V=$(cat study/snap/rw/VERSION)
sed -i "s#<small>v3\.6\.[0-9]*</small>#<small>v$V</small>#" site/study.html
sed -i "s#<span class=\"ver\">v3\.6\.[0-9]*</span>#<span class=\"ver\">v$V</span>#" site/index.html site/osce.html
sed -i "s#APP_VERSION = '3\.6\.[0-9]*'#APP_VERSION = '$V'#" site/osce.html
echo "stamped v$V"
