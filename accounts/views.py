from django.shortcuts import redirect, render

# from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.
def signup(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("articles:index")
    else:
        form = CustomUserCreationForm()
    context = {
        "form": form,
    }

    return render(request, "accounts/signup.html", context)


def login(request):

    form = AuthenticationForm()

    context = {
        "form": form,
    }

    return render(request, "accounts/login.html", context)
