from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PerfilProdutorForm
from .models import PerfilProdutor


@login_required
def meu_perfil_produtor(request):
    if not request.user.is_produtor:
        messages.error(request, "Apenas usuários produtores podem acessar essa página.")
        return redirect("dashboard:home")

    try:
        perfil = request.user.perfil_produtor
    except PerfilProdutor.DoesNotExist:
        perfil = None

    if request.method == "POST":
        form = PerfilProdutorForm(
            request.POST,
            request.FILES,
            instance=perfil,
        )

        if form.is_valid():
            perfil_produtor = form.save(commit=False)
            perfil_produtor.user = request.user
            perfil_produtor.save()

            messages.success(request, "Perfil do produtor salvo com sucesso.")
            return redirect("produtores:meu_perfil")
    else:
        form = PerfilProdutorForm(instance=perfil)

    return render(
        request,
        "produtores/meu_perfil.html",
        {
            "form": form,
            "perfil": perfil,
        },
    )