from django.contrib import admin

from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "produto",
        "comprador",
        "quantidade",
        "status",
        "criado_em",
    )
    list_filter = ("status", "criado_em")
    search_fields = (
        "produto__nome",
        "comprador__username",
        "comprador__email",
    )
    date_hierarchy = "criado_em"
