from django.db import models
from address.models import AddressField
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
import random
import string
from congregations.models import Congregation

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
    age = models.PositiveIntegerField(null=True, blank=True)
    address = AddressField(on_delete=models.CASCADE, null=True, blank=True)
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
    contact_date = models.DateField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True, max_length=3000)

    def __str__(self):
        return self.call.name
    

class Territory(models.Model):
    TERRITORY_STATUSES = [
        ('1', 'Completed'),
        ('2', 'Signed Out'),
    ]

    territory_id = models.CharField(max_length=16, unique=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=TERRITORY_STATUSES, default='1')
    signed_out = models.DateField(null=True, blank=True)
    last_completed = models.DateField(null=True, blank=True)
    map = models.FileField(validators=[FileExtensionValidator(['pdf'])])
    
    def _generate_territory_id(self):
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
        if not self.territory_id:
            self.territory_id = self._generate_territory_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.number} - {self.congregation}'


class Street(models.Model):
        
    name = models.CharField(max_length=254)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class NHRecord(models.Model):
    
    number = models.PositiveIntegerField()
    street = models.ForeignKey(Street, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.number} {self.street}'
    

class DoNotCall(models.Model):

    address = AddressField(on_delete=models.CASCADE)
    territory = models.ForeignKey(Territory, on_delete=models.CASCADE)
    notes = models.TextField(max_length=3000)

    def __str__(self):
        return str(self.address)