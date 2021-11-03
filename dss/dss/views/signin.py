from account_.models import *
from django.views.generic import View
from django.shortcuts import render
from dss.forms import *
import bcrypt

class Signin(View):
    """
    Sign In
    """
    def get(self,request):
        form = LoginForm();
        return render(request,'dss/signin.html',{'form':form})
    def post(self,request):
        form = LoginForm(request.POST,request.FILES)
        if form.is_valid() :
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            if User.objects.filter(id=id).exists():
                user = User.objects.get(id=id)
                if bcrypt.checkpw(str(password).encode('utf-8'), str(user.password).encode('utf-8')):
                    return render(request,'dss/signin.html',{'form':form})
            return render(request,'dss/signin.html',{'form':form})
        else :
            form = LoginForm();
            text = "잘못 입력하셨습니다."
            return render(request,'dss/signin.html',{'form':form,'text':text})

