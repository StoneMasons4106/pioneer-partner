from django.db import models
from django.contrib.auth.models import User
from allauth.account.models import EmailAddress
from allauth.account.signals import email_confirmed
from django.db.models.signals import post_save
from django.dispatch import receiver
from congregations.models import Congregation, ServiceGroup

# Create your models here.

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=254, null=True, blank=True)
    location = models.CharField(max_length=45, null=True, blank=True)
    profile_picture = models.ImageField(null=True, blank=True)
    congregation = models.ForeignKey(Congregation, on_delete=models.CASCADE, null=True, blank=True)
    service_group = models.ForeignKey(ServiceGroup, on_delete=models.CASCADE, null=True, blank=True)
    liked_post_notifications = models.BooleanField(default=False)
    comment_post_notifications = models.BooleanField(default=False)

    def add_email_address(self, request, new_email):
        return EmailAddress.objects.add_email(request, self.user, new_email, confirm=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()


@receiver(email_confirmed)
def update_user_email(sender, request, email_address, **kwargs):
    # Once the email address is confirmed, make new email_address primary.
    # This also sets user.email to the new email address.
    # email_address is an instance of allauth.account.models.EmailAddress
    email_address.set_as_primary()
    EmailAddress.objects.filter(user=email_address.user).exclude(primary=True).delete()