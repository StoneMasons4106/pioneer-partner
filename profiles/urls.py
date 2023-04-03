from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.profile, name='profile'),
    path('<str:username>/', views.user_view, name='userview'),
    path('<str:username>/edit/', views.edit_user, name='edit_user'),
    path('<str:username>/cart_shift/<int:shift_id>/', views.cart_shift, name='user_cart_shift'),
    path('me/update_settings/', views.update_settings, name="update_settings"),
]