from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import AccountStatus, Profile, Role


def get_profile(user):
    if not user.is_authenticated:
        return None
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            'role': Role.ADMIN if user.is_superuser else Role.SEEKER,
        },
    )
    return profile


def require_role(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            profile = get_profile(request.user)
            if profile.status == AccountStatus.SUSPENDED:
                messages.error(request, 'Your account has been suspended.')
                return redirect('accounts.logout')
            if profile.role not in roles and not (
                request.user.is_superuser and Role.ADMIN in roles
            ):
                messages.error(request, 'You do not have access to that page.')
                return redirect('home.index')
            request.profile = profile
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


def block_suspended(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = get_profile(request.user)
            if profile.status == AccountStatus.SUSPENDED:
                messages.error(request, 'Your account has been suspended.')
                return redirect('accounts.logout')
            request.profile = profile
        return view_func(request, *args, **kwargs)

    return _wrapped
