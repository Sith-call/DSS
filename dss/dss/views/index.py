from django.views.generic import View
from django.shortcuts import render

class Index(View):
    """
    Index of Site
    """
    def get(self,request):
        return render(request,'dss/index.html')

