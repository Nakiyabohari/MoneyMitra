from django import forms
from django.contrib.auth.models import User
from .models import Profile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'password']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'gender', 'profile_photo']