# apps/account/urls.py
# sub_urlpatterns for account
from django.urls import path, include

from .views import AccountOverviewView, \
    DepositAccountAppendView, CheckAccountAppendView, \
    DepositAccountProfileView, CheckAccountProfileView, \
    DepositAccountUpdateView, CheckAccountUpdateView, \
    DepositAccountDelete, CheckAccountDelete

app_name = 'account'
urlpatterns = [
    path('', AccountOverviewView.as_view(), name = 'overview'),
    path('deposit-append/', DepositAccountAppendView.as_view(), name = 'deposit_append'),
    path('check-append/', CheckAccountAppendView.as_view(), name = 'check_append'),
    path('deposit-profile/<slug:pk>', DepositAccountProfileView.as_view(), name = 'deposit_profile'),
    path('check-profile/<slug:pk>', CheckAccountProfileView.as_view(), name = 'check_profile'),
    path('deposit-update/<slug:pk>', DepositAccountUpdateView.as_view(), name = 'deposit_update'),
    path('check-update/<slug:pk>', CheckAccountUpdateView.as_view(), name = 'check_update'),
    path('deposit-delete/<slug:deposit_account_ID>',DepositAccountDelete, name = 'deposit_delete'),
    path('check-delete/<slug:check_account_ID>',CheckAccountDelete, name = 'check_delete'),
    #path('delete/<slug:loan_ID>',LoanDelete, name = 'delete'),
]
