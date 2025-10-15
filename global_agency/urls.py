# global_agency/urls.py
from django.urls import path
from . import views

app_name = 'global_agency'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('start-application/', views.start_application, name='start_application'),
]

