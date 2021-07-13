from django.contrib import admin

# Register your models here.
from .models import Loan, Payment

admin.site.register(Loan)
admin.site.register(Payment)