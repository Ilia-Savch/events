from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users.managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField("Почта", unique=True)
    phone_number = PhoneNumberField(
        "Телефон", unique=True, null=True, blank=True)
    about = models.CharField("Обо мне", max_length=1000, null=True, blank=True)
    ava = models.ImageField(
        "Аватарка", upload_to="ava/%Y/%m/%d", null=True, blank=True)
    is_organizer = models.BooleanField('Организатор',  null=True, blank=True,)

    USERNAME_FIELD = "username"

    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return f"{self.username}({self.pk})"
