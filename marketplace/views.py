from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from produtores.models import PerfilProdutor

from .forms import ProdutoForm
from .models import CategoriaProduto, Produto


def lista_produtos(request):
    produtos = Produto.objects.select_related("categoria", "produtor")
    categorias = CategoriaProduto.objects.all()

    busca = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria", "").strip()
    regiao = request.GET.get("regiao", "").strip()
    status = request.GET.get("status", "").strip()

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    if categoria_id:
        produtos = produtos.filter(categoria_id=categoria_id)

    if regiao:
        produtos = produtos.filter(regiao__icontains=regiao)

    if status:
        produtos = produtos.filter(status=status)

    return render(
        request,
        "marketplace/lista_produtos.html",
        {
            "produtos": produtos,
            "categorias": categorias,
            "status_choices": Produto.StatusProduto.choices,
            "filtros": {
                "q": busca,
                "categoria": categoria_id,
                "regiao": regiao,
                "status": status,
            },
        },
    )


def detalhe_produto(request, id):
    produto = get_object_or_404(
        Produto.objects.select_related("categoria", "produtor", "produtor__user"),
        id=id,
    )

    return render(
        request,
        "marketplace/detalhe_produto.html",
        {
            "produto": produto,
        },
    )


@login_required
def criar_produto(request):
    if not request.user.is_produtor:
        messages.error(request, "Apenas usuarios produtores podem cadastrar produtos.")
        return redirect("marketplace:lista_produtos")

    try:
        perfil = request.user.perfil_produtor
    except PerfilProdutor.DoesNotExist:
        messages.warning(
            request,
            "Complete seu perfil de produtor antes de cadastrar produtos.",
        )
        return redirect("produtores:meu_perfil")

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)

        if form.is_valid():
            produto = form.save(commit=False)
            produto.produtor = perfil
            produto.save()

            messages.success(request, "Produto cadastrado com sucesso.")
            return redirect("marketplace:detalhe_produto", id=produto.id)
    else:
        form = ProdutoForm()

    return render(
        request,
        "marketplace/form_produto.html",
        {
            "form": form,
        },
    )
