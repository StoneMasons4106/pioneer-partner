from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
import os
import requests

# Create your views here.

@login_required
def cart_shifts(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    token = os.environ.get('JUSTACART_TOKEN')
    shifts = requests.get(f'https://imjustacart.com/api/shifts?token={token}&email={request.user.email}')

    if "ERROR" in shifts.text:
        shifts = {}
    elif shifts.json():
        shifts = shifts.json()['data']
    else:
        shifts = {}

    context = {
        'profile': profile,
        'shifts': shifts,
        'title': 'Pioneer Partner - My Cart Shifts',
    }

    return render(request, 'service/cart_shifts.html', context)


@login_required
def cart_shift(request, shift_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    token = os.environ.get('JUSTACART_TOKEN')
    shifts = requests.get(f'https://imjustacart.com/api/shifts?token={token}&email={request.user.email}')

    for shift in shifts.json()['data']:
        if int(shift['Schedule']['id']) == shift_id:
            correct_shift = shift
            break

    context = {
        'profile': profile,
        'shift': correct_shift,
        'title': f'Pioneer Partner - Cart Shift - {shift_id}',
    }

    return render(request, 'service/cart_shift.html', context)