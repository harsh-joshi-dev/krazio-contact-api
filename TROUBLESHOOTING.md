# Troubleshooting 502 Bad Gateway on Render

## Common Causes and Solutions

### 1. Check Render Logs

The first step is to check the logs in your Render dashboard:
1. Go to your service in Render dashboard
2. Click on **"Logs"** tab
3. Look for error messages

Common errors you might see:
- `ModuleNotFoundError` - Missing dependency
- `ImportError` - Import issue
- `Port already in use` - Port configuration issue
- `SMTP authentication failed` - Email credentials issue

### 2. Verify Start Command

In Render dashboard → Settings → Start Command, make sure it's one of:

**Option 1 (Recommended):**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30
```

**Option 2 (Using config file):**
```bash
gunicorn --config gunicorn_config.py app:app
```

**Option 3 (Simple):**
```bash
gunicorn app:app
```

### 3. Verify Environment Variables

Make sure ALL these are set in Render dashboard → Environment:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=krazio.developers@gmail.com
SMTP_PASSWORD=scoq vbap nqhx dlyj
FROM_EMAIL=krazio.developers@gmail.com
TO_EMAIL=krazio.developers@gmail.com
```

**Important:** Render automatically sets `PORT` - you don't need to set it manually.

### 4. Check Build Logs

1. Go to Render dashboard → Your service
2. Click on **"Events"** tab
3. Check if the build completed successfully
4. Look for any errors during `pip install -r requirements.txt`

### 5. Verify Python Version

Make sure `runtime.txt` contains:
```
python-3.11.0
```

Or remove `runtime.txt` and let Render auto-detect.

### 6. Test Locally with Gunicorn

Before deploying, test locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Test with gunicorn
gunicorn app:app --bind 0.0.0.0:5001 --workers 2

# Or with config
gunicorn --config gunicorn_config.py app:app
```

### 7. Common Fixes

#### Fix 1: Update Start Command
If using the simple command, try the explicit one:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30
```

#### Fix 2: Check App Variable
Make sure `app.py` has:
```python
app = Flask(__name__)
```

And it's accessible (not inside `if __name__ == '__main__'`).

#### Fix 3: Add Health Check
The app already has a health endpoint at `/health`. Test it after deployment.

#### Fix 4: Increase Timeout
If requests are timing out, increase the timeout:
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --timeout 60
```

### 8. Debug Steps

1. **Check if service is running:**
   - Look at the service status in Render dashboard
   - Should show "Live" status

2. **Check recent deployments:**
   - Go to "Events" tab
   - See if latest deployment succeeded

3. **Test health endpoint:**
   ```bash
   curl https://your-service.onrender.com/health
   ```

4. **Check for import errors:**
   - Look for `ModuleNotFoundError` in logs
   - Make sure all dependencies are in `requirements.txt`

### 9. Quick Fixes to Try

**Option A: Update Start Command in Render**
1. Go to Settings → Start Command
2. Change to: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30`
3. Save and redeploy

**Option B: Check File Structure**
Make sure `app.py` is in the root directory, not in a subdirectory.

**Option C: Verify Requirements**
Make sure `requirements.txt` has all dependencies:
```
Flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

### 10. Still Not Working?

1. **Check Render Status:** [status.render.com](https://status.render.com)
2. **Review Render Docs:** [render.com/docs](https://render.com/docs)
3. **Check Logs Again:** Look for specific error messages
4. **Try Manual Deploy:** Trigger a manual redeploy from dashboard

## Quick Test Commands

After fixing, test these endpoints:

```bash
# Health check
curl https://your-service.onrender.com/health

# Root endpoint
curl https://your-service.onrender.com/

# Contact form (test)
curl -X POST https://your-service.onrender.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test",
    "phone": "+1234567890",
    "business_email": "test@example.com",
    "message": "Test"
  }'
```

