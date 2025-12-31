#!/bin/bash
# Restart script for Krazio Email API

APP_NAME="krazio-email-api"

if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Restarting ${APP_NAME}..."
systemctl restart ${APP_NAME}
systemctl status ${APP_NAME}

