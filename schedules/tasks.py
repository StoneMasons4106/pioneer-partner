from celery import shared_task
from .models import ScheduleRequest
from datetime import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import logging
import os

logger = logging.getLogger(__name__)

@shared_task(name="schedule_reminders")
def send_schedule_reminders():
    today = datetime.today().strftime('%Y-%m-%d')
    schedule_requests = ScheduleRequest.objects.filter(day=today, confirmation='2')

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

    logger.debug(f'Emails were sent for {len(schedule_requests)} requests.')