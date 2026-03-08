from django.urls import path
from . import views

urlpatterns = [
    path('addincome/', views.addincome, name='addincome'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('expensereport/', views.expensereport, name='expensereport'),
    path('transactionhistory/', views.transaction_history, name='transaction_history'),
]