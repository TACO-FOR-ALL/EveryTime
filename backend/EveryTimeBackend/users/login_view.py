from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def my_login_view(request):
    if request.method == "POST":        # "POST" 는 웹 개발에서 데이터를 request body에 담아 서버로 보내는 방식. GET보다 보안에 민감
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 성공 후 리다이렉트
            return redirect('home')
        else:
            # 실패 시 메시지와 함께 다시 로그인 페이지로
            return render(request, 'login.html', {'error': '아이디 또는 비밀번호가 잘못되었습니다.'})
    else:
        return render(request, 'login.html')
