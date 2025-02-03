from django.contrib.auth.models import AbstractUser
from django.db import models

from django_countries.fields import CountryField

class User(AbstractUser):
		# Multiple Choice
    class LanguageChoices(models.TextChoices):
        KOREAN = ("ko", "Korean")
        ENGLISH = ("en", "English")

    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    language = models.CharField(
        max_length=10,
        choices=LanguageChoices.choices,
        default="en",
    )

    gender = models.CharField(
        max_length=10,
        choices=GenderChoices.choices,
        blank=True,
        null=True,
    )

    age = models.IntegerField(
        default=0,
    )

    country = CountryField(
        blank_label="(select country)",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.username
