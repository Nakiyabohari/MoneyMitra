from django import forms
from .models import EmiManager

class EmiManagerForm(forms.ModelForm):
    class Meta:
        model = EmiManager
        fields = '__all__'

        widgets = {
            'emi_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter EMI Name'
            }),

            'monthly_amount': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Monthly Amount'
            }),

            'duration': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Duration (months)'
            }),

            'start_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
        }