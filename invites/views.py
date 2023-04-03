from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from invites.models import Invite
from congregations.models import Congregation, ServiceGroup
from profiles.models import UserProfile
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
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


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def invites(request):

    profile = get_object_or_404(UserProfile, user=request.user)
    invites = Invite.objects.filter(congregation=profile.congregation)

    context = {
        'profile': profile,
        'invites': invites,
        'title': 'Pioneer Partner - Invites',
    }

    return render(request, 'invites/invites.html', context)


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def delete_invite(request, invite_code):

    invite = get_object_or_404(Invite, code=invite_code)
    invite.delete()
    messages.success(request, 'Invite has been removed.')

    return redirect('invites')


@user_passes_test(congregation_admin_check, login_url='/congregation/')
def add_invite(request, congregation_id):

    profile = get_object_or_404(UserProfile, user=request.user)
    congregation = get_object_or_404(Congregation, pk=profile.congregation.id)
    service_groups = ServiceGroup.objects.filter(congregation=congregation)
    congregation_id = congregation.congregation_id

    if request.method == "POST":
        request_data = request.body.decode().replace('+', ' ').replace('%40', '@')
        name_split = request_data.split('name=')[1]
        name = name_split.split('&')[0]
        email_split = request_data.split('email=')[1]
        email = email_split.split('&')[0]
        service_group_id = request_data.split('service-group=')[1]
        service_group = get_object_or_404(ServiceGroup, pk=service_group_id)
        invite = Invite(congregation=congregation, name=name, email=email, service_group=service_group)
        invite.save()

        invite_notification_message = render_to_string(
            'invites/emails/invite.txt', {
                'name': name,
                'my_hostname': os.environ.get('MY_HOSTNAME'),
                'code': invite.code,
            }
        )

        invite_notification_message_wrapper = EmailMessage(
            f'Pioneer Partner Invitation: {name}',
            invite_notification_message,
            to=[email]
        )

        invite_notification_message_wrapper.send()

        messages.success(request, 'Invite has been added.')
        return redirect('invites')

    context = {
        'profile': profile,
        'congregation_id': congregation_id,
        'service_groups': service_groups,
        'title': 'Pioneer Partner - Add Invite',
    }

    return render(request, 'invites/add_invite.html', context)

