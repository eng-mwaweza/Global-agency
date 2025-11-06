# global_agency/views.py
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
        'australia': {
            'name': 'Australia',
            'flag': '🇦🇺',
            'universities': [
                {'name': 'University of Melbourne', 'slug': 'melbourne'},
                {'name': 'University of Sydney', 'slug': 'sydney'},
                {'name': 'Australian National University', 'slug': 'anu'},
                {'name': 'University of Queensland', 'slug': 'queensland'},
                {'name': 'Monash University', 'slug': 'monash'},
            ]
        },
        'germany': {
            'name': 'Germany',
            'flag': '🇩🇪',
            'universities': [
                {'name': 'Technical University of Munich', 'slug': 'tum'},
                {'name': 'Ludwig Maximilian University of Munich', 'slug': 'lmu-munich'},
                {'name': 'Heidelberg University', 'slug': 'heidelberg'},
                {'name': 'Free University of Berlin', 'slug': 'fu-berlin'},
                {'name': 'Humboldt University of Berlin', 'slug': 'humboldt-berlin'},
            ]
        },
        'china': {
            'name': 'China',
            'flag': '🇨🇳',
            'universities': [
                {'name': 'Tsinghua University', 'slug': 'tsinghua'},
                {'name': 'Peking University', 'slug': 'peking'},
                {'name': 'Fudan University', 'slug': 'fudan'},
                {'name': 'Shanghai Jiao Tong University', 'slug': 'shanghai-jiao-tong'},
                {'name': 'Zhejiang University', 'slug': 'zhejiang'},
            ]
        },
        'india': {
            'name': 'India',
            'flag': '🇮🇳',
            'universities': [
                {'name': 'Indian Institute of Technology Bombay', 'slug': 'iit-bombay'},
                {'name': 'University of Delhi', 'slug': 'delhi'},
                {'name': 'Indian Institute of Science', 'slug': 'iisc'},
                {'name': 'Indian Institute of Technology Delhi', 'slug': 'iit-delhi'},
                {'name': 'University of Mumbai', 'slug': 'mumbai'},
            ]
        },
        'turkey': {
            'name': 'Turkey',
            'flag': '🇹🇷',
            'universities': [
                {'name': 'Middle East Technical University', 'slug': 'metu'},
                {'name': 'Bogazici University', 'slug': 'bogazici'},
                {'name': 'Istanbul University', 'slug': 'istanbul'},
                {'name': 'Ankara University', 'slug': 'ankara'},
            ]
        },
        'netherlands': {
            'name': 'Netherlands',
            'flag': '🇳🇱',
            'universities': [
                {'name': 'University of Amsterdam', 'slug': 'amsterdam'},
                {'name': 'Delft University of Technology', 'slug': 'delft'},
                {'name': 'Utrecht University', 'slug': 'utrecht'},
                {'name': 'Leiden University', 'slug': 'leiden'},
            ]
        },
        'thailand': {
            'name': 'Thailand',
            'flag': '🇹🇭',
            'universities': [
                {'name': 'Chulalongkorn University', 'slug': 'chulalongkorn'},
                {'name': 'Mahidol University', 'slug': 'mahidol'},
                {'name': 'Chiang Mai University', 'slug': 'chiang-mai'},
                {'name': 'Thammasat University', 'slug': 'thammasat'},
            ]
        },
        'norway': {
            'name': 'Norway',
            'flag': '🇳🇴',
            'universities': [
                {'name': 'University of Oslo', 'slug': 'oslo'},
                {'name': 'University of Bergen', 'slug': 'bergen'},
                {'name': 'Norwegian University of Science and Technology', 'slug': 'ntnu'},
                {'name': 'University of Tromsø', 'slug': 'tromso'},
            ]
        },
        'malaysia': {
            'name': 'Malaysia',
            'flag': '🇲🇾',
            'universities': [
                {'name': 'University of Malaya', 'slug': 'malaya'},
                {'name': 'Universiti Kebangsaan Malaysia', 'slug': 'ukm'},
                {'name': 'Universiti Sains Malaysia', 'slug': 'usm'},
                {'name': 'Universiti Putra Malaysia', 'slug': 'upm'},
            ]
        },
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
        # ========== USA UNIVERSITIES ==========
        'harvard': {
            'name': 'Harvard University', 'country': 'USA', 'location': 'Cambridge, Massachusetts', 'ranking': 'World Rank: #1',
            'established': '1636', 'total_students': '21,000', 'international_students': '12%', 'student_faculty_ratio': '7:1',
            'overview': 'Harvard University is a private Ivy League research university in Cambridge, Massachusetts. Founded in 1636, it is the oldest institution of higher learning in the United States.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1520+ or ACT 34+, TOEFL 100+ or IELTS 7.5+',
            'ug_gpa': '3.9', 'sat_score': '1520', 'act_score': '34', 'alevel_grades': 'A*A*A', 'ib_score': '42',
            'toefl': '100', 'ielts': '7.5', 'duolingo': '125', 'pte': '70', 'grad_gpa': '3.7', 'gre': '330', 'gmat': '730',
            'deadline': 'January 1 (Regular Decision)', 'tuition': '$54,000 - $58,000 per year', 'living_costs': '$20,000 - $25,000 per year',
            'scholarships': 'Need-blind admission, full financial aid for families earning <$85,000',
            'website': 'https://www.harvard.edu', 'admission_email': 'college@fas.harvard.edu', 'phone': '+1 (617) 495-1551',
            'address': 'Massachusetts Hall, Cambridge, MA 02138, USA',
        },
        'stanford': {
            'name': 'Stanford University', 'country': 'USA', 'location': 'Stanford, California', 'ranking': 'World Rank: #2',
            'established': '1885', 'total_students': '17,000', 'international_students': '24%', 'student_faculty_ratio': '5:1',
            'overview': 'Stanford University is a private research university known for its entrepreneurial character and relationship with Silicon Valley.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1500+ or ACT 33+, TOEFL 100+ or IELTS 7.0+',
            'ug_gpa': '3.9', 'sat_score': '1500', 'act_score': '33', 'alevel_grades': 'A*A*A', 'ib_score': '40',
            'toefl': '100', 'ielts': '7.0',
            'deadline': 'January 5 (Regular Decision)', 'tuition': '$57,000 per year', 'living_costs': '$18,000 per year',
            'scholarships': 'Merit-based and need-based scholarships available',
            'website': 'https://www.stanford.edu', 'admission_email': 'admission@stanford.edu', 'phone': '+1 (650) 723-2091',
            'address': '450 Serra Mall, Stanford, CA 94305, USA',
        },
        'mit': {
            'name': 'MIT', 'country': 'USA', 'location': 'Cambridge, Massachusetts', 'ranking': 'World Rank: #3',
            'established': '1861', 'total_students': '11,000', 'international_students': '29%', 'student_faculty_ratio': '3:1',
            'overview': 'Massachusetts Institute of Technology is a private land-grant research university known for its programs in engineering and physical sciences.',
            'requirements': 'Minimum GPA 3.9/4.0, TOEFL 100+ or IELTS 7.0+, SAT 1550+',
            'ug_gpa': '3.9', 'sat_score': '1550', 'act_score': '35', 'alevel_grades': 'A*A*A*', 'ib_score': '41',
            'toefl': '100', 'ielts': '7.0',
            'deadline': 'January 5 (Regular Action)', 'tuition': '$53,000 per year', 'living_costs': '$17,000 per year',
            'scholarships': 'Need-blind admission, meets full demonstrated need',
            'website': 'https://www.mit.edu', 'admission_email': 'admissions@mit.edu', 'phone': '+1 (617) 253-1000',
            'address': '77 Massachusetts Ave, Cambridge, MA 02139, USA',
        },
        'caltech': {
            'name': 'California Institute of Technology', 'country': 'USA', 'location': 'Pasadena, California', 'ranking': 'World Rank: #6',
            'established': '1891', 'total_students': '2,200', 'international_students': '33%', 'student_faculty_ratio': '3:1',
            'overview': 'Caltech is a world-renowned science and engineering institute that marshals some of the world\'s brightest minds.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1550+ or ACT 35+, TOEFL 100+ or IELTS 7.0+',
            'deadline': 'January 3 (Regular Decision)', 'tuition': '$56,000 per year', 'living_costs': '$17,500 per year',
            'scholarships': 'Need-based financial aid available',
            'website': 'https://www.caltech.edu', 'admission_email': 'ugadmissions@caltech.edu', 'phone': '+1 (626) 395-6811',
            'address': '1200 E California Blvd, Pasadena, CA 91125, USA',
        },
        'chicago': {
            'name': 'University of Chicago', 'country': 'USA', 'location': 'Chicago, Illinois', 'ranking': 'World Rank: #10',
            'established': '1890', 'total_students': '16,000', 'international_students': '24%', 'student_faculty_ratio': '5:1',
            'overview': 'The University of Chicago is a private research university known for its commitment to rigorous inquiry.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1520+ or ACT 34+, TOEFL 100+ or IELTS 7.0+',
            'deadline': 'January 4 (Regular Decision)', 'tuition': '$59,000 per year', 'living_costs': '$16,000 per year',
            'scholarships': 'Need-based and merit scholarships available',
            'website': 'https://www.uchicago.edu', 'admission_email': 'collegeadmissions@uchicago.edu', 'phone': '+1 (773) 702-1234',
            'address': '5801 S Ellis Ave, Chicago, IL 60637, USA',
        },
        'princeton': {
            'name': 'Princeton University', 'country': 'USA', 'location': 'Princeton, New Jersey', 'ranking': 'World Rank: #7',
            'established': '1746', 'total_students': '8,400', 'international_students': '23%', 'student_faculty_ratio': '5:1',
            'overview': 'Princeton University is a private Ivy League research university known for its commitment to teaching and research.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1500+ or ACT 34+, TOEFL 100+ or IELTS 7.0+',
            'deadline': 'January 1 (Regular Decision)', 'tuition': '$56,000 per year', 'living_costs': '$17,000 per year',
            'scholarships': 'Need-blind admission for all students',
            'website': 'https://www.princeton.edu', 'admission_email': 'uaoffice@princeton.edu', 'phone': '+1 (609) 258-3060',
            'address': 'Princeton, NJ 08544, USA',
        },
        'yale': {
            'name': 'Yale University', 'country': 'USA', 'location': 'New Haven, Connecticut', 'ranking': 'World Rank: #8',
            'established': '1701', 'total_students': '13,600', 'international_students': '22%', 'student_faculty_ratio': '6:1',
            'overview': 'Yale University is a private Ivy League research university known for its excellence in liberal arts education.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1520+ or ACT 34+, TOEFL 100+ or IELTS 7.0+',
            'deadline': 'January 2 (Regular Decision)', 'tuition': '$59,000 per year', 'living_costs': '$16,500 per year',
            'scholarships': 'Need-based financial aid available',
            'website': 'https://www.yale.edu', 'admission_email': 'student.questions@yale.edu', 'phone': '+1 (203) 432-9300',
            'address': 'New Haven, CT 06520, USA',
        },
        'columbia': {
            'name': 'Columbia University', 'country': 'USA', 'location': 'New York City, New York', 'ranking': 'World Rank: #11',
            'established': '1754', 'total_students': '33,000', 'international_students': '35%', 'student_faculty_ratio': '6:1',
            'overview': 'Columbia University is a private Ivy League research university in New York City.',
            'requirements': 'Minimum GPA 3.9/4.0, SAT 1500+ or ACT 34+, TOEFL 105+ or IELTS 7.5+',
            'deadline': 'January 1 (Regular Decision)', 'tuition': '$61,000 per year', 'living_costs': '$16,000 per year',
            'scholarships': 'Need-based financial aid available',
            'website': 'https://www.columbia.edu', 'admission_email': 'ugrad-ask@columbia.edu', 'phone': '+1 (212) 854-2522',
            'address': '116th St & Broadway, New York, NY 10027, USA',
        },

        # ========== UK UNIVERSITIES ==========
        'oxford': {
            'name': 'University of Oxford', 'country': 'UK', 'location': 'Oxford, England', 'ranking': 'World Rank: #4',
            'established': '1096', 'total_students': '24,000', 'international_students': '45%', 'student_faculty_ratio': '11:1',
            'overview': 'The University of Oxford is a collegiate research university and the oldest university in the English-speaking world.',
            'requirements': 'A-levels: A*A*A, IB: 38-40 points, IELTS 7.5+',
            'ug_gpa': '3.7', 'alevel_grades': 'A*A*A', 'ib_score': '39', 'toefl': '110', 'ielts': '7.5',
            'deadline': 'October 15 (Undergraduate)', 'tuition': '£25,000 - £35,000 per year', 'living_costs': '£12,000 - £15,000 per year',
            'scholarships': 'Rhodes Scholarships, Clarendon Fund, departmental scholarships',
            'website': 'https://www.ox.ac.uk', 'admission_email': 'undergraduate.admissions@admin.ox.ac.uk', 'phone': '+44 (0)1865 288000',
            'address': 'University Offices, Wellington Square, Oxford OX1 2JD, UK',
        },
        'cambridge': {
            'name': 'University of Cambridge', 'country': 'UK', 'location': 'Cambridge, England', 'ranking': 'World Rank: #5',
            'established': '1209', 'total_students': '23,000', 'international_students': '40%', 'student_faculty_ratio': '11:1',
            'overview': 'The University of Cambridge is a collegiate research university that ranks among the most prestigious universities in the world.',
            'requirements': 'A-levels: A*A*A, IB: 40-42 points, IELTS 7.5+',
            'ug_gpa': '3.8', 'alevel_grades': 'A*A*A', 'ib_score': '42', 'toefl': '110', 'ielts': '7.5',
            'deadline': 'October 15 (Undergraduate)', 'tuition': '£22,000 - £35,000 per year', 'living_costs': '£11,000 - £14,000 per year',
            'scholarships': 'Cambridge Trust Scholarships, College-specific awards',
            'website': 'https://www.cam.ac.uk', 'admission_email': 'admissions@cam.ac.uk', 'phone': '+44 (0)1223 333308',
            'address': 'The Old Schools, Trinity Lane, Cambridge CB2 1TN, UK',
        },
        'imperial': {
            'name': 'Imperial College London', 'country': 'UK', 'location': 'London, England', 'ranking': 'World Rank: #6',
            'established': '1907', 'total_students': '19,000', 'international_students': '60%', 'student_faculty_ratio': '11:1',
            'overview': 'Imperial College London is a public research university specializing in science, engineering, medicine, and business.',
            'requirements': 'A-levels: A*A*A, IB: 39 points, IELTS 7.0+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '£32,000 - £38,000 per year', 'living_costs': '£15,000 - £18,000 per year',
            'scholarships': 'President\'s Scholarships, Departmental awards',
            'website': 'https://www.imperial.ac.uk', 'admission_email': 'ug.admissions@imperial.ac.uk', 'phone': '+44 (0)20 7589 5111',
            'address': 'South Kensington Campus, London SW7 2AZ, UK',
        },
        'lse': {
            'name': 'London School of Economics', 'country': 'UK', 'location': 'London, England', 'ranking': 'World Rank: #27',
            'established': '1895', 'total_students': '11,000', 'international_students': '70%', 'student_faculty_ratio': '13:1',
            'overview': 'LSE is a public research university specializing in social sciences and one of the most international universities in the world.',
            'requirements': 'A-levels: A*AA, IB: 38 points, IELTS 7.0+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '£22,000 per year', 'living_costs': '£13,000 - £15,000 per year',
            'scholarships': 'LSE Scholarships, Departmental awards',
            'website': 'https://www.lse.ac.uk', 'admission_email': 'ug.admissions@lse.ac.uk', 'phone': '+44 (0)20 7405 7686',
            'address': 'Houghton St, London WC2A 2AE, UK',
        },
        'ucl': {
            'name': 'University College London', 'country': 'UK', 'location': 'London, England', 'ranking': 'World Rank: #9',
            'established': '1826', 'total_students': '41,000', 'international_students': '53%', 'student_faculty_ratio': '10:1',
            'overview': 'UCL is a public research university and a constituent college of the federal University of London.',
            'requirements': 'A-levels: A*AA, IB: 39 points, IELTS 7.0+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '£21,000 - £28,000 per year', 'living_costs': '£12,000 - £15,000 per year',
            'scholarships': 'UCL Scholarships, Global Excellence Scholarships',
            'website': 'https://www.ucl.ac.uk', 'admission_email': 'undergraduate-admissions@ucl.ac.uk', 'phone': '+44 (0)20 7679 2000',
            'address': 'Gower St, London WC1E 6BT, UK',
        },
        'edinburgh': {
            'name': 'University of Edinburgh', 'country': 'UK', 'location': 'Edinburgh, Scotland', 'ranking': 'World Rank: #22',
            'established': '1583', 'total_students': '35,000', 'international_students': '42%', 'student_faculty_ratio': '12:1',
            'overview': 'The University of Edinburgh is a public research university and one of Scotland\'s ancient universities.',
            'requirements': 'A-levels: AAA, IB: 37 points, IELTS 6.5+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '£20,000 - £26,000 per year', 'living_costs': '£9,000 - £12,000 per year',
            'scholarships': 'Edinburgh Global Scholarships, College-specific awards',
            'website': 'https://www.ed.ac.uk', 'admission_email': 'sra.admissions@ed.ac.uk', 'phone': '+44 (0)131 650 1000',
            'address': 'Old College, South Bridge, Edinburgh EH8 9YL, UK',
        },

        # ========== CANADA UNIVERSITIES ==========
        'toronto': {
            'name': 'University of Toronto', 'country': 'Canada', 'location': 'Toronto, Ontario', 'ranking': 'World Rank: #18',
            'established': '1827', 'total_students': '93,000', 'international_students': '25%', 'student_faculty_ratio': '25:1',
            'overview': 'The University of Toronto is a public research university and Canada\'s leading institution of learning.',
            'requirements': 'Minimum GPA 3.6/4.0, IELTS 6.5+ or TOEFL 100+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'CAD 45,000 - CAD 55,000 per year', 'living_costs': 'CAD 12,000 - CAD 15,000 per year',
            'scholarships': 'Lester B. Pearson Scholarship, President\'s Scholars',
            'website': 'https://www.utoronto.ca', 'admission_email': 'ask@adm.utoronto.ca', 'phone': '+1 (416) 978-2011',
            'address': '27 King\'s College Cir, Toronto, ON M5S, Canada',
        },
        'ubc': {
            'name': 'University of British Columbia', 'country': 'Canada', 'location': 'Vancouver, British Columbia', 'ranking': 'World Rank: #31',
            'established': '1908', 'total_students': '66,000', 'international_students': '30%', 'student_faculty_ratio': '18:1',
            'overview': 'UBC is a public research university and one of the most international universities in Canada.',
            'requirements': 'Minimum GPA 3.3/4.0, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'CAD 38,000 - CAD 50,000 per year', 'living_costs': 'CAD 12,000 - CAD 15,000 per year',
            'scholarships': 'International Major Entrance Scholarship, Outstanding International Student Award',
            'website': 'https://www.ubc.ca', 'admission_email': 'international.reception@ubc.ca', 'phone': '+1 (604) 822-2211',
            'address': '2329 West Mall, Vancouver, BC V6T 1Z4, Canada',
        },
        'mcgill': {
            'name': 'McGill University', 'country': 'Canada', 'location': 'Montreal, Quebec', 'ranking': 'World Rank: #30',
            'established': '1821', 'total_students': '40,000', 'international_students': '32%', 'student_faculty_ratio': '16:1',
            'overview': 'McGill University is a public research university and one of Canada\'s best-known institutions of higher learning.',
            'requirements': 'Minimum GPA 3.2/4.0, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'CAD 22,000 - CAD 48,000 per year', 'living_costs': 'CAD 12,000 - CAD 15,000 per year',
            'scholarships': 'McGill Entrance Scholarship, PBEEE - Quebec program',
            'website': 'https://www.mcgill.ca', 'admission_email': 'admissions@mcgill.ca', 'phone': '+1 (514) 398-4455',
            'address': '845 Sherbrooke St W, Montreal, Quebec H3A 0G4, Canada',
        },
        'alberta': {
            'name': 'University of Alberta', 'country': 'Canada', 'location': 'Edmonton, Alberta', 'ranking': 'World Rank: #119',
            'established': '1908', 'total_students': '40,000', 'international_students': '22%', 'student_faculty_ratio': '21:1',
            'overview': 'The University of Alberta is a public research university known for its excellence in humanities, sciences, and engineering.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'March 1 (Undergraduate)', 'tuition': 'CAD 22,000 - CAD 30,000 per year', 'living_costs': 'CAD 10,000 - CAD 12,000 per year',
            'scholarships': 'International Student Scholarship, Regional Excellence Scholarship',
            'website': 'https://www.ualberta.ca', 'admission_email': 'registrar@ualberta.ca', 'phone': '+1 (780) 492-3111',
            'address': '116 St & 85 Ave, Edmonton, AB T6G 2R3, Canada',
        },
        'mcmaster': {
            'name': 'McMaster University', 'country': 'Canada', 'location': 'Hamilton, Ontario', 'ranking': 'World Rank: #85',
            'established': '1887', 'total_students': '33,000', 'international_students': '18%', 'student_faculty_ratio': '26:1',
            'overview': 'McMaster University is a public research university known for its innovation in learning and discovery.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 86+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'CAD 25,000 - CAD 35,000 per year', 'living_costs': 'CAD 10,000 - CAD 12,000 per year',
            'scholarships': 'McMaster President\'s Award, International Excellence Award',
            'website': 'https://www.mcmaster.ca', 'admission_email': 'macadmit@mcmaster.ca', 'phone': '+1 (905) 525-9140',
            'address': '1280 Main St W, Hamilton, ON L8S 4L8, Canada',
        },

        # ========== AUSTRALIA UNIVERSITIES ==========
        'melbourne': {
            'name': 'University of Melbourne', 'country': 'Australia', 'location': 'Melbourne, Victoria', 'ranking': 'World Rank: #33',
            'established': '1853', 'total_students': '52,000', 'international_students': '42%', 'student_faculty_ratio': '12:1',
            'overview': 'The University of Melbourne is a public research university and a sandstone university.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 79+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'AUD 35,000 - AUD 45,000 per year', 'living_costs': 'AUD 18,000 - AUD 25,000 per year',
            'scholarships': 'Melbourne International Undergraduate Scholarship',
            'website': 'https://www.unimelb.edu.au', 'admission_email': 'admissions@unimelb.edu.au', 'phone': '+61 3 9035 5511',
            'address': 'Parkville VIC 3010, Australia',
        },
        'sydney': {
            'name': 'University of Sydney', 'country': 'Australia', 'location': 'Sydney, New South Wales', 'ranking': 'World Rank: #41',
            'established': '1850', 'total_students': '61,000', 'international_students': '43%', 'student_faculty_ratio': '15:1',
            'overview': 'The University of Sydney is a public research university and Australia\'s first university.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 85+',
            'deadline': 'January 31 (Undergraduate)', 'tuition': 'AUD 35,000 - AUD 50,000 per year', 'living_costs': 'AUD 18,000 - AUD 25,000 per year',
            'scholarships': 'Sydney Scholars Awards, Vice-Chancellor\'s International Scholarships',
            'website': 'https://www.sydney.edu.au', 'admission_email': 'admissions.info@sydney.edu.au', 'phone': '+61 2 8627 1444',
            'address': 'Camperdown NSW 2006, Australia',
        },
        'anu': {
            'name': 'Australian National University', 'country': 'Australia', 'location': 'Canberra, ACT', 'ranking': 'World Rank: #34',
            'established': '1946', 'total_students': '20,000', 'international_students': '37%', 'student_faculty_ratio': '15:1',
            'overview': 'ANU is a public research university located in Canberra, the capital of Australia.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 80+',
            'deadline': 'December 15 (Undergraduate)', 'tuition': 'AUD 30,000 - AUD 45,000 per year', 'living_costs': 'AUD 15,000 - AUD 20,000 per year',
            'scholarships': 'ANU Chancellor\'s International Scholarship',
            'website': 'https://www.anu.edu.au', 'admission_email': 'admissions@anu.edu.au', 'phone': '+61 2 6125 5111',
            'address': 'Acton ACT 2601, Australia',
        },
        'queensland': {
            'name': 'University of Queensland', 'country': 'Australia', 'location': 'Brisbane, Queensland', 'ranking': 'World Rank: #50',
            'established': '1909', 'total_students': '55,000', 'international_students': '40%', 'student_faculty_ratio': '20:1',
            'overview': 'The University of Queensland is a public research university primarily located in Brisbane.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 87+',
            'deadline': 'November 30 (Undergraduate)', 'tuition': 'AUD 30,000 - AUD 45,000 per year', 'living_costs': 'AUD 15,000 - AUD 20,000 per year',
            'scholarships': 'UQ Excellence Scholarship, International Science Scholarship',
            'website': 'https://www.uq.edu.au', 'admission_email': 'international.admissions@uq.edu.au', 'phone': '+61 7 3365 1111',
            'address': 'Brisbane QLD 4072, Australia',
        },
        'monash': {
            'name': 'Monash University', 'country': 'Australia', 'location': 'Melbourne, Victoria', 'ranking': 'World Rank: #57',
            'established': '1958', 'total_students': '67,000', 'international_students': '35%', 'student_faculty_ratio': '20:1',
            'overview': 'Monash University is a public research university and a member of Australia\'s Group of Eight.',
            'requirements': 'Minimum GPA 3.0/4.0, IELTS 6.5+ or TOEFL 79+',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'AUD 30,000 - AUD 45,000 per year', 'living_costs': 'AUD 18,000 - AUD 22,000 per year',
            'scholarships': 'Monash International Merit Scholarship',
            'website': 'https://www.monash.edu', 'admission_email': 'monashconnect@monash.edu', 'phone': '+61 3 9902 6011',
            'address': 'Wellington Rd, Clayton VIC 3800, Australia',
        },

        # ========== GERMANY UNIVERSITIES ==========
        'tum': {
            'name': 'Technical University of Munich', 'country': 'Germany', 'location': 'Munich, Germany', 'ranking': 'World Rank: #50',
            'established': '1868', 'total_students': '42,000', 'international_students': '34%', 'student_faculty_ratio': '14:1',
            'overview': 'Technical University of Munich is a research university with a focus on engineering, technology, medicine, and natural and life sciences.',
            'requirements': 'High School Diploma, TestAS exam, German B2+ for German programs',
            'deadline': 'July 15 (Winter Semester)', 'tuition': 'No tuition fees (only semester fee of €150-300)', 'living_costs': '€800 - €1,200 per month',
            'scholarships': 'DAAD scholarships, Deutschlandstipendium, TUM scholarships',
            'website': 'https://www.tum.de', 'admission_email': 'study@tum.de', 'phone': '+49 89 289 01',
            'address': 'Arcisstraße 21, 80333 München, Germany',
        },
        'lmu-munich': {
            'name': 'Ludwig Maximilian University of Munich', 'country': 'Germany', 'location': 'Munich, Germany', 'ranking': 'World Rank: #59',
            'established': '1472', 'total_students': '52,000', 'international_students': '17%', 'student_faculty_ratio': '35:1',
            'overview': 'LMU Munich is a public research university and one of Europe\'s premier academic and research institutions.',
            'requirements': 'High School Diploma, German C1 for German programs',
            'deadline': 'July 15 (Winter Semester)', 'tuition': 'No tuition fees (only semester fee of €128)', 'living_costs': '€850 - €1,000 per month',
            'scholarships': 'LMU Scholarship, Deutschlandstipendium',
            'website': 'https://www.lmu.de', 'admission_email': 'international@lmu.de', 'phone': '+49 89 2180 0',
            'address': 'Geschwister-Scholl-Platz 1, 80539 München, Germany',
        },
        'heidelberg': {
            'name': 'Heidelberg University', 'country': 'Germany', 'location': 'Heidelberg, Germany', 'ranking': 'World Rank: #54',
            'established': '1386', 'total_students': '30,000', 'international_students': '20%', 'student_faculty_ratio': '18:1',
            'overview': 'Heidelberg University is a public research university and Germany\'s oldest university.',
            'requirements': 'High School Diploma, German C1 for German programs',
            'deadline': 'July 15 (Winter Semester)', 'tuition': 'No tuition fees (only semester fee of €171)', 'living_costs': '€700 - €900 per month',
            'scholarships': 'Heidelberg University Scholarship, Deutschlandstipendium',
            'website': 'https://www.uni-heidelberg.de', 'admission_email': 'studium@uni-heidelberg.de', 'phone': '+49 6221 54 0',
            'address': 'Grabengasse 1, 69117 Heidelberg, Germany',
        },
        'fu-berlin': {
            'name': 'Free University of Berlin', 'country': 'Germany', 'location': 'Berlin, Germany', 'ranking': 'World Rank: #130',
            'established': '1948', 'total_students': '33,000', 'international_students': '22%', 'student_faculty_ratio': '12:1',
            'overview': 'The Free University of Berlin is a public research university known for its research in humanities, social sciences, and natural sciences.',
            'requirements': 'High School Diploma, German C1 for German programs',
            'deadline': 'July 15 (Winter Semester)', 'tuition': 'No tuition fees (only semester fee of €312)', 'living_costs': '€850 - €1,000 per month',
            'scholarships': 'FU Berlin Scholarship, Deutschlandstipendium',
            'website': 'https://www.fu-berlin.de', 'admission_email': 'info-service@fu-berlin.de', 'phone': '+49 30 8381',
            'address': 'Kaiserswerther Str. 16-18, 14195 Berlin, Germany',
        },
        'humboldt-berlin': {
            'name': 'Humboldt University of Berlin', 'country': 'Germany', 'location': 'Berlin, Germany', 'ranking': 'World Rank: #120',
            'established': '1810', 'total_students': '35,000', 'international_students': '18%', 'student_faculty_ratio': '15:1',
            'overview': 'Humboldt University of Berlin is a public research university that has educated 29 Nobel Prize winners.',
            'requirements': 'High School Diploma, German C1 for German programs',
            'deadline': 'July 15 (Winter Semester)', 'tuition': 'No tuition fees (only semester fee of €312)', 'living_costs': '€850 - €1,000 per month',
            'scholarships': 'Humboldt Scholarship, Deutschlandstipendium',
            'website': 'https://www.hu-berlin.de', 'admission_email': 'international@hu-berlin.de', 'phone': '+49 30 2093 0',
            'address': 'Unter den Linden 6, 10117 Berlin, Germany',
        },

        # ========== CHINA UNIVERSITIES ==========
        'tsinghua': {
            'name': 'Tsinghua University', 'country': 'China', 'location': 'Beijing, China', 'ranking': 'World Rank: #16',
            'established': '1911', 'total_students': '48,000', 'international_students': '12%', 'student_faculty_ratio': '12:1',
            'overview': 'Tsinghua University is a public research university and a member of the C9 League of Chinese universities.',
            'requirements': 'High School Diploma, HSK 5 for Chinese programs, IELTS 6.5+ for English programs',
            'deadline': 'January 15 (Undergraduate)', 'tuition': 'CNY 26,000 - CNY 40,000 per year', 'living_costs': 'CNY 20,000 - CNY 30,000 per year',
            'scholarships': 'Chinese Government Scholarship, Tsinghua University Scholarship',
            'website': 'https://www.tsinghua.edu.cn', 'admission_email': 'admissions@tsinghua.edu.cn', 'phone': '+86 10 6278 3001',
            'address': '30 Shuangqing Rd, Haidian District, Beijing, China',
        },
        'peking': {
            'name': 'Peking University', 'country': 'China', 'location': 'Beijing, China', 'ranking': 'World Rank: #17',
            'established': '1898', 'total_students': '40,000', 'international_students': '15%', 'student_faculty_ratio': '10:1',
            'overview': 'Peking University is a public research university and a member of the C9 League of Chinese universities.',
            'requirements': 'High School Diploma, HSK 6 for Chinese programs, IELTS 6.5+ for English programs',
            'deadline': 'December 31 (Undergraduate)', 'tuition': 'CNY 26,000 - CNY 40,000 per year', 'living_costs': 'CNY 20,000 - CNY 30,000 per year',
            'scholarships': 'Chinese Government Scholarship, Peking University Scholarship',
            'website': 'https://www.pku.edu.cn', 'admission_email': 'study@pku.edu.cn', 'phone': '+86 10 6275 1234',
            'address': '5 Yiheyuan Rd, Haidian District, Beijing, China',
        },
        'fudan': {
            'name': 'Fudan University', 'country': 'China', 'location': 'Shanghai, China', 'ranking': 'World Rank: #31',
            'established': '1905', 'total_students': '35,000', 'international_students': '18%', 'student_faculty_ratio': '12:1',
            'overview': 'Fudan University is a public research university and a member of the C9 League of Chinese universities.',
            'requirements': 'High School Diploma, HSK 5 for Chinese programs, IELTS 6.5+ for English programs',
            'deadline': 'December 31 (Undergraduate)', 'tuition': 'CNY 23,000 - CNY 45,000 per year', 'living_costs': 'CNY 18,000 - CNY 25,000 per year',
            'scholarships': 'Chinese Government Scholarship, Fudan University Scholarship',
            'website': 'https://www.fudan.edu.cn', 'admission_email': 'admission@fudan.edu.cn', 'phone': '+86 21 6564 2222',
            'address': '220 Handan Rd, Yangpu District, Shanghai, China',
        },
        'shanghai-jiao-tong': {
            'name': 'Shanghai Jiao Tong University', 'country': 'China', 'location': 'Shanghai, China', 'ranking': 'World Rank: #46',
            'established': '1896', 'total_students': '42,000', 'international_students': '10%', 'student_faculty_ratio': '15:1',
            'overview': 'Shanghai Jiao Tong University is a public research university and a member of the C9 League of Chinese universities.',
            'requirements': 'High School Diploma, HSK 5 for Chinese programs, IELTS 6.0+ for English programs',
            'deadline': 'December 31 (Undergraduate)', 'tuition': 'CNY 24,000 - CNY 50,000 per year', 'living_costs': 'CNY 18,000 - CNY 25,000 per year',
            'scholarships': 'Chinese Government Scholarship, SJTU Scholarship',
            'website': 'https://www.sjtu.edu.cn', 'admission_email': 'iso@sjtu.edu.cn', 'phone': '+86 21 3420 6001',
            'address': '800 Dongchuan Rd, Minhang District, Shanghai, China',
        },
        'zhejiang': {
            'name': 'Zhejiang University', 'country': 'China', 'location': 'Hangzhou, China', 'ranking': 'World Rank: #53',
            'established': '1897', 'total_students': '54,000', 'international_students': '12%', 'student_faculty_ratio': '14:1',
            'overview': 'Zhejiang University is a public research university and a member of the C9 League of Chinese universities.',
            'requirements': 'High School Diploma, HSK 5 for Chinese programs, IELTS 6.0+ for English programs',
            'deadline': 'February 28 (Undergraduate)', 'tuition': 'CNY 20,000 - CNY 42,000 per year', 'living_costs': 'CNY 15,000 - CNY 20,000 per year',
            'scholarships': 'Chinese Government Scholarship, Zhejiang University Scholarship',
            'website': 'https://www.zju.edu.cn', 'admission_email': 'admission@zju.edu.cn', 'phone': '+86 571 8795 1114',
            'address': '866 Yuhangtang Rd, Xihu District, Hangzhou, China',
        },

        # ========== INDIA UNIVERSITIES ==========
        'iit-bombay': {
            'name': 'Indian Institute of Technology Bombay', 'country': 'India', 'location': 'Mumbai, India', 'ranking': 'World Rank: #172',
            'established': '1958', 'total_students': '10,000', 'international_students': '5%', 'student_faculty_ratio': '9:1',
            'overview': 'IIT Bombay is a public technical and research university and one of the premier engineering institutions in India.',
            'requirements': 'JEE Advanced qualified, minimum 75% in 12th grade',
            'deadline': 'April 30 (Undergraduate)', 'tuition': 'INR 200,000 - INR 300,000 per year', 'living_costs': 'INR 100,000 - INR 150,000 per year',
            'scholarships': 'Institute Merit-cum-Means Scholarship, Government Scholarships',
            'website': 'https://www.iitb.ac.in', 'admission_email': 'acadsec@iitb.ac.in', 'phone': '+91 22 2572 2545',
            'address': 'Powai, Mumbai, Maharashtra 400076, India',
        },
        'delhi': {
            'name': 'University of Delhi', 'country': 'India', 'location': 'New Delhi, India', 'ranking': 'World Rank: #521-530',
            'established': '1922', 'total_students': '132,000', 'international_students': '3%', 'student_faculty_ratio': '28:1',
            'overview': 'The University of Delhi is a collegiate public research university offering courses in various disciplines.',
            'requirements': 'Minimum 60% in 12th grade, entrance exams for specific programs',
            'deadline': 'June 30 (Undergraduate)', 'tuition': 'INR 10,000 - INR 50,000 per year', 'living_costs': 'INR 80,000 - INR 120,000 per year',
            'scholarships': 'University Merit Scholarship, Government Scholarships',
            'website': 'https://www.du.ac.in', 'admission_email': 'registrar@du.ac.in', 'phone': '+91 11 2700 6900',
            'address': 'University Rd, New Delhi, Delhi 110007, India',
        },
        'iisc': {
            'name': 'Indian Institute of Science', 'country': 'India', 'location': 'Bangalore, India', 'ranking': 'World Rank: #225',
            'established': '1909', 'total_students': '4,000', 'international_students': '2%', 'student_faculty_ratio': '8:1',
            'overview': 'IISc is a public, deemed, research university for higher education and research in science, engineering, design, and management.',
            'requirements': 'JEE Advanced/KVPY/IIT-JAM qualified, Strong research background',
            'deadline': 'March 31 (Undergraduate)', 'tuition': 'INR 150,000 - INR 250,000 per year', 'living_costs': 'INR 80,000 - INR 120,000 per year',
            'scholarships': 'Institute Fellowship, Government Scholarships',
            'website': 'https://www.iisc.ac.in', 'admission_email': 'registrar@iisc.ac.in', 'phone': '+91 80 2293 2001',
            'address': 'CV Raman Rd, Bengaluru, Karnataka 560012, India',
        },
        'iit-delhi': {
            'name': 'Indian Institute of Technology Delhi', 'country': 'India', 'location': 'New Delhi, India', 'ranking': 'World Rank: #174',
            'established': '1961', 'total_students': '9,000', 'international_students': '4%', 'student_faculty_ratio': '10:1',
            'overview': 'IIT Delhi is a public technical and research university located in Hauz Khas, Delhi.',
            'requirements': 'JEE Advanced qualified, minimum 75% in 12th grade',
            'deadline': 'April 30 (Undergraduate)', 'tuition': 'INR 250,000 - INR 350,000 per year', 'living_costs': 'INR 100,000 - INR 150,000 per year',
            'scholarships': 'Merit-cum-Means Scholarship, Institute Scholarships',
            'website': 'https://www.iitd.ac.in', 'admission_email': 'webmaster@admin.iitd.ac.in', 'phone': '+91 11 2659 7135',
            'address': 'Hauz Khas, New Delhi, Delhi 110016, India',
        },
        'mumbai': {
            'name': 'University of Mumbai', 'country': 'India', 'location': 'Mumbai, India', 'ranking': 'World Rank: 801-1000',
            'established': '1857', 'total_students': '800,000', 'international_students': '1%', 'student_faculty_ratio': '50:1',
            'overview': 'The University of Mumbai is a public state university located in Mumbai. It is one of the largest universities in the world.',
            'requirements': 'Minimum 45% in 12th grade, entrance exams for professional courses',
            'deadline': 'June 15 (Undergraduate)', 'tuition': 'INR 5,000 - INR 50,000 per year', 'living_costs': 'INR 80,000 - INR 120,000 per year',
            'scholarships': 'University Scholarships, Government Scholarships',
            'website': 'https://www.mu.ac.in', 'admission_email': 'examination@mu.ac.in', 'phone': '+91 22 2654 3000',
            'address': 'Mahatma Gandhi Rd, Fort, Mumbai, Maharashtra 400032, India',
        },

        # ========== TURKEY UNIVERSITIES ==========
        'metu': {
            'name': 'Middle East Technical University', 'country': 'Turkey', 'location': 'Ankara, Turkey', 'ranking': 'World Rank: #551-560',
            'established': '1956', 'total_students': '27,000', 'international_students': '5%', 'student_faculty_ratio': '20:1',
            'overview': 'METU is a public technical university located in Ankara, known for its contributions to engineering and natural sciences.',
            'requirements': 'METU Entrance Exam, minimum high school diploma, English proficiency',
            'deadline': 'July 15 (Undergraduate)', 'tuition': 'USD 600 - USD 1,500 per year', 'living_costs': 'USD 300 - USD 500 per month',
            'scholarships': 'METU Development Foundation Scholarship, Turkish Government Scholarships',
            'website': 'https://www.metu.edu.tr', 'admission_email': 'iso@metu.edu.tr', 'phone': '+90 312 210 2000',
            'address': 'Üniversiteler Mahallesi, Dumlupınar Bulvarı No:1, 06800 Çankaya/Ankara, Turkey',
        },
        'bogazici': {
            'name': 'Bogazici University', 'country': 'Turkey', 'location': 'Istanbul, Turkey', 'ranking': 'World Rank: #601-650',
            'established': '1863', 'total_students': '17,000', 'international_students': '3%', 'student_faculty_ratio': '15:1',
            'overview': 'Bogazici University is a public research university located on the Bosphorus in Istanbul. It is known for its high academic standards.',
            'requirements': 'Bogazici University Entrance Exam, high school diploma, English proficiency',
            'deadline': 'July 10 (Undergraduate)', 'tuition': 'USD 500 - USD 1,200 per year', 'living_costs': 'USD 350 - USD 550 per month',
            'scholarships': 'University Scholarships, Turkish Government Scholarships',
            'website': 'https://www.boun.edu.tr', 'admission_email': 'registrar@boun.edu.tr', 'phone': '+90 212 359 5400',
            'address': 'Bebek, 34342 Beşiktaş/İstanbul, Turkey',
        },
        'istanbul': {
            'name': 'Istanbul University', 'country': 'Turkey', 'location': 'Istanbul, Turkey', 'ranking': 'World Rank: 801-1000',
            'established': '1453', 'total_students': '76,000', 'international_students': '4%', 'student_faculty_ratio': '25:1',
            'overview': 'Istanbul University is a prominent Turkish university located in Istanbul. It is the oldest and one of the most respected educational institutions in Turkey.',
            'requirements': 'Istanbul University Entrance Exam, high school diploma',
            'deadline': 'July 20 (Undergraduate)', 'tuition': 'USD 400 - USD 1,000 per year', 'living_costs': 'USD 300 - USD 500 per month',
            'scholarships': 'University Scholarships, Turkish Government Scholarships',
            'website': 'https://www.istanbul.edu.tr', 'admission_email': 'oidb@istanbul.edu.tr', 'phone': '+90 212 440 0000',
            'address': 'Beyazıt, 34452 Fatih/İstanbul, Turkey',
        },
        'ankara': {
            'name': 'Ankara University', 'country': 'Turkey', 'location': 'Ankara, Turkey', 'ranking': 'World Rank: 801-1000',
            'established': '1946', 'total_students': '70,000', 'international_students': '3%', 'student_faculty_ratio': '22:1',
            'overview': 'Ankara University is a public university in Ankara, the capital city of Turkey. It was the first higher education institution founded in Turkey after the formation of the republic.',
            'requirements': 'Ankara University Entrance Exam, high school diploma',
            'deadline': 'July 25 (Undergraduate)', 'tuition': 'USD 350 - USD 900 per year', 'living_costs': 'USD 280 - USD 450 per month',
            'scholarships': 'University Scholarships, Turkish Government Scholarships',
            'website': 'https://www.ankara.edu.tr', 'admission_email': 'oidb@ankara.edu.tr', 'phone': '+90 312 212 6040',
            'address': 'Dögol Caddesi, 06100 Tandoğan/Ankara, Turkey',
        },

        # ========== NETHERLANDS UNIVERSITIES ==========
        'amsterdam': {
            'name': 'University of Amsterdam', 'country': 'Netherlands', 'location': 'Amsterdam, Netherlands', 'ranking': 'World Rank: #55',
            'established': '1632', 'total_students': '31,000', 'international_students': '25%', 'student_faculty_ratio': '12:1',
            'overview': 'The University of Amsterdam is a public research university and one of the largest research universities in Europe.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 92+',
            'ug_gpa': '3.0', 'alevel_grades': 'ABB', 'ib_score': '34', 'toefl': '92', 'ielts': '6.5',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '€8,000 - €12,000 per year', 'living_costs': '€800 - €1,200 per month',
            'scholarships': 'Amsterdam Merit Scholarship, Holland Scholarship',
            'website': 'https://www.uva.nl', 'admission_email': 'international@uva.nl', 'phone': '+31 (0)20 525 9111',
            'address': 'Spui 21, 1012 WX Amsterdam, Netherlands',
        },
        'leiden': {
            'name': 'Leiden University', 'country': 'Netherlands', 'location': 'Leiden, Netherlands', 'ranking': 'World Rank: #77',
            'established': '1575', 'total_students': '33,000', 'international_students': '16%', 'student_faculty_ratio': '14:1',
            'overview': 'Leiden University is the oldest university in the Netherlands, known for its excellence in humanities, law, and sciences.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 90+',
            'ug_gpa': '3.0', 'alevel_grades': 'ABB', 'ib_score': '34', 'toefl': '90', 'ielts': '6.5',
            'deadline': 'April 1 (Undergraduate)', 'tuition': '€10,000 - €15,000 per year', 'living_costs': '€800 - €1,100 per month',
            'scholarships': 'Leiden University Excellence Scholarship, Holland Scholarship',
            'website': 'https://www.universiteitleiden.nl', 'admission_email': 'study@leidenuniv.nl', 'phone': '+31 (0)71 527 8011',
            'address': 'Rapenburg 70, 2311 EZ Leiden, Netherlands',
        },
        'utrecht': {
            'name': 'Utrecht University', 'country': 'Netherlands', 'location': 'Utrecht, Netherlands', 'ranking': 'World Rank: #66',
            'established': '1636', 'total_students': '37,000', 'international_students': '12%', 'student_faculty_ratio': '13:1',
            'overview': 'Utrecht University is a public research university and one of the oldest universities in the Netherlands.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 83+',
            'ug_gpa': '3.0', 'alevel_grades': 'ABB', 'ib_score': '34', 'toefl': '83', 'ielts': '6.5',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '€9,000 - €13,000 per year', 'living_costs': '€800 - €1,100 per month',
            'scholarships': 'Utrecht Excellence Scholarship, Holland Scholarship',
            'website': 'https://www.uu.nl', 'admission_email': 'study@uu.nl', 'phone': '+31 (0)30 253 3550',
            'address': 'Heidelberglaan 8, 3584 CS Utrecht, Netherlands',
        },
        'delft': {
            'name': 'Delft University of Technology', 'country': 'Netherlands', 'location': 'Delft, Netherlands', 'ranking': 'World Rank: #47',
            'established': '1842', 'total_students': '25,000', 'international_students': '28%', 'student_faculty_ratio': '11:1',
            'overview': 'TU Delft is the oldest and largest Dutch public technical university, known for its engineering programs.',
            'requirements': 'High School Diploma with strong mathematics and physics, IELTS 6.5+ or TOEFL 90+',
            'ug_gpa': '3.2', 'alevel_grades': 'AAB', 'ib_score': '36', 'toefl': '90', 'ielts': '6.5',
            'deadline': 'January 15 (Undergraduate)', 'tuition': '€15,000 per year', 'living_costs': '€800 - €1,200 per month',
            'scholarships': 'TU Delft Excellence Scholarship, Justus & Louise van Effen Scholarship',
            'website': 'https://www.tudelft.nl', 'admission_email': 'study@tudelft.nl', 'phone': '+31 (0)15 278 8010',
            'address': 'Mekelweg 5, 2628 CD Delft, Netherlands',
        },

        # ========== THAILAND UNIVERSITIES ==========
        'chulalongkorn': {
            'name': 'Chulalongkorn University', 'country': 'Thailand', 'location': 'Bangkok, Thailand', 'ranking': 'World Rank: #224',
            'established': '1917', 'total_students': '37,000', 'international_students': '5%', 'student_faculty_ratio': '15:1',
            'overview': 'Chulalongkorn University is a public research university and the oldest institution of higher education in Thailand.',
            'requirements': 'High School Diploma, IELTS 6.0+ or TOEFL 79+',
            'deadline': 'March 31 (Undergraduate)', 'tuition': 'THB 50,000 - THB 150,000 per year', 'living_costs': 'THB 10,000 - THB 15,000 per month',
            'scholarships': 'Chulalongkorn University Scholarship, Thai Government Scholarship',
            'website': 'https://www.chula.ac.th', 'admission_email': 'inter@chula.ac.th', 'phone': '+66 2 215 3555',
            'address': '254 Phayathai Rd, Wang Mai, Pathum Wan, Bangkok 10330, Thailand',
        },
        'mahidol': {
            'name': 'Mahidol University', 'country': 'Thailand', 'location': 'Bangkok, Thailand', 'ranking': 'World Rank: #256',
            'established': '1888', 'total_students': '33,000', 'international_students': '4%', 'student_faculty_ratio': '14:1',
            'overview': 'Mahidol University is a public research university in Thailand, originally established as a medical school.',
            'requirements': 'High School Diploma, IELTS 6.0+ or TOEFL 79+',
            'deadline': 'March 15 (Undergraduate)', 'tuition': 'THB 60,000 - THB 180,000 per year', 'living_costs': 'THB 10,000 - THB 15,000 per month',
            'scholarships': 'Mahidol University Scholarship, Thai Government Scholarship',
            'website': 'https://www.mahidol.ac.th', 'admission_email': 'inter.mu@mahidol.ac.th', 'phone': '+66 2 849 6230',
            'address': '999 Phutthamonthon 4 Rd, Salaya, Phutthamonthon, Nakhon Pathom 73170, Thailand',
        },
        'chiang-mai': {
            'name': 'Chiang Mai University', 'country': 'Thailand', 'location': 'Chiang Mai, Thailand', 'ranking': 'World Rank: #601-650',
            'established': '1964', 'total_students': '35,000', 'international_students': '3%', 'student_faculty_ratio': '16:1',
            'overview': 'Chiang Mai University is a public research university in northern Thailand and a leading institution in the region.',
            'requirements': 'High School Diploma, IELTS 5.5+ or TOEFL 61+',
            'deadline': 'April 30 (Undergraduate)', 'tuition': 'THB 40,000 - THB 120,000 per year', 'living_costs': 'THB 8,000 - THB 12,000 per month',
            'scholarships': 'Chiang Mai University Scholarship, Thai Government Scholarship',
            'website': 'https://www.cmu.ac.th', 'admission_email': 'inter@cmu.ac.th', 'phone': '+66 53 941 000',
            'address': '239 Huay Kaew Rd, Suthep, Mueang Chiang Mai District, Chiang Mai 50200, Thailand',
        },
        'thammasat': {
            'name': 'Thammasat University', 'country': 'Thailand', 'location': 'Bangkok, Thailand', 'ranking': 'World Rank: #601-650',
            'established': '1934', 'total_students': '33,000', 'international_students': '2%', 'student_faculty_ratio': '18:1',
            'overview': 'Thammasat University is a public research university in Thailand, known for its social sciences and law programs.',
            'requirements': 'High School Diploma, IELTS 6.0+ or TOEFL 79+',
            'deadline': 'March 31 (Undergraduate)', 'tuition': 'THB 45,000 - THB 140,000 per year', 'living_costs': 'THB 10,000 - THB 15,000 per month',
            'scholarships': 'Thammasat University Scholarship, Thai Government Scholarship',
            'website': 'https://www.tu.ac.th', 'admission_email': 'inter@tu.ac.th', 'phone': '+66 2 613 3333',
            'address': '2 Prachan Rd, Phra Borom Maha Ratchawang, Phra Nakhon, Bangkok 10200, Thailand',
        },

        # ========== NORWAY UNIVERSITIES ==========
        'oslo': {
            'name': 'University of Oslo', 'country': 'Norway', 'location': 'Oslo, Norway', 'ranking': 'World Rank: #119',
            'established': '1811', 'total_students': '28,000', 'international_students': '15%', 'student_faculty_ratio': '12:1',
            'overview': 'The University of Oslo is a public research university and the oldest university in Norway.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'December 1 (Undergraduate)', 'tuition': 'No tuition fees (only semester fee of NOK 600)', 'living_costs': 'NOK 10,000 - NOK 15,000 per month',
            'scholarships': 'Quota Scheme, Erasmus+',
            'website': 'https://www.uio.no', 'admission_email': 'international@uio.no', 'phone': '+47 22 85 50 50',
            'address': 'Problemveien 7, 0313 Oslo, Norway',
        },
        'bergen': {
            'name': 'University of Bergen', 'country': 'Norway', 'location': 'Bergen, Norway', 'ranking': 'World Rank: #199',
            'established': '1946', 'total_students': '18,000', 'international_students': '11%', 'student_faculty_ratio': '12:1',
            'overview': 'The University of Bergen is a public university located in Bergen, Norway. The university today serves approximately 18,000 students.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'December 1 (Undergraduate)', 'tuition': 'No tuition fees (only semester fee of NOK 590)', 'living_costs': 'NOK 9,000 - NOK 13,000 per month',
            'scholarships': 'Quota Scheme, Erasmus+',
            'website': 'https://www.uib.no', 'admission_email': 'post@uib.no', 'phone': '+47 55 58 00 00',
            'address': 'Postboks 7800, 5020 Bergen, Norway',
        },
        'ntnu': {
            'name': 'Norwegian University of Science and Technology', 'country': 'Norway', 'location': 'Trondheim, Norway', 'ranking': 'World Rank: #352',
            'established': '1760', 'total_students': '40,000', 'international_students': '10%', 'student_faculty_ratio': '14:1',
            'overview': 'NTNU is a public research university in Norway with the main campus in Trondheim.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'December 1 (Undergraduate)', 'tuition': 'No tuition fees (only semester fee of NOK 580)', 'living_costs': 'NOK 9,000 - NOK 13,000 per month',
            'scholarships': 'Quota Scheme, Erasmus+',
            'website': 'https://www.ntnu.no', 'admission_email': 'opptak@ntnu.no', 'phone': '+47 73 59 50 00',
            'address': 'Høgskoleringen 1, 7034 Trondheim, Norway',
        },
        'tromso': {
            'name': 'University of Tromsø', 'country': 'Norway', 'location': 'Tromsø, Norway', 'ranking': 'World Rank: 401-500',
            'established': '1968', 'total_students': '17,000', 'international_students': '11%', 'student_faculty_ratio': '13:1',
            'overview': 'The University of Tromsø is a public research university located in the city of Tromsø, Norway.',
            'requirements': 'High School Diploma, IELTS 6.5+ or TOEFL 90+',
            'deadline': 'December 1 (Undergraduate)', 'tuition': 'No tuition fees (only semester fee of NOK 590)', 'living_costs': 'NOK 8,000 - NOK 12,000 per month',
            'scholarships': 'Quota Scheme, Erasmus+',
            'website': 'https://en.uit.no', 'admission_email': 'international@uit.no', 'phone': '+47 77 64 40 00',
            'address': 'Hansine Hansens veg 18, 9019 Tromsø, Norway',
        },

        # ========== MALAYSIA UNIVERSITIES ==========
        'malaya': {
            'name': 'University of Malaya', 'country': 'Malaysia', 'location': 'Kuala Lumpur, Malaysia', 'ranking': 'World Rank: #65',
            'established': '1905', 'total_students': '27,000', 'international_students': '13%', 'student_faculty_ratio': '15:1',
            'overview': 'The University of Malaya is a public research university and the oldest and most comprehensive university in Malaysia.',
            'requirements': 'High School Diploma, IELTS 5.5+ or TOEFL 550+',
            'deadline': 'June 30 (Undergraduate)', 'tuition': 'MYR 15,000 - MYR 35,000 per year', 'living_costs': 'MYR 1,000 - MYR 1,500 per month',
            'scholarships': 'UM Scholarship, Malaysian Government Scholarship',
            'website': 'https://www.um.edu.my', 'admission_email': 'study@um.edu.my', 'phone': '+60 3 7967 3272',
            'address': 'Jalan Universiti, 50603 Kuala Lumpur, Malaysia',
        },
        'ukm': {
            'name': 'Universiti Kebangsaan Malaysia', 'country': 'Malaysia', 'location': 'Bangi, Malaysia', 'ranking': 'World Rank: #129',
            'established': '1970', 'total_students': '25,000', 'international_students': '8%', 'student_faculty_ratio': '16:1',
            'overview': 'UKM is a public research university located in Bandar Baru Bangi, Selangor.',
            'requirements': 'High School Diploma, IELTS 5.5+ or TOEFL 500+',
            'deadline': 'June 15 (Undergraduate)', 'tuition': 'MYR 12,000 - MYR 30,000 per year', 'living_costs': 'MYR 900 - MYR 1,300 per month',
            'scholarships': 'UKM Scholarship, Malaysian Government Scholarship',
            'website': 'https://www.ukm.my', 'admission_email': 'hepa@ukm.edu.my', 'phone': '+60 3 8921 5555',
            'address': '43600 UKM Bangi, Selangor, Malaysia',
        },
        'usm': {
            'name': 'Universiti Sains Malaysia', 'country': 'Malaysia', 'location': 'Penang, Malaysia', 'ranking': 'World Rank: #143',
            'established': '1969', 'total_students': '30,000', 'international_students': '7%', 'student_faculty_ratio': '14:1',
            'overview': 'USM is a public research university in Malaysia. Founded in 1969, it is one of the oldest universities in northern Malaysia.',
            'requirements': 'High School Diploma, IELTS 5.5+ or TOEFL 500+',
            'deadline': 'June 20 (Undergraduate)', 'tuition': 'MYR 13,000 - MYR 32,000 per year', 'living_costs': 'MYR 800 - MYR 1,200 per month',
            'scholarships': 'USM Scholarship, Malaysian Government Scholarship',
            'website': 'https://www.usm.my', 'admission_email': 'registry@usm.my', 'phone': '+60 4 653 3888',
            'address': '11800 USM, Penang, Malaysia',
        },
        'upm': {
            'name': 'Universiti Putra Malaysia', 'country': 'Malaysia', 'location': 'Serdang, Malaysia', 'ranking': 'World Rank: #143',
            'established': '1931', 'total_students': '28,000', 'international_students': '6%', 'student_faculty_ratio': '15:1',
            'overview': 'UPM is a public research university in Serdang, Selangor, Malaysia. It was originally established as a school of agriculture.',
            'requirements': 'High School Diploma, IELTS 5.5+ or TOEFL 500+',
            'deadline': 'June 25 (Undergraduate)', 'tuition': 'MYR 14,000 - MYR 33,000 per year', 'living_costs': 'MYR 850 - MYR 1,300 per month',
            'scholarships': 'UPM Scholarship, Malaysian Government Scholarship',
            'website': 'https://www.upm.edu.my', 'admission_email': 'pro@upm.edu.my', 'phone': '+60 3 9769 7777',
            'address': '43400 UPM Serdang, Selangor, Malaysia',
        },
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
        {'code': 'australia', 'name': 'Australia', 'flag': '🇦🇺', 'description': 'Top-ranked universities in beautiful locations'},
        {'code': 'germany', 'name': 'Germany', 'flag': '🇩🇪', 'description': 'Tuition-free education at public universities'},
        {'code': 'china', 'name': 'China', 'flag': '🇨🇳', 'description': 'Rapidly growing universities with scholarships'},
        {'code': 'india', 'name': 'India', 'flag': '🇮🇳', 'description': 'Affordable quality education in diverse fields'},
        {'code': 'turkey', 'name': 'Turkey', 'flag': '🇹🇷', 'description': 'Bridge between Europe and Asia with English programs'},
        {'code': 'netherlands', 'name': 'Netherlands', 'flag': '🇳🇱', 'description': 'English-taught programs in innovative environment'},
        {'code': 'thailand', 'name': 'Thailand', 'flag': '🇹🇭', 'description': 'Affordable tropical study destination'},
        {'code': 'norway', 'name': 'Norway', 'flag': '🇳🇴', 'description': 'Free tuition at public universities for all students'},
        {'code': 'malaysia', 'name': 'Malaysia', 'flag': '🇲🇾', 'description': 'Quality education at low cost in Southeast Asia'},
    ]
    
    context = {'countries': countries}
    return render(request, 'global_agency/all_countries.html', context)
