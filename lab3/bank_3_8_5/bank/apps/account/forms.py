# apps/account/forms.py: stores the form class for appending accounts

from django import forms
from .models import DepositAccount, CheckAccount
from apps.user.models import User

# the form to append a DepositAccount
# requires: ModelForm, DepositAccount
class DepositAccountAppendForm(forms.ModelForm):
    
    class Meta:
        model = DepositAccount
        fields = [ 'ID', 'Subbank', 'Users', 'Money', \
            'RegDate', 'InterestRate', 'CurrencyType', 'Manager']
    
    Users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = True
    )

    # save this form
    def save(self, commit = True):
        deposit_account = super().save(commit = False)
        if commit:
            deposit_account.save()
        return deposit_account

# the form to append a CheckAccount
# requires: ModelForm, CheckAccount
class CheckAccountAppendForm(forms.ModelForm):
    
    class Meta:
        model = CheckAccount
        fields = [ 'ID', 'Subbank', 'Users', 'Money', \
            'RegDate', 'OverDraft', 'Manager']
    
    Users = forms.ModelMultipleChoiceField(
        queryset = User.objects.all(),
        widget = forms.CheckboxSelectMultiple
    )

    # save this form
    def save(self, commit = True):
        check_account = super().save(commit = False)
        if commit:
            check_account.save()
        return check_account

