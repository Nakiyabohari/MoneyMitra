from django.urls import path
from . import views

urlpatterns = [
    path('', views.emimanager, name='emimanager'),
    path('emi/addemi/', views.addemi, name='addemi'),
    path('emi/delete/<int:id>/', views.delete_emi, name='delete_emi'),  # ✅ NEW
]