from django.contrib import admin
from .models import Call, ReturnVisit
from address.forms import AddressField
from address.forms import AddressWidget

# Register your models here.

class CallAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'call_id',
        'user',
        'contact_date',
    )

    fields = (
        'user',
        'name',
        'gender',
        'age',
        'address',
        'notes',
    )

    ordering = ('user',)

    formfield_overrides = {AddressField: {"widget": AddressWidget(attrs={"style": "width: 300px; height: 100px;"})}}


class ReturnVisitAdmin(admin.ModelAdmin):
    list_display = (
        'call',
        'contact_date',
    )

    fields = (
        'notes',
    )

    ordering = ('call',)


admin.site.register(Call, CallAdmin)
admin.site.register(ReturnVisit, ReturnVisitAdmin)
