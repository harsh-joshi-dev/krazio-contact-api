# Quick Deployment Checklist

## ✅ Pre-Deployment Checklist

- [x] All code files are ready
- [x] `requirements.txt` includes gunicorn
- [x] `render.yaml` configuration file created
- [x] `runtime.txt` specifies Python version
- [x] `.gitignore` excludes `.env` and sensitive files
- [x] App uses `PORT` environment variable (Render provides this)
- [x] Debug mode disabled in production

## 📋 Deployment Steps

### 1. Git Setup
```bash
# If not already initialized
git init
git add .
git commit -m "Ready for Render deployment"

# Create repository on GitHub/GitLab/Bitbucket, then:
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Render Setup

1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository
4. Configure:
   - **Name:** `krazio-email-api`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

### 3. Environment Variables

Add these in Render Dashboard → Environment:

```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=krazio.developers@gmail.com
SMTP_PASSWORD=scoq vbap nqhx dlyj
FROM_EMAIL=krazio.developers@gmail.com
TO_EMAIL=krazio.developers@gmail.com
```

### 4. Deploy

- Click **"Create Web Service"**
- Wait for build to complete
- Your API will be live at: `https://your-service-name.onrender.com`

## 🧪 Test After Deployment

```bash
# Health check
curl https://your-service-name.onrender.com/health

# Test contact form
curl -X POST https://your-service-name.onrender.com/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+1234567890",
    "business_email": "test@example.com",
    "company": "Test Co",
    "message": "Test message"
  }'
```

## 📝 Files Ready for Deployment

- ✅ `app.py` - Main application
- ✅ `requirements.txt` - Dependencies
- ✅ `render.yaml` - Render configuration (optional)
- ✅ `runtime.txt` - Python version
- ✅ `.gitignore` - Excludes sensitive files
- ✅ `DEPLOYMENT.md` - Full deployment guide

## ⚠️ Important Reminders

- Never commit `.env` file
- Free tier spins down after 15 min inactivity
- First request after spin-down may be slow
- All environment variables must be set in Render dashboard

