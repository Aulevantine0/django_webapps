from django.db import models
# Create your models here.
from register import models as register_models


class Transaction(models.Model):
    sender = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='sender_user')
    receiver = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='receiver_user')
    amount = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.sender.user.get_full_name()


class TransactionRequest(models.Model):
    '''
    In this model, sender will get a request from receiver and sender need to accept the request in order to proceed
    with the transaction
    '''
    amount_sender = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='amount_sender_user')
    amount_receiver = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE, null=True, blank=True,
                                        related_name='amount_receiver_user')
    amount = models.FloatField(null=True, blank=True)
    accepted_by_sender = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.amount_receiver.user.get_full_name()


class Notification(models.Model):
    '''
    In this model all the trnasaction Notification will be available.
    '''
    userprofile = models.ForeignKey('register.UserProfile', on_delete=models.CASCADE, null=True, blank=True)
    transaction = models.ForeignKey('payapp.Transaction', on_delete=models.CASCADE, null=True, blank=True)
    message = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    amount_send = models.BooleanField(null=True, blank=True, default=False)
    amount_received = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.userprofile.user.get_full_name()
