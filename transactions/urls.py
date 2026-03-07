from django.urls import path
from . import views

urlpatterns = [
    path('addincome/', views.addincome, name='addincome'),
    path('add__expense/', views.add__expense, name='add__expense'),
    path('expensereport/', views.expensereport, name='expensereport'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),   
]