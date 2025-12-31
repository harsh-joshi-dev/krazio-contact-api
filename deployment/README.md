# Krazio Email API - Dedicated Server Deployment Guide

This folder contains everything you need to deploy the Krazio Email API on your dedicated server.

## 📋 Prerequisites

Before deploying, ensure your server has:

- **Linux OS** (Ubuntu 20.04+ or Debian 10+ recommended)
- **Python 3.11** installed
- **Systemd** (usually pre-installed)
- **Root/sudo access**
- **Internet connection** (for downloading dependencies)

## 📦 Deployment Steps

### 0. Email Service Configuration

This application supports **SendGrid** (recommended) and **SMTP** (for dedicated servers).

**Option A: SendGrid (Recommended - Works Everywhere)**
- Set `SENDGRID_API_KEY` in environment variables
- Works on Render and dedicated servers
- Free tier: 100 emails/day

**Option B: SMTP (Dedicated Servers Only)**
- Set SMTP credentials in environment variables
- Only works on servers with SMTP port access

### 1. Transfer Files to Server

Upload this entire `deployment` folder to your server. You can use:

```bash
# Using SCP
scp -r deployment/ user@your-server:/path/to/deployment/

# Using SFTP
sftp user@your-server
put -r deployment/
```

### 2. Run Deployment Script

SSH into your server and run:

```bash
cd /path/to/deployment
chmod +x *.sh
sudo ./deploy.sh
```

The deployment script will:
- Create application directory at `/opt/krazio-email-api`
- Set up Python virtual environment
- Install all dependencies
- Create systemd service
- Set up environment configuration

### 3. Configure Environment Variables

Edit the `.env` file with your email configuration:

```bash
sudo nano /opt/krazio-email-api/.env
```

**Option A: SendGrid Configuration (Recommended)**

```env
SENDGRID_API_KEY=SG.your_sendgrid_api_key_here
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=recipient@example.com
PORT=5000
```

Get your SendGrid API key from: https://app.sendgrid.com/settings/api_keys

**Option B: SMTP Configuration (Traditional)**

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-gmail-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=recipient@example.com
PORT=5000
```

**Important:** 
- The app will automatically use SendGrid if `SENDGRID_API_KEY` is set, otherwise it uses SMTP
- For Gmail SMTP, you need to use an App Password, not your regular password
- See [Gmail App Passwords](https://support.google.com/accounts/answer/185833) for instructions

### 4. Start the Service

```bash
sudo systemctl start krazio-email-api
sudo systemctl enable krazio-email-api  # Enable auto-start on boot
```

### 5. Verify Deployment

Check service status:

```bash
sudo systemctl status krazio-email-api
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

If you're using a reverse proxy (nginx/apache), test through that:

```bash
curl http://your-domain.com/health
```

## 🔧 Management Scripts

All scripts should be run with `sudo`:

- **`deploy.sh`** - Initial deployment (run once)
- **`start.sh`** - Start the service
- **`stop.sh`** - Stop the service
- **`restart.sh`** - Restart the service
- **`update.sh`** - Update application files and dependencies
- **`status.sh`** - View service status and logs

Example usage:

```bash
sudo ./start.sh
sudo ./restart.sh
sudo ./status.sh
```

## 🌐 Reverse Proxy Setup (Nginx)

To serve the API behind Nginx, add this configuration:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Then enable and reload:

```bash
sudo ln -s /etc/nginx/sites-available/krazio-email /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## 🔒 Firewall Configuration

If using UFW firewall:

```bash
# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS (if using SSL)
sudo ufw allow 443/tcp

# Allow direct access to app port (optional, usually behind reverse proxy)
sudo ufw allow 5000/tcp
```

## 📊 Monitoring & Logs

### View Logs

```bash
# Real-time logs
sudo journalctl -u krazio-email-api -f

# Last 100 lines
sudo journalctl -u krazio-email-api -n 100

