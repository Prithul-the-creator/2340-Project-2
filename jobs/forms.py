from django import forms

from .models import Application, Job


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['note']
        widgets = {
            'note': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'rows': 2,
                'maxlength': 1000,
                'placeholder': 'Add a short note about why this role interests you',
                'required': True,
            }),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company', 'description', 'skills_needed', 'location',
            'employment_type', 'salary', 'remote_work', 'visa_sponsorship',
        ]
        labels = {
            'salary': 'Pay',
            'remote_work': 'Remote role',
            'visa_sponsorship': 'Visa sponsorship offered',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control mb-2',
                'rows': 4, 'required': True}),
            'skills_needed': forms.TextInput(attrs={
                'class': 'form-control mb-2',
                'placeholder': 'Separate skills with commas'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control mb-2'
            }),
            'employment_type': forms.Select(attrs={
                'class': 'form-select mb-2'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control mb-2',
                'step': '1',
                'min': '0'
            }),
            'remote_work': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visa_sponsorship': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
