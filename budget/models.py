from django.db import models
from django.contrib.auth.models import User


# 1️⃣ Monthly Income
class MonthlyIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.salary}"


# 2️⃣ Monthly Savings
class MonthlySavings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"


# 3️⃣ Savings Goals
class SavingsGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField()

    def progress(self):
        if self.target_amount > 0:
            return (self.current_amount / self.target_amount) * 100
        return 0

    def __str__(self):
        return self.title


# 4️⃣ Category (Now Includes Budget + Month)
class Category(models.Model):
    CATEGORY_TYPE = (
        ('expense', 'Expense'),
        ('investment', 'Investment'),
        ('savings', 'Savings'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=CATEGORY_TYPE, default='expense')

    # Added fields as you said
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    month = models.DateField(help_text="Select first day of month")

    def __str__(self):
        return self.name


# 5️⃣ Expense (Updated as You Said)
class Expense(models.Model):

    PAYMENT_CHOICES = (
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Card'),
        ('bank', 'Bank Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.category.name} - {self.amount}"
