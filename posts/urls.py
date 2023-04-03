from django.urls import path
from . import views

urlpatterns = [
    path('add_like/', views.add_like, name='add_like'),
    path('remove_like/', views.remove_like, name='remove_like'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('add_bookmark/', views.add_bookmark, name='add_bookmark'),
    path('remove_bookmark/', views.remove_bookmark, name='remove_bookmark'),
    path('add/', views.add_post, name='add_post'),
    path('edit/<str:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<str:post_id>/', views.delete_post, name='delete_post'),
    path('<str:post_id>/', views.post, name='post'),
]