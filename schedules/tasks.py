from celery import shared_task
from django.shortcuts import get_object_or_404
from profiles.models import UserProfile
from .models import ScheduleRequest
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from twilio.rest import Client
import logging
import os

logger = logging.getLogger(__name__)

@shared_task(name="schedule_reminders")
def send_schedule_reminders():
    today = datetime.today().strftime('%Y-%m-%d')
    schedule_requests = ScheduleRequest.objects.filter(day=today, confirmation='2')
    twilio_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_ACCOUNT_AUTH_TOKEN')
    twilio_phone = os.environ.get('TWILIO_PHONE')
    client = Client(twilio_sid, twilio_auth_token)

    for request in schedule_requests:
        request_reminder_message = render_to_string(
            'schedules/emails/schedule_reminder.txt', {
                'requesting_name': request.requesting_user,
                'to_name': request.to_user,
                'my_hostname': os.environ.get('MY_HOSTNAME')
            }
        )
        request_reminder_message_wrapper = EmailMessage(
            f'Schedule Request Reminder: {today}',
            request_reminder_message,
            to=[request.requesting_user.email, request.to_user.email],
        )
        
        request_reminder_message_wrapper.send()

        requesting_user_profile = get_object_or_404(UserProfile, user=request.requesting_user)
        to_user_profile = get_object_or_404(UserProfile, user=request.to_user)

        client.messages.create(
            from_=twilio_phone,
            body='Hello! This is a reminder that you have service plans for today! If you would like to view these plans, please visit https://www.pioneerpartner.net/schedule/schedule_requests/. Thank you.',
            to=requesting_user_profile.phone
        )

        client.messages.create(
            from_=twilio_phone,
            body='Hello! This is a reminder that you have service plans for today! If you would like to view these plans, please visit https://www.pioneerpartner.net/schedule/schedule_requests/. Thank you.',
            to=to_user_profile.phone
        )

    logger.debug(f'Emails and texts were sent for {len(schedule_requests)} requests.')