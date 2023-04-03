from django.db import models
from congregations.models import Congregation, ServiceGroup
import random
import string

# Create your models here.

class Invite(models.Model):

    code = models.CharField(max_length=10, unique=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=254)
    email = models.EmailField()
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, null=True, blank=True)

    def _generate_code(self):
        """
        Generate a random, unique post ID using UUID
        """
        output_string = ''.join(random.SystemRandom().choice(string.ascii_letters.lower() + string.digits) for _ in range(10))
        return output_string

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.code:
            self.code = self._generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code