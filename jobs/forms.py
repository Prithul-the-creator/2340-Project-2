from django import forms

from .models import Application


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
