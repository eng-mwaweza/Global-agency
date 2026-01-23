from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.utils import timezone
from global_agency.models import ContactMessage, StudentApplication
from student_portal.models import Application, Document, Payment
from .models import UserProfile
from .decorators import employee_required, admin_required

@csrf_protect
def employee_login(request):
    # If user is already authenticated and can access employee portal, redirect to dashboard
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
            if profile.can_access_employee_portal():
                return redirect('employee:employee_dashboard')
            else:
                # Logout if user cannot access employee portal
                logout(request)
                messages.error(request, "Access denied. Please use the student portal.")
                return redirect('employee:employee_login')
        except UserProfile.DoesNotExist:
            pass
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user can access employee portal
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.can_access_employee_portal():
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.get_full_name()}!")
                    
                    # Redirect admins to admin dashboard if needed
                    if profile.is_admin():
                        return redirect('employee:admin_dashboard')
                    else:
                        return redirect('employee:employee_dashboard')
                else:
                    messages.error(request, "Access denied. This portal is for admin-created employees only. Students should use the student portal.")
            except UserProfile.DoesNotExist:
                messages.error(request, "Access denied. User profile not found. Please contact administrator.")
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, "employee/login.html")

@login_required
@employee_required
def employee_dashboard(request):
    # Get user profile for role-based access
    profile = UserProfile.objects.get(user=request.user)
    
    # Get data from both global_agency and student_portal
    applications = StudentApplication.objects.all().order_by('-created_at')
    student_applications = Application.objects.all().order_by('-created_at')  # ALL employees see ALL applications
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    documents = Document.objects.all().order_by('-uploaded_at')[:10]

    # REMOVED: Assignment logic - all employees see all applications

    context = {
        'profile': profile,
        'applications': applications,
        'student_applications': student_applications,
        'contact_messages': contact_messages,
        'documents': documents,
        'applications_count': applications.count() + student_applications.count(),
        'messages_count': contact_messages.count(),
        'documents_count': Document.objects.count(),
        'pending_reviews': student_applications.filter(status='submitted').count(),
        'is_admin': profile.is_admin(),
        'is_regular_employee': profile.is_regular_employee(),
    }
    return render(request, 'employee/dashboard.html', context)

@login_required
@admin_required
def admin_dashboard(request):
    """Admin-only dashboard with advanced features"""
    profile = UserProfile.objects.get(user=request.user)
    
    # Admin-specific data
    total_students = UserProfile.objects.filter(role='student').count()
    total_employees = UserProfile.objects.filter(role='employee').count()
    total_admins = UserProfile.objects.filter(role='admin').count()
    
    # Recent activity
    recent_applications = Application.objects.all().order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.all().order_by('-created_at')[:5]
    
    # Payment statistics
    total_payments = Payment.objects.filter(is_successful=True)
    total_revenue = sum(payment.amount for payment in total_payments)
    
    context = {
        'profile': profile,
        'total_students': total_students,
        'total_employees': total_employees,
        'total_admins': total_admins,
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='submitted').count(),
        'recent_applications': recent_applications,
        'recent_messages': recent_messages,
        'total_revenue': total_revenue,
        'successful_payments': total_payments.count(),
    }
    return render(request, 'employee/admin_dashboard.html', context)

@login_required
@csrf_protect
def employee_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("employee:employee_login")

@login_required
@employee_required
def application_detail(request, pk):
    application = get_object_or_404(StudentApplication, pk=pk)
    profile = UserProfile.objects.get(user=request.user)
    
    context = {
        'application': application,
        'is_admin': profile.is_admin(),
    }
    return render(request, 'employee/application_detail.html', context)

@login_required
@employee_required
def student_application_list(request):
    """View all student portal applications"""
    profile = UserProfile.objects.get(user=request.user)
    
    # ALL employees see ALL applications (removed admin/employee distinction)
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
        'is_admin': profile.is_admin(),
    }
    return render(request, 'employee/student_application_list.html', context)

@login_required
@employee_required
def student_application_detail(request, application_id):
    """View detailed student portal application"""
    profile = UserProfile.objects.get(user=request.user)
    
    # ALL employees can see ANY application
    application = get_object_or_404(Application, id=application_id)
    
    documents = Document.objects.filter(student=application.student)
    payments = Payment.objects.filter(application=application)
    
    context = {
        'application': application,
        'documents': documents,
        'payments': payments,
        'is_admin': profile.is_admin(),
    }
    return render(request, 'employee/student_application_detail.html', context)

@login_required
@employee_required
@csrf_protect
def update_student_application_status(request, application_id):
    """Update student portal application status"""
    profile = UserProfile.objects.get(user=request.user)
    
    # ALL employees can update ANY application
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status in dict(Application.APPLICATION_STATUS):
            application.status = new_status
            application.notes = notes
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
        else:
            messages.error(request, 'Invalid status selected.')
    
    return redirect('employee:student_application_detail', application_id=application_id)

