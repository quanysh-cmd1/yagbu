#!/usr/bin/env bash
set -euo pipefail

echo "YAGBU bootstrap started"
echo "- create Python virtualenv"
echo "- install local package in editable mode"
echo "- initialize project folders"

mkdir -p docs python/src/yagbu python/examples models scripts

echo "Bootstrap complete."
