from django import template
from notifications.models import Notification

register = template.Library()

@register.filter(name='notifications')
def notifications(notifications):
    notifications = Notification.objects.filter(status='1')
    return notifications