from django.contrib.auth.models import AbstractUser
from django.db import models
from Client.validators import validate_itn


class ExtendedUser(AbstractUser):
    ITN = models.CharField(unique=True, verbose_name="ИНН", validators=[validate_itn], max_length=12, null=True, blank=True, db_index=True)
    balance = models.DecimalField(decimal_places=2, max_digits=10, verbose_name="Баланс", default=0.00)

    class Meta:
        verbose_name = "Пользователя"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.ITN:
            return f"{self.username}: {self.ITN}"
        else:
            return f"{self.username}: ИНН не указан."
