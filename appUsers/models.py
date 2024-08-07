from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    dietary_preferences = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


