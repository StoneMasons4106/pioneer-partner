from django.db import models
from address.models import AddressField
from django.contrib.auth.models import User
import random
import string

# Create your models here.

class Call(models.Model):
    GENDERS = [
        ('1', 'Male'),
        ('2', 'Female'),
    ]

    call_id = models.CharField(max_length=16, unique=True)
    name = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDERS, default='1')
    age = models.IntegerField(null=True, blank=True)
    address = AddressField(null=True, blank=True)
    contact_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True, max_length=3000)

    def _generate_call_id(self):
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
        if not self.call_id:
            self.call_id = self._generate_call_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

class ReturnVisit(models.Model):

    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    contact_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True, max_length=3000)

    def __str__(self):
        return self.call