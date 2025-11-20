from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Application(models.Model):
    APPLICATION_STATUS = [
        ('pending_payment', 'Pending Payment'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected'),
    ]
    
    APPLICATION_TYPES = [
        ('university', 'University Application'),
        ('visa', 'Visa Application'),
        ('scholarship', 'Scholarship'),
        ('loan', 'Student Loan'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    application_type = models.CharField(max_length=20, choices=APPLICATION_TYPES)
    university_name = models.CharField(max_length=255, blank=True)
    course = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='pending_payment')
    submission_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=5000.00)

    def __str__(self):
        return f"{self.get_application_type_display()} - {self.student.username}"

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('passport', 'Passport'),
        ('academic_transcript', 'Academic Transcript'),
        ('degree_certificate', 'Degree Certificate'),
        ('recommendation_letter', 'Recommendation Letter'),
        ('sop', 'Statement of Purpose'),
        ('cv', 'CV'),
        ('language_test', 'Language Test Results'),
        ('financial_documents', 'Financial Documents'),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_document_type_display()} - {self.student.username}"

class Message(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} - {self.student.username}"

# ADD THIS PAYMENT MODEL
class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='mobile_money')
    transaction_id = models.CharField(max_length=100, blank=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.id} - {self.student.username}"

# ADD THIS APPLICATION ASSIGNMENT MODEL
class ApplicationAssignment(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='assignments')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_applications')
    assigned_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['application', 'employee']
        verbose_name = 'Application Assignment'
        verbose_name_plural = 'Application Assignments'
        ordering = ['-assigned_date']
    
    def __str__(self):
        return f"{self.employee.username} - Application #{self.application.id} ({self.application.student.username})"