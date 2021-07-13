# apps/user/urls.py
# sub_urlpatterns for user 
from django.urls import path, include

from .views import UserAppendView, UserOverviewView, \
        UserProfileView, UserProfileUpdateView, UserDelete

app_name = 'user'
urlpatterns = [
    path('', UserOverviewView.as_view(), name = 'overview'),
    path('append/', UserAppendView.as_view(), name = 'append'),
    path('profile/<slug:pk>', UserProfileView.as_view(), name = 'profile'),
    path('update/<slug:pk>',UserProfileUpdateView.as_view(), name = 'update'),
    path('delete/<slug:user_ID>',UserDelete, name = 'delete')
]