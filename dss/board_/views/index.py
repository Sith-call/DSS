from django.shortcuts import redirect, render
from django.views.generic import View
from board_.models import *
# Create your views here.

class Index(View):
    def get(self,request):
        if(Post.objects.all().exists()):
            post_list = Post.objects.all()
            return render(request,'board/index.html',{'post_list':post_list})
        return render(request,'board/index.html')