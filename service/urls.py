from django.urls import path
from . import views

urlpatterns = [
    path('cart_shifts/', views.cart_shifts, name='cart_shifts'),
    path('cart_shift/<int:shift_id>/', views.cart_shift, name='cart_shift'),
    path('calls/', views.calls, name='calls'),
    path('calls/add/', views.add_call, name='add_call'),
    path('my_territories/', views.my_territories, name='my_territories'),
    path('calls/return_visit/add/<int:call_id>/', views.add_return_visit, name='add_return_visit'),
    path('call/<int:call_id>/', views.call, name='call'),
    path('my_territory/<int:territory_id>/', views.my_territory, name='my_territory'),
    path('my_territory/<int:territory_id>/nh_records/', views.nh_records, name='nh_records'),
    path('my_territory/<int:territory_id>/nh_records/<int:street_id>/', views.nh_record, name='nh_record'),
    path('my_territory/<int:territory_id>/nh_records/<int:street_id>/delete/', views.delete_nh_record, name='delete_nh_record'),
    path('my_territory/<int:territory_id>/nh_records/<int:street_id>/<int:house_id>/delete/', views.delete_house_record, name='delete_house_record'),
    path('my_territory/<int:territory_id>/add_nh_record/', views.add_nh_record, name='add_nh_record'),
    path('delete_call/<int:call_id>/', views.delete_call, name='delete_call'),
    path('call/transfer/<int:call_id>/', views.transfer_call, name='transfer_call'),
    path('call/return_visit/edit/<int:call_id>/<int:return_visit_id>/', views.edit_return_visit, name='edit_return_visit'),
    path('call/return_visit/delete/<int:call_id>/<int:return_visit_id>/', views.delete_return_visit, name='delete_return_visit'),
]