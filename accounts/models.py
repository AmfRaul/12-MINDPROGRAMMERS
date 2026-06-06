from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class TipoConta(models.TextChoices):
        PRODUTOR = "produtor", "Produtor rural"
        COMPRADOR = "comprador", "Comprador"
        INVESTIDOR = "investidor", "Investidor"

    tipo_conta = models.CharField(
        max_length=20,
        choices=TipoConta.choices,
        default=TipoConta.COMPRADOR,
    )

    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.username

    @property
    def is_produtor(self):
        return self.tipo_conta == self.TipoConta.PRODUTOR

    @property
    def is_comprador(self):
        return self.tipo_conta == self.TipoConta.COMPRADOR

    @property
    def is_investidor(self):
        return self.tipo_conta == self.TipoConta.INVESTIDOR