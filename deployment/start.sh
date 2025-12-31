#!/bin/bash
# Start script for Krazio Email API

APP_NAME="krazio-email-api"

if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Starting ${APP_NAME}..."
systemctl start ${APP_NAME}
systemctl status ${APP_NAME}

