from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = [
            "quantidade",
            "mensagem",
        ]
        labels = {
            "quantidade": "Quantidade desejada",
            "mensagem": "Mensagem para o produtor",
        }
        widgets = {
            "mensagem": forms.Textarea(attrs={"rows": 4}),
        }


class AtualizarStatusPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["status"]
        labels = {
            "status": "Status do pedido",
        }
