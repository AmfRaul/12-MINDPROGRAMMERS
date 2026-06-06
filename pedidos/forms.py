from django import forms

from .models import Pedido


class PedidoForm(forms.ModelForm):
    def __init__(self, *args, produto=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.produto = produto

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

    def clean_quantidade(self):
        quantidade = self.cleaned_data.get("quantidade")

        if quantidade is None:
            return quantidade

        if quantidade <= 0:
            raise forms.ValidationError("Informe uma quantidade maior que zero.")

        if self.produto and quantidade > self.produto.quantidade_disponivel:
            raise forms.ValidationError(
                "A quantidade solicitada nao pode ser maior que a disponivel."
            )

        return quantidade
