from django.contrib import admin
from .models import Congregation, ServiceGroup, ServiceMeeting
from address.forms import AddressField
from address.forms import AddressWidget

# Register your models here.

class CongregationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'congregation_id',
    )

    fields = (
        'name',
        'address',
        'number',
    )

    ordering = ('congregation_id',)

    formfield_overrides = {AddressField: {"widget": AddressWidget(attrs={"style": "width: 300px; height: 100px;"})}}


class ServiceGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'congregation',
        'service_group_id'
    )

    fields = (
        'name',
        'congregation',
        'service_location',
    )

    ordering = ('congregation',)


class ServiceMeetingAdmin(admin.ModelAdmin):
    list_display = (
        'day',
        'time',
        'congregation',
    )

    fields = (
        'day',
        'time',
        'congregation',
        'service_group',
        'service_location',
    )

    ordering = ('congregation',)


admin.site.register(Congregation, CongregationAdmin)
admin.site.register(ServiceGroup, ServiceGroupAdmin)
admin.site.register(ServiceMeeting, ServiceMeetingAdmin)