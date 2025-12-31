# Quick Start Guide

## Fastest Way to Deploy

1. **Upload this entire `deployment` folder to your server:**
   ```bash
   scp -r deployment/ user@your-server:/home/user/
   ```

2. **SSH into your server and run:**
   ```bash
   cd /home/user/deployment
   sudo chmod +x *.sh
   sudo ./deploy.sh
   ```

3. **Configure your email settings:**
   ```bash
   sudo nano /opt/krazio-email-api/.env
   ```
   
   Update these values:
   - `SMTP_USERNAME` - Your Gmail address
   - `SMTP_PASSWORD` - Your Gmail App Password
   - `TO_EMAIL` - Where to receive contact form submissions

4. **Start the service:**
   ```bash
   sudo systemctl start krazio-email-api
   sudo systemctl enable krazio-email-api
   ```

5. **Test it:**
   ```bash
   curl http://localhost:5000/health
   ```

Done! Your API is now running.

## Quick Commands

```bash
# Start service
sudo systemctl start krazio-email-api

# Stop service
sudo systemctl stop krazio-email-api

# Restart service
sudo systemctl restart krazio-email-api

# View status
sudo systemctl status krazio-email-api

# View logs
sudo journalctl -u krazio-email-api -f
```

## What Gets Installed

- Application files in `/opt/krazio-email-api/`
- Python virtual environment with all dependencies
- Systemd service for automatic startup
- Runs on port 5000 (configurable in `.env`)

## Need Help?

See `README.md` for detailed documentation.

