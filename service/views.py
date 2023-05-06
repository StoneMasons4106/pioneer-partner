from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
import os
import requests
from django.contrib import messages
from .models import Call

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


@login_required
def calls(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    calls = Call.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'calls': calls,
        'title': 'Pioneer Partner - Calls',
    }

    return render(request, 'service/calls.html', context)


@login_required
def delete_call(request, call_id):

    if len(str(call_id)) != 16:
        call_id = str(call_id).zfill(16)
    
    call = get_object_or_404(Call, call_id=call_id)
    call.delete()
    messages.success(request, 'Call has been successfully been deleted.')

    return redirect('calls')