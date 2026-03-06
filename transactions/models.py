from django.db import models
from django.contrib.auth.models import User


class Income_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    amount = models.IntegerField()
    income_source = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)


class Expense_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    expense_amount = models.IntegerField()
    category = models.CharField(max_length=100)
    date = models.DateField()
    expense_payment_method = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)


class Expensereport_model(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    month = models.IntegerField()
    year = models.IntegerField()
    salary = models.IntegerField()