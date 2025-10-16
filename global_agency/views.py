# global_agency/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentApplicationForm
from .forms import ContactMessageForm

def home(request):
    return render(request, 'global_agency/index.html')


def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you! Your consultation request has been sent successfully.")
            return redirect('global_agency:contact')  # reload the same page
        else:
            messages.error(request, "⚠️ Please correct the errors and try again.")
    else:
        form = ContactMessageForm()

    return render(request, 'global_agency/includes/contact.html', {'form': form})




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


