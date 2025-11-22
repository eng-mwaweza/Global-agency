# Generated migration for updating existing payment records

from django.db import migrations
from datetime import datetime


def update_existing_payments(apps, schema_editor):
    """Update existing payment records with unique order references"""
    Payment = apps.get_model('student_portal', 'Payment')
    
    for idx, payment in enumerate(Payment.objects.all(), start=1):
        # Generate unique order reference for existing payments
        timestamp = int(datetime.now().timestamp())
        payment.order_reference = f"LEGACY{payment.id}_{timestamp}_{idx}"
        payment.currency = 'TZS'
        payment.status = 'success' if payment.is_successful else 'failed'
        payment.payment_gateway = 'manual'
        payment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('student_portal', '0004_applicationassignment'),
    ]

    operations = [
        migrations.RunPython(update_existing_payments),
    ]
