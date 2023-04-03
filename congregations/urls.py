from django.urls import path
from . import views

urlpatterns = [
    path('', views.congregation, name='congregation'),
    path('edit/', views.edit_congregation_info, name='edit_congregation_info'),
    path('service_groups/', views.service_groups, name='service_groups'),
    path('service_meetings/', views.service_meetings, name='service_meetings'),
    path('group_service_meetings/<int:id>/', views.group_service_meetings, name='group_service_meetings'),
    path('service_meeting/<int:id>/', views.service_meeting, name='service_meeting'),
    path('service_meeting/edit/<int:id>/', views.edit_service_meeting, name='edit_service_meeting'),
    path('service_meeting/delete/<int:id>/', views.delete_service_meeting, name='delete_service_meeting'),
    path('add_service_group/', views.add_service_group, name='add_service_group'),
    path('add_service_meeting/', views.add_service_meeting, name='add_service_meeting'),
    path('service_group/<int:service_group_id>/', views.service_group, name='service_group'),
    path('service_group/edit/<int:service_group_id>/', views.edit_service_group_info, name='edit_service_group_info'),
    path('service_group/delete/<int:service_group_id>/', views.delete_service_group, name='delete_service_group'),
]