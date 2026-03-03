from django.db import models

# Create your models here.
class Income_model(models.Model):
    amount = models.IntegerField()
    income_source = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)

class Expense_model(models.Model):
    expense_amount = models.IntegerField()
    category = models.CharField(max_length=100)
    date = models.DateField()   # ✅ FIXED
    expense_payment_method = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)

class Expensereport_model(models.Model):
    month = models.IntegerField()
    year = models.IntegerField()
    salary = models.IntegerField()