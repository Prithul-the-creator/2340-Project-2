from django.contrib.auth.forms import UserCreationForm
from django.forms.utils import ErrorList
from django import forms
from django.utils.safestring import mark_safe

from .models import (
    Education,
    Experience,
    Link,
    LinkType,
    Privacy,
    Profile,
    Project,
    Role,
    skills_from_text,
)


class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(
            ''.join(
                [
                    f'<div class="alert alert-danger" role="alert">{e}</div>'
                    for e in self
                ]
            )
        )


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (Role.SEEKER, 'I am looking for work'),
            (Role.RECRUITER, 'I am hiring'),
        ],
        widget=forms.RadioSelect,
        initial=Role.SEEKER,
    )
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
        ]:
            if fieldname in self.fields:
                self.fields[fieldname].help_text = None
                self.fields[fieldname].widget.attrs.update({'class': 'field'})
        self.fields['role'].widget.attrs.update({'class': 'h-4 w-4 accent-accent'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.role = self.cleaned_data['role']
            profile.save()
        return user


class ProfileBasicsForm(forms.ModelForm):
    skills_text = forms.CharField(
        required=False,
        help_text='Comma-separated skills (e.g. Python, React, SQL)',
        widget=forms.TextInput(attrs={'class': 'field'}),
    )

    class Meta:
        model = Profile
        fields = [
            'headline',
            'bio',
            'location',
            'avatar',
            'resume',
            'company',
            'company_website',
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'field'}),
            'bio': forms.Textarea(attrs={'class': 'field', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'field'}),
            'avatar': forms.ClearableFileInput(attrs={'class': 'field'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'field'}),
            'company': forms.TextInput(attrs={'class': 'field'}),
            'company_website': forms.URLInput(attrs={'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills_text'].initial = ', '.join(
                self.instance.skills.values_list('name', flat=True)
            )

    def save(self, commit=True):
        profile = super().save(commit=commit)
        if commit:
            self._save_skills(profile)
        return profile

    def _save_skills(self, profile):
        profile.skills.set(skills_from_text(self.cleaned_data.get('skills_text')))


class PrivacyForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['privacy']
        widgets = {
            'privacy': forms.RadioSelect,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['privacy'].choices = Privacy.choices


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['school', 'degree', 'field', 'graduation_year']
        widgets = {
            'school': forms.TextInput(attrs={'class': 'field'}),
            'degree': forms.TextInput(attrs={'class': 'field'}),
            'field': forms.TextInput(attrs={'class': 'field'}),
            'graduation_year': forms.NumberInput(attrs={'class': 'field'}),
        }


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = [
            'title',
            'company',
            'location',
            'start_date',
            'end_date',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'field'}),
            'company': forms.TextInput(attrs={'class': 'field'}),
            'location': forms.TextInput(attrs={'class': 'field'}),
            'start_date': forms.DateInput(
                attrs={'class': 'field', 'type': 'date'}
            ),
            'end_date': forms.DateInput(
                attrs={'class': 'field', 'type': 'date'}
            ),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 3}),
        }


class ProjectForm(forms.ModelForm):
    skills_text = forms.CharField(
        required=False,
        help_text='Comma-separated skills used in this project',
        widget=forms.TextInput(attrs={'class': 'field'}),
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'url']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'field'}),
            'description': forms.Textarea(attrs={'class': 'field', 'rows': 3}),
            'url': forms.URLInput(attrs={'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skills_text'].initial = ', '.join(
                self.instance.skills.values_list('name', flat=True)
            )

    def save(self, commit=True):
        project = super().save(commit=commit)
        if commit:
            project.skills.set(skills_from_text(self.cleaned_data.get('skills_text')))
        return project


class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ['link_type', 'url', 'label']
        widgets = {
            'link_type': forms.Select(attrs={'class': 'field'}),
            'url': forms.URLInput(attrs={'class': 'field'}),
            'label': forms.TextInput(attrs={'class': 'field'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['link_type'].choices = LinkType.choices


class AdminUserUpdateForm(forms.Form):
    role = forms.ChoiceField(
        choices=Role.choices, widget=forms.Select(attrs={'class': 'field'})
    )
    status = forms.ChoiceField(
        choices=[
            ('ACTIVE', 'Active'),
            ('SUSPENDED', 'Suspended'),
        ],
        widget=forms.Select(attrs={'class': 'field'}),
    )
