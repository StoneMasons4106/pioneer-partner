"""loudspeaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from profiles.views import CustomPasswordChangeView
from exception import handler404, handler500, handler400, handler403
import os
from django.views.generic.base import RedirectView

hostname = os.environ.get('MY_HOSTNAME')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/password/change/', CustomPasswordChangeView.as_view(), name='account_password_change'),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', RedirectView.as_view(url=f'{hostname}dashboard/'), name='dashboard-redirect'),
    path('', include('pwa.urls')),
    path('profile/', include('profiles.urls')),
    path('posts/', include('posts.urls')),
    path('congregation/', include('congregations.urls')),
    path('schedule/', include('schedules.urls')),
    path('invites/', include('invites.urls')),
    path('notifications/', include('notifications.urls')),
    path('bug/', include('bugs.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
