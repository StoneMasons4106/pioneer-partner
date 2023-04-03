from django import forms
from .models import ScheduleRequest

class ScheduleRequestForm(forms.ModelForm):
    class Meta:
        model = ScheduleRequest
        exclude = ('requesting_user', 'to_user', 'day', 'start_time', 'end_time', 'notes',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'confirmation': '1',
            'confirmation_notes': 'Write something here...',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['required'] = 'required'