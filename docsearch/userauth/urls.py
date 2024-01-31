from django.urls import path
from .views import signup , signin , getallusers , logout

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('getallusers/', getallusers, name='getallusers'),
    path('logout/', logout, name='logout'),
]