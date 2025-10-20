# employee/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from global_agency.models import ContactMessage, StudentApplication

def employee_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('employee:employee_dashboard')
        else:
            return render(request, "employee/login.html", {"error": "Invalid username or password"})
    return render(request, "employee/login.html")


@login_required

def employee_dashboard(request):
    applications = StudentApplication.objects.all().order_by('-created_at')
    contact_messages = ContactMessage.objects.all().order_by('-created_at')

    context = {
        'applications': applications,
        'contact_messages': contact_messages,
        'applications_count': applications.count(),
        'messages_count': contact_messages.count(),
        'pending_reviews': applications.filter().count(),  # can adjust later
    }
    return render(request, 'employee/dashboard.html', context)



@login_required
def employee_logout(request):
    logout(request)
    return redirect("employee:employee_login")

from django.shortcuts import render, get_object_or_404


@login_required
def application_detail(request, pk):
    application = get_object_or_404(StudentApplication, pk=pk)
    return render(request, 'employee/application_detail.html', {'application': application})

