from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import StudentProfile, Application, Document, Message, Payment  # Added Payment import
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
            application.status = 'pending_payment'  # Changed to pending payment
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
        # Simulate payment processing
        payment = Payment.objects.create(
            student=request.user,
            application=application,
            amount=application.payment_amount,
            payment_method=request.POST.get('payment_method', 'mobile_money'),
            transaction_id=f"TXN{application.id}{request.user.id}",
            is_successful=True
        )
        
        # Update application status
        application.is_paid = True
        application.status = 'submitted'
        application.save()
        
        messages.success(request, 'Payment successful! Your application has been submitted.')
        return redirect('student_portal:applications')
    
    return render(request, 'student_portal/payment.html', {
        'application': application,
        'payment_amount': application.payment_amount
    })

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