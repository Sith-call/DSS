
from django import forms
from django.db.models.fields import AutoField

class SignupForm(forms.Form):
    id = forms.CharField(label='id')
    name = forms.CharField(label='name')
    email = forms.EmailField(label='email')
    password = forms.CharField(widget=forms.PasswordInput(),label='password')
    password_check = forms.CharField(widget=forms.PasswordInput(),label='password_check')