#!/bin/bash
# Deployment script for Krazio Email API on dedicated server

set -e  # Exit on error

echo "========================================="
echo "Krazio Email API - Deployment Script"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="krazio-email-api"
APP_DIR="/opt/${APP_NAME}"
SERVICE_USER="www-data"
PYTHON_VERSION="3.11"

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating application directory...${NC}"
mkdir -p ${APP_DIR}
mkdir -p ${APP_DIR}/logs
mkdir -p ${APP_DIR}/venv

echo -e "${YELLOW}Step 2: Copying application files...${NC}"
# Copy all files from current directory
cp -r . ${APP_DIR}/ || {
    # If run from deployment folder, copy parent files
    cp ../app.py ${APP_DIR}/ 2>/dev/null || true
    cp ../wsgi.py ${APP_DIR}/ 2>/dev/null || true
    cp ../requirements.txt ${APP_DIR}/ 2>/dev/null || true
    cp ../runtime.txt ${APP_DIR}/ 2>/dev/null || true
    cp ../gunicorn_config.py ${APP_DIR}/ 2>/dev/null || true
    cp env.example ${APP_DIR}/.env.example 2>/dev/null || true
}

echo -e "${YELLOW}Step 3: Setting up Python virtual environment...${NC}"
cd ${APP_DIR}

# Check if Python 3.11 is available
if ! command -v python3.11 &> /dev/null; then
    echo -e "${RED}Python 3.11 is not installed. Please install it first.${NC}"
    echo "On Ubuntu/Debian: sudo apt-get install python3.11 python3.11-venv python3.11-dev"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    python3.11 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}Step 4: Setting up environment variables...${NC}"
if [ ! -f "${APP_DIR}/.env" ]; then
    if [ -f "${APP_DIR}/.env.example" ]; then
        cp ${APP_DIR}/.env.example ${APP_DIR}/.env
        echo -e "${YELLOW}Created .env file from .env.example. Please edit it with your configuration:${NC}"
        echo "  sudo nano ${APP_DIR}/.env"
    else
        echo -e "${YELLOW}Creating .env file template...${NC}"
        cat > ${APP_DIR}/.env << EOF
# SMTP Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=recipient@example.com
PORT=5000
EOF
        echo -e "${YELLOW}Created .env file. Please edit it with your configuration:${NC}"
        echo "  sudo nano ${APP_DIR}/.env"
    fi
else
    echo -e "${GREEN}.env file already exists. Skipping...${NC}"
fi

echo -e "${YELLOW}Step 5: Setting up systemd service...${NC}"
cat > /etc/systemd/system/${APP_NAME}.service << EOF
[Unit]
Description=Krazio Email API
After=network.target

[Service]
Type=notify
User=${SERVICE_USER}
Group=${SERVICE_USER}
WorkingDirectory=${APP_DIR}
Environment="PATH=${APP_DIR}/venv/bin"
EnvironmentFile=${APP_DIR}/.env
ExecStart=${APP_DIR}/venv/bin/gunicorn -c ${APP_DIR}/gunicorn_config.py app:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
chown -R ${SERVICE_USER}:${SERVICE_USER} ${APP_DIR}
chmod -R 755 ${APP_DIR}
chmod 600 ${APP_DIR}/.env 2>/dev/null || true

echo -e "${YELLOW}Step 6: Reloading systemd and enabling service...${NC}"
systemctl daemon-reload
systemctl enable ${APP_NAME}.service

echo ""
echo -e "${GREEN}========================================="
echo "Deployment completed successfully!"
echo "=========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Edit the environment file:"
echo "   sudo nano ${APP_DIR}/.env"
echo ""
echo "2. Start the service:"
echo "   sudo systemctl start ${APP_NAME}"
echo ""
echo "3. Check service status:"
echo "   sudo systemctl status ${APP_NAME}"
echo ""
echo "4. View logs:"
echo "   sudo journalctl -u ${APP_NAME} -f"
echo ""
echo -e "${YELLOW}Note: Make sure to configure your .env file before starting the service!${NC}"

