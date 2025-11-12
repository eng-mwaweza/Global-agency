from django import forms
from .models import StudentProfile, Application, Document

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'nationality', 'emergency_contact', 'profile_picture']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['application_type', 'university_name', 'course', 'country']
        widgets = {
            'university_name': forms.TextInput(attrs={'placeholder': 'Enter university name'}),
            'course': forms.TextInput(attrs={'placeholder': 'Enter course/program'}),
            'country': forms.TextInput(attrs={'placeholder': 'Enter country'}),
        }

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['document_type', 'file', 'description']