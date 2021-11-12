from django import forms

class LoginForm(forms.Form):
    id = forms.CharField(label='id')
    password = forms.CharField(widget=forms.PasswordInput(),label='password')