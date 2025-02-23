

def current_user_context(request):
    return {
        'current_user': request.user,
        'message_notification': request.user.message_notifications.filter(is_read=False).count()
    }

