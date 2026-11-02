from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Project user model.

    Starts equivalent to Django's default user, but gives the project
    a stable place to add customer-specific fields later.
    """

    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["username"]
        constraints = [
            models.CheckConstraint(
                condition=~models.Q(email=""),
                name="user_email_must_not_be_empty",
            ),
        ]

    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="address",
    )
    house_name_or_number = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )
    street = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        default="",
    )
    postcode = models.CharField(
        max_length=10,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name_plural = "addresses"

    def __str__(self):
        parts = [
            self.house_name_or_number,
            self.street,
            self.city,
            self.postcode,
        ]

        return ", ".join(part for part in parts if part)