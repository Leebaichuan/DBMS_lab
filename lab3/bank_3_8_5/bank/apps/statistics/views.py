# apps/statistics/views.py
# this file stores some classes and functions for statistic

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse
from django.utils import timezone

from apps.subbank.models import Subbank
from apps.loan.models import Loan
from apps.account.models import DepositAccount, CheckAccount

# get statistic overview page overall
def GetStatisticsOverview(request):
    return render(request, 'statistics/overview.html')


# for showing the statistics of subbanks by loan
# requires: ListView, Subbank, Loan
class StatisticsByLoanView(ListView):
    template_name = 'statistics/business/by_loan.html'
    model = Subbank
    
    # get the amount and total money of loans of each subbank
    def get_context_data(self, **kwargs):
        context = super(StatisticsByLoanView, self).get_context_data(**kwargs)
        # get the wholeset of subbanks and loans
        subbanks = Subbank.objects.all()
        loans = Loan.objects.all()
        # they store the total amount and money of loans 
        # and the corresponding total amount of users of each subbank  
        total_amount = []
        total_money = []
        total_user_num = []
        # get the total loan amount and loan money for each subbank
        for subbank in subbanks:
            amount = 0
            money = 0
            users = set({})
            for loan in loans:
                if loan.Subbank == subbank:
                    amount += 1
                    money += loan.Money
                    users.add(loan.User)

            total_amount.append(amount)
            total_money.append(money)
            total_user_num.append( len(users) )
        # pack them together and send them back to the front end
        all_info = zip(subbanks, total_amount, total_money, total_user_num)
        context['all_info'] = all_info
        return context


# for showing the statistics of subbanks by deposit account
# requires: ListView, Subbank, DepositAccount
class StatisticsByAccountView(ListView):
    template_name = 'statistics/business/by_account.html'
    model = Subbank
    
    # get the amount and total money of accounts of each subbank
    def get_context_data(self, **kwargs):
        context = super(StatisticsByAccountView, self).get_context_data(**kwargs)
        # get the wholeset of subbanks and accounts
        subbanks = Subbank.objects.all()
        deposit_accounts = DepositAccount.objects.all()
        # they store the total amount and money of accounts 
        # and the number of their coresponding users of each subbank  
        total_amount = []
        total_money = []
        total_user_num = []
        # get the total account amount and account money 
        # and user number for each subbank
        for subbank in subbanks:
            amount = 0
            money = 0
            users = set({})
            # count the deposit accounts
            for deposit_account in deposit_accounts:
                if deposit_account.Subbank == subbank:
                    amount += 1
                    money += deposit_account.Money
                    users.add(deposit_account.Users.all())

            total_amount.append(amount)
            total_money.append(money)
            total_user_num.append( len(users) )
        # pack them together and send them back to the front end
        all_info = zip(subbanks, total_amount, total_money, total_user_num)
        context['all_info'] = all_info
        return context


# for showing the statistics of subbanks by year
# requires: ListView, Subbank, Loan, DepositAccount
class StatisticsByYearView(ListView):
    template_name = 'statistics/time/by_year.html'
    model = Subbank
    
    # the class of a triple of basic info of a subbank in a year
    class InfoTriple(object):
        amount = 0
        money = 0
        user_num = 0
        def __init__(self, amount, money, user_num):
            self.amount = amount
            self.money = money
            self.user_num = user_num
 
    # get the amount, total money and user number of business of each subbank
    def get_context_data(self, **kwargs):
        context = super(StatisticsByYearView, self).get_context_data(**kwargs)
        # get the wholeset of subbanks, loans and accounts
        subbanks = Subbank.objects.all()
        deposit_accounts = DepositAccount.objects.all()
        loans = Loan.objects.all()
        # count the years 2015 ~2021
        year_num = 7
        year_list = [1] * year_num
        for i in range(year_num):
            year_list[i] = i + 2015
        # they store the total amount and money of business
        # and the number of their coresponding users of each subbank  
        total_info = []
        # get the total business amount and money 
        # and user number for each subbank
        for subbank in subbanks:
            # for each subbank
            each_info = dict()
            each_users = dict()
            for i in year_list:
                each_info[i] = self.InfoTriple(0,0,0)
                each_users[i] = set({})


            # count the loan of each year
            for loan in loans:
                if loan.Subbank == subbank:
                    year = loan.CreatedDate.year
                    # count the business amount
                    each_info[year].amount += 1
                    # count the business money
                    each_info[year].money += loan.Money
                    # count the user number
                    each_users[year].add(loan.User)

            # count the deposit accounts of each year
            for deposit_account in deposit_accounts:
                if deposit_account.Subbank == subbank:
                    year = deposit_account.RegDate.year
                    # count the business amount
                    each_info[year].amount += 1
                    # count the business money
                    each_info[year].money += deposit_account.Money
                    # count the user number
                    each_users[year].add(deposit_account.Users.all())


            # save the result of one subbank
            for i in year_list:
                each_info[i].user_num = len(each_users[i])
            total_info.append(each_info)

        # pack them together and send them back to the front end
        all_info = zip(subbanks, total_info)
        context['all_info'] = all_info
        return context

