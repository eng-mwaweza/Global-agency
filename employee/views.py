from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from global_agency.models import ContactMessage, StudentApplication
from student_portal.models import Application, Document, Payment  # Add student portal models

def employee_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee:employee_dashboard')
        else:
            return render(request, "employee/login.html", {"error": "Invalid username or password"})
    return render(request, "employee/login.html")

@login_required
def employee_dashboard(request):
    # Get data from both global_agency and student_portal
    applications = StudentApplication.objects.all().order_by('-created_at')
    student_applications = Application.objects.all().order_by('-created_at')  # Student portal applications
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    documents = Document.objects.all().order_by('-uploaded_at')[:10]  # Recent documents

    context = {
        'applications': applications,
        'student_applications': student_applications,
        'contact_messages': contact_messages,
        'documents': documents,
        'applications_count': applications.count() + student_applications.count(),
        'messages_count': contact_messages.count(),
        'documents_count': Document.objects.count(),
        'pending_reviews': student_applications.filter(status='submitted').count(),
    }
    return render(request, 'employee/dashboard.html', context)

@login_required
def employee_logout(request):
    logout(request)
    return redirect("employee:employee_login")

@login_required
def application_detail(request, pk):
    application = get_object_or_404(StudentApplication, pk=pk)
    return render(request, 'employee/application_detail.html', {'application': application})

@login_required
def student_application_list(request):
    """View all student portal applications"""
    applications = Application.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        applications = applications.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        applications = applications.filter(
            Q(student__username__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(university_name__icontains=search_query) |
            Q(course__icontains=search_query) |
            Q(country__icontains=search_query)
        )
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'employee/student_application_list.html', context)

@login_required
def student_application_detail(request, application_id):
    """View detailed student portal application"""
    application = get_object_or_404(Application, id=application_id)
    documents = Document.objects.filter(student=application.student)
    payments = Payment.objects.filter(application=application)
    
    context = {
        'application': application,
        'documents': documents,
        'payments': payments,
    }
    return render(request, 'employee/student_application_detail.html', context)

@login_required
def update_student_application_status(request, application_id):
    """Update student portal application status"""
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in dict(Application.APPLICATION_STATUS):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('employee:student_application_detail', application_id=application_id)

@login_required
def document_list(request):
    """View all uploaded documents"""
    documents = Document.objects.all().order_by('-uploaded_at')
    
    # Filter by document type if provided
    doc_type_filter = request.GET.get('doc_type')
    if doc_type_filter:
        documents = documents.filter(document_type=doc_type_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        documents = documents.filter(
            Q(student__username__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query) |
            Q(document_type__icontains=search_query)
        )
    
    context = {
        'documents': documents,
        'doc_type_filter': doc_type_filter,
        'search_query': search_query,
    }
    return render(request, 'employee/document_list.html', context)

@login_required
def contact_messages(request):
    """View all contact messages"""
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        contact_messages = contact_messages.filter(status=status_filter)
    
    context = {
        'contact_messages': contact_messages,
        'status_filter': status_filter,
    }
    return render(request, 'employee/contact_messages.html', context)
@login_required
def contact_messages(request):
    """View all contact messages and consultations"""
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    consultations = ContactMessage.objects.all().order_by('-created_at')  # This gets all consultation forms
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        contact_messages = contact_messages.filter(status=status_filter)
        consultations = consultations.filter(status=status_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        contact_messages = contact_messages.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
        consultations = consultations.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(message__icontains=search_query) |
            Q(destination__icontains=search_query)
        )
    
    context = {
        'contact_messages': contact_messages,
        'consultations': consultations,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    return render(request, 'employee/contact_messages.html', context)

@login_required
def update_message_status(request, message_id):
    """Update contact message status"""
    message = get_object_or_404(ContactMessage, id=message_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['new', 'read', 'replied', 'archived']:
            message.status = new_status
            message.save()
            messages.success(request, f'Message status updated to {new_status.title()}')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('employee:contact_messages')