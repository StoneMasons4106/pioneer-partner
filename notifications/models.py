from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.

class Notification(models.Model):
    NOTIFICATION_READ = [
        ('1', 'Unread'),
        ('2', 'Read'),
    ]

    NOTIFICATION_TYPE = [
        ('1', 'Schedule Request'),
        ('2', 'Post Like'),
        ('3', 'Post Comment'),
    ]

    notification_id = models.CharField(max_length=32, null=False, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    info = models.TextField(max_length=1024)
    url = models.URLField(max_length=1024)
    status = models.CharField(max_length=10, choices=NOTIFICATION_READ, default='1', null=True, blank=True)
    type = models.CharField(max_length=25, choices=NOTIFICATION_TYPE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def _generate_notification_id(self):
        """
        Generate a random, unique notification ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.ascii_letters.lower() + string.digits) for _ in range(32))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.notification_id:
            self.notification_id = self._generate_notification_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.notification_id