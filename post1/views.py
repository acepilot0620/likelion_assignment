from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib import auth
from .models import Post,Account

# Create your views here.
def home(request):
    post_list = Post.objects.all()
    return render(request, 'post/index.html',{'post_list':post_list})

def create(request):
    if request.method == 'POST':
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.save()
        return redirect('home')
    else:
        return render(request,'post/create.html')

def detail(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request,'post/generic.html',{'post':post})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=email, password=password)
        nickname = Account.objects.get(user=user).nickname

        # 로그인에 실패한 경우
        if user is None:
            messages.info(request, ": 회원정보가 일치하지 않습니다. 다시 시도해주세요")
            return redirect('login')

        auth.login(request, user)
        return render(request, 'post/index.html', { 'nickname': nickname })
    else:
        return render(request, 'post/login.html')

def logout(request):
    auth.logout(request)
    return render(request, 'post/index.html')

def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        nickname = request.POST.get('nickname')
        
        # 입력 값이 비어있을 때
        if nickname == "" or email == "" or password == "":
            messages.info(request,"회원가입 정보를 모두 기입해주세요.")
            return redirect('signup')

        # 비밀번호가 다를 때
        if not password == password_confirm:
            messages.info(request, ": 비밀번호가 다릅니다.")
            return redirect('signup')
        
        # Validation 성공한 경우
        user = User.objects.create_user(username=email, password=password)
        account = Account(user=user, email=email, nickname=nickname)
        account.save()
        return redirect('home')
    else:
        return render(request, 'post/signup.html')
