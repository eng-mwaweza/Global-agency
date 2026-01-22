from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView
from globalagency_project.sitemap import sitemaps

def get_localized_urls():
    """Generate URL patterns for all languages"""
    urlpatterns = []
    valid_languages = [code for code, _ in settings.LANGUAGES]
    
    for lang in valid_languages:
        # Add a prefix path for each language
        urlpatterns.append(
            path(f'{lang}/', include([
                path('', include(('global_agency.urls', 'global_agency'), namespace=f'global_agency_{lang}')),
                path('employee/', include(('employee.urls', 'employee'), namespace=f'employee_{lang}')),
                path('student-portal/', include(('student_portal.urls', 'student_portal'), namespace=f'student_portal_{lang}')),
            ]))
        )
    
    return urlpatterns

# Non-localized URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('setlang/', set_language, name='set_language'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Add all language-prefixed URLs
urlpatterns += get_localized_urls()

# Root redirect
urlpatterns += [
    path('', RedirectView.as_view(url='/en/', permanent=False), name='root_redirect'),
]

# Media and static files in DEBUG mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)