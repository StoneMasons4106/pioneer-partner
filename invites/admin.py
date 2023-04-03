from django.contrib import admin
from .models import Invite

# Register your models here.

class InviteAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'code',
        'congregation',
        'email',
    )

    fields = (
        'name',
        'congregation',
        'service_group',
        'email',
    )

    ordering = ('congregation',)

admin.site.register(Invite, InviteAdmin)