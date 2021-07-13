# apps/loans/urls.py
# sub_urlpatterns for loan
from django.urls import path, include

from .views import LoanAppendView, LoanOverviewView, \
        LoanProfileView, LoanPay, LoanDelete

app_name = 'loan'
urlpatterns = [
    path('', LoanOverviewView.as_view(), name = 'overview'),
    path('append/', LoanAppendView.as_view(), name = 'append'),
    path('profile/<slug:pk>',LoanProfileView.as_view(), name = 'profile'),
    path('pay/<slug:loan_ID>',LoanPay, name = 'pay'),
    path('delete/<slug:loan_ID>',LoanDelete, name = 'delete'),
]
