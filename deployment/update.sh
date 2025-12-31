#!/bin/bash
# Update script for Krazio Email API

set -e

APP_NAME="krazio-email-api"
APP_DIR="/opt/${APP_NAME}"

if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

echo "========================================="
echo "Updating ${APP_NAME}..."
echo "========================================="

# Stop the service
echo "Stopping service..."
systemctl stop ${APP_NAME} || true

# Backup current .env file
if [ -f "${APP_DIR}/.env" ]; then
    echo "Backing up .env file..."
    cp ${APP_DIR}/.env ${APP_DIR}/.env.backup.$(date +%Y%m%d_%H%M%S)
fi

# Update application files (assuming files are in current directory)
echo "Copying new files..."
# Copy all files except .env and venv
cp app.py ${APP_DIR}/ 2>/dev/null || echo "Warning: app.py not found"
cp wsgi.py ${APP_DIR}/ 2>/dev/null || echo "Warning: wsgi.py not found"
cp requirements.txt ${APP_DIR}/ 2>/dev/null || echo "Warning: requirements.txt not found"
cp gunicorn_config.py ${APP_DIR}/ 2>/dev/null || echo "Warning: gunicorn_config.py not found"

# Update dependencies
echo "Updating Python dependencies..."
cd ${APP_DIR}
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Set permissions
chown -R www-data:www-data ${APP_DIR}
chmod -R 755 ${APP_DIR}

# Start the service
echo "Starting service..."
systemctl start ${APP_NAME}
systemctl status ${APP_NAME}

echo ""
echo "Update completed successfully!"
echo "View logs with: sudo journalctl -u ${APP_NAME} -f"

