"""Simple caching utilities"""
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
