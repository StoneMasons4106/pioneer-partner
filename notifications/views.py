from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification
from profiles.models import UserProfile
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def all_notifications(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    all_notifications = Notification.objects.filter(user=request.user).order_by("-created")

    context = {
        'profile': profile,
        'all_notifications': all_notifications,
        'title': 'Pioneer Partner - All Notifications',
    }

    return render(request, 'notifications/all_notifications.html', context)


@login_required
def new_notifications(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    new_notifications = Notification.objects.filter(user=request.user, status='1').order_by("-created")

    context = {
        'profile': profile,
        'new_notifications': new_notifications,
        'title': f'Pioneer Partner - New Notifications ({len(new_notifications)})',
    }

    return render(request, 'notifications/new_notifications.html', context)


@login_required
def mark_all_read(request):

    new_notifications = Notification.objects.filter(user=request.user, status='1')

    for notification in new_notifications:
        notification.status = '2'
        notification.save()

    return redirect('all_notifications')


@login_required
def mark_notification_read(request, notification_id):

    if request.method == 'POST':
        request_data = request.body.decode()
        notification_id = request_data.split('notificationId=')[1]
        notification = get_object_or_404(Notification, notification_id=notification_id)
        if notification.status == '1':
            notification.status = '2'
            notification.save()

    return HttpResponse("OK")