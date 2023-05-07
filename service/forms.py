from django import forms
from address.forms import AddressField
from .models import Call
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