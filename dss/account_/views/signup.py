from django.shortcuts import render
from django.views.generic import View
from account_.forms import *
from account_.views.do_duplicate_check import *
from account_.views.get_bcrypt_value import *
from account_.views.get_client_ip import *

# Create your views here.

class Signup(View):
    def get(self,request):
        form = SignupForm()
        return render(request,'account/signup.html',{'form':form})

    def post(self,request):
        """
        Request have information of user.
        """
        form = SignupForm(request.POST,request.FILES)
        if form.is_valid() :
            user = User()
            user.id = form.cleaned_data['id']
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user_password_check = form.cleaned_data['password_check']
            flag = do_duplicate_check(request)
            if (user.password == user_password_check)  and (flag == "pass"):
                new_user = User()
                ip = get_client_ip(request)
                new_user.id = user.id
                new_user.name = user.name
                new_user.email = user.email
                new_user.password = get_bcrypt_value(user.password)
                new_user.save()
                print("IP : {0} 가입 성공".format(ip))
                return render(request,'account/success_signup.html')
            else:
                text = "아이디 중복 또는 비밀번호 다름"
                form = SignupForm()
                return render(request,'account/signup.html',{'form':form,'text':text})
        else:
            text = "정보 불충분"
            form = SignupForm()
            return render(request,'account/signup.html',{'form':form,'text':text})