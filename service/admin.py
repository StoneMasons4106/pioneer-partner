from django.contrib import admin
from .models import Call, ReturnVisit, Territory, Street, NHRecord, DoNotCall
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


class TerritoryAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'territory_id',
        'congregation',
        'status',
    )

    fields = (
        'number',
        'congregation',
        'status',
        'assigned_to',
        'signed_out',
        'last_completed',
        'map',
    )

    ordering = ('congregation',)


class StreetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'territory',
    )

    fields = (
        'name',
        'territory',
    )

    ordering = (
        'territory',
    )


class NHRecordAdmin(admin.ModelAdmin):
    list_display = (
        'number',
        'street',
    )

    fields = (
        'number',
        'street',
    )

    ordering = (
        'street',
    )


class DoNotCallAdmin(admin.ModelAdmin):
    list_display = (
        'address',
        'territory',
    )

    fields = (
        'address',
        'territory',
        'notes',
    )

    ordering = (
        'territory',
    )


admin.site.register(Call, CallAdmin)
admin.site.register(ReturnVisit, ReturnVisitAdmin)
admin.site.register(Territory, TerritoryAdmin)
admin.site.register(Street, StreetAdmin)
admin.site.register(NHRecord, NHRecordAdmin)
admin.site.register(DoNotCall, DoNotCallAdmin)
