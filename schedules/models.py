from django.db import models
from django.contrib.auth.models import User
from profiles.models import UserProfile
from congregations.models import Congregation
from django.shortcuts import get_object_or_404
import random
import string
from datetime import date

# Create your models here.

class RegularServiceDay(models.Model):
    DAYS_OF_WEEK = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, default='1')
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user} is normally in service on {self.get_day_display()}s from {self.start_time} to {self.end_time}'

    def get_congregation(self):
        profile = get_object_or_404(UserProfile, user=self.user)
        return profile.congregation


class ScheduleRequest(models.Model):
    REQUEST_CONFIRMATION = [
        ('1', 'No'),
        ('2', 'Yes'),
    ]

    request_id = models.CharField(max_length=16, null=False, editable=False, unique=True)
    requesting_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requesting_user')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    day = models.DateField()
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    end_time = models.TimeField(auto_now=False, auto_now_add=False)
    notes = models.TextField(max_length=512, blank=True, null=True)
    confirmation = models.CharField(max_length=5, choices=REQUEST_CONFIRMATION, null=True, blank=True)
    confirmation_notes = models.TextField(max_length=512, blank=True, null=True)

    def __str__(self):
        return f'{self.requesting_user} would like to work with {self.to_user} on {self.day} from {self.start_time} to {self.end_time}'

    def _generate_request_id(self):
        """
        Generate a random, unique post ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.digits) for _ in range(16))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.request_id:
            self.request_id = self._generate_request_id()
        super().save(*args, **kwargs)

    def check_date(self):
        now = date.today()
        if self.day < now:
            self.delete()
            return True
        else:
            return False