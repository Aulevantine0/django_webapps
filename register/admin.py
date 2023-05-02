from django.contrib import admin

# Register your models here.

from .models import *
from . import models as account_models

admin.site.register(UserProfile)
