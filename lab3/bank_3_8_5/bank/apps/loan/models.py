# apps/loan/models.py
# relational schema for loan and payment
from django.db import models
from django.utils import timezone
from django.urls import reverse

from apps.subbank.models import Subbank,Employee
from apps.user.models import User

## the entity of loan
class Loan(models.Model):
    ID = models.CharField(max_length = 20, primary_key = True)
    # the Loan is issued by a Subbank
    Subbank = models.ForeignKey(
        Subbank, 
        related_name = 'Loan_issued_by_Subbank',
        on_delete = models.CASCADE
    )
    Money = models.DecimalField(max_digits = 20, decimal_places = 2)
    # the Loan is owned by a User
    User = models.ForeignKey(
        User,
        related_name = 'Loan_owned_by_User',
        on_delete = models.CASCADE,
        null = True
    )
    CreatedDate = models.DateField(null = True, blank = True)
    # the Loan is managed by a bank employee
    Manager = models.ForeignKey(
        Employee,
        related_name = "Loan_managed_by_Employee",
        on_delete = models.CASCADE,
        null = True
    )

    def __str__(self):
        return self.ID

    class Meta:
        ordering = ['-CreatedDate']

# the entity of payment
class Payment(models.Model):
    # Payment pays for a Loan
    Loan = models.ForeignKey(
        Loan, 
        related_name = 'Payment_pays_for_Loan',
        on_delete = models.CASCADE
    )
    PayDate = models.DateField(null = True, blank = True)
    PayMoney = models.DecimalField(max_digits = 20, decimal_places = 2)
    
    class meta:
        ordering = ['-PayDate']
