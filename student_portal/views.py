from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
import json
from datetime import datetime
from .models import StudentProfile, Application, Document, Message, Payment
from .forms import StudentProfileForm, DocumentForm, ApplicationForm

@csrf_protect
def student_login(request):
    if request.user.is_authenticated:
        return redirect('student_portal:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
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
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentProfileForm(instance=profile)
    
    return render(request, 'student_portal/profile.html', {'form': form, 'profile': profile})

@login_required
def applications(request):
    applications_list = Application.objects.filter(student=request.user).order_by('-created_at')
    return render(request, 'student_portal/applications.html', {'applications': applications_list})

@login_required
def application_detail(request, application_id):
    application = get_object_or_404(Application, id=application_id, student=request.user)
    return render(request, 'student_portal/application_detail.html', {'application': application})

@login_required
@csrf_protect
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            try:
                application = form.save(commit=False)
                application.student = request.user
                application.status = 'pending_payment'
                application.payment_amount = 5000  # Set payment amount
                application.save()
            
                return redirect('student_portal:payment', application_id=application.id)
                
            except Exception as e:
                messages.error(request, f'Error creating application: {str(e)}')
        else:
            # Form is invalid - display errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        error_messages.append(error)
                    else:
                        field_name = form.fields[field].label if field in form.fields else field
                        error_messages.append(f"{field_name}: {error}")
            
            if error_messages:
                messages.error(request, 'Please correct the following errors:')
                for error_msg in error_messages:
                    messages.error(request, error_msg)
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = ApplicationForm()
    
    return render(request, 'student_portal/create_application.html', {'form': form})

@login_required
@csrf_protect
def payment_page(request, application_id):
    application = get_object_or_404(Application, id=application_id, student=request.user)
    
    # Check if application is already paid
    if application.is_paid:
        messages.info(request, 'This application has already been paid for.')
        return redirect('student_portal:application_detail', application_id=application.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return render(request, 'student_portal/payment.html', {
                'application': application,
                'payment_amount': application.payment_amount
            })
        
        try:
            if payment_method == 'mobile_money':
                phone_number = request.POST.get('phone_number')
                mobile_provider = request.POST.get('mobile_provider')
                
                if not phone_number or not mobile_provider:
                    messages.error(request, 'Please provide phone number and mobile provider.')
                    return render(request, 'student_portal/payment.html', {
                        'application': application,
                        'payment_amount': application.payment_amount
                    })
                
                return process_mobile_money_payment(request, application, phone_number, mobile_provider)
                
            elif payment_method == 'bank_transfer':
                bank_name = request.POST.get('bank_name')
                account_number = request.POST.get('account_number')
                account_name = request.POST.get('account_name')
                
                if not all([bank_name, account_number, account_name]):
                    messages.error(request, 'Please provide all bank transfer details.')
                    return render(request, 'student_portal/payment.html', {
                        'application': application,
                        'payment_amount': application.payment_amount
                    })
                
                return process_bank_transfer(request, application, bank_name, account_number, account_name)
                
            elif payment_method == 'card':
                card_number = request.POST.get('card_number')
                card_holder = request.POST.get('card_holder')
                expiry_date = request.POST.get('expiry_date')
                cvv = request.POST.get('cvv')
                
                if not all([card_number, card_holder, expiry_date, cvv]):
                    messages.error(request, 'Please provide all card details.')
                    return render(request, 'student_portal/payment.html', {
                        'application': application,
                        'payment_amount': application.payment_amount
                    })
                
                return process_card_payment(request, application, card_number, card_holder, expiry_date, cvv)
                
            else:
                messages.error(request, 'Invalid payment method selected.')
                
        except Exception as e:
            messages.error(request, f'Payment processing failed: {str(e)}')
    
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
        
        # Simulate payment processing (replace with actual mobile money API integration)
        import time
        time.sleep(2)  # Simulate API call
        
        # For demo purposes, we'll simulate a successful payment
        # In production, you would integrate with actual mobile money APIs like:
        # - M-Pesa API
        # - Tigo Pesa API
        # - Airtel Money API
        
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
            'airtel_money': 'Airtel Money',
            'halopesa': 'HaloPesa'
        }
        
        messages.success(
            request, 
            f'Payment of TZS {application.payment_amount:,} successful via {provider_names.get(provider, "mobile money")}! Your application has been submitted.'
        )
        
        return redirect('student_portal:application_detail', application_id=application.id)
        
    except Exception as e:
        messages.error(request, f'Mobile money payment failed: {str(e)}')
        return redirect('student_portal:payment', application_id=application.id)

def process_bank_transfer(request, application, bank_name, account_number, account_name):
    """Process bank transfer payment"""
    try:
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
        
        messages.success(request, f'Bank transfer payment of TZS {application.payment_amount:,} completed successfully! Your application has been submitted.')
        return redirect('student_portal:application_detail', application_id=application.id)
        
    except Exception as e:
        messages.error(request, f'Bank transfer failed: {str(e)}')
        return redirect('student_portal:payment', application_id=application.id)

def process_card_payment(request, application, card_number, card_holder, expiry_date, cvv):
    """Process card payment"""
    try:
        # Basic card validation
        if len(card_number.replace(' ', '')) < 13:
            messages.error(request, 'Invalid card number')
            return redirect('student_portal:payment', application_id=application.id)
        
        if len(cvv) not in [3, 4]:
            messages.error(request, 'Invalid CVV')
            return redirect('student_portal:payment', application_id=application.id)
        
        card_last_four = card_number.replace(' ', '')[-4:]
        
        transaction_id = f"CD{application.id}{int(datetime.now().timestamp())}"
        
        payment = Payment.objects.create(
            student=request.user,
            application=application,
            amount=application.payment_amount,
            payment_method='card',
            card_last_four=card_last_four,
            card_holder=card_holder,
            transaction_id=transaction_id,
            is_successful=True,
            status='completed'
        )
        
        application.is_paid = True
        application.status = 'submitted'
        application.save()
        
        messages.success(request, f'Card payment of TZS {application.payment_amount:,} completed successfully! Your application has been submitted.')
        return redirect('student_portal:application_detail', application_id=application.id)
        
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
            transaction_id = None
            status = None
            
            if provider == 'mpesa':
                transaction_id = data.get('TransID')
                status = data.get('ResultCode')
            elif provider == 'tigo_pesa':
                transaction_id = data.get('transaction_id')
                status = data.get('status')
            elif provider == 'airtel_money':
                transaction_id = data.get('id')
                status = data.get('status')
            elif provider == 'halopesa':
                transaction_id = data.get('transactionId')
                status = data.get('status')
            
            if not transaction_id:
                return JsonResponse({'status': 'error', 'message': 'No transaction ID provided'})
            
            # Find and update payment
            try:
                payment = Payment.objects.get(transaction_id=transaction_id)
                
                if status in ['0', 'success', 'completed']:
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
                
            except Payment.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Payment not found'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'})

