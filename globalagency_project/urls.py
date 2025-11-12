from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('global_agency.urls')),  # include app urls
    path('employee/', include(('employee.urls', 'employee'), namespace='employee')),
    path('student-portal/', include('student_portal.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)