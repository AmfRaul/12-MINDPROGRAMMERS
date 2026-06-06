from django.conf import settings
from django.db import models


class PerfilProdutor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil_produtor",
    )

    nome_negocio = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)

    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    tipo_producao = models.CharField(
        max_length=150,
        help_text="Ex: hortaliças, frutas, leite, grãos, orgânicos etc.",
    )

    capacidade_producao = models.CharField(
        max_length=150,
        blank=True,
        help_text="Ex: 500 kg por semana, 2 toneladas por mês etc.",
    )

    contato_comercial = models.CharField(max_length=100, blank=True)
    exibir_contato = models.BooleanField(default=True)

    foto = models.ImageField(
        upload_to="produtores/",
        blank=True,
        null=True,
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Perfil do produtor"
        verbose_name_plural = "Perfis dos produtores"

    def __str__(self):
        return self.nome_negocio