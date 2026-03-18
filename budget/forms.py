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
        'class': 'form-input',
        'placeholder': 'Goal Name',
        'pattern': '[A-Za-z ]+',
        'title': 'Only letters allowed',
        'oninput': "this.value = this.value.replace(/[^A-Za-z ]/g, '')"
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
CATEGORY_CHOICES = [
    ("Food & Dining", "Food & Dining"),
    ("Transportation", "Transportation"),
    ("Utilities", "Utilities"),
    ("Entertainment", "Entertainment"),
    ("Shopping", "Shopping"),
    ("Health", "Health"),
    ("Education", "Education"),
    ("Others", "Others"),
    ("Custom", "Custom"),
]


class CategoryForm(forms.ModelForm):

    # ✅ ADD HERE (NOT inside Meta)
    month = forms.CharField(
        widget=forms.TextInput(attrs={
            'type': 'month',
            'class': 'salary-input'
        })
    )

    name = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={
            'class': 'salary-input',
            'id': 'categorySelect'
        })
    )

    custom_name = forms.CharField(
    required=False,
    widget=forms.TextInput(attrs={   # ✅ CORRECT
        'class': 'salary-input',
        'placeholder': 'Enter Category Name',
        'pattern': '[A-Za-z ]+',
        'title': 'Only letters allowed',
        'oninput': "this.value = this.value.replace(/[^A-Za-z ]/g, '')",
        'id': 'customCategory'
    })
    )

    class Meta:
        model = Category
        fields = ['name', 'budget_amount', 'month']

        widgets = {
            'budget_amount': forms.NumberInput(attrs={
                'class': 'salary-input',
                'placeholder': 'Budget amount'
            }),
        }

    # ✅ ADD THIS ALSO
    def clean_month(self):
        from datetime import datetime
        month = self.cleaned_data.get('month')
        return datetime.strptime(month, "%Y-%m").date().replace(day=1)


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