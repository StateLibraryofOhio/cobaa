#!/bin/bash
apt-get update
apt-get install -y libpango1.0-0 libcairo2 libgtk-3-dev libpq-dev libffi-dev
apt install libcairo2-dev pkg-config
gunicorn --preload --bind=0.0.0.0 --workers=4 startup:cobaa
