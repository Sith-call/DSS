from django.urls import path
from board_.views.index import *
from board_.views.CRUD import *
from django.views.generic import View

app_name = 'board'

urlpatterns = [
    path('',Index.as_view(),name='Index'),
    path('create/',Create.as_view(),name='Create'),
    path('read/',Read.as_view(),name='Read'),
    path('update/',Update.as_view(),name='Update'),
    path('delete/',Delete.as_view(),name='Delete'),
]