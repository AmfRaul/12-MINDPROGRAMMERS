from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.lista_produtos, name="lista_produtos"),
    path("produtos/novo/", views.criar_produto, name="criar_produto"),
    path("produtos/<int:id>/", views.detalhe_produto, name="detalhe_produto"),
]
