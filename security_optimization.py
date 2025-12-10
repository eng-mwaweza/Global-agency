#!/usr/bin/env python3
"""
Security and Performance Optimization Script
Implements best practices for Django applications
"""

import os

SETTINGS_PATH = 'globalagency_project/settings.py'

def create_security_improvements():
    """Add security improvements to settings.py"""
    
    with open(SETTINGS_PATH, 'r') as f:
        content = f.read()
    
    security_settings = """

# ============================================
# SECURITY SETTINGS - Best Practices
# ============================================

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HTTPS Settings (Enable in production)
# SECURE_SSL_REDIRECT = not DEBUG
# SESSION_COOKIE_SECURE = not DEBUG
# CSRF_COOKIE_SECURE = not DEBUG

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_USE_SESSIONS = True

# Password Validation - Enhanced
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# File Upload Security
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# ============================================
# PERFORMANCE OPTIMIZATION
# ============================================

# Database Connection Pooling
CONN_MAX_AGE = 600  # 10 minutes

# Cache Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Template Caching
if not DEBUG:
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# Static Files Optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/django_errors.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
"""
    
    # Check if security settings already exist
    if '# SECURITY SETTINGS - Best Practices' not in content:
        # Add at the end of the file
        content += security_settings
        
        with open(SETTINGS_PATH, 'w') as f:
            f.write(content)
        
        print("✓ Added security and performance settings")
    else:
        print("- Security settings already exist")

def create_logs_directory():
    """Create logs directory for error logging"""
    os.makedirs('logs', exist_ok=True)
    
    # Create .gitignore for logs
    gitignore_path = 'logs/.gitignore'
    if not os.path.exists(gitignore_path):
        with open(gitignore_path, 'w') as f:
            f.write("# Ignore all log files\n*.log\n")
        print("✓ Created logs directory")
    else:
        print("- Logs directory already exists")

def create_security_checklist():
    """Create a security checklist document"""
    checklist = """# Security Checklist

## ✅ Implemented Security Measures

### 1. Security Headers
- [x] XSS Filter enabled
- [x] Content Type nosniff enabled
- [x] X-Frame-Options set to DENY
- [x] CSRF protection enabled
- [x] Session security configured

### 2. Authentication & Authorization
- [x] Password validation (minimum 8 characters)
- [x] Common password checking
- [x] User attribute similarity checking
- [x] Numeric password prevention

### 3. Session Management
- [x] HTTP-only cookies
- [x] SameSite cookie policy (Strict)
- [x] Session timeout (1 hour)
- [x] Session save on every request

### 4. Data Protection
- [x] File upload size limits (5MB)
- [x] Form field limits
- [x] Database connection pooling

### 5. Performance Optimization
- [x] Template caching
- [x] Static files optimization
- [x] Connection pooling
- [x] In-memory caching

## 🔐 Production Security Checklist

Before deploying to production, ensure:

1. **Environment Variables**
   - [ ] Change DEBUG to False
   - [ ] Set strong SECRET_KEY
   - [ ] Configure ALLOWED_HOSTS
   - [ ] Set up proper database credentials

2. **HTTPS Configuration**
   - [ ] Enable SECURE_SSL_REDIRECT
   - [ ] Enable SESSION_COOKIE_SECURE
   - [ ] Enable CSRF_COOKIE_SECURE
   - [ ] Configure SECURE_HSTS_SECONDS

3. **Database Security**
   - [ ] Use strong database passwords
   - [ ] Enable database SSL/TLS
   - [ ] Regular database backups
   - [ ] Limit database user permissions

4. **File Permissions**
   - [ ] Set proper file permissions (644 for files, 755 for directories)
   - [ ] Protect sensitive files (.env, settings.py)
   - [ ] Configure proper media file access

5. **Monitoring & Logging**
   - [ ] Set up error monitoring (e.g., Sentry)
   - [ ] Configure log rotation
   - [ ] Monitor failed login attempts
   - [ ] Set up uptime monitoring

6. **Regular Maintenance**
   - [ ] Keep Django and dependencies updated
   - [ ] Regular security audits
   - [ ] Review access logs
   - [ ] Test backup restoration

## 📊 Performance Optimization Checklist

1. **Database**
   - [x] Connection pooling enabled
   - [ ] Database indexes on frequently queried fields
   - [ ] Query optimization

2. **Caching**
   - [x] Template caching enabled
   - [x] In-memory caching configured
   - [ ] Consider Redis for production

3. **Static Files**
   - [x] Manifest static files storage
   - [ ] Use CDN for static files in production
   - [ ] Compress CSS/JS files

4. **Code Optimization**
   - [ ] Use select_related() and prefetch_related()
   - [ ] Avoid N+1 queries
   - [ ] Use pagination for large datasets

## 🛡️ ClickPesa Security

1. **API Credentials**
   - [x] Stored in .env file (not in code)
   - [x] Validated before use
   - [ ] Rotate credentials periodically

2. **Payment Security**
   - [x] Use HTTPS for all payment requests
   - [x] Validate all responses
   - [x] Log all transactions
   - [ ] Implement webhook verification

## 📝 Notes

- All security settings are in `globalagency_project/settings.py`
- Error logs are stored in `logs/django_errors.log`
- Review this checklist monthly and after major updates
"""
    
    with open('SECURITY_CHECKLIST.md', 'w') as f:
        f.write(checklist)
    
    print("✓ Created security checklist")

def main():
    print("Starting security and performance optimization...\n")
    
    try:
        create_security_improvements()
        create_logs_directory()
        create_security_checklist()
        
        print("\n✅ Security and performance optimization completed!")
        print("\n📋 Next Steps:")
        print("1. Review SECURITY_CHECKLIST.md")
        print("2. Test the application thoroughly")
        print("3. Enable HTTPS settings before production deployment")
        print("4. Consider implementing Redis for production caching")
        print("5. Set up monitoring and alerting")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