@login_required
def documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.student = request.user
                document.save()
                messages.success(request, 'Document uploaded successfully!')
                return redirect('student_portal:documents')
            except Exception as e:
                messages.error(request, f'Error uploading document: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DocumentForm()
    
    documents_list = Document.objects.filter(student=request.user).order_by('-uploaded_at')
    return render(request, 'student_portal/documents.html', {
        'form': form, 
        'documents': documents_list
    })

@login_required
def document_services(request):
    services = [
        {'type': 'university', 'name': 'University Application', 'description': 'Assistance with university applications'},
        {'type': 'visa', 'name': 'Visa Support', 'description': 'Visa application and processing support'},
        {'type': 'passport', 'name': 'Passport Application', 'description': 'Passport application and renewal'},
        {'type': 'loan', 'name': 'Student Loan Services', 'description': 'Student loan application assistance'},
        {'type': 'tcu', 'name': 'TCU Services', 'description': 'Tanzania Commission for Universities services'},
        {'type': 'flight', 'name': 'Flight Ticket Booking', 'description': 'International flight ticket booking'},
    ]
    return render(request, 'student_portal/document_services.html', {'services': services})

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
    
    if request.method == 'POST':
        # Process service request
        try:
            # Extract form data based on service type
            service_data = {
                'student': request.user,
                'service_type': service_type,
                'details': json.dumps(request.POST.dict()),
                'status': 'pending'
            }
            
            # Here you would typically save to a ServiceRequest model
            # ServiceRequest.objects.create(**service_data)
            
            messages.success(request, f'{service_names[service_type]} request submitted successfully!')
            return redirect('student_portal:document_services')
            
        except Exception as e:
            messages.error(request, f'Error submitting service request: {str(e)}')
    
    return render(request, 'student_portal/service_form.html', {
        'service_type': service_type,
        'service_name': service_names[service_type]
    })

@login_required
def messages_list(request):
    messages_list = Message.objects.filter(student=request.user).order_by('-created_at')
    
    # Mark all as read when user visits messages page
    unread_messages = messages_list.filter(is_read=False)
    if unread_messages.exists():
        unread_messages.update(is_read=True)
    
    return render(request, 'student_portal/messages.html', {'messages_list': messages_list})

@login_required
def mark_message_read(request, message_id):
    if request.method == 'POST':
        try:
            message = get_object_or_404(Message, id=message_id, student=request.user)
            message.is_read = True
            message.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
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
        'transaction_id': payment.transaction_id,
        'amount': payment.amount
    })

@login_required
def delete_application(request, application_id):
    """Delete an application"""
    if request.method == 'POST':
        try:
            application = get_object_or_404(Application, id=application_id, student=request.user)
            
            # Only allow deletion if not paid
            if not application.is_paid:
                application.delete()
                messages.success(request, 'Application deleted successfully.')
            else:
                messages.error(request, 'Cannot delete paid applications.')
                
        except Exception as e:
            messages.error(request, f'Error deleting application: {str(e)}')
    
    return redirect('student_portal:applications')

@login_required
def delete_document(request, document_id):
    """Delete a document"""
    if request.method == 'POST':
        try:
            document = get_object_or_404(Document, id=document_id, student=request.user)
            document.delete()
            messages.success(request, 'Document deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting document: {str(e)}')
    
    return redirect('student_portal:documents')

@login_required
def application_statistics(request):
    """Get application statistics for dashboard"""
    applications = Application.objects.filter(student=request.user)
    
    stats = {
        'total': applications.count(),
        'submitted': applications.filter(status='submitted').count(),
        'pending_payment': applications.filter(status='pending_payment').count(),
        'under_review': applications.filter(status='under_review').count(),
        'approved': applications.filter(status='approved').count(),
        'rejected': applications.filter(status='rejected').count(),
    }
    
    return JsonResponse(stats)

# Error handling views
def handler404(request, exception):
    return render(request, 'student_portal/404.html', status=404)

def handler500(request):
    return render(request, 'student_portal/500.html', status=500)

def handler403(request, exception):
    return render(request, 'student_portal/403.html', status=403)

def handler400(request, exception):
    return render(request, 'student_portal/400.html', status=400)