from django import forms
from . import models as payapp_models


class TransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = payapp_models.Transaction
        fields = ['receiver', 'amount', ]


class TransactionRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount_sender'].label = 'Send To'

    class Meta:
        model = payapp_models.TransactionRequest
        fields = ['amount_sender', 'amount', ]
