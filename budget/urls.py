from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.income, name='income'),
    path('savings/', views.monthly_savings, name='savings'),
    path('savings_goal/', views.savings_goal, name='savings_goal'),
    path("add_money/<int:goal_id>/<int:amount>/", views.add_money, name="add_money"),
    path("delete_goal/<int:goal_id>/", views.delete_goal, name="delete_goal"),
    path("remove_money/<int:goal_id>/<int:amount>/", views.remove_money, name="remove_money"),
    

    # Nakiya's page
    path('MonthlyBudget/', views.monthly_budget, name='monthly_budget'),
    path('BudgetAnalysis/', views.budget_analysis, name='budget_analysis'),
    path('monthly_summary/',views.monthly_summary,name='monthly_summary'),
    path("delete_budget/<int:id>/", views.delete_budget, name="delete_budget"),
    path("edit_budget/<int:id>/", views.edit_budget, name="edit_budget"),
]