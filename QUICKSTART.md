# ClickPesa Integration - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Get Your ClickPesa Credentials
1. Visit https://dashboard.clickpesa.com
2. Sign up or log in
3. Create a new application
4. Copy your **Client ID** and **API Key**

### Step 2: Configure Your Environment
1. Open `.env` file in the project root
2. Update these lines with your credentials:
```env
CLICKPESA_CLIENT_ID=your_client_id_here
CLICKPESA_API_KEY=your_api_key_here
PAYMENT_GATEWAY=clickpesa
```

### Step 3: Run Setup Script
```powershell
.\setup_clickpesa.ps1
```

Or manually:
```powershell
# Activate virtual environment
.\env\Scripts\Activate.ps1

# Install packages
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### Step 4: Test Payment
1. Go to http://127.0.0.1:8000/student-portal/
2. Create a new application
3. Enter a test phone number (get from ClickPesa docs)
4. Complete the payment with test PIN

## 📱 Payment Methods Supported

### Mobile Money (USSD-PUSH)
- M-Pesa Tanzania
- Tigo Pesa
- Airtel Money
- HaloPesa

**How it works:**
1. Student enters phone number (e.g., 255712345678)
2. USSD prompt sent to their phone
3. Student enters PIN to authorize
4. Payment confirmed automatically

### Card Payments (Visa/Mastercard)
- International cards supported
- Secure hosted payment page
- 3D Secure authentication

**How it works:**
1. Student selects card payment
2. Redirected to ClickPesa secure page
3. Enters card details
4. Payment processed instantly

## 🔧 Configuration Options

### Switch Payment Gateway

Edit `.env`:
```env
# Use ClickPesa (recommended)
PAYMENT_GATEWAY=clickpesa

# Use AzamPay (legacy)
PAYMENT_GATEWAY=azampay

# Disable online payments
PAYMENT_GATEWAY=manual
```

### Change Currency
```env
# For mobile money (Tanzania)
CURRENCY=TZS

# For card payments (international)
CURRENCY=USD
```

### Payment Amount
In `student_portal/views.py` line 140:
```python
application.payment_amount = 5000  # Change this value
```

Or in Application model default:
```python
payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)
```

## 📊 Admin Panel

View all payments at:
```
http://127.0.0.1:8000/admin/student_portal/payment/
```

Filter by:
- Status (pending, processing, success, failed)
- Payment method (mobile_money, card)
- Payment gateway (clickpesa, azampay)
- Date range

## 🔍 Testing

### Test Mobile Money
Use ClickPesa sandbox credentials:
- Phone: Get test numbers from ClickPesa
- PIN: Use sandbox PIN

### Test Card Payment
Test card details:
```
Card Number: 4111 1111 1111 1111
Expiry: Any future date (e.g., 12/25)
CVV: 123
Name: Test User
```

## 🔔 Webhook Setup (Production)

Register your webhook in ClickPesa dashboard:
```
https://yourdomain.com/student-portal/webhook/clickpesa/
```

This allows automatic payment status updates.

## ⚠️ Common Issues

### "Token generation failed"
- ✅ Check CLICKPESA_CLIENT_ID and CLICKPESA_API_KEY in `.env`
- ✅ Ensure no extra spaces in credentials
- ✅ Verify credentials are active in ClickPesa dashboard

### "No payment channels available"
- ✅ Mobile provider may be temporarily down
- ✅ Try different phone number
- ✅ Check ClickPesa status page

### Payment stuck in "Processing"
- ✅ Student may not have completed USSD prompt
- ✅ Click "Check Status Now" button
- ✅ Allow up to 2 minutes for processing

### Import error: decouple
```powershell
pip install python-decouple
```

### Import error: requests
```powershell
pip install requests
```

## 📞 Support

### ClickPesa Support
- Email: support@clickpesa.com
- Dashboard: https://dashboard.clickpesa.com
- Docs: https://developer.clickpesa.com

### Integration Issues
1. Check `CLICKPESA_INTEGRATION.md` for detailed docs
2. Review Django logs for errors
3. Test with small amounts first
4. Verify credentials are correct

## 🎯 Features Implemented

✅ Mobile money payments (USSD-PUSH)
✅ Card payments (hosted page)
✅ Payment status tracking
✅ Automatic verification
✅ Webhook support
✅ Payment history
✅ Multi-gateway support
✅ Error handling
✅ Transaction logging

## 📝 Important Files

- `.env` - API credentials
- `student_portal/clickpesa_service.py` - Payment API
- `student_portal/models.py` - Payment model
- `student_portal/views.py` - Payment views
- `CLICKPESA_INTEGRATION.md` - Full documentation

## 🚦 Production Checklist

Before going live:
- [ ] Get production API credentials
- [ ] Update `.env` with production keys
- [ ] Set `DEBUG=False`
- [ ] Configure HTTPS/SSL
- [ ] Register production webhook URL
- [ ] Test with real small amounts
- [ ] Set up error monitoring
- [ ] Configure email notifications
- [ ] Review security settings
- [ ] Set up database backups

## 💡 Tips

1. **Always test in sandbox first** before using production
2. **Keep API credentials secure** - never commit to Git
3. **Monitor payment logs** in Django admin
4. **Set up email notifications** for failed payments
5. **Use descriptive order references** for easier tracking
6. **Implement payment reconciliation** for accounting

## 🔐 Security Best Practices

- ✅ API keys stored in `.env` (not in code)
- ✅ `.env` file in `.gitignore`
- ✅ CSRF protection enabled
- ✅ HTTPS required in production
- ✅ Webhook signature verification (optional)
- ✅ Rate limiting on payment endpoints (recommended)

---

**Happy Coding! 🎉**

For detailed documentation, see `CLICKPESA_INTEGRATION.md`
