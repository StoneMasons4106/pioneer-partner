from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import RegularServiceDay, ScheduleRequest
from django.contrib import messages
from profiles.models import UserProfile
from notifications.models import Notification
import urllib
from django.contrib.auth.models import User
from .forms import ScheduleRequestForm
import os
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import requests


# Create your views here.

@login_required
def regular_days(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    regular_days = RegularServiceDay.objects.filter(user=request.user).order_by('day')

    context = {
        'profile': profile,
        'regular_days': regular_days,
        'title': 'Pioneer Partner - My Regular Days',
    }

    return render(request, 'schedules/regular_days.html', context)


@login_required
def delete_regular_day(request, id):

    regular_day = get_object_or_404(RegularServiceDay, pk=id)
    regular_day.delete()
    messages.success(request, 'Service day has been removed.')

    return redirect('regular_days')


@login_required
def edit_regular_day(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    regular_day = get_object_or_404(RegularServiceDay, pk=id)

    if request.method == "POST":
        updated_regular_day = request.body.decode().replace('%3A', ':')
        
        day_of_week_split = updated_regular_day.split('day-of-week=')
        day_of_week = day_of_week_split[1].split('&')[0]
        regular_day.day = day_of_week
        
        start_time_split = updated_regular_day.split('start-time=')
        start_time = start_time_split[1].split('&')[0]
        regular_day.start_time = start_time
        
        end_time_split = updated_regular_day.split('end-time=')
        end_time = end_time_split[1].split('&')[0]
        regular_day.end_time = end_time
        
        regular_day.save()
        
        messages.success(request, 'Day has been successfully edited!')
        return redirect('regular_days')

    context = {
        'profile': profile,
        'regular_day': regular_day,
        'title': 'Pioneer Partner - Edit Regular Day',
    }

    return render(request, 'schedules/edit_regular_day.html', context)


@login_required
def add_regular_day(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == "POST":
        new_regular_day_info = request.body.decode().replace('%3A', ':')

        day_of_week_split = new_regular_day_info.split('day-of-week=')
        day_of_week = day_of_week_split[1].split('&')[0]
        
        start_time_split = new_regular_day_info.split('start-time=')
        start_time = start_time_split[1].split('&')[0]
        
        end_time_split = new_regular_day_info.split('end-time=')
        end_time = end_time_split[1].split('&')[0]

        new_regular_day = RegularServiceDay(user=request.user, day=day_of_week, start_time=start_time, end_time=end_time, congregation=profile.congregation)
        new_regular_day.save()

        messages.success(request, 'New regular service day added!')
        return redirect('regular_days')

    context = {
        'profile': profile,
        'title': 'Pioneer Partner - Add Regular Day',
    }

    return render(request, 'schedules/add_regular_day.html', context)


@login_required
def whos_out_when_im_out(request):

    my_service_days = RegularServiceDay.objects.filter(user=request.user).order_by('day')
    profile = get_object_or_404(UserProfile, user=request.user)

    my_days = []
    common_service_days = []

    for day in my_service_days:
        if day.day in my_days:
            pass
        else:
            my_days.append(day.get_day_display)

        common_service_day = RegularServiceDay.objects.filter(day=day.day, end_time__gte=day.start_time, start_time__lte=day.end_time, congregation=profile.congregation)
        for object in common_service_day:
            if object.user != request.user:
                common_service_days.append(object)

    context = {
        'common_service_days': common_service_days,
        'profile': profile,
        'title': "Pioneer Partner - Who's Out When I'm Out",
    }
    
    return render(request, 'schedules/whos_out_when_im_out.html', context)


@login_required
def congregation_view(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    service_days = RegularServiceDay.objects.filter(congregation=profile.congregation)

    congregation_service_days = []
    for day in service_days:
        if day.user != request.user:
            congregation_service_days.append(day)

    context = {
        'profile': profile,
        'congregation_service_days': congregation_service_days,
        'title': 'Pioneer Partner - Congregation View',
    }

    return render(request, 'schedules/congregation_view.html', context)


@login_required
def schedule_requests(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    schedule_request_incoming = ScheduleRequest.objects.filter(to_user=request.user, confirmation=None)
    schedule_request_incoming_filtered = []
    if schedule_request_incoming:
        for object in schedule_request_incoming:
            past = object.check_date()
            if past:
                pass
            else:
                schedule_request_incoming_filtered.append(object)
    
    schedule_request_outgoing = ScheduleRequest.objects.filter(requesting_user=request.user, confirmation=None)
    schedule_request_outgoing_filtered = []
    if schedule_request_outgoing:
        for object in schedule_request_outgoing:
            past = object.check_date()
            if past:
                pass
            else:
                schedule_request_outgoing_filtered.append(object)
    
    confirmed = ScheduleRequest.objects.filter(to_user=request.user, confirmation='2') | ScheduleRequest.objects.filter(requesting_user=request.user, confirmation='2')
    confirmed_filtered = []
    if confirmed:
        for object in confirmed:
            past = object.check_date()
            if past:
                pass
            else:
                confirmed_filtered.append(object)

    context = {
        'profile': profile,
        'schedule_request_incoming': schedule_request_incoming_filtered,
        'schedule_request_outgoing': schedule_request_outgoing_filtered,
        'confirmed': confirmed_filtered,
        'title': 'Pioneer Partner - Schedule Requests',
    }

    return render(request, 'schedules/schedule_requests.html', context)


@login_required
def schedule_request(request, request_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    schedule_request = get_object_or_404(ScheduleRequest, request_id=str(request_id).zfill(16))

    if request.method == "POST":
        form = ScheduleRequestForm(request.POST, instance=schedule_request)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule request responded to successfully.')
            return redirect('schedule_requests')
    else:
        form = ScheduleRequestForm(instance=schedule_request)

    context = {
        'profile': profile,
        'schedule_request': schedule_request,
        'form': form,
        'title': 'Pioneer Partner - Schedule Request',
    }

    return render(request, 'schedules/schedule_request.html', context)


@login_required
def request_to_work_together(request, username):

    profile = get_object_or_404(UserProfile, user=request.user)
    to_user = get_object_or_404(User, username=username)

    if request.method == "POST":
        new_schedule_request_data = request.body.decode().replace('%3A', ':')

        day_split = new_schedule_request_data.split('day=')
        day = day_split[1].split('&')[0]

        start_time_split = new_schedule_request_data.split('start-time=')
        start_time = start_time_split[1].split('&')[0]
        
        end_time_split = new_schedule_request_data.split('end-time=')
        end_time = end_time_split[1].split('&')[0]

        notes_split = new_schedule_request_data.split('notes=')
        try:
            notes = urllib.parse.unquote(notes_split[1].split('&')[0], encoding='utf-8', errors='replace').replace("+", " ")
        except:
            notes = ''

        new_schedule_request = ScheduleRequest(requesting_user=request.user, to_user=to_user, day=day, start_time=start_time, end_time=end_time, notes=notes)
        new_schedule_request.save()

        hostname = os.environ.get('MY_HOSTNAME')
        new_notification = Notification(user=to_user, info=f'{request.user} would like to work with you on {day} from {start_time} to {end_time}. Please respond to this scheduling request at your convenience.', url=f'{hostname}schedule/schedule_request/{new_schedule_request.request_id}', status='1', type='1')
        new_notification.save()

        request_notification_message = render_to_string(
            'schedules/emails/notification.txt', {
                'name': new_notification.user,
                'my_hostname': os.environ.get('MY_HOSTNAME'),
                'notification_url': new_notification.url,
                'notification_type': new_notification.get_type_display()
                }
        )

        request_notification_message_wrapper = EmailMessage(
            f'New Notification: {new_notification.get_type_display()}',
            request_notification_message,
            to=[new_notification.user.email]
        )

        request_notification_message_wrapper.send()

        if to_user.first_name and to_user.last_name:
            messages.success(request, f'Successfully requested to work with {to_user.first_name} {to_user.last_name}')
        else:
            messages.success(request, f'Successfully requested to work with {username}')
        return redirect('userview', username=username)

    context = {
        'profile': profile,
        'username': username,
        'to_user': to_user,
        'title': 'Pioneer Partner - Request to Work Together',
    }

    return render(request, 'schedules/schedule_request_form.html', context)
