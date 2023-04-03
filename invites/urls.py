from django.urls import path
from . import views

urlpatterns = [
    path('', views.invites, name='invites'),
    path('delete/<str:invite_code>/', views.delete_invite, name='delete_invite'),
    path('add/<int:congregation_id>/', views.add_invite, name='add_invite')
]