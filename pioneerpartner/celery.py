import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pioneerpartner.settings')
app = Celery("pioneerpartner")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "trigger-email-notifications": {
        "task": "schedule_reminders",
        "schedule": crontab(minute=0, hour=5, day_of_week="*")
    }
}