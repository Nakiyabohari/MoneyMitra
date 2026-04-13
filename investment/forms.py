from django import forms
from .models import InvestmentPlan


class InvestmentForm(forms.ModelForm):
    class Meta:
        model = InvestmentPlan
        fields = ['investment_type', 'monthly_amount']