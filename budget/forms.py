from django import forms
from .models import MonthlyIncome, MonthlySavings, SavingsGoal, Category, Expense


# 1️⃣ Monthly Income Form (your friend's code - unchanged)
class MonthlyIncomeForm(forms.ModelForm):
    class Meta:
        model = MonthlyIncome
        fields = ['salary']
        widgets = {
            'salary': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Enter your monthly income'
            })
        }


# 2️⃣ Monthly Savings Form (your friend's code - unchanged)
class MonthlySavingsForm(forms.ModelForm):
    class Meta:
        model = MonthlySavings
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Enter your savings amount'
            })
        }


# 3️⃣ Savings Goal Form
class SavingsGoalForm(forms.ModelForm):
    class Meta:
        model = SavingsGoal
        fields = ['title', 'target_amount', 'current_amount', 'deadline', 'color']

        widgets = {

            'title': forms.TextInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Goal name'
            }),

            'target_amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Target amount'
            }),

            'current_amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Current saved amount'
            }),

            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'salary-input'
            }),

            # ⭐ important
            'color': forms.HiddenInput()
        }

# 4️⃣ Category Form (with monthly budget)
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'budget_amount', 'month']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Category name'
            }),
            'type': forms.Select(attrs={
                'class': 'salary-input'
            }),
            'budget_amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Budget amount'
            }),
            'month': forms.DateInput(attrs={
                'type': 'date',
                'class': 'salary-input'
            })
        }


# 5️⃣ Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'payment_type', 'notes']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'salary-input'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Expense amount'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'salary-input'
            }),
            'payment_type': forms.Select(attrs={
                'class': 'salary-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'salary-input',
                'rows': 3,
                'placeholder': 'Optional notes'
            })
        }