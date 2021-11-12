from django.urls import path
from board_.views.index import *
from django.views.generic import View

app_name = 'board'

urlpatterns = [
    path('/',Index.as_view(),name='Index'),
]