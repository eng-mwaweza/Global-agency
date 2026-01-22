import os
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='final')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ["*"]

# ADD THESE AUTHENTICATION SETTINGS
LOGIN_URL = '/employee/login/'
LOGIN_REDIRECT_URL = '/employee/dashboard/'
LOGOUT_REDIRECT_URL = '/employee/login/'

# ClickPesa API Configuration
CLICKPESA_CLIENT_ID = config('CLICKPESA_CLIENT_ID', default='')
CLICKPESA_API_KEY = config('CLICKPESA_API_KEY', default='')
CLICKPESA_BASE_URL = config('CLICKPESA_BASE_URL', default='https://api.clickpesa.com/third-parties')
CLICKPESA_CHECKSUM = config('CLICKPESA_CHECKSUM', default='')

# Payment Gateway Selection
PAYMENT_GATEWAY = config('PAYMENT_GATEWAY', default='clickpesa')  # 'clickpesa' or 'azampay'
CURRENCY = config('CURRENCY', default='TZS')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # Added for SEO sitemap generation
    'crispy_forms',
    'global_agency',
    'employee',
     'student_portal',  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Added Whitenoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Added for i18n
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'globalagency_project.middleware.i18n.LanguageSwitcherMiddleware',  # Custom language switcher
]

ROOT_URLCONF = 'globalagency_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'globalagency_project.context_processors.language_context',  # Add language variables to templates
            ],
        },
    },
]

WSGI_APPLICATION = 'globalagency_project.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DB_NAME'),  # Database name from .env
        'USER': config('DB_USER'),  # Database username from .env
        'PASSWORD': config('DB_PASSWORD'),  # Database password from .env
        'HOST': config('DB_HOST', default='localhost'),  # Database host from .env
        'PORT': config('DB_PORT', default='3306'),  # Database port from .env
        'OPTIONS': {
            'charset': 'utf8mb4',  # Use utf8mb4 for full UTF-8 support including emojis
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1, NAMES utf8mb4 COLLATE utf8mb4_unicode_ci",
            'use_unicode': True,
        },
        'TEST': {
            'CHARSET': 'utf8mb4',
            'COLLATION': 'utf8mb4_unicode_ci',
        }
    }
}


LANGUAGE_CODE = 'en'
TIME_ZONE = 'Africa/Dar_es_Salaam'

# Internationalization settings
USE_I18N = True
USE_L10N = True

# Supported languages
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('en', _('English')),
    ('sw', _('Swahili')),
    ('ar', _('Arabic')),
    ('fr', _('French')),
]

# Locale paths for translation files
LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files configuration
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Added for production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'  # Added for Whitenoise

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
# AUTH_USER_MODEL = 'global_agency.StudentUser'

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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

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

# =============================================================================
# SECURITY SETTINGS - Production Ready
# =============================================================================

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# HTTPS Settings (Enable in production)
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_HSTS_SECONDS = 31536000  # 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Session Security
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_SAVE_EVERY_REQUEST = True

# CSRF Protection
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
CSRF_USE_SESSIONS = True

# Password Validation (Enhanced)
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
FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Allowed File Extensions
ALLOWED_UPLOAD_EXTENSIONS = [
    '.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.gif', '.txt'
]

# Content Security Policy Headers (Add django-csp if needed)
# CSP_DEFAULT_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "cdn.tailwindcss.com", "cdnjs.cloudflare.com")
# CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "fonts.googleapis.com", "cdnjs.cloudflare.com")
# CSP_FONT_SRC = ("'self'", "fonts.gstatic.com", "cdnjs.cloudflare.com")
# CSP_IMG_SRC = ("'self'", "data:")

# Rate Limiting (Add django-ratelimit if needed)
# RATELIMIT_ENABLE = True
# RATELIMIT_VIEW = 'django_ratelimit.decorators.ratelimit'

# Admin Security
ADMIN_URL = 'secure-admin-panel/'  # Change default admin URL
ADMIN_ENABLED = True

# Database Security
CONN_MAX_AGE = 600  # Connection pooling - 10 minutes
CONN_HEALTH_CHECKS = True

# =============================================================================
# PERFORMANCE OPTIMIZATION SETTINGS
# =============================================================================

# Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'global-agency-cache',
        'TIMEOUT': 300,  # 5 minutes
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 3,
        }
    }
}

# Template Caching
# Only set the cached loader when not in DEBUG. When using custom loaders,
# APP_DIRS must not be True. We keep APP_DIRS=True in DEBUG for easier dev,
# and enable cached loader in production by setting APP_DIRS to False and
# providing the cached loader. This avoids the "app_dirs must not be set when
# loaders is defined" ImproperlyConfigured error.
if not DEBUG:
    # Disable APP_DIRS when providing explicit loaders
    TEMPLATES[0]['APP_DIRS'] = False
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# Static Files Optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Compression (Add django-compressor if needed)
# COMPRESS_ENABLED = True
# COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
# COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']

# Database Optimization
DATABASES['default'].update({
    'CONN_MAX_AGE': CONN_MAX_AGE,
    'CONN_HEALTH_CHECKS': CONN_HEALTH_CHECKS,
    'OPTIONS': {
        'timeout': 20,
        'check_same_thread': False,
    } if 'sqlite' in DATABASES['default']['ENGINE'] else {}
})

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'student_portal': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
        'global_agency': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# =============================================================================
