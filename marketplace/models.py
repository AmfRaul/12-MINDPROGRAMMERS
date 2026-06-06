from django.db import models

from produtores.models import PerfilProdutor


class CategoriaProduto(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Categoria de produto"
        verbose_name_plural = "Categorias de produtos"
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Produto(models.Model):
    class StatusProduto(models.TextChoices):
        DISPONIVEL = "disponivel", "Disponivel"
        INDISPONIVEL = "indisponivel", "Indisponivel"
        SOB_ENCOMENDA = "sob_encomenda", "Sob encomenda"

    produtor = models.ForeignKey(
        PerfilProdutor,
        on_delete=models.CASCADE,
        related_name="produtos",
    )
    categoria = models.ForeignKey(
        CategoriaProduto,
        on_delete=models.PROTECT,
        related_name="produtos",
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    quantidade_disponivel = models.DecimalField(max_digits=10, decimal_places=2)
    unidade_medida = models.CharField(max_length=30)
    preco = models.DecimalField("preco", max_digits=10, decimal_places=2)
    regiao = models.CharField("regiao", max_length=150)
    data_disponibilidade = models.DateField()
    data_entrega_estimada = models.DateField(blank=True, null=True)
    imagem = models.ImageField(
        upload_to="marketplace/produtos/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=StatusProduto.choices,
        default=StatusProduto.DISPONIVEL,
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ["-criado_em"]

    def __str__(self):
        return self.nome
