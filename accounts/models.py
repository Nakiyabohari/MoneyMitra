from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=150)
    occupation = models.CharField(max_length=100)

    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    profile_photo = models.ImageField(upload_to='profile/', blank=True, null=True)

    # 🔥 Financial Fields
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    savings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    investments = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    emi = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.user.email