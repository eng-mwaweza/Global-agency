"""
Context processors for global template variables
"""
from django.conf import settings
from django.utils.translation import get_language


def language_context(request):
    """Add language-related variables to template context"""
    return {
        'LANGUAGES': settings.LANGUAGES,
        'CURRENT_LANGUAGE': get_language(),
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
    }
