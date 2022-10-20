from django.shortcuts import redirect, render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model


# Create your views here.
def signup(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 회원가입 후 자동로그인
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect("articles:index")
    else:
        form = AuthenticationForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)


def logout(request):
    auth_logout(request)
    return redirect("articles:index")


def index(request):

    users = get_user_model().objects.all()

    context = {
        "users": users,
    }

    return render(request, "accounts/index.html", context)


def detail(request, user_pk):

    user = get_user_model().objects.get(pk=user_pk)

    context = {
        "user": user,
    }
    return render(request, "accounts/detail.html", context)


# 관리자가 회원 정보 확인할 때
def update(request, user_pk):

    user = get_user_model().objects.get(pk=user_pk)

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=user)
        # form = CustomUserChangeForm(data=request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail", user.pk)
    else:
        form = CustomUserChangeForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "accounts/update.html", context)


# 로그인한 유저의 본인 정보 수정
def update2(request):

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        # form = CustomUserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("accounts:detail")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }

    return render(request, "accounts/update.html", context)


from django.contrib.auth import update_session_auth_hash


def change_password(request):

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        # form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("accounts:detail")
    else:
        form = PasswordChangeForm(request.user)
    context = {
        "form": form,
    }

    return render(request, "accounts/change_password.html", context)


def delete(request):
    request.user.delete()
    auth_logout(request)

    return redirect("accounts:index")
