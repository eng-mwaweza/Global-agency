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
        """Process language switching - ALWAYS USE ENGLISH"""
        # CRITICAL: Always use English as the default language
        # Do not check URL prefixes, GET params, or browser language
        language = settings.LANGUAGE_CODE  # Always 'en'
        
        # Set language in session
        request.session['django_language'] = language
        
        # Activate English for this request
        activate(language)
        
        return None
    
    def process_response(self, request, response):
        """Ensure language context is properly set in response headers"""
        current_language = get_language()
        
        # Add language to response headers
        response['Content-Language'] = current_language
        
        return response


