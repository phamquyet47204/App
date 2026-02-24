from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    mssv = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["email", "mssv"]

    def __str__(self):
        return f"{self.mssv} - {self.get_full_name() or self.username}"
