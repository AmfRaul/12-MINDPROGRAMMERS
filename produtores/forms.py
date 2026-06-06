from django import forms

from .models import PerfilProdutor


class PerfilProdutorForm(forms.ModelForm):
    class Meta:
        model = PerfilProdutor
        fields = [
            "nome_negocio",
            "descricao",
            "cidade",
            "estado",
            "tipo_producao",
            "capacidade_producao",
            "contato_comercial",
            "exibir_contato",
            "foto",
        ]

        labels = {
            "nome_negocio": "Nome da propriedade ou negócio",
            "descricao": "Descrição",
            "cidade": "Cidade",
            "estado": "Estado",
            "tipo_producao": "Tipo de produção",
            "capacidade_producao": "Capacidade de produção",
            "contato_comercial": "Contato comercial",
            "exibir_contato": "Exibir contato comercial publicamente",
            "foto": "Foto do produtor ou propriedade",
        }

        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
        }