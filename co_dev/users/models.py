from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import admin


class User(AbstractUser):
    description = models.TextField()


admin.site.register(User)