# Logs since today
sudo journalctl -u krazio-email-api --since today
```

### Application Logs

Application logs are also stored at:

```
/opt/krazio-email-api/logs/
```

## 🔄 Updating the Application

When you need to update the application:

1. Copy new files to the deployment folder
2. Run the update script:

```bash
sudo ./update.sh
```

The update script will:
- Stop the service
- Backup your `.env` file
- Copy new application files
- Update dependencies
- Restart the service

## 🛠️ Troubleshooting

### Service won't start

```bash
# Check service status
sudo systemctl status krazio-email-api

# Check logs for errors
sudo journalctl -u krazio-email-api -n 50

# Verify Python and dependencies
sudo -u www-data /opt/krazio-email-api/venv/bin/python --version
sudo -u www-data /opt/krazio-email-api/venv/bin/pip list
```

### Email not sending

1. Verify `.env` file configuration:
   ```bash
   sudo cat /opt/krazio-email-api/.env
   ```

2. Test SMTP connection manually:
   ```bash
   sudo -u www-data /opt/krazio-email-api/venv/bin/python -c "
   import smtplib
   import os
   from dotenv import load_dotenv
   load_dotenv('/opt/krazio-email-api/.env')
   server = smtplib.SMTP(os.getenv('SMTP_SERVER'), int(os.getenv('SMTP_PORT')))
   server.starttls()
   server.login(os.getenv('SMTP_USERNAME'), os.getenv('SMTP_PASSWORD'))
   print('SMTP connection successful')
   server.quit()
   "
   ```

### Permission issues

```bash
# Fix ownership
sudo chown -R www-data:www-data /opt/krazio-email-api

# Fix permissions
sudo chmod -R 755 /opt/krazio-email-api
sudo chmod 600 /opt/krazio-email-api/.env
```

### Port already in use

If port 5000 is already in use, change it in `.env`:

```bash
sudo nano /opt/krazio-email-api/.env
# Change PORT=5000 to another port, e.g., PORT=8000
sudo systemctl restart krazio-email-api
```

## 📁 Directory Structure

After deployment:

```
/opt/krazio-email-api/
├── app.py                    # Main application
├── wsgi.py                   # WSGI entry point
├── requirements.txt          # Python dependencies
├── gunicorn_config.py        # Gunicorn configuration
├── .env                      # Environment variables (keep secret!)
├── .env.example              # Environment template
├── venv/                     # Python virtual environment
└── logs/                     # Application logs
```

## 🔐 Security Recommendations

1. **Never commit `.env` file** - It contains sensitive credentials
2. **Use Gmail App Passwords** - More secure than regular passwords
3. **Set up SSL/TLS** - Use Let's Encrypt with Certbot
4. **Regular updates** - Keep system and dependencies updated
5. **Firewall** - Only open necessary ports
6. **Monitor logs** - Regularly check for suspicious activity

## 📞 API Endpoints

Once deployed, your API will be available at:

- **Root:** `GET http://your-domain.com/`
- **Health Check:** `GET http://your-domain.com/health`
- **Ping:** `GET http://your-domain.com/ping`
- **Contact Form:** `POST http://your-domain.com/api/contact`
- **Contact Form (Alt):** `POST http://your-domain.com/contact`

### Example API Request

```bash
curl -X POST http://your-domain.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+1234567890",
    "business_email": "john@example.com",
    "company": "Example Corp",
    "message": "Hello, I am interested in your services."
  }'
```

## 📝 Notes

- The service runs as `www-data` user for security
- Service automatically restarts on failure (systemd RestartSec=10)
- Service starts automatically on boot (systemd WantedBy)
- Application listens on `0.0.0.0` to accept connections from any interface
- Default port is 5000, but can be changed in `.env`

## 🆘 Support

If you encounter issues:

1. Check service logs: `sudo journalctl -u krazio-email-api -f`
2. Verify configuration: `sudo cat /opt/krazio-email-api/.env`
3. Test manually: Run the app directly to see errors
4. Check system resources: `htop` or `free -h`