@login_required
@employee_required
def document_list(request):
    """View all uploaded documents"""
    profile = UserProfile.objects.get(user=request.user)
    
    # ALL employees see ALL documents
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
        'is_admin': profile.is_admin(),
    }
    return render(request, 'employee/document_list.html', context)

@login_required
@employee_required
def contact_messages(request):
    """View all contact messages and consultations"""
    profile = UserProfile.objects.get(user=request.user)
    
    contact_messages = ContactMessage.objects.all().order_by('-created_at')
    consultations = ContactMessage.objects.all().order_by('-created_at')
    
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
        'is_admin': profile.is_admin(),
    }
    return render(request, 'employee/contact_messages.html', context)

@login_required
@employee_required
@csrf_protect
def update_message_status(request, message_id):
    """Update contact message status"""
    profile = UserProfile.objects.get(user=request.user)
    
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

@login_required
@employee_required
def user_management(request):
    """User management for admins only"""
    profile = UserProfile.objects.get(user=request.user)
    
    if not profile.is_admin():
        messages.error(request, "Access denied. Admin privileges required.")
        return redirect('employee:employee_dashboard')
    
    users = UserProfile.objects.all().order_by('-created_at')
    
    # Filter by role if provided
    role_filter = request.GET.get('role')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    context = {
        'users': users,
        'role_filter': role_filter,
        'search_query': search_query,
    }
    return render(request, 'employee/user_management.html', context)

@login_required
@admin_required
@csrf_protect
def create_employee(request):
    """Create new employee accounts (admin only)"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role', 'employee')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        try:
            # Create user
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                role=role
            )
            
            messages.success(request, f'Successfully created {role} account for {username}')
            return redirect('employee:user_management')
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
    
    return render(request, 'employee/create_employee.html')

@login_required
@employee_required
def profile_settings(request):
    """Employee profile settings"""
    profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        # Update user information
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Update profile
        profile.phone_number = request.POST.get('phone_number', '')
        profile.department = request.POST.get('department', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('employee:profile_settings')
    
    context = {
        'profile': profile,
    }
    return render(request, 'employee/profile_settings.html', context)

@login_required
@admin_required
def payment_management(request):
    """Payment management for admins"""
    payments = Payment.objects.all().order_by('-payment_date')
    
    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        if status_filter == 'successful':
            payments = payments.filter(is_successful=True)
        elif status_filter == 'failed':
            payments = payments.filter(is_successful=False)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        payments = payments.filter(
            Q(transaction_id__icontains=search_query) |
            Q(student__username__icontains=search_query) |
            Q(student__first_name__icontains=search_query) |
            Q(student__last_name__icontains=search_query)
        )
    
    total_revenue = sum(payment.amount for payment in payments.filter(is_successful=True))
    
    context = {
        'payments': payments,
        'status_filter': status_filter,
        'search_query': search_query,
        'total_revenue': total_revenue,
        'successful_count': payments.filter(is_successful=True).count(),
        'failed_count': payments.filter(is_successful=False).count(),
    }
    return render(request, 'employee/payment_management.html', context)

@login_required
@admin_required
@csrf_protect
def update_payment_status(request, payment_id):
    """Manually update payment status (admin only)"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    if request.method == 'POST':
        new_status = request.POST.get('status') == 'successful'
        payment.is_successful = new_status
        payment.save()
        
        # Update application status if payment is successful
        if new_status:
            payment.application.is_paid = True
            if payment.application.status == 'pending_payment':
                payment.application.status = 'submitted'
            payment.application.save()
        
        messages.success(request, f'Payment status updated to {"Successful" if new_status else "Failed"}')
    
    return redirect('employee:payment_management')

# API endpoints for AJAX requests
@login_required
@employee_required
def get_dashboard_stats(request):
    """Get dashboard statistics for AJAX requests"""
    profile = UserProfile.objects.get(user=request.user)
    
    stats = {
        'total_applications': Application.objects.count(),
        'pending_applications': Application.objects.filter(status='submitted').count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(status='new').count(),
        'total_documents': Document.objects.count(),
        'total_revenue': sum(payment.amount for payment in Payment.objects.filter(is_successful=True)),
    }
    
    return JsonResponse(stats)

