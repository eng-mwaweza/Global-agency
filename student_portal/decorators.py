from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from functools import wraps
from employee.models import UserProfile

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('student:student_login')
        
        try:
            profile = UserProfile.objects.get(user=request.user)
            if not profile.can_access_student_portal():
                return HttpResponseForbidden("Access denied. Self-registered student account required. Please use the employee portal for employee access.")
        except UserProfile.DoesNotExist:
            return HttpResponseForbidden("Access denied. User profile not found. Please contact administrator.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view