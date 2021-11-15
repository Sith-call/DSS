from django.shortcuts import redirect, render
from board_.models import *
from django.views.generic import View
import datetime, hashlib
# Create your views here.

class Create(View):
    def get(self,request):
        # 사용자 세션이 존재하는지 확인한다.
        if(request.session['user_id']):
            # post_id를 user_id와 now를 합친 문자열의 해쉬값으로 설정한다.
            # post_id는 post 테이블의 primary key이다.
            now = datetime.datetime.now()
            key = request.session['user_id']+str(now)
            hash_value = hashlib.sha256()
            hash_value.update(key.encode('utf-8'))
            post_id = int(hash_value.hexdigest(),16)
            # 이때 post_id는 생성했지만, 튜플은 생성되지 않았다.
            # 사용자가 모든 정보를 입력하고 서버에 이를 전송한 뒤에 튜플이 생성됨.
            return render(request,'board/write.html',{'post_id':post_id})
        # 사용자 세션이 없다면, 웹 사이트의 엔트리 페이지로 이동한다.
        # 왜냐하면 서비스를 이용하려면, 제일 먼저 로그인부터 해야 한다.
        else:
            return render(request,'dss/index.html')
    
    def post(self,request):
        # 사용자로부터 정보가 들어옴.
        # 사용자 세션이 존재하는지 확인한다.
        if(request.session['user_id']):
            # 튜플을 생성한다.
            post = Post()
            post.post_id = request.GET.get('post_id')
            post.owner = request.session['user_id']
            post.subject = request.POST.get('subject')
            post.content = request.POST.get('content')
            # 모든 정보를 입력한 뒤에 튜플을 테이블에 저장.
            post.save()
            # 게시글 목록을 반환한다.
            if(Post.objects.all().exists()):
                post_list = Post.objects.all()
                return render(request,'board/index.html',{'post_list':post_list})
            return render(request,'board/index.html')
        # 세션이 없다면 초기 화면으로.
        else:
            return render(request,'dss/index.html')
    
class Read(View):
    def get(self,request):
        if(request.session['user_id']):
            # post_id를 통해서 어떤 게시글을 원하는지 특정한다.
            post_id = request.GET.get('post_id')
            post = Post.objects.get(post_id=post_id)
            # 검색된 해당 튜플의 값을 render 함수에 전달한다.
            # post:True는 필요 없는건데.. 수정하지 않았다.
            subject = post.subject
            content = post.content
            return render(request,'board/read.html',{'subject':subject,'content':content,'post_id':post_id,'post':True})
        else:
            return render(request,'dss/index.html')
    
class Update(View):
    # 먼저 get 메소드를 통해서 update 템플릿을 반환한다.
    # 그리고 항상 post_id가 url에 쿼리 파라미터로 존재해야 게시글을 제어할 수 있다.
    def get(self,request):
        post_id = request.GET.get('post_id')
        return render(request,'board/update.html',{'post_id':post_id})
    # update 템플릿으로부터 정보가 들어왔다.(post메소드)
    def post(self,request):
        if(request.session['user_id']):
            # post_id를 쿼리 파라미터로부터 파싱한다.
            post_id = request.GET.get('post_id')
            post = Post.objects.get(post_id=post_id)
            # 튜플의 값을 수정한다.
            post.subject = request.POST.get('subject')
            post.content = request.POST.get('content')
            # 저장한다.
            post.save()
            print(post_id+' is updated.')
            if(Post.objects.all().exists()):
                post_list = Post.objects.all()
                return render(request,'board/index.html',{'post_list':post_list})
            return render(request,'board/index.html')
        else:
            return render(request,'dss/index.html')
    
class Delete(View):
    def get(self,request):
        if(request.session['user_id']):
            post_id = request.GET.get('post_id')
            post = Post.objects.get(post_id=post_id)
            post.delete()
            if(Post.objects.all().exists()):
                post_list = Post.objects.all()
                return render(request,'board/index.html',{'post_list':post_list})
            return render(request,'board/index.html')
        else:
            return render(request,'dss/index.html')

"""
    [요약]
    CRUD의 근간은 Post 테이블의 primary key인 post_id를 어떻게 활용하는지이다.
    
    먼저 Create를 할 때 post_id를 세션값인 user_id와 datetime을 합쳐서 해쉬값으로 생성한다.
    그리고 이것을 Get method의 반환값과 함께 템플릿에 렌더링하여 클라이언트에게 전송한다.
    이것을 전달 받은 클라이언트는 모든 내용을 작성한 뒤에 다시 post_id를 쿼리 파라미터로 서버에 전송한다.
    서버는 이제 사용자가 모든 정보를 입력했기에 post_id와 함께 튜플을 생성하여 이를 데이터베이스에 저장한다.
    
    Board의 index 페이지는 이러한 post_id 사용을 염두에 두고 만들어졌다.
    그래서 게시글에 연결된 하이퍼링크의 쿼리파라미터에는 각 게시글의 post_id가 들어있다.
    따라서 해당 게시글을 Read하려고 한다면, 서버는 쿼리 파라미터를 통해서 그 게시글을 특정하고
    이를 다시 사용자에게 반환한다.
    
    Index 페이지의 하이퍼링크마다 각각의 게시글의 post_id가 있기 때문에 update와 delete도 이를 활용한다.
    쿼리 파라미터로 전달된 post_id를 이용하여 해당 게시글을 특정할 수만 있다면,
    그 게시글을 수정하고 삭제하는 것은 손쉽게 코딩할 수 있다.
"""