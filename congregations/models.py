from django.db import models
from address.models import AddressField
import random
import string

# Create your models here.

class Congregation(models.Model):

    name = models.CharField(max_length=254)
    address = AddressField(null=True, blank=True)
    congregation_id = models.CharField(max_length=10, unique=True)
    number = models.CharField(max_length=10)
    justacart_token = models.CharField(max_length=254, null=True, blank=True)

    def _generate_congregation_id(self):
        """
        Generate a random, unique post ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.digits) for _ in range(9))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.congregation_id:
            self.congregation_id = self._generate_congregation_id()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class ServiceGroup(models.Model):

    name = models.CharField(max_length=254)
    service_group_id = models.CharField(max_length=10, unique=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE)
    service_location = AddressField(null=True, blank=True)

    def _generate_service_group_id(self):
        """
        Generate a random, unique post ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.digits) for _ in range(9))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.service_group_id:
            self.service_group_id = self._generate_service_group_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ServiceMeeting(models.Model):
    DAYS_OF_WEEK = [
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        ('7', 'Sunday'),
    ]

    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK, default='1')
    time = models.TimeField(auto_now=False, auto_now_add=False)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, null=True, blank=True)
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, null=True, blank=True)
    service_location = AddressField(null=True, blank=True)
    zoom = models.BooleanField(default=False, null=True, blank=True)
    zoom_id = models.CharField(max_length=30, null=True, blank=True)
    zoom_password = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if self.zoom and self.service_group:
            return f'{self.service_group} meets regularly for service on {self.get_day_display()} on Zoom at {self.time}'
        elif self.zoom:
            return f'{self.congregation} meets regularly for service on {self.get_day_display()} on Zoom at {self.time}'
        elif self.service_group:
            return f'{self.service_group} meets regularly for service on {self.get_day_display()} at {self.service_group.service_location} at {self.time}'
        else:
            return f'{self.congregation} meets regularly for service on {self.get_day_display()} at {self.service_location} at {self.time}'