from django.shortcuts import redirect, render
from django.views.generic import View
# Create your views here.

class Index(View):
    def get(self,request):
        return redirect('board/index.html')