from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='images/user/', null=True, blank=True)
    email = models.EmailField(
                                   max_length=150,
                                   unique=True,
                                   validators=[validate_email],
                                   error_messages={
                                       "unique": ("A user with that email already exists."),
                                   }, )
