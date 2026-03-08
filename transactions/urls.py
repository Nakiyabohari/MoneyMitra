from django.urls import path
from . import views

urlpatterns = [
    path('addincome/', views.addincome, name='addincome'),
    path('add__expense/', views.add__expense, name='add__expense'),
    path('expensereport/', views.expensereport, name='expensereport'),
    path('transactionhistory/', views.transaction_history, name='transaction_history'),
]