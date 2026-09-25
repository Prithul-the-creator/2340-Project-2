from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import get_profile, require_role
from .forms import (
    AdminUserUpdateForm,
    CustomErrorList,
    CustomUserCreationForm,
    EducationForm,
    ExperienceForm,
    LinkForm,
    PrivacyForm,
    ProfileBasicsForm,
    ProjectForm,
)
from .models import (
    AccountStatus,
    Education,
    Experience,
    Link,
    Privacy,
    Profile,
    Project,
    Role,
    skills_from_text,
)
from jobs.services import check_saved_searches_for_profile


@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')


def login(request):
    template_data = {'title': 'Log in'}
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})

    user = authenticate(
        request,
        username=request.POST.get('username'),
        password=request.POST.get('password'),
    )
    if user is None:
        template_data['error'] = 'The username or password is incorrect.'
        return render(request, 'accounts/login.html', {'template_data': template_data})

    profile = get_profile(user)
    if profile.status == AccountStatus.SUSPENDED:
        template_data['error'] = 'Your account has been suspended.'
        return render(request, 'accounts/login.html', {'template_data': template_data})

    auth_login(request, user)
    return redirect('home.index')


def signup(request):
    template_data = {'title': 'Sign up'}
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html', {'template_data': template_data})

    form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account created. You can log in now.')
        return redirect('accounts.login')

    template_data['form'] = form
    return render(request, 'accounts/signup.html', {'template_data': template_data})


@login_required
def profile_view(request):
    profile = get_profile(request.user)
    template_data = {
        'title': 'Profile',
        'profile': profile,
        'is_owner': True,
    }
    return render(request, 'accounts/profile.html', {'template_data': template_data})


@login_required
def profile_edit(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = ProfileBasicsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            if profile.role == Role.SEEKER:
                check_saved_searches_for_profile(profile)
            messages.success(request, 'Profile updated.')
            return redirect('accounts.profile')
    else:
        form = ProfileBasicsForm(instance=profile)

    template_data = {
        'title': 'Edit profile',
        'form': form,
        'profile': profile,
        'education_form': EducationForm(),
        'experience_form': ExperienceForm(),
        'project_form': ProjectForm(),
        'link_form': LinkForm(),
    }
    return render(request, 'accounts/profile_edit.html', {'template_data': template_data})


@login_required
def education_add(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            edu = form.save(commit=False)
            edu.profile = profile
            edu.save()
            if profile.role == Role.SEEKER:
                check_saved_searches_for_profile(profile)
            messages.success(request, 'Education added.')
    return redirect('accounts.profile_edit')


@login_required
def education_delete(request, pk):
    profile = get_profile(request.user)
    edu = get_object_or_404(Education, pk=pk, profile=profile)
    if request.method == 'POST':
        edu.delete()
        messages.success(request, 'Education removed.')
    return redirect('accounts.profile_edit')


@login_required
def experience_add(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            exp = form.save(commit=False)
            exp.profile = profile
            exp.save()
            messages.success(request, 'Experience added.')
    return redirect('accounts.profile_edit')


@login_required
def experience_delete(request, pk):
    profile = get_profile(request.user)
    exp = get_object_or_404(Experience, pk=pk, profile=profile)
    if request.method == 'POST':
        exp.delete()
        messages.success(request, 'Experience removed.')
    return redirect('accounts.profile_edit')


@login_required
def project_add(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.profile = profile
            project.save()
            project.skills.set(skills_from_text(form.cleaned_data.get('skills_text')))
            if profile.role == Role.SEEKER:
                check_saved_searches_for_profile(profile)
            messages.success(request, 'Project added.')
    return redirect('accounts.profile_edit')


@login_required
def project_delete(request, pk):
    profile = get_profile(request.user)
    project = get_object_or_404(Project, pk=pk, profile=profile)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project removed.')
    return redirect('accounts.profile_edit')


@login_required
def link_add(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = profile
            link.save()
            messages.success(request, 'Link added.')
    return redirect('accounts.profile_edit')


@login_required
def link_delete(request, pk):
    profile = get_profile(request.user)
    link = get_object_or_404(Link, pk=pk, profile=profile)
    if request.method == 'POST':
        link.delete()
        messages.success(request, 'Link removed.')
    return redirect('accounts.profile_edit')


@login_required
def privacy_settings(request):
    profile = get_profile(request.user)
    if request.method == 'POST':
        form = PrivacyForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if profile.role == Role.SEEKER:
                check_saved_searches_for_profile(profile)
            messages.success(request, 'Privacy settings updated.')
            return redirect('accounts.privacy')
    else:
        form = PrivacyForm(instance=profile)

    template_data = {
        'title': 'Privacy settings',
        'form': form,
        'profile': profile,
        'privacy_help': {
            Privacy.PUBLIC_RECRUITERS: 'Recruiters can find and view your profile in candidate search.',
            Privacy.APPLICATIONS_ONLY: 'Only recruiters for jobs you apply to can see your profile.',
            Privacy.PRIVATE: 'Your profile is hidden from all recruiters.',
        },
    }
    return render(request, 'accounts/privacy.html', {'template_data': template_data})


@require_role(Role.ADMIN)
def manage_users(request):
    users = (
        User.objects.select_related('profile')
        .order_by('-date_joined')
    )
    template_data = {
        'title': 'Manage users',
        'users': users,
    }
    return render(request, 'accounts/manage_users.html', {'template_data': template_data})


@require_role(Role.ADMIN)
def manage_user_detail(request, user_id):
    target = get_object_or_404(User.objects.select_related('profile'), pk=user_id)
    profile = get_profile(target)

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST)
        if form.is_valid():
            new_role = form.cleaned_data['role']
            new_status = form.cleaned_data['status']
            if target == request.user and new_status == AccountStatus.SUSPENDED:
                messages.error(request, 'You cannot suspend your own account.')
            elif target == request.user and new_role != Role.ADMIN:
                messages.error(request, 'You cannot remove your own admin role.')
            else:
                profile.role = new_role
                profile.status = new_status
                profile.save()
                if new_role == Role.ADMIN:
                    target.is_staff = True
                    target.save(update_fields=['is_staff'])
                messages.success(request, f'Updated {target.username}.')
                return redirect('accounts.manage_users')
    else:
        form = AdminUserUpdateForm(
            initial={'role': profile.role, 'status': profile.status}
        )

    template_data = {
        'title': f'User · {target.username}',
        'target': target,
        'profile': profile,
        'form': form,
    }
    return render(
        request, 'accounts/manage_user_detail.html', {'template_data': template_data}
    )


@require_role(Role.ADMIN)
def manage_roles(request):
    template_data = {
        'title': 'Roles',
        'roles': [
            {
                'name': 'Job Seeker',
                'code': Role.SEEKER,
                'description': 'Create a profile, search and apply to jobs, track applications, and control privacy.',
            },
            {
                'name': 'Recruiter',
                'code': Role.RECRUITER,
                'description': 'Post jobs, search candidates, review applications, save searches, and receive recommendations.',
            },
            {
                'name': 'Administrator',
                'code': Role.ADMIN,
                'description': 'Manage users and roles, suspend accounts, and keep the platform fair and safe.',
            },
        ],
    }
    return render(request, 'accounts/manage_roles.html', {'template_data': template_data})
