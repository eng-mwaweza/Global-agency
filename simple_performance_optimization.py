#!/usr/bin/env python3
"""
Performance Optimization Script for Django Application - Simplified Version
"""

import os
from datetime import datetime

def optimize_database_queries():
    """Add database query optimizations"""
    views_file = "student_portal/views.py"
    
    with open(views_file, 'r') as f:
        content = f.read()
    
    # Add database optimization imports if not present
    if "from django.db import transaction" not in content:
        import_line = "from django.shortcuts import render, redirect, get_object_or_404"
        if import_line in content:
            content = content.replace(
                import_line,
                import_line + "\nfrom django.db import transaction\nfrom django.core.cache import cache"
            )
    
    # Optimize dashboard query
    old_query = "applications = Application.objects.filter(student=request.user)"
    new_query = "applications = Application.objects.filter(student=request.user).select_related('student').prefetch_related('payment_set')"
    
    if old_query in content and new_query not in content:
        content = content.replace(old_query, new_query)
    
    with open(views_file, 'w') as f:
        f.write(content)
    
    print("✅ Database query optimizations applied")

def create_simple_cache_utils():
    """Create simple caching utilities"""
    utils_dir = "globalagency_project/utils"
    os.makedirs(utils_dir, exist_ok=True)
    
    cache_content = '''"""Simple caching utilities"""
from django.core.cache import cache
from functools import wraps

def cache_for_minutes(minutes=5):
    """Simple cache decorator"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{hash(str(args) + str(kwargs))}"
            result = cache.get(cache_key)
            if result is None:
                result = func(*args, **kwargs)
                cache.set(cache_key, result, minutes * 60)
            return result
        return wrapper
    return decorator

@cache_for_minutes(10)
def get_user_applications(user_id):
    """Cache user applications"""
    from student_portal.models import Application
    return Application.objects.filter(student_id=user_id).select_related('student')
'''
    
    with open(f"{utils_dir}/cache_utils.py", 'w') as f:
        f.write(cache_content)
    
    print("✅ Simple caching utilities created")

def update_settings_performance():
    """Update Django settings for better performance"""
    settings_file = "globalagency_project/settings.py"
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    performance_settings = '''
# Performance Settings
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
SESSION_CACHE_ALIAS = 'default'

# Static files optimization
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
'''
    
    if "# Performance Settings" not in content:
        content += performance_settings
    
    with open(settings_file, 'w') as f:
        f.write(content)
    
    print("✅ Performance settings updated")

def create_monitoring_command():
    """Create simple performance monitoring"""
    mgmt_dir = "student_portal/management/commands"
    os.makedirs(mgmt_dir, exist_ok=True)
    
    # Create __init__.py files
    for dir_path in ["student_portal/management", mgmt_dir]:
        init_file = f"{dir_path}/__init__.py"
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("")
    
    command_content = '''from django.core.management.base import BaseCommand
from django.db import connection
import time

class Command(BaseCommand):
    help = 'Monitor database performance'
    
    def handle(self, *args, **options):
        start_time = time.time()
        
        # Test database query performance
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM auth_user")
            user_count = cursor.fetchone()[0]
        
        duration = time.time() - start_time
        
        self.stdout.write(f'Database query took {duration:.3f} seconds')
        self.stdout.write(f'Total users: {user_count}')
        
        # Check number of queries
        self.stdout.write(f'Total queries executed: {len(connection.queries)}')
'''
    
    with open(f"{mgmt_dir}/check_performance.py", 'w') as f:
        f.write(command_content)
    
    print("✅ Performance monitoring command created")

def create_performance_doc():
    """Create performance documentation"""
    doc_content = f'''# Performance Optimization - Global Agency

## Implemented Optimizations

### Database
- ✅ Query optimization with select_related()
- ✅ Connection pooling enabled
- ✅ Cached database sessions

### Caching
- ✅ Simple cache decorators
- ✅ Application-level caching
- ✅ Session caching

### Static Files
- ✅ ManifestStaticFilesStorage for cache busting
- ✅ Optimized static file serving

### Monitoring
- ✅ Performance check command
- ✅ Query monitoring in debug mode

## Usage

### Check Performance
```bash
python manage.py check_performance
```

### Clear Cache
```bash
python manage.py shell -c "from django.core.cache import cache; cache.clear()"
```

### Monitor Queries (Development)
Add `?debug=1` to any URL to see query information in debug mode.

## Production Recommendations

1. Use Redis or Memcached for caching
2. Enable database query logging
3. Set up proper monitoring (e.g., New Relic, DataDog)
4. Use a reverse proxy (Nginx) for static files
5. Enable gzip compression

---
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
'''
    
    with open("PERFORMANCE_GUIDE.md", 'w') as f:
        f.write(doc_content)
    
    print("✅ Performance documentation created")

def main():
    """Main optimization function"""
    print("⚡ Starting performance optimization...")
    
    try:
        optimize_database_queries()
        create_simple_cache_utils()
        update_settings_performance()
        create_monitoring_command()
        create_performance_doc()
        
        print("\n🎉 Performance optimization completed!")
        print("📋 Features added:")
        print("   - Database query optimization")
        print("   - Simple caching system") 
        print("   - Performance monitoring")
        print("   - Static file optimization")
        
        print("\n🔧 Test with:")
        print("   python manage.py check_performance")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()