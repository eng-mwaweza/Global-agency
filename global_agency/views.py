from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
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
            # Save the application
            application = form.save()
            
            # Create student account
            student_user = application.create_student_account()
            
            if student_user:
                # Success message with login details
                success_message = (
                    f"✅ Application submitted successfully! "
                    f"Your student account has been created. "
                    f"<br><br>"
                    f"<strong>Login Details:</strong><br>"
                    f"Username: <code>{application.username}</code><br>"
                    f"Password: <code>{application.temporary_password}</code>"
                    f"<br><br>"
                    f"Please go to the <a href='/student-portal/' class='font-semibold text-blue-600 hover:text-blue-800'>Student Portal</a> to login and track your application."
                )
                messages.success(request, success_message)
                return redirect('global_agency:application_success')
            else:
                messages.warning(request, "Application submitted, but there was an issue creating your student account. Please contact support.")
                return redirect('global_agency:application_success')
        else:
            messages.error(request, "⚠️ Please correct the errors below.")
    else:
        form = StudentApplicationForm()

    return render(request, 'global_agency/start_application.html', {'form': form})

def application_success(request):
    """Display success page after application submission"""
    return render(request, 'global_agency/application_success.html')

# ... KEEP ALL YOUR EXISTING VIEWS BELOW EXACTLY AS THEY ARE ...
# [All your existing views for universities, countries, TCU services remain unchanged]

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
    Render detailed view for a specific LOCAL university (Tanzanian)
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

def country_universities(request, country):
    """
    Render universities for a specific country (Abroad universities)
    """
    # Expanded countries data with more universities
    countries_data = {
        'usa': {
            'name': 'United States',
            'flag': '🇺🇸',
            'universities': [
                {'name': 'Harvard University', 'slug': 'harvard'},
                {'name': 'Stanford University', 'slug': 'stanford'},
                {'name': 'MIT', 'slug': 'mit'},
                {'name': 'California Institute of Technology', 'slug': 'caltech'},
                {'name': 'University of Chicago', 'slug': 'chicago'},
                {'name': 'Princeton University', 'slug': 'princeton'},
                {'name': 'Yale University', 'slug': 'yale'},
                {'name': 'Columbia University', 'slug': 'columbia'},
            ]
        },
        'uk': {
            'name': 'United Kingdom',
            'flag': '🇬🇧',
            'universities': [
                {'name': 'University of Oxford', 'slug': 'oxford'},
                {'name': 'University of Cambridge', 'slug': 'cambridge'},
                {'name': 'Imperial College London', 'slug': 'imperial'},
                {'name': 'London School of Economics', 'slug': 'lse'},
                {'name': 'University College London', 'slug': 'ucl'},
                {'name': 'University of Edinburgh', 'slug': 'edinburgh'},
            ]
        },
        'canada': {
            'name': 'Canada',
            'flag': '🇨🇦',
            'universities': [
                {'name': 'University of Toronto', 'slug': 'toronto'},
                {'name': 'University of British Columbia', 'slug': 'ubc'},
                {'name': 'McGill University', 'slug': 'mcgill'},
                {'name': 'University of Alberta', 'slug': 'alberta'},
                {'name': 'McMaster University', 'slug': 'mcmaster'},
            ]
        },
        # ... [rest of your existing country data remains the same]
    }
    
    country_data = countries_data.get(country.lower())
    if not country_data:
        # Handle invalid country - redirect to all countries page
        return redirect('global_agency:all_countries')
    
    context = {
        'country': country_data,
        'country_code': country.lower()
    }
    return render(request, 'global_agency/country_universities.html', context)

def abroad_university_detail(request, university_slug):
    """
    Render detailed view for a specific ABROAD university
    """
    # COMPREHENSIVE university data for ALL countries
    universities = {
        # ... [your existing university data remains exactly the same]
    }
    
    university = universities.get(university_slug)
    if not university:
        # University not found - redirect to all countries
        return redirect('global_agency:all_countries')
    
    context = {'university': university}
    return render(request, 'global_agency/abroad_university_detail.html', context)
   
def all_countries(request):
    """
    Render the page showing all available countries for study abroad
    """
    countries = [
        {'code': 'usa', 'name': 'United States', 'flag': '🇺🇸', 'description': 'World-class universities with diverse programs'},
        {'code': 'uk', 'name': 'United Kingdom', 'flag': '🇬🇧', 'description': 'Historic universities with 3-year bachelor degrees'},
        {'code': 'canada', 'name': 'Canada', 'flag': '🇨🇦', 'description': 'High-quality education with post-study work opportunities'},
        # ... [rest of your existing countries data]
    ]
    
    context = {'countries': countries}
    return render(request, 'global_agency/all_countries.html', context)

def tcu_services(request):
    """
    Render TCU services page showing how GASE helps students with TCU processes
    """
    # ... [your existing TCU services data remains exactly the same]
    context = {'tcu_data': tcu_services_data}
    return render(request, 'global_agency/tcu_services.html', context)