from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

# from djangogram.users.forms import SignUpForm
from .forms import SignUpForm

def main(request):
    if request.method == 'GET':
        return render(request, 'users/main.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect(reverse('posts:index'))

        else:
            # Return an 'invalid login' error message.
            return render(request, 'users/main.html')

def signup(request):
    if request.method == 'GET':
        form = SignUpForm()

        # render한다 (request를, 'html로', {context 내용을.})
        return render(request, 'users/signup.html', {'form': form})

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid(): # is_valid() : 장고 폼의 유효성 검사 함수.
            form.save() # user db에 데이터 저장.

            # 자동 로그인 기능 만들기.
            # 저장된 데이터 불러오기.
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # 기존에 만든 로그인 logic 가져오기.
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect(reverse('posts:index'))

        return render(request, 'users/main.html')
