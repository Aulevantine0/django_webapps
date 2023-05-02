import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from . import models as payapp_models, utils as payapp_utils


class TransactionTable(tables.Table):
    action = tables.Column(empty_values=())
    amounts = tables.Column(empty_values=())
    created_at = tables.Column(verbose_name='Time')

    def __init__(self, data, request=None, **kwargs):
        self.request = request
        super().__init__(data, **kwargs)

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = payapp_models.Transaction

        fields = ['sender', 'receiver', 'amounts', 'created_at']

    def render_amounts(self, value, record):
        record: payapp_models.Transaction
        currency = self.request.user.userprofile.currency
        sender_currency = record.sender.currency
        receiver_currency = record.receiver.currency
        amount = record.amount
        converted_amount = payapp_utils.get_converted_amount(sender_currency, currency, amount)
        return round(converted_amount, 2)

    def render_action(self, record):
        return format_html("""
        <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
        """.format(
            delete=reverse("delete-transactions", kwargs={"id": record.id}),
        )
        )


class NotificationTable(tables.Table):
    # action = tables.Column(empty_values=())
    created_at = tables.Column(verbose_name='Time')
    userprofile = tables.Column(verbose_name='Name')
    message = tables.Column(verbose_name='Details')

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = payapp_models.Notification
        fields = ['userprofile', 'message', 'amount', 'created_at']

    # def render_action(self, record):
    #     return format_html("""
    #     <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
    #     """.format(
    #         delete=reverse("delete-transactions", kwargs={"id": record.id}),
    #     )
    #     )


class TransactionRequestTable(tables.Table):
    action = tables.Column(empty_values=())
    amounts = tables.Column(empty_values=())
    amount_receiver = tables.Column(verbose_name='Requested By')
    created_at = tables.Column(verbose_name='Time')

    def __init__(self, data, request=None, **kwargs):
        self.request = request
        super().__init__(data, **kwargs)

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = payapp_models.TransactionRequest

        fields = ['amount_receiver', 'amounts', 'created_at']

    def render_amounts(self, value, record):
        record: payapp_models.TransactionRequest
        currency = self.request.user.userprofile.currency
        receiver_currency = record.amount_receiver.currency
        # receiver_currency = record.receiver.currency
        amount = record.amount
        converted_amount = payapp_utils.get_converted_amount(receiver_currency, currency, amount)
        return round(converted_amount, 2)

    def render_action(self, record):
        return format_html("""
        <button class='btn btn-sm text-green' href='{approve}' onclick='approve_transaction_request(this)'><i class='fa fa-check'></i></button>
        <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
        """.format(
            approve=reverse("approve-transactionrequest", kwargs={"id": record.id}),
            delete=reverse("delete-transactionrequest", kwargs={"id": record.id}),
        )
        )
