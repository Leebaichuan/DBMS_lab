from django.contrib import admin

# Register your models here.
from .models import DepositAccount, CheckAccount

admin.site.register(DepositAccount)
admin.site.register(CheckAccount)