from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
    
    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username...'})
        self.fields['first_name'].widget.attrs.update({"class": 'form-control', "placeholder": 'First name...'})
        self.fields['last_name'].widget.attrs.update({"class": 'form-control', "placeholder": 'Last name...'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password...'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': "Confirm password..."})
        

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username...'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password...'})
