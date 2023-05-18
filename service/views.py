from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from profiles.models import UserProfile
from django.contrib.auth.models import User
import os
import requests
from django.contrib import messages
from .models import Call, ReturnVisit
from .forms import AddCall, AddReturnVisit

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
    token = os.environ.get(f'JUSTACART_TOKEN_{profile.congregation.congregation_id}')
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
def call(request, call_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    call = get_object_or_404(Call, call_id=call_id)
    return_visits = ReturnVisit.objects.filter(call=call).order_by("-contact_date")

    if request.method == 'POST':
        form = AddCall(request.POST, instance=call)
        if form.is_valid():
            messages.success(request, 'Call updated successfully.')
            form.save()
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddCall(instance=call)

    context = {
        'profile': profile,
        'call': call,
        'form': form,
        'return_visits': return_visits,
        'title': 'Pioneer Partner - Call',
        'page': 'Edit Congregation',
    }

    return render(request, 'service/call.html', context)


@login_required
def add_call(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        form = AddCall(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            messages.success(request, 'Call added successfully.')
            return redirect('calls')
        else:
            messages.error(request, 'Request failed. Please ensure the form is valid.')
    else:
        form = AddCall()

    context = {
        'profile': profile,
        'page': 'Edit Congregation',
        'form': form,
        'title': 'Pioneer Partner - Add Call',
    }

    return render(request, 'service/add_call.html', context)


@login_required
def transfer_call(request, call_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    congregation_users = UserProfile.objects.filter(congregation=profile.congregation)
    users = [user for user in congregation_users if user.user != request.user]
    call = get_object_or_404(Call, call_id=call_id)

    if request.method == "POST":
        data = request.body.decode()
        username = data.split("user=")[1]
        user = get_object_or_404(User, username=username)
        call.user = user
        call.save()
        messages.success(request, 'Call has been successfully transferred.')
        return redirect('calls')

    context = {
        'profile': profile,
        'users': users,
        'call': call,
        'title': 'Pioneer Partner - Transfer Call',
    }

    return render(request, 'service/transfer_call.html', context)


@login_required
def add_return_visit(request, call_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    call = get_object_or_404(Call, call_id=call_id)

    if request.method == "POST":
        form = AddReturnVisit(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.call = get_object_or_404(Call, call_id=call_id)
            instance.save()
            messages.success(request, 'Return visit added successfully.')
            return redirect('call', call_id=call_id)
        else:
            messages.error(request, 'Request failed. Please ensure the form is valid.')
    else:
        form = AddReturnVisit()

    context = {
        'profile': profile,
        'call': call,
        'form': form,
        'title': 'Pioneer Partner - Add Return Visit',
    }

    return render(request, 'service/add_return_visit.html', context)


@login_required
def edit_return_visit(request, call_id, return_visit_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    rv = get_object_or_404(ReturnVisit, pk=return_visit_id)

    if request.method == 'POST':
        form = AddReturnVisit(request.POST, instance=rv)
        if form.is_valid():
            form.save()
            messages.success(request, 'Return visit updated successfully.')
            return redirect('call', call_id=call_id)
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddReturnVisit(instance=rv)

    context = {
        'profile': profile,
        'call_id': call_id,
        'return_visit': rv,
        'form': form,
        'title': 'Pioneer Partner - Edit Return Visit',
    }

    return render(request, 'service/edit_return_visit.html', context)


@login_required
def delete_return_visit(request, call_id, return_visit_id):
    
    rv = get_object_or_404(ReturnVisit, pk=return_visit_id)
    rv.delete()
    messages.success(request, 'Return visit has been successfully been deleted.')

    return redirect('call', call_id=call_id)


@login_required
def delete_call(request, call_id):

    if len(str(call_id)) != 16:
        call_id = str(call_id).zfill(16)
    
    call = get_object_or_404(Call, call_id=call_id)
    call.delete()
    messages.success(request, 'Call has been successfully been deleted.')

    return redirect('calls')