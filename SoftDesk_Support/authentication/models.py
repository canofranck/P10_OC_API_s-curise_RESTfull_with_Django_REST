from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator


class CustomUser(AbstractUser):
    """
    Custom user model extending the AbstractUser.
    """

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
        """
        Returns the string representation of the user.

        :return: Username of the user.
        """
        return self.username
