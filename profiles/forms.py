from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'headline', 'show_headline_to_recruiters',
            'location', 'show_location_to_recruiters',
            'skills', 'show_skills_to_recruiters',
            'education', 'show_education_to_recruiters',
            'work_experience', 'show_work_experience_to_recruiters',
            'projects', 'show_projects_to_recruiters',
            'links', 'show_links_to_recruiters',
        ]
        labels = {
            'show_headline_to_recruiters': 'Show headline to recruiters',
            'show_skills_to_recruiters': 'Show skills to recruiters',
            'show_education_to_recruiters': 'Show education to recruiters',
            'show_work_experience_to_recruiters': 'Show experience to recruiters',
            'show_links_to_recruiters': 'Show links to recruiters',
            'show_location_to_recruiters': 'Show location to recruiters',
            'show_projects_to_recruiters': 'Show projects to recruiters',
        }
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Python, writing, project management, etc.'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'links': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Please add only one link per line'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Atlanta, GA'}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Please add only one project per line'}),
            'show_headline_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_skills_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_education_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_work_experience_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_links_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_location_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'show_projects_to_recruiters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
