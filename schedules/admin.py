from django.contrib import admin
from .models import RegularServiceDay, ScheduleRequest

# Register your models here.

class RegularServiceDayAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'day',
        'start_time',
        'end_time',
    )

    fields = (
        'user',
        'day',
        'start_time',
        'end_time',
        'congregation',
    )

    ordering = ('user',)


class ScheduleRequestAdmin(admin.ModelAdmin):
    list_display = (
        'request_id',
        'requesting_user',
        'to_user',
        'day',
    )

    fields = (
        'requesting_user',
        'to_user',
        'day',
        'start_time',
        'end_time',
        'notes',
        'confirmation',
        'confirmation_notes',
    )

    ordering = ('requesting_user',)


admin.site.register(RegularServiceDay, RegularServiceDayAdmin)
admin.site.register(ScheduleRequest, ScheduleRequestAdmin)