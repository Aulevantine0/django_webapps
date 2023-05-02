from django.urls import path, reverse
from . import views as payapp_views, admin_views as admin_view

urlpatterns = [
    path('all-notifications', payapp_views.all_notifications, name='all-notifications'),
    path('all-transactions', payapp_views.all_transactions, name='all-transactions'),
    path('all-request-transactions', payapp_views.all_request_transactions, name='all-request-transactions'),
    path('add-transactions', payapp_views.add_transactions, name='add-transactions'),
    path('add-transaction-request', payapp_views.add_transaction_request, name='add-transactions-request'),
    path('delete-transactions/<int:id>', payapp_views.delete_transactions, name='delete-transactions'),
    path('delete-transactionrequest/<int:id>', payapp_views.delete_transaction_request,
         name='delete-transactionrequest'),
    path('approve-transactionrequest/<int:id>', payapp_views.approve_transaction_request,
         name='approve-transactionrequest'),
    #     ==========ADMIN URLS==========
    path('all-users', admin_view.all_users, name='all-users'),
    path('all-admin', admin_view.add_admin, name='add-admin'),
    path('all-transactions-admin', admin_view.all_transactions_admin, name='all-transactions-admin'),
]


def all_transaction():
    return reverse("all-transactions")


def all_request_transaction():
    return reverse("all-request-transactions")


def all_notifications():
    return reverse("all-notifications")


def add_transaction():
    return reverse("add-transactions")


def add_admin():
    return reverse("add-admin")


def add_transaction_request():
    return reverse("add-transactions-request")


def delete_transaction():
    return reverse("add-transactions")


def delete_transactionsrequest():
    return reverse("delete-transactionrequest")


def approve_transactions_request():
    return reverse("approve-transactionrequest")

# def add_transaction():
#     return reverse("add-transactions")
