# Fix SendGrid 403 Forbidden Error

## ❌ Error: HTTP Error 403: Forbidden

This error means **your sender email is not verified** in SendGrid.

## ✅ Quick Fix

You need to verify your sender email address in SendGrid:

1. **Go to SendGrid Dashboard**: https://app.sendgrid.com

2. **Navigate to Settings → Sender Authentication**
   - Direct link: https://app.sendgrid.com/settings/sender_auth

3. **Click "Verify a Single Sender"**

4. **Fill in the form:**
   - **From Email Address:** `krazio.developers@gmail.com` (your FROM_EMAIL)
   - **From Name:** `Krazio Team` (or your company name)
   - Fill in all other required fields

5. **Check your email inbox** (krazio.developers@gmail.com)

6. **Click the verification link** in the email from SendGrid

7. **Done!** Your emails should now work.

## 🔍 Verify It's Set Up

After verifying, test again:

```bash
curl -X POST http://localhost:5001/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "phone": "+1234567890",
    "business_email": "test@example.com",
    "company": "Test Company",
    "message": "Testing after verification"
  }'
```

## 📋 Alternative: Domain Authentication

If you want to send from any email on your domain (more advanced):

1. Go to **Settings → Sender Authentication → Domain Authentication**
2. Follow the DNS setup instructions
3. This allows sending from any email on your domain

For now, **Single Sender Verification is the easiest** and works immediately.

## ⚠️ Important Notes

- You **must verify the sender email** before SendGrid will send emails
- The verification email might take a few minutes to arrive
- Check spam folder if you don't see it
- Once verified, it works immediately (no wait time)

## 🚀 After Verification

Once your sender email is verified:
1. Restart your app (if needed)
2. Test the contact form again
3. Emails should send successfully!

---

**Need help?** Check SendGrid docs: https://docs.sendgrid.com/ui/sending-email/sender-verification

