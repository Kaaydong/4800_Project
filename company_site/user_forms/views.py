from django.shortcuts import render, redirect 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm 
from django.contrib.auth import login, logout, get_user_model

from . import models

# Create your views here.
def register_page(request):
    if request.method == "POST": 
        form = UserCreationForm(request.POST) 
        if form.is_valid(): 
            login(request, form.save())

            # Create Settings instance for new User
            user = get_user_model().objects.get(id=request.user.id)
            settings_instance = models.Settings(user_key=user)
            settings_instance.save()

            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "user_forms/register.html", { "form": form })


def login_page(request): 
    if request.method == "POST": 
        form = AuthenticationForm(data=request.POST)
        if form.is_valid(): 
            login(request, form.get_user())
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect("/")
    else: 
        form = AuthenticationForm()
    return render(request, "user_forms/login.html", { "form": form })


def logout_view(request):
    logout(request) 
    return redirect("/")


def account_settings_page(request):
    if request.user.is_authenticated:
        # Render info if User is logged in
        account_info = [request.user.username]
    else:
        return redirect("/users/login")
    
    return render(request, "user_forms/account_settings.html", {'ACCOUNT_INFO': account_info})