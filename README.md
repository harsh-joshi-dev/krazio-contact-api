# Contact Us API

A Python Flask API for handling contact form submissions and sending emails via SMTP.

## Features

- RESTful API endpoint for contact form submissions
- Email validation
- Phone number validation
- SMTP email sending (supports Gmail and other email providers)
- CORS enabled for frontend integration
- Environment variable configuration

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your details:

```bash
cp env.example .env
```

Edit `.env` with your email configuration:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
TO_EMAIL=recipient@example.com
```

### 3. Gmail Setup (If using Gmail)

Gmail requires an **App Password** instead of your regular password for SMTP authentication:

1. Go to your Google Account settings: https://myaccount.google.com/
2. Navigate to **Security** → **2-Step Verification** (enable it if not already enabled)
3. Go to **App passwords**: https://myaccount.google.com/apppasswords
4. Select **Mail** as the app and **Other (Custom name)** as the device
5. Enter "Contact API" as the name
6. Click **Generate**
7. Copy the 16-character password and use it as `SMTP_PASSWORD` in your `.env` file

**Note:** If you don't see the App passwords option, make sure 2-Step Verification is enabled.

### 4. Other Email Providers

For other email providers, update the SMTP settings in `.env`:

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

**Yahoo:**
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

**Custom SMTP:**
```env
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587
```

## Running the API

```bash
python app.py
```

The API will run on `http://localhost:5000`

## API Endpoints

### POST /api/contact

Submit a contact form.

**Request Body:**
```json
{
  "name": "John Doe",
  "phone": "+1234567890",
  "business_email": "john@example.com",
  "company": "Example Corp",  // Optional
  "message": "Hello, I'm interested in your services."
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Contact form submitted successfully. We will get back to you soon!"
}
```

**Error Response (400/500):**
```json
{
  "success": false,
  "message": "Error message here"
}
```

### GET /health

Health check endpoint.

**Response (200):**
```json
{
  "status": "healthy",
  "message": "Contact API is running"
}
```

## Example Usage

### Using curl:

```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "phone": "+1234567890",
    "business_email": "john@example.com",
    "company": "Example Corp",
    "message": "Hello, I would like to know more about your services."
  }'
```

### Using JavaScript (fetch):

```javascript
fetch('http://localhost:5000/api/contact', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'John Doe',
    phone: '+1234567890',
    business_email: 'john@example.com',
    company: 'Example Corp',
    message: 'Hello, I would like to know more about your services.'
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Security Notes

- Never commit your `.env` file to version control
- Use App Passwords for Gmail instead of your regular password
- Consider using environment variables directly in production instead of `.env` files
- For production, use a proper WSGI server like Gunicorn or uWSGI
- Enable HTTPS in production

## Production Deployment

### Deploying to Render

This app is configured for deployment on Render. Follow these steps:

#### Option 1: Using Render Dashboard (Recommended)

1. **Push your code to GitHub/GitLab/Bitbucket**

2. **Create a new Web Service on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select the repository containing this code

3. **Configure the service:**
   - **Name:** `krazio-email-api` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

4. **Set Environment Variables in Render Dashboard:**
   - Go to your service → Environment tab
   - Add the following environment variables:
     ```
     SMTP_SERVER=smtp.gmail.com
     SMTP_PORT=587
     SMTP_USERNAME=your-email@gmail.com
     SMTP_PASSWORD=your-app-password
     FROM_EMAIL=your-email@gmail.com
     TO_EMAIL=recipient@example.com
     ```

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Your API will be available at `https://your-service-name.onrender.com`

#### Option 2: Using render.yaml (Infrastructure as Code)

If you're using `render.yaml`, Render will automatically configure the service:

1. Push your code (including `render.yaml`) to your repository
2. In Render Dashboard, select "New +" → "Blueprint"
3. Connect your repository
4. Render will read `render.yaml` and create the service
5. Set the environment variables in the Render dashboard (they're marked as `sync: false` in the YAML)

#### Important Notes for Render:

- **Port:** Render automatically sets the `PORT` environment variable. The app uses this automatically.
- **HTTPS:** Render provides HTTPS by default for all services
- **Free Tier:** Render's free tier spins down after 15 minutes of inactivity. Consider upgrading for production use.
- **Environment Variables:** Never commit sensitive credentials. Always set them in the Render dashboard.

### Local Production Testing

For local production testing, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

