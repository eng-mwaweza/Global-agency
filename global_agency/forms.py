from django import forms
from .models import ContactMessage
class ContactForm(forms.ModelForm):
    class Meta:
        model=ContactMessage
        fields=['name','email','phone','message']

from .models import StudentApplication

class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows':2}),
            'emergency_address': forms.Textarea(attrs={'rows':2}),
            'heard_about_other': forms.TextInput(),
        }
        




