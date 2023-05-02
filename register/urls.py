from django.urls import path, reverse

from . import views as account_views

urlpatterns = [
    path("logout", account_views.account_logout, name="logout"),
    path("register/", account_views.account_register, name="register"),
    path("", account_views.login_view, name="login"),
]
