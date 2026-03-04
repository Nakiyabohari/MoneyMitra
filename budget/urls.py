from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.monthly_income, name='monthly_income'),
    path('savings/', views.monthly_savings, name='savings'),

    # Nakiya's page
    path('MonthlyBudget/', views.monthly_budget, name='monthly_budget'),
]