from django.views.generic import View
from django.shortcuts import render

class Menu(View):
    """
    Index of Site
    """
    def get(self,request):
        return render(request,'dss/menu.html')

