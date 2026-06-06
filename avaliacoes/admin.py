from django.contrib import admin

from .models import Avaliacao


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = (
        "pedido",
        "comprador",
        "nota",
        "criado_em",
    )
    list_filter = ("nota", "criado_em")
    search_fields = (
        "pedido__produto__nome",
        "comprador__username",
        "comentario",
    )
    date_hierarchy = "criado_em"
