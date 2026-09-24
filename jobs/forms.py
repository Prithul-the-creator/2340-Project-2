from django import forms

from accounts.models import Skill

from .models import (
    Application,
    ApplicationStatus,
    EmploymentType,
    Job,
    JobStatus,
    SalaryUnit,
    SavedSearch,
    VisaSponsorship,
    WorkModel,
)


class JobForm(forms.ModelForm):
    skills_text = forms.CharField(
        required=False,
        help_text='Comma-separated required skills',
        widget=forms.TextInput(attrs={'class': 'field'}),
    )

    class Meta:
        model = Job
        fields = [
            'title',
            'company',
            'location',
            'work_model',
            'employment_type',
            'description',
            'responsibilities',
            'qualifications',
            'salary_min',
            'salary_max',
            'salary_unit',
            'visa_sponsorship',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'field'}),
            'company': forms.TextInput(attrs={'class': 'field'}),
            'location': forms.TextInput(attrs={'class': 'field'}),
            'work_model': forms.Select(attrs={'class': 'field'}),
            'employment_type': forms.Select(attrs={'class': 'field'}),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 5}),
            'responsibilities': forms.Textarea(
                attrs={'class': 'field', 'rows': 4}
            ),
            'qualifications': forms.Textarea(
                attrs={'class': 'field', 'rows': 4}
            ),
            'salary_min': forms.NumberInput(attrs={'class': 'field'}),
            'salary_max': forms.NumberInput(attrs={'class': 'field'}),
            'salary_unit': forms.Select(attrs={'class': 'field'}),
            'visa_sponsorship': forms.Select(attrs={'class': 'field'}),
            'status': forms.Select(attrs={'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_model'].choices = WorkModel.choices
        self.fields['employment_type'].choices = EmploymentType.choices
        self.fields['salary_unit'].choices = SalaryUnit.choices
        self.fields['visa_sponsorship'].choices = VisaSponsorship.choices
        self.fields['status'].choices = JobStatus.choices
        if self.instance and self.instance.pk:
            self.fields['skills_text'].initial = ', '.join(
                self.instance.skills.values_list('name', flat=True)
            )

    def save(self, commit=True):
        job = super().save(commit=commit)
        if commit:
            self._save_skills(job)
        return job

    def _save_skills(self, job):
        raw = self.cleaned_data.get('skills_text', '')
        names = [n.strip() for n in raw.split(',') if n.strip()]
        skills = []
        for name in names:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills.append(skill)
        job.skills.set(skills)


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['note']
        widgets = {
            'note': forms.Textarea(
                attrs={
                    'class': 'field',
                    'rows': 4,
                    'maxlength': 500,
                    'placeholder': 'Optional note to the recruiter (max 500 characters)',
                }
            ),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = ApplicationStatus.choices


class SavedSearchForm(forms.ModelForm):
    class Meta:
        model = SavedSearch
        fields = ['name', 'notify_email', 'notify_in_app']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field'}),
            'notify_email': forms.CheckboxInput(attrs={'class': 'h-4 w-4 accent-[#2563EB]'}),
            'notify_in_app': forms.CheckboxInput(attrs={'class': 'h-4 w-4 accent-[#2563EB]'}),
        }
