from django import forms
from address.forms import AddressField
from .models import Call, ReturnVisit, Street, Territory
from profiles.models import UserProfile
from .widgets import NumberInput

class AddCall(forms.ModelForm):
    class Meta:
        model = Call
        address = AddressField()
        exclude = ('call_id', 'user', 'contact_date',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['age'].widget = NumberInput()
        placeholders = {
            'name': 'Name',
            'gender': 'Gender',
            'age': 'Age',
            'address': 'Address',
            'notes': 'Notes',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            if field != 'address':
                self.fields[field].widget.attrs['class'] = 'form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'address form-control'


class AddReturnVisit(forms.ModelForm):
    class Meta:
        model = ReturnVisit
        exclude = ('call', 'contact_date',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'notes': 'Notes',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddStreet(forms.ModelForm):
    class Meta:
        model = Street
        exclude = ('territory',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Street Name',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddTerritory(forms.ModelForm):
    class Meta:
        model = Territory
        exclude = ('territory_id', 'congregation', 'status', 'signed_out', 'last_completed',)

    def __init__(self, congregation, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['number'].widget = NumberInput()
        profiles = UserProfile.objects.filter(congregation=congregation)
        users = [['', '--------------']]
        for profile in profiles:
            users.append([profile.user.id, profile.user.username])
        self.fields['assigned_to'].choices = users
        placeholders = {
            'number': 'Territory Number',
            'assigned_to': 'Assigned To',
            'map': 'Map',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'