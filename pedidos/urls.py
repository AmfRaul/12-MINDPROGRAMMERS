from django.urls import path

from . import views

app_name = "pedidos"

urlpatterns = [
    path("", views.meus_pedidos, name="meus_pedidos"),
    path("produto/<int:produto_id>/novo/", views.criar_pedido, name="criar_pedido"),
    path("<int:pedido_id>/status/", views.atualizar_status_pedido, name="atualizar_status"),
]
