from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from profiles.models import UserProfile
from django.contrib.auth.models import User
from django.http.response import HttpResponse
import requests
import urllib
from django.contrib import messages
from .models import Call, ReturnVisit, Territory, Street, NHRecord, DoNotCall
from .forms import AddCall, AddReturnVisit, AddStreet, AddTerritory, AddDoNotCall
from datetime import date
import json

# Create your views here.

def congregation_admin_check(user):
    response = False
    
    groups = user.groups.all()
    for group in groups:
        if group.name == 'Congregation Admin':
            response = True
        else:
            continue

    return response


@login_required
def cart_shifts(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    token = profile.congregation.justacart_token
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
    token = profile.congregation.justacart_token
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
    call = get_object_or_404(Call, call_id=str(call_id).zfill(16))
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
    call = get_object_or_404(Call, call_id=str(call_id).zfill(16))

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
    call = get_object_or_404(Call, call_id=str(call_id).zfill(16))

    if request.method == "POST":
        form = AddReturnVisit(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.call = get_object_or_404(Call, call_id=str(call_id).zfill(16))
            instance.save()
            messages.success(request, 'Return visit added successfully.')
            return redirect('call', call_id=str(call_id).zfill(16))
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
            return redirect('call', call_id=str(call_id).zfill(16))
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

    return redirect('call', call_id=str(call_id).zfill(16))


@login_required
def delete_call(request, call_id):

    if len(str(call_id)) != 16:
        call_id = str(call_id).zfill(16)
    
    call = get_object_or_404(Call, call_id=call_id)
    call.delete()
    messages.success(request, 'Call has been successfully been deleted.')

    return redirect('calls')


@login_required
def my_territories(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    territories = Territory.objects.filter(status='2', assigned_to=request.user)

    context = {
        'profile': profile,
        'territories': territories,
        'title': 'Pioneer Partner - My Territories',
    }

    return render(request, 'service/my_territories.html', context)


@login_required
def my_territory(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    do_not_calls = DoNotCall.objects.filter(territory=territory)

    if request.method == "POST":
        territory.status = '1'
        territory.assigned_to = None
        territory.last_completed = date.today()
        territory.save()
        nh_records = Street.objects.filter(territory=territory)
        nh_records.delete()
        messages.success(request, 'Territory has been marked complete!')
        return redirect('my_territories')

    context = {
        'profile': profile,
        'territory': territory,
        'do_not_calls': do_not_calls,
        'title': 'Pioneer Partner - My Territory',
    }

    return render(request, 'service/my_territory.html', context)


@login_required
def nh_records(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    streets = Street.objects.filter(territory=territory)

    context = {
        'profile': profile,
        'territory': territory,
        'streets': streets,
        'title': 'Pioneer Partner - NH Records',
    }

    return render(request, 'service/nh_records.html', context)


@login_required
def add_nh_record(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))

    if request.method == 'POST':
        form = AddStreet(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.territory = territory
            instance.save()
            messages.success(request, 'NH Record added successfully!')
            return redirect('nh_records', territory_id=str(territory_id).zfill(16))
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddStreet()

    context = {
        'profile': profile,
        'territory': territory,
        'form': form,
        'title': 'Pioneer Partner - Add NH Record',
    }

    return render(request, 'service/add_nh_record.html', context)


@login_required
def nh_record(request, territory_id, street_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    street = get_object_or_404(Street, pk=street_id)
    houses = NHRecord.objects.filter(street=street)

    if request.method == "POST":
        data = request.body.decode('ascii', 'replace')
        cleaned_data = urllib.parse.unquote(data, encoding='utf-8', errors='replace').replace("+", " ")
        house_number_split = cleaned_data.split('form[1][value]=')[1]
        house_number = house_number_split.split('&')[0]
        house = NHRecord(number=int(house_number), street=street)
        house.save()
        data = {"house_id": house.id}
        return HttpResponse(json.dumps(data, indent=4), content_type="application/json")

    context = {
        'profile': profile,
        'territory': territory,
        'street': street,
        'houses': houses,
        'title': 'Pioneer Partner - NH Record',
    }

    return render(request, 'service/nh_record.html', context)


@login_required
def delete_nh_record(request, territory_id, street_id):

    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    street = get_object_or_404(Street, pk=street_id)
    street.delete()
    messages.success(request, 'NH record has been deleted.')
    return redirect('nh_records', territory_id=str(territory.territory_id).zfill(16))


@login_required
def delete_house_record(request, territory_id, street_id, house_id):

    if request.method == "POST":
        data = request.body.decode('ascii', 'replace')
        cleaned_data = urllib.parse.unquote(data, encoding='utf-8', errors='replace').replace("+", " ")
        house_id = cleaned_data.split('form[3][value]=')[1]
        house = get_object_or_404(NHRecord, pk=house_id)
        house.delete()
        return HttpResponse(200)
    

@login_required
def congregation_territories(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    congregation = profile.congregation
    territories = Territory.objects.filter(congregation=congregation, status="1").order_by("last_completed")[:5]

    context = {
        'profile': profile,
        'territories': territories,
        'groups': request.user.groups.all(),
        'title': 'Pioneer Partner - Congregation Territories',
    }

    return render(request, 'service/congregation_territories.html', context)


@login_required
def congregation_territory(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    do_not_calls = DoNotCall.objects.filter(territory=territory)

    if request.method == "POST":
        territory.assigned_to = request.user
        territory.status = '2'
        territory.signed_out = date.today()
        territory.save()
        messages.success(request, 'Territory has been successfully signed out.')
        return redirect('my_territory', territory_id=str(territory_id).zfill(16))

    context = {
        'profile': profile,
        'groups': request.user.groups.all(),
        'territory': territory,
        'do_not_calls': do_not_calls,
        'title': 'Pioneer Partner - Congregation Territory',
    }

    return render(request, 'service/congregation_territory.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation_territories/')
def add_territory(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AddTerritory(profile.congregation, request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.congregation = profile.congregation
            if instance.assigned_to:
                instance.status = '2'
                instance.signed_out = date.today()
            else:
                instance.status = '1'
            instance.save()
            messages.success(request, 'Territory added successfully.')
            return redirect('congregation_territories')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddTerritory(profile.congregation)

    context = {
        'profile': profile,
        'form': form,
        'title': 'Pioneer Partner - Add Territory',
    }

    return render(request, 'service/add_territory.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation_territories/')
def edit_territory(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))

    if request.method == 'POST':
        form = AddTerritory(profile.congregation, request.POST, request.FILES, instance=territory)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.congregation = profile.congregation
            instance.save()
            messages.success(request, 'Territory edited successfully.')
            return redirect('congregation_territory', territory_id=str(territory_id).zfill(16))
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddTerritory(profile.congregation, instance=territory)

    context = {
        'profile': profile,
        'groups': request.user.groups.all(),
        'territory': territory,
        'form': form,
        'title': 'Pioneer Partner - Edit Territory',
    }

    return render(request, 'service/edit_territory.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation_territories/')
def delete_territory(request, territory_id):

    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    territory.delete()
    messages.success(request, 'Territory has been deleted.')
    return redirect('congregation_territories')


@login_required
def do_not_call(request, territory_id, do_not_call_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    do_not_call = get_object_or_404(DoNotCall, pk=do_not_call_id)

    context = {
        'profile': profile,
        'territory': territory,
        'do_not_call': do_not_call,
        'title': 'Pioneer Partner - Do Not Call',
    }

    return render(request, 'service/do_not_call.html', context)


@login_required
def add_do_not_call(request, territory_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))

    if request.method == 'POST':
        form = AddDoNotCall(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.territory = territory
            instance.save()
            messages.success(request, 'Do not call added successfully.')
            if territory.assigned_to == request.user:
                return redirect('my_territory', territory_id=str(territory_id).zfill(16))
            else:
                return redirect('congregation_territory', territory_id=str(territory_id).zfill(16))
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddDoNotCall()

    context = {
        'profile': profile,
        'territory': territory,
        'form': form,
        'page': 'Edit Congregation',
        'title': 'Pioneer Partner - Add Do Not Call',
    }

    return render(request, 'service/add_do_not_call.html', context)


@login_required
def delete_do_not_call(request, territory_id, do_not_call_id):

    do_not_call = get_object_or_404(DoNotCall, pk=do_not_call_id)
    territory = get_object_or_404(Territory, territory_id=str(territory_id).zfill(16))
    do_not_call.delete()
    messages.success(request, 'Do not call has been removed.')
    if territory.assigned_to == request.user:
        return redirect('my_territory', territory_id=str(territory_id).zfill(16))
    else:
        return redirect('congregation_territory', territory_id=str(territory_id).zfill(16))