# authentication/urls.py

from django.urls import path
from .views import register_user, obtain_auth_token, get_all_users, logout

urlpatterns = [
    path('register/', register_user, name='register_user'),
    path('login/', obtain_auth_token, name='obtain_auth_token'),
    path('get_all_users/', get_all_users, name='get_all_users'),
    path('logout/', logout, name='logout'),
]
