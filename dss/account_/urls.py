from django.urls import path
from account_.views.signup import *
from django.views.generic import View

app_name = 'account'

urlpatterns = [
    path('signup/',Signup.as_view(),name='Signup'),
]