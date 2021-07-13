# apps/user/views.py
# this file stores some classes and functions for user
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse

from .forms import UserAppendForm
from .models import User
from apps.loan.models import Loan
from apps.account.models import DepositAccount, CheckAccount

# for appending user
# requires: CreateView, User, reverse
class UserAppendView(CreateView):

    template_name = 'user/append.html'
    model = User
    fields = ['ID', 'Name', 'PhoneNum', 'Address', \
        'Contact_Name', 'Contact_PhoneNum', 'Contact_Email']
    
    # after success, redirect to overview
    def get_success_url(self):
        return reverse('user:overview')

    # save the data when the submitted form is valid
    def form_valid(self, form):
        user = form.save(commit = False)
        user.save()
        return super().form_valid(form)

    # show the error when the submitted form is invalid
    def form_invalid(self, form):
        cleaned_form = form.cleaned_data
        # check if the user ID already exists
        if 'ID' not in cleaned_form:
            return HttpResponse("Loan ID already exists in the form")
        else:
            return HttpResponse("form is invalid for other errors")

# for showing all users
# requires: ListView, User
class UserOverviewView(ListView):
    template_name = 'user/overview.html'
    model = User
    context_object_name = 'users'
    queryset = User.objects.all()
    
# for showing profile of a particular user
# requires DetailView, User
class UserProfileView(DetailView):
    template_name = 'user/profile.html'
    model = User

    # get the particular user record
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        user_id = self.object.pk
        context['user'] = User.objects.get(ID = user_id)
        return context

# for updating a user profile
# requires UpdateView, User, reverse
class UserProfileUpdateView(UpdateView):
    template_name = 'user/update.html'
    model = User
    fields = [ 'Name', 'PhoneNum', 'Address', 'Contact_Name',\
             'Contact_PhoneNum', 'Contact_Email']

    # get the particular user record
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        user_id = self.object.pk
        context['user'] = User.objects.get(ID = user_id)
        return context

    # the url after successful operation
    def get_success_url(self):
        return reverse('user:overview')
    
    # save the data
    def form_valid(self, form):
        user = form.save(commit = False)
        user.save()
        return super().form_valid(form)

# for deleting a user
# we need to check whether the user has a account or loan,
# if so, we can't delete it
# @request: the HTTP request
# @user_ID: the primary key of a user
def UserDelete(request, user_ID):
    # get the selected loan from its loan_ID and its remaining money
    user = User.objects.get(ID = user_ID)

    # for http post request, check whether delete to delete the user
    if request.method == 'POST':
        loans = Loan.objects.filter(User = user)
        deposit_accounts = DepositAccount.objects.all()
        check_accounts = CheckAccount.objects.all()
        # 1. check whether the user owns a loan
        if loans:
            return HttpResponse("the user %s %s has owned a loan" %(user.ID, user.Name) )
        # 2. check whether the user has a deposit account
        for deposit_account in deposit_accounts:
            deposit_account_users = deposit_account.Users.all()
            if user in deposit_account_users:
              return HttpResponse("the user %s %s has owned a deposit account" %(user.ID, user.Name) )
        
        # 3. check whether the user has a check account
        for check_account in check_accounts:
            check_account_users = check_account.Users.all()
            if user in check_account_users:
               return HttpResponse("the user %s %s has owned a check account" %(user.ID, user.Name) )

        # 4. no problem, just delete the user
        User.objects.filter(ID = user_ID).delete()
        return HttpResponseRedirect(reverse('user:overview'))
    else:
        return HttpResponseRedirect(reverse('user:overview'))