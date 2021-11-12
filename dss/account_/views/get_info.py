from django.shortcuts import render
from django.views.generic import View
from account_.models import User

class Info(View):
    def get(self,request):
        # 쿠키값으로 사용자 특정
        user_id = request.COOKIES.get('user_id')
        # 사용자 정보 불러오기
        user_info = User.objects.get(id=user_id)
        info_id = user_info.id
        info_name = user_info.name
        info_email = user_info.email
        # response 반환
        return render(request,'account/information.html',{'info_id':info_id,'info_name':info_name,'info_email':info_email,'info_list':True})




""" [참고자료]
    1. https://inuplace.tistory.com/602
"""