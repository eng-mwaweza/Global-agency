# global_agency/urls.py
from django.urls import path
from . import views

app_name = 'global_agency'

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('start-application/', views.start_application, name='start_application'),
    path('vyuo-vya-ndani/', views.vyuo_ndani, name='vyuo_ndani'),
    path('university/<str:university_name>/', views.university_detail, name='university_detail'),
   # New URLs for universities
      path('universities/country/<str:country>/', views.country_universities, name='country_universities'),
    path('universities/abroad/<str:university_slug>/', views.abroad_university_detail, name='abroad_university_detail'),
    path('universities/countries/', views.all_countries, name='all_countries'),
    
     ]

