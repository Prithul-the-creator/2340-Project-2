from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


from .models import Profile
from .forms import ProfileForm


@login_required
def create_profile(req):
    profile, was_createdd = Profile.objects.get_or_create(user=req.user)
    if req.method == 'POST':
        form = ProfileForm(req.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('accounts.profile')
    else:
        form = ProfileForm(instance=profile)
    return render(req, 'profiles/create_profile.html', {'form': form})
