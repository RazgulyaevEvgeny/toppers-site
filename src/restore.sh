#!/bin/bash
# Восстановление рабочей среды сборки в новой сессии Claude (пути зашиты в скриптах).
# Запуск из корня репозитория:  bash src/restore.sh
set -e
R="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p /home/claude/v /home/claude/proj /home/claude/m3 /home/claude/site
cp -r "$R"/src/v/. /home/claude/v/
cp /home/claude/v/final.html /home/claude/final.html
cp -r "$R"/src/proj/. /home/claude/proj/
cp -r "$R"/site/models "$R"/site/posters /home/claude/proj/
cp -r "$R"/src/m3/. /home/claude/m3/
cp -r "$R"/site/. /home/claude/site/
echo "ok: сборка  cd /home/claude/v && python3 vD32.py   -> /home/claude/site"
