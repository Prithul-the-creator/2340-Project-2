from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from accounts.models import AccountStatus, Privacy, Profile, Role

from .models import Notification, SavedSearch


def visible_seeker_queryset(recruiter_user=None):
    qs = (
        Profile.objects.filter(role=Role.SEEKER, status=AccountStatus.ACTIVE)
        .exclude(privacy=Privacy.PRIVATE)
        .select_related('user')
        .prefetch_related('skills', 'projects', 'educations')
    )
    if recruiter_user is None:
        return qs.filter(privacy=Privacy.PUBLIC_RECRUITERS)

    public = Q(privacy=Privacy.PUBLIC_RECRUITERS)
    applied = Q(
        privacy=Privacy.APPLICATIONS_ONLY,
        user__applications__job__owner=recruiter_user,
    )
    return qs.filter(public | applied).distinct()


def filter_candidates(queryset, filters):
    q = (filters.get('q') or '').strip()
    skills = (filters.get('skills') or '').strip()
    location = (filters.get('location') or '').strip()
    school = (filters.get('school') or '').strip()
    graduation_year = (filters.get('graduation_year') or '').strip()
    projects = (filters.get('projects') or '').strip()

    if q:
        queryset = queryset.filter(
            Q(user__first_name__icontains=q)
            | Q(user__last_name__icontains=q)
            | Q(user__username__icontains=q)
            | Q(headline__icontains=q)
            | Q(bio__icontains=q)
        )
    if location:
        queryset = queryset.filter(location__icontains=location)
    if skills:
        for skill in [s.strip() for s in skills.split(',') if s.strip()]:
            queryset = queryset.filter(skills__name__icontains=skill)
    if school:
        queryset = queryset.filter(educations__school__icontains=school)
    if graduation_year.isdigit():
        queryset = queryset.filter(educations__graduation_year=int(graduation_year))
    if projects:
        queryset = queryset.filter(
            Q(projects__name__icontains=projects)
            | Q(projects__description__icontains=projects)
        )
    return queryset.distinct()


def filters_from_request(request):
    keys = [
        'q',
        'skills',
        'location',
        'school',
        'graduation_year',
        'projects',
    ]
    return {k: request.GET.get(k, '').strip() for k in keys}


def recommend_candidates_for_job(job, limit=5):
    job_skills = set(job.skills.values_list('name', flat=True))
    job_location = (job.location or '').lower().strip()
    candidates = visible_seeker_queryset(job.owner)
    already_applied = job.applications.values_list('seeker_id', flat=True)
    candidates = candidates.exclude(user_id__in=already_applied)

    scored = []
    for profile in candidates:
        reasons = []
        profile_skills = set(profile.skills.values_list('name', flat=True))
        overlap = job_skills & profile_skills
        if overlap:
            reasons.append(
                'Skills in common: ' + ', '.join(sorted(overlap)[:5])
            )
        project_overlap = set()
        for project in profile.projects.all():
            project_overlap |= set(project.skills.values_list('name', flat=True))
        project_hits = job_skills & project_overlap
        if project_hits:
            reasons.append(
                'Project experience with: ' + ', '.join(sorted(project_hits)[:4])
            )
        if job_location and profile.location:
            if job_location in profile.location.lower() or profile.location.lower() in job_location:
                reasons.append(f'Located near {job.location}')
        if not reasons:
            continue
        score = len(overlap) * 3 + len(project_hits) * 2 + (
            1 if any('Located' in r for r in reasons) else 0
        )
        scored.append((score, profile, reasons))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [
        {'profile': profile, 'reasons': reasons}
        for _, profile, reasons in scored[:limit]
    ]


def _profile_matches_filters(profile, filters):
    qs = Profile.objects.filter(pk=profile.pk)
    return filter_candidates(qs, filters).exists()


def check_saved_searches_for_profile(profile):
    if profile.role != Role.SEEKER:
        return
    if profile.privacy == Privacy.PRIVATE:
        return

    searches = SavedSearch.objects.filter(
        Q(notify_in_app=True) | Q(notify_email=True)
    ).select_related('recruiter')

    for search in searches:
        visible = visible_seeker_queryset(search.recruiter).filter(pk=profile.pk)
        if not visible.exists():
            continue
        if not _profile_matches_filters(profile, search.filters or {}):
            continue

        message = (
            f'New candidate match for “{search.name}”: '
            f'{profile.display_name}'
        )
        link = f'/candidates/{profile.pk}/'

        if search.notify_in_app:
            exists = Notification.objects.filter(
                user=search.recruiter,
                notification_type='saved_search',
                link=link,
                message=message,
            ).exists()
            if not exists:
                Notification.objects.create(
                    user=search.recruiter,
                    notification_type='saved_search',
                    message=message,
                    link=link,
                )

        if search.notify_email and search.recruiter.email:
            send_mail(
                subject=f'Seekr: new match for {search.name}',
                message=message + f'\nView: {link}',
                from_email=None,
                recipient_list=[search.recruiter.email],
                fail_silently=True,
            )

        search.last_notified_at = timezone.now()
        search.save(update_fields=['last_notified_at'])
