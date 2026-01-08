from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuario personalizado extendiendo AbstractUser.
    Preparado para autenticación y pagos (Stripe).
    """

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    stripe_customer_id = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self):
        return self.username