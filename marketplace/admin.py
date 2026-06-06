from django.contrib import admin

from .models import CategoriaProduto, Produto


@admin.register(CategoriaProduto)
class CategoriaProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em")
    search_fields = ("nome",)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "produtor",
        "categoria",
        "quantidade_disponivel",
        "unidade_medida",
        "preco",
        "regiao",
        "status",
        "criado_em",
    )
    list_filter = ("categoria", "status", "regiao")
    search_fields = ("nome", "descricao", "produtor__nome_negocio")
    date_hierarchy = "criado_em"
