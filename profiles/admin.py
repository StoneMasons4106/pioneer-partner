from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'congregation',
    )

    fields = (
        'user',
        'bio',
        'location',
        'phone',
        'profile_picture',
        'service_group',
        'congregation',
        'liked_post_notifications',
        'comment_post_notifications',
    )

    ordering = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)