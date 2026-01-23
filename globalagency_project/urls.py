from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import set_language
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from globalagency_project.sitemap import sitemaps

# Non-localized URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('setlang/', set_language, name='set_language'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    # Direct app URLs (no language prefix by default - uses LANGUAGE_CODE='en')
    path('', include(('global_agency.urls', 'global_agency'))),
    path('employee/', include(('employee.urls', 'employee'))),
    path('student-portal/', include(('student_portal.urls', 'student_portal'))),
]

# Media and static files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)