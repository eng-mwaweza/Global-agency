# global_agency/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StudentApplicationForm, ContactMessageForm
import json
import os
from django.core.paginator import Paginator
from pathlib import Path

def home(request):
    return render(request, 'global_agency/index.html')

def contact(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Thank you! Your consultation request has been sent successfully.")
            return redirect('global_agency:contact')
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
            return redirect('global_agency:start_application')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = StudentApplicationForm()

    return render(request, 'global_agency/start_application.html', {'form': form})

def load_universities_data():
    """Load universities data from JSON file"""
    BASE_DIR = Path(__file__).resolve().parent.parent
    json_path = os.path.join(BASE_DIR, 'static', 'global_agency', 'data', 'universities.json')
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"Error loading universities data: {e}")
        return {
            'admission_guidebook': {
                'higher_education_institutions': [],
                'minimum_entry_requirements': {'general_programs': []},
                'general_information': {'important_dates': {}}
            }
        }

def vyuo_ndani(request):
    """
    Render the Vyuo Vya Ndani page with server-side data and pagination
    """
    data = load_universities_data()
    universities = data['admission_guidebook']['higher_education_institutions']

    # Server-side filtering
    query = request.GET.get('query', '').strip().lower()
    location_filter = request.GET.get('location', '').strip().lower()
    program_filter = request.GET.get('program', '').strip().lower()
    
    filtered_universities = universities
    
    if query:
        filtered_universities = [
            u for u in filtered_universities
            if query in u.get('name', '').lower()
        ]
    
    if location_filter:
        filtered_universities = [
            u for u in filtered_universities
            if location_filter in u.get('location', '').lower()
        ]
    
    if program_filter:
        filtered_universities = [
            u for u in filtered_universities
            if any(program_filter in p.get('name', '').lower() for p in u.get('programs', []))
        ]

    # Pagination
    page_number = request.GET.get('page', 1)
    paginator = Paginator(filtered_universities, 12)  # Show 12 universities per page
    page_obj = paginator.get_page(page_number)

    # Get unique locations for filter dropdown
    locations = sorted(list(set(u.get('location', '') for u in universities if u.get('location'))))

    context = {
        'universities': list(page_obj),
        'page_obj': page_obj,
        'locations': locations,
        'current_query': query,
        'current_location': location_filter,
        'current_program': program_filter,
    }
    
    return render(request, 'global_agency/vyuo_ndani.html', context)

def university_detail(request, university_name):
    """
    Render detailed view for a specific university
    """
    data = load_universities_data()
    universities = data['admission_guidebook']['higher_education_institutions']
    
    # Find the specific university by name
    university = None
    for uni in universities:
        if uni['name'] == university_name:
            university = uni
            break
    
    if not university:
        # University not found
        return render(request, 'global_agency/university_not_found.html', {
            'university_name': university_name
        })
    
    context = {
        'university': university,
        'admission_guidebook': data['admission_guidebook']
    }
    
    return render(request, 'global_agency/university_detail.html', context)