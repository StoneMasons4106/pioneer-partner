from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from posts.models import Post
from profiles.models import UserProfile
from congregations.models import ServiceMeeting
from django.db.models import Q
from schedules.models import RegularServiceDay
from datetime import datetime, date, timedelta
import requests
import os

# Create your views here.

@login_required
def dashboard(request):
    '''A view to return the main dashboard'''

    profile = get_object_or_404(UserProfile, user=request.user)
    posts = Post.objects.filter(Q(comment__isnull=True), congregation=profile.congregation).order_by("-created")[:20]
    
    my_hour_data = []
    congregation_hour_data = []
    regular_days = RegularServiceDay.objects.filter(user=request.user)
    congregation_days = RegularServiceDay.objects.filter(congregation=profile.congregation)

    for day in range(1, 8):
        if regular_days:
            sum = 0
            regular_day = RegularServiceDay.objects.filter(id__in=regular_days, day=day)
            if regular_day:
                for object in regular_day:
                    time_diff = datetime.combine(date.today(), object.end_time) - datetime.combine(date.today(), object.start_time)
                    time_diff_delta = time_diff / timedelta(hours=1)
                    sum += time_diff_delta
                my_hour_data.append(sum)
            else:
               my_hour_data.append(0) 
        else:
            my_hour_data.append(0)

        if congregation_days:
            sum = 0
            congregation_day = RegularServiceDay.objects.filter(id__in=congregation_days, day=day)
            if congregation_day:
                for object in congregation_day:
                    time_diff = datetime.combine(date.today(), object.end_time) - datetime.combine(date.today(), object.start_time)
                    time_diff_delta = time_diff / timedelta(hours=1)
                    sum += time_diff_delta
                congregation_hour_data.append(sum)
            else:
               congregation_hour_data.append(0) 
        else:
            congregation_hour_data.append(0)    
        
    
    filter_regular_days = RegularServiceDay.objects.filter(day=datetime.today().weekday()+1, congregation=profile.congregation).distinct("user")
    filtered_regular_days = []
    for day in filter_regular_days:
        if day.user != request.user:
            filtered_regular_days.append(day)


    today = datetime.today().weekday()
    congregation_service_meetings = ServiceMeeting.objects.filter(Q(service_group__isnull=True), congregation=profile.congregation, day=today+1)
    weather_api_key = os.environ.get('WEATHER_API_KEY')

    if profile.location:
        try:
            current_weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={profile.location}').json()
        except:
            current_weather = {}
    else:
        try:
            ipapi_request = requests.get(f'https://ipapi.co/{request.META.get("HTTP_TRUE_CLIENT_IP")}/json/').json()
            current_weather = requests.get(f'http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={ipapi_request["city"]}, {ipapi_request["region_code"]}').json()
        except:
            current_weather = {}

    context = {
        'profile': profile,
        'posts': posts,
        'my_hour_data': my_hour_data,
        'congregation_hour_data': congregation_hour_data,
        'regular_days': len(filtered_regular_days),
        'current_weather': current_weather,
        'congregation_service_meetings': len(congregation_service_meetings),
        'title': 'Pioneer Partner - Dashboard',
    }

    return render(request, 'dashboard/dashboard.html', context)