@login_required
@employee_required
@csrf_protect
def verify_mpesa_payment(request, application_id):
    """Employee verifies M-PESA payment for an application"""
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        mpesa_reference = request.POST.get('mpesa_reference', '').strip()
        payment_notes = request.POST.get('payment_notes', '').strip()
        payment_status = request.POST.get('payment_status')
        
        if payment_status == 'paid':
            application.payment_status = 'paid'
            application.is_paid = True
            application.mpesa_reference = mpesa_reference
            application.payment_notes = payment_notes
            application.payment_verified_by = request.user
            application.payment_verification_date = timezone.now()
            
            # Update application status
            if application.status == 'pending_payment':
                application.status = 'submitted'
            
            application.save()
            messages.success(request, f'Payment verified successfully for {application.student.get_full_name()}')
        elif payment_status == 'pending_verification':
            application.payment_status = 'pending_verification'
            application.mpesa_reference = mpesa_reference
            application.payment_notes = payment_notes
            application.save()
            messages.info(request, 'Payment marked as pending verification')
        else:
            messages.error(request, 'Invalid payment status')
    
    return redirect('employee:student_application_detail', application_id=application_id)

@login_required
@employee_required
def export_application_pdf(request, application_id):
    """Export single student application to PDF"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from django.http import HttpResponse
    from io import BytesIO
    
    application = get_object_or_404(Application, id=application_id)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="application_{application.id}_{application.student.username}.pdf"'
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Add title
    title = Paragraph("AFRICA WESTERN EDUCATION COMPANY LTD", title_style)
    elements.append(title)
    elements.append(Paragraph("Student Application Report", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Application Information
    elements.append(Paragraph("Application Information", heading_style))
    
    app_data = [
        ['Application ID:', str(application.id)],
        ['Application Type:', application.get_application_type_display()],
        ['Status:', application.get_status_display()],
        ['Submission Date:', application.submission_date.strftime('%Y-%m-%d %H:%M')],
    ]
    
    if application.university_name:
        app_data.append(['University:', application.university_name])
    if application.course:
        app_data.append(['Course:', application.course])
    if application.country:
        app_data.append(['Country:', application.country])
    
    app_table = Table(app_data, colWidths=[2*inch, 4*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(app_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Information
    elements.append(Paragraph("Student Information", heading_style))
    
    student_data = [
        ['Name:', application.student.get_full_name()],
        ['Username:', application.student.username],
        ['Email:', application.student.email],
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Information
    elements.append(Paragraph("Payment Information", heading_style))
    
    payment_data = [
        ['Payment Status:', application.get_payment_status_display()],
        ['Amount:', f"TZS {application.payment_amount:,.2f}"],
        ['Paid:', 'Yes' if application.is_paid else 'No'],
    ]
    
    if application.mpesa_account_name:
        payment_data.append(['M-PESA Account Name:', application.mpesa_account_name])
    if application.payment_verified_by:
        payment_data.append(['Verified By:', application.payment_verified_by.get_full_name()])
    if application.payment_verified_at:
        payment_data.append(['Verification Date:', application.payment_verified_at.strftime('%Y-%m-%d %H:%M')])
    if application.payment_notes:
        payment_data.append(['Notes:', application.payment_notes])
    
    payment_table = Table(payment_data, colWidths=[2*inch, 4*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(payment_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

@login_required
@employee_required
def export_all_applications_pdf(request):
    """Export all student applications to a single PDF"""
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT, TA_CENTER
    from django.http import HttpResponse
    from io import BytesIO
    from django.utils import timezone as tz
    
    applications = Application.objects.all().order_by('-created_at')
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="all_applications_{tz.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Create PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    # Add title
    title = Paragraph("AFRICA WESTERN EDUCATION COMPANY LTD", title_style)
    elements.append(title)
    elements.append(Paragraph("All Student Applications Report", styles['Heading2']))
    elements.append(Paragraph(f"Generated: {tz.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary Table
    summary_data = [
        ['Total Applications:', str(applications.count())],
        ['Paid Applications:', str(applications.filter(is_paid=True).count())],
        ['Pending Payment:', str(applications.filter(payment_status='not_paid').count())],
        ['Pending Verification:', str(applications.filter(payment_status='pending_verification').count())],
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e5e7eb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Applications List Table
    elements.append(Paragraph("Applications List", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    
    # Create table data
    table_data = [['ID', 'Student', 'Type', 'Status', 'Payment', 'Date']]
    
    for app in applications:
        table_data.append([
            str(app.id),
            app.student.get_full_name()[:20],
            app.get_application_type_display()[:15],
            app.get_status_display()[:15],
            app.get_payment_status_display()[:15],
            app.created_at.strftime('%Y-%m-%d')
        ])
    
    app_list_table = Table(table_data, colWidths=[0.5*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.9*inch])
    app_list_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    elements.append(app_list_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response


@login_required
@employee_required
def verify_payment(request, application_id):
    """Verify M-PESA payment for an application"""
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            # Verify payment
            application.payment_status = 'paid'
            application.is_paid = True
            application.payment_verified_at = timezone.now()
            application.payment_verified_by = request.user
            application.save()
            
            messages.success(request, f'Payment verified successfully for {application.student.get_full_name()}')
        
        elif action == 'reject':
            # Reject payment
            rejection_reason = request.POST.get('rejection_reason', 'Payment verification failed')
            application.payment_status = 'rejected'
            application.is_paid = False
            application.payment_verified_at = timezone.now()
            application.payment_verified_by = request.user
            application.payment_notes = rejection_reason
            application.save()
            
            messages.warning(request, f'Payment rejected for {application.student.get_full_name()}. Reason: {rejection_reason}')
        
        return redirect('employee:student_application_detail', application_id=application_id)
    
    return redirect('employee:student_application_detail', application_id=application_id)


@login_required
@employee_required
def export_single_application_pdf(request, application_id):
    """Export a single application to PDF"""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from io import BytesIO
    from django.http import HttpResponse
    
    application = get_object_or_404(Application, id=application_id)
    
    # Create the HttpResponse object with PDF headers
    response = HttpResponse(content_type='application/pdf')
    filename = f'Application_{application.id}_{application.student.get_full_name().replace(" ", "_")}.pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    # Create the PDF object
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    # Title
    elements.append(Paragraph("AFRICA WESTERN EDUCATION COMPANY LTD", title_style))
    elements.append(Paragraph("Student Application Details", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Application Information
    elements.append(Paragraph("Application Information", heading_style))
    app_data = [
        ['Application ID:', str(application.id)],
        ['Application Type:', application.get_application_type_display()],
        ['Status:', application.get_status_display()],
        ['Submission Date:', application.created_at.strftime('%B %d, %Y at %I:%M %p')],
        ['Last Updated:', application.updated_at.strftime('%B %d, %Y at %I:%M %p')],
    ]
    
    app_table = Table(app_data, colWidths=[2*inch, 4*inch])
    app_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(app_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Student Information
    elements.append(Paragraph("Student Information", heading_style))
    student_data = [
        ['Full Name:', application.student.get_full_name()],
        ['Email:', application.student.email],
        ['Phone:', getattr(application.student_profile, 'phone_number', 'N/A')],
        ['Date of Birth:', str(getattr(application.student_profile, 'date_of_birth', 'N/A'))],
        ['Gender:', getattr(application.student_profile, 'gender', 'N/A')],
        ['Nationality:', getattr(application.student_profile, 'nationality', 'N/A')],
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(student_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Academic Information
    if application.application_type == 'study_abroad':
        elements.append(Paragraph("Study Abroad Details", heading_style))
        academic_data = [
            ['Preferred Country:', application.preferred_country or 'N/A'],
            ['Preferred University:', application.preferred_university or 'N/A'],
            ['Program of Interest:', application.program_of_interest or 'N/A'],
            ['Education Level:', application.education_level or 'N/A'],
        ]
    else:
        elements.append(Paragraph("Local University Details", heading_style))
        academic_data = [
            ['Preferred University:', application.preferred_university or 'N/A'],
            ['Program of Interest:', application.program_of_interest or 'N/A'],
            ['Education Level:', application.education_level or 'N/A'],
        ]
    
    academic_table = Table(academic_data, colWidths=[2*inch, 4*inch])
    academic_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(academic_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Payment Information
    elements.append(Paragraph("Payment Information", heading_style))
    payment_data = [
        ['Payment Status:', application.get_payment_status_display()],
        ['Payment Amount:', f'{application.payment_amount:,.0f} TZS' if application.payment_amount else 'N/A'],
        ['Is Paid:', 'Yes' if application.is_paid else 'No'],
    ]
    
    if application.mpesa_account_name:
        payment_data.append(['M-PESA Account Name:', application.mpesa_account_name])
    
    if application.payment_verified_at:
        payment_data.append(['Verified At:', application.payment_verified_at.strftime('%B %d, %Y at %I:%M %p')])
        if application.payment_verified_by:
            payment_data.append(['Verified By:', application.payment_verified_by.get_full_name()])
    
    payment_table = Table(payment_data, colWidths=[2*inch, 4*inch])
    payment_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e0e7ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(payment_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Documents
    documents = Document.objects.filter(application=application)
    if documents.exists():
        elements.append(Paragraph("Uploaded Documents", heading_style))
        doc_data = [['Document Type', 'Uploaded Date']]
        for doc in documents:
            doc_data.append([
                doc.get_document_type_display(),
                doc.uploaded_at.strftime('%B %d, %Y')
            ])
        
        doc_table = Table(doc_data, colWidths=[3*inch, 3*inch])
        doc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(doc_table)
    
    # Footer
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(f"Generated on {timezone.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
    elements.append(Paragraph("AFRICA WESTERN EDUCATION COMPANY LTD - Confidential", footer_style))
    
    # Build PDF
    doc.build(elements)
    
    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response