from django.urls import path
from . import views

urlpatterns = [
    path('income/', views.monthly_income, name='monthly_income'),
    path('savings/', views.monthly_savings, name='savings'),
    path('savings_goal/', views.savings_goal, name='savings_goal'),
    path("add_money/<int:goal_id>/<int:amount>/", views.add_money, name="add_money"),
    path("delete_goal/<int:goal_id>/", views.delete_goal, name="delete_goal"),
    
]