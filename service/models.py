from django.db import models
from address.models import AddressField
from django.contrib.auth.models import User

# Create your models here.

class Call(models.Model):

    name = models.CharField(max_length=254)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = AddressField(null=True, blank=True)
    contact_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True, max_length=3000)

    def __str__(self):
        return self.name
    

class ReturnVisit(models.Model):

    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    contact_date = models.DateTimeField()
    notes = models.TextField(null=True, blank=True, max_length=3000)

    def __str__(self):
        return self.call