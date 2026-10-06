from .models import Cart, Notification


def unread_notifications(request):
    if not request.user.is_authenticated:
        return {}
    return {'unread_notification_count': Notification.objects.filter(recruiter=request.user, is_read=False).count()}


def cart_count(request):
    if not request.user.is_authenticated:
        return {}
    return {'cart_count': Cart.objects.filter(user=request.user).count()}
