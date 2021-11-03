
from account_.models import User
from django.http import JsonResponse 

def do_duplicate_check(request):
    """
    아이디 중복확인
    """
    user_email = request.POST.get('email')
    try:
        # 중복 검사 실패
        _id = User.objects.get(email=user_email)
        print(_id)
    except:
        # 중복 검사 성공
        _id = None
    if _id is None:
        duplicate = "pass"
    else:
        duplicate = "fail"
    context = {'duplicate': duplicate}
    # return JsonResponse(context) ajax를 배우고 다시 리팩토링
    return duplicate