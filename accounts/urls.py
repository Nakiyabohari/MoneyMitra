from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
     # Income
    path('income/', views.income, name='income'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.user_logout, name='logout'),
    path('menu/', views.menu, name='menu'),

    # NEW
    path('calculator/', views.calculator, name='calculator'),
    path('calendar/', views.calendar_view, name='calendar'),

   

    # Add Income
    path('addincome/', views.add_income, name='add_income'),

    #emi manager
    path('emimanager/', views.emimanager, name='emimanager'),

    #Monthly Budget
    path('MonthlyBudget/', views.MonthlyBudget, name='MonthlyBudget'),

    #Budget Analysis
    path('BudgetAnalysis/', views.BudgetAnalysis, name='BudgetAnalysis'),

    #Savings Goals
    path('savings_goal/', views.savings_goal, name='savings_goal'),

    #Expense Report
    path('expensereport/', views.expense_report, name='expensereport'),

    #Add Expense
    path('add_expense/', views.add_expense, name='add_expense'),
]