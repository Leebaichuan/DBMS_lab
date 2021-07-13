# apps/loan/forms.py: stores the form class for Loan Append 
#                       and a payment

from django import forms
from .models import Loan

# the form to record the info to append user
# requires: Loan,ModelForm
class LoanAppendForm(forms.ModelForm):
    
    # the User model
    class Meta:
        model = Loan
        fields = ( 'ID', 'Subbank', 'Money', \
            'User', 'CreatedDate', 'Manager')

    # save this form
    def save(self, commit = True):
        # Save the provided password in hashed format
        loan = super().save(commit = False)
        if commit:
            loan.save()
        return loan

# the form to record the info to append user
# requires: Form
class MoneyForm(forms.Form):
    PayMoney = forms.DecimalField(max_digits = 20, decimal_places = 2)
