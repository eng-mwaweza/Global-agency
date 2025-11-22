# ClickPesa Integration Troubleshooting Guide

## Current Issue: 401 Unauthorized Error

### Problem
When attempting to make payments, you're receiving:
```
Payment preview failed: Invalid JSON response from ClickPesa API. Status: 401, Content: Unauthorized
```

### Root Cause
Your ClickPesa API credentials are **INVALID or EXPIRED**. All authentication methods tested (Bearer token, X-API-Key, Basic Auth, etc.) return 401 Unauthorized.

---

## Solution: Get Valid ClickPesa Credentials

### Step 1: Access ClickPesa Dashboard

1. **Go to**: https://dashboard.clickpesa.com
2. **Log in** with your ClickPesa account credentials
3. If you don't have an account:
   - Sign up at https://clickpesa.com
   - Complete the registration process
   - Verify your account

### Step 2: Get API Credentials

Once logged in:

1. **Navigate to** one of these sections (depending on your dashboard layout):
   - **Settings** → **API Credentials**
   - **Developer** → **API Keys**
   - **Account** → **API Settings**
   - **Integration** → **API Access**

2. **Generate new credentials** or copy existing valid ones:
   - Look for "Generate API Key" or "Create New Credentials"
   - You'll receive:
     - **Client ID** (32 characters, format: `IDxxxxxxxxxxxxxxxxxxxxxxxxxx`)
     - **API Key** (40-50 characters, format: `SKxxxxxxxxxxxxxxxxxxxxxxxxxx`)

3. **Copy both values** carefully

### Step 3: Update Your .env File

1. Open `c:\Users\USER\Desktop\Global-agency\.env`

2. Replace the credentials:
   ```env
   CLICKPESA_CLIENT_ID=<paste_your_new_client_id_here>
   CLICKPESA_API_KEY=<paste_your_new_api_key_here>
   CLICKPESA_BASE_URL=https://api.clickpesa.com/third-parties
   ```

3. **Remove any extra spaces** or quotes

4. **Save the file**

### Step 4: Verify Environment

Make sure you're using the correct API URL:

- **Production**: `https://api.clickpesa.com/third-parties`
- **Sandbox** (if available): Check ClickPesa documentation for sandbox URL
  - May be: `https://sandbox.clickpesa.com/third-parties`
  - Or: `https://api-sandbox.clickpesa.com/third-parties`

If testing, use sandbox credentials with sandbox URL.

### Step 5: Restart Django Server

**Important**: Environment variables are loaded when Django starts.

1. **Stop the server**: Press `Ctrl+C` in the terminal running the server

2. **Restart**:
   ```powershell
   python manage.py runserver
   ```

3. **Clear browser cache** or use incognito mode

### Step 6: Test Payment Again

1. Go to: http://localhost:8000/student-portal/applications/36/payment/
2. Try to make a payment
3. The error should be resolved

---

## Additional Checks

### Check 1: Account Status

Verify your ClickPesa account is:
- ✅ **Active** (not suspended or pending verification)
- ✅ **API access enabled** (some accounts need approval)
- ✅ **Payment limit sufficient** (some accounts have transaction limits)

### Check 2: IP Whitelist

Some ClickPesa accounts require IP whitelisting:

1. Check if your dashboard has "IP Whitelist" settings
2. Add your server's IP address
3. For local development, add: `127.0.0.1` and your public IP

### Check 3: API Version

Ensure you're using the correct API version:

- Current implementation uses: `/third-parties/payments/`
- If this doesn't work, check ClickPesa docs for API version changes

---

## Testing Credentials Manually

Run this command to test your credentials:

```powershell
python manage.py shell -c "
from student_portal.clickpesa_service import clickpesa_service
import logging
logging.basicConfig(level=logging.INFO)

success, data, error = clickpesa_service.preview_ussd_push(
    1000, '255712345678', 'TEST001', 'TZS'
)
print(f'Success: {success}')
print(f'Error: {error}')
"
```

**Expected result if credentials are valid**:
- `Success: True`
- No error message
- Data returned with payment preview details

**If still getting 401**:
- Credentials are still invalid
- Double-check you copied them correctly
- Generate new credentials from dashboard

---

## Common Mistakes

### ❌ Mistake 1: Using Old/Expired Credentials
**Solution**: Generate new credentials from dashboard

### ❌ Mistake 2: Extra Spaces in .env
```env
# WRONG
CLICKPESA_CLIENT_ID= IDe8QmHJgNYHEBVhpkmZTQ3smgQ7qzbz

# CORRECT
CLICKPESA_CLIENT_ID=IDe8QmHJgNYHEBVhpkmZTQ3smgQ7qzbz
```

### ❌ Mistake 3: Using Quotes
```env
# WRONG
CLICKPESA_CLIENT_ID="IDe8QmHJgNYHEBVhpkmZTQ3smgQ7qzbz"

# CORRECT
CLICKPESA_CLIENT_ID=IDe8QmHJgNYHEBVhpkmZTQ3smgQ7qzbz
```

### ❌ Mistake 4: Not Restarting Server
Always restart Django after changing .env

### ❌ Mistake 5: Sandbox/Production Mismatch
- Sandbox credentials → Sandbox URL
- Production credentials → Production URL

---

## Contact ClickPesa Support

If you've tried everything and still getting 401:

**ClickPesa Support:**
- Email: support@clickpesa.com
- Phone: Check their website
- Dashboard: Look for "Help" or "Support" section

**What to tell them:**
- "I'm getting 401 Unauthorized when calling preview-ussd-push-request API"
- "I need to verify my API credentials are active and valid"
- Provide your Client ID (NOT your API Key)
- Ask about IP whitelisting requirements

---

## Alternative: Use Demo/Test Mode

While waiting for valid credentials, you can:

1. Set `PAYMENT_GATEWAY=demo` in .env (if implemented)
2. Or modify views to skip actual API calls during development
3. Or use mock responses for testing

---

## Summary

**The core issue**: Your current ClickPesa credentials (`IDe8QmHJgN...` and `SKEMa028C6...`) are **NOT AUTHORIZED** to access the ClickPesa API.

**The fix**: Get fresh, valid credentials from https://dashboard.clickpesa.com and update your .env file.

**After fix**: Restart server and test payment.

**If still broken**: Contact ClickPesa support to verify your account has API access.
