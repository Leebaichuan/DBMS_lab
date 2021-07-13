# apps/statistics/urls.py
# sub_urlpatterns for statistics
from django.urls import path, include

from .views import GetStatisticsOverview, \
    StatisticsByLoanView, StatisticsByAccountView, \
    StatisticsByYearView, StatisticsByMonthView, StatisticsBySeasonView

app_name = 'statistics'
urlpatterns = [
    path('', GetStatisticsOverview, name = 'overview'),
    path('business/by-loan', StatisticsByLoanView.as_view(), name = 'by_loan'),
    path('business/by-account', StatisticsByAccountView.as_view(), name = 'by_account'),
    path('business/by-year', StatisticsByYearView.as_view(), name = 'by_year'),
    path('business/by-month', StatisticsByMonthView.as_view(), name = 'by_month'),
    path('business/by-season', StatisticsBySeasonView.as_view(), name = 'by_season'),
]
