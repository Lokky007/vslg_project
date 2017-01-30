from django.shortcuts import render, redirect

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserLoginForm

# Login - check and redirect
def Login(request):
    loginForm = UserLoginForm(request.POST or None)
    if loginForm.is_valid():
        username = loginForm.cleaned_data.get("username")
        password = loginForm.cleaned_data.get("passsword")
        user = authenticate(username=username, password=password)
        print user, username, password
        login(request, user)
        if request.user.is_authenticated():
            return redirect('/main/')

    return render(request, 'polls/registration/login.html', {"loginForm": loginForm})

# Register - check data and if correct, redirect.
def Register(request):
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("user_login")
        password = form.cleaned_data.get("user_pass")
        fname = form.cleaned_data.get("user_name")
        lname = form.cleaned_data.get("user_last_name")
        email = form.cleaned_data.get("user_email")

        user = User.objects.create_user(username, email, password, last_name=lname, first_name=fname)
        return render(request, 'polls/registration/success.html', {"username": username})

    return render(request, 'polls/registration/register.html', {"form": form})

# Logout function for destroy relation
def Logout (request):
    logout(request)
    return render(request, 'polls/registration/logout.html')
