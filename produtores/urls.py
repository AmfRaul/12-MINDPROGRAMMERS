from django.urls import path

from . import views

app_name = "produtores"

urlpatterns = [
    path("meu-perfil/", views.meu_perfil_produtor, name="meu_perfil"),
]