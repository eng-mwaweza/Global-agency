from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    path('login/', views.employee_login, name='employee_login'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('logout/', views.employee_logout, name='employee_logout'),
    path('application/<int:pk>/', views.application_detail, name='application_detail'),

]
