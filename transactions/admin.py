from django.contrib import admin
from .models import Income_model
from .models import Expense_model
from .models import Expensereport_model
from .models import Transaction_history_model
# Register your models here.
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('amount', 'income_source', 'payment_method' ,'notes')
admin.site.register(Income_model,IncomeAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('expense_amount', 'category', 'date' ,'expense_payment_method','notes')
admin.site.register(Expense_model,ExpenseAdmin)

class ExpensereportAdmin(admin.ModelAdmin):
    list_display = ('month', 'year', 'salary')
admin.site.register(Expensereport_model,ExpensereportAdmin)

class TransactionhistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'category', 'amount', 'date')
admin.site.register(Transaction_history_model,TransactionhistoryAdmin)



