from django import forms
from .models import ContactMessage, StudentApplication

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'destination', 'message']


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = '__all__'
        widgets = {
            # Personal Information
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'nationality': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Tanzanian'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '255712345678'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Your residential address'
            }),
            
            # Parents Details
            'father_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Father\'s full name'
            }),
            'father_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '255712345678'
            }),
            'father_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'father@example.com'
            }),
            'father_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Teacher, Engineer'
            }),
            'mother_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mother\'s full name'
            }),
            'mother_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '255712345678'
            }),
            'mother_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'mother@example.com'
            }),
            'mother_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Nurse, Business Owner'
            }),
            
            # O-Level
            'olevel_school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'School name'
            }),
            'olevel_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tanzania'
            }),
            'olevel_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'School address'
            }),
            'olevel_region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Region'
            }),
            'olevel_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2020'
            }),
            'olevel_candidate_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'S1234/2020/0001'
            }),
            'olevel_gpa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3.5 or Division I'
            }),
            
            # A-Level
            'alevel_school': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'School name'
            }),
            'alevel_country': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tanzania'
            }),
            'alevel_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'School address'
            }),
            'alevel_region': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Region'
            }),
            'alevel_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2022'
            }),
            'alevel_candidate_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'S1234/2022/0001'
            }),
            'alevel_gpa': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 3.5 or Division I'
            }),
            
            # Preferences
            'preferred_country_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First choice country'
            }),
            'preferred_country_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Second choice country'
            }),
            'preferred_country_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Third choice country'
            }),
            'preferred_country_4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fourth choice country'
            }),
            'preferred_program_1': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First choice program'
            }),
            'preferred_program_2': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Second choice program'
            }),
            'preferred_program_3': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Third choice program'
            }),
            'preferred_program_4': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Fourth choice program'
            }),
            
            # Emergency Contact
            'emergency_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Emergency contact name'
            }),
            'emergency_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Emergency contact address'
            }),
            'emergency_occupation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Doctor, Teacher'
            }),
            'emergency_gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'emergency_relation': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Uncle, Aunt, Guardian'
            }),
            'heard_about_us': forms.Select(attrs={
                'class': 'form-control'
            }),
            'heard_about_other': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please specify'
            }),
        }
