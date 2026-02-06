# ClickPesa Payment Gateway Integration

This document explains the ClickPesa payment gateway integration for the Africa Western Education Student Portal.

## Overview

The student portal now supports real payment processing through ClickPesa API, allowing students to pay for their applications using:
- **Mobile Money** (M-Pesa, Tigo Pesa, Airtel Money, etc.) via USSD-PUSH
- **Card Payments** (Visa/Mastercard) via hosted payment page

## Setup Instructions

### 1. Get ClickPesa API Credentials

1. Sign up at [ClickPesa Dashboard](https://dashboard.clickpesa.com)
2. Create a new application
3. Copy your `Client ID` and `API Key`

### 2. Configure Environment Variables

Edit the `.env` file in the project root:

```env
# ClickPesa API Credentials
CLICKPESA_CLIENT_ID=your_actual_client_id_here
CLICKPESA_API_KEY=your_actual_api_key_here
CLICKPESA_BASE_URL=https://api.clickpesa.com/third-parties

# Payment Gateway Selection
PAYMENT_GATEWAY=clickpesa

# Currency
CURRENCY=TZS
```

**Important:** Replace `your_actual_client_id_here` and `your_actual_api_key_here` with your real credentials from ClickPesa dashboard.

### 3. Install Dependencies

```powershell
# Activate virtual environment
.\env\Scripts\Activate.ps1

# Install required packages
pip install -r requirements.txt
```

### 4. Run Database Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 5. Start the Development Server

```powershell
python manage.py runserver
```

## How It Works

### Mobile Money Payment Flow

1. **Student submits application** → Redirected to payment page
2. **Student enters phone number** → ClickPesa validates the number
3. **USSD push sent** → Student receives USSD prompt on their phone
4. **Student enters PIN** → Payment is authorized
5. **Auto-verification** → Page auto-refreshes every 10 seconds to check status
6. **Payment confirmed** → Application status updated to "submitted"

### Card Payment Flow

1. **Student selects card payment** → Preview validates payment details
2. **Payment link generated** → Student redirected to ClickPesa hosted page
3. **Student enters card details** → Secure card payment on ClickPesa servers
4. **Payment processed** → Student redirected back to verification page
5. **Status confirmed** → Application updated automatically

## API Endpoints

### Student Portal URLs

- `POST /student-portal/applications/<id>/payment/` - Process payment
- `GET /student-portal/payment/<id>/verify/` - Payment verification page
- `GET /student-portal/payment/<id>/status/` - AJAX status check
- `POST /student-portal/webhook/clickpesa/` - ClickPesa webhook (for callbacks)

### ClickPesa Webhook Setup

Register your webhook URL in ClickPesa dashboard:
```
https://yourdomain.com/student-portal/webhook/clickpesa/
```

This allows ClickPesa to notify your system when payment status changes.

## Payment Model Fields

The `Payment` model includes:

- `order_reference` - Unique reference for each transaction
- `transaction_id` - ClickPesa transaction ID
- `payment_reference` - Payment reference from provider
- `status` - pending, processing, success, failed, settled
- `payment_gateway` - clickpesa, azampay, or manual
- `payment_method` - mobile_money, card, bank_transfer
- `currency` - TZS or USD
- `clickpesa_response` - JSON field storing full API response

## Testing

### Test Mobile Money Payment

1. Create a new application
2. Enter test phone number (get test credentials from ClickPesa)
3. Use test PIN to complete payment
4. Verify payment status updates automatically

### Test Card Payment

1. Create a new application
2. Select card payment option
3. Use ClickPesa test card numbers:
   - Card: 4111 1111 1111 1111
   - Expiry: Any future date
   - CVV: 123

## Payment Gateway Switching

To switch between payment gateways, update `.env`:

```env
# Use ClickPesa
PAYMENT_GATEWAY=clickpesa

# Or use AzamPay (legacy)
PAYMENT_GATEWAY=azampay

# Or disable online payments
PAYMENT_GATEWAY=manual
```

## Troubleshooting

### Common Issues

1. **"Token generation failed"**
   - Check your `CLICKPESA_CLIENT_ID` and `CLICKPESA_API_KEY` in `.env`
   - Ensure credentials are correct in ClickPesa dashboard
   - Check API endpoint URL

2. **"No payment channels available"**
   - Mobile money provider may be down
   - Try different phone number
   - Check ClickPesa status page

3. **"Payment stuck in processing"**
   - Click "Check Status Now" button
   - Wait for customer to complete payment on their phone
   - Check ClickPesa dashboard for transaction status

4. **Webhook not receiving callbacks**
   - Ensure webhook URL is registered in ClickPesa dashboard
   - Webhook must be publicly accessible (not localhost)
   - Check server logs for incoming requests

### Debug Mode

Enable detailed logging in `clickpesa_service.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Notes

- Never commit `.env` file to version control
- Keep API credentials secret
- Use HTTPS in production
- Validate webhook signatures (implement checksum validation)
- Monitor failed payment attempts

## ClickPesa API Documentation

Full API docs: https://developer.clickpesa.com/

### Key Endpoints Used

- `POST /payments/preview-ussd-push-request` - Validate mobile money
- `POST /payments/initiate-ussd-push-request` - Send USSD push
- `POST /payments/preview-card-payment` - Validate card payment
- `POST /payments/initiate-card-payment` - Create card payment link
- `GET /payments/{orderReference}` - Check payment status
- `GET /account/balance` - Check account balance

## Support

For ClickPesa API issues:
- Email: support@clickpesa.com
- Dashboard: https://dashboard.clickpesa.com

For integration issues:
- Check server logs
- Review payment records in Django admin
- Test with smaller amounts first

## Production Checklist

Before going live:

- [ ] Update `DEBUG=False` in `.env`
- [ ] Set proper `ALLOWED_HOSTS` in settings
- [ ] Configure production database
- [ ] Set up HTTPS/SSL certificate
- [ ] Register production webhook URL
- [ ] Test with real small amounts
- [ ] Set up payment monitoring
- [ ] Configure email notifications
- [ ] Enable ClickPesa production mode
- [ ] Set up backup payment gateway

## License

This integration is part of the Africa Western Education platform.