# CUSTOM SECURITY MIDDLEWARE
# =============================================================================

# Note: The main MIDDLEWARE list is defined earlier in this file with all necessary middleware
# including LocaleMiddleware for i18n. Do not override it here.
# The MIDDLEWARE variable is already properly configured with all required middleware.

# Performance Settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Static files optimization
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# =============================================================================
# PERFORMANCE OPTIMIZATION SETTINGS
# =============================================================================

# Database query optimization
DATABASES['default']['CONN_MAX_AGE'] = 600  # Connection pooling

# Only add MySQL-specific options if using MySQL
if DATABASES['default']['ENGINE'] == 'django.db.backends.mysql':
    DATABASES['default']['OPTIONS']['init_command'] = "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1, NAMES utf8mb4"

# Query optimization
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Template optimization
if not DEBUG:
    TEMPLATES[0]['APP_DIRS'] = False
    TEMPLATES[0]['OPTIONS']['loaders'] = [
        ('django.template.loaders.cached.Loader', [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ]),
    ]

# Cache Framework Configuration - For production use Redis
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'africa-western-education',
        'OPTIONS': {
            'MAX_ENTRIES': 10000,
            'CULL_FREQUENCY': 4,
        },
        'TIMEOUT': 300,  # 5 minutes
        'KEY_PREFIX': 'aweducol',
        'VERSION': 1,
    }
}

# Session cache settings
SESSION_CACHE_ALIAS = 'default'

# Middleware optimization
MIDDLEWARE.insert(3, 'django.middleware.gzip.GZipMiddleware')
MIDDLEWARE.insert(4, 'django.middleware.http.ConditionalGetMiddleware')

# Static files gzip compression
WHITENOISE_COMPRESS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_ADD_HEADERS_BEFORE = True

# Image optimization
WHITENOISE_MANIFEST_STRICT = False

# =============================================================================
# SEO & ACCESSIBILITY OPTIMIZATION
# =============================================================================

# Enable gzip compression
GZIP_LEVEL = 9

# HTTP caching headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'SAMEORIGIN'

# HSTS settings (Enable in production)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# CSP Headers
CSP_DEFAULT_SRC = ("'self'", "https:", "data:", "blob:")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https:", "cdn.tailwindcss.com", "unpkg.com")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https:", "fonts.googleapis.com", "cdn.tailwindcss.com")
CSP_IMG_SRC = ("'self'", "https:", "data:", "blob:")
CSP_FONT_SRC = ("'self'", "https:", "fonts.gstatic.com", "cdnjs.cloudflare.com")

# SEO Meta Settings
ROBOTS_USE_HOST = False
ROBOTS_USE_HTTPS = not DEBUG
ROBOTS_RULES = [
    {'useragent': '*', 'allow': '/'},
    {'useragent': '*', 'disallow': '/admin'},
    {'useragent': '*', 'disallow': '/employee'},
]

# =============================================================================
# INTERNATIONALIZATION & LOCALIZATION
# =============================================================================

# Use i18n
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Internationalization middleware is already in place
# Locale paths already configured above

# =============================================================================
# PRODUCTION-READY SETTINGS
# =============================================================================

# Allowed hosts - configure for production
if not DEBUG:
    ALLOWED_HOSTS = [
        'africawesterneducation.com',
        'www.africawesterneducation.com',
        'api.africawesterneducation.com',
    ]

# CSRF and Security
CSRF_TRUSTED_ORIGINS = []
if not DEBUG:
    CSRF_TRUSTED_ORIGINS = [
        'https://africawesterneducation.com',
        'https://www.africawesterneducation.com',
    ]

# Secure cookies
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = False

CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SAMESITE = 'Lax'

# Password validation with stricter requirements
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# File upload security
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644

# Logging optimization
LOGGING_CONFIG = None

# =============================================================================
# ADVANCED CACHING & CDN SETTINGS
# =============================================================================

# Cache individual views
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600  # 10 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'aweducol'

# API Response caching
DEFAULT_CACHE_TIMEOUT = 300

# =============================================================================
# PERFORMANCE MONITORING
# =============================================================================

# Enable SQL logging in development only
if DEBUG:
    LOGGING['loggers']['django.db.backends'] = {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    }

# =============================================================================
# SITEMAP & ROBOTS CONFIGURATION
# =============================================================================

# Sitemap settings
SITEMAP_CHANGEFREQ_DEFAULT = 'weekly'
SITEMAP_PRIORITY_DEFAULT = 0.5

# Google Search Console verification
GOOGLE_SITE_VERIFICATION = config('GOOGLE_SITE_VERIFICATION', default='')
BING_SITE_VERIFICATION = config('BING_SITE_VERIFICATION', default='')

# =============================================================================
# ANALYTICS & MONITORING
# =============================================================================

# Google Analytics
GA4_MEASUREMENT_ID = config('GA4_MEASUREMENT_ID', default='')

# Sentry error tracking (optional)
SENTRY_DSN = config('SENTRY_DSN', default='')

if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.1,
        send_default_pii=False
    )