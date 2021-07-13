# bank/urls.py
# root urlpatterns for this application 
from django.contrib import admin
from django.urls import include, path
from apps.core.views import GetHome

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', GetHome, name = 'home'),
    path('user/', include('apps.user.urls')),
    path('loan/', include('apps.loan.urls')),
    path('account/', include('apps.account.urls')),
    path('statistics/', include('apps.statistics.urls')),
]

