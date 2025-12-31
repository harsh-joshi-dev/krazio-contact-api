# Troubleshooting SendGrid 403 Error (Even After Verification)

## ❌ Still Getting 403 After Verification?

If you've verified your sender email but still get 403 errors, check these:

## ✅ Checklist

### 1. Verify API Key Permissions

Your API key needs "Mail Send" permissions:

1. Go to SendGrid Dashboard: https://app.sendgrid.com
2. Navigate to: **Settings → API Keys**
3. Find your API key (or create a new one)
4. Click on it to view/edit
5. Make sure **"Mail Send"** permission is enabled (or use "Full Access")
6. Save changes

**If using a restricted API key:**
- Create a new API key with "Full Access" for testing
- Or ensure "Mail Send" permission is specifically enabled

### 2. Verify Sender Email Status

1. Go to: **Settings → Sender Authentication → Single Sender Verification**
2. Check that `krazio.developers@gmail.com` shows a **green checkmark (✓)**
3. If it shows red X, the verification isn't complete - check your email again
4. The email must be fully verified (green checkmark) before it works

### 3. Verify Email Address Matches Exactly

Make sure the `FROM_EMAIL` in your `.env` file matches the verified sender **exactly**:

```env
FROM_EMAIL=krazio.developers@gmail.com
```

- No extra spaces
- All lowercase (Gmail addresses are case-insensitive, but keep it consistent)
- Exact match with what's verified in SendGrid

### 4. Check SendGrid Account Status

1. Check for any account warnings/alerts in SendGrid dashboard
2. Ensure your account is active (not suspended)
3. Check if there are any billing issues (even on free tier)

### 5. Wait a Few Minutes

Sometimes verification can take a few minutes to propagate:
- Verify the sender email
- Wait 2-5 minutes
- Try again

### 6. Create a New API Key

If nothing works, create a fresh API key:

1. Go to: **Settings → API Keys**
2. Click **"Create API Key"**
3. Name it: "Krazio Email API - Production"
4. Choose **"Full Access"** (or at minimum, ensure "Mail Send" is enabled)
5. Copy the new API key
6. Update your `.env` file:

```env
SENDGRID_API_KEY=SG.your_new_api_key_here
```

7. Restart your app

### 7. Verify Sender Identity Type

**Single Sender Verification** (what you likely have):
- ✅ Good for testing and small volumes
- ✅ Quick to set up
- ❌ Limited (only that one email address)

**Domain Authentication** (better for production):
- ✅ Can send from any email on your domain
- ✅ Better deliverability
- ❌ Requires DNS setup

For now, **Single Sender Verification** should work fine.

## 🔍 Test Steps

1. **Verify API Key works:**
   ```bash
   # In SendGrid dashboard, go to API Keys
   # Check that your key has "Mail Send" permission
   ```

2. **Verify sender is verified:**
   ```bash
   # In SendGrid dashboard
   # Settings > Sender Authentication > Single Sender Verification
   # Should show green checkmark (✓) not red X
   ```

3. **Check FROM_EMAIL matches:**
   ```bash
   cat .env | grep FROM_EMAIL
   # Should be: FROM_EMAIL=krazio.developers@gmail.com
   # Must match exactly what's verified in SendGrid
   ```

4. **Test with new API key:**
   ```bash
   # Create new API key with Full Access
   # Update .env file
   # Restart app
   ```

## 🆘 Still Not Working?

1. **Check SendGrid Activity Feed:**
   - Go to: **Activity → Email Activity**
   - See if emails are being attempted
   - Check error messages there

2. **Contact SendGrid Support:**
   - Go to: https://support.sendgrid.com
   - They can check your account settings

3. **Try Domain Authentication:**
   - More complex but more reliable
   - Go to: Settings > Sender Authentication > Domain Authentication

## ✅ Most Common Solution

**90% of the time, the issue is:**
- API key doesn't have "Mail Send" permissions
- Or sender email verification isn't complete (red X instead of green ✓)

**Fix:**
1. Check API key permissions → Enable "Mail Send"
2. Verify sender email → Must show green checkmark
3. Restart app
4. Test again

