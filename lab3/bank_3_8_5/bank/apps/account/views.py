# apps/account/views.py
# this file stores some classes and functions for account

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.utils import timezone

from .forms import DepositAccountAppendForm, CheckAccountAppendForm

from apps.subbank.models import Subbank
from apps.user.models import User
from apps.account.models import DepositAccount, CheckAccount

# for appending deposit account
# requires: CreateView, User, reverse
class DepositAccountAppendView(CreateView):

    template_name = 'account/deposit/deposit_append.html'
    model = DepositAccount
    form_class = DepositAccountAppendForm
    
    # after success, redirect to home first
    def get_success_url(self):
        return reverse('account:overview')

    # save the data when the submitted form is valid
    def form_valid(self, form):
        # get the users, subbank and money
        deposit_account = form.save(commit = False)
        users = form.cleaned_data['Users']
        subbank = deposit_account.Subbank
        money = deposit_account.Money
        interetst_rate = deposit_account.InterestRate
        # 1. check if a user already has a deposit account in the same subbank
        for user in users:
            deposit_account_set = DepositAccount.objects.all()
            for each_deposit_account in deposit_account_set:
                if each_deposit_account.Subbank == subbank:
                    each_deposit_account_users = each_deposit_account.Users.all()
                    if user in each_deposit_account_users:
                        return HttpResponse("the user %s %s has owned a deposit account in %s subbank" %(user.ID, user.Name, subbank.Name) )
        # 2. check if the money is negative
        if money < 0:
            return HttpResponse("the money in a deposit account should not be negative")
        # 3. check if the interest rate is negative
        elif interetst_rate < 0:
            return HttpResponse("the interest rate should not be negative")
        # no problem, save the deposit account
        # and the change the asset of the subbank
        else:
            subbank.Asset = subbank.Asset + deposit_account.Money
            subbank.save()
            deposit_account.save()
            for user in users:
                deposit_account.Users.add(user)
            deposit_account.save()
            return super().form_valid(form)

    # show the error when the submitted form is invalid
    def form_invalid(self, form):
        cleaned_form = form.cleaned_data
        # check if the loan ID already exists
        if 'ID' not in cleaned_form:
            return HttpResponse("Account ID already exists in the form")


# for appending check account
# requires: CreateView, User, reverse
class CheckAccountAppendView(CreateView):

    template_name = 'account/check/check_append.html'
    model = CheckAccount
    form_class = CheckAccountAppendForm
    
    # after success, redirect to home first
    def get_success_url(self):
        return reverse('account:overview')

    
    # save the data when the submitted form is valid
    def form_valid(self, form):
        # get the users, subbank and money
        check_account = form.save(commit = False)
        users = form.cleaned_data['Users']
        subbank = check_account.Subbank
        money = check_account.Money
        overdraft = check_account.OverDraft
        # 1. check if a user has a deposit account in the same subbank
        for user in users:
            check_account_set = CheckAccount.objects.all()
            for each_check_account in check_account_set:
                if each_check_account.Subbank == subbank:
                    each_check_account_users = each_check_account.Users.all()
                    if user in each_check_account_users:
                        return HttpResponse("the user %s %s has owned a check account in %s subbank" %(user.ID, user.Name, subbank.Name) )
        # 2. check if the money is negative
        if money < 0:
            return HttpResponse("the money in a check account should not be negative")
        # 3. check if the overdraft is negative
        if overdraft < 0:
            return HttpResponse("the overdraft in a check account should not be negative")
        # 3. check if the overdraft is less than money
        if overdraft < money:
            return HttpResponse("the overdraft in a check account should not be less than the remaining money")
        # no problem, save the deposit account
        # and the change the asset of the subbank
        else:
            subbank.Asset = subbank.Asset + check_account.Money
            subbank.save()
            check_account.save()
            for user in users:
                check_account.Users.add(user)
            check_account.save()
            return super().form_valid(form)

    # show the error when the submitted form is invalid
    def form_invalid(self, form):
        cleaned_form = form.cleaned_data
        # check if the loan ID already exists
        if 'ID' not in cleaned_form:
            return HttpResponse("Account ID already exists in the form")


# for showing all accounts
# requires: ListView, DepositAccount, CheckAccount
class AccountOverviewView(ListView):
    template_name = 'account/overview.html'
    model = DepositAccount
    
    # get all of the deposit account and check account
    def get_context_data(self, **kwargs):
        context = super(AccountOverviewView, self).\
            get_context_data(**kwargs)
        context['deposit_accounts'] = DepositAccount.objects.\
            select_related().all()
        context['check_accounts'] = CheckAccount.objects.\
            select_related().all()
        return context


# for showing profile of a particular deposit account
# requires DetailView, Deposit Account
class DepositAccountProfileView(DetailView):
    template_name = 'account/deposit/deposit_profile.html'
    model = DepositAccount

    # get the particular deposit account
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(DepositAccountProfileView, self).\
            get_context_data(**kwargs)
        deposit_account_id = self.object.pk
        context['deposit_account'] = DepositAccount.\
            objects.select_related().get(ID = deposit_account_id)
        return context

# for showing profile of a particular check account
# requires DetailView, Check Account
class CheckAccountProfileView(DetailView):
    template_name = 'account/check/check_profile.html'
    model = CheckAccount

    # get the particular deposit account
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(CheckAccountProfileView, self).\
            get_context_data(**kwargs)
        check_account_id = self.object.pk
        context['check_account'] = CheckAccount.objects.\
            select_related().get(ID = check_account_id)
        return context

