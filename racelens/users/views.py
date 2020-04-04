from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django import forms

from .forms import LoginForm, UserRegistrationForm


def login_view(request):
    """ /login """
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        next_url = request.GET.get("next")
        user = authenticate(request, username=username, password=password)


        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next_url or "/")
        else:
            form.add_error("username", forms.ValidationError("Su usuario o contraseña no son correctas."))
            form.add_error("password", "")
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form, "title": "Iniciar sesión"})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj["username"]
            email = userObj["email"]
            password = userObj["password"]
            name = userObj["name"]
            last_name = userObj["last_name"]
            
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                new_user = User.objects.create_user(username, email, password)
                new_user.first_name = name
                new_user.last_name = last_name
                new_user.save()

                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                if User.objects.filter(username=username).exists():
                    form.add_error("username", forms.ValidationError("El usuario ya existe."))
                if User.objects.filter(email=email).exists():
                    form.add_error("email", "Ya hay una cuenta con ese correo.")
    else:
        form = UserRegistrationForm()

    return render(request, "users/login.html", {"form": form, "title": "Registrate"})
