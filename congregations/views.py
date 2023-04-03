from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from profiles.models import UserProfile
from django.contrib.auth.decorators import login_required, user_passes_test
from invites.models import Invite
from .models import Congregation, ServiceGroup, ServiceMeeting
from django.contrib import messages
from datetime import datetime
from .forms import EditCongregationInfo, EditServiceGroupInfo, AddServiceGroup

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
def congregation(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    congregation_users = UserProfile.objects.filter(congregation=profile.congregation)
    active_invites = Invite.objects.filter(congregation=profile.congregation)
    service_groups = ServiceGroup.objects.filter(congregation=profile.congregation)
    number_of_users = len(congregation_users)
    number_of_invites = len(active_invites)
    number_of_service_groups = len(service_groups)

    maps_url = 'https://www.google.com/maps/place/'

    count = 0
    for word in profile.congregation.address.raw.split(' '):
        if count == 0:
            count = count + 1
            maps_url += word
        else:
            maps_url += f'+{word}'


    context = {
        'profile': profile,
        'congregation': profile.congregation,
        'congregation_users': congregation_users,
        'number_of_users': number_of_users,
        'number_of_invites': number_of_invites,
        'number_of_service_groups': number_of_service_groups,
        'maps_url': maps_url,
        'groups': request.user.groups.all(),
        'title': f'Pioneer Partner - Congregation - {profile.congregation.name}',
    }

    return render(request, 'congregations/congregation.html', context)


@login_required
def service_group(request, service_group_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_group = get_object_or_404(ServiceGroup, service_group_id=service_group_id)
    service_group_members = UserProfile.objects.filter(service_group=service_group)

    today = datetime.today().weekday()
    group_service_meetings = ServiceMeeting.objects.filter(service_group=service_group, day=today+1)

    maps_url = 'https://www.google.com/maps/place/'

    count = 0
    for word in service_group.service_location.raw.split(' '):
        if count == 0:
            count = count + 1
            maps_url += word
        else:
            maps_url += f'+{word}'

    context = {
        'profile': profile,
        'service_group': service_group,
        'service_group_members': service_group_members,
        'groups': request.user.groups.all(),
        'group_service_meetings': len(group_service_meetings),
        'maps_url': maps_url,
        'title': f'Pioneer Partner - Service Group - {service_group.name}',
    }

    return render(request, 'congregations/service_group.html', context)


@login_required
def service_meetings(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_meetings = ServiceMeeting.objects.filter(Q(service_group__isnull=True), congregation=profile.congregation)

    context = {
        'profile': profile,
        'service_meetings': service_meetings,
        'groups': request.user.groups.all(),
        'title': 'Pioneer Partner - Congregation Service Meetings',
    }

    return render(request, 'congregations/service_meetings.html', context)


@login_required
def group_service_meetings(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    group_service_meetings = ServiceMeeting.objects.filter(service_group=id)

    context = {
        'profile': profile,
        'service_meetings': group_service_meetings,
        'groups': request.user.groups.all(),
        'title': 'Pioneer Partner - Group Service Meetings',
    }

    return render(request, 'congregations/group_service_meetings.html', context)


@login_required
def service_meeting(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_meeting = get_object_or_404(ServiceMeeting, id=id)

    context = {
        'profile': profile,
        'service_meeting': service_meeting,
        'groups': request.user.groups.all(),
        'title': 'Pioneer Partner - Service Meeting',
    }

    return render(request, 'congregations/service_meeting.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def delete_service_meeting(request, id):

    service_meeting = get_object_or_404(ServiceMeeting, id=id)
    service_meeting.delete()
    messages.success(request, 'Service meeting has been deleted.')

    return redirect('service_meetings')


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def edit_congregation_info(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    congregation = get_object_or_404(Congregation, congregation_id=profile.congregation.congregation_id)

    if request.method == 'POST':
        form = EditCongregationInfo(request.POST, instance=congregation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congregation updated successfully.')
            return redirect('congregation')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = EditCongregationInfo(instance=congregation)

    context = {
        'profile': profile,
        'congregation': congregation,
        'form': form,
        'page': 'Edit Congregation',
        'title': f'Pioneer Partner - Edit Congregation - {congregation.name}',
    }

    return render(request, 'congregations/edit_congregation_info.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def edit_service_group_info(request, service_group_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_group = get_object_or_404(ServiceGroup, service_group_id=service_group_id)

    if request.method == 'POST':
        form = EditServiceGroupInfo(request.POST, instance=service_group)
        if form.is_valid():
            form.save()
            messages.success(request, 'Service group updated successfully.')
            return redirect('service_group')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = EditServiceGroupInfo(instance=service_group)

    context = {
        'profile': profile,
        'service_group': service_group,
        'groups': request.user.groups.all(),
        'form': form,
        'page': 'Edit Congregation',
        'title': f'Pioneer Partner - Edit Service Group - {service_group.name}',
    }

    return render(request, 'congregations/edit_service_group_info.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def service_groups(request):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    service_groups = ServiceGroup.objects.filter(congregation=profile.congregation)

    context = {
        'profile': profile,
        'service_groups': service_groups,
        'title': 'Pioneer Partner - Service Groups',
    }

    return render(request, 'congregations/service_groups.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def add_service_group(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = AddServiceGroup(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.congregation = profile.congregation
            instance.save()
            messages.success(request, 'Service group added successfully.')
            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = AddServiceGroup()

    context = {
        'profile': profile,
        'form': form,
        'page': 'Edit Congregation',
        'title': 'Pioneer Partner - Add Service Group',
    }

    return render(request, 'congregations/add_service_group.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def delete_service_group(request, service_group_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    service_group = get_object_or_404(ServiceGroup, service_group_id=service_group_id)
    service_groups = ServiceGroup.objects.filter(congregation=profile.congregation).exclude(service_group_id=service_group_id)

    if request.method == "POST":
        data = request.body.decode()
        id = int(data.split('service-group=')[1])
        new_group = get_object_or_404(ServiceGroup, service_group_id=id)
        users = UserProfile.objects.filter(service_group=service_group)
        for user in users:
            user.service_group = new_group
            user.save()
        service_group.delete()
        messages.success(request, 'Service group successfully deleted.')
        return redirect('service_groups')

    context = {
        'profile': profile,
        'service_group': service_group,
        'service_groups': service_groups,
        'title': 'Pioneer Partner - Delete Service Group',
    }

    return render(request, 'congregations/delete_service_group.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def add_service_meeting(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_groups = ServiceGroup.objects.filter(congregation=profile.congregation)
    form = AddServiceGroup()

    if request.method == "POST":
        new_service_meeting_info = request.body.decode().replace('%3A', ':').replace('%2C', ',').replace('+', ' ')

        day_split = new_service_meeting_info.split('day=')
        day = day_split[1].split('&')[0]
        
        time_split = new_service_meeting_info.split('time=')
        time = time_split[1].split('&')[0]

        try:
            service_group_split = new_service_meeting_info.split('service-group=')
            service_group = get_object_or_404(ServiceGroup, id=service_group_split[1].split('&')[0])
        except:
            service_group = None

        try:
            service_location_split = new_service_meeting_info.split('service-location=')
            service_location = service_location_split[1].split('&')[0]
        except:
            service_location = None

        if service_location:
            new_service_meeting = ServiceMeeting(day=day, time=time, congregation=profile.congregation, service_group=service_group, service_location=service_location)
            new_service_meeting.save()
        else:
            new_service_meeting = ServiceMeeting(day=day, time=time, congregation=profile.congregation, service_group=service_group)
            new_service_meeting.save()

        messages.success(request, 'New service meeting added.')
        return redirect('service_meetings')
    
    context = {
        'profile': profile,
        'service_groups': service_groups,
        'form': form,
        'page': 'Edit Congregation',
        'title': 'Pioneer Partner - Add Service Meeting',
    }

    return render(request, 'congregations/add_service_meeting.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def edit_service_meeting(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_meeting = get_object_or_404(ServiceMeeting, id=id)
    service_groups = ServiceGroup.objects.filter(congregation=profile.congregation)
    form = AddServiceGroup()

    if request.method == "POST":
        new_service_meeting_info = request.body.decode().replace('%3A', ':').replace('%2C', ',').replace('+', ' ')

        day_split = new_service_meeting_info.split('day=')
        day = day_split[1].split('&')[0]
        
        time_split = new_service_meeting_info.split('time=')
        time = time_split[1].split('&')[0]

        try:
            service_group_split = new_service_meeting_info.split('service-group=')
            service_group = get_object_or_404(ServiceGroup, id=service_group_split[1].split('&')[0])
        except:
            service_group = None

        try:
            service_location_split = new_service_meeting_info.split('service-location=')
            service_location = service_location_split[1].split('&')[0]
        except:
            service_location = None

        service_meeting.day = day
        service_meeting.time = time
        service_meeting.service_group = service_group
        if service_location:
            service_meeting.service_location = service_location
        service_meeting.save()

        messages.success(request, 'Service meeting edited successfully.')
        return redirect('service_meetings')
    
    context = {
        'profile': profile,
        'service_groups': service_groups,
        'service_meeting': service_meeting,
        'time': service_meeting.time.strftime('%H:%M:%S'),
        'form': form,
        'page': 'Edit Congregation',
        'title': 'Pioneer Partner - Edit Service Meeting',
    }

    return render(request, 'congregations/edit_service_meeting.html', context)