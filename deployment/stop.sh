#!/bin/bash
# Stop script for Krazio Email API

APP_NAME="krazio-email-api"

if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "Stopping ${APP_NAME}..."
systemctl stop ${APP_NAME}
echo "${APP_NAME} stopped."

