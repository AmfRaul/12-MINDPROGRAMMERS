from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.lista_produtos, name="lista_produtos"),
    path("meus-produtos/", views.meus_produtos, name="meus_produtos"),
    path("produtos/novo/", views.criar_produto, name="criar_produto"),
    path("produtos/<int:id>/editar/", views.editar_produto, name="editar_produto"),
    path("produtos/<int:id>/excluir/", views.excluir_produto, name="excluir_produto"),
    path("produtos/<int:id>/", views.detalhe_produto, name="detalhe_produto"),
]
