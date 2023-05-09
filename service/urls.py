from django.urls import path
from . import views

urlpatterns = [
    path('cart_shifts/', views.cart_shifts, name='cart_shifts'),
    path('cart_shift/<int:shift_id>/', views.cart_shift, name='cart_shift'),
    path('calls/', views.calls, name='calls'),
    path('calls/add/', views.add_call, name='add_call'),
    path('call/<int:call_id>', views.call, name='call'),
    path('delete_call/<int:call_id>', views.delete_call, name='delete_call'),
]