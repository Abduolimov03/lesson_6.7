from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Parollar tog‘ri kelmadi')
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Bu username orqali oldin ro‘yxatdan o‘tilgan')
            return redirect('signup')

        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1
        )
        messages.success(request, 'Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz')
        return redirect('login')

    return render(request, 'account/signup.html')

@login_required(login_url='login')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        if not username or not password:
            messages.error(request, 'Login yoki parol kiritilmadi')
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Siz login qildingiz')
            return redirect('index')

        messages.error(request, 'bunaqa user topilmadi ')

        return redirect('login')


    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Siz dasturdan chiqdingiz')
    return redirect('index')