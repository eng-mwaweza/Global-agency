from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('login/', views.employee_login, name='employee_login'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('logout/', views.employee_logout, name='employee_logout'),
    
    # Global agency applications
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    
    # Student portal applications
    path('student-applications/', views.student_application_list, name='student_application_list'),
    path('student-applications/<int:application_id>/', views.student_application_detail, name='student_application_detail'),
    path('student-applications/<int:application_id>/update-status/', views.update_student_application_status, name='update_student_application_status'),
    
    # Documents
    path('documents/', views.document_list, name='document_list'),
    
    # Contact messages
    path('contact-messages/', views.contact_messages, name='contact_messages'),
]