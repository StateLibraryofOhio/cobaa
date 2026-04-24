#!/bin/bash
set -e

echo "[startup] installing WeasyPrint runtime libs..."
apt-get update
DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
  libpango-1.0-0 \
  libcairo2 \
  libgdk-pixbuf-2.0-0 \
  libffi8 \
  shared-mime-info \
  fonts-dejavu-core
rm -rf /var/lib/apt/lists/*

echo "[startup] starting gunicorn..."
exec gunicorn --bind=0.0.0.0:${PORT:-8000} --workers=2 cobaa.wsgi:application
