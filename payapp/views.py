from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_tables2 import RequestConfig

from . import tables as payapp_tables
from . import forms as payapp_forms
from . import urls as payapp_urls, models as payapp_models, utils as payapp_utils


# Create your views here.

@login_required
@csrf_exempt
def all_notifications(request):
    context = {
        "title": "List of Notifications",
        "page_name": "Notifications",
        "queryset": [],
        "table": payapp_tables.NotificationTable(
            payapp_models.Notification.objects.filter(userprofile=request.user.userprofile).order_by('-id')),
        "add_url": payapp_urls.add_transaction(),

        'nav_conf': {
            'active_classes': ['notifications', 'notifications'],
            'collapse_class': 'notifications',
        },
    }
    return render(request, "home/tables.html", context)


@login_required
@csrf_exempt
def all_request_transactions(request):
    data = payapp_tables.TransactionRequestTable(
        payapp_models.TransactionRequest.objects.filter(amount_sender=request.user.userprofile,
                                                        accepted_by_sender=False).order_by('-id'))

    RequestConfig(request).configure(data)
    context = {
        "title": "Received Transaction Requests",
        'balance_details': 'Your balance amount is: {amount} {currency}'.format(
            amount=round(request.user.userprofile.balance, 2),
            currency=request.user.userprofile.currency),
        "page_name": "Transactions",
        "queryset": [],
        "table": data,
        "add_url": payapp_urls.add_transaction(),
        "header": {
            "links": [
                {
                    "title": "Make New Transaction Request",
                    "href": payapp_urls.add_transaction_request(),
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
def all_transactions(request):
    data = payapp_tables.TransactionTable(payapp_models.Transaction.objects.filter(
        Q(sender=request.user.userprofile) | Q(receiver=request.user.userprofile)).order_by('-id'))
    RequestConfig(request).configure(data)
    context = {
        "title": "List of Transactions",
        'balance_details': 'Your balance amount is: {amount} {currency}'.format(amount=request.user.userprofile.balance,
                                                                                currency=request.user.userprofile.currency),
        "page_name": "Transactions",
        "queryset": [],
        "table": data,
        "add_url": payapp_urls.add_transaction(),
        "header": {
            "links": [
                {
                    "title": "Make New Transaction",
                    "href": payapp_urls.add_transaction(),
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
def add_transaction_request(request):
    if request.method == 'POST':
        form = payapp_forms.TransactionRequestForm(request.POST)
        if form.is_valid():
            if request.user.userprofile.id == int(request.POST.get('amount_sender')):
                messages.error(request, 'You cannot make transaction request to yourself')
                return redirect('add-transactions-request')
            transaction_request = form.save()
            transaction_request.amount_receiver = request.user.userprofile
            transaction_request.save()
            sender_notification_message = f"You have received a new Payment request from {request.user.get_full_name()}"
            sender_notification = payapp_models.Notification.objects.create(
                userprofile_id=request.POST.get('amount_sender'), message=sender_notification_message,
            )
            return redirect('all-transactions')
        else:
            messages.error(request, 'Form is not valid')
    context = {
        "title": "Request Transaction",
        "page_name": "Request Transaction",
        "form": payapp_forms.TransactionRequestForm(),
        "back_url": payapp_urls.all_request_transaction(),
        'balance_details': 'Your balance amount is: {amount} {currency}'.format(
            amount=round(request.user.userprofile.balance, 2),
            currency=request.user.userprofile.currency),
        "forms": [
            {
                "title": "Request Transaction",
                "form": payapp_forms.TransactionRequestForm()
            },
        ],
        "header": {
            "links": [
            ],
        },
        'nav_conf': {
            'active_classes': ['transactions', 'transactions'],
            'collapse_class': 'transactions',
        },
    }
    return render(request, "laboratories/add.html", context=context)


@login_required
@csrf_exempt
def add_transactions(request):
    if request.method == 'POST':
        form = payapp_forms.TransactionForm(request.POST)
        if form.is_valid():
            if request.user.userprofile.id == int(request.POST.get('receiver')):
                messages.error(request, 'You cannot make transaction to yourself')
                return redirect('add-transactions')
            converted_amount = payapp_utils.convert_amount_and_proceed_transaction(request)
            if not converted_amount[0]:
                messages.error(request, converted_amount[1])
                return redirect('add-transactions')
            send_notification = payapp_utils.send_notification_to_both_users(request, converted_amount[1])
            transaction = form.save()
            transaction.sender = request.user.userprofile
            transaction.save()
            send_notification[0].transaction = transaction
            send_notification[1].transaction = transaction
            send_notification[0].save()
            send_notification[1].save()

            return redirect('all-transactions')
        else:
            messages.error(request, 'Form is not valid')
    context = {
        "title": "Add Transaction",
        "page_name": "Add Transaction",
        "form": payapp_forms.TransactionForm(),
        "back_url": payapp_urls.all_transaction(),
        'balance_details': 'Your balance amount is: {amount} {currency}'.format(amount=request.user.userprofile.balance,
                                                                                currency=request.user.userprofile.currency),
        "forms": [
            {
                "title": "Test Info",
                "form": payapp_forms.TransactionForm()
            },
        ],
        "header": {
            "links": [
            ],
        },
        'nav_conf': {
            'active_classes': ['transactions', 'transactions'],
            'collapse_class': 'transactions',
        },
    }
    return render(request, "laboratories/add.html", context=context)


@login_required
@csrf_exempt
def delete_transactions(request, id):
    try:
        transactions = get_object_or_404(payapp_models.Transaction, id=id)
        payapp_models.Notification.objects.filter(transaction=transactions).delete()
        transactions.delete()
        return JsonResponse({'success': True}, safe=False)
    except:
        return JsonResponse({'success': False}, safe=False)


@login_required
@csrf_exempt
def delete_transaction_request(request, id):
    try:
        transactions = get_object_or_404(payapp_models.TransactionRequest, id=id)
        transactions.delete()
        return JsonResponse({'success': True}, safe=False)
    except:
        return JsonResponse({'success': False}, safe=False)


@login_required
@csrf_exempt
def approve_transaction_request(request, id):
    try:
        transaction_request_obj = get_object_or_404(payapp_models.TransactionRequest, id=id)
        initial_converted_amount = payapp_utils.get_converted_amount(transaction_request_obj.amount_receiver.currency,
                                                                     transaction_request_obj.amount_sender.currency,
                                                                     transaction_request_obj.amount)
        converted_amount = payapp_utils.get_converted_amount(transaction_request_obj.amount_sender.currency,
                                                             transaction_request_obj.amount_receiver.currency,
                                                             initial_converted_amount)
        deduct_amount = payapp_utils.deduct_amount_from_sender_account(transaction_request_obj.amount_sender,
                                                                       round(initial_converted_amount, 2))
        if not deduct_amount[0]:
            return deduct_amount
        payapp_utils.add_amount_to_receiver_account(transaction_request_obj.amount_receiver, converted_amount)
        if not converted_amount:
            messages.error(request, 'Something went wrong in conversion of amount')
            return redirect('all-request-transactions')
        transaction_obj = payapp_models.Transaction.objects.create(sender=transaction_request_obj.amount_sender,
                                                                   receiver=transaction_request_obj.amount_receiver,
                                                                   amount=round(initial_converted_amount, 2))
        sender_message = f"You have Made a Transaction of {round(initial_converted_amount, 2)}{transaction_request_obj.amount_sender.currency} to {transaction_request_obj.amount_receiver.user.get_full_name()}"
        receiver_message = f"You have received an amount of {round(converted_amount, 2)}{transaction_request_obj.amount_receiver.currency} from {transaction_request_obj.amount_sender.user.get_full_name()}"
        sender_notification = payapp_models.Notification.objects.create(
            userprofile=transaction_request_obj.amount_sender, message=sender_message,
            amount_send=True,
            amount=round(initial_converted_amount, 2))
        receiver_notification = payapp_models.Notification.objects.create(
            userprofile=transaction_request_obj.amount_receiver,
            message=receiver_message,
            amount_received=True,
            amount=round(converted_amount, 2))
        sender_notification.transaction = transaction_obj
        receiver_notification.transaction = transaction_obj
        sender_notification.save()
        receiver_notification.save()
        transaction_request_obj.accepted_by_sender = True
        transaction_request_obj.save()
        return JsonResponse({'success': True}, safe=False)
    except:
        return JsonResponse({'success': False}, safe=False)
