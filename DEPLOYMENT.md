# Render Deployment Guide

This guide will walk you through deploying the Krazio Email API to Render.

## Prerequisites

1. **GitHub/GitLab/Bitbucket Account** - Your code needs to be in a Git repository
2. **Render Account** - Sign up at [render.com](https://render.com) if you don't have one
3. **Gmail App Password** - Already configured in your code

## Step-by-Step Deployment

### Step 1: Push Code to Git Repository

1. Initialize git (if not already done):
```bash
git init
git add .
git commit -m "Initial commit - Contact form API"
```

2. Create a repository on GitHub/GitLab/Bitbucket

3. Push your code:
```bash
git remote add origin <your-repository-url>
git branch -M main
git push -u origin main
```

**Important:** Make sure `.env` is in `.gitignore` (it should be already) - never commit sensitive credentials!

### Step 2: Deploy on Render

#### Option A: Using Render Dashboard (Recommended)

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Sign in or create an account

2. **Create New Web Service**
   - Click **"New +"** button
   - Select **"Web Service"**

3. **Connect Repository**
   - Click **"Connect account"** if you haven't connected your Git provider
   - Authorize Render to access your repositories
   - Select your repository (`krazio-email`)

4. **Configure Service**
   - **Name:** `krazio-email-api` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** Choose closest to your users
   - **Branch:** `main` (or your default branch)
   - **Root Directory:** Leave empty (or `.` if needed)
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. **Set Environment Variables**
   Click on **"Advanced"** → **"Add Environment Variable"** and add:
   
   ```
   SMTP_SERVER = smtp.gmail.com
   SMTP_PORT = 587
   SMTP_USERNAME = krazio.developers@gmail.com
   SMTP_PASSWORD = scoq vbap nqhx dlyj
   FROM_EMAIL = krazio.developers@gmail.com
   TO_EMAIL = krazio.developers@gmail.com
   ```
   
   **Note:** Render will automatically set the `PORT` environment variable - you don't need to set it.

6. **Deploy**
   - Click **"Create Web Service"**
   - Render will start building and deploying your app
   - Wait for the build to complete (usually 2-5 minutes)

7. **Get Your API URL**
   - Once deployed, your API will be available at:
   - `https://your-service-name.onrender.com`
   - Example: `https://krazio-email-api.onrender.com`

#### Option B: Using render.yaml (Blueprint)

1. **Push render.yaml to Repository**
   - Make sure `render.yaml` is committed to your repository

2. **Create Blueprint**
   - In Render Dashboard, click **"New +"** → **"Blueprint"**
   - Connect your repository
   - Render will read `render.yaml` and configure the service

3. **Set Environment Variables**
   - Go to your service → **Environment** tab
   - Add the environment variables listed above
   - Variables marked `sync: false` in `render.yaml` need to be set manually

4. **Deploy**
   - Render will automatically deploy

### Step 3: Verify Deployment

1. **Check Health Endpoint**
   ```bash
   curl https://your-service-name.onrender.com/health
   ```
   
   Should return:
   ```json
   {
     "status": "healthy",
     "message": "Contact API is running"
   }
   ```

2. **Test Contact Endpoint**
   ```bash
   curl -X POST https://your-service-name.onrender.com/api/contact \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Test User",
       "phone": "+1234567890",
       "business_email": "test@example.com",
       "company": "Test Company",
       "message": "This is a test message"
     }'
   ```

## Environment Variables Reference

| Variable | Value | Description |
|----------|-------|-------------|
| `SMTP_SERVER` | `smtp.gmail.com` | Gmail SMTP server |
| `SMTP_PORT` | `587` | SMTP port (TLS) |
| `SMTP_USERNAME` | `krazio.developers@gmail.com` | Your Gmail address |
| `SMTP_PASSWORD` | `scoq vbap nqhx dlyj` | Gmail App Password |
| `FROM_EMAIL` | `krazio.developers@gmail.com` | Sender email |
| `TO_EMAIL` | `krazio.developers@gmail.com` | Recipient email for leads |
| `PORT` | (auto-set) | Port number (Render sets this) |

## API Endpoints

Once deployed, your API will be available at:

- **Root:** `GET https://your-service-name.onrender.com/`
- **Health Check:** `GET https://your-service-name.onrender.com/health`
- **Contact Form:** `POST https://your-service-name.onrender.com/api/contact`
- **Contact Form (Alt):** `POST https://your-service-name.onrender.com/contact`

## Important Notes

### Free Tier Limitations

- **Spin Down:** Free tier services spin down after 15 minutes of inactivity
- **Cold Start:** First request after spin-down may take 30-60 seconds
- **Upgrade:** Consider upgrading to paid plan for production use

### Security

- ✅ Never commit `.env` file to Git
- ✅ Use environment variables in Render dashboard
- ✅ Gmail App Passwords are more secure than regular passwords
- ✅ HTTPS is enabled automatically on Render

### Monitoring

- Check **Logs** tab in Render dashboard for errors
- Monitor **Metrics** tab for performance
- Set up **Alerts** for service failures

### Updating Deployment

1. Make changes to your code
2. Commit and push to your repository:
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```
3. Render will automatically detect changes and redeploy

## Troubleshooting

### Build Fails

- Check build logs in Render dashboard
- Verify `requirements.txt` is correct
- Ensure Python version matches `runtime.txt`

### Email Not Sending

- Verify environment variables are set correctly
- Check Gmail App Password is valid
- Review logs for SMTP errors
- Test SMTP connection locally first

### Service Not Starting

- Check start command: `gunicorn app:app`
- Verify `app.py` exists in root directory
- Check logs for import errors

### 502 Bad Gateway

- Service might be spinning up (free tier)
- Wait 30-60 seconds and try again
- Check service status in dashboard

## Support

For issues:
1. Check Render logs
2. Test locally with `gunicorn app:app`
3. Verify all environment variables are set
4. Check Render status page: [status.render.com](https://status.render.com)

