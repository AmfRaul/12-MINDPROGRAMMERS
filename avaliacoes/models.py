from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from pedidos.models import Pedido


class Avaliacao(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.CASCADE,
        related_name="avaliacao",
    )
    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="avaliacoes_feitas",
    )
    nota = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ],
    )
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.nota}/5 - {self.pedido.produto.nome}"
