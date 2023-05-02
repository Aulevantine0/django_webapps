import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html

from . import models as payapp_models, utils as payapp_utils
from register import models as register_models


class UserTable(tables.Table):
    # action = tables.Column(empty_values=())
    created_at = tables.Column(verbose_name='Registration Date')

    def __init__(self, data, request=None, **kwargs):
        self.request = request
        super().__init__(data, **kwargs)

    class Meta:
        attrs = {"class": 'table table-stripped data-table table-xs',
                 'data-add-url': 'Url here'}
        model = register_models.UserProfile

        fields = ['user', 'currency', 'balance', 'created_at']

    # def render_action(self, record):
    #     return format_html("""
    #     <button class='btn btn-sm text-green' href='{approve}' onclick='approve_transaction_request(this)'><i class='fa fa-check'></i></button>
    #     <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
    #     """.format(
    #         approve=reverse("approve-transactionrequest", kwargs={"id": record.id}),
    #         delete=reverse("delete-transactionrequest", kwargs={"id": record.id}),
    #     )
    #     )


class TransactionAdminTable(tables.Table):
    # action = tables.Column(empty_values=())
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
        currency = record.sender.currency
        return '{amount} {currency}'.format(amount=record.amount, currency=currency)

    # def render_action(self, record):
    #     return format_html("""
    #     <button class='btn btn-sm text-danger delete-btn' href='{delete}' onclick='delete_func(this)'><i class='fa fa-trash'></i></button>
    #     """.format(
    #         delete=reverse("delete-transactions", kwargs={"id": record.id}),
    #     )
    #     )
