from django.db import models
from django.contrib.auth.models import User

class EmiManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    emi_name = models.CharField(max_length=200)
    monthly_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text="Duration in months")
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.emi_name}"