from accounts.decorators import get_profile
from accounts.models import Role
from jobs.models import Notification


def seekr_context(request):
    context = {
        'user_profile': None,
        'user_role': None,
        'unread_notification_count': 0,
        'Role': Role,
    }
    if request.user.is_authenticated:
        profile = get_profile(request.user)
        context['user_profile'] = profile
        context['user_role'] = profile.role
        context['unread_notification_count'] = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
    return context
