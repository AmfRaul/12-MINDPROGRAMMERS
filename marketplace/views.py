from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
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
    avaliacoes = (
        produto.pedidos.filter(avaliacao__isnull=False)
        .select_related("avaliacao", "comprador")
        .order_by("-avaliacao__criado_em")
    )
    media_avaliacoes = avaliacoes.aggregate(media=Avg("avaliacao__nota"))["media"]

    return render(
        request,
        "marketplace/detalhe_produto.html",
        {
            "produto": produto,
            "avaliacoes": avaliacoes,
            "media_avaliacoes": media_avaliacoes,
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
            "titulo": "Novo produto",
            "botao": "Salvar produto",
        },
    )


@login_required
def meus_produtos(request):
    if not request.user.is_produtor:
        messages.error(request, "Apenas produtores podem acessar esta pagina.")
        return redirect("marketplace:lista_produtos")

    try:
        perfil = request.user.perfil_produtor
    except PerfilProdutor.DoesNotExist:
        messages.warning(request, "Complete seu perfil de produtor para gerenciar produtos.")
        return redirect("produtores:meu_perfil")

    produtos = Produto.objects.filter(produtor=perfil).select_related("categoria")

    return render(
        request,
        "marketplace/meus_produtos.html",
        {
            "produtos": produtos,
        },
    )


@login_required
def editar_produto(request, id):
    produto = get_object_or_404(
        Produto.objects.select_related("produtor"),
        id=id,
    )

    if produto.produtor.user != request.user:
        messages.error(request, "Voce nao tem permissao para editar este produto.")
        return redirect("marketplace:lista_produtos")

    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES, instance=produto)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso.")
            return redirect("marketplace:detalhe_produto", id=produto.id)
    else:
        form = ProdutoForm(instance=produto)

    return render(
        request,
        "marketplace/form_produto.html",
        {
            "form": form,
            "produto": produto,
            "titulo": "Editar produto",
            "botao": "Salvar alteracoes",
        },
    )


@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(
        Produto.objects.select_related("produtor"),
        id=id,
    )

    if produto.produtor.user != request.user:
        messages.error(request, "Voce nao tem permissao para excluir este produto.")
        return redirect("marketplace:lista_produtos")

    if request.method == "POST":
        produto.delete()
        messages.success(request, "Produto excluido com sucesso.")
        return redirect("marketplace:meus_produtos")

    return render(
        request,
        "marketplace/confirmar_exclusao_produto.html",
        {
            "produto": produto,
        },
    )
