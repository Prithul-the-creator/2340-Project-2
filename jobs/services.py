from django.core.mail import send_mail
from django.db.models import Q
from django.utils import timezone

from accounts.models import AccountStatus, Privacy, Profile, Role

from .models import Notification, SavedSearch, WorkModel


FILTER_LABELS = {
    'q': 'Keyword',
    'skills': 'Skills',
    'location': 'Location',
    'school': 'School',
    'graduation_year': 'Graduation year',
    'projects': 'Projects',
}


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
    return {k: request.GET.get(k, '').strip() for k in FILTER_LABELS}


def describe_filters(filters):
    return [
        (label, filters[key])
        for key, label in FILTER_LABELS.items()
        if filters.get(key)
    ]


def rank_candidates(queryset, filters):
    # Every result already matches every filter, so rank by evidence: searched
    # skills used in real projects first, then fuller profiles, then newest.
    terms = [
        s.strip().lower()
        for s in (filters.get('skills') or '').split(',')
        if s.strip()
    ]
    ranked = []
    for profile in queryset.prefetch_related('projects__skills').order_by('-updated_at'):
        projects = profile.projects.all()
        project_skills = {
            skill.name.lower() for project in projects for skill in project.skills.all()
        }
        shown_in_projects = sum(
            1 for term in terms if any(term in name for name in project_skills)
        )
        completeness = (
            bool(profile.headline)
            + bool(profile.educations.all())
            + bool(projects)
        )
        ranked.append((shown_in_projects * 3 + completeness, profile))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [profile for _, profile in ranked]


def matching_profile_ids(search):
    queryset = filter_candidates(
        visible_seeker_queryset(search.recruiter), search.filters or {}
    )
    return list(queryset.values_list('pk', flat=True))


def recommend_candidates_for_job(job, limit=5):
    # Skill rows are created per spelling, so compare names case-insensitively.
    job_skills = {
        name.lower(): name for name in job.skills.values_list('name', flat=True)
    }
    job_location = (job.location or '').lower().strip()
    if job.work_model == WorkModel.REMOTE:
        job_location = ''
    already_applied = job.applications.values_list('seeker_id', flat=True)
    dismissed = job.dismissed_recommendations.values_list('profile_id', flat=True)
    candidates = (
        visible_seeker_queryset(job.owner)
        .exclude(user_id__in=already_applied)
        .exclude(pk__in=dismissed)
        .prefetch_related('projects__skills')
    )

    scored = []
    for profile in candidates:
        reasons = []
        profile_skills = {skill.name.lower() for skill in profile.skills.all()}
        overlap = sorted(job_skills[k] for k in job_skills.keys() & profile_skills)
        if overlap:
            reasons.append(
                f'Has {len(overlap)} of {len(job_skills)} required skills: '
                + ', '.join(overlap[:5])
            )
        project_skills = {
            skill.name.lower()
            for project in profile.projects.all()
            for skill in project.skills.all()
        }
        project_hits = sorted(
            job_skills[k] for k in job_skills.keys() & project_skills
        )
        if project_hits:
            reasons.append(
                'Project experience with: ' + ', '.join(project_hits[:4])
            )
        near = False
        if job_location and profile.location:
            location = profile.location.lower()
            near = job_location in location or location in job_location
            if near:
                reasons.append(f'Located near {job.location}')
        if not reasons:
            continue
        score = len(overlap) * 3 + len(project_hits) * 2 + (1 if near else 0)
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

    # seen_profile_ids holds everyone a search has already surfaced (the
    # matches at save time plus earlier alerts), so only new matches alert.
    searches = SavedSearch.objects.select_related('recruiter')

    for search in searches:
        if profile.pk in search.seen_profile_ids:
            continue
        visible = visible_seeker_queryset(search.recruiter).filter(pk=profile.pk)
        if not visible.exists():
            continue
        if not _profile_matches_filters(profile, search.filters or {}):
            continue

        search.seen_profile_ids = [*search.seen_profile_ids, profile.pk]
        update_fields = ['seen_profile_ids']
        message = (
            f'New candidate match for “{search.name}”: '
            f'{profile.display_name}'
        )
        link = f'/candidates/{profile.pk}/'

        if search.notify_in_app:
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

        if search.notify_in_app or search.notify_email:
            search.last_notified_at = timezone.now()
            update_fields.append('last_notified_at')
        search.save(update_fields=update_fields)
