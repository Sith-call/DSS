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
        # SignupForm : 일반폼이자 회원가입 정보를 받아오는 폼.
        # 템플릿에 구현된 SignupForm에 담겨온 정보를 form이란 변수에 담는다.
        form = SignupForm(request.POST,request.FILES)
        # SignupForm에서 받아온 정보들이 모두 유효한지 확인한다.
        if form.is_valid() :
            # User Model의 객체를 하나 생성한다.
            # 이 객체를 통해 form으로부터 받아온 정보를 넣어둘 수 있다.
            # 지금 보니 굳이 user를 사용하지 않아도 됐네.
            user = User()
            # form으로부터 데이터를 파싱하여 객체에 저장한다.
            user.id = form.cleaned_data['id']
            user.name = form.cleaned_data['name']
            user.email = form.cleaned_data['email']
            user.password = form.cleaned_data['password']
            user_password_check = form.cleaned_data['password_check']
            # 아이디 중복검사를 실시한다. 검사를 통과한다면 "pass"를 반환
            flag = do_duplicate_check(request)
            # 비밀번호를 제대로 입력하였는지 체크한다.
            if (user.password == user_password_check)  and (flag == "pass"):
                # 새롭게 저장할 user를 생성한다.
                new_user = User()
                # 가입성공 로그를 기록하기 위해서 ip주소를 받아온다.
                ip = get_client_ip(request)
                # 새로운 user의 정보를 입력한다.
                new_user.id = user.id
                new_user.name = user.name
                new_user.email = user.email
                # 이때 비밀번호는 해싱하여 저장한다.(키스트레칭 & 솔팅)
                new_user.password = get_bcrypt_value(user.password)
                # 새로운 유저를 모델에 저장한다.
                new_user.save()
                print("IP : {0} 가입 성공".format(ip))
                # 가입 성공 문구를 반환한다.
                return render(request,'account/success_signup.html')
            else:
                text = "아이디 중복 또는 비밀번호 다름"
                form = SignupForm()
                return render(request,'account/signup.html',{'form':form,'text':text})
        # form이 유효하지 않다면 아래와 같이 다시 입력할 수 있도록 한다.
        else:
            text = "정보 불충분"
            form = SignupForm()
            return render(request,'account/signup.html',{'form':form,'text':text})