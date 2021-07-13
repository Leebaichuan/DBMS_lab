# apps/loan/views.py
# this file stores some classes and functions for loan

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.utils import timezone

from .forms import LoanAppendForm, MoneyForm
from .models import Loan, Payment
from apps.subbank.models import Subbank
from apps.user.models import User

# for appending user
# requires: CreateView, User, reverse
class LoanAppendView(CreateView):

    template_name = 'loan/append.html'
    model = Loan
    fields = [ 'ID', 'Subbank', 'Money', \
            'User', 'CreatedDate', 'Manager']
    
    # after success, redirect to home first
    def get_success_url(self):
        return reverse('home')

    # save the data when the submitted form is valid
    def form_valid(self, form):
        loan = form.save(commit = False)
        subbank = loan.Subbank
        asset = Subbank.objects.get(Name = subbank).Asset
        # check if the loan is too much
        if loan.Money > asset:
            return HttpResponse("Too much loan here")
        # no problem, append it
        else:
            subbank.Asset = subbank.Asset - loan.Money
            subbank.save()
            loan.save()
            return super().form_valid(form)

    # show the error when the submitted form is invalid
    def form_invalid(self, form):
        cleaned_form = form.cleaned_data
        # check if the loan ID already exists
        if 'ID' not in cleaned_form:
            return HttpResponse("Loan ID already exists in the form")
        # check if the loan is too much
        elif loan_money > asset:
            return HttpResponse("Too much loan here")
        else:
            return HttpResponse("form is invalid for other errors")


# for showing all loans
# requires: ListView, Loan
class LoanOverviewView(ListView):
    template_name = 'loan/overview.html'
    model = Loan
    context_object_name = 'loans'
    queryset = Loan.objects.select_related().all()
    

# for showing profile of a particular loan
# requires DetailView, User
class LoanProfileView(DetailView):
    template_name = 'loan/profile.html'
    model = Loan

    # get the particular loan record and its payment record
    # according to the received pk
    def get_context_data(self, **kwargs):
        context = super(LoanProfileView, self).get_context_data(**kwargs)
        loan_id = self.object.pk
        loan = Loan.objects.get(ID = loan_id)
        context['loan'] = Loan.objects.select_related().get(ID = loan_id)
        context['payments'] = Payment.objects.filter(Loan = loan)
        return context

# for paying back the money for a loan
# @request: the HTTP request
# @loan_ID: the primary key of a loan
# note that the pay_money should <= remain money in loan
def LoanPay(request, loan_ID):
    # get the selected loan from its loan_ID and its remaining money
    loan = get_object_or_404(Loan, pk = loan_ID)
    remain_money = loan.Money
    # for http post request, send the data to back end
    if request.method == 'POST':
        # get the transmitted form
        form = MoneyForm(request.POST)
        print(form)
        if form.is_valid:
            # get the pay_money from front end
            form_set = form.cleaned_data
            pay_money = form_set['PayMoney']
            # pay_money < 0, invalid input
            if pay_money < 0:
                return render(request, 'loan/profile.html', {
                    'loan': loan,
                    'error_message': "pay money cannot be negative",
                })
            # pay too much money, also invalid
            elif(pay_money > remain_money):
                return render(request, 'loan/profile.html', {
                    'loan': loan,
                    'error_message': "pay money cannot be more than remain_money",
                })
            # successfully pay back the loan, go back to loan page
            else:
                # insert a new payment record
                payment = Payment(Loan = loan, \
                        PayDate = timezone.now(), PayMoney = pay_money)
                payment.save()
                # also save the revised loan record
                loan.Money = loan.Money - pay_money
                loan.save()
                return HttpResponseRedirect(reverse('loan:profile', args = (loan_ID,)))
    else:
        form = MoneyForm()
        return HttpResponseRedirect(reverse('loan:profile', args = (loan_ID,)))

# for deleting a loan
# @request: the HTTP request
# @loan_ID: the primary key of a loan
def LoanDelete(request, loan_ID):
    # get the selected loan from its loan_ID and its remaining money
    loan = get_object_or_404(Loan, pk = loan_ID)
    remain_money = loan.Money
    # for http post request, check whether delete the loan
    if request.method == 'POST':
        # there is still some debt in the loan, we cannot delete it
        if remain_money > 0:
            return render(request, 'loan/profile.html', {
                'loan': loan,
                'error_message': \
                    "fail to delete due to the existence of remaining money",
            })
        # no debt in the loan, so we can delete it and redirect to homepage
        else:
            Loan.objects.filter(pk = loan_ID).delete()
            return HttpResponseRedirect(reverse('loan:overview'))
    else:
        return HttpResponseRedirect(reverse('loan:overview'))
