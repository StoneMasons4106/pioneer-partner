from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'notification_id',
        'user',
        'status',
        'type',
        'created',
    )

    fields = (
        'user',
        'info',
        'url',
        'status',
        'type',
    )

    ordering = ('notification_id',)


admin.site.register(Notification, NotificationAdmin)
