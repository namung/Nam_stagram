import pkgutil
from telnetlib import STATUS
from urllib import response
from webbrowser import get
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse

from djangogram.users.models import User as user_model
from . import models, serializers
from .forms import CreatePostForm, CommentForm, UpdatePostForm

# Create your views here.
def index(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id) # pk = 로그인된 유저의 아이디. user_model에서 가져옴.
            following = user.following.all() # 그 유저의 모든 팔로잉 유저 가져옴.
            posts = models.Post.objects.filter(
                Q(author__in = following) | Q(author = user) # Q객체 사용해서 여러 조건 가능. or 조건 사용하기 위해 씀. feild 뒤에 '__in' 키워드 사용하면 팔로잉 유저가 여러명 있다면 해당 유저의 모든 포스트를 가져옴.
            ).order_by("-create_at")

            serializer = serializers.PostSerializer(posts, many=True) # 시리얼라이저로 모델에서 추출한 post 넘기기. 포스트는 여러개가 될 수 있으니 many=True 값 꼭 넣기!
            print(serializer.data) # 변경된 데이터 확인.

            return render(
                request,
                'posts/main.html',
                {"posts": serializer.data, "comment_form": comment_form}
            )

def post_create(request):
    # 게시물 등록을 위한 화면을 요청(GET 방식)
    if request.method == 'GET':
        form = CreatePostForm()
        return render(request, 'posts/post_create.html', {"form": form}) # template에 request와 form을 넘김.

    elif request.method == 'POST':
        if request.user.is_authenticated:
            # (user_model에서 user id를 가져와. -> 유저 객체 가져옴.)
            user = get_object_or_404(user_model, pk=request.user.id)

            # image = request.FILES['image']
            # caption = request.POST['caption']

            # # 포스트에 대한 객체 만들기
            # new_post = models.Post.objects.create(
            #     author = user,
            #     image = image,
            #     caption = caption
            # )

            # # 저장하기
            # new_post.save()

            # 요청받은 post data와 file을 form에 넘겨줌.
            form = CreatePostForm(request.POST, request.FILES)

            if form.is_valid(): # 유효성 검사 후,
                post = form.save(commit=False) # form 내용 저장. commit=false로 하면 db에 저장되지는 않음. 임시저장 느낌.
                post.author = user # post 테이블은 user가 외래키이기 때문에 반드시 명시해주어야 함.
                post.save() # db에 저장됨.
            else:
                print(form.errors)

            return redirect(reverse('posts:index'))

        else:
            return render(request, 'users/main.html')

def post_update(request, post_id):
    if request.user.is_authenticated:
        # 포스트 작성자 수정 요청 한 거 맞는지 작성자 체크
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user != post.author:
            return redirect(reverse('posts:index'))

        # 맞다면 수정을 위한 페이지를 요청하는 GET방식 요청.
        if request.method == 'GET':
            form = UpdatePostForm(instance=post)
            return render(
                request,
                'posts/post_update.html',
                {"form": form, "post":post}
            )

        elif request.method == 'POST':
            # 업데이트 버튼 클릭 후 저장을 위한 POST api 요청 로직.
            form = UpdatePostForm(request.POST)
            if form.is_valid():
                post.caption = form.cleaned_data['caption']
                post.save()

            return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')

def post_delete(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)
        if request.user == post.author:
            post.delete()

        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')

def comment_create(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(models.Post, pk=post_id)

        form = CommentForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False) # db에 저장 no!. 왜냐면 form에는댓글 내용만 있기 때문에 댓글 작성자와 댓글이 어느 포스트의 댓글인지에 대한 내용이 없음.
            comment.author = request.user # 댓글작성자
            comment.posts = post # 포스트
            comment.save() # db에 저장

            # 피드 페이지로 데이터 넘기기(posts앱의 index alias)
            # url 뒤에 '#' 다음에 입력된 값이 있다면 html에 그 값(id 선택자)이 있는 부분으로 스크롤이 내려감.
            return redirect(reverse('posts:index') + "#comment-" + str(comment.id))

        else:
            return render(request, 'users/main.html')

def comment_delete(request, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(models.Comment, pk=comment_id)
        if request.user == comment.author:
            comment.delete()

        return redirect(reverse('posts:index'))

    else:
        return render(request, 'users/main.html')

def post_like(request, post_id):
    # result란 key 값은 서버단과 클라이어튼 단에서 데이터 주고 받을 수 있게 약속된 걸 사용해야함. 우리만의 약속. hi라고 해도 됨. 단 맞춰주어야 함.
    response_body = {"result": ""}

    # 로그인 한 유저만 좋아요 클릴할 수 있도록 분기 처리.
    if request.user.is_authenticated:
        if request.method == "POST":

            # 현재 좋아요 상태인지 아닌지 db 조회하기.
            post = get_object_or_404(models.Post, pk=post_id)

            # 조회 조건 추가(filter 이용).
            # Post 테이블의 image_likes 컬럼은 User 모델임. 즉, user가 들어감.
            # image_likes를 조회한다 => user모델을 조회한다.
            # exists() -> user.id 가 있으면 True, 없으면 False
            existed_user = post.image_likes.filter(pk=request.user.id).exists()

            if existed_user:
                # 좋아요 누른 상태일 때는 "좋아요 취소."
                post.image_likes.remove(request.user) # db에 반영
                response_body['result'] = "dislike"
            else:
                # 좋아요가 아닐 때는 "좋아요."
                post.image_likes.add(request.user) # db에 반영
                response_body['result'] = "like"

            post.save()
            return JsonResponse(status=200, data=response_body)
    else:
        # 클라이언트에 데이터 넘겨줄 때 json 형태로 보내줘야 ajax 처리가 가능함.
        return JsonResponse(status=403, data=response_body) # 로그인 안 된 유저는 비어있는 결과값 보내기.

def search(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            searchKeyword = request.GET.get("q", "") # q키에 대한 값 가져오는 것. q 키에 대한 값이 없다면 두 번째 인자를 대신하여 받음.

            # 키워드를 검색하고 유저에게 피드 페이지를 보여주는 logic은 index logic과 굉장히 유사함!
            comment_form = CommentForm()

            user = get_object_or_404(user_model, pk=request.user.id)
            following = user.following.all()
            posts = models.Post.objects.filter(
                # 사용자가 입력한 내용이 보이게 추가해주자.
                # caption = ' ' 이렇게 입력하면 오로지 입력값과 일치한 값만 보이기 때문에,
                # __contatins 접미사를 사용하자.
                # (팔로잉한 게시물 또는 내가 작성한 게시물) and (searchKeyword가 포함된 게시물)
                (Q(author__in = following) | Q(author = user)) & Q(caption__contains=searchKeyword)
            ).order_by("-create_at")

            serializer = serializers.PostSerializer(posts, many=True) #
            print(serializer.data)

            return render(
                request,
                'posts/main.html',
                {"posts": serializer.data, "comment_form": comment_form}
            )
    else:
        return render(request, 'users/main.html')
