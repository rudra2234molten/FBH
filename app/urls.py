from django.urls import path
from . import views

urlpatterns = [
    path('',views.Index,name='home'),
    path('create/',views.Create,name='create'),
    path('pin/',views.Pin,name='pin'),
    path('otp_validation',views.Otp,name='pin_valid'),
    path('balance/',views.Balance,name='balance'),
    path('withdraw/',views.Withdraw,name='withdraw'),
    path('deposite/',views.Deposite,name='deposite'),
    path('transfer/',views.Transfer,name='transfer')
]
