from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe

RECRUITER_PERMS = ['view_application', 'change_application']

def get_recruiter_group():
    group, _ = Group.objects.get_or_create(name='Recruiter')
    group.permissions.add(*Permission.objects.filter(
        content_type__app_label='jobs', codename__in=RECRUITER_PERMS))
    return group

class CustomErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return mark_safe(''.join([f'<div class="alert alert-danger" role="alert">{e}</div>' for e in self]))

class CustomUserCreationForm(UserCreationForm):
    account_type = forms.ChoiceField(
        choices=[('applicant', 'Applicant'), ('recruiter', 'Recruiter')],
        initial='applicant',
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs.update( {'class': 'form-control'} )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and self.cleaned_data['account_type'] == 'recruiter':
            user.groups.add(get_recruiter_group())
        return user
