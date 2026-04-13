from django.contrib import admin
from .models import MonthlyIncome, MonthlySavings, SavingsGoal, Category, Expense


# 1️⃣ Monthly Income
@admin.register(MonthlyIncome)
class MonthlyIncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'salary')
    list_filter = ('month',)
    search_fields = ('user__username',)


# 2️⃣ Monthly Savings
@admin.register(MonthlySavings)
class MonthlySavingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'amount')
    list_filter = ('month',)
    search_fields = ('user__username',)


# 3️⃣ Savings Goals
@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'target_amount', 'current_amount', 'deadline')
    list_filter = ('deadline',)
    search_fields = ('title', 'user__username')


# 4️⃣ Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'type', 'budget_amount', 'month')
    list_filter = ('type', 'month')
    search_fields = ('name', 'user__username')


# 5️⃣ Expense
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('category', 'user', 'amount', 'date', 'payment_type')
    list_filter = ('payment_type', 'date')
    search_fields = ('category__name', 'user__username')