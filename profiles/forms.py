from django import forms
from .models import UserProfile
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'congregation', 'liked_post_notifications', 'comment_post_notifications', 'service_group',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'profile_picture': 'Profile Picture',
            'bio': 'Bio',
            'location': 'Location',
            'phone': 'Phone',
        }

        for field in self.fields:
            if field == 'profile_picture':
                self.fields[field].widget.initial_text = ""
                self.fields[field].widget.input_text = ""
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_superuser', 'is_staff', 
        'is_active', 'date_joined', 'groups', 'user_permissions',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].required = True
        placeholders = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }

        self.fields['username'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]}'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control'