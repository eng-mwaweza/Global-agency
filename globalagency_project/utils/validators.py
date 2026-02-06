"""
Input validation utilities for security
"""
import re
import html
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class InputValidator:
    """Comprehensive input validation class"""
    
    @staticmethod
    def sanitize_input(value):
        """Sanitize user input to prevent XSS"""
        if isinstance(value, str):
            # HTML escape
            value = html.escape(value)
            # Remove potentially dangerous patterns
            dangerous_patterns = [
                r'javascript:',
                r'vbscript:',
                r'onload\s*=',
                r'onerror\s*=',
                r'<script',
                r'</script>',
                r'<iframe',
                r'<object',
                r'<embed',
            ]
            
            for pattern in dangerous_patterns:
                value = re.sub(pattern, '', value, flags=re.IGNORECASE)
        
        return value
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate phone number format"""
        if not phone:
            raise ValidationError(_('Phone number is required'))
        
        # Remove spaces and common characters
        phone = re.sub(r'[^\d+]', '', str(phone))
        
        # Check for valid Tanzania phone number
        if re.match(r'^(\+255|255|0)[67]\d{8}$', phone):
            return phone
        
        raise ValidationError(_('Invalid phone number format'))
    
    @staticmethod
    def validate_file_upload(file):
        """Validate uploaded file for security"""
        if not file:
            return True
        
        # Check file size (5MB limit)
        if file.size > 5 * 1024 * 1024:
            raise ValidationError(_('File size must be less than 5MB'))
        
        # Check file extension
        allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.txt']
        file_extension = '.' + file.name.split('.')[-1].lower() if '.' in file.name else ''
        
        if file_extension not in allowed_extensions:
            raise ValidationError(_('File type not allowed'))
        
        # Check for suspicious file names
        suspicious_patterns = ['../', '.htaccess', '.php', '.asp', '.jsp', '.exe', '.bat']
        for pattern in suspicious_patterns:
            if pattern in file.name.lower():
                raise ValidationError(_('Suspicious file name detected'))
        
        return True
    
    @staticmethod
    def validate_sql_injection(value):
        """Check for SQL injection patterns"""
        if isinstance(value, str):
            sql_patterns = [
                r"('|(\')|(\-\-)|(%27)|(%2D%2D))",
                r"union.*select",
                r"select.*from",
                r"drop\s+table",
                r"insert\s+into",
                r"delete\s+from",
                r"update.*set",
                r"exec\s*\(",
            ]
            
            for pattern in sql_patterns:
                if re.search(pattern, value, re.IGNORECASE):
                    raise ValidationError(_('Invalid input detected'))
        
        return value

def sanitize_dict(data):
    """Sanitize all string values in a dictionary"""
    validator = InputValidator()
    if isinstance(data, dict):
        return {key: validator.sanitize_input(value) for key, value in data.items()}
    return data
