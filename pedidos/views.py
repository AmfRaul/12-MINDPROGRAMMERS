from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render

from marketplace.models import Produto

from .forms import AtualizarStatusPedidoForm, PedidoForm
from .models import Pedido


@login_required
def criar_pedido(request, produto_id):
    produto = get_object_or_404(
        Produto.objects.select_related("produtor", "produtor__user"),
        id=produto_id,
    )

    if request.user.is_produtor and produto.produtor.user == request.user:
        messages.error(request, "Voce nao pode criar pedido para o proprio produto.")
        return redirect("marketplace:detalhe_produto", id=produto.id)

    if request.method == "POST":
        form = PedidoForm(request.POST)

        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.comprador = request.user
            pedido.produto = produto
            pedido.save()

            messages.success(request, "Pedido enviado ao produtor.")
            return redirect("pedidos:meus_pedidos")
    else:
        form = PedidoForm()

    return render(
        request,
        "pedidos/form_pedido.html",
        {
            "form": form,
            "produto": produto,
        },
    )


@login_required
def meus_pedidos(request):
    pedidos_comprador = Pedido.objects.filter(comprador=request.user).select_related(
        "produto",
        "produto__produtor",
    )
    pedidos_produtor = Pedido.objects.none()

    if request.user.is_produtor:
        try:
            perfil = request.user.perfil_produtor
            pedidos_produtor = Pedido.objects.filter(produto__produtor=perfil).select_related(
                "comprador",
                "produto",
            )
        except ObjectDoesNotExist:
            pedidos_produtor = Pedido.objects.none()

    return render(
        request,
        "pedidos/meus_pedidos.html",
        {
            "pedidos_comprador": pedidos_comprador,
            "pedidos_produtor": pedidos_produtor,
        },
    )


@login_required
def atualizar_status_pedido(request, pedido_id):
    pedido = get_object_or_404(
        Pedido.objects.select_related("produto", "produto__produtor"),
        id=pedido_id,
    )

    if not request.user.is_produtor or pedido.produto.produtor.user != request.user:
        messages.error(request, "Voce nao tem permissao para atualizar este pedido.")
        return redirect("pedidos:meus_pedidos")

    if request.method == "POST":
        form = AtualizarStatusPedidoForm(request.POST, instance=pedido)

        if form.is_valid():
            form.save()
            messages.success(request, "Status do pedido atualizado.")
            return redirect("pedidos:meus_pedidos")
    else:
        form = AtualizarStatusPedidoForm(instance=pedido)

    return render(
        request,
        "pedidos/atualizar_status.html",
        {
            "form": form,
            "pedido": pedido,
        },
    )
