from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "categoria",
            "nome",
            "descricao",
            "quantidade_disponivel",
            "unidade_medida",
            "preco",
            "regiao",
            "data_disponibilidade",
            "data_entrega_estimada",
            "imagem",
            "status",
        ]

        labels = {
            "categoria": "Categoria",
            "nome": "Nome do produto",
            "descricao": "Descricao",
            "quantidade_disponivel": "Quantidade disponivel",
            "unidade_medida": "Unidade de medida",
            "preco": "Preco",
            "regiao": "Regiao",
            "data_disponibilidade": "Data de disponibilidade",
            "data_entrega_estimada": "Data estimada de entrega",
            "imagem": "Imagem do produto",
            "status": "Status",
        }

        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 4}),
            "data_disponibilidade": forms.DateInput(attrs={"type": "date"}),
            "data_entrega_estimada": forms.DateInput(attrs={"type": "date"}),
        }
