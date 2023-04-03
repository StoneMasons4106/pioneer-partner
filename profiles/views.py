from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile
from django.contrib.auth.models import User
from .forms import UserProfileForm, UserForm
from allauth.account.models import EmailAddress
from django.contrib import messages
from allauth.account.views import PasswordChangeView
from posts.models import Post
from congregations.models import Congregation, ServiceGroup
from schedules.models import RegularServiceDay
from django.db.models import Q
import requests
import os

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
def profile(request):
    '''A view to return the profile page'''

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=request.user)
    posts = Post.objects.filter(Q(comment__isnull=True), user=user).order_by("-created")
    bookmarks = Post.objects.filter(bookmarks__id=user.id).order_by("-created")

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        form_two = UserForm(request.POST, instance=user)
        if form.is_valid() and form_two.is_valid():
            try:
                user_email = get_object_or_404(EmailAddress, user_id=request.user)
                if str(request.POST.get('email')) != str(user_email):
                    new_email = request.POST.get('email')
                    profile.add_email_address(request, new_email)
                    messages.success(request, 'Profile updated successfully, please confirm the new email in your profile by clicking the link in the email sent to you.')
                else:
                    messages.success(request, 'Profile updated successfully.')
                form.save()
                form_two.save()
            except EmailAddress.MultipleObjectsReturned:
                messages.error(request, 'Please confirm the email in your profile before attempting to update it again.')
        else:
            messages.error(request, 'Update failed. Please ensure the form is valid.')
    else:
        form = UserProfileForm(instance=profile)
        form_two = UserForm(instance=user)

    context = {
        'profile': profile,
        'user': user,
        'form': form,
        'form_two': form_two,
        'posts': posts,
        'bookmarks': bookmarks,
        'title': 'Pioneer Partner - My Profile',
    }

    return render(request, 'profiles/profile.html', context)


@login_required
def user_view(request, username):

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.user == user:

        return redirect('profile')
    
    else:

        if profile.congregation == user_profile.congregation:

            posts = Post.objects.filter(Q(comment__isnull=True), user=user).order_by("-created")
            service_days = RegularServiceDay.objects.filter(user=user).order_by('day')

            token = os.environ.get('JUSTACART_TOKEN')
            shifts = requests.get(f'https://imjustacart.com/api/shifts?token={token}&email={user.email}')

            if "ERROR" in shifts.text:
                shifts = {}
            elif shifts.json():
                shifts = shifts.json()['data']
            else:
                shifts = {}

            context = {
                'user': user,
                'profile': profile,
                'user_profile': user_profile,
                'posts': posts,
                'service_days': service_days,
                'shifts': shifts,
                'groups': request.user.groups.all(),
                'title': f'Pioneer Partner - User View - {user.username}',
            }

            return render(request, 'profiles/userview.html', context)
        
        else:

            messages.error(request, f'{user.username} is no longer assigned to your congregation.')
            return redirect(request.META['HTTP_REFERER'])


@login_required
def update_settings(request):
    
    if request.method == "POST":
        profile = get_object_or_404(UserProfile, user=request.user)
        updated_settings_data = request.body.decode()

        if 'liked-post' in updated_settings_data:
            profile.liked_post_notifications = True
        else:
            profile.liked_post_notifications = False

        if 'comment-post' in updated_settings_data:
            profile.comment_post_notifications = True
        else:
            profile.comment_post_notifications = False

        profile.save()

        messages.success(request, 'Notification settings updated successfully!')
        return redirect('profile')


@login_required
def cart_shift(request, username, shift_id):
    
    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=username)
    token = os.environ.get('JUSTACART_TOKEN')
    shifts = requests.get(f'https://imjustacart.com/api/shifts?token={token}&email={user.email}')

    for shift in shifts.json()['data']:
        if int(shift['Schedule']['id']) == shift_id:
            correct_shift = shift
            break

    context = {
        'profile': profile,
        'shift': correct_shift,
        'user': user,
        'title': f'Pioneer Partner - Cart Shift - {shift_id}',
    }

    return render(request, 'profiles/cart_shift.html', context)


@user_passes_test(congregation_admin_check, login_url='/dashboard/')
def edit_user(request, username):

    profile = get_object_or_404(UserProfile, user=request.user)
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    congregations = Congregation.objects.all()
    service_groups = ServiceGroup.objects.all()

    if request.method == "POST":

        data = request.body.decode()
        congregation_id = data.split('congregation=')[1].split('&')[0]
        service_group_id = data.split('service-group=')[1].split('&')[0]
        congregation = get_object_or_404(Congregation, congregation_id=congregation_id)
        service_group = get_object_or_404(ServiceGroup, service_group_id=service_group_id)
        regular_service_days = RegularServiceDay.objects.filter(user=user)

        if service_group.congregation != congregation:
            messages.error(request, 'The service group selected must be part of the congregation selected on the form.')
            return redirect(request.META['HTTP_REFERER'])
        else:
            user_profile.congregation = congregation
            user_profile.service_group = service_group
            user_profile.save()
            for day in regular_service_days:
                day.congregation = congregation
                day.save()
            messages.success(request, 'The user has been successfully updated.')
            return redirect(request.META['HTTP_REFERER'])

    context = {
        'profile': profile,
        'user_profile': user_profile,
        'congregations': congregations,
        'service_groups': service_groups,
        'title': f'Pioneer Partner - Edit User - {user_profile.user.username}',
    }

    return render(request, 'profiles/edit_user.html', context)


class CustomPasswordChangeView(PasswordChangeView):
    success_url = '/profile/me'