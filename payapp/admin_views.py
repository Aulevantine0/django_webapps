from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig

from . import tables as payapp_tables
from . import forms as payapp_forms
from . import urls as payapp_urls, models as payapp_models, utils as payapp_utils, admin_tables as admin_table, \
    admin_forms as admin_form
from register import models as register_models
from django.contrib.auth.models import User


@login_required
@csrf_exempt
def all_users(request):
    data = admin_table.UserTable(register_models.UserProfile.objects.all().order_by('-id'))
    RequestConfig(request).configure(data)
    context = {
        'is_admin': True,
        "title": "All Users",
        "page_name": "All Users",
        "queryset": [],
        "table": data,
        "add_url": payapp_urls.add_admin(),
        "header": {
            "links": [
                {
                    "title": "Add Admin",
                    "href": payapp_urls.add_admin(),
                    "classes": "btn btn-sm btn-outline-success",
                    "icon": "fa fa-plus"
                },

            ],
        },

        'nav_conf': {
            'active_classes': ['admin-settings', 'payapps'],
            'collapse_class': 'payapps',
        },
    }
    return render(request, "home/tables.html", context)


@login_required
@csrf_exempt
def add_admin(request):
    form = admin_form.RegisterForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user_obj = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
            user_obj.set_password(password)
            user_obj.is_staff = True
            user_obj.save()
            messages.success(request, "Signup Successfully!")
            return redirect("all-users")
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


@login_required
@csrf_exempt
def all_transactions_admin(request):
    data = admin_table.TransactionAdminTable(payapp_models.Transaction.objects.all().order_by('-id'))
    RequestConfig(request).configure(data)
    context = {
        'is_admin': True,
        "title": "All Transactions",
        "page_name": "Transactions",
        "queryset": [],
        "table": data,
        # "add_url": payapp_urls.add_transaction(),
        "header": {
            # "links": [
            #     {
            #         "title": "Make New Transaction",
            #         "href": payapp_urls.add_transaction(),
            #         "classes": "btn btn-sm btn-outline-success",
            #         "icon": "fa fa-plus"
            #     },
            #
            # ],
        },

        'nav_conf': {
            'active_classes': ['admin-settings', 'payapps'],
            'collapse_class': 'payapps',
        },
    }
    return render(request, "home/tables.html", context)
