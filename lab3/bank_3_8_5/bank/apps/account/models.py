# apps/account/models.py
# relational schema for account

from django.db import models
from django.utils import timezone
from django.urls import reverse

from apps.user.models import User
from apps.subbank.models import Subbank, Employee


# the base entity of Account
# account has two types: deposit_account and check_account
# note that an account can be shared by multiple clients
# one client can at most have one deposit_account and one check_account
# in one subbank
class AccountBase(models.Model):
    ID = models.CharField(max_length = 20, primary_key = True)
    # the AccountBase is issued by a Subbank
    Subbank = models.ForeignKey(
        Subbank,
        on_delete = models.CASCADE,
        null = True
    )
    # The many-to-many key of User
    Users = models.ManyToManyField(User)
    
    Money = models.DecimalField(max_digits = 20, decimal_places = 2)
    RegDate = models.DateTimeField(null = True)
    
    # the Account is managed by a bank employee
    Manager = models.ForeignKey(
        Employee,
        on_delete = models.CASCADE,
        null = True
    )

    class Meta:
        abstract = True
        ordering = ['-RegDate']

    def __str__(self):
        return self.ID
        

# the entity of deposit account, which inherit the base account
class DepositAccount(AccountBase):
    InterestRate = models.DecimalField(max_digits = 5, decimal_places = 2)
    # here we only have two choices of currency
    CurrencyType = models.IntegerField(choices = \
        (   (1, 'RMB'),  \
            (2, 'US DOLLAR') ) )


# the entity of check account, which inherit the base account
class CheckAccount(AccountBase):
    OverDraft = models.DecimalField(max_digits = 20, decimal_places = 2)
