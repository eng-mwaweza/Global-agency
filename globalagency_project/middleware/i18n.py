"""
Custom middleware for language handling and internationalization
"""
import re
from django.conf import settings
from django.utils.translation import activate, get_language
from django.utils.deprecation import MiddlewareMixin


class LanguageSwitcherMiddleware(MiddlewareMixin):
    """
    Middleware to handle language switching from URL prefixes and GET parameters
    """
    
    def process_request(self, request):
        """Process language switching from URL prefix or GET parameters"""
        # Get list of valid language codes
        valid_languages = [code for code, name in settings.LANGUAGES]
        
        # First, try to extract language from URL path
        path = request.path
        language = None
        
        # Check if path starts with a language code (e.g., /en/, /sw/, /ar/, /fr/)
        for lang_code in valid_languages:
            if path.startswith(f'/{lang_code}/'):
                language = lang_code
                break
        
        # If no language in URL, check GET parameters
        if not language:
            language = request.GET.get('lang')
        
        # Validate and set language
        if language and language in valid_languages:
            # Set language in session using the correct session key
            request.session['django_language'] = language
            # Activate the language for this request
            activate(language)
        else:
            # Fallback to default language
            activate(settings.LANGUAGE_CODE)
        
        return None
    
    def process_response(self, request, response):
        """Ensure language context is properly set in response headers"""
        current_language = get_language()
        
        # Add language to response headers
        response['Content-Language'] = current_language
        
        return response


