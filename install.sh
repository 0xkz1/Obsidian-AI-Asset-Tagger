#!/bin/bash

# --- Obsidian AI Asset Tagger Service Installer ---
# This script sets up the tagger as a systemd background service.

# Check for root privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

# Detect current user and paths
REAL_USER=$SUDO_USER
WORKDIR=$(pwd)
PYTHON_PATH=$(which python3)

echo "Installing Obsidian AI Asset Tagger Service..."
echo "  User: $REAL_USER"
echo "  Workdir: $WORKDIR"
echo "  Python: $PYTHON_PATH"

# Generate the service file from template
SERVICE_FILE="/etc/systemd/system/obsidian-tagger.service"
sed -e "s|{{USER}}|$REAL_USER|g" \
    -e "s|{{WORKDIR}}|$WORKDIR|g" \
    -e "s|{{PYTHON_PATH}}|$PYTHON_PATH|g" \
    service/obsidian-tagger.service.template > $SERVICE_FILE

echo "  -> Created $SERVICE_FILE"

# Reload systemd and enable service
systemctl daemon-reload
systemctl enable obsidian-tagger
systemctl restart obsidian-tagger

echo ""
echo "Success! The service is now running in the background."
echo "Commands to manage the service:"
echo "  - View status:  systemctl status obsidian-tagger"
echo "  - View logs:    journalctl -u obsidian-tagger -f"
echo "  - Restart:      systemctl restart obsidian-tagger"
echo ""
