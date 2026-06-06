from django.conf import settings
from django.db import models

from marketplace.models import Produto


class Pedido(models.Model):
    class StatusPedido(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITO = "aceito", "Aceito"
        RECUSADO = "recusado", "Recusado"
        CONCLUIDO = "concluido", "Concluido"
        CANCELADO = "cancelado", "Cancelado"

    comprador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name="pedidos",
    )
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    mensagem = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusPedido.choices,
        default=StatusPedido.PENDENTE,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Pedido #{self.id} - {self.produto.nome}"

    @property
    def produtor(self):
        return self.produto.produtor

    @property
    def valor_estimado(self):
        return self.quantidade * self.produto.preco
