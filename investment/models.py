from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class InvestmentPlan(models.Model):

    INVESTMENT_CHOICES = [
        ('Mutual Funds', 'Mutual Funds'),
        ('ETFs', 'ETFs'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='investment_plans'
    )

    investment_type = models.CharField(
        max_length=50,
        choices=INVESTMENT_CHOICES
    )

    monthly_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00'))]
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'investment_type']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.investment_type}"