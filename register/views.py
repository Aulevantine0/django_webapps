from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth.models import User
from .forms import LoginForm, RegisterForm
from register import models as register_models


# Create your views here.
@login_required
def account_logout(request):
    logout(request)
    return redirect("login")


def account_register(request):
    form = RegisterForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            currency = form.cleaned_data.get("currency")

            if currency == '1':
                currency_name = register_models.usd
                balance = 1000 * 1.11
            elif currency == '2':
                currency_name = register_models.gbp
                balance = 1000 * 0.88
            elif currency == '3':
                currency_name = register_models.euro
                balance = 1000
            else:
                currency_name = None
                balance = None

            user_obj = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            register_models.UserProfile.objects.create(user=user_obj, currency=currency_name,
                                                       balance=balance)
            messages.success(request, "Signup Successfully!")
            return redirect("login")
        else:
            messages.error(request, "Error validating the form")
    return render(request, "accounts/login.html",
                  {
                      "form": form,
                      "msg": msg,
                      "title": "Signup",
                      "subtitle": "Add your Details",
                      "btn_title": "Sign Up",
                      'signup_flag': True
                  }
                  )


@csrf_exempt
def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                user: User
                if user.is_staff:
                    messages.success(request, "Welcome Admin!")
                    return redirect('all-users')
                messages.success(request, "Welcome User!")
                return redirect('all-transactions')
            else:
                messages.error(request, "Email or Password not correct!")
        else:
            messages.error(request, "Error validating the form")
    return render(request, "accounts/login.html",
                  {
                      "form": form,
                      "msg": msg,
                      "title": "Login",
                      "subtitle": "Add your credentials",
                      "btn_title": "Sign in"
                  }
                  )


def redirect_to_webapps2023(request):
    return redirect('/webapps2023/')
