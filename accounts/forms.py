from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "telefone",
            "tipo_conta",
            "password1",
            "password2",
        ]

        labels = {
            "username": "Nome de usuario",
            "telefone": "Telefone",
            "tipo_conta": "Tipo de conta",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ja existe uma conta com este e-mail.")

        return email
