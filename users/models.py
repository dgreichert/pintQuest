from django.db import models
from django.contrib.auth.models import User
from django import forms

class SignupForm(forms.Form):
    username = forms.RegexField(
        max_length=30, 
        min_length=3, 
        regex=r'^[\w.-]+$', 
        error_message="Enter a valid username (a-z, A-Z, 0-9, _, ., -) ",
        )
    email = forms.EmailField()
    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))
    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(render_value=False))

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError("This username is already in use. Please choose another.")
    
    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError("This email already in use. Please choose another.")      

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("You must type the same password each time")
        return self.cleaned_data     

    def save(self):
        new_user = User.objects.create_user(username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'])
        return new_user
