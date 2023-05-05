from django.urls import path
from . import views

urlpatterns = [
    path('cart_shifts/', views.cart_shifts, name='cart_shifts'),
    path('cart_shift/<int:shift_id>/', views.cart_shift, name='cart_shift'),
    path('calls/', views.calls, name='calls'),
]