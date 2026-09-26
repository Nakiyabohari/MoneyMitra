from django.urls import path
from . import views

urlpatterns = [
    path('', views.investment_view, name='investment'),
    path('mitra-ai/', views.mitra_ai, name='mitra_ai'),  # ← THIS MUST EXIST
    path("investment/details/", views.investment_details, name="investment_details")\
    
]