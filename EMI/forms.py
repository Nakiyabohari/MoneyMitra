from django import forms
from .models import EmiManager

class EmiManagerForm(forms.ModelForm):
    class Meta:
        model = EmiManager

        # REMOVE user from form
        fields = [
            'emi_name',
            'monthly_amount',
            'duration',
            'start_date',
            'end_date'
        ]

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
                'type': 'text',
                'placeholder': 'Start Date (dd-mm-yyyy)',
                'onfocus': "(this.type='date')",
                'onblur': "if(!this.value)this.type='text'"
            }),

            'end_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'text',
                'placeholder': 'End Date (dd-mm-yyyy)',
                'onfocus': "(this.type='date')",
                'onblur': "if(!this.value)this.type='text'"
            }),
        }