from django.urls import path
from . import views

urlpatterns = [
    path('cart_shifts/', views.cart_shifts, name='cart_shifts'),
    path('cart_shift/<int:shift_id>/', views.cart_shift, name='cart_shift'),
    path('calls/', views.calls, name='calls'),
    path('calls/add/', views.add_call, name='add_call'),
    path('calls/return_visit/add/<int:call_id>/', views.add_return_visit, name='add_return_visit'),
    path('call/<int:call_id>/', views.call, name='call'),
    path('delete_call/<int:call_id>/', views.delete_call, name='delete_call'),
    path('call/return_visit/edit/<int:call_id>/<int:return_visit_id>/', views.edit_return_visit, name='edit_return_visit'),
    path('call/return_visit/delete/<int:call_id>/<int:return_visit_id>/', views.delete_return_visit, name='delete_return_visit'),
]