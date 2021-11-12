from account_.models import *
from django.views.generic import View
from django.shortcuts import render
from dss.forms import *
import bcrypt
from dss.settings import SESSION_COOKIE_AGE;

class Signin(View):
    """
    로그인 함수
    """
    # GET 메소드 -> 로그인 페이지 요청
    def get(self,request):
        form = LoginForm();
        return render(request,'dss/signin.html',{'form':form})
    # POST 메소드 -> 사용자가 보내는 데이터와 데이터베이스의 정보 일치 여부 확인
    def post(self,request):
        # LoginForm으로부터 데이터 파싱
        form = LoginForm(request.POST,request.FILES)
        # LoginForm이 유효 
        if form.is_valid() :
            # 데이터 파싱
            id = form.cleaned_data['id']
            password = form.cleaned_data['password']
            # 파싱한 id 데이터가 DB에 있음
            if User.objects.filter(id=id).exists():
                # 아이디 파싱
                user = User.objects.get(id=id)
                # 비밀번호 일치
                if bcrypt.checkpw(str(password).encode('utf-8'), str(user.password).encode('utf-8')): 
                    # 아이디 존재 && 비밀번호 일치
                    # session 생성 및 만료 시간 설정
                    request.session["user_id"] = id
                    request.session.set_expiry(SESSION_COOKIE_AGE) # 특이점은 알아서 sessionid라는 쿠키가 전달된다.
                    # response 생성 및 쿠키 설정
                    response = render(request,'dss/menu.html',{'user_id':id})
                    response.set_cookie("user_id",id,max_age=SESSION_COOKIE_AGE)
                    # response 반환
                    return response
                # 비밀번호 불일치
                else:
                    new_form = LoginForm();
                    text = "비밀번호가 틀렸습니다."
                    return render(request,'dss/signin.html',{'form':new_form,'text':text})
            # 파싱한 id 데이터가 DB에 없음.
            else :
                new_form = LoginForm();
                text = "없는 회원입니다."
                return render(request,'dss/signin.html',{'form':new_form,'text':text})
        # LoginForm이 유효하지 않음.
        else :
            new_form = LoginForm();
            text = "모든 값을 입력해야 합니다."
            return render(request,'dss/signin.html',{'form':new_form,'text':text})

class Logout(View):
    def get(self,request):
        if request.COOKIES.get('user_id'):
            # 세션 삭제
            del(request.session['user_id'])
            # 쿠키 삭제
            response = render(request,'dss/index.html')
            response.delete_cookie('user_id')
        return response



"""
    [여기서 한 가지 몰랐던 점]
    request.session['key']를 사용하면
    알아서 이 key라는 세션의 세션id가 
    쿠키값으로 브라우저에 전송이 된다.
    그래서 내가 굳이 쿠키까지 구현하지 않아도 되고
    세셔만 사용해도 무관한다.
    
    그러나 이 코드에선 연습을 위해 쿠키까지 내가 구현한다.
    사실 쿠키값이 노출되선 안되기 때문에 쿠키값을 해싱하여
    전송하지만 이 과정은 생략했다.
    
    [참고자료]
    1. https://docs.djangoproject.com/en/3.2/topics/http/sessions/#using-sessions-in-views
    2. https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Sessions
    3. https://techvidvan.com/tutorials/django-cookies-handling/
    4. https://velog.io/@rosewwross/Django-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%8B%9C-cookie%EC%97%90-token-%EC%A0%80%EC%9E%A5%ED%95%98%EA%B8%B0
    5. http://okminseok.blogspot.com/2019/07/django-cookie.html
    6. https://gmyankee.tistory.com/220
    7. https://stackoverflow.com/questions/2299435/django-delete-all-cookie
"""
    
