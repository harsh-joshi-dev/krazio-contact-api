#!/bin/bash
# Status script for Krazio Email API

APP_NAME="krazio-email-api"

echo "Service Status:"
systemctl status ${APP_NAME} --no-pager

echo ""
echo "Recent Logs:"
journalctl -u ${APP_NAME} -n 50 --no-pager

