from django import forms
from .models import Income_model
from .models import Expense_model
# from .models import Transaction_model
class addincome_Form(forms.ModelForm):
    class Meta:
        model = Income_model
        fields = ['amount', 'income_source', 'payment_method', 'notes']

class add_expense_Form(forms.ModelForm):
    class Meta:
        model = Expense_model
        fields = ['expense_amount', 'category', 'date', 'expense_payment_method','notes']


