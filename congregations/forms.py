from allauth.account.forms import SignupForm
from django import forms
from address.forms import AddressField
from django.shortcuts import get_object_or_404
from invites.models import Invite
from profiles.models import UserProfile
from django.forms import ValidationError
from .models import Congregation, ServiceGroup

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')
    invite_code = forms.CharField(max_length=10, label='Invite Code')

    def clean(self):
        try:
            get_object_or_404(Invite, code=self.cleaned_data['invite_code'])
        except:
            raise ValidationError('Invalid invite code, please try again.')
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        profile = get_object_or_404(UserProfile, user=user)
        invite = get_object_or_404(Invite, code=self.cleaned_data['invite_code'])
        profile.congregation = invite.congregation
        profile.service_group = invite.service_group
        profile.save()
        invite.delete()
        return user


class EditCongregationInfo(forms.ModelForm):
    class Meta:
        model = Congregation
        address = AddressField()
        exclude = ('congregation_id',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'address': 'Address',
            'number': 'Number',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'name' or field == 'number':
                self.fields[field].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'address form-control'


class EditServiceGroupInfo(forms.ModelForm):
    class Meta:
        model = ServiceGroup
        address = AddressField()
        exclude = ('congregation', 'service_group_id',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'service_location': 'Service Group Location',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'name':
                self.fields[field].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'address form-control'



class AddServiceGroup(forms.ModelForm):
    class Meta:
        model = ServiceGroup
        address = AddressField()
        exclude = ('congregation', 'service_group_id',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name',
            'service_location': 'Service Group Location',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field == 'name':
                self.fields[field].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'address form-control'