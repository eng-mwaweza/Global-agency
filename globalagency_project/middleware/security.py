"""
Custom Security Middleware for Global Agency Application
"""
import logging
import time
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger('django.security')

class SecurityHeadersMiddleware:
    """Add additional security headers"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Remove server information
        if 'Server' in response:
            del response['Server']
            
        return response

class RateLimitMiddleware:
    """Simple rate limiting middleware"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Get client IP
        ip = self.get_client_ip(request)
        
        # Rate limiting for login attempts
        if request.path.startswith('/student-portal/login/') and request.method == 'POST':
            key = f'login_attempts_{ip}'
            attempts = cache.get(key, 0)
            
            if attempts >= 5:  # Max 5 attempts per hour
                logger.warning(f'Rate limit exceeded for IP {ip} on login')
                return HttpResponseForbidden('Too many login attempts. Please try again later.')
            
            cache.set(key, attempts + 1, 3600)  # 1 hour timeout
        
        # Rate limiting for payment attempts
        if '/payment/' in request.path and request.method == 'POST':
            key = f'payment_attempts_{ip}'
            attempts = cache.get(key, 0)
            
            if attempts >= 10:  # Max 10 payment attempts per hour
                logger.warning(f'Rate limit exceeded for IP {ip} on payment')
                return HttpResponseForbidden('Too many payment attempts. Please try again later.')
            
            cache.set(key, attempts + 1, 3600)  # 1 hour timeout
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class SecurityLoggingMiddleware:
    """Log security-related events"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        
        # Log suspicious requests
        self.log_suspicious_requests(request)
        
        response = self.get_response(request)
        
        # Log slow requests (potential DoS)
        duration = time.time() - start_time
        if duration > 5:  # Requests taking more than 5 seconds
            logger.warning(f'Slow request: {request.path} took {duration:.2f} seconds')
        
        return response
    
    def log_suspicious_requests(self, request):
        """Log potentially suspicious requests"""
        # Log requests with suspicious patterns
        suspicious_patterns = [
            'admin', 'wp-admin', 'phpmyadmin', '.php', '.asp', '.jsp',
            'eval(', 'script>', 'javascript:', 'vbscript:', 'onload=',
            '<script', 'SELECT * FROM', 'UNION SELECT', 'DROP TABLE'
        ]
        
        path = request.path.lower()
        query_string = request.META.get('QUERY_STRING', '').lower()
        
        for pattern in suspicious_patterns:
            if pattern in path or pattern in query_string:
                ip = self.get_client_ip(request)
                logger.warning(f'Suspicious request from {ip}: {request.path}?{request.META.get("QUERY_STRING", "")}')
                break
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
