"""
Custom middleware for language handling and internationalization
"""
from django.conf import settings
from django.utils.translation import activate, get_language
from django.utils.deprecation import MiddlewareMixin


class LanguageSwitcherMiddleware(MiddlewareMixin):
    """
    Middleware to handle language switching via GET parameters and session
    """
    
    def process_request(self, request):
        """Process language switching from query parameters"""
        # Check if language is in GET parameters
        language = request.GET.get('lang')
        
        # Validate language code
        valid_languages = [code for code, name in settings.LANGUAGES]
        
        if language and language in valid_languages:
            # Set language in session
            request.session[settings.LANGUAGE_SESSION_KEY] = language
            activate(language)
        
        return None
    
    def process_response(self, request, response):
        """Ensure language context is properly set"""
        current_language = get_language()
        
        # Add language to response headers for debugging (optional)
        response['Content-Language'] = current_language
        
        return response
