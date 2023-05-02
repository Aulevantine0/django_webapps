from django.db import models
from django.contrib.auth.models import User

usd = 'USD'
gbp = 'GBP'
euro = 'EURO'
currency_choices = [
    (usd, usd),
    (gbp, gbp),
    (euro, euro)
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    currency = models.CharField(max_length=100, choices=currency_choices, null=True, blank=True)
    balance = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.user.username
