from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  # Çakışmayı önlemek için related_name ekledik
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',  # Çakışmayı önlemek için related_name ekledik
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_query_name='custom_user'
    )

    def __str__(self):
        return self.username