# for showing the statistics of subbanks by month
# requires: ListView, Subbank, Loan, DepositAccount
class StatisticsByMonthView(ListView):
    template_name = 'statistics/time/by_month.html'
    model = Subbank
    
    # the class of a triple of basic info of a subbank in a month
    class InfoTriple(object):
        amount = 0
        money = 0
        user_num = 0
        def __init__(self, amount, money, user_num):
            self.amount = amount
            self.money = money
            self.user_num = user_num
 
    # get the amount, total money and user number of business of each subbank
    def get_context_data(self, **kwargs):
        context = super(StatisticsByMonthView, self).get_context_data(**kwargs)
        # get the wholeset of subbanks, loans and accounts
        subbanks = Subbank.objects.all()
        deposit_accounts = DepositAccount.objects.all()
        loans = Loan.objects.all()
        # count the months 1 ~ 12
        month_num = 12
        month_list = [1] * month_num
        for i in range(month_num):
            month_list[i] = i + 1
        # they store the total amount and money of business
        # and the number of their coresponding users of each subbank  
        total_info = []
        # get the total business amount and money 
        # and user number for each subbank
        for subbank in subbanks:
            # for each subbank
            each_info = dict()
            each_users = dict()
            for i in month_list:
                each_info[i] = self.InfoTriple(0,0,0)
                each_users[i] = set({})


            # count the loan of each year
            for loan in loans:
                if loan.Subbank == subbank:
                    month = loan.CreatedDate.month
                    # count the business amount
                    each_info[month].amount += 1
                    # count the business money
                    each_info[month].money += loan.Money
                    # count the user number
                    each_users[month].add(loan.User)

            # count the deposit accounts of each year
            for deposit_account in deposit_accounts:
                if deposit_account.Subbank == subbank:
                    month = deposit_account.RegDate.month
                    # count the business amount
                    each_info[month].amount += 1
                    # count the business money
                    each_info[month].money += deposit_account.Money
                    # count the user number
                    each_users[month].add(deposit_account.Users.all())


            # save the result of one subbank
            for i in month_list:
                each_info[i].user_num = len(each_users[i])
            total_info.append(each_info)

        # pack them together and send them back to the front end
        all_info = zip(subbanks, total_info)
        context['all_info'] = all_info
        return context


# for showing the statistics of subbanks by season
# requires: ListView, Subbank, Loan, DepositAccount
class StatisticsBySeasonView(ListView):
    template_name = 'statistics/time/by_season.html'
    model = Subbank
    
    # the class of a triple of basic info of a subbank in a season
    class InfoTriple(object):
        amount = 0
        money = 0
        user_num = 0
        def __init__(self, amount, money, user_num):
            self.amount = amount
            self.money = money
            self.user_num = user_num
    
    # get the amount, total money and user number of business of each subbank
    def get_context_data(self, **kwargs):
        context = super(StatisticsBySeasonView, self).get_context_data(**kwargs)
        # get the wholeset of subbanks, loans and accounts
        subbanks = Subbank.objects.all()
        deposit_accounts = DepositAccount.objects.all()
        loans = Loan.objects.all()
        # count the seasons 1 ~ 4
        season_num = 4
        season_list = [1] * season_num
        for i in range(season_num):
            season_list[i] = i + 1
        # they store the total amount and money of business
        # and the number of their coresponding users of each subbank  
        total_info = []
        # get the total business amount and money 
        # and user number for each subbank
        for subbank in subbanks:
            # for each subbank
            each_info = dict()
            each_users = dict()
            for i in season_list:
                each_info[i] = self.InfoTriple(0,0,0)
                each_users[i] = set({})


            # count the loan of each year
            for loan in loans:
                if loan.Subbank == subbank:
                    month = loan.CreatedDate.month
                    # get the season that the month is in
                    season = (month + 2) // 3
                    # count the business amount
                    each_info[season].amount += 1
                    # count the business money
                    each_info[season].money += loan.Money
                    # count the user number
                    each_users[season].add(loan.User)

            # count the deposit accounts of each year
            for deposit_account in deposit_accounts:
                if deposit_account.Subbank == subbank:
                    month = deposit_account.RegDate.month
                    # get the season that the month is in
                    season = (month + 2) // 3
                    # count the business amount
                    each_info[season].amount += 1
                    # count the business money
                    each_info[season].money += deposit_account.Money
                    # count the user number
                    each_users[season].add(deposit_account.Users.all())


            # save the result of one subbank
            for i in season_list:
                each_info[i].user_num = len(each_users[i])
            total_info.append(each_info)

        # pack them together and send them back to the front end
        all_info = zip(subbanks, total_info)
        context['all_info'] = all_info
        return context