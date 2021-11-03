from django import forms

class LoginForm(forms.Form):
    ID = forms.EmailField(label='id')
    PASSWORD = forms.CharField(widget=forms.PasswordInput(),label='password')