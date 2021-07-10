from django.urls import path
#
from . import views

#


urlpatterns = [
    path('login/', views.account_login),
    path('logout/', views.account_logout),
    path('register/', views.account_register),
    path('define/', views.define_user),
]
