# SendGrid Setup Guide

## What You Need to Provide

### Just One Thing: **SendGrid API Key**

That's it! I'll handle all the code integration. You just need to:

1. **Sign up for SendGrid** (it's free)
2. **Get your API Key**
3. **Give me the API Key** (I'll add it to your environment variables)

---

## Step-by-Step: Getting Your SendGrid API Key

### Step 1: Sign Up for SendGrid

1. Go to: https://sendgrid.com/
2. Click **"Start for Free"** or **"Sign Up"**
3. Fill in your details:
   - Email address
   - Password
   - Company name (optional)
4. **No credit card required** for the free tier!

### Step 2: Verify Your Email

- Check your email inbox
- Click the verification link from SendGrid

### Step 3: Create an API Key

1. Once logged in, go to: **Settings → API Keys**
   - Or visit: https://app.sendgrid.com/settings/api_keys

2. Click **"Create API Key"**

3. Choose permissions:
   - **Name:** `Krazio Email API` (or any name you like)
   - **Permissions:** Select **"Full Access"** (or just "Mail Send" if you prefer)

4. Click **"Create & View"**

5. **IMPORTANT:** Copy the API key immediately!
   - It will look something like: `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
   - You can only see it once! Save it somewhere safe.

### Step 4: Verify Your Sender Email (Important!)

SendGrid requires you to verify the email address you'll be sending FROM:

1. Go to: **Settings → Sender Authentication**
   - Or visit: https://app.sendgrid.com/settings/sender_auth

2. Click **"Verify a Single Sender"**

3. Fill in the form:
   - **From Email Address:** `krazio.developers@gmail.com` (or your email)
   - **From Name:** `Krazio Team` (or your company name)
   - Fill in the rest of the required fields

4. Check your email and click the verification link

---

## What I Need From You

Just provide me with:

```
SENDGRID_API_KEY=SG.your_api_key_here
```

**That's it!** I'll:
- ✅ Install the SendGrid library
- ✅ Update your code to use SendGrid
- ✅ Keep all your existing HTML email templates (no changes needed!)
- ✅ Update environment variables
- ✅ Make it work on both Render and your dedicated server

---

## Environment Variables You'll Need

After integration, you'll set these environment variables:

### For Render (Render Dashboard):
```
SENDGRID_API_KEY=SG.your_api_key_here
FROM_EMAIL=krazio.developers@gmail.com
TO_EMAIL=krazio.developers@gmail.com
```

### For Dedicated Server (.env file):
```
SENDGRID_API_KEY=SG.your_api_key_here
FROM_EMAIL=krazio.developers@gmail.com
TO_EMAIL=krazio.developers@gmail.com
```

**Note:** You can remove all the SMTP_* variables once SendGrid is set up (or keep them if you want SMTP as backup for dedicated server).

---

## Free Tier Limits

- **100 emails per day** (3,000 per month)
- Perfect for contact forms (2 emails per submission = 50 submissions/day)
- No credit card required
- No expiration

---

## Security Notes

- ✅ Never commit your API key to Git
- ✅ Store it only in environment variables
- ✅ The API key I'll use will only have "Mail Send" permissions (minimum required)
- ✅ You can revoke/recreate API keys anytime from SendGrid dashboard

---

## Ready?

Once you have your SendGrid API key, just let me know and I'll:
1. Integrate SendGrid into your code
2. Test it works correctly
3. Update all deployment files
4. Make it production-ready!

**Time needed:** Integration takes about 5-10 minutes once I have your API key.

