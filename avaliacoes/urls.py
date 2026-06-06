from django.urls import path

from . import views

app_name = "avaliacoes"

urlpatterns = [
    path("pedido/<int:pedido_id>/", views.avaliar_pedido, name="avaliar_pedido"),
]
