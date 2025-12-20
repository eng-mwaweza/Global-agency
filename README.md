# Africa Western Education - Student Application Portal

A Django-based web application for managing student applications for universities abroad.

## 🆕 Latest Update: ClickPesa Payment Gateway Integration

The student portal now supports **real payment processing** through ClickPesa API!

### Payment Methods Available:
- ✅ **Mobile Money** (M-Pesa, Tigo Pesa, Airtel Money, HaloPesa) via USSD-PUSH
- ✅ **Card Payments** (Visa/Mastercard) via secure hosted page
- ✅ **Multi-gateway support** (ClickPesa, AzamPay, Manual)

### Quick Start with ClickPesa:

1. **Get your credentials** from [ClickPesa Dashboard](https://dashboard.clickpesa.com)

2. **Update `.env` file:**
```env
CLICKPESA_CLIENT_ID=your_client_id_here
CLICKPESA_API_KEY=your_api_key_here
PAYMENT_GATEWAY=clickpesa
```

3. **Run setup script:**
```powershell
.\setup_clickpesa.ps1
```

**📖 Full Documentation:**
- [Quick Start Guide](QUICKSTART.md) - Setup in 5 minutes
- [Integration Guide](CLICKPESA_INTEGRATION.md) - Complete technical docs
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - What was added
- [Changes Overview](CHANGES.txt) - Files modified

## Standard Setup (Without Payment Gateway)

Run:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Features

- Student registration and profile management
- Application submission for universities
- Document upload and management
- Payment processing (Mobile Money, Cards)
- Employee/Admin dashboard
- Application tracking and status updates
- Multi-gateway payment support

## Technology Stack

- **Backend:** Django 4.2
- **Database:** SQLite (development) / PostgreSQL (production)
- **Payment Gateway:** ClickPesa API
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Bootstrap, Custom CSS

## Project Structure

```
Global-agency/
├── globalagency_project/     # Main project settings
├── student_portal/           # Student portal app
│   ├── clickpesa_service.py # Payment gateway integration
│   ├── models.py            # Database models
│   ├── views.py             # Business logic
│   └── templates/           # HTML templates
├── employee/                 # Employee/Admin app
├── global_agency/            # Main app
├── .env                      # Environment variables (create this)
├── requirements.txt          # Python dependencies
└── manage.py                # Django management script
```

## Environment Variables

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your_secret_key_here
DEBUG=True

# ClickPesa API Credentials
CLICKPESA_CLIENT_ID=your_client_id_here
CLICKPESA_API_KEY=your_api_key_here
CLICKPESA_BASE_URL=https://api.clickpesa.com/third-parties

# Payment Gateway Selection
PAYMENT_GATEWAY=clickpesa

# Application Settings
CURRENCY=TZS
```

## Admin Access

Access the admin panel at: `http://127.0.0.1:8000/admin/`

Manage:
- Applications
- Payments
- Students
- Documents
- Messages

## Testing Payments

### Mobile Money (Sandbox):
- Use test phone numbers from ClickPesa
- Enter test PIN when prompted
- Payment verified automatically

### Card Payments (Test):
- Card: 4111 1111 1111 1111
- Expiry: Any future date
- CVV: 123

## Production Deployment

Before going live:
1. ✅ Get production ClickPesa credentials
2. ✅ Set `DEBUG=False` in `.env`
3. ✅ Configure `ALLOWED_HOSTS`
4. ✅ Set up HTTPS/SSL
5. ✅ Register webhook URL in ClickPesa dashboard
6. ✅ Use production database (PostgreSQL)
7. ✅ Test with small real amounts first

See [CLICKPESA_INTEGRATION.md](CLICKPESA_INTEGRATION.md) for complete production guide.

## Support

- **ClickPesa Issues:** support@clickpesa.com
- **ClickPesa Dashboard:** https://dashboard.clickpesa.com
- **ClickPesa Docs:** https://developer.clickpesa.com

## License

© 2025 Africa Western Education. All rights reserved.