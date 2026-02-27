from django.contrib import admin
from .models import InvestmentPlan


@admin.register(InvestmentPlan)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'investment_type', 'monthly_amount', 'created_at')
    list_filter = ('investment_type',)
    search_fields = ('user__username',)