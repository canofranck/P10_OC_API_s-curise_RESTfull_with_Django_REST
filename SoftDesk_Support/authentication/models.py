from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class CustomUser(AbstractUser):

    username = models.CharField(max_length=255, unique=True)
    age = models.PositiveSmallIntegerField(
        default=15, validators=[MinValueValidator(15)], verbose_name=("age")
    )
    can_be_contacted = models.BooleanField(
        default=False, verbose_name=("contact consent")
    )
    can_data_be_shared = models.BooleanField(
        default=False, verbose_name=("share consent")
    )
    created_time = models.DateTimeField(
        auto_now_add=True, verbose_name=("created time")
    )

    def __str__(self):
        return self.username
