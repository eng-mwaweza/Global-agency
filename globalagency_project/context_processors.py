"""
Context processors for global template variables
"""
from django.conf import settings
from django.utils.translation import get_language


def language_context(request):
    """Add language-related variables to template context - ALWAYS ENGLISH"""
    return {
        'LANGUAGES': settings.LANGUAGES,
        'CURRENT_LANGUAGE': 'en',  # Always English
        'LANGUAGE_CODE': 'en',  # Always English
    }
