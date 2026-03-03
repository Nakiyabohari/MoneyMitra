from django import forms
from .models import MonthlyIncome, MonthlySavings


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