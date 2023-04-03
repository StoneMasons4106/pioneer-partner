from django.urls import path
from . import views

urlpatterns = [
    path('regular_days/', views.regular_days, name='regular_days'),
    path('regular_days/delete/<int:id>/', views.delete_regular_day, name='delete_regular_day'),
    path('regular_days/edit/<int:id>/', views.edit_regular_day, name='edit_regular_day'),
    path('regular_days/add/', views.add_regular_day, name='add_regular_day'),
    path('whos_out_when_im_out/', views.whos_out_when_im_out, name='whos_out_when_im_out'),
    path('congregation_view/', views.congregation_view, name='congregation_view'),
    path('request/<str:username>/', views.request_to_work_together, name='request_to_work_together'),
    path('schedule_request/<str:request_id>/', views.schedule_request, name='schedule_request'),
    path('schedule_requests/', views.schedule_requests, name='schedule_requests'),
]