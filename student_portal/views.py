from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import StudentProfile, Application, Document, Message, Payment
from .forms import StudentProfileForm, DocumentForm, ApplicationForm

def student_login(request):
    if request.user.is_authenticated:
        return redirect('student_portal:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('student_portal:dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
    
    return render(request, 'student_portal/login.html')

@login_required(login_url='student_portal:login')
def student_dashboard(request):
    # Get student data
    applications = Application.objects.filter(student=request.user)
    documents = Document.objects.filter(student=request.user)
    unread_messages = Message.objects.filter(student=request.user, is_read=False)
    
    context = {
        'applications': applications,
        'documents_count': documents.count(),
        'unread_messages_count': unread_messages.count(),
    }
    return render(request, 'student_portal/dashboard.html', context)

@login_required
def student_profile(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('student_portal:profile')
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student_portal/profile.html', {'form': form, 'profile': profile})

@login_required
def applications(request):
    applications_list = Application.objects.filter(student=request.user)
    return render(request, 'student_portal/applications.html', {'applications': applications_list})

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id, student=request.user)
    return render(request, 'student_portal/application_detail.html', {'application': application})

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = request.user
            application.status = 'pending_payment'
            application.payment_amount = 50000  # Set payment amount
            application.save()
            messages.success(request, 'Application created! Please complete payment to submit.')
            return redirect('student_portal:payment', application_id=application.id)
    else:
        form = ApplicationForm()
    
    return render(request, 'student_portal/create_application.html', {'form': form})

@login_required
def payment_page(request, application_id):
    application = get_object_or_404(Application, id=application_id, student=request.user)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')
        mobile_provider = request.POST.get('mobile_provider')
        
        if payment_method == 'mobile_money':
            # Process mobile money payment
            return process_mobile_money_payment(request, application, phone_number, mobile_provider)
        elif payment_method == 'bank_transfer':
            # Process bank transfer
            return process_bank_transfer(request, application)
        elif payment_method == 'card':
            # Process card payment
            return process_card_payment(request, application)
    
    return render(request, 'student_portal/payment.html', {
        'application': application,
        'payment_amount': application.payment_amount
    })

def process_mobile_money_payment(request, application, phone_number, provider):
    """Process mobile money payment"""
    try:
        # Generate unique transaction ID
        transaction_id = f"MM{application.id}{int(datetime.now().timestamp())}"
        
        # Create pending payment record
        payment = Payment.objects.create(
            student=request.user,
            application=application,
            amount=application.payment_amount,
            payment_method='mobile_money',
            mobile_provider=provider,
            phone_number=phone_number,
            transaction_id=transaction_id,
            is_successful=False,
            status='pending'
        )
        
        # Simulate successful payment for demo
        # In production, integrate with actual mobile money APIs here
        
        payment.is_successful = True
        payment.status = 'completed'
        payment.save()
        
        # Update application status
        application.is_paid = True
        application.status = 'submitted'
        application.save()
        
        # Send success message based on provider
        provider_names = {
            'mpesa': 'M-Pesa',
            'tigo_pesa': 'Tigo Pesa', 
            'airtel_money': 'Airtel Money'
        }
        
        messages.success(
            request, 
            f'Payment successful via {provider_names.get(provider, "mobile money")}! Your application has been submitted.'
        )
        
        return redirect('student_portal:applications')
        
    except Exception as e:
        messages.error(request, f'Payment initiation failed: {str(e)}')
        return redirect('student_portal:payment', application_id=application.id)

def process_bank_transfer(request, application):
    """Process bank transfer payment"""
    try:
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        account_name = request.POST.get('account_name')
        
        transaction_id = f"BT{application.id}{int(datetime.now().timestamp())}"
        
        payment = Payment.objects.create(
            student=request.user,
            application=application,
            amount=application.payment_amount,
            payment_method='bank_transfer',
            bank_name=bank_name,
            account_number=account_number,
            account_name=account_name,
            transaction_id=transaction_id,
            is_successful=True,
            status='completed'
        )
        
        application.is_paid = True
        application.status = 'submitted'
        application.save()
        
        messages.success(request, 'Bank transfer payment completed successfully!')
        return redirect('student_portal:applications')
        
    except Exception as e:
        messages.error(request, f'Bank transfer failed: {str(e)}')
        return redirect('student_portal:payment', application_id=application.id)

def process_card_payment(request, application):
    """Process card payment"""
    try:
        card_number = request.POST.get('card_number', '')
        card_last_four = card_number[-4:] if card_number else '0000'
        
        transaction_id = f"CD{application.id}{int(datetime.now().timestamp())}"
        
        payment = Payment.objects.create(
            student=request.user,
            application=application,
            amount=application.payment_amount,
            payment_method='card',
            card_last_four=card_last_four,
            transaction_id=transaction_id,
            is_successful=True,
            status='completed'
        )
        
        application.is_paid = True
        application.status = 'submitted'
        application.save()
        
        messages.success(request, 'Card payment completed successfully!')
        return redirect('student_portal:applications')
        
    except Exception as e:
        messages.error(request, f'Card payment failed: {str(e)}')
        return redirect('student_portal:payment', application_id=application.id)

@login_required
def payment_verification(request, payment_id):
    """Page to verify payment status"""
    payment = get_object_or_404(Payment, id=payment_id, student=request.user)
    
    if request.method == 'POST':
        # Check payment status
        if not payment.is_successful:
            # Simulate payment verification
            payment.is_successful = True
            payment.status = 'completed'
            payment.save()
            
            payment.application.is_paid = True
            payment.application.status = 'submitted'
            payment.application.save()
            
            messages.success(request, 'Payment verified successfully!')
            return redirect('student_portal:applications')
        else:
            messages.info(request, 'Payment is still being processed. Please wait...')
    
    return render(request, 'student_portal/payment_verification.html', {
        'payment': payment,
        'application': payment.application
    })

@csrf_exempt
def payment_webhook(request, provider):
    """Webhook endpoint for payment providers"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract transaction details based on provider
            if provider == 'mpesa':
                transaction_id = data.get('TransID')
                status = data.get('ResultCode')
            elif provider == 'tigo_pesa':
                transaction_id = data.get('transaction_id')
                status = data.get('status')
            elif provider == 'airtel_money':
                transaction_id = data.get('id')
                status = data.get('status')
            
            # Find and update payment
            payment = Payment.objects.get(transaction_id=transaction_id)
            
            if status == '0' or status == 'success':
                payment.is_successful = True
                payment.status = 'completed'
                payment.save()
                
                payment.application.is_paid = True
                payment.application.status = 'submitted'
                payment.application.save()
                
            else:
                payment.status = 'failed'
                payment.save()
                
            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

@login_required
def documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.student = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('student_portal:documents')
    else:
        form = DocumentForm()
    
    documents_list = Document.objects.filter(student=request.user)
    return render(request, 'student_portal/documents.html', {'form': form, 'documents': documents_list})

@login_required
def document_services(request):
    return render(request, 'student_portal/document_services.html')

@login_required
def service_form(request, service_type):
    service_names = {
        'university': 'University Application',
        'visa': 'Visa Support',
        'passport': 'Passport Application',
        'loan': 'Student Loan Services',
        'tcu': 'TCU Services',
        'flight': 'Flight Ticket Booking',
    }
    
    if service_type not in service_names:
        messages.error(request, 'Invalid service type')
        return redirect('student_portal:document_services')
    
    return render(request, 'student_portal/service_form.html', {
        'service_type': service_type,
        'service_name': service_names[service_type]
    })

@login_required
def messages_list(request):
    messages_list = Message.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'student_portal/messages.html', {'messages_list': messages_list})

@login_required
def mark_message_read(request, message_id):
    message = get_object_or_404(Message, id=message_id, student=request.user)
    message.is_read = True
    message.save()
    return JsonResponse({'success': True})

def student_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student_portal:login')

# Utility function to check payment status
@login_required
def check_payment_status(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, student=request.user)
    return JsonResponse({
        'is_successful': payment.is_successful,
        'status': payment.status,
        'transaction_id': payment.transaction_id
    })