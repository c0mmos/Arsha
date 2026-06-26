from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_date = models.DateTimeField(auto_now_add=True)