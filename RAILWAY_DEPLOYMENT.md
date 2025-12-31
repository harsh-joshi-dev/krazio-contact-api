# Railway Deployment Guide

## Quick Setup

1. **Push code to GitHub** (if not already done)
2. **Go to Railway Dashboard**: [railway.app](https://railway.app)
3. **Create New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Railway will auto-detect** Python and deploy

## Configuration Files

### ✅ Already Configured:

- **`runtime.txt`** - Python version: `3.11`
- **`requirements.txt`** - All dependencies
- **`Procfile`** - Start command for Railway
- **`nixpacks.toml`** - Build configuration (optional, Railway auto-detects)

## Environment Variables

Set these in Railway Dashboard → Variables:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=krazio.developers@gmail.com
SMTP_PASSWORD=scoq vbap nqhx dlyj
FROM_EMAIL=krazio.developers@gmail.com
TO_EMAIL=krazio.developers@gmail.com
```

**Note:** Railway automatically sets `PORT` - don't set it manually.

## Start Command

Railway will use the `Procfile` automatically. If you need to override:

```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --timeout 300 --graceful-timeout 120
```

## Troubleshooting

### Python Version Error

If you see `mise ERROR Failed to install core:python@3.11.0`:

1. **Option 1:** Remove `runtime.txt` and let Railway auto-detect
2. **Option 2:** Change `runtime.txt` to just `3.11` (already done)
3. **Option 3:** Use `nixpacks.toml` (already created)

### Build Fails

1. Check build logs in Railway dashboard
2. Verify `requirements.txt` is correct
3. Make sure all dependencies are listed

### App Not Starting

1. Check logs for errors
2. Verify environment variables are set
3. Test start command locally:
   ```bash
   gunicorn app:app --bind 0.0.0.0:5000 --workers 1
   ```

### 502 Bad Gateway

1. Check if service is running (Railway dashboard)
2. Verify start command in settings
3. Check logs for worker timeout errors
4. Increase timeout if needed (already set to 300s)

## Testing After Deployment

```bash
# Health check
curl https://your-app.railway.app/health

# Test contact form
curl -X POST https://your-app.railway.app/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+1234567890",
    "business_email": "test@example.com",
    "company": "Test Co",
    "message": "Test message"
  }'
```

## Railway vs Render Differences

- **Build System:** Railway uses Nixpacks (auto-detects), Render uses Docker
- **Python Version:** Railway uses `3.11` in runtime.txt, Render uses `python-3.11.0`
- **Start Command:** Both use Procfile, but Railway can also use nixpacks.toml
- **Port:** Both auto-set `$PORT` environment variable

## Files for Railway

- ✅ `runtime.txt` - Python version
- ✅ `requirements.txt` - Dependencies  
- ✅ `Procfile` - Start command
- ✅ `nixpacks.toml` - Build config (optional)
- ✅ `railway.json` - Railway config (optional)

## Quick Deploy Steps

1. **GitHub:** Push your code
2. **Railway:** New Project → GitHub Repo
3. **Variables:** Add environment variables
4. **Deploy:** Railway auto-deploys
5. **Test:** Check your Railway URL

Your app will be live at: `https://your-app-name.up.railway.app`

