"""dss URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from dss.views.index import *
from dss.views.signin import * 
from dss.views.menu import * 

app_name='dss'

# for Administrator
urlpatterns = [
    path('admin/', admin.site.urls),
]
# for dss
urlpatterns +=[
    path('', Index.as_view(),name='Index'),
    path('/', Index.as_view(),name='Index'),
    path('signin/', Signin.as_view(),name='Signin'),
    path('logout/',Logout.as_view(),name='Logout'),
    path('menu/',Menu.as_view(),name='Menu')
]
# for other apps
urlpatterns +=[
    path('account/',include('account_.urls'),name='account'),
    path('board/',include('board_.urls'),name='board'),
]
