from django import template


register = template.Library()


@register.filter
def unread_messages(user):
    return user.message_notifications.filter(is_read=False).count()

