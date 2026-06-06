from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CadastroUsuarioForm


def cadastro(request):
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard:home")
    else:
        form = CadastroUsuarioForm()

    return render(request, "accounts/cadastro.html", {"form": form})


@login_required
def perfil(request):
    return render(request, "accounts/perfil.html")