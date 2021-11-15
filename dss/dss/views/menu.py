from django.views.generic import View
from django.shortcuts import render

class Menu(View):
    """
    Index of Site
    """
    def get(self,request):
        user_id = request.session['user_id']
        return render(request,'dss/menu.html',{'user_id':user_id})

