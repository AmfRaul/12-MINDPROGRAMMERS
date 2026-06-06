from django.contrib import admin

from .models import PerfilProdutor


@admin.register(PerfilProdutor)
class PerfilProdutorAdmin(admin.ModelAdmin):
    list_display = [
        "nome_negocio",
        "user",
        "cidade",
        "estado",
        "tipo_producao",
        "criado_em",
    ]

    list_filter = [
        "estado",
        "tipo_producao",
        "criado_em",
    ]

    search_fields = [
        "nome_negocio",
        "user__username",
        "cidade",
        "tipo_producao",
    ]