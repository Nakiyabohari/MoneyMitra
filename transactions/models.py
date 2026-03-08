from django.db import models
from django.contrib.auth.models import User
from budget.models import Category


# # Category model must come first
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     TYPE_CHOICES = [
#         ('income', 'Income'),
#         ('expense', 'Expense'),
#     ]
#     type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='expense')

#     def __str__(self):
#         return self.name


class Income_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.IntegerField()
    income_source = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)



class Expense_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    expense_amount = models.IntegerField()

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE    
    )

    date = models.DateField()

    expense_payment_method = models.CharField(max_length=100)

    notes = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.category} - ₹{self.expense_amount}"


class Expensereport_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()
    salary = models.IntegerField()


class Transaction_history_model(models.Model):
    TRANSACTION_TYPE = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]

    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"