# for updating a deposit account
# requires UpdateView, DepositAccount, reverse
class DepositAccountUpdateView(UpdateView):
    template_name = 'account/deposit/deposit_update.html'
    model = DepositAccount
    form_class = DepositAccountAppendForm

    # get the particular deposit account
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(DepositAccountUpdateView, self).\
            get_context_data(**kwargs)
        deposit_account_id = self.object.pk
        context['deposit_account'] = DepositAccount.\
            objects.get(ID = deposit_account_id)
        return context

    # the url after successful operation
    def get_success_url(self):
        return reverse('account:overview')
    
    # save the data when the submitted form is valid
    def form_valid(self, form):
        # get the users, subbank and money
        deposit_account = form.save(commit = False)
        users = form.cleaned_data['Users']
        subbank = deposit_account.Subbank
        money = deposit_account.Money
        interetst_rate = deposit_account.InterestRate
        # 1. check if a user already has a deposit account in the same subbank
        for user in users:
            deposit_account_set = DepositAccount.objects.all()
            for each_deposit_account in deposit_account_set:
                if each_deposit_account.Subbank == subbank \
                    and each_deposit_account != deposit_account :
                    each_deposit_account_users = each_deposit_account.Users.all()
                    if user in each_deposit_account_users:
                        return HttpResponse("the user %s %s has owned a deposit account in %s subbank" %(user.ID, user.Name, subbank.Name) )
        # 2. check if the money is negative
        if money < 0:
            return HttpResponse("the money in a deposit account should not be negative")
        # 3. check if the interest rate is negative
        elif interetst_rate < 0:
            return HttpResponse("the interest rate should not be negative")
        # no problem, save the deposit account
        # and the change the asset of the subbank
        else:
            subbank.Asset = subbank.Asset + deposit_account.Money
            subbank.save()
            deposit_account.save()
            for user in users:
                deposit_account.Users.add(user)
            deposit_account.save()
            return super().form_valid(form)
    
    

# for updating a check account
# requires UpdateView, CheckAccount, reverse
class CheckAccountUpdateView(UpdateView):
    template_name = 'account/check/check_update.html'
    model = CheckAccount
    form_class = CheckAccountAppendForm

    # get the particular check account
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(CheckAccountUpdateView, self).\
            get_context_data(**kwargs)
        deposit_account_id = self.object.pk
        context['deposit_account'] = CheckAccount.objects.\
            get(ID = deposit_account_id)
        return context

    # the url after successful operation
    def get_success_url(self):
        return reverse('account:overview')
    
      # save the data when the submitted form is valid
    def form_valid(self, form):
        # get the users, subbank and money
        check_account = form.save(commit = False)
        users = form.cleaned_data['Users']
        subbank = check_account.Subbank
        money = check_account.Money
        overdraft = check_account.OverDraft
        # 1. check if a user has a deposit account in the same subbank
        for user in users:
            check_account_set = CheckAccount.objects.all()
            for each_check_account in check_account_set:
                if each_check_account.Subbank == subbank \
                    and each_check_account != check_account :
                    each_check_account_users = each_check_account.Users.all()
                    if user in each_check_account_users:
                        return HttpResponse("the user %s %s has owned a check account in %s subbank" %(user.ID, user.Name, subbank.Name) )
        # 2. check if the money is negative
        if money < 0:
            return HttpResponse("the money in a check account should not be negative")
        # 3. check if the overdraft is negative
        if overdraft < 0:
            return HttpResponse("the overdraft in a check account should not be negative")
        # 3. check if the overdraft is less than money
        if overdraft < money:
            return HttpResponse("the overdraft in a check account should not be less than the remaining money")
        # no problem, save the deposit account
        # and the change the asset of the subbank
        else:
            subbank.Asset = subbank.Asset + check_account.Money
            subbank.save()
            check_account.save()
            for user in users:
                check_account.Users.add(user)
            check_account.save()
            return super().form_valid(form)


# for deleting a deposit account
# @request: the HTTP request
# @deposit_account_ID: the primary key of a deposit account
def DepositAccountDelete(request, deposit_account_ID):
    # get the selected deposit account from its ID
    deposit_account = get_object_or_404(DepositAccount, pk = deposit_account_ID)
    # for http post request, check whether to delete the deposit account
    if request.method == 'POST':
        # delete this account, and withdraw the money to the users
        money = deposit_account.Money
        subbank = deposit_account.Subbank
        subbank.Asset = subbank.Asset - money
        subbank.save()
        DepositAccount.objects.filter(pk = deposit_account_ID).delete()
        return HttpResponseRedirect(reverse('account:overview'))
    else:
        return HttpResponseRedirect(reverse('account:overview'))


# for deleting a check account
# @request: the HTTP request
# @check_account_ID: the primary key of a check account
def CheckAccountDelete(request, check_account_ID):
    # get the selected check account from its ID
    check_account = get_object_or_404(CheckAccount, pk = check_account_ID)
    # for http post request, check whether to delete the deposit account
    if request.method == 'POST':
        # delete this account, and withdraw the money to the users
        money = check_account.Money
        subbank = check_account.Subbank
        subbank.Asset = subbank.Asset - money
        subbank.save()
        CheckAccount.objects.filter(pk = check_account_ID).delete()
        return HttpResponseRedirect(reverse('account:overview'))
    else:
        return HttpResponseRedirect(reverse('account:overview'))