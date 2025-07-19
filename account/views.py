from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from account.forms import SignUpForm, LoginForm, ChangePassForm
from .utils import generate_code, send_to_mail


# @login_required(login_url='login')
# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#         password1 = request.POST['password1']
#         password2 = request.POST['password2']
#
#         if password1 != password2:
#             messages.error(request, 'Parollar tog‘ri kelmadi')
#             return redirect('signup')
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Bu username orqali oldin ro‘yxatdan o‘tilgan')
#             return redirect('signup')
#
#         User.objects.create_user(
#             username=username,
#             first_name=first_name,
#             last_name=last_name,
#             email=email,
#             password=password1
#         )
#         messages.success(request, 'Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz')
#         return redirect('login')
#
#     return render(request, 'account/signup.html')
#
# @login_required(login_url='login')
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#
#
#         if not username or not password:
#             messages.error(request, 'Login yoki parol kiritilmadi')
#             return redirect('login')
#
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, 'Siz login qildingiz')
#             return redirect('index')
#
#         messages.error(request, 'bunaqa user topilmadi ')
#
#         return redirect('login')
#
#
#     return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Siz dasturdan chiqdingiz')
    return redirect('index')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Bu username orqali oldin ro‘yxatdan o‘tilgan')
                return redirect('signup')
            form.save()
            messages.success(request, 'Siz muvaffaqiyatli ro‘yxatdan o‘tdingiz')
            return redirect('login')
        else:
            messages.error(request, 'Nimadur xatolik ketdi')
    else:
        form = SignUpForm()
    return render(request, 'account/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Siz muvaffaqiyatli tizimga kirdingiz')
            return redirect('index')
        else:
            messages.error(request, 'Login yoki parol noto‘g‘ri')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'account/profile.html', {'user':user})

@login_required
def change_pass_view(request):
    if request.method == 'GET':
        code = generate_code()
        request.session['verification_code'] = code
        send_to_mail(request.user.email, code)
        messages.info(request, 'Emailingizga tasdiqlash kodi yuborildi.')
        form = ChangePassForm()
        return render(request, 'account/change_pass.html', {'form': form})

    else:
        form = ChangePassForm(request.POST)
        if form.is_valid():
            old_pass = form.cleaned_data['old_pass']
            new_pass = form.cleaned_data['new_pass']
            confirm_pass = form.cleaned_data['confirm_pass']
            code = form.cleaned_data['code']
            session_code = request.session.get('verification_code')

            if not request.user.check_password(old_pass):
                messages.error(request, 'Eski parol noto‘g‘ri.')
                return render(request, 'account/change_pass.html', {'form': form})

            if new_pass != confirm_pass:
                messages.error(request, 'Parollar mos emas.')
                return render(request, 'account/change_pass.html', {'form': form})

            if session_code != code:
                messages.error(request, 'Tasdiqlash kodi noto‘g‘ri.')
                return render(request, 'account/change_pass.html', {'form': form})

            user = request.user
            user.set_password(new_pass)
            user.save()

            messages.success(request, 'Parolingiz muvaffaqiyatli o‘zgartirildi. Iltimos, qaytadan tizimga kiring.')
            return redirect('login')

        else:
            return render(request, 'account/change_pass.html', {'form': form})