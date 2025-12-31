# Testing Your Email API

## 🚀 App is Running!

Your Flask app is now running on **http://localhost:5001**

## ✅ Test Endpoints

### 1. Health Check
```bash
curl http://localhost:5001/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Contact API is running"
}
```

### 2. Root Endpoint
```bash
curl http://localhost:5001/
```

### 3. Test Contact Form (Send Real Email)

**Important:** This will send 2 emails:
1. Admin notification to `TO_EMAIL` (krazio.developers@gmail.com)
2. User confirmation to the `business_email` provided

```bash
curl -X POST http://localhost:5001/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+1234567890",
    "business_email": "test@example.com",
    "company": "Test Company",
    "message": "This is a test message from the API"
  }'
```

Expected response (success):
```json
{
  "success": true,
  "message": "Contact form submitted successfully. A confirmation email has been sent to your business email. We will get back to you soon!"
}
```

## 📧 What Happens

When you submit the contact form:
1. ✅ Admin receives a beautiful HTML email at `TO_EMAIL` (krazio.developers@gmail.com)
2. ✅ User receives a confirmation email at the `business_email` they provided
3. ✅ Both emails are sent via **SendGrid** (you should see "✓ Using SendGrid for email delivery" in logs)

## 🔍 Check Logs

View app logs:
```bash
tail -f /tmp/flask_app.log
```

Or if running in terminal:
- Check the terminal where the app is running
- Look for "✓ Using SendGrid for email delivery" message

## 🛑 Stop the App

```bash
pkill -f "python.*app.py"
```

Or press `Ctrl+C` if running in foreground.

## 🌐 Alternative Test (Browser)

You can also test using a browser or Postman:

1. Open: http://localhost:5001/health
2. Or use Postman/Insomnia to send POST requests to:
   - URL: http://localhost:5001/api/contact
   - Method: POST
   - Headers: Content-Type: application/json
   - Body: (use the JSON from the curl example above)

## ✅ Success Indicators

- Health endpoint returns `{"status": "healthy"}`
- Contact form returns `{"success": true}`
- You receive emails in your inbox
- Logs show "✓ Using SendGrid for email delivery"

## 🐛 Troubleshooting

If emails don't send:
1. Check logs for errors
2. Verify SendGrid API key is correct
3. Verify FROM_EMAIL is verified in SendGrid dashboard
4. Check SendGrid dashboard for delivery status

