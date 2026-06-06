from django import forms

from .models import Avaliacao


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = [
            "nota",
            "comentario",
        ]
        labels = {
            "nota": "Nota",
            "comentario": "Comentario",
        }
        widgets = {
            "comentario": forms.Textarea(attrs={"rows": 4}),
        }
