from register import models as register_models
from . import models as payapp_models


def get_converted_amount(sender_currency, receiver_currency, amount):
    amount = float(amount)
    if sender_currency == receiver_currency:
        return amount
    if sender_currency == register_models.usd and receiver_currency == register_models.euro:
        return amount * 0.9
    if sender_currency == register_models.usd and receiver_currency == register_models.gbp:
        return amount * 0.8
    if sender_currency == register_models.euro and receiver_currency == register_models.usd:
        return amount * 1.11
    if sender_currency == register_models.euro and receiver_currency == register_models.gbp:
        return amount * 0.88
    if sender_currency == register_models.gbp and receiver_currency == register_models.usd:
        return amount * 1.26
    if sender_currency == register_models.gbp and receiver_currency == register_models.euro:
        return amount * 1.13


def deduct_amount_from_sender_account(sender, amount):
    if sender.balance > float(amount):
        sender.balance -= float(amount)
        sender.save()
        return True, 'All Good'
    else:
        return False, 'Sender has Insufficient Balance'


def add_amount_to_receiver_account(receiver, amount):
    receiver.balance += float(amount)
    receiver.save()


def convert_amount_and_proceed_transaction(request):
    # try:
    sender = request.user.userprofile
    receiver = register_models.UserProfile.objects.filter(id=request.POST.get('receiver')).last()
    amount = request.POST.get('amount')
    converted_amount = get_converted_amount(sender.currency, receiver.currency, amount)
    deduct_amount = deduct_amount_from_sender_account(sender, amount)
    if not deduct_amount[0]:
        return deduct_amount
    add_amount_to_receiver_account(receiver, converted_amount)

    return True, converted_amount


def send_notification_to_both_users(request, converted_amount):
    sender = request.user.userprofile
    receiver = register_models.UserProfile.objects.filter(id=request.POST.get('receiver')).last()
    amount = request.POST.get('amount')
    sender_message = f"You have Made a Transaction of {amount}{sender.currency} to {receiver.user.get_full_name()}"
    receiver_message = f"You have received an amount of {round(converted_amount, 2)}{receiver.currency} from {sender.user.get_full_name()}"
    sender_notification = payapp_models.Notification.objects.create(userprofile=sender, message=sender_message,
                                                                    amount_send=True,
                                                                    amount=amount)
    receiver_notification = payapp_models.Notification.objects.create(userprofile=receiver, message=receiver_message,
                                                                      amount_received=True,
                                                                      amount=round(converted_amount, 2))
    return sender_notification, receiver_notification
