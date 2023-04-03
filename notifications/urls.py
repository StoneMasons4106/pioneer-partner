from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.all_notifications, name='all_notifications'),
    path('new/', views.new_notifications, name='new_notifications'),
    path('mark_all_read/', views.mark_all_read, name='mark_all_read'),
    path('mark_read/<str:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]