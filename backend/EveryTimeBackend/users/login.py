from django.contrib.auth import authenticate, login
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 로그인 성공 시
            return HttpResponse("로그인 성공")
        else:
            # 로그인 실패 시
            return HttpResponse("로그인 실패")
    else:
        return HttpResponse("0")