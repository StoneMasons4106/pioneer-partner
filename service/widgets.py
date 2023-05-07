from django.forms.widgets import DateInput, NumberInput

class DateInput(DateInput):
    input_type = 'date'

class NumberInput(NumberInput):
    input_type = 'number'