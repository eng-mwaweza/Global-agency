# global_agency/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentApplicationForm

def home(request):
    return render(request, 'global_agency/index.html')

def contact(request):
    return render(request, 'global_agency/includes/contact.html', )


def start_application(request):
    if request.method == 'POST':
        form = StudentApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🎉 Application submitted successfully! We will contact you soon.")
            # Redirect back to the same page (or change to a 'thank-you' view)
            return redirect('global_agency:start_application')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = StudentApplicationForm()

    return render(request, 'global_agency/start_application.html', {'form': form})


