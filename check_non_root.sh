#!/usr/bin/env bash
set -euo pipefail
IMG="${1:-studyplanner:dev}"

echo "[build] Building image..."
docker build -t "$IMG" .

echo "[check] Verifying that user is non-root..."
docker run --rm "$IMG" id -u | grep -qv '^0$' && echo "[ok] non-root user confirmed"