def tcu_services(request):
    """
    Render TCU services page showing how GASE helps students with TCU processes
    """
    tcu_services_data = {
        'overview': {
            'title': 'TCU Services Through GASE',
            'description': 'GASE partners with Tanzania Commission for Universities to simplify and expedite official education services for students.',
            'mission': 'To make TCU services accessible and efficient for all students',
            'vision': 'Seamless education services for local and international students'
        },
        'services': [
            {
                'category': 'Student Mobility Services',
                'icon': '🌍',
                'color': 'blue',
                'services': [
                    {
                        'title': 'Program Transfer',
                        'description': 'Transfer between universities with TCU approval and credit recognition.',
                        'we_help': [
                            {
                                'title': 'Prepare and verify documents',
                                'description': 'We ensure all transfer documents are complete and properly formatted before submission'
                            },
                            {
                                'title': 'Evaluate credit transfers',
                                'description': 'We help assess which credits will transfer and ensure proper recognition'
                            },
                            {
                                'title': 'Expedite TCU processing',
                                'description': 'We use our partnership to speed up approval and reduce waiting times'
                            }
                        ],
                        'duration': '2-4 weeks',
                        'fee': 'TZS 30,000'
                    },
                    {
                        'title': 'University Exchange',
                        'description': 'Support for national and international university exchange programs.',
                        'we_help': [
                            {
                                'title': 'Coordinate applications',
                                'description': 'We manage all application steps and ensure requirements are met on time'
                            },
                            {
                                'title': 'Arrange visa and accommodation',
                                'description': 'We provide guidance on visa requirements and help find suitable housing'
                            },
                            {
                                'title': 'Process TCU approvals',
                                'description': 'We handle all TCU documentation and ensure smooth approval process'
                            }
                        ],
                        'duration': '1-3 weeks',
                        'fee': 'TZS 25,000'
                    }
                ]
            },
            {
                'category': 'Verification Services',
                'icon': '📄',
                'color': 'green',
                'services': [
                    {
                        'title': 'Certificate Verification',
                        'description': 'Official verification of academic certificates for employment or further studies.',
                        'we_help': [
                            {
                                'title': 'Authenticate documents',
                                'description': 'We verify certificate authenticity and ensure they meet TCU standards'
                            },
                            {
                                'title': 'Speed up processing',
                                'description': 'We use direct channels to reduce verification time significantly'
                            },
                            {
                                'title': 'Ensure secure delivery',
                                'description': 'We provide safe and tracked delivery of verified certificates to you'
                            }
                        ],
                        'duration': '2-4 weeks',
                        'fee': 'TZS 50,000'
                    },
                    {
                        'title': 'Foreign Qualification Recognition',
                        'description': 'TCU recognition of foreign qualifications for use in Tanzania.',
                        'we_help': [
                            {
                                'title': 'Translate documents',
                                'description': 'We provide official translation services for foreign language certificates'
                            },
                            {
                                'title': 'Assess equivalence',
                                'description': 'We evaluate how foreign qualifications match Tanzanian education standards'
                            },
                            {
                                'title': 'Navigate the process',
                                'description': 'We guide you through complex recognition procedures step by step'
                            }
                        ],
                        'duration': '4-6 weeks',
                        'fee': 'TZS 100,000'
                    }
                ]
            },
            {
                'category': 'Admission Support',
                'icon': '🎓',
                'color': 'purple',
                'services': [
                    {
                        'title': 'Study Abroad Approval',
                        'description': 'TCU approval for Tanzanian students pursuing education overseas.',
                        'we_help': [
                            {
                                'title': 'Verify documents',
                                'description': 'We check all required documents meet TCU standards before submission'
                            },
                            {
                                'title': 'Process approvals',
                                'description': 'We handle the entire approval process with TCU on your behalf'
                            },
                            {
                                'title': 'Monitor status',
                                'description': 'We provide regular updates on your application progress and timeline'
                            }
                        ],
                        'duration': '3-5 weeks',
                        'fee': 'TZS 75,000'
                    },
                    {
                        'title': 'Accreditation Verification',
                        'description': 'Verify TCU accreditation status of universities and programs.',
                        'we_help': [
                            {
                                'title': 'Access TCU database',
                                'description': 'We directly check accreditation status through our TCU partnership'
                            },
                            {
                                'title': 'Generate official reports',
                                'description': 'We provide certified accreditation reports for your records'
                            },
                            {
                                'title': 'Guide institution selection',
                                'description': 'We recommend accredited alternatives if your chosen institution isn\'t approved'
                            }
                        ],
                        'duration': '1-2 weeks',
                        'fee': 'TZS 20,000'
                    }
                ]
            }
        ],
        'contact_info': {
            'website': 'https://www.gase-agency.com',
            'email': 'tcu-services@gase-agency.com',
            'phone': '+255 123 456 789',
            'address': 'Global Agency Services, Dar es Salaam, Tanzania',
            'working_hours': 'Monday - Friday: 8:00 AM - 5:00 PM'
        },
        'important_links': [
            {'name': 'GASE Website', 'url': 'https://www.gase-agency.com', 'icon': '🌐'},
            {'name': 'TCU Official Website', 'url': 'https://www.tcu.go.tz', 'icon': '🏛️'},
            {'name': 'Service Application', 'url': '#', 'icon': '📝'},
            {'name': 'Status Check', 'url': '#', 'icon': '🔍'}
        ]
    }
    
    context = {'tcu_data': tcu_services_data}
    return render(request, 'global_agency/tcu_services.html', context)